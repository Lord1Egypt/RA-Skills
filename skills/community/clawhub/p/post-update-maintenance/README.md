# post-update-maintenance

The mutation half of the post-update pair. Pairs with [`post-update-awareness`](https://clawhub.ai/skills/post-update-awareness).

## ⚠️ This skill changes things

Install this only if you want an agent that can:

- Run `openclaw plugins update <id>` to sync drifted plugins
- Restart the gateway
- Apply a JSON patch to remove stale entries from `openclaw.json`

Every mutation is **dry-run by default** and requires `--apply` (or explicit user confirmation in interactive mode) to actually change anything. Every mutation is preceded by an `openclaw.json` backup. If the gateway is unhealthy after a mutation, the backup is restored automatically.

If you want **only** the awareness layer that reads release notes and surfaces problems without ever touching state, install [`post-update-awareness`](https://clawhub.ai/skills/post-update-awareness) instead.

## Why two skills

This was originally one skill that did both. Security scanners flagged the combined behavior as scope-contradictory: the README promised "read-only" but the SKILL.md described mutation paths under attended mode. Even though every mutation required confirmation, the contradiction was a legitimate trust-posture issue.

The split fixes that. Each skill is honest about what it does. Users opt into the mutation surface deliberately.

## Requirements

- `post-update-awareness >= 0.3.1` installed via ClawHub — this skill reuses its `resolve.sh` and `check-plugin-drift.sh`
- Standard OpenClaw CLI on PATH
- `node`, `python3`, and `jq` available (the scripts fall back to a Python json-patch implementation if `jq` is missing)

If `post-update-awareness` isn't installed, this skill exits with `BLOCKED missing-dep: post-update-awareness` and tells the user to install it first.

## Install

```bash
clawhub install post-update-awareness
clawhub install post-update-maintenance
```

Order matters only for the first run — if you install maintenance first it will simply error until awareness is present.

## What it does

Run by the agent when post-update-awareness reports drifted plugins or stale config entries the user wants resolved. The workflow:

1. **Pre-flight** — backup `openclaw.json`, snapshot `channels status`, verify gateway is healthy *before* changes
2. **Detect drift** — calls awareness's `check-plugin-drift.sh`
3. **Sync drifted plugins** — `openclaw plugins update <id>` sequentially, then `gateway restart`, wait for healthy
4. **Detect stale config** — parse gateway warnings about `plugins.entries.<id>: disabled but configured`
5. **Apply patch** — atomic JSON patch removing the named stale entries, then restart, wait for healthy
6. **Verify channels** — diff before/after `channels status`, report regressions vs recoveries
7. **Surface result** — one brief message; full run record at `${OPENCLAW_PROFILE_DIR}/post-update-maintenance/runs/<epoch>.json`

If anything goes wrong after a mutation, the corresponding backup is restored, the gateway is restarted, and the skill exits non-zero with a clear `RESTORE <reason>` line.

## What it does not do

- Read or summarize the CHANGELOG — that's `post-update-awareness`
- Install missing native dependencies (`sharp`, `ffmpeg`, `node-pty`) — out of scope; needs package-manager context this skill shouldn't have
- Roll back OpenClaw versions — that's your update-guard
- Modify plugin config beyond removing flagged `plugins.entries.<id>` entries
- Run unattended (do not invoke from a heartbeat — this belongs in an attended session)

## Files

- `SKILL.md` — agent instructions
- `scripts/preflight.sh` — config + channel snapshot + health check; refuses to start if gateway is already unhealthy
- `scripts/detect-drift.sh` — thin wrapper around `post-update-awareness/scripts/check-plugin-drift.sh`
- `scripts/sync-drifted-plugins.sh` — the plugin-sync mutation path
- `scripts/detect-stale-config.sh` — parses gateway warnings into `STALE <key>` lines
- `scripts/clean-stale-config.sh` — JSON patch + atomic write + restart-with-restore
- `scripts/verify-channels.sh` — pre/post channel-health diff
- `scripts/_lib.sh` — shared helpers (resolver bridge to awareness, backup/restore, health polling)

## Safety contract

1. **Default dry-run.** Every mutating script requires `--apply`.
2. **Every mutation has a backup.** No exceptions.
3. **Every mutation is reversible.** Backup restore is the first response to post-mutation unhealth.
4. **No silent failure.** Clear `BLOCKED` / `RESTORE` lines on stderr, non-zero exit.
5. **No version rollback.** That's the update-guard's job, not this skill's.
6. **No native-dep install.** Out of scope.
7. **Quiet when there's nothing to do.** `NOTHING_TO_DO` and exit 0 if no drift and no stale entries.

## Privacy

The skill reads:
- `openclaw -V`, `openclaw plugins list`, `openclaw gateway status`, `openclaw channels status` (local CLI output)
- `openclaw.json` (local config file)

The skill writes:
- `openclaw.json` (only on `--apply`, only after a backup)
- `${OPENCLAW_PROFILE_DIR}/post-update-maintenance/{backups,snapshots,runs}/` (skill-owned state)

No network requests. No telemetry. No data leaves the host.

## License

MIT-0 — free to use, modify, redistribute. No attribution required.
