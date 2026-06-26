# Calendar Reference

## List events

```
python scripts/calendar_sync.py list --start 2026-03-03T00:00Z --end 2026-03-05T00:00Z --top 20
```

Without parameters, `list` covers now through +7 days.

## Create event

```
python scripts/calendar_sync.py create \
  --subject "Meeting with team" \
  --start 2026-03-05T12:00 \
  --end 2026-03-05T13:00 \
  --tz UTC \
  --body "Weekly project sync" \
  --location "Conference Room A" \
  --attendees person1@example.com person2@example.com \
  --online
```

When `--online` is enabled, the script requests an online meeting and appends the join link to the event body if Graph returns one.
For personal Microsoft accounts (`tenant=consumers`), Graph can return no join URL even when `--online` is set.

## Update event

```
python scripts/calendar_sync.py update <eventId> --start 2026-03-05T12:30 --end 2026-03-05T13:30
```

## Cancel event

```
python scripts/calendar_sync.py cancel <eventId> --message "Rescheduling this event."
```

### Notes
- Dates should use ISO 8601 format. Add `Z` for explicit UTC.
- `--online` requests a Teams meeting; omit for in-person events.
- `OnlineMeetings.*` scopes are not supported for `tenant=consumers` in this workflow.
- Updates accept `--attendees` and overwrite the full attendee list.
