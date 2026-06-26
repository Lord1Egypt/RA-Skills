---
name: Google Drive Upload File
description: Atomic node skill to upload a file to Google Drive using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the upload fails.

# Google Drive Upload File

This skill allows the agent to upload a local file to Google Drive using the native CLI.

## Cognitive Directives
WHEN [A local file needs to be uploaded to Google Drive]
THEN [Execute the native terminal command `gog drive upload <localPath>`]

## Schema Example
```json
{
  "command": "gog drive upload /path/to/local/file.txt --json"
}
```

## Expected Output
A JSON object confirming the uploaded file and its Drive ID.
