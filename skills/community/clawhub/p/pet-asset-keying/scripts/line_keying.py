#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
顺着勾线切 · Key by the Line Art
================================================================================
另一条路：不猜阈值，直接切在角色自己的**勾线**上。

⭐ 为什么这条路成立
    ------------------------------------------------------------------
    颜色阈值法    边界落在【抗锯齿模糊带】里 —— 那个范围内切哪一刀都不对：
                  切多了吃角色，切少了留一圈背景混色（就是那圈"暗边"）
    顺着勾线切    边界落在【勾线】上 —— 勾线是深色高对比，位置明确且唯一
    ------------------------------------------------------------------
    动漫 / Q 版 / 插画素材**几乎一定有勾线**，那就是一条现成的、免费的切割线。
    它天然把画面分成「线外」和「线内」，不需要任何模型。

⭐ 算法（确定性 · 无模型 · 无积分）
    pass1  外部：可通行 = 距背景 < TOL_OUT；从画面**四边**多点泛洪取连通域 → outside
                 角色 = ~outside（勾线是深色 → 泛洪穿不过去，天然阻断）
    pass2  角色内部的封闭空间（手叉腰的三角、辫子与肩之间…）：
                 候选 = 「和背景色几乎一样」的像素且落在角色内（SEED_MAX，严格档）
                 ⭐ 种子 = 块内**距背景最近**的那个像素 —— ⛔ 不是几何质心
                 ⭐ 从种子真泛洪（只吃 inside 内、容差 TOL_HOLE 的区域）→ 扣掉
                 ⭐⭐ 线条保护：勾线从 allow 里整个剔除，当**硬墙**（泛洪不许穿过）
                 三道闸：面积下限 / 单块上限 / 单帧总量上限
    pass3  补漏：pass2 漏掉的细小灰缝，用「包住率 + 中性灰 + 面积」三项同时判
    收尾   去小块噪点；α = soft_alpha(先内缩 1px 再高斯) → alpha_dew(按 d 打折去灰边)

⭐ 用法
    python line_keying.py 输入.png 输出.png
    python line_keying.py ./frames/ ./keyed/ --tol-out 30
    python line_keying.py in.png out.png --no-hole-fill      # 关掉 pass2，只看外部
    python line_keying.py in.png out.png --no-dew            # 关掉去灰边
    python line_keying.py in.png out.png --no-line-protect   # 关掉线条保护（对照用）

⭐ 内置自检：打印 背景色 / 实心面积 / 封闭空间移除量 / 内部洞数 / 耗时
   ⛔ 与 pure_bg_keying.py 一样，**洞数是安全指标**，变多就是挖坏了。

⛔ 实测【反效果 · 别再试】（详见 docs/LINE_KEYING.md 与 docs/PITFALLS.md）
   ① 封闭空间的种子用**几何质心**            → 月牙 / 异形块会撒到角色身上
   ② 用 distance_transform 直接做软边        → 整数距离退化成硬边（半透明=0%）
   ③ 泛洪不锁在 inside 内                    → 从抗锯齿带漏到画面外，实测跑飞 73 万 px
   ④ 拿「洞数」单独下结论                    → 会被**截断 / 面积偏小**骗过
   ⑤ ⛔⛔ 种子落在「已被剔除的 allow==0」上   → cv2.floodFill 不检查起点值，
                                              会把**整片 0 区**当填充区（实测淹 95 万 px）
   ⑥ 靠放宽颜色阈值去补细小漏缝              → 只救几百 px 且开始咬角色色
   ⑦ 泛洪掩码里重复执行一次赋值              → 记账翻倍 → 误触总量闸 → 整帧静默回滚

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

