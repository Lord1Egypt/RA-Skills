---
name: Google Calendar Update Event
description: Atomic node skill to update a Google Calendar event using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the update fails.

# Google Calendar Update Event

This skill allows the agent to update an existing event in Google Calendar using the native CLI.

## Cognitive Directives
WHEN [An existing event needs to be modified or rescheduled]
THEN [Execute the native terminal command `gog calendar update <calendarId> <eventId> --summary "..." --from "..." --to "..."`]

## Schema Example
```json
{
  "command": "gog calendar update primary event_id_123 --summary \"Updated Sync Meeting\" --json"
}
```

## Expected Output
A JSON object confirming the updated event details.
