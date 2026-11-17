# Paper Schema Public API Contract

Contract version: `v1`. Base path: `/paper-schema`. All operations use the same Sciverse Bearer token, quota resource, and usage accounting.

## Fixed tool-to-route mapping

| Tool | Action | Method and public route |
| --- | --- | --- |
| `paper_schema_capabilities` | n/a | `GET /paper-schema` |
| `search_paper_schemas` | n/a | `POST /paper-schema/search` |
| `discover_related_papers` | `entity` | `POST /paper-schema/entities/related-papers` |
| `discover_related_papers` | `seed` | `POST /paper-schema/schemas/{schema_id}/related-papers` |
| `query_paper_entities` | `search` | `POST /paper-schema/entities/search` |
| `query_paper_entities` | `list` | `GET /paper-schema/schemas/{schema_id}/entities` |
| `query_paper_entities` | `get` | `GET /paper-schema/schemas/{schema_id}/entities/{entity_id}` |
| `query_paper_relations` | `search` | `POST /paper-schema/relations/search` |
| `query_paper_relations` | `get` | `GET /paper-schema/schemas/{schema_id}/relations/{relation_id}` |
| `query_paper_citations` | `summary` | `GET /paper-schema/schemas/{schema_id}/citation-summary` |
| `query_paper_citations` | `list` | `GET /paper-schema/schemas/{schema_id}/citations` |
| `query_paper_citations` | `graph` | `GET /paper-schema/schemas/{schema_id}/citation-graph` |
| `query_paper_evidence` | `search` | `POST /paper-schema/evidence/search` |
| `query_paper_evidence` | `get` | `GET /paper-schema/schemas/{schema_id}/evidence/{evidence_id}` |
| `resolve_paper_context` | `provenance` | `POST /paper-schema/resolve-provenance` |
| `resolve_paper_context` | `search` | `POST /paper-schema/search-in-schema` |
| `resolve_paper_context` | `hydrate` | `POST /paper-schema/hydrate-items` |
| `build_paper_materials` | n/a | `POST /paper-schema/materials` |

No other route is part of this skill.

## Paper search

`search_paper_schemas` accepts `query`, `filters`, `sort`, `size`, and `cursor`. At least `query` or one filter is required.

Filters:

- `schema_ids` up to 100
- `dois` up to 100
- `authors` up to 20
- `venues` up to 50
- `published_year_gte`, `published_year_lte`: 1800-2200
- `has_code`, `has_data`, `is_oa`
- `metadata_status`: `matched` or `unresolved`

Sort supports at most two fields: `year`, `metrics.citation_count`, `metrics.reference_count`, or `metrics.fwci`, with `asc` or `desc` order. Page size is 1-100.

## Entity taxonomy

- `Document`: `research_article`, `review`, `benchmark_survey`
- `Problem`
- `Contribution`: `method`, `dataset`, `finding`, `benchmark`
- `Component`: `algorithm`, `model_architecture`, `definition`, `training_strategy`, `objective_function`, `theorem`, `resource`, `assumption`, `bound`, `taxonomy`, `lemma`
- `ExperimentSetup`: `dataset`, `task`, `benchmark`, `data_split`, `inference_protocol`, `training_config`, `population`, `ensembling`
- `Measure`
- `Finding`: `comparative`, `descriptive`, `ablation_finding`, `failure_mode`, `mechanistic`, `theorem`, `bound`, `modeling`, `lemma`
- `Resource`: `code`, `project`, `dataset`, `demo`, `video`, `model`
- `Reference`

Entity search requires `query` unless `filters.schema_ids` is provided. Entity list supports repeated `entity_types`, `entity_subtypes`, and `sections` query parameters. `entity_id` is contextual to its `schema_id` and is not a canonical cross-paper identifier.

## Internal Relation types

Public relation types are:

`part_of`, `evaluates`, `about`, `uses_component`, `compares_with`, `background`, `compares_to`, `addresses_limitation_of`, `resolves`, `motivates`, `analyzes_property_of`, `builds_on`, `inspired_by`, `adapts_idea_from`, `co_contribution`, `supports`.

Relation search requires at least one structural filter among `schema_ids`, `source_entity_ids`, `target_entity_ids`, or `relation_types`. `evidence_query` only narrows a structurally scoped search. Internal source/scope markers are not public.

## Citation levels

1. `summary` reports complete reference totals, resolution coverage, and paper-edge counts.
2. `list` paginates complete resolved and unresolved references, 1-100 per page.
3. `graph` expands only resolved schema-to-schema edges. `direction` is `outbound` or `inbound`; depth is 1-3; maximum nodes and edges are each capped at 500.

Use list or summary for complete citation counts. Use graph only for navigable paper edges.

## Evidence groups

Public groups are `evidence_score`, `schema_unit`, `reference_semantics`, `reference_core`, `comparison_detail`, `citation_signal`, `formula`, `core_claim_result`, `table_evidence`, and `resource`.

Evidence search requires 1-5 groups plus one narrowing condition: `schema_ids`, `query`, `key`, `path_bucket`, numeric range, or boolean value. `group_operator` is `any` or `all`.

The public Evidence detail path uses `evidence_id`. Raw data is never requested or returned by the skill.

## Provenance and hydration

- Provenance uses exactly one mode: `schema_id` plus `marker_nums`, or `paragraph_ids`.
- Window is 0-5. Provenance can return up to 100 segments.
- Single-schema fallback search requires `schema_id` and `query`, with `top_k` 1-20.
- Hydration accepts 1-50 items and at most 20 segments per item.

## Materials

Materials accepts 1-20 `schema_ids`. Goals are `overview`, `benchmark`, `method`, `reproduction`, and `survey`. Resource limits are bounded; callers must inspect `returned`, `total`, and `truncated`.

## Public output boundary

Only the fields, values, and routes explicitly documented above are public. Reject every unknown input through positive allowlists, and do not probe or describe private storage fields, internal service metadata, hidden endpoints, or backend query syntax.

## Error contract

- `400`: invalid request
- `401`: missing or invalid authentication
- `403`: Paper Schema permission unavailable
- `404`: schema resource not found
- `429`: account, Paper Schema resource, or source quota reached
- `502`: upstream unavailable, invalid, or too large
- `504`: upstream timeout

The scripts retry only `429`, `502`, `503`, and `504`, at most three attempts.
