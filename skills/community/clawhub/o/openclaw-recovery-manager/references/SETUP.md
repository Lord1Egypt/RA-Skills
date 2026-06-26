---
name: openclaw-emergency-rollback/setup
description: One-time setup for OpenClaw Recovery Manager (installs as openclaw-emergency-rollback). Read this when the user wants to install or initialize the rollback system for the first time.
---

# OpenClaw Recovery Manager — One-Time Setup

*(Install name kept as `openclaw-emergency-rollback` for compatibility.)*

Run this setup exactly once when `~/.openclaw/rollback/` does not exist.
Do not re-run setup if the directory already exists unless the user
explicitly asks to reinstall.

---

## Prerequisites

The Recovery Manager uses Node.js (already installed with OpenClaw) and
standard Linux tools. Verify before proceeding:

```bash
echo "--- Checking dependencies ---"
node --version && echo "  ✓ node" || echo "  ✗ node NOT FOUND"
command -v tar >/dev/null  && echo "  ✓ tar"  || echo "  ✗ tar NOT FOUND"
command -v gzip >/dev/null && echo "  ✓ gzip" || echo "  ✗ gzip NOT FOUND"
echo "  ✓ no cron dependency — rollback uses detached Node timers plus a native OpenClaw gateway startup hook"
```

Node.js is required to run OpenClaw itself, so it is always present. If `tar`
or `gzip` are missing (rare, but possible on stripped Docker images), install
them:

- **Ubuntu/Debian VPS:** `sudo apt-get install -y tar gzip`
- **Docker (node:22-bookworm-slim):** Set `OPENCLAW_DOCKER_APT_PACKAGES="tar gzip"`
  in your Docker setup, or add to Dockerfile:
  `RUN apt-get update && apt-get install -y tar gzip`

---

## Step 1 — Detect the Restart Command (do NOT ask the user)

The restart command is the most critical piece of setup — a wrong value
means auto-recovery can't actually recover. **Detect it. Don't ask the user
to pick from a list.** Users often don't know which install method is in
use on their own machine, and guessing wrong silently breaks the
dead-man's-switch.

### Preferred: run the detection script

This skill ships a detection script that performs all the probes below
and prints a clean parseable result. Copy and run it from this skill's
`scripts/` directory (you can run it directly out of the skill before
copying scripts into `~/.openclaw/rollback/scripts/`):

```bash
node /path/to/this/skill/scripts/detect-restart-command.mjs
```

Output format:

```
DETECTED: <the restart command, or (none)>
REASON:   <short human-readable reason>
METHOD:   <systemd-user | systemd-system | docker-compose | pid1 | unknown>
CONFIDENCE: <high | medium | low>
```

- Exit 0 with a `DETECTED:` value → use that command.
- Exit 1 → no confident match; fall back to asking the user.

### Manual detection (only if you can't run the script)

Run each probe in order, stop at the first match.

**Probe 1 — systemd user service** *(most common on modern Linux VPS)*

```bash
systemctl --user is-active openclaw-gateway 2>/dev/null
```

If this returns `active`, the restart command is:
`systemctl --user restart openclaw-gateway`

Also try the system-level service if user-level is not active:

```bash
systemctl is-active openclaw-gateway 2>/dev/null
```

If `active`, the restart command is:
`sudo systemctl restart openclaw-gateway`

**Probe 2 — Docker Compose** *(container host)*

```bash
docker compose ps --services 2>/dev/null | grep -E '(openclaw|gateway)' \
  || docker-compose ps --services 2>/dev/null | grep -E '(openclaw|gateway)'
```

If there's a match, the restart command is:
`docker compose restart <matched-service-name>`

**Probe 3 — Running as PID 1 in a container** *(Docker/K8s primary
process)*

```bash
cat /proc/1/comm 2>/dev/null
cat /proc/1/cmdline 2>/dev/null | tr '\0' ' '
[ -f /.dockerenv ] && echo "container: docker"
grep -q 'kubepods\|containerd' /proc/1/cgroup 2>/dev/null && echo "container: k8s"
```

If in a container AND PID 1's cmdline contains `openclaw`, use:
`kill -USR1 1`

**Probe 4 — Standalone process (non-container, non-systemd)**

```bash
pgrep -af openclaw
```

If processes exist but none of Probes 1-3 matched, report this to the user
and ask how they'd like it restarted. This is the only case where asking
is appropriate.

### Verify Before Storing

Once a restart command is detected, **state what you found and why**, then
confirm with the user before writing it to `rollback-config.json`:

```
I checked how OpenClaw is running on this machine.

Detected: systemd user service (`openclaw-gateway` is active under
--user). The correct recovery restart command is:

  systemctl --user restart openclaw-gateway

This is what will run if the dead-man's-switch fires. Want me to store
this and continue setup? (Say "yes" or give me a different command.)
```