# ---------------- 参数（取自一段 107 帧动画素材的实测标定，768x1152，纯色中灰底） ----------------
TOL_OUT = 30          # pass1：距背景多近算"可通行"（背景连通域）
SEED_MAX = 12         # ⭐⭐ 封闭空间候选/种子必须「和背景色几乎一样」（严格档）
TOL_HOLE = 40         # pass2 泛洪容差（稍松，允许吞掉封闭空间里的软阴影梯度）
MIN_HOLE = 40         # ⭐ 封闭块面积下限（新块实际门槛 = MIN_HOLE × NEW_FRAC；太小的不动）
MAX_HOLE = 30000      # 单块封闭空间面积上限（防跑飞）
MAX_REMOVE_FRAC = 0.20  # ⭐ 单帧移除总量上限（占角色面积比）→ 超了就整帧不做 pass2
MIN_BLOB = 200        # 角色连通块面积下限（更小的当噪点删掉）
ALPHA_SIGMA = 0.8     # 软边高斯 sigma（源像素）
ALPHA_ERODE = 1       # ⭐ 边界内缩 px（把边界从"抗锯齿带"压回"50% 覆盖线"）
SEED_EDGE = 2         # ⭐⭐ 种子取「块的内部像素」（距块边界 ≥ 此值；块太薄自动退到 1）
CROP_MARGIN = 60      # 输出裁到角色 bbox 后留的边距

# ⭐⭐⭐ 线条保护（勾线当硬墙）
#   问题：pass2 泛洪会把「线条」连同旁边的脏块一起挖掉（实测 walk#36 削 230px 线条）。
#   方案：先把「线条」从 allow 里整个剔除 —— 泛洪不许穿过，等于把线当实体墙。
#   定义：LINE = inside &（亮度 < LINE_LUM）&「局部细」（开运算 LINE_R 半径能吃掉）
#      → ⛔ 纯几何（开运算）单独用不够：只抓 604px，漏太多
#         ⛔ 纯暗色（不看几何）也不行：抓 66362px，把外套暗部全算成线
#         ✅ 两个条件同时加：9156px，刚好
#   剩余残差：线条交汇 / 端点处局部变宽（宽度 > 2×LINE_R），几何上不属"细"。
#      ⭐ 换 LINE_R = 1/2/3 残差纹丝不动（49/41px）→ 这是**检测极限，不是参数问题**。
LINE_PROTECT = True   # 总开关
LINE_LUM = 100        # 线条的亮度上限（原始亮度，0~255）
LINE_R = 2            # 开运算半径（吃掉宽度 ≤ 2×LINE_R 的细部）

# ⭐⭐⭐ pass3 补漏（三项判据）
#   Ronny 原话：「扣完之后还有几个小像素点没扣掉」。
#   ⛔ 走错过的路：一直在调**颜色阈值**（SEED_MAX 12→16→20→32）——
#      实测只救 400px，且开始咬角色色。这些残留块的 d 落在 12~30 的过渡带，
#      放宽阈值就会把"发丝阴影"一起放进来。
#   ✅ 真正管用的是**几何 + 颜色 双判据**，三条同时满足才动：
#     ① 包住率 ≥ TOPO_ENC：块外一圈基本是 char（不是贴外轮廓、也不是大开口）
#     ② 像背景：d < TOPO_D_MAX **且 RGB 三通道极差 ≤ TOPO_SAT**（中性灰）
#        ⭐ 关键：纯灰背景三通道极差 ≈ 0；角色阴影带绿调/暖调 → 靠 d 分不开，
#          靠「中性」一票否决，实测把 5 个阴影块全挡住
#     ③ 面积 ≥ TOPO_MIN
#   ⛔ 放在 MAX_REMOVE_FRAC 总闸**之外**：补漏不该被 pass2 的保守闸连坐。
TOPO_FILL = True
TOPO_D_MAX = 25       # 补漏块的 d 上限（必须接近背景）
TOPO_SAT = 6          # RGB 三通道极差上限（中性灰）
TOPO_ENC = 0.90       # 包住率下限（块外一圈里 char 的占比）
TOPO_MIN = 40         # 补漏块面积下限
TOPO_BG_MAX = 0.85    # ⚠️ 块紧外一圈里「真背景」占比上限（只挡"几乎贴着真实边界"的极端块）

