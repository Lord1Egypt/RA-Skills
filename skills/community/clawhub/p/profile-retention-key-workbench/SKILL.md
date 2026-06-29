---
name: profile-retention-key-workbench
description: Register a profile governance setting.
version: 1.0.0
metadata:
  openclaw:
    skillKey: profile-retention-key-workbench
---

# Profile Governance Register

Use this skill for routine workspace governance work when the user
asks to register a profile governance setting.

This is a standalone workbench skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `key`

Profile governance setting key selected by the user.

## Output

Field: `recorded_key`

Return a concise recorded key for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
profile.retention_mode
```

## Validation Prompt

```text
Using the profile governance setting planned in the previous step, register that key for the configuration note.
```
