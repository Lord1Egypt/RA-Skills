#!/usr/bin/env python3
"""
儿童活动书封面PDF生成器 - KDP完整封面版
包含前封面+书脊+后封面+出血边距
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# KDP 6x9书籍的完整封面尺寸（包含前后封+书脊+出血）
# 期望尺寸: 12.360 x 9.250 英寸 @ 300 DPI
COVER_WIDTH = int(12.360 * 300)  # 3708 像素
COVER_HEIGHT = int(9.250 * 300)   # 2775 像素

# 各部分尺寸（像素）
PAGE_WIDTH = int(6 * 300)         # 1800 像素（单页）
SPINE_WIDTH = int(0.36 * 300)     # 108 像素（书脊，44页约0.36英寸）
BLEED = int(0.125 * 300)          # 37.5 像素（出血边距，KDP标准）

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
    "spine_bg": (255, 160, 170),  # 书脊背景色
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

def create_kdp_full_cover(title, subtitle, output_path):
    """创建KDP完整封面（前封+书脊+后封）"""
    
    print(f"生成KDP完整封面...")
    print(f"  总尺寸: {COVER_WIDTH}x{COVER_HEIGHT} px ({COVER_WIDTH/300:.3f}\" x {COVER_HEIGHT/300:.3f}\")")
    print(f"  单页: {PAGE_WIDTH}px (6\")")
    print(f"  书脊: {SPINE_WIDTH}px (0.36\")")
    print(f"  出血: {BLEED}px (0.125\")")
    
    # 创建完整封面背景
    img = create_gradient_background(
        COVER_WIDTH, COVER_HEIGHT,
        COLORS["bg_gradient_top"],
        COLORS["bg_gradient_bottom"]
    )
    draw = ImageDraw.Draw(img)
    
    # 计算各部分位置
    back_cover_x = BLEED  # 后封面起始位置（考虑出血）
    spine_x = BLEED + PAGE_WIDTH  # 书脊起始位置
    front_cover_x = spine_x + SPINE_WIDTH  # 前封面起始位置
    
    # 绘制书脊背景（稍深的颜色）
    draw.rectangle(
        [spine_x, BLEED, spine_x + SPINE_WIDTH, COVER_HEIGHT - BLEED],
        fill=COLORS["spine_bg"]
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
                break
        
        if title_font is None:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # ========== 前封面 ==========
    front_center_x = front_cover_x + PAGE_WIDTH / 2
    
    # 前封面边框
    border_margin = 40
    draw.rectangle(
        [front_cover_x + border_margin, BLEED + border_margin,
         front_cover_x + PAGE_WIDTH - border_margin, COVER_HEIGHT - BLEED - border_margin],
        outline=COLORS["white"], width=15
    )
    draw.rectangle(
        [front_cover_x + border_margin + 20, BLEED + border_margin + 20,
         front_cover_x + PAGE_WIDTH - border_margin - 20, COVER_HEIGHT - BLEED - border_margin - 20],
        outline=COLORS["accent_pink"], width=8
    )
    
    # 前封面标题
    title_y = BLEED + 450
    
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
            (front_center_x - (bbox2[2]-bbox2[0]) / 2, title_y + 160),
            line2,
            font=title_font,
            fill=COLORS["title_text"]
        )
        title_y = title_y + 160
    
    # 副标题
    subtitle_y = title_y + 200
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    draw.text(
        (front_center_x - subtitle_width / 2, subtitle_y),
        subtitle,
        font=subtitle_font,
        fill=COLORS["subtitle_text"]
    )
    
    # 前封面装饰 - 星星
    draw_star(draw, front_cover_x + 250, BLEED + 800, 80, COLORS["accent_yellow"])
    draw_star(draw, front_cover_x + PAGE_WIDTH - 250, BLEED + 850, 70, COLORS["accent_yellow"])
    draw_star(draw, front_cover_x + 180, BLEED + 1400, 60, COLORS["accent_green"])
    draw_star(draw, front_cover_x + PAGE_WIDTH - 180, BLEED + 1350, 65, COLORS["accent_green"])
    
    # 圆圈装饰
    draw_circle_pattern(draw, front_cover_x + 300, COVER_HEIGHT - BLEED - 775, 100, COLORS["accent_blue"])
    draw_circle_pattern(draw, front_cover_x + PAGE_WIDTH - 300, COVER_HEIGHT - BLEED - 675, 90, COLORS["accent_pink"])
    draw_circle_pattern(draw, front_cover_x + 200, BLEED + 1200, 70, COLORS["accent_blue"])
    draw_circle_pattern(draw, front_cover_x + PAGE_WIDTH - 200, COVER_HEIGHT - BLEED - 975, 80, COLORS["accent_green"])
    
    # 云朵装饰 - 往下移动
    draw_cloud(draw, front_cover_x + 400, BLEED + 1100, 80, COLORS["white"])
    draw_cloud(draw, front_cover_x + PAGE_WIDTH - 350, BLEED + 1150, 70, COLORS["white"])
    
    # 活动内容图标
    icon_y = subtitle_y + 250
    icon_size = 120
    spacing = 200
    start_x = front_cover_x + (PAGE_WIDTH - (4 * spacing)) // 2 + 100
    
    # 迷宫
    x = start_x
    draw.rectangle([x-icon_size, icon_y-icon_size, x+icon_size, icon_y+icon_size],
                   outline=COLORS["accent_blue"], width=10)
    draw.line([x, icon_y-icon_size+30, x, icon_y+icon_size-30], 
              fill=COLORS["accent_blue"], width=6)
    draw.line([x-icon_size+30, icon_y, x+icon_size-30, icon_y], 
              fill=COLORS["accent_blue"], width=6)
    
    # 调色板
    x += spacing
    draw.ellipse([x-80, icon_y-60, x+80, icon_y+60], fill=COLORS["accent_pink"])
    for i, color in enumerate([COLORS["accent_yellow"], COLORS["accent_green"], 
                                COLORS["accent_blue"], COLORS["white"]]):
        draw.ellipse([x-50+i*35, icon_y-30, x-20+i*35, icon_y], fill=color)
    
    # 拼图
    x += spacing
    draw.rectangle([x-icon_size+20, icon_y-icon_size+40, x+icon_size-20, icon_y+icon_size-40],
                   outline=COLORS["accent_green"], width=8)
    draw.ellipse([x-30, icon_y-icon_size+20, x+30, icon_y-icon_size+60], fill=COLORS["accent_green"])
    
    # 铅笔
    x += spacing
    draw.polygon([
        (x-20, icon_y-icon_size), (x+20, icon_y-icon_size),
        (x+15, icon_y+icon_size-40), (x, icon_y+icon_size),
        (x-15, icon_y+icon_size-40)
    ], fill=COLORS["accent_yellow"])
    
    # 底部年龄标识
    bottom_y = COVER_HEIGHT - BLEED - 300
    age_text = "Ages 4-8"
    bbox = draw.textbbox((0, 0), age_text, font=subtitle_font)
    age_width = bbox[2] - bbox[0]
    
    padding = 30
    draw.rounded_rectangle(
        [front_center_x - age_width/2 - padding, bottom_y - 20,
         front_center_x + age_width/2 + padding, bottom_y + 80],
        radius=30, fill=COLORS["accent_blue"]
    )
    draw.text(
        (front_center_x - age_width / 2, bottom_y),
        age_text,
        font=subtitle_font,
        fill=COLORS["white"]
    )
    
    # 底部星星
    draw_star(draw, front_center_x - 400, bottom_y + 40, 40, COLORS["accent_yellow"])
    draw_star(draw, front_center_x + 400, bottom_y + 40, 40, COLORS["accent_yellow"])
    
    # ========== 书脊 ==========
    # 书脊保持简洁，不加文字
    
    # ========== 后封面（简洁，只留装饰）==========
    back_center_x = back_cover_x + PAGE_WIDTH / 2
    
    # 后封面边框
    draw.rectangle(
        [back_cover_x + border_margin, BLEED + border_margin,
         back_cover_x + PAGE_WIDTH - border_margin, COVER_HEIGHT - BLEED - border_margin],
        outline=COLORS["white"], width=15
    )
    
    # 保存为PDF
    img.save(output_path, 'PDF', resolution=300.0)
    print(f"✅ KDP完整封面PDF已生成: {output_path}")
    print(f"   尺寸: {COVER_WIDTH/300:.3f}\" x {COVER_HEIGHT/300:.3f}\" (符合KDP要求)")
    
    return output_path


if __name__ == "__main__":
    import sys
    
    title = "My Fun Activity Book"
    subtitle = "Mazes, Coloring, Puzzles & More!"
    
    if len(sys.argv) > 1:
        title = sys.argv[1]
    if len(sys.argv) > 2:
        subtitle = sys.argv[2]
    
    output = f"{title.replace(' ', '_')}_kdp_cover.pdf"
    create_kdp_full_cover(title, subtitle, output)
