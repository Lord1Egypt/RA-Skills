# Taste multi-location brand merge (locations as metadata)

A recurring Taste data-quality problem: chains / multi-location venues (Ike's Love &
Sandwiches, Starbucks, Whole Foods, Little Star Pizza, Philz, Kasa Indian Eatery…)
arrive as **many separate `items.jsonl` rows**, one per location, each with its own
`place_id` and (after enrichment) its own Chronicle `Place` entity. This fragments
signal strength, duplicates recommendations, and breaks the 1:1 Taste↔Chronicle link.
The fix: collapse each brand into ONE canonical item, fold locations into a
`locations` metadata array, and point every Chronicle `Place` for that brand at the
single canonical entity via `merged_into`.

## Merge algorithm (Union-Find)

```
parent = {}
def find(x): parent.setdefault(x,x); ...path-compress...
def union(a,b): parent[find(a)] = find(b)

def norm(s): return re.sub(r"[^a-z0-9]","",(s or '').lower())   # DELETE punctuation, never space

for each pair (a,b) of distinct item_ids:
    pa = {place_id for rows of a}; pb = {...b}
    if pa & pb:                       union(a,b)        # same physical venue
    elif norm(name_a) and norm(name_a) == norm(name_b): union(a,b)  # same brand, diff locations
```
Components of size>1 that contain ≥1 `place_id` are brands to merge. (Name-only unions
are safe here: every flagged pair was a real multi-location brand, not an unrelated
collision. Confirm by checking the pair's `place_id`s differ — that's expected for
true multi-location brands.)

### Canonical selection (one row survives)
Prefer, in order: id starts with `item-` (not a UUID) → `enriched:true` → most linked
signals → first seen. Keep the canonical display `name` (geocoder display names are
unreliable for truncated Styx names — never overwrite).

### Fold locations
```
canon['locations'] = [ {place_id, name, address, city, neighborhood, chronicle_id}
                       for each distinct place_id across all member rows ]
```
Then remap every signal whose `item_id` was a folded member to the canonical `item_id`.

### Chronicle side (keep the link intact)
- Canonical `Place` entity gets a `locations` fact: `predicate_canonical="locations"`,
  body = JSON of the locations array (idempotent via `qualifiers_hash({"source":"taste_merge"})`).
- Every secondary `Place` entity for the brand → `store.update_belief("entities", sec, merged_into=canon_belief_id)`.

## ⚠️ CRITICAL rewrite bug (hit 2026-07-14)
When rewriting `items.jsonl`, do NOT do `keep_ids = all_ids - remap.keys()` then append
canonical items. The canonical id is NOT in `remap`, so its ORIGINAL rows survive AND you
append a fresh canonical → the brand ends up DOUBLED (duplicate `item_id` rows, signals
still pointing at folded ids, dangling Chronicle `external_ref`s).
**Correct:** exclude EVERY id that is a member of any merged component (canon + folded),
then append exactly one canonical item per brand:
```
merged_member_ids = {m for members in multi.values() for m in members}
new_items = [it for it in items if it['item_id'] not in merged_member_ids] + canonical_items
```

## Verification after merge
- `len(items) == len(distinct item_ids)` and zero duplicate `item_id`s.
- Canonical items carry `locations` (count == number of merged brands).
- `signals.jsonl`: zero signals still pointing at a folded/deduplicated id.
- Chronicle: `COUNT(*) FROM entities WHERE type='Place' AND merged_into IS NOT NULL` ==
  number of secondary entities; `locations` facts == number of merged brands.
- Forward integrity: every Taste-linked Chronicle `Place.external_ref` is a CURRENT
  Taste `item_id` (no dangling refs to folded rows).
- Reverse integrity: every Taste item `chronicle_id` resolves to a `Place` whose
  `external_provider='taste'` and `external_ref` == that item's `item_id`.

## Runnables
Reusable script: `<fs-root>/indigo_tmp/phase4_merge.py` (Union-Find + canonical pick +
Chronicle `merged_into` + `locations` fact; `--apply` writes, default is dry-run).
Pair with `phase1_people.py` / `phase2_places.py` / `phase3_enrich.py` for the full
Taste↔Chronicle linkage pipeline.