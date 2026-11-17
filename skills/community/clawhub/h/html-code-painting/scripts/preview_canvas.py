#!/usr/bin/env python3
"""
preview_canvas.py — 无浏览器环境 Canvas 渲染管线 Python 复刻模板（html-code-painting 技能配套）

用途：沙盒无 Chromium/无头浏览器时，把作品 HTML 里 Canvas 的 JS 绘制逻辑逐笔翻译到
本脚本「翻译区」，用 Pillow+numpy 生成 PNG 预览图做视觉自查。
方法与陷阱详见 references/python-preview.md（必读，尤其 rand 消耗顺序一节）。

用法：
    python preview_canvas.py            # 按下方配置生成预览
    python preview_canvas.py --outdir /tmp/preview   # 指定输出目录

输出（默认 ./preview_out/）：
    full.png   全图原尺寸       → 评估整体色调/构图/密度
    thumb.png  25% 缩览         → 明度大关系（对应"眯眼测试"）
    zoom_center.png zoom_fg.png 视觉中心/前景 2x 放大 → 笔触与细节抽查

依赖：numpy、Pillow（pip install numpy pillow）

翻译守则（务必遵守，详见手册）：
  1. Rng 与 JS mulberry32 逐步一致（含 & M32）；grain 等独立种子的层单独建 Rng。
  2. rand() 消耗顺序与 HTML 完全一致：实参从左到右、声明行先消耗、短路条件保持短路。
  3. 图层顺序严格照抄 HTML 绘制顺序；每层模糊/透明度完成后按序 alpha_composite。
  4. 评估时甄别"真实问题 vs 复刻局限"：feTurbulence/blur/glow 类质感差异不算数。
"""

import argparse
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# ============================================================
# 作品配置区（翻译前先从这里抄 HTML 的常量）
# ============================================================
W, H = 1313, 1000          # 画布尺寸（与 HTML canvas 一致；HTML 若是 2x 缩放，此处按 CSS 尺寸）
SEED = 20260828            # 主随机种子（与 HTML mulberry32 种子一致）
SEED_GRAIN = 777           # 颗粒层独立种子（与 HTML grain 层种子一致）

M32 = 0xFFFFFFFF


class Rng:
    """mulberry32 精确复刻——每步 & M32，序列与 JS 完全一致。"""

    def __init__(self, seed):
        self.s = seed & M32

    def rand(self):
        self.s = (self.s + 0x6D2B79F5) & M32
        t = self.s ^ (self.s >> 15)
        t = (t * (t | 1)) & M32
        t = ((t + (t ^ (t >> 7))) & M32) ^ t
        return (t ^ (t >> 14)) / 2**32


# ============================================================
# 渲染工具库（一般无需改动）
# ============================================================
def hx(hexstr, a=255):
    """'#RRGGBB' -> (r,g,b,a)。"""
    hexstr = hexstr.lstrip("#")
    return (int(hexstr[0:2], 16), int(hexstr[2:4], 16), int(hexstr[4:6], 16), a)


def vgrad_rgb(y0, y1, stops):
    """垂直线性渐变，返回 (n,3) float 数组。stops=[(pos0,c0),(pos1,c1),...] pos∈[0,1]。"""
    n = y1 - y0
    t = (np.arange(n, dtype=np.float32) / max(n - 1, 1))
    cs = np.array([c for _, c in stops], np.float32)
    ps = np.array([p for p, _ in stops], np.float32)
    out = np.empty((n, 3), np.float32)
    for i in range(len(ps) - 1):
        m = (t >= ps[i]) & (t <= ps[i + 1])
        tt = (t[m] - ps[i]) / max(ps[i + 1] - ps[i], 1e-6)
        for c in range(3):
            out[m, c] = cs[i, c] * (1 - tt) + cs[i + 1, c] * tt
    return out


def radial_mix(w, h, cx, cy, stops):
    """径向渐变 RGBA，返回 (h,w,4) float。stops=[(pos,(r,g,b),alpha),...]。"""
    gy, gx = np.mgrid[0:h, 0:w]                      # gy 在前：mgrid 首返回值对应行(y)
    d = np.sqrt((gx - cx) ** 2 + (gy - cy) ** 2)
    ps = np.array([p for p, _, _ in stops], np.float32)
    cs = np.array([c for _, c, _ in stops], np.float32)
    als = np.array([a for _, _, a in stops], np.float32)
    out = np.zeros((h, w, 4), np.float32)
    t = np.clip(d / max(ps[-1], 1e-6), 0, 1)
    for i in range(len(ps) - 1):
        m = (d <= ps[i + 1])
        tt = np.clip((d[m] - ps[i]) / max(ps[i + 1] - ps[i], 1e-6), 0, 1)
        for c in range(3):
            v = cs[i, c] * (1 - tt) + cs[i + 1, c] * tt
            out[m, c] = np.where(out[m, c] == 0, v, out[m, c])
        out[m, 3] = np.where(out[m, 3] == 0, als[i] * (1 - tt) + als[i + 1] * tt, out[m, 3])
    return out


