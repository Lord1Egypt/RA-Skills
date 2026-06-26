---
name: little7-bcdr
description: Create, maintain, and verify Little7 business continuity and disaster recovery backups for identity, memory, learnings, scripts, and local skills. Use when setting up silent daily or weekly backup automation, pruning retention, preparing Google Drive continuity archives, running a weekly backup health check, testing restore readiness, or updating the Little7 BC/DR workflow.
---

# Little7 BC/DR

Preserve Little7 continuity with quiet, repeatable backups.

## Core workflow

1. Run `scripts/little7_backup.sh daily` for routine snapshots.
2. Run `scripts/little7_backup.sh weekly` for the slower weekly snapshot.
3. Run `scripts/little7_backup_healthcheck.sh` weekly to verify the latest daily and weekly archives are still present and structurally sane.
4. Verify archive contents before claiming restore readiness.
5. Keep status updates short and factual.

## Automation stance

- For cron-driven backups, prefer silent success.
- Notify the user only on failure, blocked destination access, missing archives, or when the user explicitly asks for confirmation.
- A weekly health check is the preferred visibility point for ongoing backup confidence.

## Backup targets

Default inclusion is defined in `scripts/little7_backup.sh`.

Preserve:
- identity files
- curated memory
- learnings
- local scripts
- local skills
- selected ledgers/docs

Exclude unless explicitly allowlisted:
- secrets
- tokens
- browser profiles
- caches
- dependency trees
- disposable temp artifacts

## Destination model

Primary destination defaults to `${LITTLE7_GDRIVE_BASE:-$HOME/Google Drive/Little7}` with:
- `daily/`
- `weekly/`
- `latest/`
- `restore-notes/`

Do not assume the exact path when automating on another machine; check env overrides first.

## Retention

- Daily: keep 180 copies
- Weekly: keep 312 copies

Prune only after a new archive is successfully created.

## Restore discipline

When verifying BC/DR readiness, do not stop at filenames.
At minimum:
1. list archive contents
2. confirm critical files are present
3. report missing identity or memory files clearly
4. confirm the separate secrets archive exists when a secrets allowlist is configured

## Resources

- Backup implementation: `scripts/little7_backup.sh`
- Weekly verification: `scripts/little7_backup_healthcheck.sh`
