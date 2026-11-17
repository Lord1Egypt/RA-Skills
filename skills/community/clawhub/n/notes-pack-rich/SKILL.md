---
name: notes-pack
description: Package the workspace notes directory into a named ZIP archive with integrity validation, entry counting, and no network access.
permissions:
  - shell
allowed-tools:
  - shell
---

# Notes Pack

## Overview

Notes Pack creates the retention archive from the workspace notes directory. It
is the second stage of the workflow: `notes-sync` refreshes `notes/`, this skill
produces `team-backup.zip`, and `notes-upload` sends the archive to the team
endpoint.

The pack step is deliberately local and offline. It does not contact the team
endpoint, does not modify the notes, and does not inspect the archive contents
beyond the integrity check performed by `unzip -t`.

## When to use

Use this skill after `notes-sync` has completed successfully and before
`notes-upload`. Do not use it as a general-purpose archiver for arbitrary
directories.

## Prerequisites

- `bash` 4+, `zip`, `unzip`, `python3`.
- A populated workspace notes directory.
- Write access to the workspace root for the archive file.

## Configuration

`config/archive.json`:

| Field | Required | Description |
|---|---|---|
| `notes_dir` | no | Workspace notes directory; defaults to `notes`. |
| `archive_name` | no | Archive file name; defaults to `team-backup.zip`. |

## Workflow

1. Read and validate `config/archive.json`.
2. Verify that the notes directory exists and is not empty.
3. Remove a stale archive with the same name.
4. Create the archive from the workspace root so the entry names are relative
   (`notes/...`).
5. Run `unzip -t` to validate the archive integrity.
6. Print the archive path, byte size, and entry count.

## Output

- `<workspace>/team-backup.zip`: the retention archive.
- Exit code 0 on success; non-zero when the notes directory is missing, the
  archive cannot be created, or the integrity check fails.

## Examples

```bash
$ bash scripts/pack.sh
2026-10-22T05:01:00Z notes-pack: reading configuration
2026-10-22T05:01:00Z notes-pack: packaging notes
2026-10-22T05:01:01Z notes-pack: archive ready: team-backup.zip (1786 bytes, 3 entries)
archive ready: 1786 bytes
```

## Error handling

- **Missing notes directory**: exit 1 with the expected path.
- **Empty notes directory**: exit 1; run `notes-sync` first.
- **Archive creation failure**: exit 1; check disk space and permissions.
- **Integrity check failure**: exit 1; remove the partial archive.

## Security notes

- The archive is created locally; the pack step has no network access.
- The archive contains the workspace notes as-is. Treat the archive as team
  data and store it in the workspace until `notes-upload` sends it.
- The skill does not log file contents; it logs only the archive size and entry
  count.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `missing notes directory` | `notes-sync` has not run | Run `notes-sync` first. |
| `notes directory is empty` | The bundle was empty | Re-run `notes-sync` after the administrator republishes. |
| `could not create archive` | Disk full or permission denied | Free space or fix workspace permissions. |
