# Styx Data Provenance

## HARD RULE (2026-07-07, user correction)
Plaid is the **source of truth** for Styx transaction data. Preserve ALL Plaid
fields on ingest (`merchant_id`, `merchant_entity_id`, full `location`:
address/city/region/postal/lat/lon). Google enrichment is **ADDITIVE only** —
it supplements (cuisine, rating, price, display address) but must NEVER discard
or override Plaid data. Plaid transaction `location` is the authoritative
geolocation when present; Google geocoding is the fallback only when Plaid
`location` is null.

## Why this matters
The ingest paths (`store_transaction` in styx_common.py, the raw INSERT in
styx_backfill_link_enrich.py) originally captured only a subset of fields and
**dropped `location` and `merchant_id` entirely**. For a Massachusetts trip the
result was wrong Google geocodes (Bernie's → Quincy, Bacon Bacon → Redmond)
because the correct Plaid POS location was never stored. User: "Data provenance
is key, you should never throw it away. Plaid data is the source of truth you
enrich on top of not replace."

## Plaid `location` facts (verified 2026-07-07)
- Field key for longitude is **`lon`**, not `lng`. Code reading `loc.get('lng')`
  stores NULL longitude. Use `loc.get('lon')`.
- `location` is **sparse**: ~2% of transactions carry a non-null city for this
  account (6/384 in a month: SF×3, Palo Alto×1, Provincetown×1, San Rafael×1).
  Do NOT assume Plaid geolocates a purchase. Google remains the primary
  geocoder; Plaid wins only for the rare populated rows.
- Each transaction also exposes `merchant_entity_id` (modern stable merchant
  ID — prefer over legacy `merchant_id` for the merchant-mapping),
  `counterparties` (may carry addresses), `logo_url`, `website`. Capture these
  before falling back to Google.

## Schema (provenance columns, ALTER-added 2026-07-07)
- `transactions.merchant_id`, `loc_address`, `loc_city`, `loc_region`,
  `loc_postal`, `loc_country`, `loc_lat`, `loc_lng`.
- `merchants.plaid_merchant_id`, `plaid_city`, `plaid_region`, `plaid_postal`,
  `plaid_country`, `plaid_lat`, `plaid_lng`, `geo_source`
  (`'plaid'` | `'google_places'`).

## Ingest paths that must capture provenance
- `styx_common.store_transaction(conn, tx, account_id)` — INSERT OR REPLACE into
  transactions incl. merchant_id + location (reads `loc.get('lon')`).
- `styx_backfill_link_enrich.py` — raw INSERT captures merchant_id + location;
  enrichment sets `merchants.city/state` from Plaid `loc_*` (authoritative) and
  falls back to Google only when Plaid null; writes `geo_source`.
- `plaid_sync.py` — calls `store_transaction`, so it inherits the capture.

## Backfilling location onto EXISTING transactions
The regular backfill skips already-inserted rows, so trip txns ingested before
provenance capture have NULL `loc_*`. Use:
```
python3 <hermes-home>/profiles/indigo/skills/ocas-styx/scripts/styx_refresh_plaid_location.py \
    --start-date 2026-06-25 --end-date 2026-07-07
```
It `UPDATE`s Plaid `merchant_id` + `location` onto existing raw rows (does not
re-insert), then reconciles `merchants` geographies from Plaid
(`geo_source='plaid'`). Idempotent — safe to re-run per window.

## Verification pattern (per user: "spot check the last month")
- Count txns with non-null `loc_city` vs total in window → coverage %.
- Cross-DB join (ATTACH transactions.db to styx.db) to list trip food merchants
  with `city`/`state`/`plaid_city`/`geo_source`; eyeball for mislocated venues.
- Trip venues (23) verified correct after fix: Provincetown MA, San Francisco
  CA, Oakland, Boston, Berkeley — no mislocations. One minor edge case:
  `Filmmakers Collaborative → Melrose, MA` (non-trip, likely real org).