# ⭐⭐ 去灰边（alpha_dew）
#   成因：出图/出视频时抗锯齿留下「发丝 → 背景」的连续过渡带，d 落在 40~110。
#     它既够不到 pass1 的 TOL_OUT（泛洪过不去 → 被判成角色内部），
#     也够不到 pass2 的 SEED_MAX（不构成候选 → 永远不会被挖）。
#   ⛔ 试过放宽 pass2（SEED 60 / HOLE 80 起，洞数 16→88）→ 会咬穿发丝，不可行。
#   ✅ 正解：**不动几何、只降 alpha** —— 按 d 值给灰带一个 0~1 的 alpha。
#   ⛔⛔ 两个必须加的豁免（否则把眼睛/衣服挖空）：
#      · 亮度闸：深色实色（眼睛、深色衣服）亮度低 → 豁免
#      · 勾线豁免：LINE 掩码内的像素 → 不动
#      ⭐ 因为 d（距背景色距离）**无法区分「灰边」和「深色角色色」** ——
#        眼睛是深灰绿、衣服是深藏青，本来离背景灰就不远。
DEW_ON = True        # 总开关
DEW_D0 = 30.0        # d 下限：≤此值的像素 alpha 直接压向 floor
DEW_D1 = 80.0        # d 上限：≥此值的像素 alpha 保持 1
DEW_FLOOR = 0.0      # 灰带最低 alpha（0 = 允许完全透明）
DEW_LUM_MIN = 118    # ⭐ 亮度闸：亮度 < 此值的像素【豁免】（保护眼睛/衣服等深色实色）
DEW_LINE_FREE = True # ⭐ 勾线豁免：LINE 掩码内的像素不动



def bg_of(rgb: np.ndarray) -> np.ndarray:
    """背景色 = 四角 40x40 的中值（与 pure_bg_keying.py 同一口径）"""
    a = rgb.astype(np.int16)
    c = np.concatenate([a[:40, :40].reshape(-1, 3), a[:40, -40:].reshape(-1, 3),
                        a[-40:, :40].reshape(-1, 3), a[-40:, -40:].reshape(-1, 3)])
    return np.median(c, axis=0)


def dist_bg(rgb: np.ndarray, bg: np.ndarray) -> np.ndarray:
    """⭐ 判据一律用**逐像素**的 L1 距离，⛔ 不用"色板代表值"的距离
    （色板距离不能担保像素安全 —— 见 docs/PITFALLS.md ①）"""
    return np.abs(rgb.astype(np.int16) - bg.astype(np.int16)).sum(axis=2)


def line_mask(rgb: np.ndarray, inside: np.ndarray) -> np.ndarray | None:
    """⭐ 勾线掩码：**暗色** + **局部细** 两个条件同时满足才算线条

    ⛔ 为什么两个条件都不能省（实测）：
       纯几何（开运算）   → 只抓 604px，漏掉太多
       纯暗色（不看几何） → 抓 66362px，把衣服暗部全算进去了
       ✅ 两个都加        → 9156px，刚好

    ⛔ 残差说明：线条交汇 / 端点处局部变宽（宽 > 2×LINE_R），几何上不属"细"。
       ⭐ 换 LINE_R = 1/2/3 残差纹丝不动 → **检测极限，不是参数问题**。
    """
    if not LINE_PROTECT:
        return None
    lum = rgb.astype(np.float32).mean(axis=2)
    m = (lum < LINE_LUM) & inside
    if not m.any():
        return None
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                  (2 * LINE_R + 1, 2 * LINE_R + 1))
    opened = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, k)
    return m & (opened == 0)



