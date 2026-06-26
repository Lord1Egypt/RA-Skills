---
name: macos-calendar-assistant
description: Manage macOS Calendar with OpenClaw in IM-first workflows (Telegram/Discord/Feishu/iMessage/Slack), including screenshot-to-schedule extraction, idempotent create/update, move/extend/reschedule, reminders, conflict checks, daily review sync, and duplicate cleanup. Use when users ask to add/edit/move/postpone events, parse schedule screenshots/chat messages, adjust weekly plans into daily execution, or keep calendar and review notes in sync.
---

# macos-calendar-assistant

Use bundled scripts for reliable Calendar.app operations.

## Workflow

1. Extract title, start/end, timezone, calendar, location, notes, alarm.
2. Check conflicts before writing:
   - `scripts/list_events.swift <start_iso> <end_iso>`
3. Prefer idempotent writes:
   - `scripts/upsert_event.py` (create/update/skip)
4. Apply alarm if requested:
   - `scripts/set_alarm.py --uid <event_uid> --alarm-minutes <n>`
5. For hygiene, run duplicate scan:
   - `scripts/calendar_clean.py --start <iso> --end <iso>`

## Calendar routing defaults

- Workout / Run / Training → `Training`
- Work / Meeting / Client → `Work`
- Product / Development / Building → `Product`
- Personal / Social / Travel → `Life`
- If unspecified: prefer writable iCloud/CalDAV calendars over local calendars.

> Note: Calendar names vary by user setup. Map the intent to the closest local calendar name before writing.

## Commands

### List calendars
```bash
swift scripts/list_calendars.swift
```

### List events in range
```bash
swift scripts/list_events.swift "2026-03-06T00:00:00+08:00" "2026-03-06T23:59:59+08:00"
```

Output includes `uid` for follow-up alarm/edit operations.

### Idempotent create/update (recommended)
```bash
python3 scripts/upsert_event.py \
  --title "Team sync" \
  --start "2026-03-06T19:00:00+08:00" \
  --end "2026-03-06T20:00:00+08:00" \
  --calendar "Work" \
  --notes "Agenda" \
  --location "Online" \
  --alarm-minutes 15
```

Result is one of: `CREATED`, `UPDATED`, `SKIPPED`.
Use `--dry-run` for preview.

### Legacy direct add (always creates)
```bash
python3 scripts/add_event.py --title "..." --start "..." --end "..."
```

### Set alarm by UID
```bash
python3 scripts/set_alarm.py --uid "EVENT_UID" --alarm-minutes 15
```

### Move event (legacy utility)
```bash
swift scripts/move_event.swift "Team sync" "Work" "2026-03-07T10:00:00+08:00" 60 --search-days 7
# optional precise match:
# --original-start "2026-03-06T10:00:00+08:00"
```
Prefer `upsert_event.py` for most rescheduling flows; use `move_event.swift` for direct title-based move when needed.

### Duplicate scan / cleanup
```bash
python3 scripts/calendar_clean.py --start "2026-03-01T00:00:00+08:00" --end "2026-03-08T23:59:59+08:00"
python3 scripts/calendar_clean.py --start "..." --end "..." --apply --confirm yes --snapshot-out ./delete-plan.json
```

### Upcoming events (within 2 hours)
```bash
python3 scripts/within_2h.py
```

### Environment + tests
```bash
python3 scripts/env_check.py
python3 scripts/regression_test.py
scripts/smoke_test.sh
```

### Daily auto-check notifier
```bash
scripts/install.sh     # run env check + install cron from config.json
scripts/uninstall.sh   # remove cron
```

## Extraction & scheduling heuristics (from real usage)

1. **Speaker ownership from chat screenshots**
   - Treat the user's message bubble as primary intent.
   - Treat counterpart bubbles as constraints (availability/travel window), not direct auto-create tasks.

2. **Conflict policy**
   - If user explicitly says "override" (for example, "replace this slot"), allow replacing an existing slot and reschedule the displaced event.
   - If not explicit, warn and ask for a choice before overwriting.

3. **Time-window intent parsing**
   - Phrases like "4–6 PM for the other person" should first be interpreted as an availability window.
   - Convert to a formal event only after user confirmation.

4. **Reschedule priority**
   - Prefer moving flexible events (workouts/optional blocks) before strategic P0 work blocks.
   - Do not auto-move P0 items unless user explicitly requests.

5. **Confirmation prompt template**
   - Use: "I identified X as your intent and Y as counterpart constraints. I will apply Z. Confirm?"
   - Keep it short; avoid over-confirming when intent is explicit.

## Constraints

- macOS only (EventKit + Calendar permission required)
- Default timezone comes from `config.json.timezone` (fallback Asia/Shanghai) when user does not specify
- Use `--apply` only after reviewing dry-run output
