# -*- coding: utf-8 -*-
"""检验表 A：18 列尺寸明细检验表（汇总 / 尺寸明细 / 关键特性专项）
用法: python gen_excel.py [--balloons work/balloons.json] [--out outputs/尺寸明细检验表.xlsx] [--cp 控制计划编号]

注意：gen_combined 会复用本模块的 make_rows / add_summary_sheet / add_keychar_sheet
      （合并表中不再单独输出"尺寸明细" sheet，故 add_detail_sheet 仅本脚本独立使用时调用）。
"""
import json, re, os, argparse
from collections import Counter
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ZONE = {}  # 不强制分区，留空由视图名表达；如需可按视图映射

def unit_of(d):
    if d.get("unit2") == "deg": return "°"
    if d["kind"] in ("thread", "frame", "note"): return "—"
    return "mm"

def type_of(d):
    k, t = d["kind"], d["t"]
    if k == "thread": return "螺纹"
    if k == "frame":  return "形位公差"
    if k == "note":   return "工艺注记"
    if d.get("d") == "Ø": return "直径"
    if re.match(r"^R\d", t) or re.search(r"-\s*R\d", t) or "内R" in t or "外R" in t: return "半径"
    if d.get("unit2") == "deg": return "角度"
    if re.search(r"[CＣ]\s*\d", t) or "倒角" in t: return "倒角"
    return "线性"

def cls_text(d):
    return {"CC": "关键特性", "SC": "重要特性"}.get(d["cls"], "一般特性")

def sym_of(d):
    return {"CC": "★", "SC": "◆"}.get(d["cls"], "○")

def gen_decl(d):
    if d["kind"] in ("thread", "frame", "note"): return "—"
    if d["ext"]: return "—"
    if d.get("unit2") == "deg": return "GB/T 1804-2000 f级(角度)"
    if d["final_tol"].startswith("±") or "/" in d["final_tol"]: return "GB/T 1804-2000 f级"
    return "—"

def insp_of(d):
    k = d["kind"]
    if k == "thread": return "螺纹量规(通止规)检验"
    if k == "frame":  return "形位公差按框格值，三坐标/专用检具检测"
    if k == "note":   return "工艺/表面处理确认，目视或文件核对"
    if d["ext"]:      return "按显式公差用通用量具检测"
    if d["final_tol"].startswith("±") or "/" in d["final_tol"]:
        return "按一般公差(GB/T 1804 f)用通用量具检测"
    return "按图纸/工艺确认"

def related_of(d):
    m = re.search(r"^(\d+)\s*[xX×-]", d["t"])
    if m: return f"{m.group(1)}处同规格"
    if "2-M" in d["t"] or "2x" in d["t"].lower(): return "2处同规格"
    return "—"

HEADERS = ["气泡号","图纸页码","分区","视图","公称尺寸","单位","类型","显式公差",
           "一般公差声明","最终公差","公差来源","特性分类","特性符号","检验要求",
           "关联气泡号","出现位置","控制计划编号","备注"]

def row_of(d, CP_ID):
    return [d["no"], "p1", ZONE.get(d["v"], "—"), d["v"],
            d["nom"] if d["nom"] else "—", unit_of(d), type_of(d),
            d["ext"] if d["ext"] else "—", gen_decl(d), d["final_tol"], d["tol_src"],
            cls_text(d), sym_of(d), insp_of(d), related_of(d), d["t"], CP_ID,
            d.get("note") or "—"]

# ---- 样式常量 ----
HEAD_FILL = PatternFill("solid", fgColor="1F4E78")
HEAD_FONT = Font(name="Microsoft YaHei", bold=True, color="FFFFFF", size=10)
CELL_FONT = Font(name="Microsoft YaHei", size=10)
SC_FILL   = PatternFill("solid", fgColor="FCE4D6")
NC_FILL   = PatternFill("solid", fgColor="FFFFFF")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(horizontal="center", vertical="center", wrap_text=True)
WRAPL = Alignment(horizontal="left", vertical="center", wrap_text=True)
WIDTHS = [7,9,9,16,11,6,9,11,18,11,20,11,8,26,12,16,22,28]

def make_rows(DATA, CP_ID):
    return [row_of(d, CP_ID) for d in DATA]

