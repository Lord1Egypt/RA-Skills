---
name: interaction-pipeline
description: Provide consistent status updates and concise summaries after each action.
metadata:
  openclaw:
    emoji: 🔄
    skillKey: interaction-pipeline
---

# Interaction Pipeline Skill

## Purpose
Provide consistent status updates and concise summaries after each action. Ensures user always knows: 1) what was done, 2) what's next or how to repeat.

## Status Flow
Every interaction follows:
```
STARTED -> IN_PROGRESS -> DONE
                -> BLOCKED (with reason)
```

## Summary Format
After completing an action (or hitting a block), send exactly 2 lines:

Line 1: What was accomplished (past tense, no emojis unless user uses them)
Line 2: What to do next OR how to repeat the action (short, actionable)

Example (DONE):
```
Backup created at /backups/2026-03-16.tar.gz.
Run `backup` again tomorrow or set a weekly cron.
```

Example (BLOCKED):
```
Cannot connect to database: timeout.
Check DB credentials and network, then retry.
```

## Rules
- Never send DONE/OK without the 2-line summary
- For multi-step tasks, summarize after each step, not only at the end
- If user asks for status mid-task, reply with current step + estimated completion
- When blocked, include the error cause and one concrete fix

## Integration
- Hook: after every tool execution (success or failure)
- Must not be suppressed by any other skill
- Overrides any default LLM response style

## Related Skills
- `guided-conversation` (pre-action clarity)
- `adaptive-execution-profile` (risk-based behavior)