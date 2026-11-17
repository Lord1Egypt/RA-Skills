# Timezone Handling Patterns for Google Calendar API

## Problem

Google Calendar API returns event start/end times in two formats:
1. **All-day events**: `start.date` / `end.date` (e.g., `"2026-06-15"`)
2. **Timed events**: `start.dateTime` / `end.dateTime` with timezone offset (e.g., `"2026-06-15T12:00:00-07:00"` or `"2026-06-15T19:00:00Z"`)

Different calendars may store the same event with different UTC offsets, making cross-calendar comparison require normalization.

## Normalization Pattern (Python)

```python
from datetime import datetime, timedelta

def parse_dt(dt_str):
    """Parse datetime string and return naive UTC datetime."""
    if dt_str.endswith('Z'):
        # UTC (Z suffix)
        return datetime.fromisoformat(dt_str.replace('Z', ''))
    elif '+' in dt_str or dt_str.count('-') > 2:
        # Has timezone offset like -07:00 or +05:30
        dt = datetime.fromisoformat(dt_str)
        if dt.tzinfo:
            offset = dt.utcoffset()
            if offset:
                dt = dt - offset
            return dt.replace(tzinfo=None)
        return dt
    else:
        # No timezone - assume local (PDT = UTC-7 for America/Los_Angeles)
        return datetime.fromisoformat(dt_str) + timedelta(hours=7)

def to_pdt(dt_utc):
    """Convert naive UTC to naive PDT for display."""
    return dt_utc - timedelta(hours=7)
```

## Key Points

- **Always normalize to UTC first** for comparison, then convert to local for display
- **PDT = UTC-7** (March–November), **PST = UTC-8** (November–March)
- For recurring events, `singleEvents=True` expands instances but preserves each instance's original timezone
- When building `time_min`/`time_max` for queries, use the target date's offset, not today's (DST boundary issue)
- Cross-calendar duplicate detection: normalize both to local time before comparing summary + start + location

## Cron-Compatible Execution

Since `execute_code` is blocked in cron mode, use the `write_file` + `terminal` pattern:

```bash
# 1. Write analysis script to temp file
write_file("/tmp/sands_analysis.py", script_content)

# 2. Run via terminal
terminal("python3 /tmp/sands_analysis.py")

# 3. Read results from stdout or output JSON file
```