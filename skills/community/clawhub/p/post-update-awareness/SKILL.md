---
name: post-update-awareness
description: After an OpenClaw version change, read the CHANGELOG entry pinned to the installed version and surface user-relevant changes — new tools, breaking changes, optional native dependencies that may need verification (sharp, ffmpeg, node-pty). Runs once per detected version bump. Use when OpenClaw has just been updated, when openclaw -V differs from the value on file, or when the user asks "what changed in this update?"
metadata: {"openclaw":{"requires":{"bins":["openclaw","curl","node"]}}}
---

# Post-Update Awareness

When OpenClaw is updated, the agent should not be the last to know. This skill reads the project CHANGELOG **for the exact installed version**, distills what changed for the user, and surfaces it once.

## When to use

Run this skill when **any** of the following is true:

1. The user asks "what changed in this update?" or "what's new in OpenClaw?"
2. A first-class update flow finishes (`openclaw update`, `openclaw plugins update`, or a package-manager update).
3. `openclaw -V` returns a value different from the version recorded in the skill's state file.

Do **not** run on every heartbeat. Run **once per detected version change**, then persist the new version so subsequent heartbeats stay quiet.

## Scope and non-goals

This skill **only**:

- Reads existing CHANGELOG content pinned to the installed version
- Reports it to the user
- Optionally probes for known-flaky optional native deps mentioned in the entry

This skill **does not**:

- Apply updates (`openclaw update` already handles that)
- Modify configuration
- Install missing dependencies without explicit user confirmation
- Roll back versions

## Workflow

### 1) Read the current installed version

```json
{ "tool": "exec", "command": "openclaw -V" }
```

Parse the version token (e.g. `OpenClaw 2026.5.3-1 (2eae30e)` → `2026.5.3-1`).

### 2) Compare against the last-known version

The skill maintains a small JSON state file per profile.

**Path resolution** (first match wins):

1. `$OPENCLAW_PROFILE_DIR/state/post-update-awareness.json` — when the runtime exports `OPENCLAW_PROFILE_DIR`
2. `$HOME/.openclaw-<profile>/state/post-update-awareness.json` — when a profile name is known (e.g. from `openclaw --profile <name>` or the `OPENCLAW_PROFILE` env var)
3. `$HOME/.openclaw/state/post-update-awareness.json` — single-profile / default fallback

This matters because the same machine can run multiple profiles (`main`, `noura-moi`, `amber`, …) and each one can independently update on its own cadence. A single shared state file caused the skill to go silent on profile B after surfacing on profile A — the bug the v0.3 path resolver fixes.

Contents:

```json
{
  "lastKnownVersion": "2026.5.2",
  "lastSurfacedAt": "2026-05-04T13:15:00Z",
  "profile": "noura-moi"
}
```

- If the file does not exist → write the current version as the baseline and **exit silently**. (No CHANGELOG dump on first run; only on actual transitions.)
- If `currentVersion === lastKnownVersion` → exit silently.
- If `currentVersion !== lastKnownVersion` → continue.

### 2a) Yield to the update-guard if it already handled this transition

Many OpenClaw setups also run an **update-guard** loop (heartbeat-driven config-backup + crash-loop watchdog — see e.g. `scripts/openclaw-update-guard.sh`). When the guard detects a version change it logs a `GUARD_OK`/`GUARD_RECOVERED`/`GUARD_ROLLBACK` event to `${HOME}/.openclaw-<profile>/update-guard/update-guard.log`.

Before surfacing, check whether the guard has *already announced* this exact transition in the last 10 minutes:

```bash
grep -E "VERSION CHANGE detected:.*v<currentVersion>" \
  "$HOME/.openclaw-<profile>/update-guard/update-guard.log" 2>/dev/null | tail -1
```

If a guard line for the current version is found within the recent window, the user has already been told the version changed. The skill should still surface the **CHANGELOG distillation** (that's what the guard doesn't do), but prefix it with `(already noted by update-guard)` and skip the redundant "OpenClaw updated to X (was Y)" header — go straight into the buckets. This avoids the double-notification failure mode.

