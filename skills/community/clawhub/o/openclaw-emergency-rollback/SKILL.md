---
name: openclaw-emergency-rollback
description: >
  OpenClaw Emergency Config Rollback — dead man's switch system for safely making
  risky changes to OpenClaw configuration. Use this skill whenever the user mentions
  wanting to make changes to openclaw.json or agent configs and wants a safety net,
  says anything like "set emergency recovery", "create a snapshot", "take a backup
  before changes", "set a backout timer", "restore snapshot", "accept changes",
  "test emergency recovery", "run recovery test", "how does the rollback work",
  "what rollback commands", or any variation of wanting to safely change OpenClaw
  config with an automatic recovery fallback. Also trigger when the user asks about
  recovery, rollback, emergency restore, or testing the recovery system in the
  context of OpenClaw. This skill manages the full lifecycle: snapshots, watchdog
  timers, auto-restore, post-restart reminders, and destructive testing
  of the recovery pipeline — all without requiring AI, network, or user intervention
  once the timer is set. Uses only Node.js (already required by OpenClaw), zip,
  and unzip. No additional dependencies to install.
---

# OpenClaw Emergency Config Rollback

A dead man's switch system for OpenClaw configuration changes. The user takes a
snapshot of known-good config, sets a recovery timer, makes changes, and if they
don't accept the changes before the timer expires the system automatically restores
the last snapshot — with zero AI, zero network, zero user intervention required.

All scripts are Node.js (`.mjs`), which is already installed as an OpenClaw
dependency. No additional packages needed. The system uses detached Node.js timers
plus a native OpenClaw `gateway:startup` hook that re-checks persistent watchdog
state on every gateway restart rather than relying on external schedulers that often fail
in containerized environments.

---

## First-Time Setup

If `~/.openclaw/rollback/` does not exist, run setup before anything else.
Read `references/SETUP.md` now and follow it completely before proceeding.

---

## Important Note on `pkill` and Docker/K8s

If you are running OpenClaw as the primary process in a container (PID 1), **do not use `pkill -f openclaw`** to restart the gateway. If you use a background Dead Man's Switch, `pkill` will match the path name of the background script and kill your rescue job instantly.

Instead, use **`kill -USR1 1`** to surgically send the reload signal directly to the root OpenClaw process.

## Logical Sabotage vs Invalid JSON
OpenClaw protects itself from invalid JSON by instantly hot-reloading its last known good config before the gateway even restarts. To test destructive recovery properly, you must use **Logical Sabotage**: feeding OpenClaw perfectly valid JSON that logically breaks routing (e.g., a dummy token like 64 `f`s and poisoned workspace paths). This proves the rollback recovers from logical failure states.

---

## Restart recovery via native OpenClaw hook

When the config gets sabotaged and OpenClaw restarts, the detached `watchdog-timer`
may die with the old process tree. That is expected.

To make recovery survive pod/container/local restarts, this skill installs a native
OpenClaw managed hook at `~/.openclaw/hooks/watchdog-recovery/` listening to
`gateway:startup`.

On every gateway startup, the hook reads persistent `~/.openclaw/rollback/watchdog.json`:
1. If rollback is not armed, it exits immediately.
2. If rollback is armed and the hard expiry epoch has already passed, it runs
   `restore-if-armed.mjs` immediately.
3. If rollback is armed and the hard expiry epoch has not passed yet, it respawns
   `watchdog-timer.mjs` for the remaining seconds.

Because the system stores a hard absolute epoch (`expiryEpoch`) on persistent disk,
it doesn't matter how long the restart took: if OpenClaw restarts after expiry, the hook
restores immediately; if it restarts before expiry, the hook recreates the timer.

This is the native cross-environment trigger for pod, Docker, and local machine restarts.
No AI, internet, cron, or external supervisor is required.

---

## Session Start — Uptime Check (Run Every Session)

At the start of every session, run:

```bash
UPTIME=$(systemctl --user show openclaw-gateway \
  --property=ActiveEnterTimestampMonotonic 2>/dev/null \
  | awk -F= '{if($2>0) print int((systime()*1000000-$2)/1000000); else print 999}')

if [ "$UPTIME" = "999" ]; then
  UPTIME=$(ps -o etimes= -p $(pgrep -f "openclaw" 2>/dev/null) 2>/dev/null | tr -d ' ')
fi
```

