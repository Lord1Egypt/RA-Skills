# Ingestion Pipeline

## Journal source paths

Elephas reads from two sources per ingestion pass:

1. Skill journals: `~/openclaw/journals/{skill-name}/YYYY-MM-DD/{run_id}.json`
   Walk all skill directories under `~/openclaw/journals/`. Process any `.json` file whose `run_id` does not appear in the ingestion log at `~/openclaw/db/ocas-elephas/ingestion_log.jsonl`.

2. Signal intake: `~/openclaw/db/ocas-elephas/intake/{signal_id}.signal.json`
   Process signal files dropped by other skills. After processing, move to `intake/processed/`.

Skip files that fail JSON parse — log the error, do not halt the pass.

## Ingestion log

Append-only JSONL at `~/openclaw/db/ocas-elephas/ingestion_log.jsonl`.

```json
{
  "run_id": "r_xxxxxxx",
  "source_skill": "ocas-weave",
  "journal_path": "~/openclaw/journals/ocas-weave/2026-03-17/r_xxxxxxx.json",
  "journal_type": "observation",
  "signals_created": 3,
  "candidates_created": 2,
  "ingested_at": "2026-03-17T10:05:00-07:00"
}
```

## Signal creation

From Observation Journals, extract:
- `decision.payload.entities_observed` → one Signal per entity_id, type=Observation
- `decision.payload.relationships_observed` → one Signal per relationship pair
- `decision.payload.preferences_observed` → one Signal per preference

From Action Journals:
- `action.side_effect_intent` and `action.external_reference` → Signal capturing what was done

From Research Journals (Scout, Sift):
- Extract entity names, identifiers, and relationships from the research payload

Signal structure:
```json
{
  "id": "sig_{uuid7}",
  "source_skill": "ocas-weave",
  "source_journal_type": "Observation",
  "payload": {
    "proposed_type": "Entity",
    "entity_type": "Person",
    "name": "Jane Doe",
    "identifiers": [{"type": "email", "value": "jane@example.com"}]
  },
  "timestamp": "2026-03-17T10:00:04-07:00",
  "status": "active"
}
```

Write Signal to Chronicle as a Signal node. Signals are immutable after creation.

## Candidate creation

For each new Signal, check whether a matching Candidate exists:

```cypher
MATCH (c:Candidate {status: 'pending'})
WHERE c.proposed_data CONTAINS $entity_identifier
RETURN c.id
```

If matching Candidate exists: add Signal to `supporting_signals`, re-score confidence.
If no match: create new Candidate node, link via `Supports` edge from Signal.

## Confidence scoring

Initial confidence from a single Signal:
- Research journal with high provenance → `med`
- Multiple corroborating Signals from different skills → `high`
- Single Observation from one skill → `low`

Upgrade rules:
- 2+ Signals from different skills → +1 tier
- Cross-domain confirmation (e.g., Weave + Scout both observed same entity) → `high`
- Contradicting signal of equal or higher confidence → downgrade or flag

## Promotion criteria

Promote when all conditions are met:
1. At least one supporting Signal
2. Confidence is `high` (or `med` with manual approval)
3. No contradicting signal of equal or higher confidence
4. `identity_state` is `distinct` or `confirmed_same` (not `possible_match`)

On promotion: write proposed_data as Chronicle node, create `Promotes` edge from Candidate, set `Candidate.status = 'confirmed'`, set `Signal.status = 'consumed'`.

## Deduplication

During consolidation passes, detect duplicate Entity nodes:

```cypher
MATCH (a:Entity), (b:Entity)
WHERE a.id < b.id
  AND a.entity_type = b.entity_type
  AND (a.identifiers CONTAINS b.name OR a.name = b.name)
RETURN a.id, b.id, a.name, b.name
```

For each candidate pair, apply resolution precedence:
1. Exact identifier overlap → `confirmed_same` if above `auto_merge_threshold`
2. Name + location with corroborating signal → `possible_match` if between thresholds
3. Name only → flag as `possible_match`, do not auto-merge

Auto-merge: call `elephas.identity.merge`. Preserve merge history. Write Action Journal.

## Identity merge

```python
def merge_entities(conn, surviving_id: str, merged_id: str, reason: str):
    now = datetime.now(timezone.utc).isoformat()
    # Get merged entity data
    merged = list(conn.execute(
        "MATCH (e:Entity {id: $id}) RETURN e", {"id": merged_id}
    ))
    if not merged:
        raise ValueError(f"Entity {merged_id} not found")
    # Append to surviving entity's merge_history
    import json
    surviving = list(conn.execute(
        "MATCH (e:Entity {id: $id}) RETURN e.merge_history", {"id": surviving_id}
    ))
    history = json.loads(surviving[0][0] or "[]")
    history.append({"merged_id": merged_id, "merged_at": now,
                    "merged_by": "ocas-elephas", "reason": reason})
    conn.execute("""
        MERGE (e:Entity {id: $sid})
        SET e.merge_history = $history, e.identity_state = 'confirmed_same'
    """, {"sid": surviving_id, "history": json.dumps(history)})
    # Mark merged entity
    conn.execute("""
        MERGE (e:Entity {id: $mid})
        SET e.identity_state = 'confirmed_same'
    """, {"mid": merged_id})
```

Merges are reversible: the merge_history preserves the full audit trail.

## Inference generation

Runs during deep consolidation passes only (`inference.enabled: true`).

Minimum supporting nodes: `inference.min_supporting_nodes` (default: 3).

Pattern types:
- `habit_pattern` — entity repeatedly participates in events of the same type within a recurring time window
- `social_opportunity` — two entities share multiple connections but have no direct relationship
- `recurring_behavior` — entity consistently performs a specific action type

```cypher
CREATE (i:Inference {
  id: $id,
  inference_type: $type,
  confidence: $confidence,
  supporting_nodes: $supporting_nodes_json,
  description: $description,
  created_at: $now
})
```

Link via `Infers` edges. Inferences never overwrite or modify Chronicle facts.

## Error handling

Journal file unparseable — log error with path and reason, skip, continue.
Signal references entity not in Chronicle — create Candidate, do not create dangling fact.
Candidate promotion write fails — mark Candidate `pending`, log error, retry next pass.
Lock error on chronicle.lbug — surface immediately, abort pass, do not corrupt ingestion log.
Malformed intake signal file — move to `intake/errors/` with `.error` suffix, log, continue.
