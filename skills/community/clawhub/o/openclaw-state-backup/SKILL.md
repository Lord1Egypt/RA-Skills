---
name: openclaw-state-backup
version: 1.0.2
description: Create, inspect, and restore versioned OpenClaw state backups with rollback safety. Use when backing up or migrating OpenClaw memory, workspace state, gateway config, cron/session state, or when restoring a previously captured snapshot after breakage, config mistakes, host migration, or context-loss concerns.
---

# OpenClaw State Backup

Create and restore **versioned, restorable snapshots** of mutable OpenClaw state.

## What changes over time

Treat these as **mutable state** and include them in backups when they exist:

- `~/.openclaw/openclaw.json` — runtime config
- `~/.openclaw/sessions.json` — session metadata
- `~/.openclaw/restart-sentinel.json` — recent restart delivery state
- `~/.openclaw/memory/` — vector index / memory DBs
- `~/.openclaw/agents/` — per-agent runtime/session state
- `workspace/MEMORY.md`
- `workspace/memory/`
- `workspace/SESSION-STATE.md`
- `workspace/HEARTBEAT.md`
- `workspace/TOOLS.md`
- `workspace/skills/` — user-authored skills and local skill state

Treat these as **mostly static/user-maintained bootstrap files** and back them up when you want a full environment restore, but do not rely on them as fast-changing runtime state:

- `workspace/SOUL.md`
- `workspace/USER.md`
- `workspace/IDENTITY.md`
- `workspace/AGENTS.md`
- `workspace/BOOTSTRAP.md` (if still present)

## Backup strategy

Use the bundled scripts for deterministic behavior.

### Create backup

Run `scripts/backup_state.py` with:

- `--workspace <path>`
- `--state-dir <path>` (usually `~/.openclaw`)
- `--output-dir <path>` for generated snapshots
- optional `--label <name>`
- optional `--mode mutable|full` (default: `mutable`)
- optional repeated `--include-prefix <relative-path-prefix>`
- optional repeated `--exclude-prefix <relative-path-prefix>`

`mutable` captures changing state only.
`full` adds mostly-static workspace identity/bootstrap files too.

The script writes:

- a timestamped `.tar.gz`
- a `manifest.json`
- checksums for every stored file
- compatibility metadata (`formatVersion`, OpenClaw version, host/platform)
- applied include/exclude filter metadata

### Restore backup

Run `scripts/restore_state.py` with:

- `--archive <path-to-tar.gz>`
- `--workspace <path>`
- `--state-dir <path>`
- optional `--verify-only`
- optional `--dry-run`
- optional `--allow-version-mismatch`
- optional `--report-dir <path>`
- optional repeated `--include-prefix <relative-path-prefix>`
- optional repeated `--exclude-prefix <relative-path-prefix>`

Restore behavior:

1. verify archive structure + checksums
2. compare compatibility metadata
3. optionally narrow restore scope with include/exclude prefixes
4. build a restore plan (`create` / `update` / `unchanged` / `missingFromArchive`)
5. always write a JSON restore/dry-run report to disk
6. if `--dry-run`, stop after writing the diff-style report
7. otherwise create a **pre-restore rollback backup** automatically
8. restore files into place
9. write a final restore report showing what changed and where rollback lives

## Safety rules

- Always prefer `--verify-only` first when archive provenance is uncertain.
- Never overwrite from an archive that fails checksum verification.
- Never delete unrelated files outside the managed backup manifest.
- If compatibility check fails, stop unless the user explicitly wants `--allow-version-mismatch`.
- Before reporting restore success, mention the generated rollback archive path.

## File model

The scripts split backup contents into:

- `mutable/` — runtime-changing state
- `static/` — mostly-stable workspace identity/configuration files
- `meta/manifest.json` — archive manifest

Read the manifest if you need to inspect contents without restoring.

## When to use which mode

- Use **mutable** for routine safety snapshots and frequent backups.
- Use **full** before machine migration, risky reconfiguration, or major cleanup.

## Recovery guidance

If a restore causes problems, immediately restore the auto-generated **pre-restore rollback archive** created by `restore_state.py`.