Never default to `kill -USR1 1` without verifying PID 1 is actually
OpenClaw. A wrong default here silently disarms recovery.

### OpenClaw Home

Detect from the environment — don't ask unless detection fails:

```bash
[ -n "$OPENCLAW_HOME" ] && echo "$OPENCLAW_HOME"
[ -f "$HOME/.openclaw/openclaw.json" ] && echo "$HOME/.openclaw"
```

If `OPENCLAW_HOME` is set, use it. Otherwise if
`~/.openclaw/openclaw.json` exists, OC_HOME is `~/.openclaw`. Only ask if
neither resolves.

Store the detected values as RESTART_CMD and OC_HOME (absolute paths, with
`~` expanded to `$HOME`). These go into `rollback-config.json` and are not
changed automatically after setup.

---

## Step 2 — Create Directory Structure

```bash
mkdir -p ~/.openclaw/rollback/snapshots
mkdir -p ~/.openclaw/rollback/skills
mkdir -p ~/.openclaw/rollback/projects
mkdir -p ~/.openclaw/rollback/scripts
mkdir -p ~/.openclaw/rollback/logs
```

`snapshots/` holds config snapshots (the auto-restore target).
`skills/` and `projects/` hold per-target subfolders created on first
snapshot; nothing needs to be pre-created inside them.

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

If the user specified a different openclaw home path or restart command, use
those instead.

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

## Step 5 — Initialize manifest.json (config subsystem)

```bash
cat > ~/.openclaw/rollback/manifest.json << 'EOF'
{
  "watchdog_target": "snapshot-1",
  "snapshots": []
}
EOF
```

The skills and projects subsystems each maintain their own per-target
`manifest.json` files, created automatically the first time a target is
snapshotted. Nothing to initialize up front.

---

## Step 6 — Copy All Scripts

Copy every file from this skill's `scripts/` directory into
`~/.openclaw/rollback/scripts/`. This includes:

**Shared utility:**
- `utils.mjs` — shared Node.js module (imported by all `.mjs` scripts)
- `detect-restart-command.mjs` — environment probe used at setup and any time
  the user migrates infrastructure and needs to re-detect

**Config subsystem (auto-restore watchdog target — unchanged behavior):**
- `snapshot.mjs`
- `restore.mjs`
- `restore-if-armed.mjs`
- `watchdog-set.mjs`
- `watchdog-extend.mjs`
- `watchdog-clear.mjs`
- `watchdog-status.mjs`
- `watchdog-timer.mjs`
- `recovery-test.mjs`

**Skills subsystem (manual only):**
- `skills-snapshot.mjs`
- `skills-list.mjs`
- `skills-restore.mjs`

**Projects subsystem (manual only):**
- `projects-snapshot.mjs`
- `projects-list.mjs`
- `projects-restore.mjs`

After copying, make the scripts executable:

```bash
chmod +x ~/.openclaw/rollback/scripts/*.mjs
```

The `.mjs` files have `#!/usr/bin/env node` shebangs, so once they have the
execute bit, the agent or startup scripts can call them directly without a
shell wrapper.

---

## Step 7 — Install Native OpenClaw Startup Hook

This ensures that if OpenClaw restarts while the config watchdog is armed,
the recovery check runs again natively inside OpenClaw on `gateway:startup`.

The hook only ever acts on config snapshots. Skills and projects are not
part of the auto-recovery pipeline.

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
- if watchdog is armed and not yet expired, the hook respawns
  `watchdog-timer.mjs` for the remaining time

This works the same way on pod, Docker, and local installs because it uses
OpenClaw's own native startup lifecycle instead of external schedulers.

---

## Step 8 — Confirm Setup Complete

```
✅ OpenClaw Recovery Manager installed.

Location: ~/.openclaw/rollback/
Restart command: <configured>
Scripts: Node.js (.mjs) — directly executable
Startup recovery: native OpenClaw hook `watchdog-recovery` on `gateway:startup`
                  (config subsystem only — skills and projects are manual)

Subsystems:
  • config     — auto-restore watchdog (dead-man's-switch)
  • skills     — manual snapshot/restore only
  • projects   — manual snapshot/restore only

Next step: say "create snapshot" to save your current known-good config
before making any changes.

Optional: say "test emergency recovery" to run a destructive test that
verifies the full config recovery pipeline works end-to-end.
```

---

## Reinstall / Reset

If the user wants to reinstall from scratch:
1. Back up existing snapshots:
   `cp -r ~/.openclaw/rollback/ /tmp/openclaw-rollback-backup/`
   (this preserves config, skills, and projects histories)
2. `rm -rf ~/.openclaw/rollback/`
3. Remove any old startup hook that points at a previous rollback install,
   if present.
4. Run setup again from Step 1.
5. Ask the user if they want their old snapshots restored from the backup.

Never silently delete snapshots — always back them up first and ask.
