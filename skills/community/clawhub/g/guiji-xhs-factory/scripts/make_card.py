#!/usr/bin/env python3
"""小红书信息图生成器。

用法:
  python3 make_card.py --title "标题" --items "内容1" "内容2" --output card.png
  python3 make_card.py --preset tutorial  # 使用预设配色
  python3 make_card.py --batch config.json  # 批量生成
"""

import argparse
import json
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("需要安装 Pillow: pip3 install Pillow", file=sys.stderr)
    sys.exit(1)

W, H = 1080, 1440  # 3:4 竖屏

PRESETS = {
    "default": {"bg": (20, 20, 35), "accent": (100, 200, 255)},
    "tutorial": {"bg": (15, 40, 25), "accent": (0, 220, 120)},
    "case": {"bg": (40, 20, 15), "accent": (255, 150, 50)},
    "secret": {"bg": (25, 15, 40), "accent": (180, 100, 255)},
    "cover": {"bg": (15, 30, 55), "accent": (0, 180, 255)},
}


def get_fonts():
    """查找系统中文字体。"""
    paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return (
                    ImageFont.truetype(p, 52),
                    ImageFont.truetype(p, 30),
                    ImageFont.truetype(p, 24),
                )
            except Exception:
                continue
    default = ImageFont.load_default()
    return default, default, default


def make_card(title, items, output, preset="default", bg_color=None, accent=None):
    """生成一张信息图。"""
    p = PRESETS.get(preset, PRESETS["default"])
    bg = tuple(bg_color) if bg_color else p["bg"]
    ac = tuple(accent) if accent else p["accent"]

    title_font, body_font, small_font = get_fonts()
    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)

    # 左侧强调色竖条 + 标题
    draw.rectangle([60, 80, 68, 200], fill=ac)
    draw.text((90, 100), title, fill=(255, 255, 255), font=title_font)

    # 分隔线
    draw.rectangle([80, 180, W - 80, 184], fill=ac)

    # 内容列表
    y = 240
    for item in items:
        if item == "":
            y += 20
            continue
        if item.startswith("##"):
            draw.text((80, y), item[2:], fill=ac, font=body_font)
            y += 55
        elif item.startswith("--"):
            draw.text((100, y), item[2:], fill=(160, 160, 160), font=small_font)
            y += 40
        else:
            draw.text((100, y), item, fill=(220, 220, 220), font=body_font)
            y += 52

    img.save(output)
    print(f"✅ 已保存: {output}")


def batch_generate(config_path):
    """从 JSON 配置批量生成。"""
    with open(config_path) as f:
        config = json.load(f)
    for card in config.get("cards", []):
        make_card(
            title=card["title"],
            items=card["items"],
            output=card["output"],
            preset=card.get("preset", "default"),
            bg_color=card.get("bg_color"),
            accent=card.get("accent"),
        )


def main():
    parser = argparse.ArgumentParser(description="小红书信息图生成器")
    parser.add_argument("--title", help="标题文字")
    parser.add_argument("--items", nargs="+", help="内容列表（用引号包裹）")
    parser.add_argument("--output", default="card.png", help="输出文件路径")
    parser.add_argument(
        "--preset",
        default="default",
        choices=list(PRESETS.keys()),
        help="配色预设",
    )
    parser.add_argument("--batch", help="批量生成配置文件路径")
    args = parser.parse_args()

    if args.batch:
        batch_generate(args.batch)
    elif args.title and args.items:
        make_card(args.title, args.items, args.output, args.preset)
    else:
        parser.print_help()
        print("\n示例:")
        print('  python3 make_card.py --title "测试" --items "项目1" "项目2" --output test.png')
        print(f"  可用预设: {', '.join(PRESETS.keys())}")


if __name__ == "__main__":
    main()
