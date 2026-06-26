---
name: Gmail Retrieve Email
description: Atomic node skill to read a specific email via Gmail using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if retrieval fails.

# Gmail Retrieve Email

This skill allows the agent to retrieve the full contents of a specific email using the native CLI.

## Cognitive Directives
WHEN [The contents of a specific email need to be read]
THEN [Execute the native terminal command `gog gmail messages get <messageId> --json`]

## Schema Example
```json
{
  "command": "gog gmail messages get msg_id_123 --json"
}
```

## Expected Output
A JSON object containing the email headers, body, and metadata.
