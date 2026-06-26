# NervTimer Intent Schema

Use this structure when converting user messages into deterministic timer actions.

## JSON shape

```json
{
  "action": "create_timer|complete_timer|cancel_timer|list_active",
  "timer": {
    "timer_id": "optional-string",
    "title": "string",
    "reason": "string-or-null",
    "schedule_type": "one_shot|recurrent",
    "timezone": "IANA timezone, e.g. Europe/Berlin",
    "scheduled_for": "ISO-8601 timestamp for one_shot",
    "recurrence": {
      "mode": "cron|every_ms",
      "cron_expr": "optional cron expression",
      "every_ms": "optional integer"
    }
  },
  "completion": {
    "timer_ref": "optional timer id or title fragment"
  }
}
```

## Validation requirements

- `action` is required.
- `create_timer` requires `timer.title` and `timer.schedule_type`.
- For `one_shot`, `timer.scheduled_for` is required.
- For `recurrent`, `timer.recurrence.mode` is required.
- If `timer.recurrence.mode=cron`, `timer.recurrence.cron_expr` is required.
- If `timer.recurrence.mode=every_ms`, `timer.recurrence.every_ms` is required and must be `>= 60000`.

## Completion intent policy

Treat completion as explicit only. Examples:

- German: `erledigt`, `habe ich gemacht`, `ist fertig`
- English: `done`, `finished`, `i did it`

If ambiguous, ask for explicit confirmation.
