---
name: Google Drive Search Files
description: Atomic node skill to search for files in Google Drive using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the search fails.

# Google Drive Search Files

This skill allows the agent to search for files across Google Drive using the native CLI.

## Cognitive Directives
WHEN [A file or folder needs to be located in Google Drive]
THEN [Execute the native terminal command `gog drive search "query" --json`]

## Schema Example
```json
{
  "command": "gog drive search \"project proposal\" --json"
}
```

## Expected Output
A JSON array of file objects matching the search criteria.