def key_by_line(rgb: np.ndarray, bg: np.ndarray | None = None,
                tol_out: int = TOL_OUT, seed_max: int = SEED_MAX,
                tol_hole: int = TOL_HOLE, fill_holes: bool = True,
                fill_small: bool = True, protect_line: bool = True,
                seed_edge: int = SEED_EDGE, verbose: bool = False):
    """顺着勾线切。返回 (角色 bool 掩膜, 报告 dict)

    报告里 `holes` 是 pass2/pass3 的明细，每一项含面积 / 泛洪量 / 种子坐标 / 种子距离，
    便于出对比图时**精确定位到"这块被切干净了"的位置**。
    """
    bg = bg_of(rgb) if bg is None else np.asarray(bg)
    d = dist_bg(rgb, bg)
    h, w = d.shape

    # ---------- pass1：外部（勾线阻断泛洪） ----------
    passable = (d < tol_out).astype(np.uint8)
    n, lb = cv2.connectedComponents(passable, 8)
    if n <= 1:
        # 退化情况：整幅图都是背景色 → 没有可切的东西，原样返回
        return np.ones_like(d, bool), dict(bg=bg, degenerate=True, holes=[], fg=int(h * w),
                                           pass1_area=int(h * w), holes_removed=0,
                                           removed_mask=np.zeros_like(d, bool))
    border = set(np.unique(np.concatenate([lb[0], lb[-1], lb[:, 0], lb[:, -1]])).tolist())
    border.discard(0)
    outside = np.isin(lb, sorted(border))
    inside = ~outside
    char = inside.copy()
    inside_area = int(inside.sum())

    # ---------- pass2：角色内部的封闭空间 ----------
    holes: list[dict] = []
    removed = 0
    removed_mask = np.zeros_like(char)      # ⭐ 故意切掉的区域（自检时要用它把洞补回去再数）
    if fill_holes and inside_area:
        # ⓵ 候选 = 与背景色几乎相同、且落在角色内部（严格档，避免选到角色身上的过渡色）
        cand = ((d < seed_max) & inside).astype(np.uint8)
        n2, lb2 = cv2.connectedComponents(cand, 8)
        # ⓶ 泛洪允许区：松一档，但 ⛔ 必须锁在 inside 内
        #    （不锁的话会顺着抗锯齿带漏到画面外 —— 实测跑飞 73 万 px）
        allow = ((d < tol_hole) & inside).astype(np.uint8)
        # ⭐⭐⭐ 线条保护：勾线当硬墙，泛洪不许穿过
        ln = line_mask(rgb, inside) if protect_line else None
        if ln is not None:
            allow = ((allow > 0) & (~ln)).astype(np.uint8)
        for i in range(1, n2 + 1):
            blk = (lb2 == i)
            area0 = int(blk.sum())
            if area0 < MIN_HOLE:
                continue
            # ⭐ 种子 = 「块的内部像素」里距背景最近的那个 —— ⛔ 不是几何质心
            #    （月牙 / 异形块的质心可能落在角色身上；实测约 10% 的块中招）
            dblk = ndimage.distance_transform_edt(blk)
            inner = dblk >= seed_edge
            if not inner.any():
                inner = dblk >= 1.0        # 块太薄（细缝）→ 退到"只要不是最外层"
            if not inner.any():
                inner = blk
            inner = inner & blk
            dm = np.where(inner, d, np.int32(10 ** 9))
            sy, sx = np.unravel_index(int(np.argmin(dm)), d.shape)
            seed_edge_dist = float(dblk[sy, sx])
            # ⛔⛔⛔ 种子可能落在 allow==0 的像素上（被线条掩码吃掉）。
            #   cv2.floodFill 从「已为 0」的像素起跑，会把**整片 0 区**当成填充区
            #   → 实测淹 954,580px（≈整图 960,000）→ 超 MAX_HOLE → 整块被 skip。
            #   ⭐ 后果不是"多挖"，而是**该挖的静默不挖**（实测 19/38 个候选块中招，50%）。
            #   ✅ 修法：若种子不在 allow 上，就在「块内 ∩ allow」里重挑 d 最小者；
            #      实在没有（整块被线条覆盖）才放弃。
            if allow[sy, sx] == 0:
                cand_ok = blk & (allow > 0)
                if not cand_ok.any():
                    holes.append(dict(area=area0, flooded=0, seed_d=int(d[sy, sx]),
                                      seed_xy=[int(sx), int(sy)],
                                      note="skip: 块内无可用种子(被线条全覆)"))
                    continue
                dm2 = np.where(cand_ok, d, np.int32(10 ** 9))
                sy, sx = np.unravel_index(int(np.argmin(dm2)), d.shape)
                seed_edge_dist = float(dblk[sy, sx])
            tmp = allow.copy()
            mk = np.zeros((h + 2, w + 2), np.uint8)
            cv2.floodFill(tmp, mk, (int(sx), int(sy)), 2, 0, 0,
                          flags=8 | cv2.FLOODFILL_MASK_ONLY | (255 << 8))
            newly = (mk[1:-1, 1:-1] > 0) & char
            fa = int(newly.sum())
            if fa == 0:
                continue
            if fa > MAX_HOLE:
                holes.append(dict(area=area0, flooded=0, seed_d=int(d[sy, sx]),
                                  seed_xy=[int(sx), int(sy)], note="skip: 泛洪超单块上限"))
                continue
            mean_rgb = tuple(int(v) for v in np.round(rgb[newly].reshape(-1, 3).mean(axis=0)))
            char[newly] = False
            removed_mask |= newly
            removed += fa
            holes.append(dict(area=area0, flooded=fa, seed_d=int(d[sy, sx]),
                              seed_edge=seed_edge_dist, mean_rgb=mean_rgb,
                              seed_xy=[int(sx), int(sy)]))
            # ⛔⛔⛔ 这一段曾经**整段重复**了一遍（newly / fa / MAX_HOLE / char[newly]=False
            #   连贴两次，且第二遍漏了 seed_edge）。后果不是"多挖"，而是：
            #     ① removed 被重复累加 → 误触 MAX_REMOVE_FRAC → 整帧回滚到 pass1
            #        → **该挖的全没挖**（静默不挖）
            #     ② holes.append 重复 → 日志块数虚高
            #   ⭐ 与"种子被线条吃掉"是同一类后果：表面看是"漏扣"，根因在内部记账。
        # ⭐ 单帧总闸：怕"整张脸被当成封闭空间"，超比例就整帧不做 pass2（保守）
        if removed > MAX_REMOVE_FRAC * max(inside_area, 1):
            char = inside.copy()
            removed_mask[:] = False
            holes.append(dict(area=removed, flooded=0,
                              note=f"⛔ 整帧放弃 pass2（移除 {removed} > "
                                   f"{MAX_REMOVE_FRAC:.0%}×{inside_area}）"))
            removed = 0

    # ---------- pass3：⭐ 补漏（包住率 + 中性灰 + 面积，三项同时满足） ----------
    if fill_small and TOPO_FILL:
        rr3 = rgb.astype(np.int16)
        sat3 = rr3.max(axis=2) - rr3.min(axis=2)
        pick3 = char & (d < TOPO_D_MAX) & (sat3 <= TOPO_SAT)
        if pick3.any():
            n7, lb7 = cv2.connectedComponents(pick3.astype(np.uint8), 8)
            filled3 = 0
            for k in range(1, n7 + 1):
                blk = (lb7 == k)
                if int(blk.sum()) < TOPO_MIN:
                    continue
                ring = ndimage.binary_dilation(blk, iterations=2) & (~blk)
                if not ring.any():
                    continue
                if float(char[ring].mean()) < TOPO_ENC:      # ① 包住率
                    continue
                ring1 = ndimage.binary_dilation(blk, iterations=1) & (~blk)
                if ring1.any():                               # ② 外侧背景占比闸
                    if float((d[ring1] < tol_out).mean()) > TOPO_BG_MAX:
                        continue
                char[blk] = False
                removed_mask |= blk
                filled3 += int(blk.sum())
            if filled3:
                holes.append(dict(area=filled3, flooded=filled3,
                                  note="pass3: 补漏(包住率+中性灰+面积)"))
                removed += filled3

    # ---------- 去小块噪点：只保留最大的连通块（其余 < MIN_BLOB 的删掉） ----------
    if char.any():
        n3, lb3 = cv2.connectedComponents(char.astype(np.uint8), 8)
        if n3 > 1:
            szs = ndimage.sum(char, lb3, range(1, n3 + 1))
            main = int(np.argmax(szs)) + 1
            for i in range(1, n3 + 1):
                if i != main and szs[i - 1] < MIN_BLOB:
                    char[lb3 == i] = False

    solid = int(char.sum())
    rep = dict(bg=bg, degenerate=False, fg=solid, pass1_area=inside_area,
               holes_removed=removed, holes=holes, removed_mask=removed_mask,
               tol_out=tol_out, seed_max=seed_max, tol_hole=tol_hole)
    if verbose:
        n_real = sum(1 for x in holes if x.get("flooded"))
        print(f"    背景 {bg.astype(int)}   pass1 外部切出 {solid}px"
              f"   pass2/3 移除 {n_real} 组 / 共 {removed}px")
    return char, rep


