#!/usr/bin/env python3
"""
儿童活动书封面PDF生成器 - KDP安全版本
所有元素严格在安全区域内
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# KDP 6x9书籍的完整封面尺寸
COVER_WIDTH = int(12.360 * 300)   # 3708 像素
COVER_HEIGHT = int(9.250 * 300)   # 2775 像素

# 各部分尺寸
PAGE_WIDTH = int(6 * 300)         # 1800 像素
SPINE_WIDTH = int(0.36 * 300)     # 108 像素
BLEED = int(0.125 * 300)          # 37.5 像素

# KDP安全边距（从出血线往里）
SAFE_MARGIN = int(0.25 * 300)     # 0.25英寸安全边距

# 实际可绘制区域
FRONT_X_START = BLEED + PAGE_WIDTH + SPINE_WIDTH + SAFE_MARGIN
FRONT_X_END = COVER_WIDTH - BLEED - SAFE_MARGIN
FRONT_Y_START = BLEED + SAFE_MARGIN
FRONT_Y_END = COVER_HEIGHT - BLEED - SAFE_MARGIN
FRONT_WIDTH = FRONT_X_END - FRONT_X_START
FRONT_HEIGHT = FRONT_Y_END - FRONT_Y_START

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
    "spine_bg": (255, 160, 170),
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

def create_kdp_safe_cover(title, subtitle, output_path):
    """创建KDP安全封面"""
    
    print(f"生成KDP安全封面...")
    print(f"  总尺寸: {COVER_WIDTH}x{COVER_HEIGHT}px")
    print(f"  前封面安全区域: {FRONT_WIDTH}x{FRONT_HEIGHT}px")
    
    # 创建背景
    img = create_gradient_background(
        COVER_WIDTH, COVER_HEIGHT,
        COLORS["bg_gradient_top"],
        COLORS["bg_gradient_bottom"]
    )
    draw = ImageDraw.Draw(img)
    
    # 计算位置
    back_cover_x = BLEED
    spine_x = BLEED + PAGE_WIDTH
    front_cover_x = spine_x + SPINE_WIDTH
    
    # 绘制书脊背景
    draw.rectangle(
        [spine_x, BLEED, spine_x + SPINE_WIDTH, COVER_HEIGHT - BLEED],
        fill=COLORS["spine_bg"]
    )
    
    # 加载字体 - 使用更安全的字体
    try:
        # 尝试加载系统字体
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "C:/Windows/Fonts/arialbd.ttf",
        ]
        
        title_font = None
        subtitle_font = None
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                title_font = ImageFont.truetype(font_path, 120)  # 稍微减小字体
                subtitle_font = ImageFont.truetype(font_path, 50)
                break
        
        if title_font is None:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # ========== 前封面 ==========
    front_center_x = (FRONT_X_START + FRONT_X_END) / 2
    
    # 前封面边框（在安全区域内）
    border_margin = 30
    draw.rectangle(
        [FRONT_X_START + border_margin, FRONT_Y_START + border_margin,
         FRONT_X_END - border_margin, FRONT_Y_END - border_margin],
        outline=COLORS["white"], width=12
    )
    draw.rectangle(
        [FRONT_X_START + border_margin + 15, FRONT_Y_START + border_margin + 15,
         FRONT_X_END - border_margin - 15, FRONT_Y_END - border_margin - 15],
        outline=COLORS["accent_pink"], width=6
    )
    
    # 计算标题位置（确保安全）
    title_y = FRONT_Y_START + 200
    
    words = title.split()
    if len(words) <= 3:
        bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = bbox[2] - bbox[0]
        draw.text(
            (front_center_x - title_width / 2, title_y),
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
            (front_center_x - (bbox1[2]-bbox1[0]) / 2, title_y),
            line1,
            font=title_font,
            fill=COLORS["title_text"]
        )
        draw.text(
            (front_center_x - (bbox2[2]-bbox2[0]) / 2, title_y + 140),
            line2,
            font=title_font,
            fill=COLORS["title_text"]
        )
        title_y = title_y + 140
    
    # 副标题
    subtitle_y = title_y + 180
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    draw.text(
        (front_center_x - subtitle_width / 2, subtitle_y),
        subtitle,
        font=subtitle_font,
        fill=COLORS["subtitle_text"]
    )
    
    # 装饰元素 - 严格在安全区域内
    # 顶部星星
    draw_star(draw, FRONT_X_START + 150, FRONT_Y_START + 150, 60, COLORS["accent_yellow"])
    draw_star(draw, FRONT_X_END - 150, FRONT_Y_START + 150, 60, COLORS["accent_yellow"])
    
    # 中间星星（在标题两侧）
    draw_star(draw, front_center_x - 350, title_y + 50, 50, COLORS["accent_green"])
    draw_star(draw, front_center_x + 350, title_y + 50, 50, COLORS["accent_green"])
    
    # 底部圆圈（远离底部边缘）
    draw_circle_pattern(draw, FRONT_X_START + 200, FRONT_Y_END - 250, 80, COLORS["accent_blue"])
    draw_circle_pattern(draw, FRONT_X_END - 200, FRONT_Y_END - 250, 80, COLORS["accent_pink"])
    
    # 中部云朵（在副标题下方）
    cloud_y = subtitle_y + 150
    draw_cloud(draw, front_center_x - 200, cloud_y, 60, COLORS["white"])
    draw_cloud(draw, front_center_x + 200, cloud_y, 60, COLORS["white"])
    
    # 活动内容图标区域（在安全区域内居中）
    icon_y = (subtitle_y + FRONT_Y_END - 200) / 2
    icon_size = 100
    spacing = 180
    start_x = front_center_x - (3 * spacing) / 2
    
    # 迷宫
    x = start_x
    draw.rectangle([x-icon_size, icon_y-icon_size, x+icon_size, icon_y+icon_size],
                   outline=COLORS["accent_blue"], width=8)
    draw.line([x, icon_y-icon_size+25, x, icon_y+icon_size-25], 
              fill=COLORS["accent_blue"], width=5)
    draw.line([x-icon_size+25, icon_y, x+icon_size-25, icon_y], 
              fill=COLORS["accent_blue"], width=5)
    
    # 调色板
    x += spacing
    draw.ellipse([x-70, icon_y-50, x+70, icon_y+50], fill=COLORS["accent_pink"])
    
    # 拼图
    x += spacing
    draw.rectangle([x-icon_size+15, icon_y-icon_size+30, x+icon_size-15, icon_y+icon_size-30],
                   outline=COLORS["accent_green"], width=6)
    
    # 铅笔
    x += spacing
    draw.polygon([
        (x-15, icon_y-icon_size), (x+15, icon_y-icon_size),
        (x+10, icon_y+icon_size-30), (x, icon_y+icon_size),
        (x-10, icon_y+icon_size-30)
    ], fill=COLORS["accent_yellow"])
    
    # 底部年龄标识（远离底部边缘）
    bottom_y = FRONT_Y_END - 120
    age_text = "Ages 4-8"
    bbox = draw.textbbox((0, 0), age_text, font=subtitle_font)
    age_width = bbox[2] - bbox[0]
    
    padding = 25
    draw.rounded_rectangle(
        [front_center_x - age_width/2 - padding, bottom_y - 15,
         front_center_x + age_width/2 + padding, bottom_y + 60],
        radius=25, fill=COLORS["accent_blue"]
    )
    draw.text(
        (front_center_x - age_width / 2, bottom_y),
        age_text,
        font=subtitle_font,
        fill=COLORS["white"]
    )
    
    # 底部星星（在安全区域内）
    draw_star(draw, front_center_x - 300, bottom_y + 30, 35, COLORS["accent_yellow"])
    draw_star(draw, front_center_x + 300, bottom_y + 30, 35, COLORS["accent_yellow"])
    
    # ========== 书脊（无文字）==========
    
    # ========== 后封面（简洁）==========
    back_margin = 30
    draw.rectangle(
        [back_cover_x + back_margin, BLEED + back_margin,
         back_cover_x + PAGE_WIDTH - back_margin, COVER_HEIGHT - BLEED - back_margin],
        outline=COLORS["white"], width=12
    )
    
    # 保存为PDF
    img.save(output_path, 'PDF', resolution=300.0)
    print(f"✅ KDP安全封面PDF已生成: {output_path}")
    
    return output_path


if __name__ == "__main__":
    import sys
    
    title = "My Fun Activity Book"
    subtitle = "Mazes, Coloring, Puzzles & More!"
    
    if len(sys.argv) > 1:
        title = sys.argv[1]
    if len(sys.argv) > 2:
        subtitle = sys.argv[2]
    
    output = f"{title.replace(' ', '_')}_kdp_safe_cover.pdf"
    create_kdp_safe_cover(title, subtitle, output)
