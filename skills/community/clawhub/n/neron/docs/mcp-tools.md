# Neron MCP — Tool Reference

Endpoint: `https://mcp.neron.guru/mcp`

---

## instructions
No params. Returns full API reference. **Call once per conversation.**

## get_stats
No params. Returns counts of all entity types.
```json
→ { "notes": 147, "tasks": 93, "people": 19, "projects": 8, "ai_notes": 48,
     "pending_tasks": 26, "relationships": 164, "moods": 42, "bodies": 12,
     "foods": 8, "activities": 70, "resources": 15, "reflections": 36 }
```

## search
```json
{ "query": "string",
  "types?": ["note","ai_note","person","project","task","mood","body","food","activity","resource","reflection"],
  "top_k?": 10 }
```
ILIKE text search. Default types: `[note, ai_note, person, project, task]`. Add extraction types explicitly if needed.

## semantic_search
```json
{ "query": "string",
  "types?": ["note","ai_note","person","project","task","mood","body","food","activity","resource","reflection"],
  "top_k?": 10,
  "format?": "short" }
```
Embedding-based vector similarity (Voyage AI). Searches all 11 entity types by default.
- Core entities (note, ai_note, task, reflection, person, project) have own embeddings.
- Extraction entities (mood, body, food, activity, resource) searched via parent note embedding JOIN.
- `format`: `"short"` (default) trims text to 150 chars. `"full"` returns complete text.
- Cross-language capable (Russian query matches English notes).

## search_notes
```json
{ "keywords?": "space separated", "day?": "YYYY-MM-DD", "limit?": 50 }
```
At least one of `keywords` or `day` required. Keywords use OR logic.

## list_entities
```json
{ "type": "person|project|task|ai_note|note|mood|body|food|activity|resource|reflection",
  "filters?": {},
  "limit?": 50 }
```
Filters by type:
- task: `{status?: "pending"|"in_progress"|"completed"|"cancelled", project_id?: int}`
- project: `{status?: "active"|"completed"|"paused"|"archived"}`
- ai_note: `{note_type?: "insight"|"summary"|"synthesis"|"question"|"action_item"}`
- mood/body/food/activity/resource/reflection: `{note_id?: int}`

## node_context
```json
{ "entity_type": "note|person|task|ai_note|mood|body|food|activity|resource|reflection",
  "entity_id": int,
  "depth?": 1 }
```
Returns focal node + full neighborhood via AGE BFS. Depth 1-3. Gracefully degrades if AGE unavailable.
```json
→ { "focal": {"type":"note","id":97,"data":{...}},
    "neighbors": {"mood:7": {...}, "activity:12": {...}},
    "edges": [...],
    "stats": {...} }
```

## create_entity
```json
{ "type": "person|project|task|ai_note|edge|note", "data": {...} }
```
Required fields:
- **note**: `{text}` — immutable after create
- **person**: `{name}` + optional `{aliases[], context, meta{}}`
- **project**: `{name}` + optional `{description, status, meta{}}`
- **task**: `{title}` + optional `{description, status, priority(1-10), due_at, project_id, meta{}}`
- **ai_note**: `{content}` + optional `{note_type, source_note_ids[], meta_tags[]}`
- **edge**: `{from_type, from_id, to_type, to_id, relationship}` + optional `{context, properties{}}`

Returns `{type, entity: {id, ...}}`.

## update_entity
```json
{ "type": "person|project|task|ai_note|edge", "id": int, "data": {...} }
```
Partial update — only passed fields change. Works on core entities only (not notes or extractions).

## delete_entity
```json
{ "type": "person|project|task|ai_note|edge|note", "id": int }
```
Cascades: deletes connected graph_edges. Note deletion also cascades to all extractions + AGE graph nodes.

## bulk_create
```json
{ "operations": [{"type": "task", "data": {"title": "..."}}, ...] }
```
Atomic transaction. Returns `{results[], errors[]}`.

## cypher
```json
{ "query": "MATCH ...", "verbosity?": "ids" }
```
Raw Cypher on Apache AGE. Verbosity levels:
- `"ids"` (default) — bare AGE results
- `"minimal"` — id + one identifying field per entity
- `"moderate"` — key fields, omitting confidence/dates from extractions
- `"full"` — complete relational data from DB tables

All levels except `"ids"` add an `"entities"` dict keyed as `"type:id"`.

**Node labels:** `Note{note_id}`, `Task{entity_id}`, `Person{entity_id}`, `Mood{entity_id}`, `Body{entity_id}`, `Food{entity_id}`, `Activity{entity_id}`, `Resource{entity_id}`, `Reflection{entity_id}`

**Edge types:** `HAS_MOOD`, `HAS_ACTIVITY`, `HAS_BODY`, `HAS_FOOD`, `HAS_REFLECTION`, `HAS_RESOURCE`, `MENTIONS`, `HAS_TASK`, `AFTER`

**IMPORTANT:** ORDER BY cannot reference aliases — repeat the expression:
```
GOOD: RETURN count(n) AS cnt ORDER BY count(n) DESC
BAD:  RETURN count(n) AS cnt ORDER BY cnt DESC
```
