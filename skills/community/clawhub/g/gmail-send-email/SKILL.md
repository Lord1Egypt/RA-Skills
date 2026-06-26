---
name: Gmail Send Email
description: Atomic node skill to send an email via Gmail using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if sending fails.

# Gmail Send Email

This skill allows the agent to send an email using the native CLI.

## Cognitive Directives
WHEN [An email needs to be sent to one or more recipients]
THEN [Execute the native terminal command `gog gmail send --to "..." --subject "..." --body "..."`]

## Schema Example
```json
{
  "command": "gog gmail send --to \"example@gmail.com\" --subject \"Invoice\" --body \"Please find the invoice attached.\" --json"
}
```

## Expected Output
Confirmation that the email was sent successfully.
