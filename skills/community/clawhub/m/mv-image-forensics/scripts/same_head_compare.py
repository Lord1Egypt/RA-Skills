#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""same_head_compare.py — 同角色高归一 + 原像素 1:1 并排拼图

为什么需要它：
  不归一化尺寸就对比「哪张更清楚」是无意义的 —— 大图看起来糊，往往只是因为你
  把更少的像素拉伸到了同样大。

做法（按 SKILL.md §1.1）：
  1. 每张图取**前景最大连通域** bbox（⛔ 不是整体 bbox，漂浮装饰件会把它拉大）
  2. 按角色高统一缩放（INTER_AREA，只在缩小时用）
  3. 以原像素 1:1 裁顶部同一区域并排
  4. ⛔ 裁出来的小块**不再放大** —— LANCZOS 会把软边补成假锐边

用法：
  python same_head_compare.py --out cmp.png --tile-w 260 --body-h 900 ^
      --img "锚图=C:/a/P0.png" --img "F1=C:/a/F1.png" --img "F2=C:/a/F2.png"

  # 有 alpha 通道时优先用 alpha，没有就按绿幕色差找前景
  python same_head_compare.py --out cmp.png --img "A=x.png" --img "B=y.png" --top 0.42
"""
import argparse
import os
import sys

import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\msyh.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
]


def load_font(size):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def imread_any(path):
    """中文路径安全；返回 BGR 三通道 + 可选 alpha。"""
    if not os.path.exists(path):
        raise SystemExit(f"file not found: {path}")
    with open(path, "rb") as f:
        buf = np.frombuffer(f.read(), np.uint8)
    im = cv2.imdecode(buf, cv2.IMREAD_UNCHANGED)
    if im is None:
        raise SystemExit(f"decode failed: {path}")
    if im.ndim == 2:
        return cv2.cvtColor(im, cv2.COLOR_GRAY2BGR), None
    if im.shape[2] == 4:
        return im[:, :, :3].copy(), im[:, :, 3].copy()
    return im[:, :, :3].copy(), None


def fg_mask(bgr, alpha=None, thr=200):
    """前景 mask。返回 (mask, 来源说明)。

    ⚠️ 实测坑（2026-10-28）：**「有 alpha 通道」≠「是真透明底」。**
    生成通道下来的 PNG 经常是「纯绿底 + alpha 全 255」—— alpha 形同虚设。
    只信 alpha 会把整幅图当成角色，于是「角色高」被算成画幅高，归一化全错。
    （实例：锚图 P0 是 1080×1920 RGBA，alpha min=max=255，四角 BGR=(0,255,0)。）

    ⇒ 只有 alpha 里**真的存在透明区域**时才用 alpha，否则回退绿幕色差。
    """
    if alpha is not None:
        transparent_ratio = float((alpha < thr).mean())
        if transparent_ratio > 0.02:
            return alpha.astype(np.uint8) > thr, f"alpha ({transparent_ratio * 100:.1f}% transparent)"
    B, G, R = bgr[:, :, 0].astype(int), bgr[:, :, 1].astype(int), bgr[:, :, 2].astype(int)
    # 绿幕：G 明显高且比 R/B 都高出一截
    green = (G > 90) & ((G - R) > 45) & ((G - B) > 45)
    return ~green, f"green-screen chroma ({green.mean() * 100:.1f}% green)"


def largest_bbox(mask):
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    if n <= 1:
        return None
    a = st[1:, cv2.CC_STAT_AREA]
    m = 1 + int(np.argmax(a))
    x, y, w, h = [int(st[m, c]) for c in (cv2.CC_STAT_LEFT, cv2.CC_STAT_TOP,
                                          cv2.CC_STAT_WIDTH, cv2.CC_STAT_HEIGHT)]
    return x, y, w, h


def normalize_top(path, body_h, top_frac, tile_w, force_body_h=None):
    bgr, alpha = imread_any(path)
    m, src_of_mask = fg_mask(bgr, alpha)
    bb = largest_bbox(m)
    if bb is None:
        raise SystemExit(f"no foreground found: {path}")
    x, y, w, h = bb
    hw, hh = bgr.shape[1], bgr.shape[0]
    cover = (w * h) / float(hw * hh)
    warn = ""
    if cover >= 0.95 and force_body_h is None:
        warn = (f"  ⚠️ 前景 bbox 覆盖 {cover * 100:.1f}% 画幅 —— 分割可能失效"
                f"（纯色底但不是绿幕？），本张的归一化不可信")
    if force_body_h:
        h = force_body_h
        warn = f"  (角色高被 --force-body-h 覆盖为 {force_body_h}px)"
    s = body_h / float(h)
    nw, nh = max(1, int(round(bgr.shape[1] * s))), max(1, int(round(bgr.shape[0] * s)))
    # 只在缩小时用 INTER_AREA；需要放大时也用它，避免造出假锐边
    im2 = cv2.resize(bgr, (nw, nh), interpolation=cv2.INTER_AREA)

    cx = int(round((x + w / 2.0) * s))
    y2 = int(round(y * s))
    th = int(body_h * top_frac)
    x0 = max(0, cx - tile_w // 2)
    x1 = min(nw, x0 + tile_w)
    x0 = max(0, x1 - tile_w)
    crop = im2[y2:y2 + th, x0:x1]
    if crop.shape[1] < tile_w:                      # 窄图补边，别拉伸
        pad = tile_w - crop.shape[1]
        crop = np.pad(crop, ((0, 0), (0, pad), (0, 0)), mode="edge")
    if crop.shape[0] < th:
        pad = th - crop.shape[0]
        crop = np.pad(crop, ((0, pad), (0, 0), (0, 0)), mode="edge")
    return crop, h, bb, warn, src_of_mask


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--img", action="append", required=True, metavar="LABEL=PATH")
    ap.add_argument("--out", required=True)
    ap.add_argument("--body-h", type=int, default=900, help="归一后的角色高（px）")
    ap.add_argument("--tile-w", type=int, default=260, help="每格宽度（px）")
    ap.add_argument("--top", type=float, default=0.42, help="取角色顶部多少比例")
    ap.add_argument("--gap", type=int, default=14)
    ap.add_argument("--force-body-h", action="append", default=[], metavar="LABEL=PX",
                    help="手动指定某张的角色高，绕过分割（分割失效时用）")
    ap.add_argument("--title", default="★ 角色高归一 + 原像素 1:1（未放大）")
    args = ap.parse_args()

    forced = {}
    for spec in args.force_body_h:
        if "=" not in spec:
            raise SystemExit(f"--force-body-h must be LABEL=PX, got: {spec}")
        k, v = spec.split("=", 1)
        forced[k] = int(v)

    items = []
    warned = False
    for spec in args.img:
        if "=" not in spec:
            raise SystemExit(f"--img must be LABEL=PATH, got: {spec}")
        label, path = spec.split("=", 1)
        crop, body_h_src, bb, warn, src_of_mask = normalize_top(
            path, args.body_h, args.top, args.tile_w, forced.get(label))
        items.append((label, crop, body_h_src, bb))
        print(f"{label:16s} src_body_h={body_h_src:5d}  mask={src_of_mask}  bbox={bb}{warn}")
        if warn and "⚠️" in warn:
            warned = True
    if warned:
        print("\n⚠️  有图的前景分割失效 —— 归一化结果不可信。"
              "用 --force-body-h LABEL=<px> 手动指定角色高后重跑。")

    tile_h = items[0][1].shape[0]
    head, lbl_h = 58, 26
    W = (args.tile_w + args.gap) * len(items) + args.gap
    H = head + lbl_h + tile_h + 40
    canvas = Image.new("RGB", (W, H), (18, 18, 22))
    d = ImageDraw.Draw(canvas)
    f_t, f_s = load_font(22), load_font(16)
    d.text((args.gap, 12), args.title, font=f_t, fill=(240, 240, 245))

    x = args.gap
    for label, crop, body_h_src, bb in items:
        d.text((x, head - 4), label, font=f_s, fill=(255, 205, 120))
        yy = head + lbl_h
        canvas.paste(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), (x, yy))
        d.rectangle([x, yy, x + args.tile_w - 1, yy + tile_h - 1], outline=(90, 90, 100))
        d.text((x, yy + tile_h + 4), f"src body_h {body_h_src}", font=f_s, fill=(185, 185, 195))
        x += args.tile_w + args.gap

    canvas.save(args.out)
    print(f"\nsaved {canvas.size[0]}x{canvas.size[1]}  {args.out}")


if __name__ == "__main__":
    main()
