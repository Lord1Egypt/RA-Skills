# Styx Delta: Dedup by `place_id` & Reconciliation (incident 2026-07-15)

## The failure
Ingesting a Styx delta via inline Python, the pre-check compared `name.lower().strip()`
against existing Taste items. This MISSED venues already modeled under a near-name:
- `"Taco Bell"` (Styx) vs existing `"Taco Bell Cantina"`
- `"Sidewalk Juice"` (Styx, SF) vs existing `"Sidewalk Juice- San Mateo"`

Both pairs share the **same canonical Google `place_id`**. Result: 5 duplicate items
+ 5 duplicate signals created for Beit Rima, Beretta, Sidewalk Juice, Rainbow Grocery,
Freshroll (Taco Bell was linked correctly only because its `place_id` was checked
manually — inconsistently). The ingestion script still reported "5 created, 6 signals
written" = success.

## The rule
At ingestion, dedup against existing Taste items by the **canonical `place_id`** returned
from Places — NOT by `item_id` or normalized `name`. For each new Styx transaction:
1. call Places textsearch (`{merchant} {city}`) → take first SF result → get `place_id`
2. if ANY existing item has that `place_id` → **LINK** the signal to it (bump
   `visit_count`, append `visit_dates`, recompute `avg_amount`). Do NOT create an item.
3. else create exactly ONE canonical item with that `place_id`.

## Verification (MANDATORY after every write)
Run `scripts/verify_taste_delta.py`. A "N created" success message from the ingestion
script is **not** proof of integrity — status is testimony, not action. The verify
script asserts: zero `place_id` collisions, zero `item_id` duplicates, zero orphaned
signals (signal `item_id` resolves to a real item), zero `(merchant_name, date)`
duplicate `source=styx` signals, and (optionally) exactly-one-item-per expected
`place_id`. It exits non-zero on any violation so a cron job can catch it.

## Reconciliation recipe (if duplicates already written)
1. **Back up `items.jsonl` and `signals.jsonl` FIRST.**
2. Build an explicit canonical map: for each venue, the verified `(item_id, place_id)`
   pair from a live Places lookup. Keep exactly one item record per canonical `place_id`.
3. Drop records whose `item_id` matches a canonical id but whose `place_id` is wrong
   (corrupted siblings), and drop duplicate `(item_id, place_id)` twins — prefer the
   record that has a `name`.
4. Repoint any signal whose `item_id` was dropped to the canonical `item_id` (this also
   repairs pre-existing orphans at the same venue).
5. Re-run `verify_taste_delta.py` until it exits 0.

### Gotcha — this is NOT `fix_styx_dedup.py`
`scripts/fix_styx_dedup.py` targets **truncation-variant** duplicates (different Styx
names -> same place). The `place_id`-sibling duplicate (same place, duplicate `item_id`
or a wrong-place sibling record) is a different shape — use the verify + manual-reconcile
recipe above, not `fix_styx_dedup` alone.