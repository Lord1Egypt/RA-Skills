# Habit Tracker Data Format

All data lives in `~/.openclaw/workspace/habits/` by default (configurable via `HABIT_DATA_DIR` env var).

---

## habits.json

Master list of tracked habits.

```json
{
  "habits": [
    {
      "id": "exercise",           // slug — auto-generated from name, lowercase, underscores
      "name": "Exercise",         // display name
      "frequency": "daily",       // "daily" | "weekday" | "weekly"
      "created": "2024-01-15",    // ISO date string, set once at creation
      "active": true,             // false = soft-deleted (still in history)
      "emoji": "🏋️"              // optional display emoji
    }
  ]
}
```

### Frequency Semantics

| Value | Meaning | Days expected |
|-------|---------|---------------|
| `daily` | Every calendar day | Mon–Sun |
| `weekday` | Workdays only | Mon–Fri |
| `weekly` | Once per week | Any 1 day of the 7-day window |

Streak and completion rate calculations respect the frequency — a `weekday` habit not completed on Saturday doesn't break a streak.

---

## log.json

Daily completion records, keyed by ISO date.

```json
{
  "2024-01-15": {
    "exercise": {
      "done": true,
      "logged_at": "2024-01-15T08:32:00"  // ISO datetime, when log_habit.py was run
    },
    "reading": {
      "done": true,
      "logged_at": "2024-01-15T21:15:00"
    }
  },
  "2024-01-16": {
    "exercise": {
      "done": true,
      "logged_at": "2024-01-16T07:45:00"
    }
  }
}
```

### Notes

- Only completed habits appear in a date's entry — absence means not done.
- Dates with no completions may be absent entirely from the top-level object.
- `logged_at` is when the log command ran, not when the habit was done.
- Both files are created automatically by `setup_habits.py` or `log_habit.py` if missing.

---

## ID Generation

Habit IDs are slugified from the name:
- Lowercased
- Spaces → underscores
- Non-alphanumeric characters stripped
- Examples: `"Morning Run"` → `morning_run`, `"No Social Media"` → `no_social_media`

If a collision occurs (same slug, different name), a numeric suffix is appended: `reading_2`.
