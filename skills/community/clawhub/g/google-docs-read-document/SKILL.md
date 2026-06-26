---
name: Google Docs Read Document
description: Atomic node skill to read a Google Doc using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if reading fails.

# Google Docs Read Document

This skill allows the agent to read the plain text contents of a Google Document using the native CLI.

## Cognitive Directives
WHEN [The contents of a Google Doc need to be read]
THEN [Execute the native terminal command `gog docs cat <docId>`]

## Schema Example
```json
{
  "command": "gog docs cat doc_id_123"
}
```

## Expected Output
The plain text content of the Google Doc.
