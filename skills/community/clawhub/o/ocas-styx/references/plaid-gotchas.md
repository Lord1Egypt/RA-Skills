# Plaid Sync Gotchas & Recovery

## Sync Cursor Can Get Stuck

**Symptom**: Daily `/transactions/sync` runs return +0 added, ~0 modified, -0 removed for all institutions, but transactions are visible in the bank UI.

**Cause**: The cursor advances past a gap in Plaid's data feed. This happens when:
- Plaid's backfill catches up and the cursor jumps ahead
- A bank connection has a temporary gap in data availability
- The initial historical pull didn't get all transactions

**Diagnosis**:
```bash
# Run sync manually and check output
python3 <hermes-home>/profiles/indigo/scripts/plaid_sync.py
# If all institutions return 0, the cursor may be stuck
```

**Fix — Backfill via `/transactions/get`**:
1. For each institution, call `/transactions/get` with date range covering the gap
2. Insert any `transaction_id` values not already in the DB
3. Delete sync cursors: `DELETE FROM sync_cursor WHERE item_id = ?`
4. The next `/transactions/sync` run will re-establish the cursor from current

## Plaid Data Lag

Transactions visible in your bank's web UI or app may not appear in Plaid's API for **1-3 days**. This is normal. If you see a transaction in the bank but not in Plaid:

- Wait 24-48 hours for Plaid to ingest it
- The daily 7 AM sync cron will pick it up automatically once available
- Do NOT reset cursors just because a single recent transaction is missing

## Merchant Name Prefixes

When searching for transactions, be aware of processor prefixes in Plaid's `name` field:

| Prefix | Processor | Common For |
|--------|-----------|------------|
| `TST*` | Toast POS | Restaurants, cafes |
| `DD *DOORDASH` | DoorDash | Food delivery |
| `SQ*` | Square | Small retail, cafes |
| `SP*` | Stripe | Online/subscription |
| `ABM*` | ABM (parking) | Parking garages |

**Lesson**: Searching for "tiya" missed `TST*TIYA MARINA`. Always try processor prefixes when merchant name search fails.

## Pagination Limits

- `/transactions/get`: max 500 per request, paginate with `offset`
- `/transactions/sync`: pages by cursor, max ~100 per page, oldest-first

## Key Paths

- Sync script: `<hermes-home>/profiles/indigo/scripts/plaid_sync.py`
- Raw DB: `<hermes-home>/data/transactions.db`
- Enriched DB: `<hermes-home>/data/styx.db`
- Credentials: `<hermes-home>/secrets/plaid.env`
