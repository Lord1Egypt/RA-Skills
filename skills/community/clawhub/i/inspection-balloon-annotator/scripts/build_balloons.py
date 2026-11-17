# -*- coding: utf-8 -*-
"""
图纸气泡标准助手 —— 气泡标注图生成（PyMuPDF 矢量叠加：红圈+引线+编号）
用法:
  python build_balloons.py --dims work/dims_table.py --pdf <图.pdf> --png work/render.png \
        [--ocr work/ocr_master.json] [--out outputs] [--work work]
说明:
  - DIMS 来自 --dims 指定的数据模块（字段见 dims_table_template.py）。
  - 标注半径按 PDF 页面缩放比换算为真实像素半径 Rpx，避免渲染图上气泡互相重叠（关键修复）。
  - 输出: <图号>_气泡标注图_p1.pdf / .png，以及 work/balloons.json（供两份检验表复用）。
"""
import json, math, os, sys, re, argparse, importlib.util
import pymupdf
from PIL import Image
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--dims", required=True, help="尺寸主数据模块 dims_table.py 路径")
ap.add_argument("--pdf", required=True, help="源图纸 PDF")
ap.add_argument("--png", required=True, help="源图纸渲染 PNG（与 PDF 同视角、同分辨率）")
ap.add_argument("--ocr", default="work/ocr_master.json", help="OCR 文字框 json（障碍锚点）")
ap.add_argument("--out", default="outputs", help="标注图输出目录")
ap.add_argument("--work", default="work", help="中间产物目录（balloons.json 落盘处）")
ap.add_argument("--name", default=None, help="输出文件名主名（默认取 PDF 主名）")
ap.add_argument("--no-pdf", action="store_true", help="跳过输出 PDF（仅输出 PNG，可省去 deflate 时间）")
ap.add_argument("--no-png", action="store_true", help="跳过输出 PNG（仅输出 PDF；表B内嵌图仍可单独栅格化，见 gen_qc_items）")
a = ap.parse_args()

# ---- 载入尺寸主数据 ----
spec = importlib.util.spec_from_file_location("dims_table", a.dims)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
DIMS = mod.DIMS
# 气泡允许区域：优先取尺寸主表里的 ALLOWED_REGIONS（排除标题栏/图框栏，防止气泡飘入标题栏）
ALLOWED_REGIONS = getattr(mod, "ALLOWED_REGIONS", None)

SRC_PDF, SRC_PNG = a.pdf, a.png
os.makedirs(a.out, exist_ok=True); os.makedirs(a.work, exist_ok=True)
stem = a.name or os.path.splitext(os.path.basename(SRC_PDF))[0]

RED = (1, 0, 0)
MM = 2.8346   # 1mm = 2.8346pt

# ---------------- 一般公差（默认 GB/T 1804-2000 f 级；可在 dims_table 用 GENERAL_TOL_MAP / GENERAL_TOL_NAME 覆盖）----------------
GT_MAP = getattr(mod, "GENERAL_TOL_MAP", None)   # [(阈值, 公差串), ...] 阈值升序
GT_NAME = getattr(mod, "GENERAL_TOL_NAME", None)  # 如 "一般公差GB/T15055 m级"
def gt_linear(v):
    if GT_MAP:
        for thr, tol in GT_MAP:
            if v <= thr: return tol
        return GT_MAP[-1][1]
    if v <= 3:   return "±0.05"
    if v <= 6:   return "±0.05"
    if v <= 30:  return "±0.1"
    if v <= 120: return "±0.15"
    if v <= 400: return "±0.2"
    return "±0.3"

