# Complex Reminder Timetable

Use this structure to generate reminders from a detailed schedule.

## Core concepts

- `timezone`: IANA timezone, e.g. `Asia/Shanghai`
- `quiet_hours`: no reminders inside this window
- `profiles`: weekday/weekend or custom day-group behavior
- `rules`: reminder definitions with either fixed times or interval windows

## JSON shape

```json
{
  "timezone": "Asia/Shanghai",
  "quiet_hours": {"start": "23:30", "end": "07:00"},
  "profiles": {
    "weekday": {"days": ["Mon", "Tue", "Wed", "Thu", "Fri"]},
    "weekend": {"days": ["Sat", "Sun"]}
  },
  "rules": [
    {
      "id": "water-day",
      "type": "hydration",
      "message": "喝水 300ml",
      "profile": "weekday",
      "mode": "interval",
      "window_start": "08:00",
      "window_end": "22:00",
      "every_minutes": 120
    },
    {
      "id": "stand-work",
      "type": "mobility",
      "message": "起身活动 3-5 分钟",
      "profile": "weekday",
      "mode": "interval",
      "window_start": "09:30",
      "window_end": "18:30",
      "every_minutes": 55
    },
    {
      "id": "sleep-winddown",
      "type": "sleep",
      "message": "进入睡前流程",
      "profile": "weekday",
      "mode": "fixed",
      "times": ["22:30"]
    }
  ]
}
```

## Rule fields

- `mode = interval`
  - Require: `window_start`, `window_end`, `every_minutes`
  - Optional: `offset_minutes` (default 0), used to shift first reminder
- `mode = fixed`
  - Require: `times` (HH:MM list)

## Good defaults

- Hydration: 90-150 minutes
- Standing: 45-60 minutes
- Sleep wind-down: 45-75 minutes before bedtime
- Supplements: fixed at meal-linked times

## Output requirements

- Expand into a daily timetable per profile.
- Drop times that fall inside `quiet_hours`.
- Include summary counts per reminder type (e.g., water 7/day, stand 9/day).
