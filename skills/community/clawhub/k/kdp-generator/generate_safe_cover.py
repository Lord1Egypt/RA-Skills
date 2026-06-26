#!/usr/bin/env python3
"""
KDP完全安全版封面生成器 - 所有元素严格在边距内
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 6x9英寸 @ 300 DPI = 1800 x 2700 像素 (仅前封面)
COVER_WIDTH = 1800
COVER_HEIGHT = 2700

# KDP安全边距（从页面边缘往里）
SAFE_MARGIN = 75  # 0.25英寸 = 75像素 (留出足够安全空间)

# 实际可绘制区域
DRAW_X_START = SAFE_MARGIN
DRAW_X_END = COVER_WIDTH - SAFE_MARGIN
DRAW_Y_START = SAFE_MARGIN
DRAW_Y_END = COVER_HEIGHT - SAFE_MARGIN
DRAW_WIDTH = DRAW_X_END - DRAW_X_START
DRAW_HEIGHT = DRAW_Y_END - DRAW_Y_START

COLORS = {
    "bg": (255, 200, 180),        # 柔和粉色背景
    "title": (60, 60, 90),        # 深蓝灰标题
    "subtitle": (80, 80, 110),    # 中蓝灰副标题
    "accent1": (255, 180, 100),   # 橙色
    "accent2": (100, 200, 180),   # 青色
    "accent3": (255, 120, 150),   # 粉色
    "white": (255, 255, 255),
}

def create_safe_cover(title, subtitle, output_path):
    """创建完全安全的封面"""
    
    # 创建纯色背景
    img = Image.new('RGB', (COVER_WIDTH, COVER_HEIGHT), COLORS["bg"])
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    try:
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                title_font = ImageFont.truetype(font_path, 100)
                subtitle_font = ImageFont.truetype(font_path, 45)
                small_font = ImageFont.truetype(font_path, 40)
                break
        else:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
            
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # 绘制装饰边框（在安全区域内）
    border_margin = 20
    draw.rectangle(
        [DRAW_X_START + border_margin, DRAW_Y_START + border_margin,
         DRAW_X_END - border_margin, DRAW_Y_END - border_margin],
        outline=COLORS["white"], width=10
    )
    
    # 计算中心点
    center_x = COVER_WIDTH // 2
    
    # 绘制标题（在安全区域内）
    title_y = DRAW_Y_START + 150
    
    # 分行处理
    words = title.split()
    if len(words) <= 2:
        bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = bbox[2] - bbox[0]
        draw.text(
            (center_x - title_width // 2, title_y),
            title,
            font=title_font,
            fill=COLORS["title"]
        )
    else:
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
        
        bbox1 = draw.textbbox((0, 0), line1, font=title_font)
        bbox2 = draw.textbbox((0, 0), line2, font=title_font)
        
        draw.text(
            (center_x - (bbox1[2]-bbox1[0]) // 2, title_y),
            line1,
            font=title_font,
            fill=COLORS["title"]
        )
        draw.text(
            (center_x - (bbox2[2]-bbox2[0]) // 2, title_y + 120),
            line2,
            font=title_font,
            fill=COLORS["title"]
        )
        title_y = title_y + 120
    
    # 副标题
    subtitle_y = title_y + 150
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    draw.text(
        (center_x - subtitle_width // 2, subtitle_y),
        subtitle,
        font=subtitle_font,
        fill=COLORS["subtitle"]
    )
    
    # 绘制简单的装饰圆点（在安全区域内）
    # 四个角的小圆点
    dot_offset = 60
    dot_radius = 15
    
    # 左上
    draw.ellipse([DRAW_X_START + dot_offset - dot_radius, 
                  DRAW_Y_START + dot_offset - dot_radius,
                  DRAW_X_START + dot_offset + dot_radius,
                  DRAW_Y_START + dot_offset + dot_radius], 
                 fill=COLORS["accent1"])
    
    # 右上
    draw.ellipse([DRAW_X_END - dot_offset - dot_radius, 
                  DRAW_Y_START + dot_offset - dot_radius,
                  DRAW_X_END - dot_offset + dot_radius,
                  DRAW_Y_START + dot_offset + dot_radius], 
                 fill=COLORS["accent1"])
    
    # 左下
    draw.ellipse([DRAW_X_START + dot_offset - dot_radius, 
                  DRAW_Y_END - dot_offset - dot_radius,
                  DRAW_X_START + dot_offset + dot_radius,
                  DRAW_Y_END - dot_offset + dot_radius], 
                 fill=COLORS["accent2"])
    
    # 右下
    draw.ellipse([DRAW_X_END - dot_offset - dot_radius, 
                  DRAW_Y_END - dot_offset - dot_radius,
                  DRAW_X_END - dot_offset + dot_radius,
                  DRAW_Y_END - dot_offset + dot_radius], 
                 fill=COLORS["accent2"])
    
    # 中部装饰（简单线条）
    line_y = subtitle_y + 120
    draw.line([(center_x - 200, line_y), (center_x + 200, line_y)], 
              fill=COLORS["accent3"], width=5)
    
    # 底部年龄（远离底部边缘）
    age_y = DRAW_Y_END - 100
    age_text = "Ages 4-8"
    bbox = draw.textbbox((0, 0), age_text, font=small_font)
    age_width = bbox[2] - bbox[0]
    
    # 绘制背景圆角矩形
    padding = 20
    draw.rounded_rectangle(
        [center_x - age_width//2 - padding, age_y - 10,
         center_x + age_width//2 + padding, age_y + 50],
        radius=20,
        fill=COLORS["accent2"]
    )
    draw.text(
        (center_x - age_width // 2, age_y),
        age_text,
        font=small_font,
        fill=COLORS["white"]
    )
    
    # 保存为PDF
    img.save(output_path, 'PDF', resolution=300.0)
    print(f"✅ 安全封面已生成: {output_path}")
    print(f"   尺寸: {COVER_WIDTH}x{COVER_HEIGHT}px (6x9 inches @ 300 DPI)")
    print(f"   安全边距: {SAFE_MARGIN}px (0.25 inches)")
    
    return output_path


if __name__ == "__main__":
    title = "My Fun Activity Book"
    subtitle = "Mazes, Coloring, Puzzles & More!"
    
    output = "cover_safe.pdf"
    create_safe_cover(title, subtitle, output)
