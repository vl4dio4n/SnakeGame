import pygame
import sys
import random
from pygame.math import Vector2
import os

class Food():
    def __init__(self):
        self.x = random.randint(0, cell_num - 1)
        self.y = random.randint(0, cell_num - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_food(self):
        food_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(apple, food_rect)

class Snake():
    def __init__(self):
        self.body = [Vector2(5, 10)]
        self.direction = Vector2(1, 0)
        self.body_components = {}
        for img in os.listdir('Graphics\\Snake'):
            self.body_components[img] = pygame.image.load('Graphics\\Snake' + '\\' + img).convert_alpha()
            self.body_components[img] = pygame.transform.scale(self.body_components[img] , (cell_size, cell_size))
        self.crunch_sound = pygame.mixer.Sound('Sound\\Sound_crunch.wav')

    def get_tail_dir(self):
        if self.body[-1] + Vector2(0, -1) == self.body[-2]:
            return 'down'
        if self.body[-1] + Vector2(1, 0) == self.body[-2]:
            return 'left'
        if self.body[-1] + Vector2(0, 1) == self.body[-2]:
            return 'up'
        return 'right'

    def draw_snake(self):
        for index, cell in enumerate(self.body):
            cell_rect = pygame.Rect(cell.x * cell_size, cell.y * cell_size, cell_size, cell_size)
            if index == 0:
                if self.direction == Vector2(0, -1):
                    screen.blit(self.body_components['head_up.png'], cell_rect)
                elif self.direction == Vector2(1, 0):
                    screen.blit(self.body_components['head_right.png'], cell_rect)
                elif self.direction == Vector2(0, 1):
                    screen.blit(self.body_components['head_down.png'], cell_rect)
                elif self.direction == Vector2(-1, 0):
                    screen.blit(self.body_components['head_left.png'], cell_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.body_components[f'tail_{self.get_tail_dir()}.png'], cell_rect)
            else:
                if self.body[index + 1] + Vector2(2, 0) == self.body[index - 1] or self.body[index + 1] - Vector2(2, 0) == self.body[index - 1]:
                    screen.blit(self.body_components['body_horizontal.png'], cell_rect)
                elif self.body[index + 1] + Vector2(0, 2) == self.body[index - 1] or self.body[index + 1] - Vector2(0, 2) == self.body[index - 1]:
                    screen.blit(self.body_components['body_vertical.png'], cell_rect)
                elif self.body[index] + Vector2(0, -1) == self.body[index + 1] and self.body[index] + Vector2(1, 0) == self.body[index - 1]:
                     screen.blit(self.body_components['body_tr.png'], cell_rect)
                elif self.body[index] + Vector2(1, 0) == self.body[index + 1] and self.body[index] + Vector2(0, -1) == self.body[index - 1]:
                     screen.blit(self.body_components['body_tr.png'], cell_rect)
                elif self.body[index] + Vector2(-1, 0) == self.body[index + 1] and self.body[index] + Vector2(0, -1) == self.body[index - 1]:
                     screen.blit(self.body_components['body_tl.png'], cell_rect)
                elif self.body[index] + Vector2(0, -1) == self.body[index + 1] and self.body[index] + Vector2(-1, 0) == self.body[index - 1]:
                     screen.blit(self.body_components['body_tl.png'], cell_rect)
                elif self.body[index] + Vector2(-1, 0) == self.body[index + 1] and self.body[index] + Vector2(0, 1) == self.body[index - 1]:
                     screen.blit(self.body_components['body_bl.png'], cell_rect)
                elif self.body[index] + Vector2(0, 1) == self.body[index + 1] and self.body[index] + Vector2(-1, 0) == self.body[index - 1]:
                     screen.blit(self.body_components['body_bl.png'], cell_rect)
                elif self.body[index] + Vector2(0, 1) == self.body[index + 1] and self.body[index] + Vector2(1, 0) == self.body[index - 1]:
                     screen.blit(self.body_components['body_br.png'], cell_rect)
                else:
                     screen.blit(self.body_components['body_br.png'], cell_rect)

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, self.body[0] + self.direction)
        self.body = body_copy
    
    def add_cell(self):
        self.body.append(self.body[-1])
    
    def play_crunch_sound(self):
        self.crunch_sound.play()

