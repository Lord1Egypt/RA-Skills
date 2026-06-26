---
name: Google Calendar Delete Event
description: Atomic node skill to delete a Google Calendar event using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the deletion fails.

# Google Calendar Delete Event

This skill allows the agent to delete an event from Google Calendar using the native CLI.

## Cognitive Directives
WHEN [An event needs to be removed or deleted from the calendar]
THEN [Execute the native terminal command `gog calendar delete <calendarId> <eventId>`]

## Schema Example
```json
{
  "command": "gog calendar delete primary event_id_123"
}
```

## Expected Output
Confirmation that the event was deleted.
