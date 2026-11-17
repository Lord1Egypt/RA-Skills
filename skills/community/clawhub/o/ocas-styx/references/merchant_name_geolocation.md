# Merchant-name locale hints for geolocation

When Plaid `location` is null (the common case — only ~6–10% of card-present
txns carry it; online txns effectively never), the best geolocation signal is
often **already inside Plaid's `merchant_name` / raw `name`**.

## Why bare-name geocoding fails
Google Places text search returns the globally-most-prominent match when the
query has no location context. So:
- `Bernie's General Store` → Quincy, MA (a different, more-prominent Bernie's)
- `Bacon Bacon` → Redmond, OR (a copycat)

## The fix: extract the locale token
Payment processors append location tokens to transaction names. Parse them from
`merchant_name` / `name` and use as the Google query bias:

| Raw / merchant_name | Token | Resolves to |
|---|---|---|
| `BERNIES PROVINCETOWN P` / `Bernies Provincetown` | Provincetown | Provincetown, MA ✓ |
| `TST*BACON BACON - SFO` (raw) | SFO | San Francisco, CA ✓ |
| `MS* AWOLPROVINCETOWN` | Provincetown | Provincetown, MA ✓ |
| `DISTRICT MARKET @SFO 6` | SFO | SFO Terminal 3 ✓ |

Query form: `f"{display_name} {city} {state}"` (e.g. `"Bernies Provincetown Provincetown MA"`).

## Hierarchy (in priority order)
1. **Plaid `location`** (loc_city/region/lat/lng) when non-null → authoritative.
2. **Plaid `merchant_name` locale hint** → Google with locale-aware query.
3. **Google bare-name** fallback (United States) — only for merchants with no
   Plaid signal and no locale token; expect occasional wrong-branch matches for
   multi-location businesses (e.g. Rosies Cantina → Huntsville AL, Philz → Glendale CA).
4. **National/online** merchants (Amazon, Spotify, Uber, banks) → skip geocoding.

## Implementation
`scripts/build_merchant_master.py` applies this hierarchy over ALL
transactions.db rows and writes `<hermes-home>/data/merchants.db`.
`geo_source` records which tier won (`plaid` / `name_hint+google` /
`google_name` / `national_skip` / `google_fail`).

> Pitfall: `styx_places_enrich.py` hardcodes `city="San Francisco"` as its Google
> default bias — mis-geocodes non-SF merchants. Use `build_merchant_master.py` or
> `styx_universal_enrich.py` for trips/non-SF backfills.

## Known residual mis-geocodes (bare-name tier)
Multi-location brands where Google returned the wrong branch — correct manually
if exactness matters: `Rosies Cantina` (→ Provincetown, not Huntsville AL),
`Philz Coffee` (→ SF, not Glendale CA).