---
name: openclaw-recovery-manager
description: >
  OpenClaw Configuration Management & Emergency Recovery — configuration, skills, 
  and projects snapshot &recovery for OpenClaw. Use this skill whenever the user 
  wants to take a backup, restore a backup, set a dead-man's-switch recovery timer 
  for config changes, or test the recovery pipeline. Trigger phrases include: "set
  emergency recovery", "create snapshot", "take a backup before changes", "set
  a backout timer", "restore snapshot", "accept changes", "test emergency
  recovery", "run recovery test", "snapshot all skills", "snapshot global
  skills", "snapshot <agent> skills", "list skills snapshots", "restore all
  skills", "restore <agent> skills", "snapshot all projects", "snapshot
  <project> project", "list project snapshots", "restore all projects",
  "restore <project> project", "how does the rollback work", "what rollback
  commands", or any variation of wanting to safely change OpenClaw config,
  skills, or project configuration with an automatic (config) or manual
  (skills/projects) recovery fallback. Also trigger when the user asks about
  recovery, rollback, emergency restore, or testing the recovery system in the
  context of OpenClaw. Manages three independent subsystems (config with
  automatic dead-man's-switch watchdog, skills manual, projects manual) sharing
  one change log. Uses only Node.js (already required by OpenClaw), tar, and
  gzip. No additional dependencies.
---

# OpenClaw Recovery Manager

*(Skill directory / install name kept as `openclaw-emergency-rollback` to
avoid breaking existing installations.)*

The Recovery Manager provides three independent snapshot/restore subsystems
for an OpenClaw install:

1. **Config** — root `openclaw.json` + agent & global workspace identity
   files. Has an automatic **dead-man's-switch watchdog** (detached Node
   timer plus a native `gateway:startup` hook) that auto-restores the most
   recent config snapshot if the user doesn't accept their changes in time.
   This is the original recovery system and its behavior is unchanged.
2. **Skills** — global skills at `~/.openclaw/skills/` plus each configured
   agent's skills directory. Each target keeps its own independent 3-slot
   history. Manual snapshots and restores only.
3. **Projects** — each project referenced from `~/.openclaw/openclaw.json`,
   captured as its local project-level manifest and state (not working
   content). Each project keeps its own independent 3-slot history. Manual
   snapshots and restores only.

All three subsystems write to the same change log at
`~/.openclaw/rollback/logs/change.log`.

**Only the config subsystem is ever auto-restored.** The watchdog timer and
`gateway:startup` hook never touch skills or projects.

All scripts are Node.js (`.mjs`), which is already installed as an OpenClaw
dependency. No additional packages needed.

---

## First-Time Setup

If `~/.openclaw/rollback/` does not exist, run setup before anything else.
Read `references/SETUP.md` now and follow it completely before proceeding.

**Critical setup rule:** the restart command must be **detected, not asked
for**. Users often don't know how their own OpenClaw install was deployed,
and guessing `kill -USR1 1` when the machine is actually running a systemd
service silently disables auto-recovery. Probe the environment
(`systemctl --user is-active openclaw-gateway`, `docker compose ps`, PID 1
identity) before asking. Only ask the user if probes produce no confident
match, and always state what was detected and why before storing.
`references/SETUP.md` Step 1 has the full detection algorithm.

---

## Important Note on `pkill` and Docker/K8s

If you are running OpenClaw as the primary process in a container (PID 1),
**do not use `pkill -f openclaw`** to restart the gateway. If you use a
background Dead Man's Switch, `pkill` will match the path name of the
background script and kill your rescue job instantly.

Instead, use **`kill -USR1 1`** to surgically send the reload signal directly
to the root OpenClaw process.

## Logical Sabotage vs Invalid JSON

OpenClaw protects itself from invalid JSON by instantly hot-reloading its last
known good config before the gateway even restarts. To test destructive
recovery properly, you must use **Logical Sabotage**: feeding OpenClaw
perfectly valid JSON that logically breaks routing (e.g., a dummy token like
64 `f`s and poisoned workspace paths). This proves the rollback recovers from
logical failure states.

---

## Restart recovery via native OpenClaw hook *(config only)*

