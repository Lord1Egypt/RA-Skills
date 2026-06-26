---
name: openclaw-emergency-rollback/restore
description: Manual recovery instructions for OpenClaw Recovery Manager — restore config, skills, or project snapshots without AI, scripts, or network access. For use when everything is broken.
---

# Manual Recovery — No AI Required

Use this document if you have shell access but cannot use AI, the scripts
failed, or you want to manually restore a specific snapshot.

You need: a terminal, basic shell access, `tar` + `gzip`, and (for config
restore) the ability to run one command to restart OpenClaw.

All Recovery Manager archives are `tar.gz` files with absolute paths inside,
so extracting them with `tar -xzf ... -C /` puts every file back exactly
where it came from.

---

## Config Snapshots (auto-restore target)

### Step 1 — Find Your Config Snapshots

```bash
ls -lh ~/.openclaw/rollback/snapshots/
```

You will see up to three files:
- `snapshot-1.tar.gz` — most recent user-approved snapshot
- `snapshot-2.tar.gz` — second most recent
- `snapshot-3.tar.gz` — oldest

To see labels and timestamps:

```bash
node -e "
const m=require(process.env.HOME+'/.openclaw/rollback/manifest.json');
m.snapshots.forEach(s=>console.log('['+s.slot+'] '+s.label+' ('+s.timestamp+')'));
"
```

Or read the raw file: `cat ~/.openclaw/rollback/manifest.json`

### Step 2 — Restore the Snapshot

Replace `snapshot-1.tar.gz` with whichever snapshot you want:

```bash
tar -xzf ~/.openclaw/rollback/snapshots/snapshot-1.tar.gz -C /
```

This restores all files to their exact original paths:
- `~/.openclaw/openclaw.json`
- `~/.openclaw/workspace/*.md` (global workspace identity files)
- All per-agent workspace files (SOUL.md, AGENTS.md, etc.)

No path mapping needed — the archive preserves full absolute paths.

### Step 3 — Restart OpenClaw

Check what restart command was configured:

```bash
cat ~/.openclaw/rollback/rollback-config.json
```

Look for `"restartCommand"` and run it. Examples:

```bash
kill -USR1 1
systemctl --user restart openclaw-gateway
docker compose restart
docker compose down && docker compose up -d
```

### Step 4 — Verify

```bash
openclaw gateway status
```

You should see the gateway as active and running.

### Step 5 — Disarm the Watchdog (if still armed)

If the detached watchdog timer might still be running, disarm it so it
doesn't fire again:

```bash
# Stop any detached watchdog timer processes
pkill -f watchdog-timer.mjs || true

# Mark watchdog as disarmed
node -e "
const fs=require('fs');
const wf=process.env.HOME+'/.openclaw/rollback/watchdog.json';
const w=JSON.parse(fs.readFileSync(wf,'utf8'));
w.armed=false;
fs.writeFileSync(wf,JSON.stringify(w,null,2));
console.log('Watchdog disarmed.');
"
```

### If You Have a Recovery File

If a recovery test was run, there may be a clean config backup at:

```bash
ls -lh ~/.openclaw/rollback/openclaw.recovery
```

If this file exists and your snapshots are corrupted or missing:

```bash
cp ~/.openclaw/rollback/openclaw.recovery ~/.openclaw/openclaw.json
```

Then restart as described above.

---

## Skills Snapshots (manual subsystem)

### Find Your Skills Snapshots

```bash
ls ~/.openclaw/rollback/skills/
```

You'll see one subfolder per target — `global`, plus one per configured
agent. Each subfolder is an independent 3-slot history.

To see the history for a specific target:

```bash
cat ~/.openclaw/rollback/skills/global/manifest.json
cat ~/.openclaw/rollback/skills/<agent-id>/manifest.json
```

### Restore a Skills Snapshot

```bash
# Restore global skills slot 1
tar -xzf ~/.openclaw/rollback/skills/global/snapshot-1.tar.gz -C /

# Restore an agent's skills slot 2
tar -xzf ~/.openclaw/rollback/skills/<agent-id>/snapshot-2.tar.gz -C /
```

Skills restore does **not** require a gateway restart and does **not** touch
the watchdog.

---

## Project Snapshots (manual subsystem)

### Find Your Project Snapshots

```bash
ls ~/.openclaw/rollback/projects/
```

One subfolder per project. Each subfolder is an independent 3-slot history.

```bash
cat ~/.openclaw/rollback/projects/<project-name>/manifest.json
```

### Restore a Project Snapshot

```bash
# Restore project slot 1
tar -xzf ~/.openclaw/rollback/projects/<project-name>/snapshot-1.tar.gz -C /

# Restore project slot 3 (oldest)
tar -xzf ~/.openclaw/rollback/projects/<project-name>/snapshot-3.tar.gz -C /
```

This restores project-local manifests and state (not working content):
`openclaw.json`, `mcp_config.json`, `package.json`, state files, `tools/`,
`skills/`, `.openclaw/workspace.state.json`, and the `comms/` directory
tree structure. Working content, `node_modules/`, and `memory/` are not
included.

Project restore does **not** require a gateway restart and does **not** touch
the root config or the watchdog.

---

## Logs

```bash
cat ~/.openclaw/rollback/logs/restore.log    # automated restore history
cat ~/.openclaw/rollback/logs/change.log     # all changes across all subsystems
```

---

## Summary (Quickest Paths)

### Config (most common emergency)
```bash
# 1. Restore snapshot
tar -xzf ~/.openclaw/rollback/snapshots/snapshot-1.tar.gz -C /

# 2. Restart (use your actual command)
kill -USR1 1

# 3. Disarm watchdog timer
pkill -f watchdog-timer.mjs || true
```

### Skills
```bash
tar -xzf ~/.openclaw/rollback/skills/<target>/snapshot-1.tar.gz -C /
```

### Project
```bash
tar -xzf ~/.openclaw/rollback/projects/<project>/snapshot-1.tar.gz -C /
```

That's it.
