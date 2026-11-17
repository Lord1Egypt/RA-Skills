---
name: macos-memory-triage
description: Diagnose why a Mac (especially one running Claude Code, other AI coding tools, or several Electron-based IDEs at once) is slow, hanging, or freezing due to memory pressure and swap thrashing. Covers reading real swap/memory numbers, finding MCP-server and plugin process bloat, spotting orphaned or duplicate background processes, safely clearing regenerable caches, and recognizing when a killed process keeps respawning because something else supervises it. Use this whenever the user says their Mac/MacBook is slow, laggy, hanging, freezing, "using too much memory," has "high memory pressure," or asks to find/stop/kill whatever is eating RAM or CPU. Every fix in this skill is reversible (stop, kill, disable, clear cache) — it never deletes or uninstalls anything, and it says so explicitly before running anything.
---

# macOS memory triage

## Read this first: safety framing

This skill inspects live system state and then stops or disables things. That second part is real — it changes what's running on the machine. Because of that:

- **Run this only in a mode where every command is shown and manually approved before it executes** (e.g. Claude Code's default "ask before running" mode, or an explicit "accept edits" review step). Do not run this skill's remediation commands in a fully autonomous/auto-approve mode. PIDs and process names are only meaningful in the moment they were captured — a stale PID reused by an unrelated process is a real (if rare) risk, and a human glance at the `ps` line before a `kill` is cheap insurance against it.
- **Never kill a PID you haven't shown the user first.** Always print the full `ps` line for a process (command, args, start time) immediately before killing it, so the person approving the command knows what they're actually stopping.
- **Hard boundary — nothing in this skill is allowed to be irreversible.** Stopping a process, flipping a config flag off, or deleting a *regenerable cache* (like `npm`'s download cache) all count as safe: the thing comes back on its own or with a simple restart/reinstall. Deleting an application, uninstalling a package, removing user files, or any `rm -rf` outside the specific cache paths named below does **not** count as safe and is out of scope for this skill — do not do it, and do not suggest it as an escalation.
- **If a plain `kill` (or `kill -9`) doesn't make something go away for good, that is a signal to investigate, not a license to escalate.** See "When a killed process comes back" below. The answer is never "delete the app that owns it."

Keep this framing in the conversation with the user, briefly, before running remediation commands — they should know this is a "review everything" operation, not a "run and forget" one.

## Step 1 — Get real numbers before touching anything

Vague "it feels slow" isn't a diagnosis. Start with hard numbers, all read-only:

```bash
# Total RAM
sysctl hw.memsize | awk '{printf "%.1f GB\n", $2/1073741824}'

# Swap usage - the single most telling number
sysctl vm.swapusage
```

Rule of thumb: swap being heavily used (say, more than half of whatever total swap macOS has allocated) means the machine has been under real memory pressure — not just "a lot of processes," but genuinely not enough RAM for what's currently running. That distinction matters for what you recommend later: killing a handful of processes helps only if it actually closes the RAM gap.

```bash
# Top processes by memory, system-wide (not just one app's processes)
ps aux | sort -rk4 | head -25 | awk '{printf "%-8s %-6s %-6s %s\n", $2, $3"%", $4"%", $11" "$12" "$13" "$14}'
```

Look at this list with the user before assuming anything is "the problem" — a process using CPU briefly is normal; a process quietly holding a large %MEM for hours is the more interesting signal.

## Step 2 — Check for AI-tool / plugin process bloat

Tools like Claude Code, and similar MCP-based agent tools, can spawn a separate background server process for every enabled plugin/extension — often via `npx`, which does a fresh package resolution on each start. Left running across many app windows, these add up fast on a memory-constrained machine.

```bash
# List everything that looks like it's an MCP server or an npx-launched helper
ps aux | grep -iE "npx|npm exec|mcp" | grep -v grep
```

If the tool in question stores its enabled-plugin list in a config file (for Claude Code, that's `enabledPlugins` in `~/.claude/settings.json`), read it and cross-reference: plugins the user doesn't actually use are pure overhead — each one is a standing process even when idle.

Also check how many separate sessions/windows of the tool are running, and for how long:

```bash
ps -eo pid,etime,command | grep -i "<tool process name>" | grep -v grep
```

A session that's been running for many hours in a forgotten terminal tab is holding memory the whole time for no benefit. That's usually a bigger win to close than any single background helper process.

## Step 3 — Find safely-clearable cache bloat

Package manager caches are, by design, fully regenerable — clearing them frees disk space (and indirectly reduces cold-start overhead) with zero functional loss, since the tool just re-downloads what it needs next time.

```bash
du -sh ~/.npm/_npx ~/.npm/_cacache ~/.npm 2>/dev/null
```

If these are large (multiple GB is common after months of use), clearing is safe:

```bash
npm cache clean --force
rm -rf ~/.npm/_npx/*
```

This is disk cleanup, not RAM relief — mention that distinction to the user so they don't expect swap to drop from this step alone.

## Step 4 — Remediate, with review at every step

All of these are reversible. Show the exact command and what it targets before running it, and confirm the target process/plugin with the user first.

- **Disable a plugin/extension**, don't uninstall it: flip its enabled flag to `false` in its config file rather than deleting the entry. The user (or you, on request) can flip it back on any time. Changes like this typically need a full quit-and-relaunch of the app to take effect — killing the app's existing processes won't retroactively apply a config change.
- **Stop a specific process**, always by PID after confirming what it is:
  ```bash
  kill <pid>          # ask nicely first
  kill -9 <pid>        # only if it ignores the polite request
  ```
- **Close stale sessions/windows** of the tool that have been running idle for hours — same `kill` approach, same confirm-first rule.

## Step 5 — When a killed process comes back

Sometimes a process respawns within a second of being killed. That means something else is supervising it — either the OS's service manager, or a still-running parent application that treats it as a child worker it's responsible for keeping alive. Fighting this with repeated `kill` calls doesn't work and isn't the fix.

**Check if it's an OS-level service:**
```bash
launchctl list | grep -i "<name>"
```
If it shows up, it likely has a launch agent plist under `~/Library/LaunchAgents/`. Unloading it stops the process *and* the auto-restart behavior, and it's fully reversible:
```bash
launchctl unload ~/Library/LaunchAgents/<the-plist-file>.plist
# to bring it back later:
launchctl load ~/Library/LaunchAgents/<the-plist-file>.plist
```

**Check if it's a child of a running app:**
Some apps — IDEs and dev tools in particular — launch their own dedicated helper processes for automation or background tasks (a giveaway is a process that looks like a normal system binary but is started with unusual custom flags, e.g. a browser launched with its own private profile directory rather than the user's regular one). If the parent app is still running, it will simply relaunch the child. In this case the honest options are:
1. Leave it — it's a normal part of that app functioning while it's open, or
2. Quit the parent app itself if the user isn't actively using it right now.

Quitting an app is still fully reversible (relaunch it anytime) — it is not the same thing as deleting or uninstalling it, and that distinction is the one to hold onto here. Never respond to a respawning child process by suggesting the parent app be deleted or uninstalled; that's outside what this skill does, and it's a wildly disproportionate response to "a process won't stay dead."

## Step 6 — Be honest about the ceiling

After cleanup, re-check swap:

```bash
sysctl vm.swapusage
```

If it's still high, say so plainly rather than declaring victory. Process cleanup has a ceiling on a memory-constrained machine — if normal daily usage (a couple of dev tools, a browser, the OS itself) already exceeds installed RAM, no amount of killing background helpers permanently fixes that; it only buys some headroom until the same usage pattern fills it back up.

What actually helps beyond that point:
- Not running multiple heavy apps (several IDEs, multiple AI coding tool windows, etc.) at once when only one is in active use.
- Rebooting periodically — a reboot fully clears accumulated swap, which killing individual processes does not reliably do.
- Closing browser tabs/windows that aren't in use — each tab is typically its own process.

There is no user-facing macOS setting to manually "increase swap" the way some other operating systems allow. macOS already grows its swap files on disk automatically as needed; adding more swap doesn't address the underlying slowdown, because the slowdown *is* the swapping itself, not a shortage of swap space.

## Recap: what this skill will and won't do

| Action | Allowed here? | Why |
|---|---|---|
| Read memory/swap/process stats | Yes | Read-only |
| Kill/stop a confirmed process | Yes, with confirmation | Reversible — relaunches on demand |
| Disable a plugin/extension flag | Yes, with confirmation | Reversible — flip it back anytime |
| Clear a package manager cache (npm/npx etc.) | Yes | Regenerates automatically on next use |
| Unload a launchd agent | Yes, with confirmation | Reversible via `launchctl load` |
| Quit a running application | Yes, with confirmation | Reversible — relaunch anytime |
| Delete/uninstall an application | **No** | Not reliably recoverable |
| Delete user files or documents | **No** | Not reliably recoverable |
| `rm -rf` outside named cache paths | **No** | Too easy to hit something that isn't regenerable |