When the config gets sabotaged and OpenClaw restarts, the detached
`watchdog-timer` may die with the old process tree. That is expected.

To make recovery survive pod/container/local restarts, this skill installs a
native OpenClaw managed hook at `~/.openclaw/hooks/watchdog-recovery/`
listening to `gateway:startup`.

On every gateway startup, the hook reads persistent
`~/.openclaw/rollback/watchdog.json`:
1. If rollback is not armed, it exits immediately.
2. If rollback is armed and the hard expiry epoch has already passed, it runs
   `restore-if-armed.mjs` immediately.
3. If rollback is armed and the hard expiry epoch has not passed yet, it
   respawns `watchdog-timer.mjs` for the remaining seconds.

Because the system stores a hard absolute epoch (`expiryEpoch`) on persistent
disk, it doesn't matter how long the restart took: if OpenClaw restarts after
expiry, the hook restores immediately; if it restarts before expiry, the hook
recreates the timer.

This is the native cross-environment trigger for pod, Docker, and local
machine restarts. No AI, internet, cron, or external supervisor is required.

**The watchdog and `gateway:startup` hook only ever act on CONFIG snapshots.**
Skills and projects are never auto-restored.

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
  • "list snapshots"            — show all saved config snapshots
  • "restore snapshot 2"        — manually restore snapshot 2 or 3
  • "create snapshot"           — save current state as new snapshot [1]
