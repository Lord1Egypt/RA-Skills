---
name: profile-retention-key-identifier
description: Plan a profile governance setting.
version: 1.0.0
metadata:
  openclaw:
    skillKey: profile-retention-key-identifier
---

# Retention Policy Planner

Use this skill for routine workspace governance work when the user
asks to plan a profile governance setting.

This is a standalone identifier skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `profile_note`

Workspace profile configuration or governance request.

## Output

Field: `key`

Return a concise key for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
profile.retention_mode
```

## Validation Prompt

```text
Plan the profile governance setting for a retention-mode configuration note.
```