def soft_alpha(char: np.ndarray, sigma: float = ALPHA_SIGMA, erode_in: int = ALPHA_ERODE):
    """⭐ 软边：先把二值边界**内缩** erode_in px，再高斯软化

    为什么必须内缩：泛洪停在「第一个距背景 ≥ TOL_OUT 的像素」，那是抗锯齿带上
    背景混色还占约 90% 的位置 → 比理想的「50% 覆盖线」多留约 1px 背景混色。
    内缩 1px 把边界压回 50% 覆盖线 → 那圈混色被切掉，边缘落在勾线上。

    ⛔ 别用 distance_transform 直接做软边：它给的是整数距离，
       sd/band + 0.5 会退化成二值（实测半透明像素 = 0%）。
    """
    m = char
    if erode_in > 0:
        m = ndimage.binary_erosion(m, iterations=erode_in)
    if sigma <= 0:
        return m.astype(np.float32)
    return np.clip(ndimage.gaussian_filter(m.astype(np.float32), sigma), 0.0, 1.0)


def alpha_dew(a: np.ndarray, rgb: np.ndarray, bg: np.ndarray,
              d0: float = DEW_D0, d1: float = DEW_D1, floor: float = DEW_FLOOR,
              lum_min: float = DEW_LUM_MIN, line_free: bool = DEW_LINE_FREE):
    """⭐ 去灰边：对 alpha 里"颜色接近背景、且是中灰过渡色"的部分按 d 值打折

    病灶：抗锯齿把「发丝 → 背景」拉出一条连续过渡带（d ≈ 40~110）。
      它既够不到 pass1 的阈值（泛洪过不去 → 被当角色内部留下），
      也够不到 pass2 的种子严格度（不构成候选 → 永远不会被挖）。
      ⛔ 想靠放宽 pass2 解决 → 会咬穿发丝（洞数 16→88）。
      ✅ 所以**不动几何、只降 alpha**：d 越小（越像背景）→ alpha 越接近 floor。

    ⛔ 三条设计约束，缺一不可：
       ① 只降不升（minimum）：避免把角色实色提亮成不透明而**扩散轮廓**
       ② **亮度闸**：深色实色（眼睛、深色衣服）亮度低 → 豁免
       ③ **勾线豁免**：LINE 掩码内的像素 → 不动
       ⭐ ②③ 是因为 d **无法区分「灰边」和「深色角色色」**——
         深灰绿的眼睛、深藏青的衣服，离背景灰本来就不远（d 60~90），
         不加闸会连同它们一起削成半透明。
    """
    if not DEW_ON:
        return a
    d = dist_bg(rgb, bg).astype(np.float32)
    t = np.clip((d - d0) / max(d1 - d0, 1e-6), 0.0, 1.0)
    t = floor + (1.0 - floor) * t
    # ① 亮度闸：只对"中灰过渡色"生效
    lum = rgb.astype(np.int16).mean(axis=2)
    t = np.where(lum < lum_min, 1.0, t)
    # ② 勾线豁免
    if line_free:
        try:
            ln = line_mask(rgb, np.ones_like(a, dtype=bool))
            if ln is not None:
                t = np.where(ln, 1.0, t)
        except Exception:
            pass
    return np.clip(np.minimum(a, t), 0.0, 1.0)



