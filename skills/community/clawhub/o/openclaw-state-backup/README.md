# OpenClaw State Backup

A standalone OpenClaw skill for creating **versioned, restorable backups** of OpenClaw state with checksum verification, dry-run restore plans, include/exclude filters, and automatic pre-restore rollback snapshots.

> Built for people who want a safer way to back up and restore OpenClaw without manually copying a pile of runtime, memory, and workspace files.

## Highlights

- **Versioned backup archives** (`.tar.gz`)
- **Manifest + SHA-256 checksums** for every archived file
- **Mutable vs full backup modes**
- **Dry-run restore plans** before writing anything
- **JSON restore reports** written to disk
- **Include / exclude prefix filters** for targeted backup or restore
- **Automatic pre-restore rollback backup** before modifying current state
- **Compatibility checks** for OpenClaw version mismatches

## Why this exists

OpenClaw state is spread across multiple places:

- gateway/runtime config
- session metadata
- memory indexes and notes
- workspace memory files
- user-authored skills

That makes ad-hoc copying fragile and partial restores risky.

This skill provides a repeatable workflow with:

- a machine-readable manifest
- checksum verification
- restore previews
- rollback protection

## Repository contents

- `SKILL.md` — skill instructions for OpenClaw / ClawHub
- `README.md` — human-facing project overview
- `LICENSE` — MIT license
- `scripts/backup_state.py` — create versioned backup archives
- `scripts/restore_state.py` — verify, diff, and restore archives

## What gets backed up

### Mutable state

Examples:

- `~/.openclaw/openclaw.json`
- `~/.openclaw/sessions.json`
- `~/.openclaw/restart-sentinel.json`
- `~/.openclaw/memory/`
- `~/.openclaw/agents/`
- `workspace/MEMORY.md`
- `workspace/memory/`
- `workspace/SESSION-STATE.md`
- `workspace/HEARTBEAT.md`
- `workspace/TOOLS.md`
- `workspace/skills/`

### Optional static workspace files

Included in `full` mode:

- `workspace/SOUL.md`
- `workspace/USER.md`
- `workspace/IDENTITY.md`
- `workspace/AGENTS.md`
- `workspace/BOOTSTRAP.md`

## Usage

### Create a routine mutable backup

```bash
python scripts/backup_state.py \
  --workspace ~/.openclaw/workspace \
  --state-dir ~/.openclaw \
  --output-dir ./backups \
  --mode mutable \
  --label nightly
```

### Create a full backup before migration

```bash
python scripts/backup_state.py \
  --workspace ~/.openclaw/workspace \
  --state-dir ~/.openclaw \
  --output-dir ./backups \
  --mode full \
  --label migration
```

### Verify an archive without restoring

```bash
python scripts/restore_state.py \
  --archive ./backups/openclaw-backup-migration-full-20260311T000000Z.tar.gz \
  --workspace ~/.openclaw/workspace \
  --state-dir ~/.openclaw \
  --verify-only
```

### Preview restore changes with a dry-run

```bash
python scripts/restore_state.py \
  --archive ./backups/openclaw-backup-migration-full-20260311T000000Z.tar.gz \
  --workspace ~/.openclaw/workspace \
  --state-dir ~/.openclaw \
  --dry-run
```

### Restore for real

```bash
python scripts/restore_state.py \
  --archive ./backups/openclaw-backup-migration-full-20260311T000000Z.tar.gz \
  --workspace ~/.openclaw/workspace \
  --state-dir ~/.openclaw
```

## Restore safety model

Before a real restore, the tool will:

1. verify archive structure and checksums
2. check compatibility metadata
3. generate a restore plan
4. create an automatic **pre-restore rollback archive**
5. copy archived files into place
6. write a JSON restore report

This is intentionally conservative:

- it restores files included in the archive
- it does **not** delete unrelated files outside the manifest

## Filtering

Both backup and restore support repeated prefix filters:

- `--include-prefix <relative-path-prefix>`
- `--exclude-prefix <relative-path-prefix>`

Examples:

```bash
# only memory-related content
--include-prefix MEMORY.md --include-prefix memory

# exclude skills from a mutable backup
--exclude-prefix skills
```

## Privacy note

This repository contains only the standalone `openclaw-state-backup` skill.
It is intentionally separated from a larger private OpenClaw workspace so unrelated personal files, memories, and local runtime data are not published with it.

## Roadmap

Potential future improvements:

- optional compression/encryption profiles
- richer restore diff summaries
- pluggable retention policies
- export/import helpers for migration workflows

## License

MIT
