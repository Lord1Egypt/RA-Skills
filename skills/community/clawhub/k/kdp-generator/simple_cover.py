#!/usr/bin/env python3
"""
极简KDP封面生成器 - 无多余装饰
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 6x9英寸封面 @ 300 DPI
WIDTH = 1800
HEIGHT = 2700

# 安全边距
MARGIN = 100  # 约0.33英寸

def create_simple_cover(title, subtitle, color_scheme="dino", output_path="cover.pdf"):
    """创建极简封面"""
    
    # 颜色方案
    schemes = {
        "dino": {
            "bg": (144, 190, 109),      # 恐龙绿
            "title": (40, 54, 24),       # 深绿
            "subtitle": (60, 80, 40),
            "accent": (249, 166, 62),    # 橙色
        },
        "unicorn": {
            "bg": (255, 200, 230),      # 粉紫
            "title": (80, 40, 80),
            "subtitle": (100, 60, 100),
            "accent": (180, 120, 220),
        },
        "space": {
            "bg": (30, 40, 80),         # 深蓝
            "title": (255, 255, 255),    # 白
            "subtitle": (200, 200, 220),
            "accent": (100, 150, 255),
        }
    }
    
    colors = schemes.get(color_scheme, schemes["dino"])
    
    # 创建纯色背景
    img = Image.new('RGB', (WIDTH, HEIGHT), colors["bg"])
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    try:
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]
        for fp in font_paths:
            if os.path.exists(fp):
                title_font = ImageFont.truetype(fp, 120)
                subtitle_font = ImageFont.truetype(fp, 50)
                break
        else:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # 计算安全区域中心
    center_x = WIDTH // 2
    safe_top = MARGIN + 150
    safe_bottom = HEIGHT - MARGIN - 150
    
    # 绘制标题
    words = title.split()
    if len(words) <= 2:
        bbox = draw.textbbox((0, 0), title, font=title_font)
        title_y = safe_top + 100
        draw.text(
            (center_x - (bbox[2]-bbox[0])//2, title_y),
            title,
            font=title_font,
            fill=colors["title"]
        )
    else:
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
        
        bbox1 = draw.textbbox((0, 0), line1, font=title_font)
        bbox2 = draw.textbbox((0, 0), line2, font=title_font)
        
        title_y = safe_top + 80
        draw.text(
            (center_x - (bbox1[2]-bbox1[0])//2, title_y),
            line1,
            font=title_font,
            fill=colors["title"]
        )
        draw.text(
            (center_x - (bbox2[2]-bbox2[0])//2, title_y + 130),
            line2,
            font=title_font,
            fill=colors["title"]
        )
        title_y = title_y + 130
    
    # 副标题
    if subtitle:
        subtitle_y = title_y + 180
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        draw.text(
            (center_x - (bbox[2]-bbox[0])//2, subtitle_y),
            subtitle,
            font=subtitle_font,
            fill=colors["subtitle"]
        )
    
    # 底部年龄（简洁版）
    age_y = safe_bottom - 50
    age_text = "Ages 4-8"
    bbox = draw.textbbox((0, 0), age_text, font=subtitle_font)
    
    # 简单圆角背景
    padding = 25
    draw.rounded_rectangle(
        [center_x - (bbox[2]-bbox[0])//2 - padding, age_y - 15,
         center_x + (bbox[2]-bbox[0])//2 + padding, age_y + 55],
        radius=20,
        fill=colors["accent"]
    )
    draw.text(
        (center_x - (bbox[2]-bbox[0])//2, age_y),
        age_text,
        font=subtitle_font,
        fill=(255, 255, 255)
    )
    
    # 保存
    img.save(output_path, 'PDF', resolution=300.0)
    print(f"✅ 极简封面已生成: {output_path}")
    return output_path


if __name__ == "__main__":
    # 恐龙书封面
    create_simple_cover(
        "Dinosaur Adventure Activity Book",
        "Mazes, Coloring, Puzzles & More!",
        color_scheme="dino",
        output_path="dino_cover.pdf"
    )