for d in DIMS:
    try: v = float(d.get("nom", "") or "nan")
    except Exception: v = None
    if d["kind"] == "note":    d["final_tol"], d["tol_src"] = "—", "工艺注记"
    elif d["kind"] == "frame":  d["final_tol"], d["tol_src"] = "图纸框格值", "图纸标注"
    elif d["kind"] == "thread": d["final_tol"], d["tol_src"] = "按螺纹标准", "螺纹标准"
    elif d.get("unit2") == "deg":
        d["final_tol"], d["tol_src"] = "±1°", (GT_NAME + "(角度)") if GT_NAME else "一般公差GB/T1804-f(角度)"
    elif d["ext"]:             d["final_tol"], d["tol_src"] = d["ext"], "图纸标注"
    elif v is None:            d["final_tol"], d["tol_src"] = "待确认", "未声明"
    else:                      d["final_tol"], d["tol_src"] = gt_linear(v), (GT_NAME or "一般公差GB/T1804-2000 f级")

# ---------------- 编号（视图内 上→下、左→右）----------------
VIEW_ORDER = getattr(mod, "VIEW_ORDER", None)
if VIEW_ORDER is None:
    seen = []
    for d in DIMS:
        if d["v"] not in seen: seen.append(d["v"])
    VIEW_ORDER = seen
byv = {}
for d in DIMS: byv.setdefault(d["v"], []).append(d)
ordered = []
for v in VIEW_ORDER:
    g = byv.get(v, []); g.sort(key=lambda x: (round(x["ay"]/45), x["ax"]))
    ordered += g
for i, d in enumerate(ordered, 1): d["no"] = i
TOTAL = len(ordered)

# ---------------- 障碍：OCR 文字框 + 图像密度 ----------------
def _load_boxes(path):
    ocr = json.load(open(path, encoding="utf-8"))
    raw = ocr["labels"] if isinstance(ocr, dict) and "labels" in ocr else ocr
    out = []
    for o in raw:
        if "x0" in o and "y0" in o and "x1" in o and "y1" in o:
            out.append((o["x0"], o["y0"], o["x1"], o["y1"]))
        elif "x" in o and "w" in o:
            x, y, w, h = o["x"], o["y"], o["w"], o["h"]
            out.append((x-w/2, y-h/2, x+w/2, y+h/2))
    return out
BOXES = _load_boxes(a.ocr) if os.path.exists(a.ocr) else []

