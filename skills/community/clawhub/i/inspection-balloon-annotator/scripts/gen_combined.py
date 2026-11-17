# -*- coding: utf-8 -*-
"""合并检验表：把「尺寸明细检验表」的 [汇总][关键特性专项] 并入「检验记录表」，尺寸明细 sheet 不输出。

输出单一 xlsx，sheet 顺序：
  1) 检验记录表        (原表B：逐条检验记录 + 检验结论)
  2) 标注图纸(气泡图)   (内嵌标注 PNG)
  3) 未注公差基准       (GB/T1804-f / GB/T1184-H 等)
  4) 汇总              (原表A：统计 + 各视图分布)
  5) 关键特性专项       (原表A：CC/SC 的 18 列明细)

用法: python gen_combined.py [--balloons work/balloons.json] [--png outputs/..._气泡标注图_p1.png]
       [--meta work/drawing_meta.json] [--out outputs/检验记录表.xlsx] [--cp 控制计划编号]
"""
import json, os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_inspection_xlsx as B
import gen_excel as G
import gen_qc_items as Q


def build_combined(DATA, meta, img_path, CP_ID):
    # 1) 表 B：检验记录表 + 标注图纸(气泡图) + 未注公差基准
    items = Q.build_items(DATA, meta)
    wb = B.build(items, img_path, None, items["title"], wb=None, embed_img=True)
    # 2) 并入 表 A 的 汇总 + 关键特性专项（尺寸明细 sheet 不输出）
    rows = G.make_rows(DATA, CP_ID)
    G.add_summary_sheet(wb, DATA, CP_ID)
    G.add_keychar_sheet(wb, rows, DATA)
    return wb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--balloons", default="work/balloons.json")
    ap.add_argument("--png", default=None, help="标注图 PNG（内嵌到『标注图纸(气泡图)』sheet）")
    ap.add_argument("--meta", default="work/drawing_meta.json")
    ap.add_argument("--out", default="outputs/检验记录表.xlsx")
    ap.add_argument("--cp", default="MEST/Q/CP-（按控制计划填写）")
    a = ap.parse_args()

    DATA = json.load(open(a.balloons, encoding="utf-8"))
    meta = {}
    if os.path.exists(a.meta):
        meta = json.load(open(a.meta, encoding="utf-8"))

    wb = build_combined(DATA, meta, a.png, a.cp)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    wb.save(a.out)
    n_sc = sum(1 for d in DATA if d["cls"] in ("CC", "SC"))
    print("saved 合并检验表:", a.out,
          "| sheets:", wb.sheetnames,
          "| 记录项:", len(DATA), "| 关键/重要特性(CC/SC):", n_sc)


if __name__ == "__main__":
    main()
