---
name: ledger-monthly-report
description: Generate monthly ledger statistics in CNY with amount and ratio by tag/category, top expense breakdown, and labeled charts. Use when user asks to统计收支, 看占比, 画图表, or requests monthly summary visuals.
---

# Ledger Monthly Report

Use this skill for monthly financial summaries and charts.

## Required rules

1. Always convert/aggregate using `amount_cny` (RMB baseline).
2. Report must include:
   - expense by tag: amount + ratio
   - expense by major category: amount + ratio
   - top expense heads
   - income/expense totals and ratio
3. Charts must include:
   - tag bar chart
   - tag pie chart
   - major-category chart
   - income/expense ratio chart
4. All charts must display numeric amount labels.
5. Send charts to user, then delete local chart files if requested.
6. Generated chart files must stay ignored by git (`reports/*.png` already ignored).

## Command

**IMPORTANT: Get current date on entry to determine the default month.**

```bash
# Get current year-month in Asia/Taipei timezone
CURRENT_MONTH=$(TZ='Asia/Taipei' date +%Y-%m)
```

If user does not specify a month, use `$CURRENT_MONTH` as default.

Use project script (all paths relative to workspace root):

```bash
. projects/.venv-chart/bin/activate
python projects/scripts/monthly_report_cny.py \
  --data-root projects/data \
  --month "$CURRENT_MONTH" \
  --out-dir projects/reports
```

Outputs (under `projects/reports/`):

- `projects/reports/<YYYY-MM>_summary_cny.json`
- `projects/reports/<YYYY-MM>_expense_by_tag_cny.png`
- `projects/reports/<YYYY-MM>_expense_by_tag_pie_cny.png`
- `projects/reports/<YYYY-MM>_expense_by_major_cny.png`
- `projects/reports/<YYYY-MM>_income_expense_ratio_cny.png`

## Reply template

- 总收入（CNY）
- 总支出（CNY）
- 净额（CNY）
- 按标签支出（金额+占比）
- 按大类支出（金额+占比）
- 大头支出 Top N
- 收支占比（收入 vs 支出）

Then send charts.

## Cleanup

If user says charts can be removed after sending:

- delete the generated `reports/*.png` files for that month.
- keep summary json unless user asks to remove it too.
