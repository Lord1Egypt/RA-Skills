---
name: Google Docs Update Document
description: Atomic node skill to update a Google Doc using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the update fails.

# Google Docs Update Document

This skill allows the agent to write or insert text into an existing Google Document using the native CLI.

## Cognitive Directives
WHEN [Text needs to be added, written, or updated in a Google Doc]
THEN [Execute the native terminal command `gog docs write <docId> --text "..."` or `gog docs edit <docId> <find> <replace>`]

## Schema Example
```json
{
  "command": "gog docs edit doc_id_123 \"old text\" \"new text\""
}
```

## Expected Output
A JSON object or confirmation string indicating the update was successful.
