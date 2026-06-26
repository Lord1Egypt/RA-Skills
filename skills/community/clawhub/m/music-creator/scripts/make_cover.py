#!/usr/bin/env python3
"""
封面图文字合成工具

在 AI 生成的纯画面封面图上叠加中文标题和制作信息，
避免 AI 图像生成的中文乱码问题。

用法：
  python3 make_cover.py \
    --input /tmp/song-cover-raw.jpg \
    --title "我爱小微" \
    --artist "microsnow" \
    --output /tmp/song-cover.jpg
"""

import argparse
import os
import sys


def make_cover(input_path, title, artist, subtitle=None, output_path=None):
    from PIL import Image, ImageDraw, ImageFont, Image as PILImage

    if not os.path.exists(input_path):
        print(f"❌ 文件不存在: {input_path}")
        sys.exit(1)

    # 加载并调整大小
    img = Image.open(input_path).resize((800, 800), Image.LANCZOS)

    # 查找中文字体
    font_path = None
    candidates = [
        '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Black.ttc',
        '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc',
        '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Medium.ttc',
        '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
    ]
    for fp in candidates:
        if os.path.exists(fp):
            font_path = fp
            break

    if not font_path:
        print("❌ 未找到中文字体")
        sys.exit(1)

    # 字体
    title_font = ImageFont.truetype(font_path, 72)
    sub_font = ImageFont.truetype(font_path, 28)
    credit_font = ImageFont.truetype(font_path, 24)

    # 创建叠加层
    overlay = PILImage.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    # 顶部渐变遮罩
    for y in range(220):
        alpha = int(180 * (1 - y / 220))
        overlay_draw.line([(0, y), (800, y)], fill=(0, 0, 0, alpha))

    # 底部渐变遮罩
    for y in range(160):
        alpha = int(160 * (1 - (160 - y) / 160))
        overlay_draw.line([(0, 640 + y), (800, 640 + y)], fill=(0, 0, 0, alpha))

    # 合成
    img_rgba = img.convert('RGBA')
    img_rgba = PILImage.alpha_composite(img_rgba, overlay)
    draw = ImageDraw.Draw(img_rgba)

    # 标题
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    tx = (800 - tw) // 2
    ty = 80
    draw.text((tx + 2, ty + 2), title, fill=(0, 0, 0, 180), font=title_font)
    draw.text((tx, ty), title, fill=(255, 255, 255, 255), font=title_font)

    # 副标题
    if subtitle:
        sub = subtitle
    else:
        sub = "单  曲"
    bbox = draw.textbbox((0, 0), sub, font=sub_font)
    sw = bbox[2] - bbox[0]
    draw.text(((800 - sw) // 2, 170), sub, fill=(220, 220, 220, 220), font=sub_font)

    # 底部制作信息
    credit_y = 720
    credits = [
        f"作词：{artist}",
        f"作曲：{artist}",
        f"演唱：{artist}",
        f"制作人：{artist}",
    ]
    for line in credits:
        bbox = draw.textbbox((0, 0), line, font=credit_font)
        lw = bbox[2] - bbox[0]
        draw.text(((800 - lw) // 2, credit_y), line, fill=(220, 220, 220, 200), font=credit_font)
        credit_y += 32

    # 保存
    final = img_rgba.convert('RGB')
    if not output_path:
        output_path = input_path.replace('-raw', '')
    final.save(output_path, quality=92)
    print(f"✅ 封面已保存: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description='封面图文字合成')
    parser.add_argument('--input', required=True, help='原始封面图路径')
    parser.add_argument('--title', required=True, help='歌曲名/标题')
    parser.add_argument('--artist', required=True, help='艺术家/制作人名')
    parser.add_argument('--subtitle', default=None, help='副标题（默认"单曲"）')
    parser.add_argument('--output', default=None, help='输出路径')

    args = parser.parse_args()
    make_cover(args.input, args.title, args.artist, args.subtitle, args.output)


if __name__ == '__main__':
    main()