If uptime is under 90 seconds AND `~/.openclaw/rollback/watchdog.json` exists
and shows `"armed": true`, the gateway just bounced. Open the session with the
**Watchdog Reminder** (see below).

If armed but uptime is over 90 seconds, still check and remind — the user may
have connected to a running session mid-timer.

If `armed: false` or watchdog file doesn't exist, start the session normally.

---

## Watchdog Reminder (show when watchdog is armed)

Run `~/.openclaw/rollback/scripts/watchdog-status.mjs` and display:

```
⚠️  Emergency recovery is armed.

Snapshot [1] "<label>" will auto-restore in ~XX minutes
unless you accept or extend.

Commands:
  • "accept changes"            — disarm watchdog, lock in current config
  • "extend recovery XX minutes" — add more time to the timer
  • "list snapshots"            — show all saved snapshots
  • "restore snapshot 2"        — manually restore snapshot 2 or 3
  • "create snapshot"           — save current state as new snapshot [1]
```

---

## User Commands Reference

### "create snapshot [description]"
Save current OpenClaw config as the new known-good restore point.

1. Run: `~/.openclaw/rollback/scripts/snapshot.mjs "<description>" "<ai_summary>"`
2. Write an AI summary (1–2 sentences) of the current config state by reading
   `~/.openclaw/openclaw.json` — note the default model, number of agents, any
   notable tools or channels — and pass it as the second argument
3. Reply with snapshot confirmation showing all current snapshots (max 3):

```
✅ Snapshot saved.
[1] Apr 20 2:30 PM — <description>  ← restore target
[2] Apr 19 9:00 AM — <previous label>
[3] Apr 18 4:00 PM — <oldest label>
```

Slot [1] is always the most recent. Slot [3] is always the oldest.
When a 4th snapshot would be created, slot [3] is overwritten as the others
shift. Snapshots are never deleted without the user explicitly creating a new
one that pushes the oldest out. If the user wants to preserve all three, they
can copy slot [3] before creating a new snapshot.

---

### "set emergency recovery XX minutes" / "start emergency recovery XX minutes"
Arm the watchdog dead man's switch.

1. Run: `~/.openclaw/rollback/scripts/watchdog-set.mjs <minutes>`
2. Reply:

```
⏱️ Watchdog armed — XX minutes.
Snapshot [1] "<label>" auto-restores at <HH:MM> if not accepted.
Make your changes whenever you're ready.
```

If no snapshot exists yet, tell the user to create one first before arming.

---

### "extend recovery XX minutes"
Add time to the active watchdog timer.

1. Run: `~/.openclaw/rollback/scripts/watchdog-extend.mjs <minutes>`
2. Reply with new expiry time and minutes remaining.

---

### "accept changes"
Disarm the watchdog — user is happy with the current config.

1. Run: `~/.openclaw/rollback/scripts/watchdog-clear.mjs`
2. Reply:

```
✅ Watchdog disarmed. Your changes are locked in.
Say "create snapshot" to save this config as your new restore point [1].
```

---

### "list snapshots"
Show all saved snapshots.

Read `~/.openclaw/rollback/manifest.json` and display:

```
Saved snapshots (most recent first):
[1] Apr 20 2:30 PM — "opus model working, github tool added"
    Config: claude-opus-4 default, 2 agents (main, coding), github MCP active
[2] Apr 19 9:00 AM — "initial clean setup"
    Config: claude-sonnet-4 default, 1 agent (main), no extra tools
[3] Apr 18 4:00 PM — "baseline before any changes"
    Config: claude-haiku-4 default, 1 agent (main)

Restore target: [1] (auto-restored if watchdog fires)
Watchdog: ARMED — 14m 32s remaining  [or: NOT ARMED]
```

---

### "restore snapshot [1|2|3]"
Manually restore a specific snapshot immediately.

1. Confirm with user: "This will overwrite your current OpenClaw config with
   snapshot [N] '<label>' from <timestamp> and restart the gateway. Are you sure?"
2. On confirmation: run `~/.openclaw/rollback/scripts/restore.mjs <slot>`
3. Gateway restarts. Next session will detect uptime < 90 seconds.
4. If watchdog was armed, it is disarmed as part of restore.

---

### "test emergency recovery" / "run recovery test"
Run a destructive test of the full recovery pipeline.

