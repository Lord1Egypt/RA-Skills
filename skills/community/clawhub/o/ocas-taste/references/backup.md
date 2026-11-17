# Backup and Restore

## What's backed up

All taste and styx data is backed up to GitHub LFS (`<fs-root>/indigo-repo`):

| File | Source | Description |
|------|--------|-------------|
| `data/styx.db` | `<hermes-home>/data/styx.db` | Merchant database (162 food + 19 travel) |
| `data/transactions.db` | `<hermes-home>/data/transactions.db` | Plaid transaction history |
| `data/ocas-taste-signals.jsonl` | `<hermes-home>/commons/data/ocas-taste/signals.jsonl` | ~7,800 consumption signals |
| `data/ocas-taste-items.jsonl` | `<hermes-home>/commons/data/ocas-taste/items.jsonl` | ~980 enriched entities |
| `data/ocas-taste-extractions.jsonl` | `<hermes-home>/commons/data/ocas-taste/extractions.jsonl` | Raw email/calendar extractions |
| `data/ocas-taste-links.jsonl` | `<hermes-home>/commons/data/ocas-taste/links.jsonl` | Entity relationships |
| `data/ocas-taste-decisions.jsonl` | `<hermes-home>/commons/data/ocas-taste/decisions.jsonl` | Audit log |
| `data/ocas-taste-config.json` | `<hermes-home>/commons/data/ocas-taste/config.json` | Configuration |

## What's NOT backed up

- `state.db` (14G) — too large for GitHub LFS
- `<fs-root>/commons/data/ocas-taste/` — stale copy, removed

## Backup script

bash <fs-root>/indigo-repo/scripts/backup_all_hermes_data.sh

Runs daily at 03:00 via Backup Hermes Sessions to GitHub cron job.

## LFS tracking

Git LFS tracks: *.jsonl, *.db, *.lbug, *.sqlite3, *.tar.gz

## Restore from backup

cd <fs-root>/indigo-repo
git lfs pull
cp data/styx.db <hermes-home>/data/styx.db
cp data/ocas-taste-*.jsonl <hermes-home>/commons/data/ocas-taste/
cp data/transactions.db <hermes-home>/data/transactions.db

## Disk space management

- Old local backups in <fs-root>/backup/ are cleaned up automatically (keep 3 days)
- state.db (14G) is never backed up - it's session state that can be regenerated