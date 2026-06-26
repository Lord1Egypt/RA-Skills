---
name: Google Docs Create Document
description: Atomic node skill to create a Google Doc using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the creation fails.

# Google Docs Create Document

This skill allows the agent to create a new Google Document using the native CLI.

## Cognitive Directives
WHEN [A new Google Doc needs to be created]
THEN [Execute the native terminal command `gog docs create <title> --json`]

## Schema Example
```json
{
  "command": "gog docs create \"My New Document\" --json"
}
```

## Expected Output
A JSON object with the new document ID and details.
