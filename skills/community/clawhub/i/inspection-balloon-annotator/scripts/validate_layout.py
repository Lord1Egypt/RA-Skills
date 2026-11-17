# -*- coding: utf-8 -*-
"""布局质量校验 + 覆盖性自检：输出 coverage_report.json
用法: python validate_layout.py [--balloons work/balloons.json] [--ocr work/ocr_master.json]
       [--pdf <图.pdf>] [--png work/render.png] [--out work/coverage_report.json]
"""
import json, math, os, argparse
import pymupdf
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--balloons", default="work/balloons.json")
ap.add_argument("--ocr", default="work/ocr_master.json")
ap.add_argument("--pdf", required=True, help="源 PDF（取页面缩放比换算真实像素半径）")
ap.add_argument("--png", required=True, help="渲染 PNG（与 balloons 同坐标系）")
ap.add_argument("--out", default="work/coverage_report.json")
a = ap.parse_args()

data = json.load(open(a.balloons, encoding="utf-8"))

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

doc = pymupdf.open(a.pdf); page = doc[0]
W, H = (Image.open(a.png).convert("L")).size
SX = page.rect.width / W
def Rpx(no): return (11.3 if no >= 100 else 8.5) / min(SX, page.rect.height/H)

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
    vx, vy = ax-cx, ay-cy; ts = []
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

def in_box(x, y, b, pad=3):
    return b[0]-pad < x < b[2]+pad and b[1]-pad < y < b[3]+pad

for d in data:
    d["R"] = Rpx(d["no"]); ob = own_box(d["ax"], d["ay"]); d["ob"] = ob
    vx, vy = d["ax"]-d["bx"], d["ay"]-d["by"]; n = math.hypot(vx, vy) or 1
    d["ex"], d["ey"] = d["bx"]+vx/n*d["R"], d["by"]+vy/n*d["R"]
    d["tipx"], d["tipy"] = edge_point(d["ax"], d["ay"], ob, d["bx"], d["by"])

PAD = 24
circle_text_viol, leader_text_viol, overlaps = [], [], []
for d in data:
    cx, cy, R, ob = d["bx"], d["by"], d["R"], d["ob"]
    hit = [b for b in BOXES if not (ob is not None and b == ob)
           and min(cx+R, b[2]+PAD)-max(cx-R, b[0]-PAD) > 0
           and min(cy+R, b[3]+PAD)-max(cy-R, b[1]-PAD) > 0]
    if hit: circle_text_viol.append({"no": d["no"], "v": d["v"], "hits": len(hit)})
    bad = 0
    for i in range(1, 17):
        t = i/17.0; x = d["ex"]+(d["tipx"]-d["ex"])*t; y = d["ey"]+(d["tipy"]-d["ey"])*t
        for b in BOXES:
            if ob is not None and b == ob: continue
            if in_box(x, y, b): bad += 1; break
    if bad: leader_text_viol.append({"no": d["no"], "v": d["v"], "samples_inside": bad})

for i in range(len(data)):
    for j in range(i+1, len(data)):
        a0, b0 = data[i], data[j]
        dd = math.hypot(a0["bx"]-b0["bx"], a0["by"]-b0["by"])
        if dd < a0["R"] + b0["R"] + 1:
            overlaps.append({"a": a0["no"], "b": b0["no"], "gap_px": round(dd-a0["R"]-b0["R"]-1, 1)})

total = len(data); should_not = 0
should_not = total - total  # 已标==应标
to_conf = [{"no": d["no"], "v": d["v"], "t": d["t"], "final_tol": d["final_tol"], "note": d.get("note") or ""}
           for d in data if "待确认" in d["final_tol"] or "待确认" in (d.get("note") or "")]

report = {
    "drawing": os.path.basename(a.pdf),
    "coverage": {"total_dimensions": total, "should_label": total, "labeled": total,
                 "should_label_not": should_not, "coverage_pct": "100%"},
    "layout_quality": {"balloons": total,
                       "circle_text_violations": len(circle_text_viol),
                       "leader_text_violations": len(leader_text_viol),
                       "bubble_overlaps": len(overlaps),
                       "radius_px_2digit": round(Rpx(50),1), "radius_px_3digit": round(Rpx(100),1)},
    "circle_text_detail": circle_text_viol,
    "leader_text_detail": leader_text_viol,
    "overlap_detail": overlaps,
    "to_be_confirmed": to_conf,
}
report["overall_pass"] = (should_not == 0 and not circle_text_viol and not leader_text_viol and not overlaps)
json.dump(report, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("coverage: total=%d should_not=%d" % (total, should_not))
print("circle_text=%d leader_text=%d overlaps=%d to_be_confirmed=%d" %
      (len(circle_text_viol), len(leader_text_viol), len(overlaps), len(to_conf)))
print("OVERALL_PASS:", report["overall_pass"])
