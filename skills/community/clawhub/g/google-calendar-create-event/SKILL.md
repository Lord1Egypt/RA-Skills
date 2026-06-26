---
name: Google Calendar Create Event
description: Atomic node skill to create a Google Calendar event using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the creation fails.

# Google Calendar Create Event

This skill allows the agent to create a new event in Google Calendar using the native CLI.

## Cognitive Directives
WHEN [A new event needs to be scheduled or created in the calendar]
THEN [Execute the `gog` tool with the `args` parameter]

**CRITICAL RULE:** Do NOT use the `--title`, `--start`, or `--end` flags. They do not exist. You MUST use `--summary` for the title, and `--from` and `--to` for the time bounds. The time MUST be in RFC3339 format or relative (e.g. "tomorrow 16:00").

## Schema Example
```json
{
  "args": "calendar create primary --summary \"New Sync Meeting\" --from \"2026-04-26T10:00:00Z\" --to \"2026-04-26T11:00:00Z\" --json"
}
```

## Expected Output
A JSON object confirming the created event details.
