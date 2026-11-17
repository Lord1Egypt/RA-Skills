#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pixel_forensics.py — 「是谁把我的图弄糊的」取证器

为什么不看指标：
  指标不含「谁改的」这个信息。用指标回答责任问题，只会编出假根因。
  唯一能分辨「生成端本来就软」和「后处理弄糊的」的方法是：
  **拿生成端的原始档，跟交付图做逐位 diff。**

关键口径（按 SKILL.md §3.2）：
  - 只在**共同前景 mask 内**统计。背景差异（floodFill 刷纯绿）会淹没角色差异，
    实测全图 diff>8 占 76%，全部落在绿幕上，与角色无关。
  - 源多半经过补边 / 绿幕归一 ⇒ 先用 --pad-w 复现那一步，再比。
  - 同时核「缩放到底有没有发生」：比源尺寸 vs 交付尺寸，
    ⛔ 不要比角色高比值 —— 角色高会因裁切/补边而变，尺寸不会。

用法：
  python pixel_forensics.py --src C:/.../raw_F1.png --del C:/.../LU01_F1.png --pad-w 1080
  python pixel_forensics.py --src raw.png --del out.png            # 不补边
  python pixel_forensics.py --src raw.png --del out.png --json r.json

判定参考（实测 LU01）：
  diff==0 占比 97%+      ⇒ 后处理对角色像素零损伤，糊来自生成端
  diff==0 占比 60%~90%   ⇒ 中间态，看 p99：p99 ≤ 15 仍是重采样损失，不是重绘
  diff==0 占比 < 50%     ⇒ 交付图被重绘/大幅改色，逐位比对已不适用
"""
import argparse
import json
import os
import sys

import numpy as np
import cv2


def imread_any(path):
    if not os.path.exists(path):
        raise SystemExit(f"file not found: {path}")
    with open(path, "rb") as f:
        buf = np.frombuffer(f.read(), np.uint8)
    im = cv2.imdecode(buf, cv2.IMREAD_UNCHANGED)
    if im is None:
        raise SystemExit(f"decode failed: {path}")
    if im.ndim == 2:
        return cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
    return im[:, :, :3].copy()


def fg_mask(bgr):
    """绿幕色差前景。真 alpha 素材请自行替换为 alpha>200。"""
    B, G, R = bgr[:, :, 0].astype(int), bgr[:, :, 1].astype(int), bgr[:, :, 2].astype(int)
    green = (G > 90) & ((G - R) > 45) & ((G - B) > 45)
    return ~green


def pad_to_width(src, target_w):
    """复现「用两侧边缘的中位色补边到目标宽」这一步。"""
    h, w = src.shape[:2]
    if w >= target_w:
        return src, (0, 0)
    l = (target_w - w) // 2
    r = target_w - w - l
    eL = np.median(src[:, :4], axis=1).astype(np.uint8)[:, None, :]
    eR = np.median(src[:, -4:], axis=1).astype(np.uint8)[:, None, :]
    out = np.concatenate([np.repeat(eL, l, axis=1), src, np.repeat(eR, r, axis=1)], axis=1)
    return out, (l, r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="生成端原始档")
    ap.add_argument("--del", dest="deliver", required=True, help="交付图")
    ap.add_argument("--pad-w", type=int, default=0, help="复现补边到该宽度再做比对；0=不补")
    ap.add_argument("--pad-h", type=int, default=0, help="复现纵向 resize 到该高度；0=不 resize")
    ap.add_argument("--label", default="")
    ap.add_argument("--json", default="")
    args = ap.parse_args()

    src = imread_any(args.src)
    dlv = imread_any(args.deliver)
    sh, sw = src.shape[:2]
    dh, dw = dlv.shape[:2]

    rec = {"src_size": [sw, sh], "deliver_size": [dw, dh],
           "scale_x": round(dw / sw, 4), "scale_y": round(dh / sh, 4)}

    print(f"src      : {sw}x{sh}")
    print(f"delivered: {dw}x{dh}")
    print(f"scale    : x {rec['scale_x']}  y {rec['scale_y']}")

    # ── 缩放检测（比尺寸，不比角色高）
    no_resize = (sh == dh) and (sw == dw)
    print(f"resize?  : {'NO — 尺寸完全相同' if no_resize else 'YES/PADDED — 见下'}")

    # ── 复现处理链
    work, pad = src, (0, 0)
    if args.pad_w:
        work, pad = pad_to_width(work, args.pad_w)
        print(f"pad_w    : → {work.shape[1]}x{work.shape[0]}  (left {pad[0]} / right {pad[1]})")
    if args.pad_h and work.shape[0] != args.pad_h:
        work = cv2.resize(work, (work.shape[1], args.pad_h), interpolation=cv2.INTER_LANCZOS4)
        print(f"pad_h    : → resize 到高 {args.pad_h}（INTER_LANCZOS4）")
        rec["reproduced_resize"] = True

    if work.shape[:2] != dlv.shape[:2]:
        raise SystemExit(
            f"shape mismatch after repro: src {work.shape[1]}x{work.shape[0]} "
            f"vs del {dw}x{dh} — 用 --pad-w / --pad-h 复现处理链，或确认两张图真的是同一个源")

    # ── 共同前景内逐位 diff
    m = fg_mask(work) & fg_mask(dlv)
    n = int(m.sum())
    if n == 0:
        raise SystemExit("no common foreground pixels — 这两张图不是同一个角色/同一机位")

    diff = np.abs(work.astype(np.int16) - dlv.astype(np.int16)).max(axis=2)
    inside = diff[m]
    whole = (diff > 8)

    zero_ratio = float((inside == 0).mean())
    rec.update({
        "common_fg_px": n,
        "fg_mean_diff": round(float(inside.mean()), 4),
        "fg_p99_diff": float(np.percentile(inside, 99)),
        "fg_max_diff": int(inside.max()),
        "fg_zero_ratio": round(zero_ratio, 4),
        "whole_diff_gt8_ratio": round(float(whole.mean()), 4),
    })

    print()
    print(f"common fg px     : {n:,}")
    print(f"fg mean diff     : {inside.mean():.4f}")
    print(f"fg p99 / max     : {np.percentile(inside, 99):.2f} / {inside.max()}")
    print(f"fg diff==0 ratio : {zero_ratio * 100:.2f}%     ← 判据")
    print(f"whole diff>8     : {whole.mean() * 100:.2f}%   (背景键控造成，与角色无关)")

    if zero_ratio >= 0.95:
        verdict = "后处理对角色像素零损伤 ⇒ 糊来自生成端"
    elif zero_ratio >= 0.60:
        verdict = "中间态：有重采样损失但没重绘。看 p99 是否 ≤ 15 再定性"
    else:
        verdict = "交付图被重绘或大幅改色 ⇒ 逐位比对不适用，改用结构相似度 + 目检"
    print(f"\nVERDICT: {verdict}")
    rec["verdict"] = verdict
    if args.label:
        rec["label"] = args.label

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(rec, f, ensure_ascii=False, indent=2)
        print(f"saved {args.json}")


if __name__ == "__main__":
    main()
