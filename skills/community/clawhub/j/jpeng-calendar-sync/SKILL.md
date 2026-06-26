---
name: jpeng-calendar-sync
description: "Calendar synchronization skill. Sync events between Google Calendar, Outlook, and local storage. Supports CRUD operations and reminders."
version: "1.0.0"
author: "jpeng"
tags: ["calendar", "google", "outlook", "scheduling", "events"]
---

# Calendar Sync

Synchronize calendar events across Google Calendar, Outlook, and local storage.

## When to Use

- User wants to add/edit/delete calendar events
- Sync events between different calendar providers
- Set up reminders and recurring events
- Check availability and schedule meetings

## Configuration

```bash
# Google Calendar
export GOOGLE_CLIENT_ID="xxx"
export GOOGLE_CLIENT_SECRET="xxx"
export GOOGLE_REDIRECT_URI="http://localhost:8080/callback"

# Microsoft Outlook
export OUTLOOK_CLIENT_ID="xxx"
export OUTLOOK_CLIENT_SECRET="xxx"
```

## Usage

### List events

```bash
python3 scripts/calendar.py list --days 7
```

### Add event

```bash
python3 scripts/calendar.py add \
  --title "Team Meeting" \
  --start "2024-01-15T10:00:00" \
  --end "2024-01-15T11:00:00" \
  --description "Weekly sync" \
  --reminder 15
```

### Delete event

```bash
python3 scripts/calendar.py delete --event-id "xxx"
```

### Check availability

```bash
python3 scripts/calendar.py available \
  --date "2024-01-15" \
  --duration 60
```

## Output

```json
{
  "success": true,
  "event_id": "evt_xxx",
  "calendar_link": "https://calendar.google.com/..."
}
```
