---
name: power-trading-96-to-24
description: Convert 电力交易/电网边界条件 96点数据 into 24点小时数据 by averaging each consecutive 4 quarter-hour rows. Use when the user asks to do 96转24、96点转24点、15分钟转小时、日前96点边界条件汇总、检查96点模板公式、修复24点表引用列，尤其是 Excel/xlsx 场景。
---

# Power Trading 96 To 24

Convert 96-point electricity-trading data to 24-point hourly data with the fixed rule: **every 4 consecutive 15-minute points become 1 hourly point by arithmetic mean**.

## Workflow

1. Identify the 96-point source sheet.
2. Confirm there are 96 non-empty data rows.
3. Build the 24-point result by averaging rows `1-4`, `5-8`, ..., `93-96` for each metric column.
4. If writing into a template, ensure each 24-point metric column references the matching 96-point source column.
5. Verify at least the first 3 hours manually.

## Column Mapping Rule

Typical columns:

- 时刻
- 统调负荷
- 省间联络线
- 总出力
- 非现货机组出力
- 新能源
- 水电
- 抽蓄

For hour `n` in the 24-point table, average source rows `((n-1)*4+1)` to `(n*4)`.

Example:

- 24点第1小时 ← 96点第1~4行平均
- 24点第2小时 ← 96点第5~8行平均
- 24点第24小时 ← 96点第93~96行平均

## Formula Pattern

When the source sheet is named `source96`, use this pattern in the 24-point formula sheet:

```excel
=SUM(OFFSET(source96!$B$2,(ROW()-2)*4,0,4,1))/4
```

Change the column letter only. Do not change the matching logic.

## Critical Checks

- Keep **same-column mapping**. `水电` must reference the 96-point `水电` column, not another metric.
- Do not call a column "correct" only because the formula shape looks valid; verify the referenced source column.
- If a 24-point column seems missing, check whether its width was shrunk to near zero instead of being deleted.
- Formula sheets may look blank in readers that do not recalc Excel caches. Check the numeric result sheet for actual values.

## Quick Commands

Create a new workbook with `source96`, `result24`, and `formula24`:

```bash
python scripts/convert_96_to_24.py input.xlsx output.xlsx
```

Specify the source sheet explicitly when auto-detection is ambiguous:

```bash
python scripts/convert_96_to_24.py input.xlsx output.xlsx --source-sheet "日前96点边界条件数据"
```

## Template Fix Guidance

If the user asks to repair an existing template:

- Edit the existing file minimally.
- Change only the wrong `<f>` formula nodes or the target column width.
- Preserve the rest of the workbook.
- Re-validate formulas after packing.

A common correct `水电` formula is:

```excel
=SUM(OFFSET(日前96点边界条件数据!$H$2,(ROW()-2)*4,0,4,1))/4
```

## Output Expectation

Prefer delivering:

1. A source 96-point sheet
2. A computed 24-point value sheet
3. A formula-based 24-point sheet for auditability

If the user instead wants an existing template updated in place, modify that template rather than creating a separate workbook.
