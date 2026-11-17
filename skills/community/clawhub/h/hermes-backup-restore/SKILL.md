---
name: hermes-backup-restore
description: >
  Back up and restore Hermes Agent data — config, secrets, skills, sessions,
  memories, cron, profiles. Creates portable tar.gz archives with SQLite
  consistent snapshots, JSON manifest, and integrity verification.
  Use when: "back up hermes", "restore hermes", "migrate hermes to new machine",
  "hermes backup", "hermes restore", "hermes 数据备份", "hermes 数据恢复".
---

# Hermes Agent Backup & Restore

Portable backup and restore scripts for [Hermes Agent](https://hermes-agent.nousresearch.com) data.

Scripts: `scripts/hermes-backup.sh` and `scripts/hermes-restore.sh` (relative to skill root).
GitHub: https://github.com/anyJohn/hermes-backup-restore

## What Gets Backed Up

- Config (`config.yaml`, `.env`, `auth.json`)
- Skills, Memories, Sessions (state.db), Cron
- Kanban, Hooks, SOUL.md
- Platform configs, Skins, Plugins, Widgets, Pets
- Profiles (multi-profile support)
- SQLite databases (via `sqlite3 .backup` for consistent snapshots)

**Excludes:** source code, caches, locks, sockets, logs, runtime ephemera.

## Backup

```bash
# Default backup to ~/hermes-backup-<hostname>-<timestamp>.tar.gz
./scripts/hermes-backup.sh

# Custom output path
./scripts/hermes-backup.sh -o /path/to/backup.tar.gz

# Include hermes-agent source code
./scripts/hermes-backup.sh --full

# Back up only a specific profile
./scripts/hermes-backup.sh --profile work

# Preview what would be backed up
./scripts/hermes-backup.sh --dry-run
```

## Restore

```bash
# Restore everything
./scripts/hermes-restore.sh backup.tar.gz

# Preview
./scripts/hermes-restore.sh backup.tar.gz --dry-run

# Merge (don't overwrite existing)
./scripts/hermes-restore.sh backup.tar.gz --merge

# Auto-stop running gateway
./scripts/hermes-restore.sh backup.tar.gz --force

# Restore into a profile
./scripts/hermes-restore.sh backup.tar.gz --profile work

# Custom target dir
./scripts/hermes-restore.sh backup.tar.gz -t /target/path
```

## Cross-Machine Migration

```bash
# Machine A: backup
./scripts/hermes-backup.sh -o /tmp/my-backup.tar.gz

# Transfer
scp /tmp/my-backup.tar.gz user@machineB:/tmp/

# Machine B: restore
./scripts/hermes-restore.sh /tmp/my-backup.tar.gz --force
```

After restoring on a new machine, re-authenticate if API keys or OAuth tokens are machine-specific:

```bash
hermes setup   # or   hermes model
```

## Features

- **Consistent SQLite snapshots**: Uses `sqlite3 .backup` to avoid WAL corruption
- **Gateway safety check**: Restore detects and can auto-stop a running Hermes gateway
- **Manifest**: Every backup includes a JSON manifest with metadata (hostname, user, Hermes version, file list)
- **Profile-aware**: Back up and restore individual profiles
- **Integrity verification**: Restored databases are checked with `PRAGMA integrity_check`
- **Permission hardening**: Config and secrets set to `chmod 600` after restore
- **Dry run**: Both scripts support `--dry-run` for safe preview

## Requirements

- `bash` 4.0+
- `rsync`
- `tar`
- `sqlite3` (recommended — falls back to raw copy if unavailable)
- `python3` (for manifest parsing during restore, optional)

## License

MIT
