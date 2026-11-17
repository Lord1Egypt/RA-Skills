# -*- coding: utf-8 -*-
"""渲染几张「考场外」的新数字图片(与训练不同的字体与随机种子),供 predict 演示。

用法: python vision/make_samples.py
输出: data/samples/sample_<i>_<数字>.png
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

_HERE = Path(__file__).resolve().parent
OUT = _HERE.parent / "data" / "samples"


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    OUT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(2026)
    fonts = []
    # 考场外字体:训练时从未见过,专测分布外泛化
    for name in ["comic.ttf", "segoepr.ttf", "segoesc.ttf"]:
        try:
            fonts.append(ImageFont.truetype(name, 42))
        except Exception:
            continue
    if not fonts:
        fonts = [ImageFont.load_default()]
    digits = "73019"
    for i, d in enumerate(digits):
        big = 64
        img = Image.new("L", (big, big), 0)
        ImageDraw.Draw(img).text((big // 2, big // 2), d, fill=255,
                                 font=rng.choice(fonts), anchor="mm")
        img = img.rotate(rng.uniform(-20, 20), resample=Image.BILINEAR, fillcolor=0)
        img = img.resize((28, 28), Image.BILINEAR)
        img.save(OUT / f"sample_{i}_{d}.png")
    print(f"已渲染 {len(digits)} 张样例到 {OUT}")


if __name__ == "__main__":
    main()
