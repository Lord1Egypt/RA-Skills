# Cortex Memory Tool Reference

## Retrieval

### `search_memory`

Use for semantic recall of historical records.

Input:

```json
{
  "query": "What did we decide about memory decay?",
  "top_k": 8
}
```

### `query_graph`

Use for entity relationship lookup and path traversal.

Input:

```json
{
  "entity": "memoryDecay",
  "rel": "depends_on",
  "dir": "both",
  "path_to": "readFusion",
  "max_depth": 3
}
```

Typical response highlights:
- `edges[].fact_status` (`active/pending_conflict/superseded/rejected`)
- `wiki_refs`
- `evidence_ids`
- `conflict_hint` (when conflict facts are hit)

### `export_graph_view`

Use for status-aware graph snapshot export and wiki graph projection files.

Input:

```json
{
  "write_snapshot": true
}
```

### `lint_memory_wiki`

Run wiki + graph consistency lint checks and return structured repair actions.

Input:

```json
{}
```

## Conflict Governance

### `list_graph_conflicts`

List pending/handled conflicts that need confirmation.

Input:

```json
{
  "status": "pending",
  "limit": 20
}
```

### `resolve_graph_conflict`

Accept or reject a conflict candidate.

Input:

```json
{
  "conflict_id": "gcf_xxx",
  "action": "accept",
  "note": "accepted with user confirmation"
}
```

## Persistence

### `store_event`

Persist durable decisions, outcomes, and entity relations.

Input:

```json
{
  "summary": "Enabled strict graph quality mode for production.",
  "entities": ["graphQualityMode", "production"],
  "entity_types": {
    "graphQualityMode": "config",
    "production": "environment"
  },
  "outcome": "Reduced noisy relations in graph reads.",
  "relations": [
    {
      "source": "graphQualityMode",
      "target": "production",
      "type": "applied_to",
      "confidence": 0.92
    }
  ]
}
```

### `delete_memory`

Delete a specific record by id.

Input:

```json
{
  "memory_id": "mem_123"
}
```

## Session Context

### `get_hot_context`

Read currently hot records.

```json
{
  "limit": 10
}
```

### `get_auto_context`

Read auto-selected context from recent messages.

```json
{
  "include_hot": true
}
```

## Maintenance

### `sync_memory`

Import historical session data into memory.

### `reflect_memory`

Promote events into reusable rules.

### `backfill_embeddings`

Repair or rebuild missing vectors.

Input:

```json
{
  "layer": "all",
  "batch_size": 64,
  "max_retries": 3,
  "retry_failed_only": false,
  "rebuild_mode": "incremental"
}
```

### `cortex_diagnostics` (preferred) / `diagnostics` (legacy alias)

Check model connectivity, registry status, and memory health.
