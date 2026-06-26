---
name: jpeng-reminder
description: "Reminder and scheduling skill. Set one-time or recurring reminders, manage tasks, and send notifications."
version: "1.0.0"
author: "jpeng"
tags: ["reminder", "schedule", "notification", "task", "alarm"]
---

# Reminder

Set reminders and scheduled notifications.

## When to Use

- User wants to set a reminder
- Schedule recurring tasks
- Manage to-do lists
- Send timed notifications

## Features

- **One-time reminders**: Set for specific time
- **Recurring reminders**: Daily, weekly, monthly
- **Natural language**: "remind me in 30 minutes"
- **Multi-channel**: Push, email, message

## Usage

### Set reminder

```bash
python3 scripts/reminder.py add \
  --message "Team meeting" \
  --time "2024-01-15T14:00:00"
```

### Natural language

```bash
python3 scripts/reminder.py add \
  --message "Take a break" \
  --in "2 hours"
```

### Recurring reminder

```bash
python3 scripts/reminder.py add \
  --message "Daily standup" \
  --schedule "every day at 9:00"
```

### List reminders

```bash
python3 scripts/reminder.py list
```

### Complete reminder

```bash
python3 scripts/reminder.py complete --id "rem_xxx"
```

### Delete reminder

```bash
python3 scripts/reminder.py delete --id "rem_xxx"
```

## Output

```json
{
  "success": true,
  "reminder_id": "rem_xxx",
  "message": "Team meeting",
  "scheduled_for": "2024-01-15T14:00:00",
  "channel": "push"
}
```

## Storage

Reminders are persisted in `~/.openclaw/reminders.json` and survive restarts.
