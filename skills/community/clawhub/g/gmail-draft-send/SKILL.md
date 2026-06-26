---
name: Gmail Draft Send
description: Atomic node skill to send an existing Gmail draft.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, strictly limited to sending an existing draft.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection.

# Gmail Draft Send

This skill allows the agent to send an existing Gmail draft using the native CLI.

## Cognitive Directives
WHEN [An existing email draft needs to be sent]
THEN [Execute the native terminal command `gog gmail drafts send <draftId> --json`]

## Schema Example
```json
{
  "command": "gog gmail drafts send draft_id_123 --json"
}
```

## Jidoka Validation Loop
1. Try: Execute the command.
2. Evaluate: Check the JSON response to confirm the email was sent successfully.
3. Correct/Fail: If it failed or hallucinated parameters, retry up to 3 times (max_retries=3).
4. Proceed: Return the confirmation.

## Expected Output
A JSON object confirming the email was sent successfully.
