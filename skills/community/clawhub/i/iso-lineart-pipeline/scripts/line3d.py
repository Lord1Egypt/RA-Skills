#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
line3d.py —— 真三维体块 + 隐藏线消隐的线稿渲染器 v3

为什么重写：
  前两版是在二维上逐块摆多边形，谁也不知道墙顶在哪、檐口在哪，
  所以屋顶会飘、墙和檐会打架。这一版先建三维体块，投影后做 z-buffer
  消隐，再沿每条边采样判断可见性。几何自洽，飘不起来。

投影常量沿用实测：SLOPE=0.7155（JF1 前右下沿拟合 rms 0.27px），
纸底 (235,229,229)。
"""
import numpy as np
from PIL import Image, ImageDraw

# ── 画布与相机 ────────────────────────────────────────────────
W = H = 1920
SS = 2
K = 0.98
SX = 900.0 * K
SLOPE = 0.7155
SZ = 1150.0 * K
V = np.array([1.0, 1.0, -(2 * SX * SLOPE) / SZ])

PAPER = (235, 229, 229)
INK = (40, 34, 31)
W_SIL, W_STR, W_DET = 8.0, 3.8, 2.5
EPS = 0.0022

_rng = np.random.default_rng(20261105)


# ── 几何基元 ──────────────────────────────────────────────────
def _orient(face, interior):
    f = [np.asarray(p, float) for p in face]
    n = np.cross(f[1] - f[0], f[2] - f[0])
    c = sum(f) / float(len(f))
    if np.dot(n, c - np.asarray(interior, float)) < 0:
        return list(reversed(f))
    return f


def box(a0, a1, b0, b1, h0, h1, tag='str'):
    pt = {}
    for i, a in enumerate((a0, a1)):
        for j, b in enumerate((b0, b1)):
            for k, h in enumerate((h0, h1)):
                pt[i, j, k] = np.array([a, b, h], float)
    quads = [
        [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0)],
        [(1, 0, 1), (1, 1, 1), (0, 1, 1), (0, 0, 1)],
        [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)],
        [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)],
        [(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)],
        [(0, 1, 0), (1, 1, 0), (1, 1, 1), (0, 1, 1)],
    ]
    ctr = np.array([(a0 + a1) / 2, (b0 + b1) / 2, (h0 + h1) / 2])
    return [(_orient([pt[q] for q in Q], ctr), tag) for Q in quads]


def slab(top_quad, down=0.012, tag='str'):
    top = [np.asarray(p, float) for p in top_quad]
    bot = [p - np.array([0, 0, down]) for p in top]
    ctr = (sum(top) / 4.0) - np.array([0, 0, down / 2])
    faces = [(_orient(top, ctr), tag), (_orient(list(reversed(bot)), ctr), tag)]
    for i in range(4):
        j = (i + 1) % 4
        faces.append((_orient([top[i], top[j], bot[j], bot[i]], ctr), tag))
    return faces


def extrude(profile, b0, b1, tag='str'):
    """(a,h) 平面上的凸多边形沿 b 挤出——墙顶跟着屋面斜就靠它。"""
    n = len(profile)
    ctr = np.array([sum(p[0] for p in profile) / n, (b0 + b1) / 2,
                    sum(p[1] for p in profile) / n])
    faces = []
    for bb in (b0, b1):
        faces.append((_orient([np.array([a, bb, h]) for a, h in profile], ctr), tag))
    for i in range(n):
        a0, h0 = profile[i]
        a1, h1 = profile[(i + 1) % n]
        faces.append((_orient([np.array([a0, b0, h0]), np.array([a1, b0, h1]),
                               np.array([a1, b1, h1]), np.array([a0, b1, h0])], ctr), tag))
    return faces


def wquad(a0, a1, b0, b1, hbot, htop, tag='str'):
    return extrude([(a0, hbot), (a1, hbot), (a1, htop(a1)), (a0, htop(a0))],
                   b0, b1, tag)


def beam(p0, p1, wdir, w, t, tag='str'):
    """任意方向的长条——斜撑、斜梁。wdir 是宽度方向，厚度自动沿法向。"""
    p0 = np.asarray(p0, float)
    p1 = np.asarray(p1, float)
    d = p1 - p0
    d = d / np.linalg.norm(d)
    wv = np.asarray(wdir, float)
    wv = wv - d * np.dot(wv, d)
    wv = wv / np.linalg.norm(wv)
    tv = np.cross(d, wv)
    ctr = (p0 + p1) / 2

    def ring(p):
        return [p + wv * w / 2 + tv * t / 2, p - wv * w / 2 + tv * t / 2,
                p - wv * w / 2 - tv * t / 2, p + wv * w / 2 - tv * t / 2]

    A, Bq = ring(p0), ring(p1)
    faces = [(_orient(A, ctr), tag), (_orient(list(reversed(Bq)), ctr), tag)]
    for i in range(4):
        j = (i + 1) % 4
        faces.append((_orient([A[i], A[j], Bq[j], Bq[i]], ctr), tag))
    return faces


def prism(cx, cy, h0, r, h, n=12, phase=0.0, tag='str', rim=0.0):
    ang = phase + np.arange(n) * 2 * np.pi / n

    def ring(z, rr):
        return [np.array([cx + rr * np.cos(t), cy + rr * np.sin(t), z]) for t in ang]

    ctr = np.array([cx, cy, h0 + h / 2])
    bot, top = ring(h0, r), ring(h0 + h, r)
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((_orient([bot[i], bot[j], top[j], top[i]], ctr), tag))
    faces.append((_orient(list(top), ctr), tag))
    faces.append((_orient(list(bot), ctr), tag))
    if rim > 0:
        rb, rt = ring(h0 + h - rim, r * 1.07), ring(h0 + h + 0.004, r * 1.07)
        for i in range(n):
            j = (i + 1) % n
            faces.append((_orient([rb[i], rb[j], rt[j], rt[i]], ctr), tag))
    return faces


# ── 投影 ──────────────────────────────────────────────────────
def proj_rel(p):
    a, b, h = p
    return np.array([(a - b) * SX, -(a + b) * SX * SLOPE - h * SZ])


OX = OY = 0.0


def layout(faces):
    global OX, OY
    pts = np.array([proj_rel(p) for f, _ in faces for p in f])
    x0, x1 = pts[:, 0].min(), pts[:, 0].max()
    y0, y1 = pts[:, 1].min(), pts[:, 1].max()
    OX = W / 2.0 - (x0 + x1) / 2.0
    OY = H * 0.50 - (y0 + y1) / 2.0
    return x0, x1, y0, y1


# ── 消隐 ──────────────────────────────────────────────────────
def rasterize(faces):
    N = W * SS
    zbuf = np.full((N, N), np.inf, np.float32)
    drawn = 0
    for pts, _ in faces:
        P3 = np.array(pts, float)
        nrm = np.cross(P3[1] - P3[0], P3[2] - P3[0])
        if np.linalg.norm(nrm) < 1e-12 or np.dot(nrm, V) >= 0:
            continue
        P2 = np.array([proj_rel(p) for p in P3])
        P2[:, 0] = (P2[:, 0] + OX) * SS
        P2[:, 1] = (P2[:, 1] + OY) * SS
        d = P3 @ V
        A = np.hstack([P2[:3], np.ones((3, 1))])
        try:
            coef = np.linalg.solve(A, d[:3])
        except np.linalg.LinAlgError:
            continue
        x0 = max(0, int(np.floor(P2[:, 0].min())))
        x1 = min(N - 1, int(np.ceil(P2[:, 0].max())))
        y0 = max(0, int(np.floor(P2[:, 1].min())))
        y1 = min(N - 1, int(np.ceil(P2[:, 1].max())))
        if x1 <= x0 or y1 <= y0:
            continue
        xs = np.arange(x0, x1 + 1) + 0.5
        ys = np.arange(y0, y1 + 1) + 0.5
        gx, gy = np.meshgrid(xs, ys)
        area2 = sum(P2[i][0] * P2[(i + 1) % 4][1] - P2[(i + 1) % 4][0] * P2[i][1]
                    for i in range(4))
        sgn = 1.0 if area2 > 0 else -1.0
        inside = np.ones(gx.shape, bool)
        for i in range(4):
            p, q = P2[i], P2[(i + 1) % 4]
            cr = (q[0] - p[0]) * (gy - p[1]) - (q[1] - p[1]) * (gx - p[0])
            inside &= (sgn * cr) >= -0.5
            if not inside.any():
                break
        if not inside.any():
            continue
        dd = coef[0] * gx + coef[1] * gy + coef[2]
        sub = zbuf[y0:y1 + 1, x0:x1 + 1]
        m = inside & (dd < sub)
        sub[m] = dd[m]
        zbuf[y0:y1 + 1, x0:x1 + 1] = sub
        drawn += 1
    return zbuf, drawn


def wobble(P, amp=1.2):
    if len(P) < 3:
        return P
    seg = np.linalg.norm(np.diff(P, axis=0), axis=1)
    tot = seg.sum()
    if tot < 26:
        return P
    n = max(3, int(tot / 20))
    cum = np.concatenate([[0], np.cumsum(seg)])
    s = np.linspace(0, tot, n)
    x = np.interp(s, cum, P[:, 0])
    y = np.interp(s, cum, P[:, 1])
    dx, dy = np.gradient(x), np.gradient(y)
    L = np.hypot(dx, dy) + 1e-9
    nx, ny = -dy / L, dx / L
    k = max(3, n // 7)
    ctrl = _rng.uniform(-1, 1, k)
    off = np.interp(np.linspace(0, 1, n), np.linspace(0, 1, k), ctrl) * amp
    off = off - off.mean()
    return np.stack([x + nx * off, y + ny * off], 1)


def edge_polys(faces, zbuf):
    N = W * SS
    out = {'sil': [], 'str': [], 'det': []}
    wt = {'sil': W_SIL, 'str': W_STR, 'det': W_DET}
    # 剪影带：离空白纸 3px 以内的区域，落在里面的线自动加粗
    near = (zbuf >= np.inf)
    for _ in range(3):
        near = (near | np.roll(near, 1, 0) | np.roll(near, -1, 0)
                | np.roll(near, 1, 1) | np.roll(near, -1, 1))
    for pts, tag in faces:
        P3 = np.array(pts, float)
        if np.dot(np.cross(P3[1] - P3[0], P3[2] - P3[0]), V) >= 0:
            continue
        amp = 0.75 * SS * (wt[tag] / W_SIL) ** 0.6
        for k in range(len(P3)):
            p0, p1 = P3[k], P3[(k + 1) % len(P3)]
            L = np.linalg.norm(proj_rel(p1) - proj_rel(p0)) * SS
            if L < 1.0:
                continue
            n = int(L / 2.0) + 2
            t = np.linspace(0, 1, n)
            Q = p0[None, :] + t[:, None] * (p1 - p0)[None, :]
            d = Q @ V
            R = np.array([proj_rel(q) for q in Q])
            R[:, 0] = (R[:, 0] + OX) * SS
            R[:, 1] = (R[:, 1] + OY) * SS
            xi = np.clip(R[:, 0].astype(int), 0, N - 1)
            yi = np.clip(R[:, 1].astype(int), 0, N - 1)
            oob = (R[:, 0] < 0) | (R[:, 0] >= N) | (R[:, 1] < 0) | (R[:, 1] >= N)
            vis = (d <= zbuf[yi, xi] + EPS) & (~oob)
            if not vis.any():
                continue
            heavy = near[yi, xi]
            for ok, tg in ((vis & heavy, 'sil'), (vis & (~heavy), tag)):
                if not ok.any():
                    continue
                idx = np.where(ok)[0]
                breaks = np.where(np.diff(idx) > 1)[0]
                for run in np.split(idx, breaks + 1):
                    if len(run) < 2:
                        continue
                    out[tg].append(wobble(R[run], amp=amp))
    return out


def render(faces, path):
    bbox = layout(faces)
    zbuf, nd = rasterize(faces)
    polys = edge_polys(faces, zbuf)
    img = Image.new('RGB', (W * SS, H * SS), PAPER)
    d = ImageDraw.Draw(img)
    wt = {'sil': W_SIL, 'str': W_STR, 'det': W_DET}
    for tag, lst in polys.items():
        w = wt[tag] * SS
        for P in lst:
            d.line([tuple(p) for p in P], fill=INK,
                   width=max(1, int(round(w))), joint='curve')
    img = img.resize((W, H), Image.LANCZOS)
    img.save(path)
    cnt = sum(len(v) for v in polys.values())
    print(f'  faces={len(faces)} raster={nd} strokes={cnt} bbox={np.round(bbox, 1)}')
    return img


if __name__ == '__main__':
    import sys
    print(__doc__)
    print("渲染器本身不含造型。跑造型：python design_shop.py out.png")
    print(f"当前输出尺寸 {W}x{H}，超采样 {SS}x")
