# Plaid Location Backfill + Merchant-Geo Reconciliation

Verified procedure (run 2026-07-07). Fixes the case where `transactions.loc_*`
columns exist but are empty because historical rows were ingested before
provenance capture, and reconciles `merchants` geography to Plaid (source of
truth) without degrading clean Google cities.

## Why this exists

A transaction's point-of-sale geography from Plaid (`location.city`/`region`) is
**authoritative when present**. Google name-geocoding is the fallback only when
Plaid `location` is null. The original pipeline dropped Plaid's `location` on
ingest (and Google's name search sent Cape Cod venues to the wrong state, e.g.
Bernie's → Quincy). Backfilling Plaid `location` corrects this at the source.

## Verified coverage (authoritative re-pull, 1,344 txns, 2026-02..2026-07)

| channel    | with location | total | pct   |
|------------|---------------|-------|-------|
| in store   | 90            | 862   | 10.4% |
| online     | 2             | 373   | 0.5%  |
| other      | 5             | 225   | 2.2%  |

**Takeaway:** location is a card-present signal; `online` never has it. Backfill
fetches every month but only STORES `location` where Plaid returns it — `online`
rows staying NULL is correct, not a miss.

## Step 1 — Backfill `transactions.loc_*` month-by-month

`scripts/styx_backfill_location_monthly.py` iterates every month from
`MIN(date)` to today, calls `/transactions/get` per Plaid item per month, and
`UPDATE`s `loc_*` on existing rows (keyed by `transaction_id`) only when Plaid
returns a location. It never inserts new transactions.

```bash
cd <hermes-home>/profiles/indigo/skills/ocas-styx/scripts
/usr/bin/python3 styx_backfill_location_monthly.py --dry-run   # observe pattern, write nothing
/usr/bin/python3 styx_backfill_location_monthly.py             # real run
```

- Secrets loaded at runtime from `<hermes-home>/secrets/plaid.env` (never
  hardcoded).
- Prints per-month enrichment counts and a final channel x coverage cross-tab
  from Plaid's *authoritative* responses (not just our DB).
- Result this run: 6 → 87 transaction rows with Plaid location.

## Step 2 — Reconcile `merchants` geography from Plaid (guarded)

`scripts/styx_reconcile_merchant_geo.py` adds provenance columns to `merchants`
and reconciles geography. **Critical guard:** it only overrides `merchants.city`/
`state` when BOTH `plaid_city` and `plaid_region` are present. Truncated /
neighborhood-only Plaid values (`Francisco`, `Flower`, `Mission`, `Van Ness`,
`Redwood`) are written as `plaid_*` provenance only — never into `city` — so a
clean Google city is never degraded into `Francisco`.

```bash
cd <hermes-home>/profiles/indigo/skills/ocas-styx/scripts
/usr/bin/python3 styx_reconcile_merchant_geo.py --dry-run
/usr/bin/python3 styx_reconcile_merchant_geo.py
```

### Cross-DB join gotcha (why the old script broke)

`transaction_merchants` lives in `styx.db`; `transactions` lives in
`transactions.db`. They share `transaction_id` but are separate files. The
reconcile script must `ATTACH DATABASE ? AS txn` into the `styx` connection and
join `transaction_merchants tm JOIN txn.transactions t ON ...`. The deprecated
`styx_refresh_plaid_location.py` queried `transactions` directly as if same-DB
and also referenced `merchants.plaid_city`/`geo_source` before they existed.

### Result this run

- Added `plaid_city`, `plaid_region`, `geo_source` to `merchants`.
- 21 merchants overridden with complete Plaid locations (city+region present).
- 38 merchants got `plaid_*` provenance recorded.
- Zero truncated values leaked into `city` (verified).

## Verification

```sql
-- transactions with Plaid location
SELECT COUNT(*) FROM transactions WHERE loc_city IS NOT NULL OR loc_region IS NOT NULL;
-- trip proof: Cape Cod ATM resolves to Provincetown, MA from Plaid
SELECT date, merchant_name, loc_city, loc_region FROM transactions
  WHERE loc_region='MA' ORDER BY date;
-- merchants reconciled to Plaid
SELECT COUNT(*) FROM merchants WHERE geo_source='plaid';
-- guard check: no truncated city slipped into merchants.city
SELECT name, city FROM merchants WHERE geo_source='plaid'
  AND city IN ('Francisco','Flower','Mission','Van Ness','Redwood');
```

## Caveats

- **Some merchants have NO Plaid location** (Plaid doesn't geocode niche
  markets, e.g. Bernie's General Store in Provincetown). Plaid can't place them
  directly; sibling trip transactions prove the location instead. Google
  geocoding (fallback) is then the only signal — verify distinctive venues
  against the known trip area.
- Forward capture already works: `store_transaction` (styx_common.py) writes
  `loc_*` on every ingest, and `plaid_sync.py` calls it for added/modified txns.
  No live-sync change needed.
- The **Taste model** (`ocas-taste`) keeps its own venue geography and was the
  actual source of the Quincy/Redmond recommendation error. To fix there, wire
  Taste to read Plaid `transactions.loc_*` instead of name-based Google geocode.