Read `references/TESTING.md` for the complete procedure. This test:
- Creates a dedicated test snapshot of the current config
- Arms a 2-minute watchdog
- Saves a manual recovery copy at `~/.openclaw/rollback/openclaw.recovery`
- Deliberately breaks `openclaw.json` to simulate a bad config change
- Restarts the gateway (which will fail to work properly)
- Waits for either the detached watchdog timer or the native `gateway:startup` hook to restore automatically

**This is destructive.** The user will lose access to their AI session for up
to 2 minutes while the test runs. Before running, confirm the user understands
the risks and has terminal/SSH access to manually recover if something goes wrong.

---

### "how does the rollback work" / "what commands can I use" / "explain emergency rollback"

Respond with this explanation:

```
OpenClaw Emergency Rollback — How It Works

This skill gives you a safety net for risky config changes. Here's the flow:

1. SNAPSHOT — Before making changes, say:
   "create snapshot — [describe what's working]"
   This saves your current openclaw.json and all agent workspace config files
   (SOUL.md, AGENTS.md, IDENTITY.md, etc.) as a restore point. You can have
   up to 3 snapshots. Snapshot [1] is always your most recent.

2. ARM THE TIMER — When ready to make changes, say:
   "set emergency recovery 30 minutes"
   This starts a countdown. If you don't accept the changes in time, the
   system automatically restores snapshot [1] and restarts OpenClaw — even
   if AI is offline, the server rebooted, or nothing is working.

3. MAKE CHANGES — Edit config, restart the gateway, whatever you need to do.

4. ACCEPT OR RECOVER —
   • If everything works: say "accept changes" to disarm the timer.
   • If something broke and you can't get back in: do nothing. The timer
     fires automatically and restores your last known-good config.
   • If you need more time: say "extend recovery 20 minutes".

Commands:
  "create snapshot [description]"       — save current config as restore point
  "set emergency recovery XX minutes"   — arm the auto-restore timer
  "extend recovery XX minutes"          — add time to active timer
  "accept changes"                      — disarm timer, keep current config
  "list snapshots"                      — show all 3 saved snapshots
  "restore snapshot [1|2|3]"            — manually restore a specific snapshot
  "test emergency recovery"             — destructive test of the full pipeline

The watchdog uses two native local paths:
- a detached background Node timer for the live happy path
- a native OpenClaw `gateway:startup` hook for restart recovery

No external scheduler, no AI, no internet, no anything else required.
On every gateway restart, the startup hook verifies whether the hard epoch timer
expired while OpenClaw was down and restores if so. If it hasn't expired yet,
it respawns a fresh timer to finish the countdown.

Dependencies: Node.js (already installed with OpenClaw), zip, unzip.
```

---

## What Gets Backed Up

Every snapshot captures exactly these files — no more, no less:

| File | Path |
|------|------|
| Master config | `~/.openclaw/openclaw.json` |
| Agent workspace files (per agent) | `<workspace>/SOUL.md` |
| | `<workspace>/AGENTS.md` |
| | `<workspace>/USER.md` |
| | `<workspace>/IDENTITY.md` |
| | `<workspace>/TOOLS.md` |
| | `<workspace>/HEARTBEAT.md` |
| | `<workspace>/BOOT.md` (if present) |


Workspace paths and agentIds are read dynamically from `openclaw.json` at
snapshot time — covers all configured agents automatically.

**Never captured:** credentials/, auth-profiles.json, session history, memory
logs, workspace content files, .env, Docker/K8s environment config.

---

## Change Log

Append to `~/.openclaw/rollback/logs/change.log` when:
- A snapshot is taken
- The watchdog is armed, extended, or cleared
- The user requests a gateway restart (note what changed and watchdog status)
- The gateway restart is confirmed complete
- A recovery test is started or completed

Format:
```
[YYYY-MM-DD HH:MM:SS] <EVENT TYPE>
  <key: value details>
---
```

---

## Reference Files

- `references/SETUP.md` — Read this first if `~/.openclaw/rollback/` does not exist
- `references/TESTING.md` — Destructive recovery test procedure and manual fallback
- `references/RESTORE.md` — Manual recovery instructions requiring no AI or scripts
- `scripts/` — Node.js scripts (`.mjs`) — no shell wrappers needed
- `hooks/watchdog-recovery/` — Native OpenClaw startup hook for restart recovery
