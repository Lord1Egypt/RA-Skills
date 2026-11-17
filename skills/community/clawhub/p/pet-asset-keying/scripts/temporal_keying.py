#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
时序投票抠图 · Vote before you intersect
================================================================================
一句话：**让「判定」自己利用时间，而不是事后去抹平痕迹。**

⭐ 差别在哪
    ------------------------------------------------------------------
    逐帧 + 事后平滑（本工具原来的 `--temporal`）
        每帧独立算出 A、B 两个掩膜 → 逐帧取交集 → 最后对 α 做时域中值
        ⛔ 单帧的误判**已经进了结果**，事后中值只能把痕迹抹平（还会把边糊掉）

    ⭐ 判定时就投票（本文件）
        每帧算出 A、B 两个掩膜，先**不交集**
        → 对 A 序列、B 序列**分别**做时域投票（邻居帧多数同意才算前景）
        → 在"时间上已经稳定"的判定上取交集
        → 再估 α 软边
    ------------------------------------------------------------------
⭐ 为什么这更强：单帧误判（比如脚踝被模型判成背景）在邻居帧里是前景 →
   投票之后那个像素**不会被扣掉** ✅ —— 这是事后中值做不到的，因为它只能改 α，改不了判定。

⛔ 代价：投票要有邻居，**首尾要接成环**（本实现按循环处理，适合原地循环动画）；
   非循环素材（下落、落地）首尾那几帧要小心，见 docs/POSTPROCESS.md。

⭐ 用法
    python temporal_keying.py <输入帧目录> <输出目录>
    python temporal_keying.py <帧目录> <输出> --vote 5        # 投票窗口（奇数，默认 3）
    python temporal_keying.py <帧目录> <输出> --no-vote       # 关掉投票 = 逐帧交集，做对照

⭐ 内置自检会打印：被邻居帧**救回来**的像素 / 被邻居帧**否掉**的像素 / 连续 α 的帧间抖动。
   判据是「帧间抖动越小越稳」，但 ⛔ 别只看它 —— 抖动小也可能是被抹平了，必须同时看实心面积。

License: MIT
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

# ⭐ 参数与 pure_bg_keying.py 共用一份，避免两边标定漂移
from pure_bg_keying import (ALPHA_NARROW, AM_BG, AM_ERODE, AM_FG, CLOSE_R,
                            DEFAULT_MODEL, THRESH, TRIMAP_DILATE, TRIMAP_ERODE)

VOTE_K = 3              # 投票窗口（奇数）：邻居帧多数同意才算前景
CROP_MARGIN = 60

_SESSION = None


def _session(model: str):
    """模型只加载一次 —— ⛔ 逐帧 new_session() 会把 168MB 反复读进来，慢几十倍"""
    global _SESSION
    if _SESSION is None:
        from rembg import new_session
        _SESSION = new_session(model)
    return _SESSION


def bg_of(rgb: np.ndarray) -> np.ndarray:
    """背景色 = 四角 40x40 中值（与 pure_bg_keying.py 同一口径）"""
    h, w = rgb.shape[:2]
    c = np.concatenate([rgb[:40, :40].reshape(-1, 3), rgb[:40, -40:].reshape(-1, 3),
                        rgb[-40:, :40].reshape(-1, 3), rgb[-40:, -40:].reshape(-1, 3)])
    return np.median(c, axis=0)


def mask_traditional(rgb: np.ndarray, bg: np.ndarray) -> np.ndarray:
    """A：颜色阈值。⚠️ 这里只要「判定」（二值），α 留到最后统一估"""
    d = np.abs(rgb.astype(np.int16) - bg.astype(np.int16)).sum(axis=2)
    m = cv2.morphologyEx(((d > THRESH) * 255).astype(np.uint8), cv2.MORPH_CLOSE,
                         cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (CLOSE_R * 2 + 1,) * 2)) > 0
    return m


