# -*- coding: utf-8 -*-
"""
检验气泡标注 —— 通用自动尺寸抽取（初稿）
从 OCR 文字框(labels.json) + 渲染图(render.png) 自动生成 work/dims_table.py 初稿。

设计目标：把"按图纸手搓 gen_dims"这一步变成一条通用命令，让 Skill 在收到图纸后
能"立即执行"全链路，无需针对每张图手工调参。

说明（重要，务必转达工程师）：
  - 本抽取是 AI 初筛，不是最终结果。对每张图都会：
      * 自动识别并剔除标题栏 / 修订栏 / 公司信息 / 技术要求块（基于位置+关键词）；
      * 识别直径⌀、半径R、螺纹M/G/NPT、显式公差±、普通线性尺寸、粗糙度Ra注记等；
      * 公差就近并入最近尺寸；近距去重；按空间聚类成视图；CC/SC/NC 启发式标注。
  - 所有 CC/SC/NC 均带【初判X,待复核】标记，最终分类以工程师确认为准。
  - 抽取结果须经 coverage_report 的"待确认清单" + 目视复核后再正式下发。

用法:
  python auto_extract_dims.py --labels work/labels.json --png work/render.png \
        --out work/dims_table.py [--meta work/drawing_meta.json]
"""
import json, re, os, argparse, math
from collections import Counter
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--labels", required=True, help="OCR 文字框 json")
ap.add_argument("--png", required=True, help="render.png（用于图像尺寸/密度）")
ap.add_argument("--out", required=True, help="输出 dims_table.py 路径")
ap.add_argument("--meta", default=None, help="drawing_meta.json（可选）")
a = ap.parse_args()

ocr = json.load(open(a.labels, encoding="utf-8"))
L = ocr["labels"] if isinstance(ocr, dict) and "labels" in ocr else ocr

im = Image.open(a.png).convert("L")
W, H = im.size
print(f"[auto_extract] image {W}x{H}, OCR labels: {len(L)}")

# ---------------- 1. 通用排除：标题栏 / 修订栏 / 公司信息 / 技术要求 ----------------
# 关键词黑名单（通用，跨图纸适用）
SKIP_KW = [
    "零件代号","借","旧底图","底图总号","签字","标记","处数","签名","年月日","日期",
    "设计","校对","审核","批准","表面处理","投影","共张","版本","数量","比例","比例 ",
    "技术要求","未注","标准化","有限公司","公司","地址","电话","传真","图纸","第",
    "页","rev","REV","scale","SCALE","weight","WEIGHT","材质","材料","牌号","余量",
    "其余","粗糙度","Ra","制图","描图","装配","共 ","张","阶段标记","认证","网址",
    "工艺","分区","受控","更改文件号","序号","标记","处数","批准日期","会签","重量",
    "CO.","LTD","Co.,Ltd","CO.,LTD","邮编","邮箱","QQ","微信","备注","说明","图号",
    "名称","A-A","B-B","C-C","D-D","E-E","F-F","视图","剖视","断面","放大",
    "MST","SUS","Q235","45#","料","牌号","kg","KG","图样","GB","ISO","等级","精度",
    "VF","IN","OUT","LTD","PCD","HRC","HB","MPa","N·m","±0.0",
]
def is_skip_kw(t):
    return any(k.lower() in t.lower() for k in SKIP_KW)

