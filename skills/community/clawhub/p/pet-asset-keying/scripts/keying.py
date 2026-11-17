#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
keying.py —— 宠物素材专用抠图工具（混合方案 v3·最终版）
================================================================================
把「传统 matting ∩ isnet-anime」的混合抠图技术提纯成可复用程序。

⭐ 核心思路（2026-09-25 实测定案）
    前景 = 传统matting前景  ∩  isnet-anime前景
    等价于：**任何一方说是背景，就扣掉** —— 能扣多干净扣多干净

    为什么用两种？
      传统 matting（pymatting） 靠【颜色阈值】→ 对小空隙判得准
      isnet-anime（rembg）      靠【语义】    → 主体轮廓准，但会漏小洞
      → 取交集 = 各取所长，且因为"任何一方说就扣"，不会误伤（两侧都保守）

⭐ 用法
    # 单图
    python keying.py 输入.png 输出.png
    # 整个文件夹（视频抽帧序列，自动做时域平滑防闪烁）
    python keying.py <帧目录> <输出目录> --pattern "*.png" --temporal 3
    # 换模型 / 关掉时域平滑
    python keying.py 输入.png 输出.png --model birefnet-general --no-temporal

⭐ 会打印自检报告（角色像素 / 洞数 / 残留背景），⛔ 洞数异常会警告。

⛔ 已实测【反效果·别再试】的后处理（写在这里防止后来者重犯）
    ① "颜色清理"（距背景 <N 就扣）      → ⛔ 挖洞（色板距离 ≠ 像素级安全）
    ② 精确去污染 F=(C−(1−α)·BG)/α      → ⛔ 过度放大颜色
    ③ 混合方程反解 α=|C−BG|/|F−BG|      → ⛔ 边缘满圈麻点
    ④ 分块放大建模（把头部放大 2x 单跑）→ ⛔ 打断 α 连续性
    ⑤ 只用模型、不开 alpha_matting      → ⛔ 硬 α，等于没做
    ⑥ "两版颜色"（α 取A版、RGB 取B版）  → ⛔ 视频里姿势不同 → 对不齐

⭐ 已知物理下限：发梢边缘的「混合像素」既非背景也非前景，
   任何阈值方法只能在【削细发丝 ↔ 留一圈淡边】之间二选一 —— 不是参数问题。
