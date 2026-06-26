#!/usr/bin/env python3
"""
Amazon KDP 封面生成器
生成符合 KDP 要求的电子书封面

Usage:
    generate_cover.py --title "书名" --author "作者" [options]

Requirements:
    pip install pillow

KDP 封面要求：
    - 格式: JPEG 或 TIFF
    - 最小尺寸: 1000x625 像素 (宽高比 1.6:1)
    - 推荐尺寸: 2560x1600 像素
    - 分辨率: 72-300 DPI
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("❌ 需要安装 Pillow: pip install pillow")
    sys.exit(1)


# KDP 推荐尺寸
COVER_WIDTH = 2560
COVER_HEIGHT = 1600
ASPECT_RATIO = 1.6


def create_gradient_background(width: int, height: int, color1: tuple, color2: tuple) -> Image.Image:
    """创建渐变背景"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img


def get_font(size: int, font_name: str = None):
    """获取字体"""
    if font_name:
        try:
            return ImageFont.truetype(font_name, size)
        except:
            pass
    
    # 尝试常见中文字体
    font_paths = [
        '/System/Library/Fonts/PingFang.ttc',  # macOS
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',  # Linux
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        'C:/Windows/Fonts/simhei.ttf',  # Windows
        'C:/Windows/Fonts/msyh.ttc',
    ]
    
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    
    return ImageFont.load_default()


def generate_cover(
    title: str,
    author: str,
    subtitle: str = None,
    template: str = "modern",
    output: str = "cover.jpg",
    font_title: str = None,
    font_author: str = None
):
    """生成封面"""
    
    # 模板配色
    templates = {
        'modern': {
            'bg_colors': [(45, 52, 70), (60, 70, 90)],  # 深蓝渐变
            'title_color': (255, 255, 255),
            'author_color': (200, 200, 200),
            'accent': (100, 150, 255)
        },
        'warm': {
            'bg_colors': [(120, 60, 40), (180, 100, 60)],  # 暖橙渐变
            'title_color': (255, 255, 255),
            'author_color': (240, 220, 200),
            'accent': (255, 180, 100)
        },
        'minimal': {
            'bg_colors': [(250, 250, 250), (240, 240, 240)],  # 白灰渐变
            'title_color': (30, 30, 30),
            'author_color': (100, 100, 100),
            'accent': (50, 50, 50)
        },
        'dark': {
            'bg_colors': [(20, 20, 20), (40, 40, 40)],  # 深黑渐变
            'title_color': (255, 255, 255),
            'author_color': (180, 180, 180),
            'accent': (100, 200, 255)
        }
    }
    
    colors = templates.get(template, templates['modern'])
    
    # 创建背景
    img = create_gradient_background(COVER_WIDTH, COVER_HEIGHT, colors['bg_colors'][0], colors['bg_colors'][1])
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    title_font = get_font(140, font_title)
    author_font = get_font(70, font_author)
    subtitle_font = get_font(60, font_title)
    
    # 计算标题位置（居中偏上）
    title_y = COVER_HEIGHT // 3
    
    # 绘制装饰线条
    line_y = title_y - 50
    line_margin = COVER_WIDTH // 4
    draw.line(
        [(line_margin, line_y), (COVER_WIDTH - line_margin, line_y)],
        fill=colors['accent'],
        width=8
    )
    
    # 绘制标题
    # 自动换行处理
    words = title
    lines = []
    current_line = ""
    
    for char in words:
        test_line = current_line + char
        bbox = draw.textbbox((0, 0), test_line, font=title_font)
        if bbox[2] < COVER_WIDTH - 200:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = char
    
    if current_line:
        lines.append(current_line)
    
    # 如果没有换行，直接居中显示
    if not lines:
        lines = [title]
    
    # 绘制每一行标题
    total_title_height = len(lines) * 160
    current_y = title_y - total_title_height // 4
    
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (COVER_WIDTH - text_width) // 2
        
        # 添加阴影
        draw.text((x+4, current_y+4), line, font=title_font, fill=(0, 0, 0, 128))
        draw.text((x, current_y), line, font=title_font, fill=colors['title_color'])
        
        current_y += 150
    
    # 绘制副标题
    if subtitle:
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        x = (COVER_WIDTH - text_width) // 2
        y = current_y + 30
        draw.text((x, y), subtitle, font=subtitle_font, fill=colors['author_color'])
    
    # 绘制装饰线条（下方）
    author_y = COVER_HEIGHT * 2 // 3
    draw.line(
        [(line_margin, author_y - 30), (COVER_WIDTH - line_margin, author_y - 30)],
        fill=colors['accent'],
        width=4
    )
    
    # 绘制作者名
    author_text = f"{author} 著"
    bbox = draw.textbbox((0, 0), author_text, font=author_font)
    text_width = bbox[2] - bbox[0]
    x = (COVER_WIDTH - text_width) // 2
    draw.text((x, author_y), author_text, font=author_font, fill=colors['author_color'])
    
    # 保存
    img.save(output, 'JPEG', quality=95)
    print(f"✅ 封面生成成功: {output}")
    print(f"   尺寸: {COVER_WIDTH}x{COVER_HEIGHT} 像素")
    print(f"   宽高比: {ASPECT_RATIO}:1")
    return output


def validate_cover(image_path: str) -> dict:
    """验证封面是否符合 KDP 要求"""
    img = Image.open(image_path)
    width, height = img.size
    aspect_ratio = width / height
    
    issues = []
    
    if width < 1000 or height < 625:
        issues.append(f"尺寸过小: {width}x{height}, 最小应为 1000x625")
    
    if abs(aspect_ratio - ASPECT_RATIO) > 0.1:
        issues.append(f"宽高比不正确: {aspect_ratio:.2f}, 应为 {ASPECT_RATIO}")
    
    result = {
        'valid': len(issues) == 0,
        'width': width,
        'height': height,
        'aspect_ratio': aspect_ratio,
        'format': img.format,
        'issues': issues
    }
    
    return result


def main():
    parser = argparse.ArgumentParser(description='Generate Amazon KDP book cover')
    parser.add_argument('--title', '-t', required=True, help='Book title')
    parser.add_argument('--author', '-a', required=True, help='Author name')
    parser.add_argument('--subtitle', '-s', help='Subtitle')
    parser.add_argument('--template', choices=['modern', 'warm', 'minimal', 'dark'], 
                       default='modern', help='Cover template')
    parser.add_argument('--output', '-o', default='cover.jpg', help='Output filename')
    parser.add_argument('--font-title', help='Title font file')
    parser.add_argument('--font-author', help='Author font file')
    parser.add_argument('--validate', metavar='IMAGE', help='Validate existing cover image')
    
    args = parser.parse_args()
    
    if args.validate:
        result = validate_cover(args.validate)
        print(f"\n📐 封面验证结果:")
        print(f"   尺寸: {result['width']}x{result['height']}")
        print(f"   格式: {result['format']}")
        print(f"   宽高比: {result['aspect_ratio']:.2f}")
        
        if result['valid']:
            print(f"   ✅ 符合 KDP 要求")
        else:
            print(f"   ❌ 存在问题:")
            for issue in result['issues']:
                print(f"      - {issue}")
    else:
        generate_cover(
            title=args.title,
            author=args.author,
            subtitle=args.subtitle,
            template=args.template,
            output=args.output,
            font_title=args.font_title,
            font_author=args.font_author
        )


if __name__ == '__main__':
    main()