def stroke_np(base, x1, y1, x2, y2, w, rgba):
    """圆头线段（对应 ctx.lineWidth=w; lineCap='round'），src-over 写入 base(H,W,4) uint8。"""
    R = w / 2.0
    xi0, xi1 = int(min(x1, x2) - R - 1), int(max(x1, x2) + R + 2)
    yi0, yi1 = int(min(y1, y2) - R - 1), int(max(y1, y2) + R + 2)
    xi0, xi1 = max(xi0, 0), min(xi1, base.shape[1])
    yi0, yi1 = max(yi0, 0), min(yi1, base.shape[0])
    if xi1 <= xi0 or yi1 <= yi0:
        return
    gy, gx = np.mgrid[yi0:yi1, xi0:xi1]
    dx, dy = x2 - x1, y2 - y1
    L2 = dx * dx + dy * dy
    if L2 < 1e-9:
        m = (gx - x1) ** 2 + (gy - y1) ** 2 <= R * R
    else:
        t = np.clip(((gx - x1) * dx + (gy - y1) * dy) / L2, 0, 1)
        px, py = x1 + t * dx, y1 + t * dy
        m = (gx - px) ** 2 + (gy - py) ** 2 <= R * R
    a = rgba[3] / 255.0
    region = base[yi0:yi1, xi0:xi1].astype(np.float32)
    src = np.array(rgba[:3], np.float32)
    al = (m * a).astype(np.float32)
    for c in range(3):
        region[:, :, c] = src[c] * al + region[:, :, c] * (1 - al)
    region[:, :, 3] = np.maximum(region[:, :, 3], m * 255)
    base[yi0:yi1, xi0:xi1] = region.astype(np.uint8)


def np_to_img(arr):
    return Image.fromarray(arr)


def blur_composite(base_img, layer_img, radius):
    """对 layer 高斯模糊后合成到 base（对应 shadowBlur / filter:blur 的近似）。"""
    return Image.alpha_composite(base_img, layer_img.filter(ImageFilter.GaussianBlur(radius)))


def zoom_img(full, x0, y0, x1, y1, scale=2):
    """关键区放大诊断图。"""
    crop = full.crop((x0, y0, x1, y1))
    return crop.resize((crop.width * scale, crop.height * scale), Image.LANCZOS)


# ============================================================
# 翻译区：把 HTML 的绘制逻辑按图层顺序翻译到这里
# 下面是一个最小可运行示例（渐变天空 + 碎笔 + 颗粒 + vignette），
# 实际使用时替换为作品各图层的等价 Python 实现。
# ============================================================
def paint():
    rng = Rng(SEED)          # 主随机流——消耗顺序必须与 HTML 完全一致
    base = np.zeros((H, W, 4), np.uint8)
    base[:, :, 3] = 255

    # --- L1 天空渐变（对应 createLinearGradient(0,0,0,H)） ---
    # stops 按 HTML 里 addColorStop 的顺序抄；注意 [:, None, :] 广播！
    sky = vgrad_rgb(0, H, [
        (0.0, np.array([40, 55, 90], np.float32)),
        (0.55, np.array([150, 120, 110], np.float32)),
        (1.0, np.array([30, 40, 70], np.float32)),
    ])
    base[0:H, :, :3] = sky[:, None, :]

    base_img = np_to_img(base)

    # --- L2 光晕层（对应径向渐变 + shadowBlur 的层） ---
    glow = radial_mix(W, H, W * 0.72, H * 0.40, [
        (0, (255, 200, 140), 180),
        (0.5, (200, 120, 90), 60),
        (1, (0, 0, 0), 0),
    ]).astype(np.uint8)
    base_img = blur_composite(base_img, np_to_img(glow), 13)

    # --- L3 碎笔层（对应几千次 ctx.beginPath/moveTo/lineTo/stroke） ---
    strokes = np.zeros((H, W, 4), np.uint8)
    for i in range(600):
        x = rng.rand() * W
        y = rng.rand() * H
        wdt = 1 + rng.rand() * 3
        r = int(120 + rng.rand() * 120)
        g = int(60 + rng.rand() * 80)
        b = int(50 + rng.rand() * 60)
        a = int(60 + rng.rand() * 120)
        tilt = (rng.rand() - 0.5) * 60
        # 注意：以上消耗顺序 = HTML stroke 实参从左到右的求值顺序
        stroke_np(strokes, x, y, x + 14 + tilt, y + (rng.rand() - 0.5) * 8, wdt,
                  (r, g, b, a))
    base_img = Image.alpha_composite(base_img, np_to_img(strokes))

    # --- L4 颗粒 + vignette（对应 grain 层，独立种子） ---
    grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grain)
    r2 = Rng(SEED_GRAIN)
    for _ in range(9000):
        # 单像素颗粒用 point：避免多次独立随机坐标被 PIL 逆序消费
        v = int(r2.rand() * 255)
        gd.point((r2.rand() * W, r2.rand() * H), fill=(v, v, v, 28))
    base_img = Image.alpha_composite(base_img, grain)

    # vignette（对应 CSS 径向暗角）
    gy, gx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((gx - W / 2) / (W / 2)) ** 2 + ((gy - H / 2) / (H / 2)) ** 2)
    vig = (np.clip(d - 0.55, 0, 1) * 0.17 * 255).astype(np.uint8)
    dark = np.zeros((H, W, 4), np.uint8)
    dark[:, :, 3] = vig
    base_img = Image.alpha_composite(base_img, Image.fromarray(dark))

    return base_img


# ============================================================
# 输出诊断图
# ============================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="preview_out")
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    full = paint().convert("RGB")
    paths = []
    p_full = os.path.join(args.outdir, "full.png")
    full.save(p_full)
    paths.append(p_full)

    p_thumb = os.path.join(args.outdir, "thumb.png")
    full.resize((W // 4, H // 4), Image.LANCZOS).save(p_thumb)
    paths.append(p_thumb)

    p_z1 = os.path.join(args.outdir, "zoom_center.png")
    zoom_img(full, int(W * 0.5), int(H * 0.25), int(W * 0.85), int(H * 0.55)).save(p_z1)
    paths.append(p_z1)

    p_z2 = os.path.join(args.outdir, "zoom_fg.png")
    zoom_img(full, 0, int(H * 0.6), int(W * 0.4), H).save(p_z2)
    paths.append(p_z2)

    print("PREVIEW_DONE")
    for p in paths:
        print(" ", p)


if __name__ == "__main__":
    main()
