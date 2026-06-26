# Calendar & Scheduling

## Available Tools
- **gog** — Google Calendar (full CRUD)
- **apple-reminders** — macOS Reminders (date-based tasks)
- **things-mac** — Things 3 (task/project management)
- OpenClaw cron — Scheduling agent tasks

## Calendar Operations
- List events (day, week, month views)
- Create, update, delete events
- Set reminders and notifications
- Manage recurring events
- Check availability / free-busy

## Scheduling Patterns

### Time Blocking
- Group similar tasks into time blocks
- Leave buffer between meetings
- Protect deep work time

### Reminder System
```bash
# OpenClaw cron for reminders
cron add schedule="{kind: at, at: 2026-04-01T15:00:00Z}" \
  payload="{kind: systemEvent, text: Reminder: Meeting in 30 minutes}"
```

### Event-Driven Scheduling
- Email arrives → create calendar event
- Task completed → schedule follow-up
- Meeting ends → create action items

## Timezone Handling
- Always specify timezone explicitly
- Convert with: `date -d "2026-04-01 15:00 UTC" +%s`
- Store in UTC, display in local

## Calendar Best Practices
- Include meeting links in event descriptions
- Set reminders 15min before important events
- Review weekly calendar every Monday
- Block focus time proactively
- Color-code by category

## Integration Patterns
- Morning brief: calendar + weather + email summary
- Post-meeting: auto-create follow-up tasks
- Deadline tracking: calendar events → task lists