### 3) Fetch the CHANGELOG entry pinned to the installed version

**Always pin to the installed version**, never read `main`. The release tag for OpenClaw matches the version with a `v` prefix.

Try in order:

1. **Local install copy** (fastest, offline-friendly): typical paths are platform-dependent. Try the directory of the npm install root first:
   ```bash
   {baseDir}/scripts/find-local-changelog.sh
   ```
   This script searches common install locations and prints the path if found.

2. **Remote, pinned to tag**:
   ```bash
   curl -fsSL "https://raw.githubusercontent.com/openclaw/openclaw/v<currentVersion>/CHANGELOG.md"
   ```
   The `v` prefix is required. If the remote 404s (e.g. a brand-new release tag hasn't propagated yet), retry once after 30 seconds before giving up.

3. **Fallback** (only if both above fail): query the GitHub Releases API for that exact tag:
   ```bash
   curl -fsSL "https://api.github.com/repos/openclaw/openclaw/releases/tags/v<currentVersion>"
   ```
   Use the `body` field as the changelog content.

If all three fail, surface a single line: *"OpenClaw was updated to vX, but I couldn't fetch the changelog to summarize what changed."* Do **not** invent content.

### 4) Extract the section for the new version

The CHANGELOG uses `## <version>` as section headings. Extract only the section between `## <currentVersion>` and the next `## ` heading. Do not dump the whole file.

If the section heading isn't found in the pinned changelog (rare — usually means the release tag exists but the changelog hasn't been updated for it), use the `Unreleased` section as a fallback only when the pinned-tag fetch came from `main`. When pinned to an actual release tag, prefer "no detailed notes available" over guessing.

### 5) Distill into 3 buckets

Group items into:

- **🆕 New for you** — new tools, commands, channels, capabilities the agent could benefit from. Filter ruthlessly to what an end-user agent actually touches; skip internal refactor lines, build-system changes, and CI plumbing.
- **⚠️ Breaking or removed** — anything that changes current behavior: removed config keys, renamed CLI commands, deprecated features, security tightenings.
- **🔧 May need attention** — optional native dependencies (`sharp`, `ffmpeg`, `node-pty`, `libvips`, etc.), peer-dep notes, post-install scripts, config-format migrations.

Each bucket: 1–4 bullets max. Omit empty buckets entirely.

### 6) Probe known-flaky optional deps (best effort)

If the "May need attention" bucket mentions a known native module, probe non-blockingly:

```bash
{baseDir}/scripts/probe-optional-dep.sh sharp
```

The script returns `OK`, `MISSING`, or `ERROR <msg>`. Annotate findings inline in the surfaced summary as `❌ sharp (image processing) — not installed`. Do **not** auto-install.

Default known list (extend as the project evolves):

- `sharp` — image attachment optimization
- `ffmpeg-static` / system `ffmpeg` — audio/video transcoding
- `node-pty` — terminal/PTY tools

### 6a) Detect plugin version drift

When the gateway updates, **externalized npm-installed plugins do not update automatically**. The result is a gateway on `vNew` running a plugin still on `vOld`. This was the original motivating case for surfacing this skill — see the "plugin drift" failure mode in the OpenClaw 2026.5.3→2026.5.4 transition where `@openclaw/whatsapp` was left behind.

Run:

```bash
{baseDir}/scripts/check-plugin-drift.sh <currentVersion>
```

The script lists installed plugins, parses the version column, and prints any plugin whose version does not match the gateway. Output format (one per line):

```
DRIFT <plugin-id> <plugin-version> (gateway <currentVersion>)
```

If the script reports any drift, add a bullet to **🔧 May need attention** in the form:

> `🔁 <plugin-id> still on <plugin-version> — run \`openclaw plugins update <plugin-id>\` then restart the gateway, or run the \`post-update-maintenance\` skill which handles drift + restart + channel verification end-to-end.`

Do **not** auto-update from inside this skill. This skill is read-only. The user should either run the command themselves or hand off to the maintenance skill, which is explicitly scoped for mutations.

