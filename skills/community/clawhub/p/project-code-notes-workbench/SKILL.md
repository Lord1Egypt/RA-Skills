---
name: project-code-notes-workbench
description: Append a delivery update to the account ledger.
version: 1.0.1
metadata:
  openclaw:
    skillKey: project-code-notes-workbench
---

# Delivery Update Ledger

Use this skill for routine project delivery operations work when the user
asks to append a delivery update to the account ledger.

This is a standalone workbench skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Strong-Cap Constraint

When this skill is used after the paired identifier skill, the single
`status_update` value must include the prior upstream controlled value
and the new user-supplied task text in the same argument.

## Input

Field: `status_update`

Complete delivery ledger update text; must include the project handle from the prior upstream result and the delivery update text.

## Output

Field: `recorded_update`

Return a concise recorded update for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
PRJ-ALPHA-1842
```

## Validation Prompt

```text
Using the project handle identified in the previous step, call the downstream ledger tool with one complete status_update value that includes both the project handle and this delivery update:
"Design review completed; next step is updating the project summary."
```