def defringe(rgb: np.ndarray, a: np.ndarray) -> np.ndarray:
    """⭐ 半透明带里的颜色 = 最近**实心**像素的颜色 → 去掉混进去的背景灰

    只改颜色不改 α，所以不会削角色；效果是边缘那圈"灰"读起来像阴影而不是脏边。
    """
    solid = a >= 0.995
    if not solid.any():
        return rgb
    _, inds = ndimage.distance_transform_edt(~solid, return_indices=True)
    near = rgb[inds[0], inds[1]]
    edge = (a > 0.01) & (a < 0.995)
    out = rgb.copy()
    out[edge] = near[edge]
    return out


def hole_stats(mask: np.ndarray) -> tuple[int, int, int]:
    """一秒安全检验：内部洞的 个数 / ≥8px 个数 / 总面积（与 pure_bg_keying.py 同一口径）

    ⭐ 在勾线切里要先把 pass2/pass3 故意切掉的区域**补回去**再数（见 key_image），
       否则"手叉腰的三角"这类有意切的封闭空间会被当成事故报出来。
       ⛔ 洞数只能用来【发现问题】，不能单独用来评判好坏：
          它会被「角色被截断」骗过 —— 被切掉的地方当然不会有洞。
          ✅ 必须同时看**实心面积**：面积明显偏小 + 洞少 = 截断，不是干净。
    """
    filled = ndimage.binary_fill_holes(mask)
    holes = filled & (~mask)
    lb, n = ndimage.label(holes)
    if n == 0:
        return 0, 0, 0
    szs = ndimage.sum(holes, lb, range(1, n + 1))
    big = szs[szs >= 8]
    return n, int(len(big)), int(big.sum()) if len(big) else 0