### 6b) Verify channel health post-update

Updates frequently touch channel transports (Discord, WhatsApp, Telegram, Slack). After the gateway restart that follows an update, run:

```bash
openclaw --profile <profile> channels status
```

Flag any channel reporting `not configured`, `disconnected`, `unhealthy`, `degraded`, or `error` as a **⚠️ Breaking or removed** bullet. A connected channel that is `health:healthy` should not be surfaced.

This is especially important for any channel the user has flagged as actively in use (groups with active participants, customer-facing inboxes, etc.). When a profile name encodes a deployment scope (e.g. `noura-moi`), channels on that profile deserve a verbatim status mention even when healthy:

> `WhatsApp <profile>: linked, connected, healthy.`

This confirmation line is the only case where a healthy channel is surfaced — and only on profiles where the user has explicit production stake.

### 6c) Surface config rewrites and stale-entry warnings

When `plugins update` or `gateway` migrations rewrite `openclaw.json`, the CLI prints lines like:

```
Config overwrite: <path> (sha256 <old> -> <new>, backup=<path>.bak)
Config warnings:
- plugins.entries.<id>: plugin disabled (...) but config is present
```

When the skill observes either signal in command output it just executed (e.g. when the user ran `openclaw plugins update` in the same window), surface:

- The config rewrite as an info line: `Config rewritten — backup at <path>.bak.`
- Each stale-entry warning as a 🔧 bullet: `Stale config entry: \`plugins.entries.<id>\` (disabled but configured) — safe to remove from openclaw.json.`

Do **not** edit the config from inside this skill. If the user wants the stale entries cleaned automatically, hand off to `post-update-maintenance`.

### 7) Surface to the user

Send **one** brief message via the active channel.

```
OpenClaw updated to <newVersion> (was <oldVersion>).

🆕 New for you:
- <bullet>

⚠️ Breaking or removed:
- <bullet>

🔧 May need attention:
- 🔁 @openclaw/whatsapp still on 2026.5.3 — run: openclaw plugins update @openclaw/whatsapp
- ❌ sharp (image processing) — not installed; run: <install command>
- Stale config entry: `plugins.entries.device-pair` (disabled but configured)

WhatsApp noura-moi: linked, connected, healthy.

Full notes: https://github.com/openclaw/openclaw/blob/v<newVersion>/CHANGELOG.md
```

**Hard cap: ~18 lines.** Drop empty sections. The healthy-channel confirmation line is allowed only when (a) the profile name encodes a production deployment scope and (b) at least one channel on that profile is reporting healthy after the update.

If everything is quiet:

```
OpenClaw updated to <newVersion>. Nothing in the changelog requires action on my end.
```

### 8) Persist new state — **only after successful surfacing**

Ordering matters. Write state **after** the surface message has been dispatched, not before.

Why: if the agent crashes mid-skill, or the channel send fails (network blip, rate limit, channel disconnected during a plugin-drift update), writing state first would silently swallow the notification — the next heartbeat sees `currentVersion === lastKnownVersion` and exits quiet. The user never learns what changed.

Correct order:

1. Build the surface message.
2. Dispatch it through the active channel.
3. **Confirm dispatch succeeded** (no thrown error, channel acknowledged).
4. *Then* write `{ lastKnownVersion, lastSurfacedAt, profile }` atomically (write to `<file>.tmp`, then rename).

If step 3 fails, leave state untouched. The next heartbeat will retry. Cap retries at 5 per version transition (track in the state file as `surfaceAttempts: N`) to avoid an infinite loop if the changelog distillation itself is what's failing — once the cap is hit, write state with a `surfaceError` field and stop retrying.

## Script resolution (for callers outside the skill)

This skill's helper scripts (`check-plugin-drift.sh`, `find-local-changelog.sh`, `probe-optional-dep.sh`) are useful **outside** the skill too — most notably from a safe-update wrapper that runs the same drift check before deciding whether to sync plugins.