class Game():
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        while self.food.pos in self.snake.body:
            self.food = Food() 
        self.dark_grass = pygame.image.load('Graphics\\Grass\\dark_grass.jpg').convert_alpha()
        self.dark_grass = pygame.transform.scale(self.dark_grass, (cell_size, cell_size))
        self.light_grass = pygame.image.load('Graphics\\Grass\\light_grass.jpg').convert_alpha()
        self.light_grass = pygame.transform.scale(self.light_grass, (cell_size, cell_size))
        self.game_on = False
    
    def update(self):
        self.snake.move_snake()
        self.check_eaten()
        self.check_collision()

    def draw_elements(self):
        self.draw_grass()
        self.food.draw_food()
        self.snake.draw_snake()
        self.draw_score()
    
    def check_eaten(self):
        if self.food.pos == self.snake.body[0]:
            self.snake.add_cell()
            self.snake.play_crunch_sound()
            self.food = Food()
            while self.food.pos in self.snake.body:
                self.food = Food() 
    
    def check_collision(self):
        if (self.snake.body[0] in self.snake.body[1:] and len(self.snake.body) > 2) or (not 0 <= self.snake.body[0].x < cell_num) or (not 0 <= self.snake.body[0].y < cell_num):
            self.game_over()

    def game_over(self):
        f = open('Highscore.txt', mode = 'r')
        highscore = int(f.read())
        f.close()
        if len(self.snake.body) > highscore:
            highscore = len(self.snake.body)
            f = open('Highscore.txt', mode = 'w')
            f.write(str(highscore))
            f.close()
        self.game_on = False
        self.snake = Snake()
        self.food = Food()
        while self.food.pos in self.snake.body:
            self.food = Food() 

    def draw_grass(self):
        for col in range(cell_num):
            for row in range(cell_num):
                grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                if (col + row) % 2:
                    screen.blit(self.dark_grass, grass_rect)
                else:
                    screen.blit(self.light_grass, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body))
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = cell_size * cell_num - 40
        score_y = cell_size * cell_num - 40
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, score_rect.top, apple_rect.width + score_rect.width + 10, score_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)  
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

        f = open('Highscore.txt', mode = "r")
        content = f.read()
        f.close()
        text = 'HIGH ' + content
        highscore_font = pygame.font.Font('Font\\Shadow of the Deads.ttf', 25)
        highscore_surface = highscore_font.render(text, True, (50, 0, 0))
        highscore_x = 10
        highscore_y = cell_size * cell_num - 10
        highscore_rect = highscore_surface.get_rect(bottomleft = (highscore_x, highscore_y))
        screen.blit(highscore_surface, highscore_rect)


class Pause():
    def __init__(self):
        self.text = 'PAUSE'
        self.pause_font = pygame.font.Font('Font\\Shadow of the Deads.ttf', 15)
        self.pause_surface = self.pause_font.render(self.text, True, (56, 74, 12))
        self.pause_x = cell_num * cell_size - 45
        self.pause_y = 20
        self.pause_rect = self.pause_surface.get_rect(center = (self.pause_x, self.pause_y))
        
    def check_touch(self, x, y):
        if self.pause_rect.left <= x <= self.pause_rect.right and self.pause_rect.top <= y <= self.pause_rect.bottom:
            return True
        return False

    def draw_button(self, touch):
        if touch:
            color = (167, 70, 61)
        else:
            color = (167, 209, 61)
        pygame.draw.rect(screen, color, self.pause_rect)
        screen.blit(self.pause_surface, self.pause_rect)
        pygame.draw.rect(screen, (56, 74, 12), self.pause_rect, 2)

class Mute():
    def __init__(self):
        self.text = 'MUTE'
        self.mute_font = pygame.font.Font('Font\\Shadow of the Deads.ttf', 15)
        self.mute_surface = self.mute_font.render(self.text, True, (56, 74, 12))
        self.mute_x = 10
        self.mute_y = 10
        self.mute_rect = self.mute_surface.get_rect(topleft = (self.mute_x, self.mute_y))
    
    def check_touch(self, x, y):
        if self.mute_rect.left <= x <= self.mute_rect.right and self.mute_rect.top <= y <= self.mute_rect.bottom:
            return True
        return False
    
    def draw_button(self, touch):
        if touch:
            color = (167, 70, 61)
        else:
            color = (167, 209, 61)
        pygame.draw.rect(screen, color, self.mute_rect)
        screen.blit(self.mute_surface, self.mute_rect)
        pygame.draw.rect(screen, (56, 74, 12), self.mute_rect, 2)

