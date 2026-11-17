# -*- coding: utf-8 -*-
"""
生成简历分享封面图 (1200x630)，用于微信 og:image / 链接卡片配图。
依赖: pip install Pillow  （用 venv 解释器运行: .../python/envs/default/Scripts/python.exe）
字体: Windows C:/Windows/Fonts/msyh.ttc (雅黑, 注意是 .ttc 不是 .ttf)

用法:
  python gen_cover.py --name "您的姓名" --title "AI博士 · 数据科学家" \
        --tags "10年+ 大厂 AI 落地实战派" --extra "公司A / 公司B / 公司C" --out cover.png
"""
import argparse
import os
from PIL import Image, ImageDraw, ImageFont

FONT = "C:/Windows/Fonts/msyh.ttc"
FONT_B = "C:/Windows/Fonts/msyhbd.ttc"


def font(sz, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, sz)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="您的姓名")
    ap.add_argument("--title", default="AI博士 · 数据科学家")
    ap.add_argument("--tags", default="10年+ 大厂 AI 落地实战派")
    ap.add_argument("--extra", default="公司A / 公司B / 公司C")
    ap.add_argument("--out", default="cover.png")
    a = ap.parse_args()

    W, H = 1200, 630
    img = Image.new("RGB", (W, H), "#0b1220")
    d = ImageDraw.Draw(img)

    # 渐变深蓝底
    for y in range(H):
        t = y / H
        r = int(11 + t * 10)
        g = int(18 + t * 22)
        b = int(32 + t * 40)
        d.line([(0, y), (W, y)], fill=(r, g, b))

    # 左侧竖条装饰
    d.rectangle([60, 230, 66, 400], fill="#38bdf8")

    # 文案
    d.text((92, 200), a.name, font=font(76, True), fill="#ffffff")
    d.text((94, 300), a.title, font=font(34, False), fill="#7dd3fc")
    d.text((94, 372), a.tags, font=font(28, False), fill="#cbd5e1")
    d.text((94, 470), a.extra, font=font(24, False), fill="#94a3b8")

    # 右上角小标
    d.text((W - 360, 70), "个人简历 · 对话版", font=font(22, False), fill="#64748b")

    img.save(a.out)
    print("cover saved:", os.path.abspath(a.out))


if __name__ == "__main__":
    main()
