#!/usr/bin/env python3
"""
极简KDP封面生成器 - 仅保留主标题
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 6x9英寸 @ 300 DPI
WIDTH = 1800
HEIGHT = 2700

# 超大安全边距（严格在KDP虚线内）
SAFE_MARGIN = 200  # 0.67英寸，确保所有元素在安全区域内

def create_minimal_cover(title, subtitle, output_path="cover_minimal.pdf"):
    """创建极简封面 - 仅保留书名"""
    
    # 恐龙绿色系
    BG_COLOR = (144, 190, 109)
    TITLE_COLOR = (40, 54, 24)
    
    # 创建纯色背景
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
                title_font = ImageFont.truetype(fp, 100)
                break
        else:
            title_font = ImageFont.load_default()
    except:
        title_font = ImageFont.load_default()
    
    # 计算安全区域中心
    center_x = WIDTH // 2
    safe_top = SAFE_MARGIN
    safe_bottom = HEIGHT - SAFE_MARGIN
    
    # 在安全区域内垂直居中绘制标题
    safe_height = safe_bottom - safe_top
    
    # 绘制主标题（简洁版）
    words = title.split()
    if len(words) <= 3:
        # 单行或双行
        bbox = draw.textbbox((0, 0), title, font=title_font)
        # 在安全区域内垂直居中
        title_y = safe_top + (safe_height - (bbox[3] - bbox[1])) // 2
        draw.text(
            (center_x - (bbox[2]-bbox[0])//2, title_y),
            title,
            font=title_font,
            fill=TITLE_COLOR
        )
    else:
        # 三行
        mid1 = len(words) // 3
        mid2 = mid1 * 2
        line1 = " ".join(words[:mid1])
        line2 = " ".join(words[mid1:mid2])
        line3 = " ".join(words[mid2:])
        
        bbox1 = draw.textbbox((0, 0), line1, font=title_font)
        bbox2 = draw.textbbox((0, 0), line2, font=title_font)
        bbox3 = draw.textbbox((0, 0), line3, font=title_font)
        
        total_height = (bbox1[3] - bbox1[1]) + (bbox2[3] - bbox2[1]) + (bbox3[3] - bbox3[1]) + 220
        title_y = safe_top + (safe_height - total_height) // 2
        
        draw.text((center_x - (bbox1[2]-bbox1[0])//2, title_y), line1, font=title_font, fill=TITLE_COLOR)
        draw.text((center_x - (bbox2[2]-bbox2[0])//2, title_y + 110), line2, font=title_font, fill=TITLE_COLOR)
        draw.text((center_x - (bbox3[2]-bbox3[0])//2, title_y + 220), line3, font=title_font, fill=TITLE_COLOR)
    
    # 保存
    img.save(output_path, 'PDF', resolution=300.0)
    print(f"✅ 极简封面已生成: {output_path}")
    return output_path


if __name__ == "__main__":
    create_minimal_cover(
        "Dinosaur Adventure Activity Book",
        "",
        "/root/.openclaw/workspace/kdp_output/Dinosaur_Adventure/cover.pdf"
    )
