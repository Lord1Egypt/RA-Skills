---
name: openclaw-upgrade-standard
description: Safe OpenClaw upgrade procedure with backup, doctor fix, service migration, rollback, and post-upgrade testing. Prevents silent failures from Dashboard upgrades, entrypoint renames, and config breaking changes.
metadata:
  openclaw:
    emoji: "⬆️"
---

# OpenClaw Upgrade Standard

A battle-tested upgrade procedure for OpenClaw, born from a real production failure where a Dashboard upgrade silently broke Gateway communication (Telegram, WebChat) with no clear error message.

**Use this skill when:** upgrading OpenClaw to a new version, planning a safe upgrade path, or recovering from a failed upgrade.

## Why This Exists

In March 2026, a Dashboard-triggered upgrade from 2026.3.13 to 2026.3.22 caused:
- Silent Gateway failure (Telegram showed "typing" but never delivered)
- Dashboard used `pnpm` which wasn't installed
- Gateway entrypoint renamed (`entry.js` → `index.js`) without service file migration
- `openclaw doctor --fix` fixed config but NOT the systemd service file
- Required backup restore to recover

This procedure prevents all of these issues.

## Golden Rule

**NEVER upgrade via the Dashboard.** Always use CLI.

## Procedure

### Step 1: Backup (2 min)

```bash
BACKUP_DIR="$HOME/.openclaw/workspace/backups/openclaw-upgrade-$(date -u +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Config + credentials + agents
cp ~/.openclaw/openclaw.json "$BACKUP_DIR/"
cp -r ~/.openclaw/credentials "$BACKUP_DIR/" 2>/dev/null
cp -r ~/.openclaw/agents "$BACKUP_DIR/agents" 2>/dev/null

# Service file
cp ~/.config/systemd/user/openclaw-gateway.service "$BACKUP_DIR/" 2>/dev/null

# Version info
openclaw --version > "$BACKUP_DIR/state-info.txt"
npm list -g openclaw >> "$BACKUP_DIR/state-info.txt" 2>&1

echo "Backup saved to: $BACKUP_DIR"
```

### Step 2: Read Release Notes (5 min)

Check https://github.com/openclaw/openclaw/releases

**Red flags to watch for:**
- "Breaking" entries → config or plugin changes
- Plugin SDK changes → can break Telegram/Discord
- Entrypoint changes → service file needs update
- Config/State migration → may invalidate existing config

### Step 3: Doctor Baseline (1 min)

```bash
openclaw doctor 2>&1 | tee "$BACKUP_DIR/doctor-before.txt"
```

### Step 4: Upgrade (3 min)

```bash
# ALWAYS use npm, never pnpm or Dashboard
npm update -g openclaw

# Verify
openclaw --version
```

### Step 5: Doctor Fix (2 min)

```bash
# Check what needs migration
openclaw doctor

# Apply fixes (config schema changes, deprecations)
openclaw doctor --fix
```

### Step 6: Fix Service Entrypoint (1 min)

```bash
# Check if entrypoint still matches
CURRENT_ENTRY=$(grep ExecStart ~/.config/systemd/user/openclaw-gateway.service | grep -oP 'dist/\K[^\ ]+')
ACTUAL_ENTRY=$(ls ~/.npm-global/lib/node_modules/openclaw/dist/index.js 2>/dev/null && echo "index.js" || echo "entry.js")

if [ "$CURRENT_ENTRY" != "$ACTUAL_ENTRY" ]; then
  echo "⚠️  Entrypoint mismatch: service=$CURRENT_ENTRY actual=$ACTUAL_ENTRY — fixing..."
  sed -i "s|dist/$CURRENT_ENTRY|dist/$ACTUAL_ENTRY|g" ~/.config/systemd/user/openclaw-gateway.service
  echo "✅ Fixed"
else
  echo "✅ Entrypoint OK"
fi
```

### Step 7: Restart Gateway (1 min)

```bash
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway.service
sleep 5
systemctl --user status openclaw-gateway.service
```

### Step 8: Test (5 min)

| Test | Command / Action | Expected |
|---|---|---|
| Gateway running | `systemctl --user status openclaw-gateway` | active (running) |
| Version correct | `openclaw --version` | New version number |
| Doctor clean | `openclaw doctor` | No "invalid config" errors |
| WebChat | Send message in Dashboard | Response within 30s |
| Telegram | Send message to bot | Response within 30s |
| Agents listed | `openclaw status` | All agents shown |
| Cron jobs | Check cron list | Jobs intact |

### Step 9: Document (2 min)

**Success:** Note version change + any fixes applied in your daily log.

**Failure:** Save all evidence, then rollback:

```bash
# Capture evidence BEFORE rollback
openclaw doctor 2>&1 > "$BACKUP_DIR/doctor-failed.txt"
journalctl --user -u openclaw-gateway -n 200 > "$BACKUP_DIR/gateway-logs-failed.txt" 2>&1
openclaw --version >> "$BACKUP_DIR/failure-info.txt"
```

## Rollback Procedure

```bash
# 1. Install previous version
npm install -g openclaw@<OLD_VERSION>

# 2. Restore config
cp "$BACKUP_DIR/openclaw.json" ~/.openclaw/openclaw.json
cp "$BACKUP_DIR/openclaw-gateway.service" ~/.config/systemd/user/

# 3. Restart
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway.service

# 4. Verify
openclaw --version
openclaw status
```

## Known Pitfalls

| Problem | Cause | Fix |
|---|---|---|
| Dashboard upgrade fails | Uses pnpm (not installed) | Always use `npm update -g openclaw` |
| Gateway won't start | Entrypoint renamed | Fix service file (Step 6) |
| Config invalid | Schema breaking changes | `openclaw doctor --fix` |
| Telegram silent | Gateway crashed or misconfigured | Check service status + logs |
| "first-time setup mode" | Pairing state reset | Re-pair or check config |
| Skills path errors | Skill paths changed | Re-check skill directories |

## Filing a Bug Report

If the upgrade fails and rollback is needed, file a bug at `github.com/openclaw/openclaw/issues` with:
1. OS, Node version, npm version
2. Upgrade path (from → to)
3. Install method (npm global / pnpm / other)
4. `openclaw doctor` output (before and after)
5. Gateway logs (`journalctl --user -u openclaw-gateway -n 200`)
6. Steps to reproduce
7. Whether rollback succeeded
