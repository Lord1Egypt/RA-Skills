---
name: Google Drive Share File
description: Atomic node skill to share a file in Google Drive using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if sharing fails.

# Google Drive Share File

This skill allows the agent to share a file or folder in Google Drive using the native CLI.

## Cognitive Directives
WHEN [A file or folder needs to be shared with a user or made public]
THEN [Execute the native terminal command `gog drive share <fileId> --role reader --type user --email <email>`]

## Schema Example
```json
{
  "command": "gog drive share file_id_123 --role writer --type user --email example@gmail.com --json"
}
```

## Expected Output
A JSON object confirming the permission creation.
