---
name: glancely-diary
description: Time-tracked activity logging to Google Calendar. English + Chinese time parsing.
---
## Auth

Requires Google OAuth. User must:
1. Create OAuth Desktop client at console.cloud.google.com
2. Download credentials JSON to `~/.glancely/credentials/diary_logger/credentials.json`
3. First run opens browser for consent. Token cached.

## Usage

```bash
glancely diary log --title "wrapper refactor" --start 2:30pm --end 4pm
glancely diary stats
```

## Scripts

**scripts/log.py**
```
--title TEXT        Required. Activity description.
--start TIME        Start time (e.g. "2:30pm", "14:30").
--end TIME          End time.
--date DATE         Date (YYYY-MM-DD). Default: today.
```

**scripts/stats.py** — returns JSON for dashboard panel.

## Fields

- `title` (TEXT)
- `start_time` (TEXT)
- `end_time` (TEXT)
- `duration_minutes` (INTEGER)
- `date` (DATE)

## Dependencies

- google-auth>=2.20
- google-auth-oauthlib>=1.0
- google-api-python-client>=2.100
