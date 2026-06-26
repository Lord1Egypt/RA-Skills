---
name: Google Calendar Update Time
description: Atomic node skill to exclusively update the start and end time of a Google Calendar event.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, strictly limited to updating ONLY the start and end times of an event, preventing schema hallucination and ensuring single-responsibility.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the update fails. You MUST evaluate the output to ensure the time was updated correctly.

# Google Calendar Update Time

This skill allows the agent to update the start and end times of an existing event in Google Calendar using the native CLI. It does NOT update the title, location, or attendees.

## Cognitive Directives
WHEN [The start or end time of an existing event needs to be modified or rescheduled]
THEN [Execute the native terminal command `gog calendar update <calendarId> <eventId> --from "..." --to "..."`]

## Schema Example
```json
{
  "command": "gog calendar update primary event_id_123 --from \"2026-04-28T10:00:00Z\" --to \"2026-04-28T11:00:00Z\" --json"
}
```

## Jidoka Validation Loop
1. Try: Execute the command.
2. Evaluate: Check the JSON response to confirm `start` and `end` times match the requested strings.
3. Correct/Fail: If it failed or hallucinated parameters, retry up to 3 times (max_retries=3) with the exact error.
4. Proceed: Return the final valid JSON.

## Expected Output
A JSON object confirming the updated event details with the new start and end times.