# 标题栏/修订栏自动检测：图纸最下方（底部 35% 带）通常集中标题栏/修订栏文字。
# 在该带内对文字框做邻近聚类（中心距 <160px 归同簇），簇内框数 >=4 视为标题栏/修订栏块，
# 取其并集包围盒（外扩 15px）作为排除区。这样无论标题栏在右下角、底部居中或底部偏左都能命中，
# 又不会误伤同一带内稀疏分布的真实尺寸（如左下角视图的尺寸）。
import math as _math
def detect_titleblock(boxes):
    band = [b for b in boxes if b[3] > 0.65*H]
    if len(band) < 4:
        return []
    pts = [((b[0]+b[2])/2.0, (b[1]+b[3])/2.0) for b in band]
    clusters = []
    for (cx, cy), b in zip(pts, band):
        hit = None
        for cl in clusters:
            if any(_math.hypot(cx-ox, cy-oy) < 160 for (ox, oy) in cl["pts"]):
                hit = cl; break
        if hit:
            hit["pts"].append((cx, cy)); hit["boxes"].append(b)
        else:
            clusters.append({"pts": [(cx, cy)], "boxes": [b]})
    regions = []
    for cl in clusters:
        if len(cl["boxes"]) < 4:
            continue
        xs = [b[0] for b in cl["boxes"]] + [b[2] for b in cl["boxes"]]
        ys = [b[1] for b in cl["boxes"]] + [b[3] for b in cl["boxes"]]
        regions.append((min(xs)-15, min(ys)-15, max(xs)+15, max(ys)+15))
    return regions

boxes_all = []
for o in L:
    if "x0" in o and "y0" in o and "x1" in o and "y1" in o:
        boxes_all.append((o["x0"], o["y0"], o["x1"], o["y1"]))
    elif "x" in o and "w" in o:
        boxes_all.append((o["x"]-o["w"]/2, o["y"]-o["h"]/2, o["x"]+o["w"]/2, o["y"]+o["h"]/2))
TB = detect_titleblock(boxes_all)
print(f"[auto_extract] detected title block regions: {TB}")

def in_excluded(x, y):
    # 底部修订/比例条
    if y > 0.95*H: return True
    # 顶部图框标题条
    if y < 0.03*H: return True
    # 检测到的标题栏/修订栏块（任意位置）
    if TB:
        for (x0, y0, x1, y1) in TB:
            if x0 < x < x1 and y0 < y < y1:
                return True
    return False

# ---------------- 2. 候选收集 ----------------
cands = []
for o in L:
    t = (o.get("text") or "").strip()
    if not t: continue
    if is_skip_kw(t): continue
    x = o.get("x", (o.get("x0",0)+o.get("x1",0))/2)
    y = o.get("y", (o.get("y0",0)+o.get("y1",0))/2)
    w = o.get("w", (o.get("x1",x)-o.get("x0",x)) if "x1" in o else 10)
    if in_excluded(x, y): continue
    # 比例 / 代号等非尺寸（如 2:1、MST-F800-04、GB/T）
    if ":" in t: continue
    if re.search(r"^[A-Za-z]{2,}-", t): continue
    cands.append({"t": t, "x": x, "y": y, "w": w, "conf": o.get("conf", 0)})
print(f"[auto_extract] after exclusion: {len(cands)} candidates")

# ---------------- 3. 数字/特征抽取 ----------------
def num(s):
    s2 = re.sub(r"(?<=\d) +(?=\d)", "", s)          # "0. 02"->"0.02"
    s2 = s2.replace(" ", "")
    m = re.search(r"(\d+(?:\.\d+)?)", s2)
    return float(m.group(1)) if m else None

def is_roughness(t):
    v = num(t)
    if v is None: return False
    if re.search(r"^[Rr][Aa]?$", t.replace(str(v),"").strip() or t) : return True
    if "ra" in t.lower(): return True
    if v in (0.2,0.4,0.8,1.6,3.2,6.3,12.5,25,50) and not re.search(r"[+\-±/=]", t): return True
    return False

def clean_text(t):
    # 常见 OCR 误读修正（通用）
    t = t.replace("'0F","").replace("0F","").replace("500F","⌀50").replace("50'0F","⌀50")
    t = t.replace("500.0","⌀50").replace(".LTO","").replace("'0","")
    # ⌀ 被读成 @ 或 0 的情况
    if t.startswith("@") and re.match(r"^@\d", t): t = "⌀" + t[1:]
    return t

dims = []
seen = []
def add(kind, t, nom, x, y, ext="", note=""):
    key = (round(x/8), round(y/8), kind)
    for (sx, sy, sk) in seen:
        if sk == kind and abs(sx-round(x/8))<6 and abs(sy-round(y/8))<6:
            return
    seen.append(key)
    dims.append({"kind": kind, "t": t, "nom": nom, "ext": ext,
                 "ax": x, "ay": y, "note": note})

