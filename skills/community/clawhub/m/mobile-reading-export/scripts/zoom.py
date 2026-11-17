# -*- coding: utf-8 -*-
"""裁剪指定区域并放大，便于肉眼核对；同时输出该区域内的暗像素游程分布。"""
import sys
from PIL import Image

src = sys.argv[1]
out = sys.argv[2]
x0, y0, x1, y1 = [int(v) for v in sys.argv[3:7]]
scale = float(sys.argv[7]) if len(sys.argv) > 7 else 2.0

im = Image.open(src).convert('RGB')
crop = im.crop((x0, y0, x1, y1))
w, h = crop.size
crop = crop.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
crop.save(out, optimize=True)
print('WROTE', out, crop.size)

# 游程分析：在若干 y 上找暗像素区间
px = im.load()
for y in range(y0, y1, max(1, (y1 - y0) // 6)):
    runs = []
    start = None
    for x in range(im.size[0]):
        r, g, b = px[x, y]
        dark = (r < 200 or g < 200 or b < 200)
        if dark and start is None:
            start = x
        elif not dark and start is not None:
            if x - start >= 1:
                runs.append((start, x - 1))
            start = None
    if start is not None:
        runs.append((start, im.size[0] - 1))
    tail = runs[-3:] if len(runs) > 3 else runs
    print(f"  y={y} runs={len(runs)} last={tail}")
