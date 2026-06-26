#!/usr/bin/env python3
"""
儿童活动书封面PDF生成器 - KDP用
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# 6x9英寸 @ 300 DPI = 1800 x 2700 像素 (仅封面部分)
COVER_WIDTH = 1800
COVER_HEIGHT = 2700

# 颜色方案
COLORS = {
    "bg_gradient_top": (255, 183, 178),
    "bg_gradient_bottom": (255, 223, 186),
    "title_text": (70, 70, 100),
    "subtitle_text": (100, 100, 130),
    "accent_pink": (255, 107, 157),
    "accent_blue": (100, 200, 220),
    "accent_yellow": (255, 220, 100),
    "accent_green": (150, 230, 180),
    "white": (255, 255, 255),
}

def create_gradient_background(width, height, color1, color2):
    """创建渐变背景"""
    img = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img

def draw_star(draw, cx, cy, size, color, fill=True):
    """绘制星星"""
    points = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        radius = size if i % 2 == 0 else size / 2
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    
    if fill:
        draw.polygon(points, fill=color)
    else:
        draw.polygon(points, outline=color, width=3)

def draw_circle_pattern(draw, x, y, radius, color):
    """绘制圆圈装饰"""
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                 outline=color, width=8)

def draw_cloud(draw, x, y, size, color):
    """绘制云朵"""
    r = size
    draw.ellipse([x-r, y-r*0.5, x+r, y+r*0.5], fill=color)
    draw.ellipse([x-r*1.2, y, x, y+r], fill=color)
    draw.ellipse([x, y, x+r*1.2, y+r], fill=color)

def create_activity_book_cover_pdf(title, subtitle, output_path):
    """创建儿童活动书封面PDF"""
    
    # 创建渐变背景
    img = create_gradient_background(
        COVER_WIDTH, COVER_HEIGHT,
        COLORS["bg_gradient_top"],
        COLORS["bg_gradient_bottom"]
    )
    draw = ImageDraw.Draw(img)
    
    # 绘制装饰边框
    border_width = 40
    draw.rectangle(
        [border_width, border_width, 
         COVER_WIDTH-border_width, COVER_HEIGHT-border_width],
        outline=COLORS["white"], width=15
    )
    draw.rectangle(
        [border_width+20, border_width+20, 
         COVER_WIDTH-border_width-20, COVER_HEIGHT-border_width-20],
        outline=COLORS["accent_pink"], width=8
    )
    
    # 加载字体
    try:
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "C:/Windows/Fonts/arialbd.ttf",
        ]
        
        title_font = None
        subtitle_font = None
        small_font = None
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                title_font = ImageFont.truetype(font_path, 140)
                subtitle_font = ImageFont.truetype(font_path, 60)
                small_font = ImageFont.truetype(font_path, 50)
                break
        
        if title_font is None:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
            
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # 绘制标题
    title_y = 450
    
    words = title.split()
    if len(words) <= 3:
        bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = bbox[2] - bbox[0]
        draw.text(
            ((COVER_WIDTH - title_width) // 2, title_y),
            title,
            font=title_font,
            fill=COLORS["title_text"]
        )
    else:
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
        
        bbox1 = draw.textbbox((0, 0), line1, font=title_font)
        bbox2 = draw.textbbox((0, 0), line2, font=title_font)
        
        draw.text(
            ((COVER_WIDTH - (bbox1[2]-bbox1[0])) // 2, title_y),
            line1,
            font=title_font,
            fill=COLORS["title_text"]
        )
        draw.text(
            ((COVER_WIDTH - (bbox2[2]-bbox2[0])) // 2, title_y + 160),
            line2,
            font=title_font,
            fill=COLORS["title_text"]
        )
        title_y = title_y + 160
    
    # 绘制副标题
    subtitle_y = title_y + 200
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    draw.text(
        ((COVER_WIDTH - subtitle_width) // 2, subtitle_y),
        subtitle,
        font=subtitle_font,
        fill=COLORS["subtitle_text"]
    )
    
    # 绘制装饰元素 - 星星
    draw_star(draw, 250, 800, 80, COLORS["accent_yellow"])
    draw_star(draw, COVER_WIDTH-250, 850, 70, COLORS["accent_yellow"])
    draw_star(draw, 180, 1400, 60, COLORS["accent_green"])
    draw_star(draw, COVER_WIDTH-180, 1350, 65, COLORS["accent_green"])
    
    # 绘制装饰元素 - 圆圈
    draw_circle_pattern(draw, 300, 2000, 100, COLORS["accent_blue"])
    draw_circle_pattern(draw, COVER_WIDTH-300, 2100, 90, COLORS["accent_pink"])
    draw_circle_pattern(draw, 200, 1200, 70, COLORS["accent_blue"])
    draw_circle_pattern(draw, COVER_WIDTH-200, 1800, 80, COLORS["accent_green"])
    
    # 绘制装饰云朵 - 往下移动，不要挡住标题
    draw_cloud(draw, 400, 1100, 80, COLORS["white"])
    draw_cloud(draw, COVER_WIDTH-350, 1150, 70, COLORS["white"])
    
    # 绘制活动内容图标区域
    icon_y = subtitle_y + 250
    icon_size = 120
    spacing = 200
    start_x = (COVER_WIDTH - (4 * spacing)) // 2 + 100
    
    # 迷宫图标
    x = start_x
    draw.rectangle([x-icon_size, icon_y-icon_size, x+icon_size, icon_y+icon_size],
                   outline=COLORS["accent_blue"], width=10)
    draw.line([x, icon_y-icon_size+30, x, icon_y+icon_size-30], 
              fill=COLORS["accent_blue"], width=6)
    draw.line([x-icon_size+30, icon_y, x+icon_size-30, icon_y], 
              fill=COLORS["accent_blue"], width=6)
    
    # 调色板图标
    x += spacing
    draw.ellipse([x-80, icon_y-60, x+80, icon_y+60], 
                 fill=COLORS["accent_pink"])
    for i, color in enumerate([COLORS["accent_yellow"], COLORS["accent_green"], 
                                COLORS["accent_blue"], COLORS["white"]]):
        draw.ellipse([x-50+i*35, icon_y-30, x-20+i*35, icon_y], fill=color)
    
    # 拼图图标
    x += spacing
    draw.rectangle([x-icon_size+20, icon_y-icon_size+40, 
                    x+icon_size-20, icon_y+icon_size-40],
                   outline=COLORS["accent_green"], width=8)
    draw.ellipse([x-30, icon_y-icon_size+20, x+30, icon_y-icon_size+60],
                 fill=COLORS["accent_green"])
    
    # 铅笔图标
    x += spacing
    draw.polygon([
        (x-20, icon_y-icon_size), (x+20, icon_y-icon_size),
        (x+15, icon_y+icon_size-40), (x, icon_y+icon_size),
        (x-15, icon_y+icon_size-40)
    ], fill=COLORS["accent_yellow"])
    
    # 底部文字
    bottom_y = COVER_HEIGHT - 300
    
    # 年龄标识
    age_text = "Ages 4-8"
    bbox = draw.textbbox((0, 0), age_text, font=subtitle_font)
    age_width = bbox[2] - bbox[0]
    
    padding = 30
    draw.rounded_rectangle(
        [(COVER_WIDTH-age_width)//2 - padding, bottom_y - 20,
         (COVER_WIDTH+age_width)//2 + padding, bottom_y + 80],
        radius=30,
        fill=COLORS["accent_blue"]
    )
    draw.text(
        ((COVER_WIDTH - age_width) // 2, bottom_y),
        age_text,
        font=subtitle_font,
        fill=COLORS["white"]
    )
    
    # 底部装饰星星
    draw_star(draw, COVER_WIDTH//2 - 400, bottom_y + 40, 40, COLORS["accent_yellow"])
    draw_star(draw, COVER_WIDTH//2 + 400, bottom_y + 40, 40, COLORS["accent_yellow"])
    
    # 保存为PDF - KDP要求300 DPI
    img.save(output_path, 'PDF', resolution=300.0)
    print(f"✅ 封面PDF已生成: {output_path}")
    print(f"   尺寸: {COVER_WIDTH}x{COVER_HEIGHT} px (6x9 inches @ 300 DPI)")
    
    return output_path


if __name__ == "__main__":
    import sys
    
    title = "My Fun Activity Book"
    subtitle = "Mazes, Coloring, Puzzles & More!"
    
    if len(sys.argv) > 1:
        title = sys.argv[1]
    if len(sys.argv) > 2:
        subtitle = sys.argv[2]
    
    output = f"{title.replace(' ', '_')}_cover.pdf"
    create_activity_book_cover_pdf(title, subtitle, output)