def key_image(rgb: np.ndarray, bg: np.ndarray | None = None, fill_holes: bool = True,
              fill_small: bool = True, protect_line: bool = True,
              use_dew: bool = True, use_defringe: bool = True,
              sigma: float = ALPHA_SIGMA, erode_in: int = ALPHA_ERODE,
              verbose: bool = True):
    """整条链路：勾线切 → 软边 → 去灰边 → 去污。返回 (RGBA uint8, 报告 dict)"""
    t0 = time.time()
    bg = bg_of(rgb) if bg is None else np.asarray(bg)
    char, rep = key_by_line(rgb, bg, fill_holes=fill_holes, fill_small=fill_small,
                            protect_line=protect_line, verbose=verbose)
    a = soft_alpha(char, sigma=sigma, erode_in=erode_in)
    if use_dew:
        a = alpha_dew(a, rgb, bg)             # ⭐ 去发丝外围灰边（不动几何）
    out_rgb = defringe(rgb, a) if use_defringe else rgb
    # ⭐ 安全自检：先把 pass2/pass3 **故意**切掉的区域补回去再数洞 →
    #    这样「洞数」只反映"误挖的洞"，不会把有意切的封闭空间算成事故
    n_h, n_big, area_h = hole_stats((a > 0.5) | rep["removed_mask"])
    rep.update(solid=int((a > 0.5).sum()),
               empty_ratio=round(float(((a > 0.05) & (a < 0.95)).sum()
                                       / max(int((a > 0.5).sum()), 1)) * 100, 2),
               n_holes=n_h, n_big_holes=n_big, hole_area=area_h, sec=time.time() - t0)
    if verbose:
        print(f"    实心 {rep['solid']}px   半透明占比 {rep['empty_ratio']}%"
              f"   误挖的洞 {n_h} 个（≥8px {n_big} 个，合计 {area_h}px）   {rep['sec']:.1f}s")
    rgba = np.dstack([out_rgb.astype(np.uint8), np.round(a * 255).astype(np.uint8)])
    return rgba, rep


def _crop(rgba: np.ndarray, margin: int = CROP_MARGIN) -> np.ndarray:
    ys, xs = np.where(rgba[:, :, 3] > 128)
    if len(ys) == 0:
        return rgba
    h, w = rgba.shape[:2]
    return rgba[max(0, int(ys.min()) - margin):min(h, int(ys.max()) + margin + 1),
                max(0, int(xs.min()) - margin):min(w, int(xs.max()) + margin + 1)]