class Resume():
    def __init__(self):
        self.text = 'RESUME'
        self.resume_font = pygame.font.Font('Font\\Shadow of the Deads.ttf', 50)
        self.resume_surface = self.resume_font.render(self.text, True, (100, 20, 80))
        self.resume_x = 300
        self.resume_y = 300
        self.resume_rect = self.resume_surface.get_rect(center = (self.resume_x, self.resume_y))

    def check_touch(self, x, y):
        if self.resume_rect.left <= x <= self.resume_rect.right and self.resume_rect.top <= y <= self.resume_rect.bottom:
            return True
        return False
    
    def draw_button(self, touch):
        if touch:
            self.resume_surface = self.resume_font.render(self.text, True, (200, 200, 180))
        else:
            self.resume_surface = self.resume_font.render(self.text, True, (100, 20, 80))
        screen.blit(self.resume_surface, self.resume_rect)

class Start():
    def __init__(self):
        self.text = 'GO!'
        self.start_font = pygame.font.Font('Font\\Shadow of the Deads.ttf', 30)
        self.start_surface = self.start_font.render(self.text, True, (100, 20, 80))
        self.start_x = 300
        self.start_y = 150
        self.start_rect = self.start_surface.get_rect(center = (self.start_x, self.start_y))

    def check_touch(self, x, y):
        if self.start_rect.left <= x <= self.start_rect.right and self.start_rect.top <= y <= self.start_rect.bottom:
            return True
        return False
    
    def draw_button(self, touch):
        if touch:
            self.start_surface = self.start_font.render(self.text, True, (200, 200, 180))
        else:
            self.start_surface = self.start_font.render(self.text, True, (100, 20, 80))
        screen.blit(self.start_surface, self.start_rect)

class Music():
    def __init__(self):
        self.text = 'MUSIC'
        self.music_font = pygame.font.Font('Font\\Shadow of the Deads.ttf', 30)
        self.music_surface = self.music_font.render(self.text, True, (100, 20, 80))
        self.music_x = 300
        self.music_y = 225
        self.music_rect = self.music_surface.get_rect(center = (self.music_x, self.music_y))

    def check_touch(self, x, y):
        if self.music_rect.left <= x <= self.music_rect.right and self.music_rect.top <= y <= self.music_rect.bottom:
            return True
        return False
    
    def draw_button(self, touch):
        if touch:
            self.music_surface = self.music_font.render(self.text, True, (200, 200, 180))
        else:
            self.music_surface = self.music_font.render(self.text, True, (100, 20, 80))
        screen.blit(self.music_surface, self.music_rect)

class Song():
    def __init__(self, song_name, x):
        song_name = song_name.upper()
        self.text = song_name[0:len(song_name) - 4]
        self.song_font = pygame.font.Font('Font\\Shadow of the Deads.ttf', 15)
        self.song_surface = self.song_font.render(self.text, True, (100, 20, 80))
        self.song_x = 300
        self.song_y = 150 + 50 * x
        self.song_rect = self.song_surface.get_rect(center = (self.song_x, self.song_y))

    def check_touch(self, x, y):
        if self.song_rect.left <= x <= self.song_rect.right and self.song_rect.top <= y <= self.song_rect.bottom:
            return True
        return False
    
    def draw_button(self, touch):
        if touch:
            self.song_surface = self.song_font.render(self.text, True, (200, 200, 180))
        else:
            self.song_surface = self.song_font.render(self.text, True, (100, 20, 80))
        screen.blit(self.song_surface, self.song_rect)

class Back():
    def __init__(self):
        self.text = 'GO BACK'
        self.back_font = pygame.font.Font('Font\\Shadow of the Deads.ttf', 30)
        self.back_surface = self.back_font.render(self.text, True, (100, 20, 80))
        self.back_x = 300
        self.back_y = 500
        self.back_rect = self.back_surface.get_rect(center = (self.back_x, self.back_y))

    def check_touch(self, x, y):
        if self.back_rect.left <= x <= self.back_rect.right and self.back_rect.top <= y <= self.back_rect.bottom:
            return True
        return False
    
    def draw_button(self, touch):
        if touch:
            self.back_surface = self.back_font.render(self.text, True, (200, 200, 180))
        else:
            self.back_surface = self.back_font.render(self.text, True, (100, 20, 80))
        screen.blit(self.back_surface, self.back_rect)

class Quit():
    def __init__(self):
        self.text = 'QUIT'
        self.quit_font = pygame.font.Font('Font\\Shadow of the Deads.ttf', 30)
        self.quit_surface = self.quit_font.render(self.text, True, (100, 20, 80))
        self.quit_x = 300
        self.quit_y = 300
        self.quit_rect = self.quit_surface.get_rect(center = (self.quit_x, self.quit_y))

    def check_touch(self, x, y):
        if self.quit_rect.left <= x <= self.quit_rect.right and self.quit_rect.top <= y <= self.quit_rect.bottom:
            return True
        return False
    
    def draw_button(self, touch):
        if touch:
            self.quit_surface = self.quit_font.render(self.text, True, (200, 200, 180))
        else:
            self.quit_surface = self.quit_font.render(self.text, True, (100, 20, 80))
        screen.blit(self.quit_surface, self.quit_rect)  
        

