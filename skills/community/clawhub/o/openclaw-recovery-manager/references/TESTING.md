---
name: openclaw-emergency-rollback/testing
description: Destructive recovery test procedure for the OpenClaw Recovery Manager config subsystem. Read this when the user wants to test that the emergency rollback system actually works end-to-end.
---

# Emergency Recovery Test — Destructive (Config Subsystem)

This test verifies the full **config** recovery pipeline by deliberately
breaking the OpenClaw config and confirming the watchdog automatically
restores it.

Skills and projects are NOT part of this test. They are manual-only
subsystems and have no auto-restore to verify.

**This test is destructive.** During the test window (up to ~2 minutes), the
user's OpenClaw gateway will be non-functional. AI sessions, agents, and any
active connections will be interrupted.

---

## Before You Begin — Pre-Flight Checklist

Confirm ALL of these with the user before proceeding:

```
⚠️  Emergency Recovery Test — Pre-Flight Checklist

This test will:
  1. Save your current config as a test snapshot
  2. Save a manual recovery copy of openclaw.json
  3. Deliberately break your openclaw.json (logical sabotage)
  4. Restart the gateway (it will fail)
  5. Wait for the watchdog to auto-restore (~2 minutes)

During the test you WILL lose access to your AI session.

Requirements:
  □ You have terminal/SSH access to this machine right now
  □ You can run commands even if the AI agent is offline
  □ You understand this will interrupt all active sessions

Manual recovery command (if the test fails — keep this visible):
  cp ~/.openclaw/rollback/openclaw.recovery ~/.openclaw/openclaw.json
  <your restart command here>

Type "yes, run the test" to proceed.
```

Fill in the actual restart command from
`~/.openclaw/rollback/rollback-config.json`.

Do NOT proceed unless the user explicitly confirms.

---

## Test Procedure

### Step 1 — Verify Dependencies

```bash
~/.openclaw/rollback/scripts/recovery-test.mjs preflight
```

This checks that node, tar, and gzip are available, that the rollback
directory is properly initialized, and that all config-subsystem scripts are
present. If anything fails, stop and fix it before continuing.

### Step 2 — Create Test Snapshot

```bash
~/.openclaw/rollback/scripts/snapshot.mjs "pre-test known-good config" "Snapshot taken before recovery test."
```

This saves the current working config as snapshot [1].

### Step 3 — Save Manual Recovery Copy

```bash
~/.openclaw/rollback/scripts/recovery-test.mjs save-recovery
```

This copies `openclaw.json` to `~/.openclaw/rollback/openclaw.recovery`.
This is the user's last-resort manual recovery if everything else fails.

Tell the user:

```
📋 Manual recovery copy saved. If the test fails and the watchdog does not
restore your config within 5 minutes, run these two commands from any terminal:

  cp ~/.openclaw/rollback/openclaw.recovery ~/.openclaw/openclaw.json
  <restart command>

Keep this window open or write these commands down before proceeding.
```

### Step 4 — Arm the Watchdog (2 minutes)

```bash
~/.openclaw/rollback/scripts/watchdog-set.mjs 2
```

The watchdog is now armed. If nothing disarms it in 2 minutes, it will
automatically restore snapshot [1] and restart the gateway.

### Step 5 — Break the Config (logical sabotage)

```bash
~/.openclaw/rollback/scripts/recovery-test.mjs sabotage
```

This poisons the gateway auth token (64 `f`s) and modifies agent workspace
paths. The file remains valid JSON — so it gets past OpenClaw's invalid-JSON
auto-revert — but the gateway cannot route correctly. This is the correct
failure mode to exercise the watchdog.

### Step 6 — Restart the Gateway

Read the restart command from rollback-config.json and run it:

```bash
RESTART_CMD=$(node -e "console.log(require('$HOME/.openclaw/rollback/rollback-config.json').restartCommand)")
eval "$RESTART_CMD"
```

The gateway will attempt to start, load the poisoned-but-valid config, and
run in a broken routing state. This is expected.

### Step 7 — Wait for Recovery

The detached watchdog timer can fire at expiry, and the native
`gateway:startup` hook can recover on restart if the timer died. Combined
with restart/setup overhead, recovery should usually happen within ~2-3
minutes. The user should:

1. Wait 3 minutes
2. Try to connect to their agent
3. If the agent is back and working, the test passed

To verify programmatically:

```bash
~/.openclaw/rollback/scripts/recovery-test.mjs verify
```

### Step 8 — Report Results

If the config is restored and the gateway is running:

```
✅ Recovery test PASSED.

The watchdog detected the expired timer, restored snapshot [1],
and restarted the gateway automatically.

Your manual recovery copy is still at:
  ~/.openclaw/rollback/openclaw.recovery
You can delete it or keep it as an extra backup.
```

If the config was NOT restored after 5 minutes:

```
❌ Recovery test FAILED.

The watchdog did not fire. Possible causes:
  • the detached watchdog timer process never started
  • `watchdog-timer.mjs` was killed unexpectedly
  • the native `watchdog-recovery` hook is not installed/enabled
  • the startup hook ran but failed before invoking `restore-if-armed.mjs`

To restore manually:
  cp ~/.openclaw/rollback/openclaw.recovery ~/.openclaw/openclaw.json
  <restart command>

Check the logs:
  cat ~/.openclaw/rollback/logs/restore.log
  cat ~/.openclaw/rollback/logs/change.log
```

---

## What the Test Validates

1. **Snapshot creation** — config files are captured and archived correctly
2. **Watchdog arming** — detached timer started with correct expiry
3. **Startup hook recovery** — native `gateway:startup` hook re-checks
   persistent watchdog state after restart
4. **Timer expiry detection** — restore-if-armed.mjs checks epoch against
   expiry
5. **Restore execution** — archive extracted to correct paths, overwriting
   broken files
6. **Gateway restart** — restart command fires after restore
7. **Watchdog disarm** — watchdog state cleared after firing

A full destructive test should exercise both timer-path and startup-hook
recovery evidence in `restore.log`.

**This test deliberately does NOT touch skills or projects.** Those
subsystems are manual-only and do not participate in the auto-restore
pipeline.

---

## Cleaning Up After a Failed Test

If the automatic recovery didn't fire:

```bash
# 1. Restore the config
cp ~/.openclaw/rollback/openclaw.recovery ~/.openclaw/openclaw.json

# 2. Restart the gateway (use your actual command)
kill -USR1 1

# 3. Disarm the watchdog timer so it doesn't fire later
pkill -f watchdog-timer.mjs || true

# 4. Mark watchdog as disarmed
node -e "
const fs=require('fs');
const wf=process.env.HOME+'/.openclaw/rollback/watchdog.json';
const w=JSON.parse(fs.readFileSync(wf,'utf8'));
w.armed=false;
fs.writeFileSync(wf,JSON.stringify(w,null,2));
console.log('Watchdog disarmed.');
"

# 5. Verify
cat ~/.openclaw/openclaw.json | node -e "JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'));console.log('Config is valid JSON')"
```
