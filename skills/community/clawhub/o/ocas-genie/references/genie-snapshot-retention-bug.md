# Genie Snapshot Retention Bug & Post-Clean Verification

## Confirmed bug (2026-07-12)
`clean_backup_retention` (scripts/genie.py) keeps only the single newest
candidate across **ALL** backup classes combined:

    keep = valid[:keep_count]          # keep_count defaults to 1
    reclaim = invalid + valid[keep_count:]

The most-recent pre-update `state-snapshot` is a candidate in this same scan
(added in `historical_backup_candidates` as type `"state-snapshot"`). If any
other backup file has a newer mtime (e.g. a `transactions.db` copy stamped
later the same day), the snapshot falls into `reclaim` and is `shutil.rmtree`'d.

This violates the documented Safety Rule: *"The most recent snapshot is always
preserved (never auto-deleted)."*

### Symptom that hides the bug
After `--clean`, `clean_snapshots` reports `snapshots: freed 0.0 B` — but that
is because the snapshot dir is already empty (retention removed it first), so
there is nothing left to preserve. **A `0.0 B` snapshot line is NOT proof the
snapshot survived.** Verify the directory directly.

## Verification recipe (run AFTER every --clean)
1. Snapshot dir must be non-empty — check the PROFILE-SCOPED path:
   `ls -la <hermes-home>/profiles/<profile>/state-snapshots/`
   (for indigo the profile is `indigo`). The bare `<hermes-home>/state-snapshots`
   is a different, usually-empty directory — do NOT verify against it.
2. Find any dir >3 GB to confirm a large snapshot wasn't silently dropped:
   `find /root -maxdepth 4 -type d -exec du -sh {} + 2>/dev/null | awk '$1 ~ /G/ && $1+0 >= 3'`
3. Live DB integrity (resolve symlinks first):
   `sqlite3 <hermes-home>/data/styx.db "PRAGMA integrity_check;"`          # enriched Styx
   `sqlite3 <hermes-home>/data/transactions.db "PRAGMA integrity_check;"`  # live Plaid source
4. Confirm live DBs still present (not just backups):
   `find /root -iname 'transactions.db'` ; `find /root -iname 'styx.db'`

## Plaid source vs Styx DB (easy to confuse)
- `styx.db` = enriched Styx DB. Tables: `merchants`, `transaction_merchants`,
  `enrichment_runs`, `receipt_line_items`, `merchant_opaque_ids`.
- `transactions.db` = raw Plaid ingestion/source DB that Styx enriches.
  Tables: `accounts`, `plaid_items`, `sync_cursor`, `transactions`.
  Live path: `<hermes-home>/data/transactions.db` (`TXNS_DB` in
  `styx_chronicle_sync.py`). A `<fs-root>/backups/transactions.db` is only a
  *backup copy* of this source.
Do not mistake a retained `transactions.db` backup for the Styx DB, and do not
assume keeping it satisfies "back up Styx."

## Audit-trail limitation
genie prints only aggregate totals (e.g. "backup_retention: freed 26.6 GB / 27
files"). Deleted paths are NOT logged and files are unrecoverable (no git/LFS
on `<hermes-home>`). Capture `ls -la` of every backup class BEFORE `--clean`
if you need to answer "what was deleted" later.
