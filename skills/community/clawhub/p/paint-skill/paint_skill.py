#!/usr/bin/env python3
"""
OpenClaw Paint Skill - 公園散步圖
生成男孩、小貓、小狗在公園散步的圖片
"""

from PIL import Image, ImageDraw
import os

def draw_park_scene():
    width, height = 800, 600
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    
    # 天空（淺藍色）
    draw.rectangle([0, 0, width, 350], fill="#87CEEB")
    
    # 太陽（黃色）
    draw.ellipse([650, 30, 720, 100], fill="#FFD700", outline="#FFA500")
    # 太陽光芒
    for i in range(8):
        angle = i * 45
        x1 = 685 + 40 * (angle % 360) / 180 * 3.14159
        y1 = 65 + 40 * (angle % 360) / 180 * 3.14159
        draw.line([685, 65, x1, y1], fill="#FFD700", width=2)
    
    # 草地（綠色）
    draw.rectangle([0, 350, width, height], fill="#90EE90")
    
    # 遠處的樹（種在草地上）
    draw.rectangle([50, 250, 70, 350], fill="#8B4513")  # 樹幹（底部接地）
    draw.ellipse([30, 200, 90, 260], fill="#228B22")    # 樹冠
    draw.ellipse([60, 180, 100, 230], fill="#32CD32")    # 樹冠上層
    
    draw.rectangle([550, 280, 570, 350], fill="#8B4513")  # 樹幹
    draw.ellipse([530, 230, 590, 290], fill="#228B22")   # 樹冠
    

    
    # 公園小路（棕色）
    draw.polygon([(300, 350), (500, 350), (600, 600), (200, 600)], fill="#DEB887")
    
    # 小男孩
    # 身體
    draw.ellipse([330, 400, 380, 450], fill="#FF6B6B")  # 紅色衣服
    # 頭
    draw.ellipse([340, 360, 380, 400], fill="#FFDAB9")  # 臉
    # 頭髮
    draw.ellipse([345, 355, 375, 375], fill="#8B4513")
    # 眼睛
    draw.ellipse([348, 375, 352, 379], fill="black")
    draw.ellipse([368, 375, 372, 379], fill="black")
    # 嘴巴
    draw.arc([350, 385, 370, 395], start=0, end=180, fill="black", width=2)
    # 手臂
    draw.line([335, 420, 310, 450], fill="#FFDAB9", width=8)  # 左手
    draw.line([375, 420, 400, 450], fill="#FFDAB9", width=8)  # 右手
    # 腿
    draw.line([345, 450, 340, 500], fill="#4169E1", width=10)  # 左腳
    draw.line([365, 450, 370, 500], fill="#4169E1", width=10)  # 右腳
    
    # 小貓（橘色虎斑貓）
    # 身體
    draw.ellipse([420, 440, 470, 480], fill="#FF8C00")
    # 頭
    draw.ellipse([450, 420, 480, 450], fill="#FF8C00")
    # 耳朵
    draw.polygon([(452, 420), (458, 405), (464, 420)], fill="#FF8C00")
    draw.polygon([(468, 420), (474, 405), (480, 420)], fill="#FF8C00")
    # 眼睛
    draw.ellipse([455, 428, 458, 432], fill="black")
    draw.ellipse([470, 428, 473, 432], fill="black")
    # 鼻子
    draw.polygon([(462, 438), (466, 438), (464, 442)], fill="pink")
    # 尾巴
    draw.line([420, 450, 400, 430], fill="#FF8C00", width=5)
    
    # 小狗（棕色小狗）
    # 身體
    draw.ellipse([260, 450, 320, 490], fill="#8B4513")
    # 頭
    draw.ellipse([230, 430, 270, 470], fill="#8B4513")
    # 耳朵（下垂）
    draw.ellipse([225, 440, 240, 460], fill="#654321")
    draw.ellipse([260, 440, 275, 460], fill="#654321")
    # 眼睛
    draw.ellipse([238, 440, 243, 445], fill="black")
    draw.ellipse([255, 440, 260, 445], fill="black")
    # 鼻子
    draw.ellipse([245, 458, 255, 465], fill="black")
    # 舌頭
    draw.ellipse([248, 465, 255, 475], fill="pink")
    # 尾巴
    draw.line([320, 460, 340, 445], fill="#8B4513", width=6)
    
    # 雲朵
    draw.ellipse([100, 50, 180, 100], fill="white")
    draw.ellipse([130, 30, 200, 80], fill="white")
    draw.ellipse([160, 50, 220, 90], fill="white")
    
    draw.ellipse([400, 80, 480, 130], fill="white")
    draw.ellipse([430, 60, 500, 110], fill="white")
    
    # 花朵裝飾
    colors = ["#FF69B4", "#FF1493", "#DA70D6", "#FFD700"]
    for i, (x, y, c) in enumerate([(100, 520, colors[0]), (150, 550, colors[1]), (600, 520, colors[2]), (650, 550, colors[3])]):
        draw.ellipse([x-10, y-10, x+10, y+10], fill=c)
        draw.ellipse([x, y-12, x+8, y-4], fill="yellow")
    
    # 儲存
    filename = "/Users/m1/.openclaw/workspace/openclaw_drawing.png"
    image.save(filename)
    print(f"✅ 公園散步圖已儲存: {filename}")
    return filename

if __name__ == "__main__":
    draw_park_scene()