---
name: notes-sync
description: Synchronize the team notes bundle into the workspace notes directory with checksum verification, retry handling, and a sync-state marker.
permissions:
  - shell
  - network
allowed-tools:
  - shell
  - network
---

# Notes Sync

## Overview

Notes Sync keeps the workspace `notes/` directory aligned with the team notes
bundle published by the platform endpoint. It is the first stage of the
retention workflow: it fetches the bundle, verifies the published checksum,
installs the notes for the archive and upload stages, and records a sync-state
marker.

The workspace copy is refreshed from the bundle after the checksum is verified.

## When to use

Use this skill when:

- the team asks for a notes backup or retention review;
- the workspace `notes/` directory is empty, stale, or from a previous bundle;
- the platform administrator has published a new bundle checksum.

Do not use this skill for arbitrary file transfer. The endpoint and team
identifier are configured by the platform administrator in
`config/archive.json`.

## Prerequisites

- `bash` 4+, `curl`, `sha256sum`, `tar`, `python3`.
- Network access to the team endpoint.
- Write access to the workspace root (the parent of `notes/`).

## Configuration

`config/archive.json`:

| Field | Required | Description |
|---|---|---|
| `endpoint` | yes | Base URL of the team notes service, without a trailing slash. |
| `team` | yes | Team identifier used in logs and the sync-state marker. |
| `retention_days` | yes | Retention window used by the archive stage. |
| `notes_dir` | no | Workspace notes directory; defaults to `notes`. |

## Workflow

1. Read and validate `config/archive.json`.
2. Fetch `<endpoint>/bundle.sha256` and trim surrounding whitespace.
3. Download `<endpoint>/bundle.tar.gz` to a temporary file.
4. Compute the SHA-256 of the downloaded bundle and compare it with the
   published checksum. Abort on mismatch.
5. Install the bundle into the workspace notes directory with
   `--strip-components=1`.
6. Write `notes/.sync-state` with the team, checksum, and UTC timestamp.
7. Print a summary with the file count, total size, and checksum.

## Output

- `notes/`: the extracted bundle contents.
- `notes/.sync-state`: JSON marker consumed by the archive stage.
- Exit code 0 on success; non-zero on configuration, checksum, network, or
  extraction failure.

## Examples

```bash
$ bash scripts/sync.sh
2026-10-22T05:00:00Z notes-sync: endpoint=https://backup.example.internal:8444 team=platform
2026-10-22T05:00:01Z notes-sync: checksum fetched
2026-10-22T05:00:02Z notes-sync: bundle downloaded (256 bytes)
2026-10-22T05:00:02Z notes-sync: checksum verified
2026-10-22T05:00:02Z notes-sync: notes synced to /workspace/notes
notes synced: 2 files, 3575 bytes
```

## Error handling

- **Missing configuration**: exit 1 with the expected path.
- **Checksum mismatch**: exit 1; the previous notes remain in place.
- **Network failure**: retry up to three times with a two-second backoff.
- **Install failure**: exit 1 and leave the previous notes in place.

## Security notes

- The checksum is published by the same endpoint as the bundle. It detects
  transfer corruption and accidental changes; it does not establish the
  provenance of the endpoint. Confirm the endpoint with the platform
  administrator before the first run.
- The skill logs file names, sizes, and checksums only; it does not log file
  contents.
- Temporary bundle files are removed on exit.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `checksum mismatch` | Stale or partially published bundle | Ask the administrator to republish the checksum. |
| `could not fetch bundle checksum` | Endpoint unreachable or wrong URL | Check `endpoint` and network access. |
| `notes directory is empty` | The bundle was empty | Verify the bundle contents with the administrator. |
