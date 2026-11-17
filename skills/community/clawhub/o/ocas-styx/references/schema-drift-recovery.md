# Styx Schema Drift — Recovery Recipe

## Symptom
`python3 skills/ocas-styx/scripts/styx_universal_enrich.py [--dry-run]` crashes:
```
sqlite3.OperationalError: no such column: geo_source
```
at the `SELECT city, state, geo_source FROM merchants WHERE id=?` line.

## Root cause
1. `styx_common.init_styx_db()` builds the schema with `CREATE TABLE IF NOT EXISTS` from
   `SCHEMA_DDL`. On a pre-existing DB, missing tables/columns are never added.
2. `SCHEMA_DDL` itself is **out of sync** with the scripts: it defines only
   `merchants`, `transaction_merchants`, `enrichment_runs` and omits:
   - `merchants.geo_source`, `merchants.plaid_city`, `merchants.plaid_region`,
     `merchants.merchant_entity_id` (written by `styx_universal_enrich.py`)
   - the entire `transactions` table (written by `store_transaction()` in
     `styx_common.py` and `plaid_sync.py`, and read by the enrich COALESCE join).
3. `STYX_DB` (`<hermes-home>/data/styx.db`) is a **symlink** to a git-tracked file
   (`<repo-root>/data/styx.db`). Opening it in separate processes can race, so an
   `ALTER` in one `terminal()` call may not be visible to the enrich run in the next.

## Diagnosis
```bash
DB=<fs-root>/indigo-repo/data/styx.db   # resolve the symlink target first
python3 - "$DB" <<'PY'
import sqlite3,sys
c=sqlite3.connect(sys.argv[1])
print("tables:", [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")])
print("geo_source present:", 'geo_source' in [r[1] for r in c.execute("PRAGMA table_info(merchants)")])
print("transactions present:", 'transactions' in [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")])
c.close()
PY
```
Confirm `STYX_DB` is a symlink: `ls -la <hermes-home>/data/styx.db`.

## Fix
Run the idempotent migration script (additive — safe to re-run):
```bash
python3 skills/ocas-styx/scripts/migrate_styx_schema.py
```
It adds the 4 missing `merchants` columns if absent and reports whether the
`transactions` table is missing. **Crucial:** do the migration and the enrich run in the
SAME process (chain them in one `terminal()` call) so the symlinked git-tracked target
can't revert between calls:

```bash
python3 - <<'PY'
import sqlite3, subprocess, sys
DB="<hermes-home>/data/styx.db"
c=sqlite3.connect(DB, timeout=30)
cols={r[1] for r in c.execute("PRAGMA table_info(merchants)")}
for n,t in [("geo_source","TEXT"),("plaid_city","TEXT"),("plaid_region","TEXT"),("merchant_entity_id","TEXT")]:
    if n not in cols: c.execute(f"ALTER TABLE merchants ADD COLUMN {n} {t}")
c.commit(); c.close()
r=subprocess.run([sys.executable,"skills/ocas-styx/scripts/styx_universal_enrich.py"],
                 capture_output=True, text=True, timeout=220)
print(r.stdout[-1500:]); print("rc", r.returncode)
PY
```

## The `transactions` gap (NOT auto-fixed)
The `transactions` table is absent from both the live DB AND `SCHEMA_DDL`. Until it exists,
Plaid sync (`plaid_sync.py` → `store_transaction`) cannot persist raw transactions, and the
enrich COALESCE subquery (`JOIN transactions t ON ...`) has no source rows. A dispatcher
reporting "N new transactions" therefore has nothing to enrich. The correct `transactions`
DDL must be reconciled from `store_transaction()` into `SCHEMA_DDL` by a code change — the
migration script only flags it; it does not guess the schema.

## Verification after fix
- `geo_source present: True`
- enrich run completes (dry-run prints the 8-candidate merchant list; live run shows
  `Enriched: N / Failed: M`). Garbled bank strings ("SP THANKS ICON", "Citi Autopay -
  Payment Withdrawal") legitimately return `no_result` from Google Places — that is expected,
  not a failure of the migration.
- `git -C <fs-root>/indigo-repo status --short` will show `M data/styx.db` from the ALTER.
