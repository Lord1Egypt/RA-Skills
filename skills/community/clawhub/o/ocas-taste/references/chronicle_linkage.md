# Taste ↔ Chronicle bidirectional place linkage

Taste places (restaurants, hotels, venues) must exist in BOTH Taste and Chronicle and
be linked bi-directionally — the same model Weave people use. General Chronicle API +
gotchas live in the `chronicle-linkage` skill; this file is the Taste-specific recipe.

## Match + create + link (core pass)

For each Taste item that is restaurant/hotel/venue-flavored (category in
`{restaurant,cafe,bakery,bar,meal_takeaway,meal_delivery,food,travel,doordash}` OR
domain in `{restaurant,food,travel}` OR `types` intersects
`{restaurant,cafe,bar,lodging,hotel,tourist_attraction,point_of_interest,establishment,...}`):

1. Must have a stable key: `place_id` (Google). If missing, enrich first (Google Places
   legacy GET — v1 POST returns 400 from inline Python; use `maps.googleapis.com/maps/api/place/textsearch/json?query=<name+city>&key=...`).
2. `nnm = re.sub(r'[^a-z0-9]+','_', (normalized_name or venue_name or name).lower()).strip('_')`.
3. If `nnm` matches an existing Chronicle `Place` (not yet taste-linked): link to it.
   Else create `belief_id = f"taste_{item_id}"` via `store.upsert_belief("entities", {...})`.
4. On the Chronicle entity: `store.update_belief("entities", bid, external_provider="taste", external_ref=item_id)`.
5. Write join-key fact: `predicate_canonical="google_place_id"`, body=`place_id`
   (idempotent via `qualifiers_hash({"source":"taste"})`).
6. Add `it["chronicle_id"] = bid` and rewrite `items.jsonl`.

Dedup by `place_id` so repeated Taste items for one venue don't spawn multiple entities.

## Scope rule

If you link Taste, also confirm the **people (Weave)** mapping is complete — the user
expects sibling stores fixed in the same pass, not left half-linked.

## Verify

`scripts/verify_linkage.py --provider taste` (in the `chronicle-linkage` skill) —
counts both directions + 5-row integrity sample. Expect Forward == number of
Chronicle Places with `external_provider='taste'`, Reverse == Taste items with
`chronicle_id` (a few items may share one `place_id`, so Reverse can exceed Forward).

## Chronicle engine API shapes (reverse-engineered 2026-07-14)

The `chronicle-linkage` skill is the canonical home for the generic API, but the exact
call shapes that worked inline this session are recorded here so the next pass doesn't
re-derive them:

- **Load engine:** `sys.path.insert(0,"<hermes-home>/plugins/chronicle")` then
  `from engine.store import MemoryStore; from engine.reducer import Reducer;
  from engine.capture import CaptureEngine`.
  `store=MemoryStore(CHRON); store._conn().execute("PRAGMA busy_timeout=90000")`
  `red=Reducer(store, embedder=None); store.reducer=red; cap=CaptureEngine(store, red)`.
- **`upsert_belief` is on `store`, NOT `Reducer`.** `red.upsert_belief(...)` →
  `AttributeError`. Use `store.upsert_belief("entities", {...})`.
- **`entities` table has NO `status` column.** Queries like
  `SELECT ... WHERE status='active'` on `entities` fail. Facts DO have `status`.
- **Set forward link WITHOUT re-emitting events:** `store.update_belief("entities", belief_id,
  external_provider="taste", external_ref=item_id)`. The `external_ref`/`external_provider`
  fields are written from the entity payload `key` (see `reducer._insert_belief` entity branch)
  — `update_belief` patches them directly.
- **Create a new entity:** `store.upsert_belief("entities", {"belief_id": f"taste_{item_id}",
  "type":"Place","name":name,"normalized_name":nnm,"aliases":"[]","domain":"user",
  "owner":"default","read_acl":"public","external_ref":item_id,"external_provider":"taste",
  "fact_count":0,"relationship_count":0,"created_at":now,"last_seen_at":now})`.
  Idempotent: if `normalized_name`+`type`+`owner`+`domain` already exists, `upsert_belief`
  matches the existing row instead of duplicating.
- **Join-key fact:** `predicate_canonical="google_place_id"`, body=`place_id`, idempotent
  via `qualifiers_hash({"source":"taste"})`. Use a cursor (`cur=store._conn().cursor()`),
  NOT the raw connection, for `execute`/`fetchone` (`sqlite3.Connection` has no `fetchone`).
- **Merge a duplicate entity:** `store.update_belief("entities", belief_id, merged_into=canonical_belief_id)`.
- **Read raw:** `cur.execute(...)`; the `entities` row exposes `belief_id, type, name,
  normalized_name, external_ref, external_provider, merged_into, fact_count`.

## ⚠️ BACKUP A WAL-MODE SQLite DB BEFORE WRITING (corruption incident 2026-07-14)

`chronicle.db` runs in WAL mode — committed transactions live in `chronicle.db-wal`
until checkpointed. Copying ONLY `chronicle.db` (the main file) is NOT a safe backup:
the `-wal` holds uncheckpointed writes, and a `cp` of an open DB can snapshot an
internally inconsistent main file. **A phase-4 merge run then wrote to the live DB and
corrupted the main file's b-tree** (`PRAGMA integrity_check` → "Rowid out of order /
btreeInitPage() returns error code 11"). Recovery required restoring a PRE-WORK backup
and re-running all phases from scripts.

Safe backup recipe (copy the WAL too, or checkpoint first):
```
cp chronicle.db backup/chronicle.db
cp chronicle.db-wal backup/chronicle.db-wal   # if present
# OR checkpoint to fold the WAL into the main file first:
sqlite3 chronicle.db "PRAGMA wal_checkpoint(TRUNCATE);"
cp chronicle.db backup/chronicle.db
```
Also: the 3.3 GB `chronicle.db` `cp` exceeds the 60s foreground terminal limit — run
backups in `terminal(background=True, notify_on_complete=True)`, never with `&` inside a
foreground command (the guard blocks it). Verify a backup by opening it
(`SELECT COUNT(*) FROM entities WHERE type='Place'`) — a pre-work base should open with
the known pre-write place count (e.g. 300 before any Taste linking).

## People (Weave) mapping — also fix in the same pass

The user expects sibling stores fixed together, not left half-linked. The Weave↔Chronicle
person mapping had: forward link present (Chronicle `Person.external_ref`=Weave UUID,
`external_provider='weave'`) but the reverse `chronicle_id` back-link in Weave
`node_properties` was ~empty (8/1064). Fix: write `chronicle_id` into Weave
`node_properties` for every matched person (canonical = older `ent2_*` belief_id), mark
empty `kg_*` duplicate Chronicle persons `merged_into` their `ent2_*` canonical, and
create Chronicle `Person` entities for Weave orphans. Always back up first.

## Multi-location brand merge

Chains arrive as many separate `items.jsonl` rows (one per location) plus many Chronicle
`Place` entities. Collapse each brand into ONE canonical item with a `locations` metadata
array and point the secondary Chronicle entities at it via `merged_into`. Full recipe +
the critical rewrite-double-bug: see `references/multilocation_merge.md`.