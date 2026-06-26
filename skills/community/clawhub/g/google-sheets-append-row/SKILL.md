---
name: Google Sheets Append Row
description: Atomic node skill to append a row in Google Sheets using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the append fails.

# Google Sheets Append Row

This skill allows the agent to append values to a range in a Google Sheet using the native CLI.

## Cognitive Directives
WHEN [New data rows need to be appended to a Google Sheet]
THEN [Execute the native terminal command `gog sheets append <spreadsheetId> <range> --values-json '[["..."]]'`]

## Schema Example
```json
{
  "command": "gog sheets append sheet_id_123 \"Tab1!A:C\" --values-json '[[\"Val1\", \"Val2\", \"Val3\"]]' --json"
}
```

## Expected Output
A JSON object confirming the appended rows.