cell_size = 30
cell_num = 20

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen = pygame.display.set_mode((cell_size * cell_num, cell_size * cell_num))
clock = pygame.time.Clock()

pygame.mixer.music.load('Music\\punch deck brazilian street fight.mp3')
pygame.mixer.music.play(-1)

apple = pygame.image.load('Graphics\\Apple\\apple.png').convert_alpha()
apple = pygame.transform.scale(apple, (cell_size, cell_size))

game_font = pygame.font.Font('Font\\Shadow of the Deads.ttf', 25)

game_obj = Game()
pause_button = Pause()
mute_button = Mute()
resume_button = Resume()
start_button = Start()
music_button = Music()
back_button = Back()
quit_button = Quit()
playlist = []
for index, songfile in enumerate(os.listdir('Music')):
    playlist.append(Song(songfile, index))

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

game_pause = True
game_mute = False
music_button_pressed = False

while True:
    chosen_song = -1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_obj.game_on:
            if event.type == SCREEN_UPDATE and game_pause == False:
                game_obj.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game_obj.snake.direction != Vector2(0, 1):
                    game_obj.snake.direction = Vector2(0, -1) 
                    game_pause = False
                if event.key == pygame.K_RIGHT and game_obj.snake.direction != Vector2(-1, 0):
                    game_obj.snake.direction = Vector2(1, 0)
                    game_pause = False
                if event.key == pygame.K_DOWN and game_obj.snake.direction != Vector2(0, -1):
                    game_obj.snake.direction = Vector2(0, 1)
                    game_pause = False
                if event.key == pygame.K_LEFT and game_obj.snake.direction != Vector2(1, 0):
                    game_obj.snake.direction = Vector2(-1, 0)
                    game_pause = False
                if event.key == pygame.K_p:
                    game_pause = not game_pause
                if event.key == pygame.K_m:
                    game_mute = not game_mute
                    if game_mute:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.check_touch(mouse[0], mouse[1]):
                    game_pause = not game_pause
                if resume_button.check_touch(mouse[0], mouse[1]):
                    game_pause = False
                if mute_button.check_touch(mouse[0], mouse[1]):
                    game_mute = not game_mute
                    if game_mute:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not music_button_pressed:
                    if start_button.check_touch(mouse[0], mouse[1]):
                        game_obj.game_on = True
                        game_pause = False
                    if mute_button.check_touch(mouse[0], mouse[1]):
                        game_mute = not game_mute
                        if game_mute:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                    if music_button.check_touch(mouse[0], mouse[1]):
                        music_button_pressed = True 
                    if quit_button.check_touch(mouse[0], mouse[1]):
                        pygame.quit()
                        sys.exit()
                else:
                    for index, song_button in enumerate(playlist):           
                        if song_button.check_touch(mouse[0], mouse[1]):
                            chosen_song = index
                            break
                    if back_button.check_touch(mouse[0], mouse[1]):
                        music_button_pressed = False
    
    if music_button_pressed and chosen_song != -1:
        pygame.mixer.music.unload()
        pygame.mixer.music.load('Music\\' + os.listdir('Music')[index])
        pygame.mixer.music.play(-1)

    mouse = pygame.mouse.get_pos()
    screen.fill((175, 215, 70))
    game_obj.draw_elements()
    pause_button.draw_button(pause_button.check_touch(mouse[0], mouse[1]))
    mute_button.draw_button(mute_button.check_touch(mouse[0], mouse[1]))
    if game_pause and game_obj.game_on:
        resume_button.draw_button(resume_button.check_touch(mouse[0], mouse[1]))
    elif not game_obj.game_on:
        if not music_button_pressed:
            start_button.draw_button(start_button.check_touch(mouse[0], mouse[1]))
            music_button.draw_button(music_button.check_touch(mouse[0], mouse[1]))
            quit_button.draw_button(quit_button.check_touch(mouse[0], mouse[1]))
        else:
            back_button.draw_button(back_button.check_touch(mouse[0], mouse[1]))
            for song_button in playlist:
                song_button.draw_button(song_button.check_touch(mouse[0], mouse[1]))
    pygame.display.update()
    clock.tick(60)