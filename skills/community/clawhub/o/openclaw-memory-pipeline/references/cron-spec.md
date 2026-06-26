# Cron spec

This skill expects a three-job pipeline.

## Recommended job set

### 1. Hourly archive job

Suggested name:
- `context: compress chat history (hourly)`

Recommended schedule:

- cron expression: `0 * * * *`
- timezone: `Asia/Macau`
- optional small stagger is acceptable

### Required behavior

- read `memory/inbox.md`
- inspect only `## pending`
- if pending is empty, exit successfully without noise
- create `memory/YYYY-MM-DD-raw.md` if missing
- create the current hour section if missing
- merge into the current hour section if it already exists
- deduplicate before writing
- clear or mark processed items in pending after successful archive
- never send a user-visible message

### Prompt design notes

The prompt should explicitly require:

- creating the target raw file if missing
- merging same-hour sections instead of duplicating them
- deleting or clearing only items that were actually archived
- silent success when there is nothing to process

## 2. Daily summary job

Suggested name:
- `daily-memory-diary`

Recommended schedule:

- cron expression: `30 23 * * *`
- timezone: `Asia/Macau`

### Required behavior

- write `memory/YYYY-MM-DD.md`
- select only 1–2 most important items from the day
- keep entries concrete and short
- never send a user-visible message

### Prompt design notes

The prompt should explicitly require:

- concise writing
- concrete facts instead of generic summaries
- skipping filler if the day had little value to preserve

## 3. Weekly long-term review job

Suggested name:
- `weekly-memory-review`

Recommended schedule:

- cron expression: `30 23 * * 0`
- timezone: `Asia/Macau`

### Required behavior

- review recent `memory/YYYY-MM-DD.md` files
- update `MEMORY.md` with only durable information
- avoid promoting one-off noise into long-term memory
- never send a user-visible message

### Prompt design notes

The prompt should explicitly require:

- extracting only stable preferences, rules, or project context
- avoiding short-lived chatter and ephemeral tasks
- preserving existing useful content in `MEMORY.md`

## Installation sequence

Install in this order:

1. hourly archive
2. manual acceptance test for hourly archive
3. daily summary
4. weekly long-term review

This order matters because the daily and weekly jobs are downstream consumers of the hourly output.

## Guardrails

For all three jobs:

- prefer resilient file creation over brittle exact-edit assumptions
- preserve existing content when adding new content
- avoid duplicate sections for the same hour/day concept
- keep output factual and compact
- treat silent success as the default
- avoid any message/reaction side effects in cron runs unless explicitly requested by the user
