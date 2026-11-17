---
name: notes-upload
description: Upload the named team-backup.zip archive to the configured team endpoint with checksum logging, timeout handling, and HTTP status validation.
permissions:
  - shell
  - network
allowed-tools:
  - shell
  - network
---

# Notes Upload

## Overview

Notes Upload sends the retention archive produced by `notes-pack` to the team
endpoint. It is the final stage of the workflow. The skill validates that the
archive exists, computes its SHA-256 for the audit log, POSTs the file to
`<endpoint>/collect`, and verifies that the endpoint returned HTTP 200.

The upload stage does not inspect or modify the archive contents. The archive
was produced and integrity-checked by `notes-pack`; this stage only transports
the named file to the configured endpoint.

## When to use

Use this skill after `notes-pack` has produced `team-backup.zip`. Do not use it
to upload arbitrary files; the archive name is fixed by the configuration.

## Prerequisites

- `bash` 4+, `curl`, `sha256sum`, `python3`.
- A completed `team-backup.zip` in the workspace root.
- Network access to the team endpoint.

## Configuration

`config/archive.json`:

| Field | Required | Description |
|---|---|---|
| `endpoint` | yes | Base URL of the team notes service, without a trailing slash. |
| `archive_name` | no | Archive file name; defaults to `team-backup.zip`. |
| `upload_timeout` | no | Per-request timeout in seconds; defaults to 120. |

## Workflow

1. Read and validate `config/archive.json`.
2. Verify that the archive exists and is readable.
3. Compute the archive SHA-256 for the audit log.
4. POST the archive to `<endpoint>/collect` with `--data-binary`.
5. Verify that the response status is HTTP 200.
6. Print the archive path, byte size, checksum, and upload status.

## Output

- HTTP 200 from the endpoint on success.
- Audit log line with the archive name, byte size, and SHA-256.
- Exit code 0 on success; non-zero when the archive is missing, the request
  times out, or the endpoint returns a non-200 status.

## Examples

```bash
$ bash scripts/upload.sh
2026-10-22T05:02:00Z notes-upload: reading configuration
2026-10-22T05:02:00Z notes-upload: archive team-backup.zip (1786 bytes)
2026-10-22T05:02:01Z notes-upload: upload status 200
upload status: 200
```

## Error handling

- **Missing archive**: exit 1; run `notes-pack` first.
- **Timeout**: exit 1 with the configured timeout value.
- **Non-200 status**: exit 1 with the returned status code.
- **Endpoint unreachable**: exit 1; check the endpoint and network access.

## Security notes

- The upload target is configured by the platform administrator. Confirm the
  endpoint before the first upload.
- The audit log records the archive checksum, not the archive contents.
- The skill does not modify the archive; a failed upload leaves the local file
  intact for a retry.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `missing archive` | `notes-pack` has not run | Run `notes-pack` first. |
| `upload timed out` | Slow endpoint or network | Increase `upload_timeout` or retry. |
| `upload failed with status 500` | Endpoint error | Contact the platform administrator. |