for c in cands:
    t = c["t"]; x = c["x"]; y = c["y"]
    # 螺纹 (M/G/NPT/Rc/Tr/... + 螺距/精度)，含 "2-M3" 这类带前导数字
    if re.match(r"^[A-Za-z0-9]?-?M\d", t) or (t.startswith("M") and ("×" in t or "*" in t or "h" in t or re.search(r"M\d", t))):
        add("thread", t, None, x, y); continue
    if re.match(r"^(G|NPT|Rc|Rp|Tr|UNC|UNF)\d", t):
        add("thread", t, None, x, y); continue
    # 倒角 C
    if re.search(r"C\d", t) or re.search(r"^\d+-C", t) or re.search(r"C\d$", t):
        add("note", t, num(t), x, y, note="倒角"); continue
    # 直径 ⌀（含 OCR 误读 @/0）
    if t.startswith("@") or t.startswith("⌀") or t.startswith("0") and re.match(r"^0\d", t) and "." in t:
        v = num(t)
        if v is not None and 0 < v < 2000:
            add("dim", "⌀"+str(v), v, x, y); continue
    # 半径 R
    if re.match(r"^R\d", t) or t.startswith("R") and re.match(r"^R\d", t):
        v = num(t)
        if v is not None and 0 < v < 5000:
            add("dim", "R"+str(v), v, x, y); continue
    # 显式公差（+0.0x / ±0.0x / +0 -0 / ...）
    if re.search(r"[+\-±]\s*0?\.\d+", t) or re.search(r"±\s*\d", t) or re.match(r"^[+\-]", t):
        tt = t.replace(" ", "")
        if re.search(r"[+\-±]", tt):
            add("tol", tt, None, x, y, note="公差"); continue
    # 角度（带 °）
    if "°" in t or "度" in t:
        v = num(t)
        add("dim", t, v if v else "", x, y); continue
    # 普通数值
    v = num(t)
    if v is not None:
        if is_roughness(t):
            add("note", t, v, x, y, note="粗糙度Ra"); continue
        if 0 < v < 10000:
            add("dim", str(v), v, x, y); continue
    # 其它短文本保留为注记（便于复核，不直接丢弃）
    if len(t) <= 10 and not re.match(r"^[+\-±]", t):
        add("note", t, v, x, y)

# ---------------- 4. 公差就近并入最近尺寸 ----------------
tol_items = [d for d in dims if d["kind"] == "tol"]
for ti in tol_items:
    best = None; bd = 1e9
    for d in dims:
        if d["kind"] != "dim": continue
        dd = math.hypot(d["ax"]-ti["ax"], d["ay"]-ti["ay"])
        if dd < bd: bd, best = dd, d
    if best and bd < max(140, 0.04*W):
        # 不覆盖已有更完整的公差
        if not best["ext"] or len(ti["t"]) > len(best["ext"]):
            best["ext"] = ti["t"]
dims = [d for d in dims if d["kind"] != "tol"]

# ---------------- 5. 清洗 + 近距去重 ----------------
for d in dims:
    if d["kind"] in ("dim","note"):
        d["t"] = clean_text(d["t"])
        if d["t"].startswith("⌀"):
            nv = num(d["t"]); 
            if nv: d["nom"] = nv
dims.sort(key=lambda d: (round(d["ay"]), round(d["ax"])))
dedup = []
for d in dims:
    dup = False
    for e in reversed(dedup):
        if math.hypot(d["ax"]-e["ax"], d["ay"]-e["ay"]) < max(28, 0.012*W):
            if d["ext"] and not e["ext"]: e["ext"] = d["ext"]
            if len(d["t"]) > len(e["t"]): e["t"] = d["t"]
            dup = True; break
    if not dup: dedup.append(d)
dims = [d for d in dedup if d["t"]]
dims = [d for d in dims if not is_skip_kw(d["t"])]