def mask_model(rgb: np.ndarray, model: str = DEFAULT_MODEL) -> np.ndarray:
    """B：语义分割 + alpha_matting —— 再二值化当判定用"""
    from rembg import remove
    r = remove(Image.fromarray(rgb.astype(np.uint8), "RGB"), session=_session(model),
               alpha_matting=True, alpha_matting_foreground_threshold=AM_FG,
               alpha_matting_background_threshold=AM_BG, alpha_matting_erode_size=AM_ERODE)
    return np.array(r.convert("RGBA"))[:, :, 3] > 128


def vote(masks: list, k: int = VOTE_K) -> list:
    """⭐ 时域投票：一个像素要**超过一半**的窗口帧都说是前景，才算前景

    ⭐ 首尾接成环（邻居从序列两端取）—— 原地循环动画的接缝才不会断。
    ⛔ 非循环素材（下落 / 落地）首尾帧会拿到对面那一端的邻居，见文档里的注意事项。
    """
    if k < 3 or len(masks) < 2:
        return masks
    r = k // 2
    a = np.stack([m.astype(np.uint8) for m in masks])           # N,H,W
    if len(a) > r:
        pad = np.concatenate([a[-r:], a, a[:r]])
    else:                                                        # 帧数比窗口还少 → 用边缘帧补齐
        pad = np.concatenate([np.repeat(a[:1], r, 0), a, np.repeat(a[-1:], r, 0)])
    return [pad[i:i + k].sum(axis=0) * 2 > k for i in range(len(a))]


def rebuild_trimap(inter: np.ndarray, tri_erode: int = TRIMAP_ERODE,
                   tri_dilate: int = TRIMAP_DILATE) -> np.ndarray:
    """把投票后的二值交集还原成 trimap，交给 matting 估 α

    做法与 pure_bg_keying.py 完全一致，只是把「颜色阈值掩膜」换成了「投票后的交集」：
        确定前景 = 交集内缩 TRIMAP_ERODE
        未知     = 外扩 TRIMAP_DILATE 那一圈（⭐ 只有一圈，薄）
        确定背景 = 其余

    ⛔⛔ **未知带一定要薄。** 我第一版写成"凡模型说前景、又不在交集外扩区内的都算未知"，
        结果未知区变成一大片，closed-form matting 直接慢十倍以上（6 帧跑了 3 分半还没完）。
        CF 求解的代价基本跟未知区面积走 —— 薄环是这条链能跑起来的关键。
    """
    er = cv2.erode(inter.astype(np.uint8),
                   cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (tri_erode * 2 + 1,) * 2)) > 0
    dl = cv2.dilate(inter.astype(np.uint8),
                    cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (tri_dilate * 2 + 1,) * 2)) > 0
    tri = np.zeros(inter.shape, np.float32)
    tri[dl & (~er)] = 0.5
    tri[er] = 1.0
    return tri


