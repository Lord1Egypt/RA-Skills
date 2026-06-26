---
name: Gmail Delete Email
description: Atomic node skill to delete an email via Gmail using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if deletion fails.

# Gmail Delete Email

This skill allows the agent to move an email to the trash using the native CLI.

## Cognitive Directives
WHEN [An email needs to be deleted or moved to trash]
THEN [
  Execute the following Jidoka-validated loop:
  1. **Execute Node:** Execute the native terminal command `gog gmail trash <messageId>`.
  2. **Verification Step (Jidoka):** Check if the command returns a successful confirmation. IF it fails or returns an error, wait 3 seconds and retry (max 3 times). IF it still fails, report the error to the user and STOP.
]

## Schema Example
```json
{
  "command": "gog gmail trash msg_id_123"
}
```

## Expected Output
Confirmation that the email was moved to the trash.