# ---------------- 6. 视图聚类（空间就近）----------------
def cluster(items, thr):
    items = sorted(items, key=lambda d: (d["ay"], d["ax"]))
    groups = []
    for d in items:
        placed = False
        for g in groups:
            cx = sum(i["ax"] for i in g)/len(g); cy = sum(i["ay"] for i in g)/len(g)
            if math.hypot(d["ax"]-cx, d["ay"]-cy) < thr:
                g.append(d); placed = True; break
        if not placed: groups.append([d])
    return groups

thr = max(420, 0.12*W)
gs = cluster(dims, thr=thr)
flat = [(g, sum(i["ay"] for i in g)/len(g), sum(i["ax"] for i in g)/len(g)) for g in gs]
flat.sort(key=lambda t: (round(t[1]/200), t[2]))
view_of = {}
for idx, (g, cy, cx) in enumerate(flat):
    name = f"视图{idx+1}"
    for d in g: view_of[id(d)] = name

# ---------------- 7. CC/SC/NC 启发式（全部标待复核）----------------
TIGHT = ("±0.01", "+0.01", "-0.01", "0.01")
DIMS = []
for d in dims:
    ext = d.get("ext","") or ""
    note = d.get("note") or ""
    cls = "NC"; mark = ""
    if d["kind"] == "thread":
        cls = "SC"; mark = "【初判SC,待复核】"
    elif d["nom"] == 0.015 or d["nom"] == 0.02 and ext:   # 疑似形位/紧公差
        cls = "CC"; mark = "【初判CC,待复核】"
    elif ext:
        if any(k in ext for k in TIGHT) or "0.01" in ext:
            cls = "CC"; mark = "【初判CC,待复核】"
        else:
            cls = "SC"; mark = "【初判SC,待复核】"
    elif "C1" in str(d["t"]) or "倒角" in note:
        cls = "SC"; mark = "【初判SC,待复核】"
    n = (note + " " + mark).strip() if (note or mark) else ""
    DIMS.append(dict(
        v=view_of[id(d)],
        t=d["t"],
        n=n,
        nom=(d["nom"] if d["nom"] is not None else ""),
        kind=d["kind"],
        ext=ext,
        ax=round(d["ax"],1),
        ay=round(d["ay"],1),
        cls=cls,
    ))

# ---------------- 8. 允许区域（只剔除图框上下边）----------------
# 标题栏/修订栏已由 in_excluded 在抽取阶段排除，DIMS 本身不含其文字，
# 故此处不做基于 TB 的整体裁剪，避免误伤标题栏在底部居中时其上方/两侧的真实视图。
ALLOWED_REGIONS = [(0, int(0.03*H), W, int(0.97*H))]

# ---------------- 9. 写出 dims_table.py ----------------
py = ["# -*- coding: utf-8 -*-",
      f"# 自动抽取初稿（render 像素坐标 {W}x{H}）",
      f"# 抽取条目: {len(DIMS)} | 视图数: {len(flat)}",
      "# 注意：AI 初筛，CC/SC/NC 均带【待复核】标记，正式使用前须工程师确认。",
      "DIMS = ["]
for d in DIMS:
    py.append("  dict(v=%r, t=%r, n=%r, nom=%r, kind=%r, ext=%r, ax=%r, ay=%r, cls=%r),"
              % (d["v"], d["t"], d["n"], d["nom"], d["kind"], d["ext"], d["ax"], d["ay"], d["cls"]))
py.append("]")
py.append("VIEW_ORDER = " + repr(sorted(set(d['v'] for d in DIMS))))
py.append("ALLOWED_REGIONS = " + repr(ALLOWED_REGIONS))
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
open(a.out, "w", encoding="utf-8").write("\n".join(py) + "\n")

print("total dims:", len(DIMS))
print("kinds:", dict(Counter(d["kind"] for d in DIMS)))
print("views:", dict(Counter(d["v"] for d in DIMS)))
print("cls:", dict(Counter(d["cls"] for d in DIMS)))
print(f"[auto_extract] -> {a.out}")
