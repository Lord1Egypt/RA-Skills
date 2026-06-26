---
name: openclaw-safe-ops
description: Guards high-risk OpenClaw operations with preflight backups, post-change health checks, and rollback guidance. Use when running gateway restart/start/stop, config set/unset, plugin install/update/uninstall, or editing openclaw.json.
---

# OpenClaw Safe Ops

## When To Apply

Apply this skill before any high-risk OpenClaw operation:

- `openclaw gateway restart|start|stop|install|uninstall|run|status`
- `openclaw config set|unset`
- `openclaw plugins install|update|uninstall|enable|disable`
- Manual edits to `~/.openclaw/openclaw.json`

## Safety Workflow

1. Capture a backup before change:
   - `cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.manual.$(date +%Y%m%d-%H%M%S).bak`
2. Run the intended command.
3. Validate immediately:
   - `openclaw channels status --probe`
   - `openclaw status --deep`
4. If checks fail, rollback:
   - `cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json`
   - `openclaw gateway restart`
   - `openclaw status --deep`

## Preferred Command Wrapper

For local terminal operations, prefer:

- `./scripts/openclaw-safe.sh <openclaw args...>`

This wrapper auto-backs up config for risky actions, runs health checks, and rolls back on failure.

## Output Requirements

When completing a risky operation, report:

- Command executed
- Backup path used
- Health check results
- Whether rollback was needed
