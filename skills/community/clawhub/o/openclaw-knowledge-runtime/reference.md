# Reference

## Record Schemas

### `knowledge_entry`
Suggested fields:

- `knowledge_id`
- `kind`
- `layer`
- `scope`
- `title`
- `summary`
- `tags`
- `entities`
- `supports_genes`
- `derived_from_events`
- `confidence`
- `freshness`
- `reuse_score`
- `source_ref`
- `created_at`
- `updated_at`

### `knowledge_link`
Suggested fields:

- `link_id`
- `from_type`
- `from_id`
- `relation`
- `to_type`
- `to_id`
- `weight`
- `reason`
- `evidence_ref`
- `created_at`

### `entity`
Suggested fields:

- `entity_id`
- `entity_type`
- `name`
- `aliases`
- `knowledge_refs`
- `hit_count`
- `updated_at`

## Output Bundle
Recommended runtime output:

- `knowledge_hits`: top ranked entries with score and reason
- `knowledge_bias_tags`: short tags for downstream ranking
- `linked_entities`: canonical entities gathered from hits and one-hop links
- `linked_genes`: genes or reusable assets supported by selected knowledge
- `memory_layers`: layer histogram or ordered layer list
- `knowledge_context_preview`: short prompt-safe summary

## Retrieval Guidance
Use a lightweight hybrid pipeline:

1. Normalize the query from role, objective, direction, and recent signals.
2. Filter by layer, scope, tags, metadata, and direct entity overlap.
3. Score by keyword overlap, freshness, confidence, and layer weights.
4. Expand one hop through typed links.
5. Re-rank and trim for prompt safety.

## Adapter Guidance
The runtime stays standalone when host systems integrate through adapters instead of hard-coded file paths.

### `query_builder`
Input:

- role
- objective
- direction
- recent signals
- optional query bundle

Output:

- normalized keywords
- tags
- entity hints
- layer and scope hints

### `retrieval_selector`
Responsibilities:

- load store, links, and entity indexes
- rank entries
- expand through typed links
- produce the final runtime output bundle

### `task_ranker`
Responsibilities:

- compare task text and metadata with `knowledge_bias_tags`
- reward overlap with `linked_entities` and `linked_genes`
- record a short overlap reason for observability

### `prompt_context`
Responsibilities:

- compress the selected knowledge into a short context block
- preserve evidence titles and linked entities
- avoid dumping raw logs or oversized JSON

### `write_back`
Responsibilities:

- write only durable findings
- derive typed links from entities, genes, tasks, or source events
- dedupe repeated findings before persistence

### `observability`
Expose:

- hit count
- top hit titles
- linked entities
- linked genes
- memory layer coverage
- knowledge context preview

## Notes

- Keep the runtime append-friendly for raw stores and rebuildable for indexes.
- Prefer canonical entities over raw path or URL fragments.
- Treat entity extraction as a quality boundary; noisy entities reduce retrieval quality fast.
