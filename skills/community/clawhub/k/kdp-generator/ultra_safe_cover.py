#!/usr/bin/env python3
"""
超安全KDP封面 - 所有元素严格在边距内
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 6x9英寸 @ 300 DPI
WIDTH = 1800
HEIGHT = 2700

# 超大安全边距（确保在KDP虚线内）
SAFE_MARGIN = 150  # 0.5英寸

def create_ultra_safe_cover(title, subtitle, output_path="cover_safe.pdf"):
    """创建超安全封面"""
    
    # 恐龙绿色系
    BG_COLOR = (144, 190, 109)
    TITLE_COLOR = (40, 54, 24)
    SUBTITLE_COLOR = (60, 80, 40)
    ACCENT_COLOR = (249, 166, 62)
    
    # 创建背景
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    try:
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]
        for fp in font_paths:
            if os.path.exists(fp):
                title_font = ImageFont.truetype(fp, 100)  # 减小字体
                subtitle_font = ImageFont.truetype(fp, 45)
                break
        else:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # 计算安全区域
    safe_left = SAFE_MARGIN
    safe_right = WIDTH - SAFE_MARGIN
    safe_top = SAFE_MARGIN
    safe_bottom = HEIGHT - SAFE_MARGIN
    center_x = WIDTH // 2
    
    # 绘制标题（在安全区域内）
    words = title.split()
    if len(words) <= 2:
        bbox = draw.textbbox((0, 0), title, font=title_font)
        title_y = safe_top + 80
        draw.text(
            (center_x - (bbox[2]-bbox[0])//2, title_y),
            title,
            font=title_font,
            fill=TITLE_COLOR
        )
    else:
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
        
        bbox1 = draw.textbbox((0, 0), line1, font=title_font)
        bbox2 = draw.textbbox((0, 0), line2, font=title_font)
        
        title_y = safe_top + 60
        draw.text(
            (center_x - (bbox1[2]-bbox1[0])//2, title_y),
            line1,
            font=title_font,
            fill=TITLE_COLOR
        )
        draw.text(
            (center_x - (bbox2[2]-bbox2[0])//2, title_y + 110),
            line2,
            font=title_font,
            fill=TITLE_COLOR
        )
        title_y = title_y + 110
    
    # 副标题
    subtitle_y = title_y + 140
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    draw.text(
        (center_x - (bbox[2]-bbox[0])//2, subtitle_y),
        subtitle,
        font=subtitle_font,
        fill=SUBTITLE_COLOR
    )
    
    # 底部年龄（严格在安全区域内）
    age_y = safe_bottom - 80
    age_text = "Ages 4-8"
    bbox = draw.textbbox((0, 0), age_text, font=subtitle_font)
    
    # 简单矩形背景（不超出边界）
    padding = 20
    left = center_x - (bbox[2]-bbox[0])//2 - padding
    right = center_x + (bbox[2]-bbox[0])//2 + padding
    top = age_y - 10
    bottom = age_y + 50
    
    # 确保不超出安全区域
    left = max(left, safe_left + 20)
    right = min(right, safe_right - 20)
    
    draw.rounded_rectangle(
        [left, top, right, bottom],
        radius=15,
        fill=ACCENT_COLOR
    )
    draw.text(
        (center_x - (bbox[2]-bbox[0])//2, age_y),
        age_text,
        font=subtitle_font,
        fill=(255, 255, 255)
    )
    
    # 保存
    img.save(output_path, 'PDF', resolution=300.0)
    print(f"✅ 超安全封面已生成: {output_path}")
    print(f"   安全边距: {SAFE_MARGIN}px (0.5 inches)")
    return output_path


if __name__ == "__main__":
    create_ultra_safe_cover(
        "Dinosaur Adventure Activity Book",
        "Mazes, Coloring, Puzzles & More!",
        "dino_cover_ultra_safe.pdf"
    )
