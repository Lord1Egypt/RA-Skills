---
name: openclaw-emergency-rollback/setup
description: One-time setup for OpenClaw Emergency Rollback. Read this when the user wants to install or initialize the rollback system for the first time.
---

# OpenClaw Emergency Rollback — One-Time Setup

Run this setup exactly once when `~/.openclaw/rollback/` does not exist.
Do not re-run setup if the directory already exists unless the user explicitly
asks to reinstall.

---

## Prerequisites

The rollback system uses Node.js (already installed with OpenClaw) and
standard Linux tools. Verify before proceeding:

```bash
echo "--- Checking dependencies ---"
node --version && echo "  ✓ node" || echo "  ✗ node NOT FOUND"
command -v tar >/dev/null && echo "  ✓ tar" || echo "  ✗ tar NOT FOUND"
command -v unzip >/dev/null && echo "  ✓ gzip" || echo "  ✗ gzip NOT FOUND"
echo "  ✓ no cron dependency — rollback uses detached Node timers plus a native OpenClaw gateway startup hook"
```

Node.js is required to run OpenClaw itself, so it is always present. If `zip`
or `unzip` are missing (common on stripped Docker images), install them:

- **Ubuntu/Debian VPS:** `sudo apt-get install -y tar gzip`
- **Docker (node:22-bookworm-slim):** Set `OPENCLAW_DOCKER_APT_PACKAGES="tar gzip"`
  in your Docker setup, or add to Dockerfile: `RUN apt-get update && apt-get install -y tar gzip`

---

## Step 1 — Ask for Restart Command

Before creating anything, ask the user:

```
To complete setup I need to know how to restart OpenClaw on your system.
What command restarts your OpenClaw gateway?

Common options:
  • kill -USR1 1                       (standard Linux install)
  • systemctl --user restart openclaw-gateway      (explicit systemd)
  • docker compose restart                         (Docker Compose)
  • docker compose down && docker compose up -d    (Docker full cycle)

Or enter a custom command for your setup.
```

Store the answer as RESTART_CMD. This is written to `rollback-config.json`
and never changed automatically after setup.

Also ask (or detect from `~/.openclaw/openclaw.json` if it exists):
- Confirm openclaw home is `~/.openclaw` (or ask if different)

Store as OC_HOME. Use the full absolute path (expand `~` to `$HOME`).

---

## Step 2 — Create Directory Structure

```bash
mkdir -p ~/.openclaw/rollback/snapshots
mkdir -p ~/.openclaw/rollback/scripts
mkdir -p ~/.openclaw/rollback/logs
```

---

## Step 3 — Write rollback-config.json

Use the absolute path for openclawHome (expand `~` to `$HOME`):

```bash
cat > ~/.openclaw/rollback/rollback-config.json << EOF
{
  "restartCommand": "kill -USR1 1",
  "openclawHome": "$HOME/.openclaw",
  "installedAt": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
```

If the user specified a different openclaw home path, use that instead.

> NOTE: The restart command is hardcoded to `kill -USR1 1` for this environment.

---

## Step 4 — Initialize watchdog.json

```bash
cat > ~/.openclaw/rollback/watchdog.json << 'EOF'
{
  "armed": false,
  "setAt": null,
  "expiryEpoch": null,
  "expiryHuman": null,
  "minutesSet": null,
  "targetSnapshot": "snapshot-1",
  "targetLabel": null
}
EOF
```

---

## Step 5 — Initialize manifest.json

```bash
cat > ~/.openclaw/rollback/manifest.json << 'EOF'
{
  "watchdog_target": "snapshot-1",
  "snapshots": []
}
EOF
```

---

## Step 6 — Copy All Scripts

Copy every file from this skill's `scripts/` directory into
`~/.openclaw/rollback/scripts/`. This includes:

- `utils.mjs` — shared Node.js module (imported by all `.mjs` scripts)
- `snapshot.mjs` 
- `restore.mjs` 
- `restore-if-armed.mjs` 
- `watchdog-set.mjs` 
- `watchdog-extend.mjs` 
- `watchdog-clear.mjs` 
- `watchdog-status.mjs` 
- `recovery-test.mjs` 

After copying, make the shell wrappers executable:

```bash
chmod +x ~/.openclaw/rollback/scripts/*.mjs
```

The `.mjs` files have `#!/usr/bin/env node` shebangs, so once they have the
execute bit, the agent or your startup scripts can call them directly without a shell wrapper.

---

## Step 7 — Install Native OpenClaw Startup Hook

This ensures that if OpenClaw restarts while the watchdog is armed, the recovery
check runs again natively inside OpenClaw on `gateway:startup`.

Create the managed hook under `~/.openclaw/hooks/watchdog-recovery/` with:
- `HOOK.md`
- `handler.ts`

Use the versions shipped in this skill under:
- `hooks/watchdog-recovery/HOOK.md`
- `hooks/watchdog-recovery/handler.ts`

Then enable the hook:

```bash
openclaw hooks enable watchdog-recovery
openclaw hooks check
openclaw hooks list
```

Expected behavior:
- if watchdog is unarmed, the hook exits immediately
- if watchdog is armed and expired, the hook runs `restore-if-armed.mjs`
- if watchdog is armed and not yet expired, the hook respawns `watchdog-timer.mjs` for the remaining time

This works the same way on pod, Docker, and local installs because it uses
OpenClaw's own native startup lifecycle instead of external schedulers.

---

## Step 8 — Confirm Setup Complete

```
✅ OpenClaw Emergency Rollback installed.

Location: ~/.openclaw/rollback/
Restart command: kill -USR1 1
Scripts: Node.js (.mjs) — directly executable
Startup recovery: native OpenClaw hook `watchdog-recovery` on `gateway:startup`

Next step: say "create snapshot" to save your current known-good config
before making any changes.

Optional: say "test emergency recovery" to run a destructive test that
verifies the full recovery pipeline works end-to-end.
```

---

## Reinstall / Reset

If the user wants to reinstall from scratch:
1. Back up existing snapshots: `cp -r ~/.openclaw/rollback/snapshots/ /tmp/openclaw-snapshots-backup/`
2. `rm -rf ~/.openclaw/rollback/`
3. Remove any old startup hook that points at a previous rollback install, if present.
4. Run setup again from Step 1.
5. Ask the user if they want their old snapshots restored from the backup.

Never silently delete snapshots — always back them up first and ask.
