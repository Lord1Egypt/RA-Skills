---
name: glancely-mood
description: Hourly mood check-ins via chat. Log raw feelings with optional score.
---
## Usage

```bash
glancely mood log --raw "feeling great today" --score 8
glancely mood stats
```

## Scripts

**scripts/log.py**
```
--raw TEXT          Required. How you're feeling right now.
--score INT         Optional 1-10. Higher = better mood.
--at TIMESTAMP      Optional. ISO timestamp. Default: now.
```

**scripts/stats.py** — returns JSON for dashboard panel.

## Fields

- `raw` (TEXT) — free-form mood description
- `score` (INTEGER) — 1-10 scale
- `logged_at` (TIMESTAMP) — when logged

## Cron

Schedule: `0 8-23 * * *` — hourly from 8am to 11pm.
Notification: "How are you feeling right now?"