im = Image.open(SRC_PNG).convert("L"); W, H = im.size
GEO = (np.array(im.resize((W//6, H//6), Image.BILINEAR), dtype=np.float32) < 165).astype(np.float32)

def geo_frac(cx, cy, r):
    x0=max(0,int((cx-r)/6)); x1=min(GEO.shape[1],int((cx+r)/6)+1)
    y0=max(0,int((cy-r)/6)); y1=min(GEO.shape[0],int((cy+r)/6)+1)
    if x1<=x0 or y1<=y0: return 1.0
    return float(GEO[y0:y1, x0:x1].mean())

def in_allowed(cx, cy, r):
    # 若尺寸主表声明了 ALLOWED_REGIONS，则气泡圆心必须落在其中之一（留 r 边距，保证整圆在区内）
    if ALLOWED_REGIONS:
        for (x0, y0, x1, y1) in ALLOWED_REGIONS:
            if x0 + r < cx < x1 - r and y0 + r < cy < y1 - r: return True
        return False
    # 通用默认：整页留边（未声明区域时）
    if 30 < cx < W-30 and 30+r < cy < H-r: return True
    return False

def hit_boxes(cx, cy, r, pad=7, skip=None):
    n = 0
    for b in BOXES:
        if skip is not None and b == skip: continue
        nx = min(cx+r, b[2]+pad) - max(cx-r, b[0]-pad)
        ny = min(cy+r, b[3]+pad) - max(cy-r, b[1]-pad)
        if nx > 0 and ny > 0: n += 1
    return n

def seg_hits(p, q, skip=None):
    n = 0
    for i in range(1, 17):
        t = i/17.0
        x = p[0]+(q[0]-p[0])*t; y = p[1]+(q[1]-p[1])*t
        for b in BOXES:
            if skip is not None and b == skip: continue
            if b[0]-3 < x < b[2]+3 and b[1]-3 < y < b[3]+3:
                n += 1; break
    return n

def own_box(ax, ay):
    best, bestd = None, 1e9
    for b in BOXES:
        cx, cy = (b[0]+b[2])/2, (b[1]+b[3])/2
        dd = (cx-ax)**2 + (cy-ay)**2
        if dd < bestd: bestd, best = dd, b
    if best and bestd < 95**2:
        if best[0]-4 <= ax <= best[2]+4 and best[1]-4 <= ay <= best[3]+4: return best
    return None

def edge_point(ax, ay, box, cx, cy, pad=9):
    if box is None:
        vx, vy = ax-cx, ay-cy; n = math.hypot(vx, vy) or 1
        return ax - vx/n*12, ay - vy/n*12
    x0,y0,x1,y1 = box[0]-pad, box[1]-pad, box[2]+pad, box[3]+pad
    vx, vy = ax-cx, ay-cy
    ts = []
    if abs(vx) > 1e-6:
        for xb in (x0, x1):
            t = (xb-cx)/vx
            if t > 0 and y0 <= cy+vy*t <= y1: ts.append(t)
    if abs(vy) > 1e-6:
        for yb in (y0, y1):
            t = (yb-cy)/vy
            if t > 0 and x0 <= cx+vx*t <= x1: ts.append(t)
    if ts:
        t = min(ts); return cx+vx*t, cy+vy*t
    return ax, ay

# ---------------- 页面缩放：真实像素半径 ----------------
doc = pymupdf.open(SRC_PDF); page = doc[0]
SX = page.rect.width / W
SY = page.rect.height / H
def Rpx(no):
    return (11.3 if no >= 100 else 8.5) / min(SX, SY)

# ---------------- 布局 ----------------
def support(box, ux, uy, pad=4):
    if box is None: return 14.0
    hw = (box[2]-box[0])/2 + pad; hh = (box[3]-box[1])/2 + pad
    sx = hw/abs(ux) if abs(ux) > 1e-6 else 1e9
    sy = hh/abs(uy) if abs(uy) > 1e-6 else 1e9
    return min(sx, sy)

placed, RES = [], []
for d in ordered:
    no = d["no"]; R = Rpx(no)
    ax, ay = d["ax"], d["ay"]
    ob = own_box(ax, ay)
    best = None
    for k in range(72):
        ang = math.radians(k*5.0)
        ux, uy = math.cos(ang), math.sin(ang)
        dmin = R + 10 + support(ob, ux, uy)
        for extra in (0, 20, 45, 80, 130, 190, 260, 340):
            dist = dmin + extra
            cx, cy = ax+ux*dist, ay+uy*dist
            if not in_allowed(cx, cy, R): continue
            th = hit_boxes(cx, cy, R, 24, skip=ob)
            ov = 0
            for (px, py, pR) in placed:
                need = R + pR + 8
                gap = math.hypot(cx-px, cy-py) - need
                if gap < 0: ov += 1 + (-gap)/need
            ep = edge_point(ax, ay, ob, cx, cy)
            lh = seg_hits((cx, cy), ep, skip=ob)
            cost = dist + 1200*geo_frac(cx, cy, R) + 300*lh + 2600*th + 4000*ov
            if best is None or cost < best[0]: best = (cost, cx, cy, th, ov, lh)
        if best and best[3] == 0 and best[4] == 0 and best[5] == 0: break
    _, cx, cy = best[0], best[1], best[2]
    placed.append((cx, cy, R))
    d["bx"], d["by"] = cx, cy
    RES.append(d)

# ---- 松弛推挤（消除残余重叠，保持不碰文字、不出界）----
for _ in range(120):
    moved = 0.0
    for i in range(len(RES)):
        a0 = RES[i]; Ra = Rpx(a0["no"])
        fx = fy = 0.0
        for j in range(len(RES)):
            if i == j: continue
            b0 = RES[j]; Rb = Rpx(b0["no"])
            dx, dy = a0["bx"]-b0["bx"], a0["by"]-b0["by"]
            dd = math.hypot(dx, dy) or 1e-6
            need = Ra + Rb + 8
            if dd < need:
                p = (need-dd)/need
                fx += dx/dd*p*26; fy += dy/dd*p*26
        if fx or fy:
            a0["_tx"] = a0.get("_tx", 0)+fx; a0["_ty"] = a0.get("_ty", 0)+fy
    for a0 in RES:
        tx, ty = a0.pop("_tx", 0), a0.pop("_ty", 0)
        if not tx and not ty: continue
        Ra = Rpx(a0["no"])
        nx, ny = a0["bx"]+tx*0.5, a0["by"]+ty*0.5
        if in_allowed(nx, ny, Ra) and hit_boxes(nx, ny, Ra, 20, skip=own_box(a0["ax"], a0["ay"])) == 0:
            moved += abs(tx)+abs(ty)
            a0["bx"], a0["by"] = nx, ny
    if moved < 40: break

json.dump(RES, open(os.path.join(a.work, "balloons.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("TOTAL balloons:", TOTAL, "| 3位数编号:", sum(1 for d in RES if d["no"] >= 100))

# ---------------- 绘制（PDF 矢量叠加）----------------
# 坐标系说明（实测）：render_pdf.py 与 build_balloons.py 出图都用 page.get_pixmap(matrix=.../dpi=...)，
# 二者均为“页面原生(未旋转)坐标系”，与 render.png 完全一致（不应用 /Rotate）。
# 故绘制时只需按 render 像素→页面点的比例缩放即可，标注与底图天然对齐（无需矩阵换算）。
sx = page.rect.width / W
sy = page.rect.height / H
_DM = page.derotation_matrix
def P(x, y):
    X, Y = x*sx, y*sy
    return (X*_DM.a + Y*_DM.c + _DM.e, X*_DM.b + Y*_DM.d + _DM.f)

for d in RES:
    no = d["no"]; R = 11.3 if no >= 100 else 8.5
    cx, cy = P(d["bx"], d["by"])
    ax, ay = P(d["ax"], d["ay"])
    vx, vy = cx-ax, cy-ay; n = math.hypot(vx, vy) or 1
    ex, ey = cx - vx/n*R, cy - vy/n*R
    tipx, tipy = P(*edge_point(d["ax"], d["ay"], own_box(d["ax"], d["ay"]), d["bx"], d["by"]))
    page.draw_line((ex, ey), (tipx, tipy), color=RED, width=0.5)
    ux, uy = tipx-ex, tipy-ey; un = math.hypot(ux, uy) or 1
    ux, uy = ux/un, uy/un
    px, py = -uy, ux
    L, Wd = 3.6, 1.15
    p1 = (tipx, tipy)
    p2 = (tipx-ux*L+px*Wd, tipy-uy*L+py*Wd)
    p3 = (tipx-ux*L-px*Wd, tipy-uy*L-py*Wd)
    page.draw_polyline([p1, p2, p3], color=RED, fill=RED, width=0.3)
    page.draw_circle((cx, cy), R, color=RED, width=1.0)
    txt = str(no)
    fs = 11.3
    tl = pymupdf.get_text_length(txt, fontname="helv", fontsize=fs)
    # 关键修复：标注图 PNG 用 page.get_pixmap(dpi=300) 出图，与 render.png 同为“页面原生坐标系”，
    # 不应用 /Rotate。因此编号一律正立(rotate=0)绘制、并水平/垂直居中于圆心，
    # 绝不再做旋转补偿（否则数字会倒立且按角点锚定、跑出圆圈）。
    page.insert_text((cx - tl/2, cy + fs*0.35), txt, fontname="helv", fontsize=fs, color=RED)

if a.no_pdf:
    print("skip PDF output (--no-pdf)")
else:
    doc.save(os.path.join(a.out, f"{stem}_气泡标注图_p1.pdf"), deflate=True, garbage=3)
if a.no_png:
    print("skip PNG output (--no-png)")
else:
    pix = page.get_pixmap(dpi=300)
    pix.save(os.path.join(a.out, f"{stem}_气泡标注图_p1.png"))
print("saved annotated" + (" png only" if a.no_pdf else "") +
      (" pdf only" if a.no_png else "") +
      (" pdf + png" if not a.no_pdf and not a.no_png else "") + " ->", a.out)
