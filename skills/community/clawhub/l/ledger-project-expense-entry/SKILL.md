---
name: ledger-project-expense-entry
description: Record natural-language project expense messages into ledger JSONL. Use when user sends "项目+支出" directly (e.g., "OpenClaw 服务器 89"), wants quick记账, or asks to append project spending. Default to expense and CNY unless user explicitly says otherwise.
---

# Ledger Project Expense Entry

Use this skill for fast bookkeeping from short natural-language messages.

## Defaults

- `direction`: default `支出`
- `currency`: default `CNY`
- `date`: default today (Asia/Taipei)

Only change defaults if user explicitly provides different values.

## Parse target

Extract from message:

- `project` (项目名)
- `description` (消费内容)
- `amount` (number)
- optional `date`
- optional `currency`
- optional `direction` (`收入`/`支出`)
- optional `tags`

If project and description are both present, build description as:

- `<project> - <description>`

If only one exists, use that field directly.

If amount is missing, ask one short clarification question.

## Write command

**IMPORTANT: Get today's date (YYYY-MM-DD) first, for determining which month file to write to.**

```bash
# Get today's date in Asia/Taipei timezone
CURRENT_DATE=$(TZ='Asia/Taipei' date +%Y-%m-%d)
```

Then append via existing script:

```bash
python3 projects/scripts/add_ledger_entry.py \
  --data-root projects/data \
  --date "$CURRENT_DATE" \
  --direction <支出|收入> \
  --amount <number> \
  --currency <CNY|USD|JPY|...> \
  --description <project-description> \
  --tags <tag1,tag2,...> \
  --source manual \
  --batch manual
```

## Category catalog (must check before writing)

Before each write, check:

- `projects/docs/CATEGORY_CATALOG.md`

Selection policy:

- Prefer existing values from catalog (`tags`/`major_category`/`type`/`currency`).
- If user gives a new tag not in catalog and meaning is clear, write it; otherwise ask one short confirmation.
- If uncertain, keep optional fields empty rather than inventing noisy labels.

## Tag suggestion rules

- If user gives tags, use them directly.
- If user does not give tags:
  - project/infra/subscription/domain/server -> `开发成本` / `服务器` / `域名` / `通讯网络` (pick the closest one)
  - meal/drink -> `外卖` / `下馆子` / `饮料零食`
  - ride/transport -> `打车` / `交通卡` / `火车` / `飞机`
- If still uncertain, keep tags empty.

## Response format

After appending, reply with:

- month file path
- one-line summary: `日期 | 流向 | 金额币种 | 描述`
