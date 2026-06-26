---
name: openclaw-cursor-agent
description: Manage long-running Cursor CLI coding tasks through OpenClaw tools backed by tmux sessions. Use when the user asks to start a persistent coding job, inspect task status, send follow-up instructions, stop a running Cursor session, or mentions /cursor, tmux, spawn-cursor, check-status, send-command, or kill-session.
---

# OpenClaw Cursor Agent

Use this skill when the user wants OpenClaw to control a persistent `tmux -> Cursor CLI` task instead of running a short inline coding flow.

## Available Tools

- `cursor_agent_spawn_task`
- `cursor_agent_list_tasks`
- `cursor_agent_check_status`
- `cursor_agent_send_command`
- `cursor_agent_kill_session`
- `cursor_agent_doctor`

## Workflow

1. Start with `cursor_agent_doctor` if the environment may be incomplete.
2. Use `cursor_agent_spawn_task` to create a background task.
3. Use `cursor_agent_check_status` or `cursor_agent_list_tasks` to monitor it.
4. Use `cursor_agent_send_command` for `/pause`, `/resume`, `/status`, `/focus`, or new instructions.
5. Use `cursor_agent_kill_session` when the user wants to stop the run.

## Output Style

- Summarize the session name after spawning.
- Report current step, progress, and whether tmux is still alive when checking status.
- When the environment is missing `tmux`, `bash`, WSL, or Cursor CLI, tell the user exactly which dependency is missing.

## Extra Reference

- Read [references/commands.md](references/commands.md) for the recommended `/cursor` command patterns.
