# Taste dedup matching — normalization pitfalls

Condensed from a real incident (2026-07-07 MA-trip feed) where the Styx→Taste
feed created duplicate items for venues that already existed in Taste.

## Key hierarchy (PRIMARY = place_id, NOT name)

The unique venue ID is **Google `place_id`** (a real UUID, globally unique per
physical venue). Names are a *fallback* key only, used solely for rows that have
no `place_id`. User directive 2026-07-14: "Use Place ID then as the unique ID,
not names." Consequences:

- **Never dedup primarily on name.** Two distinct venues can normalize to the
  same name (Beretta vs Beretta Valencia vs Beretta Divisadero); name-only merges
  are wrong unless every member also lacks a `place_id`. Prefer `place_id` for the
  union/fold key; only fall back to exact normalized-name matching for the
  keyless minority.
- **Slugs are fragile.** `item-<slug>` ids derived from names break on any rename
  or multi-location split. They are NOT stable identifiers.

## Rekeying keyless rows (the fix when a row has no place_id)

For the place_id-less minority (unenrichable / non-venue rows), assign a stable
UUID so every item has a durable primary key instead of a slug:

```python
import uuid
new_id = f"venue_{uuid.uuid4().hex}"
it["legacy_item_id"] = it.get("item_id")   # preserve old slug for traceability
it["item_id"] = new_id
```

Then fold any internal name-duplicate groups among the keyless rows (exact
normalized name, all members lacking place_id), merge their `locations`, remap
the sibling store's signals (`item_id` → new id), and remap any dependent-store
external_ref (e.g. Chronicle `external_ref`). A reusable, parameterized
implementation lives at `eng-database-ops/scripts/rekey_keyless.py`.

**Order matters:** build the fold map using the PRESERVED `legacy_item_id` (old
slug), NOT `item_id` — because rekeying mutates `item_id` first, so reading
`item_id` post-rekey yields the new `venue_` id and the fold/signal remap breaks.
Capture old ids before rekeying.

## The original normalization bug (kept for context)



A first-pass feed matched existing Taste items only by exact
`venue_name.lower().strip()`. Two failures resulted:

1. **Apostrophe/space normalization.** Normalizing with
   `re.sub(r"[^a-z0-9 ]", " ", name)` replaces the apostrophe in `bernie's`
   with a *space*, yielding `bernie s general store` → tokens
   `{'bernie', 's'}`. The styx merchant `Bernies Provincetown` normalizes to
   `{'bernies'}`. These never match, so a brand-new item
   (`Fanizzi's Restaurant - Provincetown, MA` — the geocoder's wrong display
   name) was created on top of the existing `Bernie's General Store`.

2. **`venue_name` vs `name`.** The existing Bernie's item carried the venue
   only under `name` (`name="Bernie's General Store"`, `venue_name=None`), so
   it was absent from the `venue_name`-keyed index entirely.

## The fix

- **Delete punctuation, don't space it:** `re.sub(r"[^a-z0-9 ]", "", name)`.
  `bernie's` → `bernies`. This is the single most important change.
- **Index BOTH `name` and `venue_name`** when building the existing-item map.
- **Triple-key match:** place id, then token-subset match across
  (`name` ∪ `venue_name`). Token-subset (not just exact) catches
  `bacon` ⊂ `bacon bacon` and `bernies` == `bernies`.
- **Never overwrite the existing `name`.** The geocoder's display name is
  unreliable for truncated/stylized styx names (returned `Fanizzi's` for
  Bernie's). Keep the existing display name; only fill missing enrichment
  fields (address, rating, price, cuisine, neighborhood, place id, city).
- **City is Plaid-authoritative.** Use `styx.merchants.city` as the item city.
  The geocoder is queried only for venue *attributes* (cuisine/rating/price/
  address) — it must never override the city. This is what prevents the
  Bernie's→Quincy / Bacon→Redmond class of error.
- **Idempotent signals.** Dedup by `styx:{merchant_lower}:{date}`; re-runs are
  safe (a second run adds 0 or skips already-present signals).

## Reusable normalization snippet

```python
import re

def norm_tokens(name):
    n = (name or '').lower()
    n = re.sub(r"[^a-z0-9 ]", '', n)   # DELETE punctuation, never space it
    drop = {'provincetown', 'sfo', 'san', 'francisco', 'boston', 'oakland',
            'berkeley', 'ca', 'ma', 'sf', 'restaurant', 'bar', 'cafe', 'llc',
            'inc', 'general', 'store', 'deli', 'pizza', 'coffee', 'cantina',
            'heaven'}
    return set(t for t in n.split() if t and t not in drop)
```

The full runnable feed (geocoder call + write) should live at
`scripts/styx_taste_feed.py`; its geocoder URL / credential must be injected by
the runner's environment because the skill writer strips any file containing
those literals.

## Verification checklist after any feed

- `wc -l items.jsonl` increased by exactly the number of *new* venues (existing
  venues should be UPDATE, not CREATE).
- No two items share a `venue_name` for the same city.
- Every new item has `enriched: true` and a place id set (so future feeds
  dedup by place id).
- Trip-window signal count == number of trip transactions.