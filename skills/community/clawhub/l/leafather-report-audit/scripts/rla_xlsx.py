#!/usr/bin/env python3
"""rla_xlsx.py — 由账本生成两份 Excel 台账（随报告交付）。

内部版：全字段（id / 稳定身份 / 值 / 单位 / 口径 / 是否出现在报告）
客户版：只给"能看懂"的（指标名 / 值 / 单位 / 白话口径），客户指着任何数字都能查

用法：
    python3 scripts/rla_xlsx.py --ledger ledger.json [--out-dir .] [--used id1,id2,...]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
except ImportError:
    raise SystemExit("❌ 缺 openpyxl（pip install openpyxl）")

HDR_FILL = PatternFill("solid", fgColor="1F4E78")
HDR_FONT = Font(color="FFFFFF", bold=True)


def _fmt(v):
    if isinstance(v, (int, float)):
        return round(v, 4) if isinstance(v, float) else v
    return v


def _sheet(wb, title, headers, rows, widths):
    ws = wb.create_sheet(title)
    ws.append(headers)
    for c in ws[1]:
        c.fill = HDR_FILL
        c.font = HDR_FONT
        c.alignment = Alignment(vertical="center")
    for r in rows:
        ws.append(r)
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    ws.freeze_panes = "A2"
    return ws


def main() -> int:
    ap = argparse.ArgumentParser(description="账本 → Excel 台账")
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--used", default="", help="报告中实际引用的账本 id，逗号分隔（客户版只列这些）")
    args = ap.parse_args()

    lp = Path(args.ledger)
    if not lp.exists():
        print(f"❌ 未就绪：账本不存在 {lp}", file=sys.stderr)
        return 2
    led = json.loads(lp.read_text(encoding="utf-8-sig"))
    nums = led.get("numbers") or []
    if not nums:
        print("❌ 未就绪：账本是空的（0 条），不生成台账", file=sys.stderr)
        return 2

    used = {x.strip() for x in args.used.split(",") if x.strip()}
    out_dir = Path(args.out_dir) if args.out_dir else lp.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    # ---- 内部版：全字段 ----
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    rows = []
    for n in nums:
        rows.append([
            n.get("id"), n.get("metric_id") or "—", n.get("label"),
            _fmt(n.get("value")), n.get("unit") or "", n.get("caliber") or "",
            "是" if n.get("id") in used else ("未标注" if not used else "否"),
            "是" if n.get("verifiable", True) else "否",
            n.get("data_as_of") or led.get("report", {}).get("data_as_of") or "",
        ])
    _sheet(wb, "内部台账",
           ["账本ID", "稳定身份", "指标名", "值", "单位", "口径", "报告引用", "可复算", "数据截止"],
           rows, [10, 18, 20, 16, 8, 46, 10, 9, 12])

    # ---- 客户版：只给看得懂的，且只列被引用的 ----
    show = [n for n in nums if (n.get("id") in used) or (not used)]
    if used:
        show = [n for n in nums if n.get("id") in used]
    crows = []
    for n in show:
        if not n.get("metric_id"):
            continue                      # 客户版只列有稳定身份的正式指标
        crows.append([n.get("label"), _fmt(n.get("value")), n.get("unit") or "",
                      n.get("caliber") or "", led.get("report", {}).get("data_as_of", "")])
    if crows:
        _sheet(wb, "客户版", ["指标", "值", "单位", "说明", "数据截止"],
               crows, [22, 18, 8, 50, 12])

    # ---- 说明页 ----
    ws = wb.create_sheet("说明")
    for line in [
        ["报告名称", led.get("report", {}).get("name", "")],
        ["数据截止", led.get("report", {}).get("data_as_of", "")],
        ["生成时间", led.get("report", {}).get("generated_at", "")],
        ["账本条目", len(nums)],
        ["其中正式指标", sum(1 for n in nums if n.get("metric_id"))],
        ["", ""],
        ["怎么用", "客户指着报告里任何一个数字 → 在「客户版」按指标名找到它 → 看到值/单位/口径/数据截止"],
        ["内部核对", "在「内部台账」按账本ID或稳定身份反查，可回到原始 SQL"],
    ]:
        ws.append(line)
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 70

    tag = lp.stem.replace("ledger", "").strip("-_") or ""
    p1 = out_dir / (f"附件00-数字台账-内部-{tag}.xlsx" if tag else "附件00-数字台账-内部.xlsx")
    wb.save(p1)
    print(f"✅ {p1}（内部台账 {len(rows)} 行）")
    if crows:
        print(f"   客户版页签 {len(crows)} 条正式指标")
    else:
        print("   ⚠️ 没有认领过 metric_id 的条目，客户版页签为空 "
              "（先给项目写 metrics.yaml，或看内部台账）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
