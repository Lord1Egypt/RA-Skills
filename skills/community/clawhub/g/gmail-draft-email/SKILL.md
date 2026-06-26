---
name: Gmail Draft Email
description: Atomic node skill to draft an email via Gmail using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if drafting fails.

# Gmail Draft Email

This skill allows the agent to create an email draft using the native CLI.

## Cognitive Directives
WHEN [An email needs to be drafted but not sent]
THEN [
  Execute the following Jidoka-validated loop:
  1. **Execute Node:** Execute the native terminal command `gog gmail drafts create --to "..." --subject "..." --body "..." --json`.
  2. **Verification Step (Jidoka):** Verify the command returns a valid JSON confirmation. IF it fails or returns an error message, wait 3 seconds and retry (max 3 times). IF it still fails, report the error to the user and STOP.
]

## Schema Example
```json
{
  "command": "gog gmail drafts create --to \"example@gmail.com\" --subject \"Invoice\" --body \"Please review the attached invoice.\" --json"
}
```

## Expected Output
Confirmation that the draft was created.
