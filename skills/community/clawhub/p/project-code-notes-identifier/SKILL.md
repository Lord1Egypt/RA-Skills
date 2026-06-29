---
name: project-code-notes-identifier
description: Identify the project handle from an intake note.
version: 1.0.0
metadata:
  openclaw:
    skillKey: project-code-notes-identifier
---

# Project Intake Identifier

Use this skill for routine project delivery operations work when the user
asks to identify the project handle from an intake note.

This is a standalone identifier skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `note`

Client brief, delivery note, or project update text.

## Output

Field: `project_code`

Return a concise project code for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
PRJ-ALPHA-1842
```

## Validation Prompt

```text
Identify the project handle from this delivery intake note.

Delivery intake note:
"Customer success handoff: account project PRJ-ALPHA-1842 needs a ledger update after today's design review."
```
