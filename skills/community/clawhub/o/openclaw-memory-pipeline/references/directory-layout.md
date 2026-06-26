# Directory layout

Recommended layout:

```text
MEMORY.md
memory/
├── inbox.md
├── YYYY-MM-DD-raw.md
├── YYYY-MM-DD.md
├── projects/
├── system/
├── groups/
└── logs/
```

## Root file

### `MEMORY.md`
Use for long-term curated memory only.

Store:
- stable user preferences
- durable workflow rules
- long-running projects
- important decisions worth carrying across weeks or months

Do not use it for:
- full daily logs
- hourly archives
- temporary task noise

## `memory/`
Use this directory for process memory and intermediate notes.

### `memory/inbox.md`
Use as the capture buffer.

Recommended template:

```md
# inbox

> New facts, preferences, decisions, todos, and project state go here first.
> The hourly cron job compresses pending items into `memory/YYYY-MM-DD-raw.md`.

## pending
```

### `memory/YYYY-MM-DD-raw.md`
Use for day-level raw archive output.

- organize by hour
- append or merge under sections like `## 2026-03-19 22:00 Asia/Macau`
- keep concise factual bullets

### `memory/YYYY-MM-DD.md`
Use for the daily summary.

- keep it short
- write only the most important 1–2 items from that day

### `memory/projects/`
Use for long-lived project-specific notes.

Use when the information is easier to understand by project than by date.

### `memory/system/`
Use for durable operating rules and environment conventions.

Examples:
- browser defaults
- message formatting preferences
- agent workflow rules
- memory pipeline conventions

### `memory/groups/`
Use for group-specific context that should not be merged into general personal memory.

### `memory/logs/`
Optional holding area for diagnostic logs, validation outputs, or future extensions.
