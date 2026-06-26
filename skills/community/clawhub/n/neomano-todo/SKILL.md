---
name: neomano-todo
description: Enhanced TODO/task manager backed by a local SQLite database (instead of flat text files) with priorities (1-3), tags, due dates, reminder timestamps, explicit task lifecycle statuses (open/done/blocked/expired/forgotten), and stale-task detection to prevent backlog accumulation. Use when the user wants to add, list, filter, prioritize, update, complete, expire/forget, or review stale tasks; or when they want reminder scheduling metadata to be stored for OpenClaw cron delivery.
---

# neomano-todo

An improved personal TODO system that uses **SQLite as the backend** (not text files).

Why SQLite:
- Structured fields (priority/status/dates/tags)
- Fast filtering and sorting
- Durable local storage with zero external dependencies

## Features

- **SQLite persistence** (local file)
- **Priorities 1–3**
  - 1 = high, 2 = medium, 3 = low
- **Tags** (many-to-many)
- **Dates**
  - `due_at` (when it should be done)
  - `remind_at` (when to notify)
- **Statuses**
  - `open`, `done`, `blocked`, `expired`, `forgotten`
- **Reminder metadata for OpenClaw cron**
  - Store `remind_at` + `cron_job_id` so reminders can be created/updated/cancelled by the agent
- **Backlog control**
  - Detect “stale candidates” based on `last_touched_at` and priority thresholds

## Configuration (environment variables)

Recommended: set in `~/.openclaw/.env` on the gateway machine.

### Storage

- `NEOMANO_TODO_DB_PATH`
  - Path to the SQLite DB file.
  - Default used by the helper script: `~/.openclaw/workspace/data/neomano-todo.sqlite3`

### Reminder delivery defaults

Used by the agent when scheduling a reminder (cron delivery).

- `NEOMANO_TODO_DEFAULT_CHANNEL`
  - Example: `whatsapp`, `telegram`, etc.
- `NEOMANO_TODO_DEFAULT_TARGET`
  - Example: `+593987233203` for WhatsApp.
- `NEOMANO_TODO_TZ`
  - Example: `America/Guayaquil`

## Data model (SQLite)

The helper script auto-creates tables on first run.

Main fields stored per task:
- `title`, `notes`
- `priority` (1–3)
- `status` (`open|done|blocked|expired|forgotten`)
- `created_at`, `updated_at`, `last_touched_at`, `completed_at`
- `due_at`, `remind_at`
- `cron_job_id` (optional, set after creating a cron job)
- tags via `tags` + `task_tags`

## Helper script

Use the bundled deterministic helper script:

- `skills/neomano-todo/scripts/todo.py`

It outputs JSON to make it easy for an agent to parse.

### Commands

Add a task:

```bash
python3 skills/neomano-todo/scripts/todo.py add "Install Starlink antenna" --priority 2 --tags "starlink,truck" --notes "This weekend"
```

Get a task:

```bash
python3 skills/neomano-todo/scripts/todo.py get 12
```

List tasks:

```bash
python3 skills/neomano-todo/scripts/todo.py list --status open --order priority
python3 skills/neomano-todo/scripts/todo.py list --status open --order due
python3 skills/neomano-todo/scripts/todo.py list --tag sales --order priority
```

Complete / reopen:

```bash
python3 skills/neomano-todo/scripts/todo.py done 12
python3 skills/neomano-todo/scripts/todo.py reopen 12
```

Change status (blocked/expired/forgotten/etc):

```bash
python3 skills/neomano-todo/scripts/todo.py set-status 12 blocked
python3 skills/neomano-todo/scripts/todo.py set-status 12 forgotten
```

Change priority:

```bash
python3 skills/neomano-todo/scripts/todo.py set-priority 12 1
```

Update tags:

```bash
python3 skills/neomano-todo/scripts/todo.py set-tags 12 "sales,followup"
```

Update due/reminder timestamps:

```bash
python3 skills/neomano-todo/scripts/todo.py set-dates 12 --due-at "2026-03-29T09:00:00-05:00" --remind-at "2026-03-29T08:30:00-05:00"
```

Store cron job id (after scheduling a reminder with OpenClaw cron):

```bash
python3 skills/neomano-todo/scripts/todo.py set-cron-job 12 <cron_job_id>
```

Delete:

```bash
python3 skills/neomano-todo/scripts/todo.py delete 12
```

## Reminder scheduling (OpenClaw cron)

The script stores reminder timestamps; the agent is responsible for scheduling.

Workflow:
1) If `remind_at` is set and `status` is `open`, create/update a cron job scheduled at `remind_at`.
2) After creating the cron job, store its id in the task using `set-cron-job`.
3) When the task becomes terminal (`done`, `expired`, `forgotten`), cancel the cron job (if any).

## Backlog control: stale candidates

Policy:
- P3 not touched for 30 days → review candidate
- P2 not touched for 45 days → review candidate
- P1 is never auto-forgotten

List stale candidates:

```bash
python3 skills/neomano-todo/scripts/todo.py stale-candidates
```

## Response style

- Keep replies short.
- For WhatsApp: use bullets (no tables).
- When confirming changes: include task id, title, priority, and status.
