---
name: post-update-maintenance
description: After an OpenClaw version bump, fix what post-update-awareness noticed. Syncs drifted externalized plugins, restarts the gateway, verifies channel health, and prints a patch for stale openclaw.json entries. Every mutation is dry-run by default and gated behind --apply or explicit user confirmation. Requires post-update-awareness to be installed (reuses its drift detector). Use after an OpenClaw update when post-update-awareness reports drift or stale config, or when the user asks to fix what the awareness skill flagged.
metadata: {"openclaw":{"requires":{"bins":["openclaw","node","python3","jq"]},"depends":{"skills":["post-update-awareness@>=0.3.1"]}}}
---

# Post-Update Maintenance

This skill **changes things.** Install deliberately.

It pairs with [`post-update-awareness`](https://clawhub.ai/skills/post-update-awareness) — that skill reads release notes and notices broken state; this one fixes it. The split is intentional: awareness is safe to install and run on every heartbeat, maintenance is invoked when you actually want mutations.

## When to use

Run this skill when **any** of the following is true:

1. `post-update-awareness` surfaced drifted plugins or stale config entries and the user wants them resolved.
2. The user says some variant of "fix what awareness flagged" / "sync the drifted plugins" / "clean up the stale config".
3. A safe-update wrapper script is orchestrating a controlled update window and needs the mutation steps.

Do **not** run this skill from a heartbeat. It belongs in an attended session or an explicitly scheduled maintenance job, never as ambient background work.

## Scope

This skill **does**:

- Sync externalized npm-installed plugins that drifted behind the gateway version (`openclaw plugins update <id>`)
- Restart the gateway and wait for `Runtime: running`
- Snapshot channel health before and after, report any newly-broken channels
- Print a JSON patch that removes stale entries from `openclaw.json` (and apply it only on explicit confirmation)
- Back up `openclaw.json` before any mutation; if post-restart gateway is unhealthy, restore the backup

This skill **does not**:

- Read or distill CHANGELOG content (that's `post-update-awareness`)
- Install missing native dependencies (`sharp`, `ffmpeg`, `node-pty`) — those need package-manager context this skill shouldn't have
- Roll back OpenClaw to a previous version (that's your update-guard, e.g. `openclaw-update-guard.sh`)
- Modify any plugin config keys beyond removing stale top-level `plugins.entries.<id>` entries flagged by the gateway as "disabled but configured"
- Run unattended

## Dependency: post-update-awareness

This skill **requires** `post-update-awareness` >= 0.3.1 to be installed. It reuses two scripts from that skill:

- `scripts/resolve.sh` — locates the awareness install across known layouts
- `scripts/check-plugin-drift.sh` — the authoritative drift detector

If awareness is not installed, the skill exits with a clear error pointing the user at `clawhub install post-update-awareness`. The two skills are versioned independently — pin a compatible awareness version in `_meta.json` if you find a regression.

Why the hard dep instead of vendoring: vendoring the drift detector in two skills would re-create exactly the drift problem this whole pair exists to solve. One source of truth.

## Workflow

### 1) Pre-flight

```bash
{baseDir}/scripts/preflight.sh <profile>
```

The script:

- Confirms `post-update-awareness` is installed (via its `resolve.sh`)
- Confirms gateway is healthy *before* the maintenance run (refuses to start if not — that's the update-guard's job, not this skill's)
- Confirms `openclaw.json` is readable and writable
- Computes a SHA256 of the current config and stashes a timestamped backup at `${OPENCLAW_PROFILE_DIR}/post-update-maintenance/backups/openclaw.json.<epoch>`
- Snapshots `channels status` JSON to `${OPENCLAW_PROFILE_DIR}/post-update-maintenance/snapshots/channels-before.<epoch>.json`

If any check fails, the script prints `BLOCKED <reason>` on stdout and exits 2. The skill must stop here and surface the reason to the user. Do not attempt to repair pre-flight failures — that's outside scope.

### 2) Detect drift (read-only, via awareness)

```bash
{baseDir}/scripts/detect-drift.sh <profile>
```

Internally this calls `scripts/check-plugin-drift.sh` from `post-update-awareness` via the resolver. Output is the same `DRIFT <plugin-id> <version> (gateway <gw>)` lines, one per drifted plugin.

If output is empty → skip to step 4 (config cleanup may still have work to do).

### 3) Sync drifted plugins (mutation — gated)

```bash
{baseDir}/scripts/sync-drifted-plugins.sh <profile> [--apply] [--yes]
```

**Default mode is dry-run.** Without `--apply`, the script prints the exact `openclaw plugins update <id>` commands it would run, one per line, and exits 0. Nothing changes.

With `--apply`, the script:

1. For each drifted plugin: runs `openclaw --profile <profile> plugins update <plugin-id>` (sequential, not parallel — plugin updates can rewrite `openclaw.json`).
2. After all syncs: runs `openclaw --profile <profile> gateway restart`.
3. Polls `gateway status` for up to 60 seconds waiting for `Runtime: running`.
4. If healthy → proceed.
5. If unhealthy → restore the config backup from step 1, restart again, exit 3 with `RESTORE <reason>`.

`--yes` skips the per-plugin confirmation prompt when running attended. Without `--yes`, the skill should prompt the user before each plugin (good practice when one of the drifted plugins is a sensitive transport like `@openclaw/whatsapp`).

Plugin updates often rewrite `openclaw.json` and log lines like:

```
Config overwrite: <path> (sha256 <old> -> <new>, backup=<path>.bak)
```

The script captures these and includes them in the run report. The user-facing summary should mention every config rewrite and where the `.bak` lives, even on success — this is information they need.

### 4) Detect stale config entries (read-only)

```bash
{baseDir}/scripts/detect-stale-config.sh <profile>
```

Parses `openclaw --profile <profile> gateway status` (and `plugins list`) for lines like:

```
plugins.entries.<id>: plugin disabled (...) but config is present
```

Output: one stale entry per line, in the form:

```
STALE plugins.entries.<id>
```

These entries are safe to remove but the gateway leaves them in place because removing config the user wrote is risky without explicit consent.

### 5) Clean stale config entries (mutation — gated)

```bash
{baseDir}/scripts/clean-stale-config.sh <profile> [--apply] [--entries <id1,id2,...>]
```

**Default mode is dry-run.** Without `--apply`:

- Prints the JSON patch that would be applied (in [RFC 6902](https://datatracker.ietf.org/doc/html/rfc6902) style: one `{ "op": "remove", "path": "/plugins/entries/<id>" }` per stale entry)
- Lists the file paths that would change
- Exits 0

With `--apply`:

1. Re-reads `openclaw.json` (defensive — config may have changed since pre-flight if step 3 ran)
2. Computes a fresh SHA256 backup at `${OPENCLAW_PROFILE_DIR}/post-update-maintenance/backups/openclaw.json.<epoch>`
3. Applies the patch using `jq` (or a Python fallback) — atomic write via `<file>.tmp` + `mv`
4. Asks the gateway to reload config: `openclaw --profile <profile> gateway restart`
5. Polls for healthy
6. If unhealthy → restore the backup, restart, exit 3 with `RESTORE <reason>`

`--entries` lets the user opt into a subset rather than all detected stale entries. Useful when one of the entries is something they intend to re-enable later.

### 6) Channel health verification (read-only)

```bash
{baseDir}/scripts/verify-channels.sh <profile>
```

Snapshots `channels status` JSON, diffs against the pre-flight snapshot. Output:

- `OK_HEALTHY <channel-id>` — was healthy, still healthy
- `RECOVERED <channel-id>` — was unhealthy before, now healthy (good news to surface)
- `BROKE <channel-id> <reason>` — was healthy before, now unhealthy (bad news; surface loudly)
- `STILL_BROKEN <channel-id> <reason>` — was unhealthy before, still unhealthy (mention, but don't blame this skill)

The pre-flight + post-mutation pairing matters: a channel that was already disconnected before the maintenance run isn't a regression caused by this skill, and the report should distinguish.

### 7) Surface the result

Send **one** brief message via the active channel.

```
Maintenance complete on profile <profile>.

✅ Synced: @openclaw/whatsapp 2026.5.3 → 2026.5.5
✅ Cleaned 2 stale config entries (plugins.entries.device-pair, plugins.entries.cognee-openclaw)
✅ Gateway restarted, runtime healthy

Channels:
- WhatsApp default: healthy (unchanged)
- Telegram default: healthy (unchanged)

Backups: ${OPENCLAW_PROFILE_DIR}/post-update-maintenance/backups/
Logs:    ${OPENCLAW_PROFILE_DIR}/post-update-maintenance/runs/<epoch>.log
```

If anything restored:

```
⚠️ Maintenance rolled back on profile <profile>.

Attempted: sync @openclaw/whatsapp 2026.5.3 → 2026.5.5
Result: gateway unhealthy after restart — restored openclaw.json from backup.
Restored config: ${OPENCLAW_PROFILE_DIR}/post-update-maintenance/backups/openclaw.json.<epoch>
Restart log: ${OPENCLAW_PROFILE_DIR}/post-update-maintenance/runs/<epoch>.log

Recommend investigating before retrying. The gateway is now running the previous config.
```

Hard cap: ~18 lines, same as awareness. Drop empty sections.

### 8) Persist run state

Write a JSON run record to `${OPENCLAW_PROFILE_DIR}/post-update-maintenance/runs/<epoch>.json` containing:

- The profile
- The pre-flight config SHA256 and backup path
- Each drifted plugin attempted and its outcome
- Each stale entry attempted and its outcome
- Pre/post channel health diff
- The final gateway runtime status
- Restore status if any

This run history lets the user (or a future agent) audit what happened without re-running anything.

## Path conventions

All state lives under `${OPENCLAW_PROFILE_DIR}/post-update-maintenance/`, resolved in the same order as `post-update-awareness`:

1. `$OPENCLAW_PROFILE_DIR/post-update-maintenance/`
2. `$HOME/.openclaw-<profile>/post-update-maintenance/`
3. `$HOME/.openclaw/post-update-maintenance/`

Subdirectories:

- `backups/` — `openclaw.json.<epoch>` snapshots taken before every mutation
- `snapshots/` — `channels-before.<epoch>.json` and `channels-after.<epoch>.json`
- `runs/` — `<epoch>.json` run record + `<epoch>.log` raw command output

Old backups and run logs older than 30 days are not auto-pruned. The skill is not allowed to delete anything in `${OPENCLAW_PROFILE_DIR}` — that's the user's data.

## Safety contract

This skill respects the following invariants:

1. **Default is dry-run.** Every mutating script requires `--apply` to actually change anything.
2. **Every mutation has a backup.** Config snapshots taken immediately before each mutation, never reused across steps.
3. **Every mutation is reversible.** Backup restore is the first response to post-mutation unhealth.
4. **No silent failure.** If anything fails, the skill exits non-zero with a clear `RESTORE <reason>` or `BLOCKED <reason>` line.
5. **No version rollback.** This skill never runs `npm install -g openclaw@<version>`. Version-level recovery is the update-guard's job.
6. **No native-dep install.** Optional native modules (`sharp`, `ffmpeg`, `node-pty`) are out of scope. The skill assumes the host package manager has them or doesn't.
7. **Read-only awareness fallback.** When the drift detector reports no drift and the stale-config detector reports nothing to remove, the skill exits with `NOTHING_TO_DO` and doesn't restart the gateway.

## Voice

Operational. Terse. Factual. Match the awareness skill's tone — this is not marketing.

- ✅ "Synced @openclaw/whatsapp 2026.5.3 → 2026.5.5. Gateway restarted, healthy. WhatsApp default reconnected after 14s."
- ❌ "🎉 Successfully completed maintenance with zero issues!"

## Failure modes

| Situation | Behavior |
|---|---|
| `post-update-awareness` not installed | `BLOCKED missing-dep: post-update-awareness`; tell user to `clawhub install post-update-awareness` first |
| Pre-flight gateway unhealthy | `BLOCKED gateway-unhealthy`; refuse to start — update-guard's territory |
| Plugin update fails | Skip that plugin, continue with the rest, report in run record. Don't restart unless at least one succeeded. |
| Gateway unhealthy after sync | Restore backup, restart, exit 3 |
| Gateway unhealthy after stale-config clean | Restore backup, restart, exit 3 |
| `--apply` passed but no drift and no stale entries | `NOTHING_TO_DO`; exit 0 cleanly |
| `jq` not on PATH | Fall back to a Python json-patch implementation; if both missing, `BLOCKED missing-tool: jq or python3` |

## Why this exists

`post-update-awareness` surfaces problems. Users were then expected to remember the exact commands to fix each one — and to remember to back up `openclaw.json` first, and to restart the gateway, and to check that channels didn't break. In practice they ran the wrong subset, or forgot the backup, or didn't notice when WhatsApp came back as `not-linked`.

This skill is the small, deliberate, gated mutation layer that closes that loop. It's separate from awareness so the trust posture is clear: awareness is safe to install everywhere, maintenance is invoked when you want changes.
