# -*- coding: utf-8 -*-
"""检验表 B：3 表式检验记录表（检验记录表 + 内嵌气泡图 + 未注公差基准）
把同一份主数据 balloons.json 变换为 items.json，复用 build_inspection_xlsx 出表。
用法: python gen_qc_items.py [--balloons work/balloons.json] [--png outputs/..._气泡标注图_p1.png]
       [--meta work/drawing_meta.json] [--out outputs/检验记录表.xlsx] [--title 标题]

注意：gen_combined 会复用本模块的 build_items(DATA, meta)。
"""
import json, os, sys, argparse, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_inspection_xlsx as B


def parse_tol(s):
    s = (s or "").strip()
    if not s or s in ("—", "图纸框格值", "按螺纹标准", "待确认", "工艺注记"):
        return "—", "—"
    if s.startswith("±"):
        v = s[1:]; return "+"+v, "-"+v
    if "/" in s:
        up, lo = s.split("/", 1)
        return up, lo
    return s, s

def gauge_of(d):
    k = d["kind"]
    if k == "thread": return "螺纹量规/通止规"
    if k == "frame":  return "三坐标/专用检具"
    if k == "note":   return "目视/文件核对"
    return "通用量具(卡尺/千分尺/高度规)"

def method_of(d):
    k = d["kind"]
    if k == "thread": return "通止规检验，必要时密封/扭力抽查"
    if k == "frame":  return "三坐标/专用检具按框格值检测"
    if k == "note":   return "按工艺/表面处理要求目视或文件核对"
    if d["ext"]:      return "按显式公差用通用量具检测"
    if d["final_tol"].startswith("±") or "/" in d["final_tol"]:
        return "按一般公差(GB/T1804 f)用通用量具检测"
    return "按图纸/工艺确认"

def level_of(d):
    return {"CC": "A", "SC": "B"}.get(d["cls"], "C")

def build_items(DATA, meta):
    title = meta.get("title", "尺寸与形位公差检验记录表")
    info = meta.get("info") or [
        ["零件名称", meta.get("part", "（待填）"), "图号", meta.get("drawing_no", "（待填）")],
        ["材料", meta.get("material", "（待填）"), "表面处理", meta.get("treatment", "（待填）")],
        ["未注公差", meta.get("tolerance_note", "尺寸 GB/T1804-2000 f级 / 形位 GB/T1184-1996 H级"),
         "检验类别", meta.get("inspection_type", "首件检验")],
    ]
    items = {"title": title, "info": info, "items": [], "explicit": [["标注", "数值", "说明"]]}
    for d in DATA:
        if d["ext"]:
            up, lo = parse_tol(d["ext"])
        else:
            up, lo = parse_tol(d["final_tol"])
        items["items"].append({
            "no": d["no"], "view": d["v"], "item": d["t"],
            "basic": d["nom"] if d["nom"] else "—",
            "upper": up, "lower": lo, "tol": d["final_tol"],
            "gauge": gauge_of(d), "method": method_of(d), "level": level_of(d),
        })
        if d["ext"]:
            items["explicit"].append([d["t"], d["ext"], d.get("note") or ""])
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--balloons", default="work/balloons.json")
    ap.add_argument("--png", default=None, help="标注图 PNG（内嵌到表2；可省）")
    ap.add_argument("--meta", default="work/drawing_meta.json", help="图纸信息(标题/图号/材料等)")
    ap.add_argument("--out", default="outputs/检验记录表.xlsx")
    ap.add_argument("--title", default=None)
    a = ap.parse_args()

    DATA = json.load(open(a.balloons, encoding="utf-8"))
    meta = {}
    if os.path.exists(a.meta):
        meta = json.load(open(a.meta, encoding="utf-8"))
    items = build_items(DATA, meta)
    title = a.title or items.get("title", "尺寸与形位公差检验记录表")

    B.build(items, a.png, a.out, title)
    print("saved 检验记录表(3表):", a.out, "| items:", len(items["items"]),
          "| A/B/C:", sum(1 for x in items["items"] if x["level"]=="A"),
          sum(1 for x in items["items"] if x["level"]=="B"),
          sum(1 for x in items["items"] if x["level"]=="C"))


if __name__ == "__main__":
    main()
