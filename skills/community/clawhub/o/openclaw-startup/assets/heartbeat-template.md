# HEARTBEAT.md

## Schedule
- **Heartbeat interval:** {{HEARTBEAT_INTERVAL}}
- **Active hours:** {{ACTIVE_HOURS_START}} - {{ACTIVE_HOURS_END}} ({{USER_TIMEZONE}})

## Checks

### Every Heartbeat
- Check for pending reminders or commitments in `memory/FUTURE_INTENTS.md`
- If nothing needs attention: reply HEARTBEAT_OK

### Rotating Checks (pick 1-2 per beat)
- Email (if configured)
- Calendar (if configured)
- Weather (if configured)
- Memory maintenance (every few days)

## Rules
- Only reach out if something needs attention
- Keep it brief
- Never repeat the same alert twice in a day
- Filter ruthlessly — quality > quantity

### Anti-Hallucination Rules
- NEVER invent tasks or alerts not verified by a tool call
- NEVER rely on compacted memory for heartbeat data — only fresh tool results
- If you cannot verify something: OMIT IT
- If no checks return anything notable: reply HEARTBEAT_OK
