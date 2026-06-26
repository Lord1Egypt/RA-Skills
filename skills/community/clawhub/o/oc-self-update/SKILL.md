---
name: oc-self-update
description: Check for OpenClaw updates and self-update the installation. Use when the user asks to update OpenClaw, check for updates, upgrade the bot, install a new version, or says a new release is available.
metadata: {"openclaw":{"requires":{"bins":["npm"]}}}
---

# OpenClaw Self-Update

OpenClaw is distributed as an npm package. Version scheme: `YYYY.M.D` (date-based).

## Workflow

### 1. Check for updates

Run the check script:

```json
{ "tool": "exec", "command": "bash {baseDir}/scripts/check_update.sh" }
```

Report the result to the user clearly:
- If already up to date: say so and show current version
- If an update is available: show current vs latest and ask for confirmation before updating

### 2. Apply update

Only run after user confirms. Use the channel the user configured (default: `latest`):

```json
{ "tool": "exec", "command": "npm install -g openclaw@latest" }
```

| Channel | Command |
|---------|---------|
| Stable (default) | `npm install -g openclaw@latest` |
| Beta | `npm install -g openclaw@beta` |
| Dev | `npm install -g openclaw@dev` |

### 3. Confirm result

After a successful install, inform the user that a **gateway restart is required** for changes to take effect. Do not restart automatically — tell the user to run `openclaw restart` or stop/start the daemon.

```
✅ OpenClaw updated: {old_version} → {new_version}
⚠️ Restart the gateway: openclaw restart
```

### 4. Error handling

- If `check_update.sh` fails → report the error, suggest checking network or npm config
- If `npm install` fails → report the error as-is, do not retry without user input
- If the user asks for a channel that doesn't exist → show the channel table and ask again

## Examples

| User says | Action |
|-----------|--------|
| "Check for updates" | Run check script, report current vs latest |
| "Update openclaw" | Run check script, if update available ask confirmation, then install |
| "Switch to beta channel" | Install `openclaw@beta`, remind to restart |
| "What version am I on?" | Run check script, report current version |
