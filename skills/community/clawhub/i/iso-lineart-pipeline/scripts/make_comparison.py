#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
make_comparison.py —— 对照组版

把任意几张图并排 + 底部给游戏尺寸缩略档。
判线稿好不好，必须同时看「1:1 细节」和「240px 实际尺寸」两档：
很多问题在 1:1 看不见，在 240px 才暴露；反过来也一样。

用法：
    python make_comparison.py --out board.png \
        --item "旧:before.png" --item "新:after.png" --item "参考:ref.jpg"

    # 或者直接给文件名，标题自动用文件名
    python make_comparison.py --out board.png before.png after.png ref.jpg
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont


def load_font(size):
    for p in (r"C:/Windows/Fonts/msyh.ttc", r"C:/Windows/Fonts/msyh.ttf",
              "/System/Library/Fonts/PingFang.ttc",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                pass
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="board.png")
    ap.add_argument("--cell", type=int, default=600, help="每格边长")
    ap.add_argument("--thumb", type=int, default=220, help="底部缩略档边长")
    ap.add_argument("--title", default="")
    ap.add_argument("--item", action="append", default=[],
                    help="标题:路径，可重复")
    ap.add_argument("paths", nargs="*", help="不带标题的图片路径")
    a = ap.parse_args()

    items = []
    for it in a.item:
        title, _, path = it.partition(":")
        items.append((title, path))
    for p in a.paths:
        items.append((os.path.splitext(os.path.basename(p))[0], p))
    if not items:
        sys.exit("没有输入图。用法见文件头。")

    C, PAD = a.cell, 26
    TOP = 96 if a.title else 46
    BOT = 76 + a.thumb
    W = PAD * (len(items) + 1) + C * len(items)
    H = TOP + C + BOT
    ft, fs = load_font(32), load_font(22)
    board = Image.new("RGB", (W, H), (245, 242, 240))
    d = ImageDraw.Draw(board)
    if a.title:
        d.text((PAD, 26), a.title, font=ft, fill=(30, 26, 24))

    for i, (title, path) in enumerate(items):
        x = PAD + i * (C + PAD)
        if os.path.exists(path):
            im = Image.open(path).convert("RGB").resize((C, C), Image.LANCZOS)
        else:
            im = Image.new("RGB", (C, C), (215, 215, 215))
            d.text((x + 10, TOP + 10), "missing", font=fs, fill=(150, 60, 60))
        board.paste(im, (x, TOP))
        d.rectangle([x, TOP, x + C, TOP + C], outline=(200, 194, 190))
        d.text((x, TOP + C + 12), title, font=fs, fill=(60, 54, 50))

    d.text((PAD, TOP + C + 52), f"实际尺寸 {a.thumb}px", font=fs, fill=(96, 90, 86))
    for i, (_, path) in enumerate(items):
        if not os.path.exists(path):
            continue
        x = PAD + i * (C + PAD)
        sm = Image.open(path).convert("RGB").resize((a.thumb, a.thumb), Image.LANCZOS)
        board.paste(sm, (x + 6, TOP + C + 76))

    board.save(a.out)
    print(f"{a.out}  {board.size[0]}x{board.size[1]}  {len(items)} 格")


if __name__ == "__main__":
    main()