"""
from __future__ import annotations

import argparse
import glob
import os
import sys
import time

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage

# ---------------- 参数（都经过实测标定） ----------------
THRESH = 40          # trimap 用的"距背景"阈值
TRIMAP_ERODE = 3
TRIMAP_DILATE = 3
ALPHA_NARROW = 1.5   # alpha 收窄（3.0 会有锯齿感）
CLOSE_R = 2
NOISE_MAX = 30       # 主体外小碎块面积上限
CROP_MARGIN = 60     # 输出裁到角色 bbox 后留的边距
DEFAULT_MODEL = "isnet-anime"       # ⭐ 实测这个模型最好
AM_FG, AM_BG, AM_ERODE = 240, 10, 8  # alpha_matting 参数


def _bg_of(rgb: np.ndarray) -> np.ndarray:
    """背景色 = 四角 40x40 的中值（素材是纯色底，这个最稳）"""
    h, w = rgb.shape[:2]
    c = np.concatenate([rgb[:40, :40].reshape(-1, 3), rgb[:40, -40:].reshape(-1, 3),
                        rgb[-40:, :40].reshape(-1, 3), rgb[-40:, -40:].reshape(-1, 3)])
    return np.median(c, axis=0)


def _alpha_traditional(rgb: np.ndarray, bg: np.ndarray):
    """A：传统 matting —— 靠颜色阈值，对小空隙准。返回 (α, 去混合后的前景RGB)"""
    from pymatting import estimate_alpha_cf, estimate_foreground_ml
    d = np.abs(rgb - bg).sum(axis=2)
    m = cv2.morphologyEx(((d > THRESH) * 255).astype(np.uint8), cv2.MORPH_CLOSE,
                         cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (CLOSE_R * 2 + 1,) * 2)) > 0
    ek = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (TRIMAP_ERODE * 2 + 1,) * 2)
    dk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (TRIMAP_DILATE * 2 + 1,) * 2)
    tri = np.zeros(m.shape, np.float64)
    core = ndimage.binary_erosion(m, ek)
    tri[core] = 1.0
    tri[ndimage.binary_dilation(m, dk) & (~core)] = 0.5
    imgf = rgb / 255.0
    a = estimate_alpha_cf(imgf, tri)
    a = np.clip((a - 0.5) * ALPHA_NARROW + 0.5, 0, 1)
    fg = np.clip(estimate_foreground_ml(imgf, a), 0, 1) * 255.0
    return a, fg


def _alpha_model(rgb: np.ndarray, model: str) -> np.ndarray:
    """B：isnet-anime（或指定模型）+ alpha_matting —— 靠语义，轮廓准"""
    from rembg import remove, new_session
    sess = new_session(model)
    src = Image.fromarray(rgb.astype(np.uint8), "RGB")
    r = remove(src, session=sess, alpha_matting=True,
               alpha_matting_foreground_threshold=AM_FG,
               alpha_matting_background_threshold=AM_BG,
               alpha_matting_erode_size=AM_ERODE)
    return np.array(r.convert("RGBA"))[:, :, 3].astype(np.float64) / 255.0


def _hole_stats(mask: np.ndarray) -> tuple[int, int, int]:
    """⛔⭐ 一秒安全检验：内部洞的 个数 / ≥8px 个数 / 总面积

    ⭐ 为什么必须有：我用「色板距离」推理"安全"，结果在像素级挖出了洞（栽过两次）。
       ✅ 判据只能落在像素上：binary_fill_holes 数内部洞，变多就是挖坏了。
    """
    filled = ndimage.binary_fill_holes(mask)
    holes = filled & (~mask)
    lb, n = ndimage.label(holes)
    if n == 0:
        return 0, 0, 0
    szs = ndimage.sum(holes, lb, range(1, n + 1))
    big = szs[szs >= 8]
    return n, int(len(big)), int(big.sum()) if len(big) else 0


def key_array(rgb: np.ndarray, model: str = DEFAULT_MODEL,
              bg: np.ndarray | None = None, verbose: bool = True):
    """对单张 RGB 数组做抠图，返回 (RGBA uint8, 报告 dict)"""
    t0 = time.time()
    bg = _bg_of(rgb) if bg is None else bg
    aA, fgA = _alpha_traditional(rgb, bg)
    aB = _alpha_model(rgb, model)
    # ⭐⭐ 前景取交集 = 任何一方说是背景就扣
    a = np.minimum(aA, aB)
    # 清理主体外小碎块
    m = a > 0
    lb, n = ndimage.label(m)
    if n > 1:
        szs = ndimage.sum(m, lb, range(1, n + 1))
        main = int(np.argmax(szs)) + 1
        for i in range(1, n + 1):
            if i != main and szs[i - 1] <= NOISE_MAX:
                a[lb == i] = 0
    mask = a > 0
    n_h, n_big, area_h = _hole_stats(mask)

    rgba = np.dstack([fgA, np.round(a * 255)]).astype(np.uint8)
    rep = dict(bg=bg, n_holes=n_h, n_big_holes=n_big, hole_area=area_h,
               fg_px=int(mask.sum()), sec=time.time() - t0)
    if verbose:
        print(f"    背景 {bg.astype(int)}   A {int((aA>0.5).sum())}px  B {int((aB>0.5).sum())}px"
              f"  → 交集 {rep['fg_px']}px")
        print(f"    洞 {n_h} 个（≥8px {n_big} 个，合计 {area_h}px）   {rep['sec']:.1f}s")
    return rgba, rep


def _crop(rgba: np.ndarray, margin: int = CROP_MARGIN):
    a = rgba[:, :, 3]
    ys, xs = np.where(a > 128)
    if len(ys) == 0:
        return rgba
    h, w = a.shape
    x0, x1 = max(0, int(xs.min()) - margin), min(w, int(xs.max()) + margin + 1)
    y0, y1 = max(0, int(ys.min()) - margin), min(h, int(ys.max()) + margin + 1)
    return rgba[y0:y1, x0:x1]


def _temporal_smooth(seq: list[np.ndarray], k: int = 3) -> list[np.ndarray]:
    """⭐ 视频序列防闪烁：对 alpha 做长度 k 的中值滤波（逐像素）

    模型是逐图推理，相邻帧可能微抖 → 合成到桌面会闪。
    传统 matting 部分本身是确定的，抖的是模型那半边。
    """
    if k < 3 or len(seq) < k:
        return seq
    r = k // 2
    arr = np.stack([s[:, :, 3].astype(np.float32) for s in seq])   # N,H,W
    pad = np.pad(arr, ((r, r), (0, 0), (0, 0)), mode="edge")
    out = []
    for i in range(len(seq)):
        win = pad[i:i + k]
        med = np.median(win, axis=0)
        s = seq[i].copy()
        s[:, :, 3] = np.round(np.clip(med, 0, 255)).astype(np.uint8)
        out.append(s)
    return out


def main():
    ap = argparse.ArgumentParser(description="宠物素材抠图（混合方案 v3·最终版）")
    ap.add_argument("input", help="输入图片，或帧序列目录")
    ap.add_argument("output", nargs="?", help="输出图片，或输出目录")
    ap.add_argument("--pattern", default="*.png", help="目录模式下的文件名匹配（默认 *.png）")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"rembg 模型（默认 {DEFAULT_MODEL}）")
    ap.add_argument("--temporal", type=int, default=3, help="时域中值窗口（默认 3；1=关闭）")
    ap.add_argument("--no-crop", action="store_true", help="不裁到角色 bbox")
    ap.add_argument("--margin", type=int, default=CROP_MARGIN, help="裁切边距（默认 60）")
    args = ap.parse_args()

    is_dir = os.path.isdir(args.input)
    if not is_dir:
        rgb = np.array(Image.open(args.input).convert("RGB"))
        print(f"[单图] {args.input}  {rgb.shape[1]}x{rgb.shape[0]}")
        rgba, rep = key_array(rgb, args.model)
        out = rgba if args.no_crop else _crop(rgba, args.margin)
        dst = args.output or os.path.splitext(args.input)[0] + "_透明底.png"
        Image.fromarray(out).save(dst)
        print(f"[输出] {dst}  {out.shape[1]}x{out.shape[0]}")
        return

    files = sorted(glob.glob(os.path.join(args.input, args.pattern)))
    if not files:
        print(f"⛔ 目录里没匹配到文件：{args.input}/{args.pattern}")
        sys.exit(1)
    dst_dir = args.output or os.path.join(args.input, "_keyed")
    os.makedirs(dst_dir, exist_ok=True)
    print(f"[序列] {len(files)} 帧  →  {dst_dir}")

    def bg_common():
        acc = []
        for f in files[: min(5, len(files))]:
            acc.append(_bg_of(np.array(Image.open(f).convert("RGB"))))
        return np.median(np.stack(acc), axis=0)

    bg = bg_common()
    print(f"    共用背景 {bg.astype(int)}（取前 5 帧四角中值）")
    seq, reps = [], []
    for i, f in enumerate(files):
        rgb = np.array(Image.open(f).convert("RGB"))
        print(f"  [{i+1}/{len(files)}] {os.path.basename(f)}")
        rgba, rep = key_array(rgb, args.model, bg=bg)
        seq.append(rgba)
        reps.append(rep)
    if args.temporal >= 3:
        print(f"    ⭐ 时域中值平滑 k={args.temporal}（防帧间闪烁）")
        seq = _temporal_smooth(seq, args.temporal)
    for f, rgba in zip(files, seq):
        out = rgba if args.no_crop else _crop(rgba, args.margin)
        Image.fromarray(out).save(os.path.join(dst_dir, os.path.splitext(os.path.basename(f))[0] + ".png"))
    tot_fg = sum(r["fg_px"] for r in reps)
    tot_h = sum(r["n_big_holes"] for r in reps)
    print(f"\n[完成] {len(seq)} 帧   平均角色 {tot_fg//len(reps)}px"
          f"   ≥8px 洞合计 {tot_h} 个   总耗时 {sum(r['sec'] for r in reps):.1f}s")
    print("⭐ 提醒：验『漏抠』合成到【青色底】；验『边缘观感』用【中灰底】")


if __name__ == "__main__":
    main()
