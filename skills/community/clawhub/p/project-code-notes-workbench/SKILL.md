---
name: project-code-notes-workbench
description: Append a delivery update to the account ledger.
version: 1.0.0
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

## Input

Field: `status_update`

Delivery update text supplied by the user.

## Output

Field: `recorded_update`

Return a concise recorded update for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
PRJ-ALPHA-1842
```

## Validation Prompt

```text
Using the project handle identified in the previous step, append this delivery update:
"Design review completed; next step is updating the project summary."
```
