# OpenClaw Backup — What Gets Saved

## Backed Up ✅

| Component | Path | Why |
|---|---|---|
| **Workspace** | `~/.openclaw/workspace/` | Agent memory, MEMORY.md, SOUL.md, USER.md, all custom files |
| **Extra Workspaces** | `~/.openclaw/workspace-*/` | Multi-agent team workspaces (workspace-team, workspace-dev, etc.) |
| **Gateway config** | `~/.openclaw/openclaw.json` | Models, channels config, **bot tokens**, **API keys**, plugins |
| **Skills** | `~/.openclaw/skills/` | All installed skills |
| **Extensions** | `~/.openclaw/extensions/` | Channel extensions (feishu, etc.) |
| **Credentials** | `~/.openclaw/credentials/` | Channel pairing state (telegram-allowFrom, telegram-pairing, etc.) |
| **Channel state** | `~/.openclaw/{telegram,discord,...}/` | Update offsets, session data — allows resume without re-pairing |
| **Agent config** | `~/.openclaw/agents/*/agent/` | Model provider config (apiKey, baseUrl, custom models) |
| **Session history** | `~/.openclaw/agents/*/sessions/` | Full conversation history (.jsonl) |
| **Devices** | `~/.openclaw/devices/` | Paired nodes/phones (paired.json) |
| **Cron jobs** | `~/.openclaw/cron/` | Scheduled tasks |
| **Identity** | `~/.openclaw/identity/` | Device identity files |
| **Scripts** | `guardian.sh`, `gw-watchdog.sh`, `start-gateway.sh` | Auto-restart and guardian logic (Linux/Mac) |
| **ClawHub** | `~/.openclaw/.clawhub/` | ClawHub registry data |
| **Delivery queue** | `~/.openclaw/delivery-queue/` | Pending message delivery queue |
| **Memory index** | `~/.openclaw/memory/` | QMD memory search index |

## NOT Backed Up ❌ (by design)

| Component | Reason |
|---|---|
| `logs/` | Runtime logs, not needed for restore |
| `media/` | Too large, easily regenerated |
| `browser/` | Browser automation data, ephemeral |
| `canvas/` | Static system file, reinstalled with OpenClaw |
| `completions/` | Shell completions, auto-regenerated |
| `node_modules/` | Reinstall with npm |
| `.git/` | Source control managed separately |
| Binary assets (png/jpg/mp4/gif/webp/svg) | Size; regenerate as needed |
| `subagents/runs.json` | Ephemeral sub-agent run state |
| `*.lock`, `*.deleted.*` | Temporary state files |

## Security Note

The backup archive contains **bot tokens, API keys, and session credentials**.

- Archive is created with `chmod 600` (owner read/write only) on Linux/Mac
- Store backups in a secure location
- Never commit the `.tar.gz` to a public git repo
- Transfer via scp/sftp, not plain HTTP

## Post-Restore

After restore, all channels reconnect automatically — **no re-pairing needed**.

If Telegram is silent after 30 seconds, send `/start` to your bot to re-trigger the connection.

### Restore to a New Instance

```bash
# On the NEW machine (after installing OpenClaw):
npm i -g openclaw

# Preview first:
node backup-restore.js restore openclaw-backup_xxx.tar.gz --dry-run

# Then apply:
node backup-restore.js restore openclaw-backup_xxx.tar.gz

# That's it — no re-pairing needed.
```