```

---

## Config Subsystem Commands

### "create snapshot [description]"
Save current OpenClaw config as the new known-good restore point.

1. Run: `~/.openclaw/rollback/scripts/snapshot.mjs "<description>" "<ai_summary>"`
2. Write an AI summary (1–2 sentences) of the current config state by reading
   `~/.openclaw/openclaw.json` — note the default model, number of agents,
   any notable tools or channels — and pass it as the second argument.
3. Reply with snapshot confirmation showing all current snapshots (max 3):

```
✅ Snapshot saved.
[1] Apr 20 2:30 PM — <description>  ← restore target
[2] Apr 19 9:00 AM — <previous label>
[3] Apr 18 4:00 PM — <oldest label>
```

Slot [1] is always the most recent. Slot [3] is always the oldest. When a 4th
snapshot would be created, slot [3] is overwritten as the others shift.
Snapshots are never deleted without the user explicitly creating a new one
that pushes the oldest out. If the user wants to preserve all three, they can
copy slot [3] before creating a new snapshot.

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

### "extend recovery XX minutes"
Add time to the active watchdog timer.

1. Run: `~/.openclaw/rollback/scripts/watchdog-extend.mjs <minutes>`
2. Reply with new expiry time and minutes remaining.

### "accept changes"
Disarm the watchdog — user is happy with the current config.

1. Run: `~/.openclaw/rollback/scripts/watchdog-clear.mjs`
2. Reply:

```
✅ Watchdog disarmed. Your changes are locked in.
Say "create snapshot" to save this config as your new restore point [1].
```

### "list snapshots"
Show all saved config snapshots.

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

### "restore snapshot [1|2|3]"
Manually restore a specific config snapshot immediately.

1. Confirm with user: "This will overwrite your current OpenClaw config with
   snapshot [N] '<label>' from <timestamp> and restart the gateway. Are you
   sure?"
2. On confirmation: run `~/.openclaw/rollback/scripts/restore.mjs <slot>`
3. Gateway restarts. Next session will detect uptime < 90 seconds.
4. If watchdog was armed, it is disarmed as part of restore.

### "test emergency recovery" / "run recovery test"
Run a destructive test of the full config recovery pipeline.

Read `references/TESTING.md` for the complete procedure. This test:
- Creates a dedicated test snapshot of the current config
- Arms a 2-minute watchdog
- Saves a manual recovery copy at `~/.openclaw/rollback/openclaw.recovery`
- Deliberately breaks `openclaw.json` to simulate a bad config change
- Restarts the gateway (which will fail to work properly)
- Waits for either the detached watchdog timer or the native
  `gateway:startup` hook to restore automatically

**This is destructive.** The user will lose access to their AI session for up
to 2 minutes while the test runs. Before running, confirm the user understands
the risks and has terminal/SSH access to manually recover if something goes
wrong.

---

## Skills Subsystem Commands *(manual only, never auto-restored)*

Skills targets are discovered dynamically from `~/.openclaw/openclaw.json` at
each snapshot. Each target (global + each configured agent) maintains its own
independent 3-slot history under `~/.openclaw/rollback/skills/<target>/`.

### "snapshot all skills [description]"
Snapshot global skills and every configured agent's skills simultaneously.
All targets receive the same user-provided description.

1. Run: `~/.openclaw/rollback/scripts/skills-snapshot.mjs all "<description>"`
2. Reply with a per-target result list.

### "snapshot global skills [description]"
Snapshot only `~/.openclaw/skills/`.

1. Run: `~/.openclaw/rollback/scripts/skills-snapshot.mjs global "<description>"`

### "snapshot <agent> skills [description]"
Snapshot a single agent's skills directory.

1. Run: `~/.openclaw/rollback/scripts/skills-snapshot.mjs <agent-id> "<description>"`

### "list skills snapshots"
Show every skills target with its 3-slot history.

1. Run: `~/.openclaw/rollback/scripts/skills-list.mjs`

### "list global skills snapshots" / "list <agent> skills snapshots"
Show the 3-slot history for a single target.

1. Run: `~/.openclaw/rollback/scripts/skills-list.mjs global`
   or `~/.openclaw/rollback/scripts/skills-list.mjs <agent-id>`

### "restore all skills"
Restore each target's slot 1 independently.

1. Run: `~/.openclaw/rollback/scripts/skills-restore.mjs all`

### "restore global skills [snapshot N]" / "restore <agent> skills [snapshot N]"
Restore slot 1 (default) or a specific slot for a single target.

1. Run: `~/.openclaw/rollback/scripts/skills-restore.mjs global [N]`
   or `~/.openclaw/rollback/scripts/skills-restore.mjs <agent-id> [N]`

**Skills snapshots are never auto-restored by the recovery timer or the
`gateway:startup` hook.** They do not arm the watchdog and the watchdog never
touches them.

---

## Projects Subsystem Commands *(manual only, never auto-restored)*

Project paths are discovered dynamically from `~/.openclaw/openclaw.json` at
each snapshot. Each project keeps its own 3-slot history under
`~/.openclaw/rollback/projects/<project>/`.

### "snapshot all projects [description]"
Snapshot every configured project. All receive the same description.

1. Run: `~/.openclaw/rollback/scripts/projects-snapshot.mjs all "<description>"`

### "snapshot <project name> project [description]"
Snapshot a single project.

1. Run: `~/.openclaw/rollback/scripts/projects-snapshot.mjs <project> "<description>"`

### "list project snapshots"
Show every project with its 3-slot history.

1. Run: `~/.openclaw/rollback/scripts/projects-list.mjs`

### "list <project name> snapshots"
Show the 3-slot history for a single project.

1. Run: `~/.openclaw/rollback/scripts/projects-list.mjs <project>`

### "restore all projects"
Restore each project's slot 1 independently.

1. Run: `~/.openclaw/rollback/scripts/projects-restore.mjs all`

### "restore <project name> project [snapshot N]"
Restore slot 1 (default) or a specific slot.

1. Run: `~/.openclaw/rollback/scripts/projects-restore.mjs <project> [N]`

**Projects snapshots are never auto-restored by the recovery timer or the
`gateway:startup` hook.**

---

## What Gets Backed Up

### Config snapshots (auto-restore target)
| File | Path |
|------|------|
| Master config | `~/.openclaw/openclaw.json` |
| Global workspace identity files | `~/.openclaw/workspace/*.md` *(whole-glob: SOUL.md, AGENTS.md, any new .md)* |
| Per-agent workspace files | `<agent_workspace>/SOUL.md` |
| | `<agent_workspace>/AGENTS.md` |
| | `<agent_workspace>/USER.md` |
| | `<agent_workspace>/IDENTITY.md` |
| | `<agent_workspace>/TOOLS.md` |
| | `<agent_workspace>/HEARTBEAT.md` |
| | `<agent_workspace>/BOOT.md` *(if present)* |

Workspace paths and agentIds are read dynamically from `openclaw.json` at
snapshot time — covers all configured agents automatically.

**Never captured by config snapshots:** credentials/, auth-profiles.json,
session history, memory logs, workspace content files, .env, Docker/K8s
environment config.

### Skills snapshots (manual only)
- `~/.openclaw/skills/` (global)
- Each configured agent's skills directory (from the agent's `skills` field,
  or `<agent_workspace>/skills/` if no explicit field)

### Project snapshots (manual only) — per project folder
| Item | Notes |
|------|-------|
| `openclaw.json` | project-local manifest & MCP spawn instructions |
| `mcp_config.json` | tool bridge to external services |
| `package.json` | local MCP server dependencies |
| `TASKS.json`, `PROCESSES.json`, `SPRINT_CURRENT.json` | state files, if present |
| `./tools/` | local MCP server source scripts |
| `./skills/` | project-local skills |
| `.openclaw/workspace.state.json` | project structural state |
| `./comms/` | **directory tree structure ONLY, no file content** |

**Explicitly excluded from project snapshots:**
- `node_modules/`
- `memory/`
- `auth-profiles.json`
- `~/.openclaw/` root (already covered by config snapshots)
- All working content, repositories, large data files, .env

---

## "how does the rollback work" / "what commands can I use" / "explain recovery manager"

Respond with this explanation:

```
OpenClaw Recovery Manager — How It Works

Three independent snapshot/restore subsystems sharing one change log.

1. CONFIG (with auto-restore watchdog — the original dead-man's-switch)
   "create snapshot [description]"       — save current config as restore point
   "set emergency recovery XX minutes"   — arm the auto-restore timer
   "extend recovery XX minutes"          — add time to active timer
   "accept changes"                      — disarm timer, keep current config
   "list snapshots"                      — show all 3 saved config snapshots
   "restore snapshot [1|2|3]"            — manually restore a specific snapshot
   "test emergency recovery"             — destructive test of the full pipeline

   If the user doesn't accept config changes before the timer fires, the
   system auto-restores snapshot [1] and restarts OpenClaw — no AI, no
   network, no user intervention required.

2. SKILLS (manual only — no auto-restore, no watchdog involvement)
   "snapshot all skills [description]"
   "snapshot global skills [description]"
   "snapshot <agent> skills [description]"
   "list skills snapshots"
   "list global skills snapshots" / "list <agent> skills snapshots"
   "restore all skills"
   "restore global skills [snapshot N]"
   "restore <agent> skills [snapshot N]"

3. PROJECTS (manual only — no auto-restore, no watchdog involvement)
   "snapshot all projects [description]"
   "snapshot <project> project [description]"
   "list project snapshots"
   "list <project> snapshots"
   "restore all projects"
   "restore <project> project [snapshot N]"

Each target (config / each skill target / each project) keeps its own
independent 3-slot history. Slot [1] is always most recent, slot [3] oldest;
a 4th snapshot pushes slot [3] out.

The auto-restore watchdog is CONFIG ONLY. It never touches skills or
projects.

Dependencies: Node.js (already installed with OpenClaw), tar, gzip.
```

---

## Change Log

Append to `~/.openclaw/rollback/logs/change.log` whenever any of the
following happens in any subsystem:
- A snapshot is taken (config, skills, or project)
- The watchdog is armed, extended, or cleared *(config only)*
- The user requests a gateway restart (note what changed and watchdog status)
- The gateway restart is confirmed complete
- A recovery test is started or completed
- A skills or project restore is run

Format:
```
[YYYY-MM-DD HH:MM:SS] <EVENT TYPE>
  <key: value details>
---
```

---

## Reference Files

- `references/SETUP.md` — Read this first if `~/.openclaw/rollback/` does not exist
- `references/TESTING.md` — Destructive recovery test procedure (config subsystem)
- `references/RESTORE.md` — Manual recovery instructions requiring no AI or scripts
- `scripts/` — Node.js scripts (`.mjs`) — no shell wrappers needed
- `hooks/watchdog-recovery/` — Native OpenClaw startup hook for config restart recovery
