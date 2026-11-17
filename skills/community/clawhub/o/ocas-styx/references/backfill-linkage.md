# Backfill & Enrichment Linkage (Styx)

## Incident (2026-07-07)
- Bank feed stalled: `MAX(date)` in `transactions.db` = 2026-06-24. User asked "what new restaurant data did I get from my MA trip."
- Manual `/transactions/get` backfill recovered **162 new transactions** (MAX → 2026-07-07); cursor reset.
- `styx_universal_enrich.py` then reported `Enriched: 0 / Failed: 8` — because the backfill wrote only raw `transactions.db` rows; no `merchants`/`transaction_merchants` rows existed for the new txns. The universal enricher only resolves merchants already present in `styx.db`.
- Fix: a custom linker created `merchant` + `transaction_merchants` rows (keyed by normalized RAW name), then Google Places enrichment resolved names/addresses. See `scripts/styx_backfill_link_enrich.py`.

## Gotcha 1 — backfill doesn't link
The canonical `plaid_sync.py` does link + enrich together. A standalone `/transactions/get` backfill does NOT. After any manual backfill, link new txns into `styx.db` before running the universal enricher.

## Gotcha 2 — `name` asterisks are masking, not redaction
`******** BURGERS & BBQ` → the `4505` prefix was masked to asterisks. `merchant_name` = `Burgers & Bbq` (clean). Use `merchant_name`; never drop masked-prefix rows as "redacted." Fully-redacted `***************` (NULL `merchant_name`) is the only true redaction case.

## Gotcha 3 — Google Places geo is unreliable for niche venues
- Unbiased text search: `Rosies Cantina` → Alabama; `Twisted Pizza` → Rhode Island; `Kleins Deli` → CA (SF); `Little Vie` → LA. All are Provincetown.
- Location-biased (Provincetown): fixed those, but broke SF brands — `4505 Burgers & BBQ` → "Off the Grid" MA; `Bacon Bacon` → a Ptown cafe; `Lulu Green` → MA.
- Lesson: don't trust auto `state`. Verify distinctive venues against the known trip location. User confirmed `4505 Burgers & BBQ` = San Francisco.

## Hybrid approach that worked
- Bias to trip location ONLY for merchants whose raw name carries a location cue (PROVINCETOWN / PTOWN / AWOL) or known-local venues.
- Use unbiased (global prominence) for well-known brands — they resolve to their true home city.
- Manually correct the 2–3 that still mismatch, then persist.

## Verify after backfill
```sql
-- raw side
SELECT MAX(date), COUNT(*) FROM transactions;
-- linked + enriched side
SELECT m.name, m.state, COUNT(*) FROM merchants m
  JOIN transaction_merchants tm ON tm.merchant_id=m.id
  GROUP BY m.id ORDER BY m.state;
```