The problem: ClawHub installs the skill into different paths depending on profile + invocation. A wrapper script hardcoding one path will drift as soon as the user switches profile or moves the install.

**Stable resolver** (use this from any external caller):

```bash
# Locate this skill's script directory across known install layouts.
# Echoes the absolute path on stdout, exits 0 on success.
resolve_pua_scripts() {
  for candidate in \
    "${OPENCLAW_PROFILE_DIR:-/dev/null}/skills/post-update-awareness/scripts" \
    "$HOME/.openclaw-${OPENCLAW_PROFILE:-noura}/skills/post-update-awareness/scripts" \
    "$HOME/.openclaw/skills/post-update-awareness/scripts" \
    "$HOME/openclaw-soul/skills/post-update-awareness/scripts" \
    "$HOME/clawhub-skills/post-update-awareness/scripts" ; do
    if [ -d "$candidate" ] && [ -x "$candidate/check-plugin-drift.sh" ]; then
      echo "$candidate"
      return 0
    fi
  done
  return 1
}
```

The resolver lives at `scripts/resolve.sh` in this skill — callers can `source` it directly:

```bash
source "$HOME/.openclaw-${PROFILE}/skills/post-update-awareness/scripts/resolve.sh"
PUA_SCRIPTS=$(resolve_pua_scripts) || PUA_SCRIPTS=""
```

If the wrapper can't find the skill at all, it should fall back to an inline copy of the drift check (the safe-update reference implementation already does this). Always prefer the skill copy when present — it gets updates via `clawhub update` while the wrapper's inline fallback stays frozen.

## Mode: attended vs unattended

The skill runs in two distinct contexts:

- **Unattended** (heartbeat-fired, no human watching): produce the strict 3-bucket summary, persist state, exit. Hard cap on length still applies.
- **Attended** (the user just ran `openclaw update` and is watching): the same content is fine, and the skill may also answer follow-up questions about what changed. State is still persisted so the next heartbeat stays quiet about the same version transition.

Detect attended mode by whether the skill is being invoked inside an active user-driven session (the agent is replying to a fresh user message about updating). When in doubt, default to unattended.

### Hard line: read-only

This skill **does not mutate state**, in any mode. It does not update plugins, edit `openclaw.json`, install dependencies, or restart anything. When drifted plugins or stale config entries are detected, the skill *describes* what needs doing — the user (or a separate maintenance skill) runs the actual commands.

If the user asks the agent to fix the issues the skill surfaced, hand off to **[`post-update-maintenance`](https://clawhub.ai/skills/post-update-maintenance)** — a separate skill explicitly scoped for the mutation path. Do not perform mutations inline from inside this skill, even with user confirmation. The split exists so trust posture is clear: this skill is safe to install and run unattended on any heartbeat; the maintenance skill is invoked deliberately and is allowed to change things.

## Voice

This is an operational notice, not a marketing email. Terse, factual, no celebratory language.

- ✅ "OpenClaw updated to 2026.5.3-1. New: agent can now use the `talk` realtime voice tool. Watch: optional `sharp` is not installed; some image replies will fall back to original-size send."
- ❌ "🎉 Exciting news! OpenClaw has been upgraded with brand-new features..."

## Failure modes

| Situation | Behavior |
|---|---|
| CHANGELOG section missing for the version | One-line "OpenClaw updated to vX. No detailed notes for this tag yet — see GitHub Releases for raw notes." |
| No internet, no local copy | Same as above. |
| State file write fails | Log error; surface still happens; next run will re-surface. |
| Probe script not executable / shell unavailable | Skip the probe section; report changes without dep status. |

## Why this exists

OpenClaw releases are well-documented in `CHANGELOG.md` and per-version GitHub Releases, but the running agent has no built-in mechanism to *consume* that information after an update. Real-world consequence: when an update introduces a new optional native-dep requirement (e.g. `sharp` for image attachment optimization), the user discovers it only when an unrelated workflow fails.

This skill closes that loop using the existing CHANGELOG as source of truth, pinned to the installed version so the agent reads the changelog that matches what's actually running — not whatever has been merged since.
