---
name: openclaw-cursor-agent-system
description: Maintain the cursor-agent-system toolkit (spawn-cursor, check-status, send-command, kill-session shell scripts). Use when the user wants to modify, debug, or extend the tmux-based background task scripts.
---

# OpenClaw Cursor Agent System (Development)

Use this skill when modifying the `cursor-agent-system/` toolkit scripts.

## Toolkit Structure

```text
cursor-agent-system/
├── scripts/
│   ├── common.sh          # Shared utilities
│   ├── spawn-cursor.sh    # Start background task
│   ├── check-status.sh    # Query task status
│   ├── attach-session.sh  # Attach to tmux session
│   ├── send-command.sh    # Send instructions to task
│   └── kill-session.sh    # Stop task
├── templates/
│   └── cursor-task-prompt.md
├── status/    # Runtime: one JSON per session
├── tasks/     # Runtime: one MD + runner.sh per session
└── logs/      # Runtime: one log per session
```

## Rules

- Use `bash` with `set -euo pipefail`.
- User-facing errors in Chinese.
- Cursor CLI must run inside `tmux`, never directly.
- Session names follow `{prefix}-{task}-{timestamp}`.
- Keep shared logic in `common.sh`.
- After edits, validate shell syntax on all scripts.
- Do not delete runtime data in `status/`, `tasks/`, `logs/` unless asked.

## References

- [references/setup.md](references/setup.md) — Implementation details
- [references/task-prompt.md](references/task-prompt.md) — Task prompt template
