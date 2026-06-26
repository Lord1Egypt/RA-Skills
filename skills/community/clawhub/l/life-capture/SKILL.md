---
name: life-capture
description: capture daily-life notes into markdown and sqlite. use when the user wants to record one or more life entries such as expenses, completed tasks, schedules, reminders, or ideas; classify the content; generate tags; parse natural language into structured json; write a daily markdown note under life/daily; and sync structured fields into a local sqlite database. triggers include short single-line entries, mixed sentences containing multiple record types, or requests to log and organize personal information for later review and reporting.
---

# life-capture

Turn natural-language life logs into durable records. This skill classifies each input item, generates tags, creates user-visible markdown, writes to a daily note under `life/daily`, and syncs structured data into `life/db/life.db`.

## Default storage layout

Use these paths unless the user explicitly overrides them:

```text
life/
  daily/
  ideas/
  db/life.db
```

Create missing directories as needed. Never delete existing content. Append or update only.

## Supported record types

Map every parsed item to exactly one primary type:

- `expense`: spending, bills, purchases, subscriptions, refunds
- `task`: completed tasks, ongoing work, todos, chores, habits
- `schedule`: calendar items, appointments, time blocks, plans
- `idea`: ideas, inspiration, possible projects, reflections worth saving

When a sentence contains multiple items, split it into multiple records.

## Output contract

For each user request:

1. Parse the message into one or more records.
2. Generate a stable `id` for each record using the pattern:
   - `exp_YYYYMMDD_NNN`
   - `task_YYYYMMDD_NNN`
   - `sched_YYYYMMDD_NNN`
   - `idea_YYYYMMDD_NNN`
3. Generate 1 to 4 short tags.
4. Show the user the organized result in markdown.
5. Save the records by running `scripts/process_entry.py`.

Always keep the original user wording in `raw_text`. Never invent missing fields. Leave unknown fields null.

## User-visible response format

Because this skill is configured for visible output, show a concise but complete result after writing:

```md
## 已整理记录

### 1) <type label>
- ID: <id>
- 标签: #a #b
- 归档: <daily markdown path>
- 数据库: <written/skipped>

#### Markdown
<the markdown block written for this item>

#### JSON
```json
<the parsed record json>
```
```

If there are multiple records, repeat the block for each one.

## Parsing rules

Use `scripts/parse_entries.py` for natural-language parsing. The parser now reads configurable rules from `references/parser_config.json`, so prefer editing that file instead of changing Python when you need new categories, tags, or keyword mappings.

### Expense

Extract when present:
- `amount`
- `currency` (default `CNY` only when the currency symbol or language implies RMB; otherwise null)
- `category`
- `subcategory`
- `merchant`
- `pay_method`

Default top-level tags often include `开销` plus one semantic tag such as `餐饮` or `交通`.

Preferred categories:
- 饮食
- 交通
- 购物
- 居家
- 社交
- 娱乐
- 医疗
- 学习
- 其他

### Task

Extract when present:
- `status` (`todo`, `doing`, `done`, `cancelled`)
- `priority` (`low`, `normal`, `high`)
- `project`
- `due_date`
- `completed_at`

If the user says they already did something, default status to `done`.

### Schedule

Extract when present:
- `schedule_date`
- `start_time`
- `end_time`
- `location`
- `status` (`planned`, `done`, `skipped`)

If the user uses relative dates, resolve them from the current conversation date. Prefer passing `--today YYYY-MM-DD` to `scripts/process_entry.py` or `scripts/parse_entries.py` so relative dates like `明天` are stable across environments.

### Idea

Extract when present:
- `idea_type`
- `status` (`captured`, `reviewing`, `used`, `archived`)
- `related_task_id`

Default status to `captured`.


## Configurable parsing rules

Before editing Python, check whether the change can be made in `references/parser_config.json`.

You can change:
- category and subcategory mappings for expenses
- task project mappings
- idea type mappings
- schedule extra tag mappings
- default tags by record type
- hint regexes used in type inference

To test a modified config without changing the bundled default file:

```bash
python scripts/parse_entries.py --config /path/to/custom_config.json --text "买咖啡 18 元，明天下午两点去体检"
```

## Markdown writing rules

Write each record into the daily note for its effective date under one of these sections:
- `## 开销`
- `## 任务`
- `## 日程`
- `## 灵感`

Use this block structure:

```md
### <id>
- 时间：<time or empty>
- 标签：#tag1 #tag2
- 原始描述：<raw_text>
- 摘要：<summary>
```

Then add type-specific fields:

- Expense: 金额 / 币种 / 分类 / 子分类 / 商家 / 支付方式
- Task: 状态 / 优先级 / 项目 / 截止日期 / 完成时间
- Schedule: 日期 / 开始时间 / 结束时间 / 地点 / 状态
- Idea: 类型 / 状态 / 关联任务

## Execution workflow

### End-to-end one-command flow

Use this when the user provides natural language and wants the records saved immediately:

```bash
python scripts/process_entry.py --root life --db life/db/life.db --today 2026-03-10 --text "今天中午牛肉面 26 元，下午整理了书桌，想到可以做一个生活数据看板"
```

The wrapper script will:
1. initialize the database if missing
2. parse text into `{"records": [...]}` with `scripts/parse_entries.py`
3. save markdown and sqlite rows with `scripts/save_entry.py`
4. print parsed records plus save results as json

### Split-step flow

Use this when the user asks to inspect or verify the structured output before writing:

```bash
python scripts/parse_entries.py --text "明天下午两点去体检，买咖啡 18 元"
```

Then save:

```bash
python scripts/save_entry.py --root life --db life/db/life.db --stdin-json
```

### Database init only

Use this once before first write if `life/db/life.db` does not exist and you are not using `process_entry.py`:

```bash
python scripts/init_db.py --db life/db/life.db
```

## Database sync rules

The database design is:
- `entries`
- `expenses`
- `tasks`
- `schedules`
- `ideas`
- `tags`
- `entry_tags`

See `references/schema.md` for the schema, `references/examples.md` for sample payloads and commands, and `references/configuration.md` plus `references/parser_config.json` for configurable parsing rules.

## Failure handling

- If markdown write succeeds but database sync fails, say so clearly.
- Do not silently drop a record.
- If parsing is ambiguous, make the narrowest safe interpretation and preserve the original text.
- If a record is missing a critical type-specific field, still save the record with null fields rather than discarding it.