def key_sequence(frames: list, bg: np.ndarray | None = None, model: str = DEFAULT_MODEL,
                 k: int = VOTE_K, use_vote: bool = True, verbose: bool = True):
    """整段序列抠图。返回 (RGBA 列表, 报告 dict)

    frames：RGB uint8 数组的列表（顺序 = 时间顺序，循环动画请首尾相接）
    """
    from pymatting import estimate_alpha_cf, estimate_foreground_ml
    t0 = time.time()
    bg = bg_of(frames[0]) if bg is None else np.asarray(bg)
    n = len(frames)

    # ---------- ① 逐帧两个判定（先不交集！）----------
    A = [mask_traditional(f, bg) for f in frames]
    B = [mask_model(f, model) for f in frames]

    # ---------- ② 两个序列各自时域投票 ----------
    if use_vote:
        Av, Bv = vote(A, k), vote(B, k)
    else:
        Av, Bv = A, B

    # ---------- ③ 在"稳定后的判定"上取交集 ----------
    inter = [Av[i] & Bv[i] for i in range(n)]

    # ---------- ④ 估 α，出结果 ----------
    out, rows = [], []
    for i, R in enumerate(frames):
        tri = rebuild_trimap(inter[i])              # 与主程序同构：细环未知带
        img = R.astype(np.float64) / 255.0
        a = estimate_alpha_cf(img, tri)
        a = np.clip((a - 0.5) * ALPHA_NARROW + 0.5, 0, 1)   # 与主程序一致：收窄 → 硬一点的边
        fg = np.clip(estimate_foreground_ml(img, a), 0, 1) * 255.0
        rgba = np.dstack([fg.astype(np.uint8), np.round(a * 255).astype(np.uint8)])
        out.append(rgba)
        rows.append(dict(i=i, fg=int((a > 0.5).sum()), alpha_sum=float(a.sum())))

    # ---------- ⑤ 自检 ----------
    rep = dict(bg=bg, n=n, k=k, use_vote=use_vote, sec=time.time() - t0, frames=rows)
    if use_vote:
        rescued = int(sum((Av[i] & ~A[i]).sum() for i in range(n)))
        killed = int(sum((A[i] & ~Av[i]).sum() for i in range(n)))
        rep.update(rescued=rescued, voted_out=killed)
    if n >= 2:
        diffs = [float(np.abs(out[i][:, :, 3].astype(np.int16)
                              - out[i + 1][:, :, 3].astype(np.int16)).mean()) for i in range(n - 1)]
        rep["jitter"] = float(np.mean(diffs))
    if verbose:
        print(f"    背景 {bg.astype(int)}   {n} 帧   {rep['sec']:.1f}s")
        if use_vote:
            print(f"    ⭐ 投票 k={k}：被邻居帧**救回来** {rep['rescued']}px"
                  f"   被邻居帧**否掉** {rep['voted_out']}px")
        if "jitter" in rep:
            print(f"    连续 α 的帧间抖动 {rep['jitter']:.2f}（越小越稳；⛔ 别单看它）")
    return out, rep


def _crop(rgba: np.ndarray, margin: int = CROP_MARGIN) -> np.ndarray:
    ys, xs = np.where(rgba[:, :, 3] > 128)
    if len(ys) == 0:
        return rgba
    h, w = rgba.shape[:2]
    return rgba[max(0, int(ys.min()) - margin):min(h, int(ys.max()) + margin + 1),
                max(0, int(xs.min()) - margin):min(w, int(xs.max()) + margin + 1)]


def main():
    ap = argparse.ArgumentParser(description="时序投票抠图：先在判定层投票，再取交集")
    ap.add_argument("input", help="输入帧目录")
    ap.add_argument("output", help="输出目录")
    ap.add_argument("--pattern", default="*.png")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--vote", type=int, default=VOTE_K, help=f"投票窗口，奇数（默认 {VOTE_K}）")
    ap.add_argument("--no-vote", action="store_true", help="关掉投票 = 逐帧交集（对照组）")
    ap.add_argument("--no-crop", action="store_true")
    ap.add_argument("--margin", type=int, default=CROP_MARGIN)
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(a.input, a.pattern)))
    if not files:
        print(f"⛔ 目录里没匹配到文件：{a.input}/{a.pattern}")
        sys.exit(1)
    os.makedirs(a.output, exist_ok=True)
    frames = [np.array(Image.open(f).convert("RGB")) for f in files]
    print(f"[序列] {len(frames)} 帧  {frames[0].shape[1]}x{frames[0].shape[0]}  →  {a.output}")
    out, rep = key_sequence(frames, model=a.model, k=a.vote, use_vote=not a.no_vote)
    for f, rgba in zip(files, out):
        img = rgba if a.no_crop else _crop(rgba, a.margin)
        Image.fromarray(img).save(os.path.join(a.output,
                                              os.path.splitext(os.path.basename(f))[0] + ".png"))
    print(f"[完成] {len(out)} 帧   平均实心 {sum(r['fg'] for r in rep['frames'])//len(out)}px")
    print("⭐ 提醒：验『漏抠』合成到【青色底】；验『边缘观感』用【中灰底】")


if __name__ == "__main__":
    main()