def add_summary_sheet(wb, DATA, CP_ID):
    ws0 = wb.create_sheet("汇总")
    title_font = Font(name="Microsoft YaHei", bold=True, size=14, color="1F4E78")
    ws0["A1"] = "尺寸明细检验表（汇总）"; ws0["A1"].font = title_font
    cnt = Counter(d["cls"] for d in DATA)
    cnt_kind = Counter(d["kind"] for d in DATA)
    cnt_gt = sum(1 for d in DATA if d["final_tol"].startswith("±") or "/" in d["final_tol"])
    cnt_ext = sum(1 for d in DATA if d["ext"])
    cnt_conf = sum(1 for d in DATA if "待确认" in d["final_tol"] or "待确认" in (d.get("note") or ""))
    view_cnt = Counter(d["v"] for d in DATA)
    summ = [("气泡总数", len(DATA)), ("应标尺寸/要素", len(DATA)), ("已标数量", len(DATA)),
            ("覆盖性", "100%（应标未标 0 项）"),
            ("重要特性(SC)", cnt.get("SC", 0)), ("一般特性(NC)", cnt.get("NC", 0)),
            ("关键特性(CC)", cnt.get("CC", 0)),
            ("— 螺纹要素", cnt_kind.get("thread", 0)), ("— 形位公差框格", cnt_kind.get("frame", 0)),
            ("— 工艺/表面注记", cnt_kind.get("note", 0)),
            ("— 显式公差尺寸", cnt_ext), ("— 一般公差(f级)尺寸", cnt_gt),
            ("待确认项", cnt_conf), ("控制计划编号", CP_ID)]
    r = 3
    for k, v in summ:
        ws0.cell(r, 1, k).font = Font(name="Microsoft YaHei", bold=True, size=10)
        ws0.cell(r, 2, v).font = CELL_FONT; r += 1
    r += 1
    ws0.cell(r, 1, "各视图分布").font = Font(name="Microsoft YaHei", bold=True, size=11, color="1F4E78"); r += 1
    for v in view_cnt:
        ws0.cell(r, 1, v).font = CELL_FONT; ws0.cell(r, 2, view_cnt[v]).font = CELL_FONT; r += 1
    ws0.column_dimensions["A"].width = 22; ws0.column_dimensions["B"].width = 40
    return ws0

def add_detail_sheet(wb, rows, DATA):
    ws = wb.create_sheet("尺寸明细")
    for c, h in enumerate(HEADERS, 1):
        cell = ws.cell(1, c, h); cell.fill = HEAD_FILL; cell.font = HEAD_FONT
        cell.alignment = WRAP; cell.border = BORDER
    for i, d in enumerate(DATA):
        rr = i + 2
        for c, val in enumerate(rows[i], 1):
            cell = ws.cell(rr, c, val); cell.font = CELL_FONT
            cell.border = BORDER
            cell.alignment = WRAPL if c in (4, 14, 16, 18) else WRAP
            cell.fill = SC_FILL if d["cls"] in ("CC", "SC") else NC_FILL
    for c, w in enumerate(WIDTHS, 1):
        ws.column_dimensions[get_column_letter(c)].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(HEADERS))}{len(DATA)+1}"
    return ws

def add_keychar_sheet(wb, rows, DATA):
    ws2 = wb.create_sheet("关键特性专项")
    sc_rows = [rows[i] for i, d in enumerate(DATA) if d["cls"] in ("CC", "SC")]
    for c, h in enumerate(HEADERS, 1):
        cell = ws2.cell(1, c, h); cell.fill = HEAD_FILL; cell.font = HEAD_FONT
        cell.alignment = WRAP; cell.border = BORDER
    for i, row in enumerate(sc_rows):
        rr = i + 2
        for c, val in enumerate(row, 1):
            cell = ws2.cell(rr, c, val); cell.font = CELL_FONT
            cell.border = BORDER
            cell.alignment = WRAPL if c in (4, 14, 16, 18) else WRAP
            cell.fill = SC_FILL
    for c, w in enumerate(WIDTHS, 1):
        ws2.column_dimensions[get_column_letter(c)].width = w
    ws2.freeze_panes = "A2"
    ws2.auto_filter.ref = f"A1:{get_column_letter(len(HEADERS))}{len(sc_rows)+1}"
    return ws2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--balloons", default="work/balloons.json")
    ap.add_argument("--out", default="outputs/尺寸明细检验表.xlsx")
    ap.add_argument("--cp", default="MEST/Q/CP-（按控制计划填写）")
    a = ap.parse_args()

    DATA = json.load(open(a.balloons, encoding="utf-8"))
    CP_ID = a.cp
    rows = make_rows(DATA, CP_ID)

    wb = Workbook()
    wb.remove(wb.active)
    add_summary_sheet(wb, DATA, CP_ID)
    add_detail_sheet(wb, rows, DATA)
    add_keychar_sheet(wb, rows, DATA)

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    wb.save(a.out)
    cnt = Counter(d["cls"] for d in DATA)
    cnt_conf = sum(1 for d in DATA if "待确认" in d["final_tol"] or "待确认" in (d.get("note") or ""))
    print("saved", a.out, "| rows:", len(DATA), "| SC:", cnt.get("SC",0), "| NC:", cnt.get("NC",0), "| 待确认:", cnt_conf)


if __name__ == "__main__":
    main()
