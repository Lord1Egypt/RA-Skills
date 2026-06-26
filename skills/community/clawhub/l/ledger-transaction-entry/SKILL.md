---
name: ledger-transaction-entry
description: Convert natural-language spending/income statements into ledger JSONL records and append them into projects/data/YYYY/YYYY-MM.jsonl. Use when the user describes a transaction (expense/income), asks to记账,补账, or wants to append a new entry in the ledger project.
---

# Ledger Transaction Entry

Use this skill to append new transactions into `projects/data`.

## Required output target

- Data root: `projects/data`
- File rule: `YYYY/YYYY-MM.jsonl`
- New record must be appended to the end of the month file.

## Parse rules

From user text, extract:

- `direction`: `支出` or `收入`
- `amount`: number
- `currency`: default `CNY` if omitted
- `date`: default today (Asia/Taipei) if omitted
- `description`: short clean text
- `tag`: 单个分类标签（只能选一个）

Optional fields (only if provided clearly):

- `id`
- `major_category`
- `type`

If amount or direction is ambiguous, ask one short clarification question before writing.

## Write command

**IMPORTANT: Get today's date (YYYY-MM-DD) for determining which month file to write to.**

```bash
# Get today's date in Asia/Taipei timezone
CURRENT_DATE=$(TZ='Asia/Taipei' date +%Y-%m-%d)
```

The script will automatically add `created_at` field with current timestamp (YYYY-MM-DD HH:MM:SS) to each record.

Then run:

```bash
python3 projects/scripts/add_ledger_entry.py \
  --data-root projects/data \
  --date "$CURRENT_DATE" \
  --direction <支出|收入> \
  --amount <number> \
  --currency <CNY|USD|JPY|...> \
  --description <text> \
  --tag <tag>
```

Add optional args only when available:

- `--id`
- `--major-category`
- `--type`
- `--source manual`
- `--batch manual`

## Category catalog (must check before writing)

Before each write, check:

- `projects/docs/CATEGORY_CATALOG.md`

Selection policy:

- Prefer existing values from catalog (`tag`/`major_category`/`type`/`currency`).
- If user gives a new tag not in catalog and meaning is clear, write it; otherwise ask one short confirmation.
- 只能选一个分类，不要给多个。

## Existing common tags (只选一个)

当用户没有指定分类时，根据意图选择最合适的一个：

- 吃喝：`外卖` / `下馆子` / `饮料零食` / `买菜做饭`
- 出行：`打车` / `交通卡` / `火车` / `飞机` / `大巴`
- 居家：`生活好物` / `居家杂物` / `房租住宿`
- 订阅与网络：`通讯网络` / `服务器` / `域名`
- 投资与收入：`A股` / `美股` / `港股` / `项目营收` / `二手`

When uncertain, leave tags empty instead of guessing aggressively.

## Response after write

Confirm with:

- month file path
- appended summary (date, direction, amount, description)

## Monthly summary + chart workflow

Use this when user asks things like:

- `统计已知月份的总金额`
- `生成图表发我`
- `图表都 ignore，发完可以删`

Required behavior:

1. Read all month files under `projects/data/YYYY/YYYY-MM.jsonl`.
2. Aggregate by month:
   - total amount (absolute sum)
   - expense sum (`direction=支出`)
   - income sum (`direction=收入`)
   - net (`income-expense`)
3. Generate chart into `projects/reports/` (PNG preferred).
4. Ensure generated charts are git-ignored (keep/report patterns in `.gitignore`).
5. Send chart to user.
6. If user asks to delete after sending, delete local generated chart files.

Important note in reply:

- If source data includes multiple currencies, state that monthly totals are mixed-currency trend values unless converted to one base currency.
