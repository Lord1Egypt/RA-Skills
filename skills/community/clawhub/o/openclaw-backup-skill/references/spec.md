# OpenClaw Backup Skill — Public Spec

## Current bundled script

- `scripts/openclaw-backup.sh`

## Core behavior

The bundled script supports four mutually exclusive modes:
- `--auto` — create a regular backup, then prune regular backups
- `--backup` — create a regular backup only
- `--prune` — prune regular backups only
- `--manual` — create a manual backup only

## Default output directory

If `OUTPUT_DIR` is omitted, the bundled script writes to a general-purpose backup directory next to the parent of the resolved OpenClaw state dir.
In most cases it is:
- ~/backups/openclaw

## Archive classes

### Regular backup
- `openclaw-light-backup-YYYY-MM-DDTHH-MM-SSZ.tar.gz`

### Manual backup
- `openclaw-light-manual-backup-YYYY-MM-DDTHH-MM-SSZ.tar.gz`

Manual archives are excluded from normal prune.

## Backup contents

### Included in the current backup format
- workspace contents, including assistant identity and continuity files (for example SOUL.md, USER.md, AGENTS.md, and other workspace-level context files)
- OpenClaw config
- machine-readable cron export (`cron-export.json`)
- human-readable cron summary (`cron-summary.txt`)
- software versions (`software_versions.txt`)
- restore instructions (`RESTORE.md`)
- manifest (`manifest.json`)

### Excluded from the current backup format
- old backup storage inside workspace (legacy)
- temp artifacts
- environment variables
- system env
- system override

## Retention options

### `--keep-hours H`
Keep all regular archives from the last `H` hours.
- UTC rolling window
- compared by Unix epoch derived from the timestamp in the archive name
- `0` means disabled

### `--keep-days N`
Keep the latest regular archive for each of the last `N` UTC calendar days.

### `--keep-weeks M`
Keep the latest regular archive for each of the last `M` UTC ISO weeks.

### `--dry-run`
Allowed only with `--prune`.

Meaning:
- do not delete any archives or logs;
- compute the normal prune decision exactly as usual;
- report which regular archives would be kept and which would be deleted.

## Retention model

The final keep-set is the union of:
- all regular archives from the last `keep-hours` hours, if enabled;
- daily winners;
- weekly winners;
- the freshly created archive as forced keep in `--auto` mode.

Retention decisions are based on the UTC timestamp encoded in the filename, not on file timestamps from the filesystem.

## Safety model

The script should not delete automatically:
- manual archives;
- malformed archive-like filenames;
- unrelated files;
- temporary `.part` files.

If a filename cannot be parsed safely as a valid timestamped regular archive, it must be ignored, not deleted.

## Platform assumptions

The script currently targets:
- Linux
- Bash 4+
- GNU-style userland behavior where used by the script
