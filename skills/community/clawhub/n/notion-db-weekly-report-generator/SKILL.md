---
name: notion-db-weekly-report-generator
description: Free basic version that converts Notion-style task records into weekly report markdown. Reserves premium upgrade hooks for trend analysis and management summary automation.
---

# Notion 数据库 → 周报生成器

## Value

- Free tier: generate weekly report markdown from task records.
- Premium tier (reserved): trend charting, cross-week comparison, auto executive summary.

## Input

- `user_id`
- `week_label`
- `records` (array)
- optional `tier` (`free`/`premium`)

## Run

```bash
python3 scripts/notion_db_weekly_report_generator.py \
  --user-id user_005 \
  --week-label "2026-W10" \
  --records-json '[{"title":"落地页改版","owner":"小王","status":"进行中","progress":70}]'
```

## Tests

```bash
python3 -m unittest scripts/test_notion_db_weekly_report_generator.py -v
```
