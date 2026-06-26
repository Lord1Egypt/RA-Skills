---
name: openclaw-emergency-rollback/restore
description: Manual recovery instructions for restoring OpenClaw config without AI, scripts, or network access. For use when everything is broken.
---

# Manual Recovery — No AI Required

Use this document if you have shell access but cannot use AI, the scripts
failed, or you want to manually restore a specific snapshot.

You need: a terminal, basic shell access, `unzip`, and the ability to run
one command to restart OpenClaw.

---

## Step 1 — Find Your Snapshots

```bash
ls -lh ~/.openclaw/rollback/snapshots/
```

You will see up to three files:
- `snapshot-1.zip` — most recent user-approved snapshot
- `snapshot-2.zip` — second most recent
- `snapshot-3.zip` — oldest

To see labels and timestamps:

```bash
node -e "
const m=require(process.env.HOME+'/.openclaw/rollback/manifest.json');
m.snapshots.forEach(s=>console.log('['+s.slot+'] '+s.label+' ('+s.timestamp+')'));
"
```

Or just read the raw file: `cat ~/.openclaw/rollback/manifest.json`

---

## Step 2 — Restore the Snapshot

Replace `snapshot-1.zip` with whichever snapshot you want:

```bash
unzip -o ~/.openclaw/rollback/snapshots/snapshot-1.zip -d /
```

This restores all files to their exact original paths:
- `~/.openclaw/openclaw.json`
- All agent workspace files (SOUL.md, AGENTS.md, etc.)

No path mapping needed — the zip preserves full absolute paths.

---

## Step 3 — Restart OpenClaw

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

---

## Step 4 — Verify

```bash
openclaw gateway status
```

You should see the gateway as active and running.

---

## Step 5 — Disarm the Watchdog (if still armed)

If the detached watchdog timer might still be running, disarm it so it doesn't fire again:

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

---

## If You Have a Recovery File

If a recovery test was run, there may be a clean config backup at:

```bash
ls -lh ~/.openclaw/rollback/openclaw.recovery
```

If this file exists and your snapshots are corrupted or missing:

```bash
cp ~/.openclaw/rollback/openclaw.recovery ~/.openclaw/openclaw.json
```

Then restart as described in Step 3.

---

## Logs

```bash
cat ~/.openclaw/rollback/logs/restore.log    # automated restore history
cat ~/.openclaw/rollback/logs/change.log     # all changes, snapshots, watchdog events
```

---

## Summary (Quickest Path)

```bash
# 1. Restore snapshot
unzip -o ~/.openclaw/rollback/snapshots/snapshot-1.zip -d /

# 2. Restart (use your actual command)
kill -USR1 1

# 3. Disarm watchdog timer
pkill -f watchdog-timer.mjs || true
```

That's it.
