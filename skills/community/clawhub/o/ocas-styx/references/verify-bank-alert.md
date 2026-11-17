# Verifying a bank/credit alert against local Styx data

When a bank/card email alert claims a charge (e.g. "charged twice $155 on Jul 20"),
do NOT escalate to <operator> on the email alone. Cross-check the local Styx ledger
first. This catches stale/erroneous alerts and surfaces evidence <operator> needs.

## Locate the active ledger

The DB path has migrated over time. Do NOT trust a single hardcoded path.
Confirm via freshness:

```bash
# Find candidate ledgers anywhere under /root
find /root -name 'transactions.db' -not -path '*/node_modules/*' 2>/dev/null

# For each candidate, the ACTIVE copy = most-recently-modified AND non-empty
for db in <fs-root>/indigo-repo/data/transactions.db <backups-root>/transactions.db; do
  [ -f "$db" ] && printf "%s  mtime=%s  maxdate=" "$db" "$(stat -c %y "$db"|cut -d. -f1)" \
    && sqlite3 "$db" "SELECT MAX(date) FROM transactions;" 2>/dev/null
done
```

As of 2026-07-22 the live copy is `<fs-root>/indigo-repo/data/transactions.db`
(mtime 06:11, MAX(date)=2026-07-07). Older copies exist at `<backups-root>/`
and `<fs-root>/<agent-handle>-site-commons/indigo/data/`. Pick the most-recent mtime.

## Schema (transactions.db)

- `accounts` — `account_id, name, official_name, mask, type, subtype`
  (e.g. Savor credit card mask `1713`, account_id `gvvbkvE4xm…1713`)
- `transactions` — `account_id, transaction_id UNIQUE, amount, date, name,
  merchant_name, pending`
- `plaid_items` / `sync_cursor` — institution linkage + incremental-sync cursors

## Verification recipe

```sql
-- 1. Data freshness: does the ledger even cover the alert date?
SELECT MIN(date), MAX(date), COUNT(*) FROM transactions;

-- 2. Exact amount anywhere in history (tol ±$0.02)
SELECT transaction_id, account_id, amount, date, name, merchant_name
FROM transactions WHERE abs(amount - 155.0) < 0.02;

-- 3. All transactions on the alleged date
SELECT account_id, amount, date, name, merchant_name, pending
FROM transactions WHERE date = '2026-07-20' ORDER BY abs(amount) DESC;

-- 4. Card-mask check: does the alert's mask match a linked account?
SELECT official_name, mask, subtype FROM accounts WHERE type='credit';
SELECT * FROM transactions WHERE name LIKE '%1548%' OR account_id LIKE '%1548%';
```

## Interpretation patterns (from a real 2026-07-22 Capital One case)

- **Ledger lags the alert.** MAX(date)=2026-07-07 but the alert cites Jul 20 →
  local data is ~2 weeks stale for that window. Absence of the charge is NOT
  proof it didn't happen; flag as "unverifiable from local data."
- **Card-mask mismatch.** Alert cited Savor `…1548`; only linked Savor in Plaid
  is mask `…1713`. No `…1548` card exists → alert may reference an
  unlinked/different card or be erroneous.
- **Net result:** local data neither confirms nor denies; escalate to <operator>
  with BOTH the local findings AND the mask discrepancy so he can verify in-app.

## What finch/agent CANNOT do

Actual dispute, login, or financial decision requires <operator>. Mark task
`open`/`blocked_on_owner` and attach the verification notes.
