---
name: meeting-minutes-task-extractor
description: Free basic version that extracts actionable tasks from meeting minutes. Reserves premium upgrade hooks for deeper action decomposition and project tracker export.
---

# Meeting Minutes → Task Extractor

## Value

- Free tier: extract up to 5 actionable tasks with assignee/due-date hints.
- Premium tier (reserved): extract up to 20 tasks, milestone decomposition, and tracker export.

## Input

- `user_id`
- `meeting_title`
- `meeting_notes`
- optional `tier` (`free`/`premium`)

## Run

```bash
python3 scripts/meeting_minutes_task_extractor.py \
  --user-id user_002 \
  --meeting-title "增长周会" \
  --meeting-notes "由小王负责落地页改版，截止2026-03-08"
```

## Tests

```bash
python3 -m unittest scripts/test_meeting_minutes_task_extractor.py -v
```
