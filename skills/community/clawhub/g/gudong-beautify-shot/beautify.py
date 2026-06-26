#!/usr/bin/env python3
"""
Screenshot Beautifier - 截图美化工具

给截图添加渐变背景和圆角，支持底部添加文字描述。
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# 默认参数
PADDING = 60
CORNER_RADIUS = 20
TEXT_SIZE = 32
TEXT_COLOR = "#4a4a4a"
TEXT_MARGIN = 20
TEXT_GAP = 30

# 默认渐变配色（蜜桃橙粉）
GRADIENT_COLORS = ("#f3b7ad", "#ffdfba")

# 字体路径（按优先级尝试）
FONT_PATHS = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
]


def hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def get_font(size: int) -> ImageFont.FreeTypeFont:
    for font_path in FONT_PATHS:
        if Path(font_path).exists():
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                continue
    try:
        return ImageFont.truetype(size=size)
    except Exception:
        return ImageFont.load_default()


def create_gradient(width: int, height: int, color_top: str, color_bottom: str) -> Image.Image:
    """创建垂直渐变背景（高性能版本）"""
    base = Image.new('RGB', (width, height))
    r1, g1, b1 = hex_to_rgb(color_top)
    r2, g2, b2 = hex_to_rgb(color_bottom)
    pixels = base.load()
    for y in range(height):
        ratio = y / max(height - 1, 1)
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        for x in range(width):
            pixels[x, y] = (r, g, b)
    return base


def add_rounded_corners(img: Image.Image, radius: int) -> Image.Image:
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
    output = Image.new('RGBA', img.size, (0, 0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)
    return output


def beautify(input_path: str, output_path: str = None, text: str = None) -> str:
    """美化截图，返回输出文件路径"""
    original = Image.open(input_path)
    img_w, img_h = original.size

    # 计算背景尺寸
    bg_w = img_w + PADDING * 2
    extra_h = 0
    text_y = 0

    if text:
        font = get_font(TEXT_SIZE)
        dummy = ImageDraw.Draw(Image.new('RGB', (1, 1)))
        bbox = dummy.textbbox((0, 0), text, font=font)
        text_h = bbox[3] - bbox[1]
        extra_h = TEXT_GAP + text_h + TEXT_MARGIN
        text_y = PADDING + img_h + TEXT_GAP
        bg_h = PADDING + img_h + extra_h + TEXT_MARGIN
    else:
        bg_h = img_h + PADDING * 2

    # 渐变背景
    background = create_gradient(bg_w, bg_h, *GRADIENT_COLORS).convert('RGBA')

    # 圆角截图贴到背景
    rounded = add_rounded_corners(original, CORNER_RADIUS)
    background.paste(rounded, (PADDING, PADDING), rounded)

    # 底部文字
    if text:
        draw = ImageDraw.Draw(background)
        font = get_font(TEXT_SIZE)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = (bg_w - tw) // 2
        draw.text((x + 1, text_y + 1), text, font=font, fill=(0, 0, 0, 80))
        draw.text((x, text_y), text, font=font, fill=hex_to_rgb(TEXT_COLOR))

    # 保存（保持 RGBA 避免白边）
    if output_path is None:
        p = Path(input_path)
        output_path = str(p.parent / f"{p.stem}_beautified.png")

    background.convert('RGBA').save(output_path, 'PNG')
    return output_path


def main():
    import argparse
    parser = argparse.ArgumentParser(description='截图美化工具')
    parser.add_argument('input', help='输入图片路径')
    parser.add_argument('-o', '--output', help='输出图片路径')
    parser.add_argument('-t', '--text', help='底部文字描述')
    args = parser.parse_args()
    print(beautify(args.input, args.output, args.text))


if __name__ == '__main__':
    main()
