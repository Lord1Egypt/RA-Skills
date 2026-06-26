---
name: glancely-mit
description: Most Important Task tracker. Set one MIT per day, check in nightly.
---
## Usage

```bash
glancely mit set --date 2026-05-06 --task "ship v0.2" --completed false
glancely mit today
glancely mit stats
```

## Scripts

**scripts/log.py**
```
--upsert           Create or update today's MIT
--date DATE        Date (YYYY-MM-DD)
--task TEXT        Required. The one task.
--completed BOOL   true or false
```

**scripts/today_brief.py** — returns today's MIT as JSON.

**scripts/stats.py** — returns JSON for dashboard panel.

## Fields

- `task` (TEXT) — the MIT description
- `date` (DATE)
- `completed` (INTEGER) — 0 or 1
- `logged_at` (TIMESTAMP)

## Cron

Schedule: `0 23 * * *` — 11pm nightly.
Notification: "What was your Most Important Task today?"
