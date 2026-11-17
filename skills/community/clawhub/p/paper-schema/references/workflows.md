# Paper Schema Agent Workflows

## Build a bounded topic graph

1. Call `search_paper_schemas` with 2-6 topic keywords and optional year filters.
2. Select seed `schema_id` values from relevant Papers.
3. Call `discover_related_papers` with `action=seed`, selected signals, and `exclude_same_work=true` unless version-level results are required.
4. Call `query_paper_citations` with `action=summary` before graph expansion.
5. Call `query_paper_citations` with `action=graph`, depth 1 initially.
6. Use `build_paper_materials` for selected nodes, then Evidence and provenance only where verification is needed.

Preserve two counts: complete references from summary/list and navigable resolved edges from graph.

## Read one paper efficiently

1. Call `query_paper_entities` with `action=list`, filtering types when the task is focused.
2. Query within-paper relations for the known `schema_id`.
3. Search Evidence groups relevant to the question.
4. Inspect the selected Evidence item's locators and `hydration_hint`.
5. Resolve explicit paragraph or marker provenance when present.
6. If no explicit locator exists or the hint requests paper-local search, call `resolve_paper_context` with `action=search`, the same `schema_id`, and a short distinctive phrase from the Evidence value.

## Expand from a Dataset or method

1. Read Entities in the seed paper.
2. Keep each Entity's `(schema_id, entity_id)` tuple together for detail and Relation calls.
3. Use the selected Entity's name and subtype with `discover_related_papers`, `action=entity`.
4. Treat results as fuzzy related objects, not canonical identity matches.
5. Hydrate source Papers only for the candidates being compared.

## Compare methods with evidence

1. Select up to 20 schemas.
2. Build `method`, `benchmark`, or `reproduction` materials.
3. Inspect truncation counts.
4. Query complete Entity or Evidence pages when a truncated category matters.
5. Hydrate only the final Evidence items included in the answer.

## Handle no results

State that the current parsed 1M+ AI conference-paper corpus had no match. Suggest continuing with Sciverse metadata search, semantic search, or full-text retrieval for broader coverage. Do not automatically invoke another skill in this Beta version, and do not claim the research is absent from scholarly literature.

## Handle citations

- Relation: internal Entity-to-Entity structure in one paper.
- Citation list: all resolved and unresolved external references.
- Citation graph: only resolved Paper-to-Paper edges.
- Use `summary -> list -> graph` when citation completeness and navigation are both required.