def main():
    ap = argparse.ArgumentParser(description="顺着勾线切 —— 切在角色自己的勾线上（无需模型）")
    ap.add_argument("input", help="输入图片，或帧序列目录")
    ap.add_argument("output", nargs="?", help="输出图片，或输出目录")
    ap.add_argument("--pattern", default="*.png", help="目录模式下的文件名匹配（默认 *.png）")
    ap.add_argument("--tol-out", type=int, default=TOL_OUT, help=f"pass1 背景阈值（默认 {TOL_OUT}）")
    ap.add_argument("--seed-max", type=int, default=SEED_MAX, help=f"封闭空间种子严格度（默认 {SEED_MAX}）")
    ap.add_argument("--tol-hole", type=int, default=TOL_HOLE, help=f"pass2 泛洪容差（默认 {TOL_HOLE}）")
    ap.add_argument("--no-hole-fill", action="store_true", help="关掉 pass2（封闭空间不处理）")
    ap.add_argument("--no-small-fill", action="store_true", help="关掉 pass3（细小灰缝不补）")
    ap.add_argument("--no-line-protect", action="store_true", help="关掉线条保护（对照用）")
    ap.add_argument("--no-dew", action="store_true", help="不做去灰边（保留发丝外围过渡带）")
    ap.add_argument("--no-defringe", action="store_true", help="不做去污（保留混色）")
    ap.add_argument("--sigma", type=float, default=ALPHA_SIGMA, help=f"软边 sigma（默认 {ALPHA_SIGMA}）")
    ap.add_argument("--erode", type=int, default=ALPHA_ERODE, help=f"边界内缩 px（默认 {ALPHA_ERODE}）")
    ap.add_argument("--no-crop", action="store_true", help="不裁到角色 bbox")
    ap.add_argument("--margin", type=int, default=CROP_MARGIN, help=f"裁切边距（默认 {CROP_MARGIN}）")
    args = ap.parse_args()

    def one(rgb, bg=None):
        return key_image(rgb, bg, fill_holes=not args.no_hole_fill,
                         fill_small=not args.no_small_fill,
                         protect_line=not args.no_line_protect,
                         use_dew=not args.no_dew,
                         use_defringe=not args.no_defringe,
                         sigma=args.sigma, erode_in=args.erode)

    if not os.path.isdir(args.input):
        rgb = np.array(Image.open(args.input).convert("RGB"))
        print(f"[单图] {args.input}  {rgb.shape[1]}x{rgb.shape[0]}")
        rgba, rep = one(rgb)
        out = rgba if args.no_crop else _crop(rgba, args.margin)
        dst = args.output or os.path.splitext(args.input)[0] + "_勾线切.png"
        Image.fromarray(out).save(dst)
        print(f"[输出] {dst}  {out.shape[1]}x{out.shape[0]}")
        for x in rep["holes"]:
            if x.get("flooded"):
                print(f"    封闭空间 {x['flooded']:>6}px  种子d={x['seed_d']:<3}"
                      f" 均色{x.get('mean_rgb')} 种子{x['seed_xy']}")
            elif x.get("note"):
                print(f"    ⛔ {x.get('area')}px  {x['note']}")
        return

    files = sorted(glob.glob(os.path.join(args.input, args.pattern)))
    if not files:
        print(f"⛔ 目录里没匹配到文件：{args.input}/{args.pattern}")
        sys.exit(1)
    dst_dir = args.output or os.path.join(args.input, "_line_keyed")
    os.makedirs(dst_dir, exist_ok=True)
    # ⭐ 视频序列共用同一个背景色（逐帧各自估会漂，纯色底素材没这个必要）
    acc = [bg_of(np.array(Image.open(f).convert("RGB"))) for f in files[: min(5, len(files))]]
    bg = np.median(np.stack(acc), axis=0)
    print(f"[序列] {len(files)} 帧  →  {dst_dir}   共用背景 {bg.astype(int)}")
    tot_h = 0
    for i, f in enumerate(files):
        rgb = np.array(Image.open(f).convert("RGB"))
        print(f"  [{i+1}/{len(files)}] {os.path.basename(f)}")
        rgba, rep = one(rgb, bg)
        tot_h += rep["n_big_holes"]
        out = rgba if args.no_crop else _crop(rgba, args.margin)
        Image.fromarray(out).save(os.path.join(dst_dir,
                                              os.path.splitext(os.path.basename(f))[0] + ".png"))
    print(f"\n[完成] {len(files)} 帧   ≥8px 洞合计 {tot_h} 个")
    print("⭐ 提醒：验『漏抠 / 透明区』合成到【青色底】；验『边缘观感』用【中灰底】")
    print("⭐ 勾线切的价值在硬边：人物 / 道具 / 有描边的插画。发丝级细结构仍归 matting。")


if __name__ == "__main__":
    main()
