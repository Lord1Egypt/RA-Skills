---
name: Google Drive Download File
description: Atomic node skill to download a file from Google Drive using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the download fails.

# Google Drive Download File

This skill allows the agent to download a file from Google Drive using the native CLI.

## Cognitive Directives
WHEN [A file needs to be downloaded locally from Google Drive]
THEN [Execute the native terminal command `gog drive download <fileId> --out <localPath>`]

## Schema Example
```json
{
  "command": "gog drive download file_id_123 --out /tmp/document.pdf"
}
```

## Expected Output
Confirmation that the file was downloaded to the specified path.
