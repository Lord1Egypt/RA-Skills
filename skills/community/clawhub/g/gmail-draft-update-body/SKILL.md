---
name: Gmail Draft Update Body
description: Atomic node skill to update the body text of an existing Gmail draft.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, strictly limited to updating the body of a draft, preventing complex multi-field string constructions.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection.

# Gmail Draft Update Body

This skill allows the agent to update the body of an existing Gmail draft using the native CLI.

## Cognitive Directives
WHEN [The body of a Gmail draft needs to be set or updated]
THEN [Execute the native terminal command `gog gmail drafts update <draftId> --body "..." --json`]

## Schema Example
```json
{
  "command": "gog gmail drafts update draft_id_123 --body \"Please review the attached invoice.\" --json"
}
```

## Jidoka Validation Loop
1. Try: Execute the command.
2. Evaluate: Check the JSON response to confirm the body was updated.
3. Correct/Fail: If it failed or hallucinated parameters, retry up to 3 times (max_retries=3).
4. Proceed: Return the confirmation.

## Expected Output
A JSON object confirming the draft was updated.
