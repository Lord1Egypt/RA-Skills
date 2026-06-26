---
name: Gmail Modify Labels
description: Atomic node skill to modify email labels in Gmail using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the modification fails.

# Gmail Modify Labels

This skill allows the agent to add or remove labels from an email or thread using the native CLI.

## Cognitive Directives
WHEN [Labels on an email need to be changed, added, or removed]
THEN [
  Execute the following Jidoka-validated loop:
  1. **Execute Node:** Execute the native terminal command `gog gmail messages modify <messageId> ...` or equivalent label command.
  2. **Verification Step (Jidoka):** Verify the command returns a successful confirmation. IF it fails or returns an error message, wait 3 seconds and retry (max 3 times). IF it still fails, report the error to the user and STOP.
]

## Schema Example
```json
{
  "command": "gog gmail messages modify msg_id_123 --add-label INBOX --remove-label UNREAD --json"
}
```

## Expected Output
Confirmation that the labels were updated.
