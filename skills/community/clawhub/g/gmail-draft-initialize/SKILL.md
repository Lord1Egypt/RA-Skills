---
name: Gmail Draft Initialize
description: Atomic node skill to initialize a Gmail draft with recipients.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, strictly limited to initializing a draft with recipients, preventing complex multi-field string constructions.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the initialization fails.

# Gmail Draft Initialize

This skill allows the agent to create a new, empty email draft in Gmail with specified recipients. It does NOT set the subject or body (use the dedicated update skills for those).

## Cognitive Directives
WHEN [A new email needs to be drafted]
THEN [Execute the native terminal command `gog gmail drafts create --to "..." --json`]

## Schema Example
```json
{
  "command": "gog gmail drafts create --to \"example@gmail.com\" --json"
}
```

## Jidoka Validation Loop
1. Try: Execute the command.
2. Evaluate: Check the JSON response to confirm the draft ID is returned.
3. Correct/Fail: If it failed or hallucinated parameters, retry up to 3 times (max_retries=3) with the exact error.
4. Proceed: Return the final draft ID for subsequent update steps.

## Expected Output
A JSON object confirming the draft was created and returning the `draftId`.
