---
name: Google Drive Delete File
description: Atomic node skill to delete a file in Google Drive using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the deletion fails.

# Google Drive Delete File

This skill allows the agent to move a file to trash in Google Drive using the native CLI.

## Cognitive Directives
WHEN [A file needs to be removed or moved to trash in Google Drive]
THEN [Execute the native terminal command `gog drive delete <fileId>`]

## Schema Example
```json
{
  "command": "gog drive delete file_id_123"
}
```

## Expected Output
Confirmation that the file was moved to the trash.
