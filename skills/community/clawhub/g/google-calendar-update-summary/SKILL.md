---
name: Google Calendar Update Summary
description: Atomic node skill to exclusively update the summary (title) of a Google Calendar event.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, strictly limited to updating ONLY the summary (title) of an event, preventing schema hallucination and ensuring single-responsibility.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the update fails. You MUST evaluate the output to ensure the summary was updated.

# Google Calendar Update Summary

This skill allows the agent to update the summary (title) of an existing event in Google Calendar using the native CLI. It does NOT update times, locations, or attendees.

## Cognitive Directives
WHEN [The title or summary of an existing event needs to be modified]
THEN [Execute the native terminal command `gog calendar update <calendarId> <eventId> --summary "..."`]

## Schema Example
```json
{
  "command": "gog calendar update primary event_id_123 --summary \"Updated Sync Meeting\" --json"
}
```

## Jidoka Validation Loop
1. Try: Execute the command.
2. Evaluate: Check the JSON response to confirm `summary` matches the requested string.
3. Correct/Fail: If it failed or hallucinated parameters, retry up to 3 times (max_retries=3) with the exact error.
4. Proceed: Return the final valid JSON.

## Expected Output
A JSON object confirming the updated event details with the new summary.
