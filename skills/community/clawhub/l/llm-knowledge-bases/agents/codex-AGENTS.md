# LLM Knowledge Bases

Use this guide when Codex should operate a Vault managed by the `LLM Knowledge Bases` MCP server.

Core model:

- `raw/` stores captured source material
- `wiki/` stores the persistent knowledge layer
- `wiki/sources/` stores compiled source pages
- `wiki/outputs/` stores archived answers
- `wiki/concepts/`, `wiki/entities/`, and `wiki/syntheses/` store durable derived pages
- `wiki/_indexes/`, `wiki/index.md`, and `wiki/log.md` keep the vault navigable
- `.llm-kb/representations/` stores runtime-managed OCR, vision, metadata, and profiling artifacts for non-text assets

Boundaries:

- treat the Vault as runtime-managed
- use MCP tools for all Vault reads and writes
- never modify `raw/`
- never write directly into `wiki/` or `.llm-kb/representations/` with generic file tools
- never invent IDs, hashes, representation paths, or `source_refs`
- use `kb_read_raw` only for text-readable raw files
- use the representation-first path for PDFs and images

Required MCP tools:

- `kb_status`
- `kb_list_raw`
- `kb_read_raw`
- `kb_get_raw_asset`
- `kb_prepare_source`
- `kb_prepare_source_bundle`
- `kb_prepare_representation`
- `kb_upsert_representation`
- `kb_read_representations`
- `kb_upsert_source_note`
- `kb_prepare_output`
- `kb_upsert_output`
- `kb_prepare_derived_note`
- `kb_upsert_derived_note`
- `kb_search`
- `kb_read_notes`
- `kb_map_gaps`
- `kb_promote_gap`
- `kb_repair_source_ids`
- `kb_rebuild_indexes`
- `kb_lint`

Canonical actions:

1. `ingest-source`
   - `kb_status`
   - `kb_list_raw(changed_only=true)`
   - for text/data: `kb_prepare_source` -> `kb_read_raw`
   - for PDFs/images: `kb_prepare_source_bundle` -> `kb_get_raw_asset` -> representation tools -> `kb_read_representations`
   - write one grounded source page
   - `kb_upsert_source_note`
   - `kb_rebuild_indexes`

2. `ask-and-file`
   - `kb_search`
   - `kb_read_notes`
   - answer only from retrieved notes
   - use `kb_upsert_output` for query-specific archives
   - use `kb_upsert_derived_note` for durable concept/entity/synthesis pages

3. `maintain-wiki`
   - `kb_lint`
   - inspect indexes and relevant pages
   - use `kb_repair_source_ids` first when source ids, manifest entries, source note paths, or raw hashes have drifted
   - repair narrowly through runtime tools
   - `kb_rebuild_indexes`

4. `map-gaps`
   - `kb_search`
   - `kb_read_notes`
   - `kb_map_gaps`
   - optionally `kb_promote_gap` when the best current candidate should be landed immediately

Natural-language triggers:

The explicit prefix `$llm-knowledge-bases` is optional.
Use it when you want maximum routing certainty, but short natural-language requests should still trigger this guide when the intent is clear.

- `check my wiki`, `总览检查`: run `kb_status` plus `kb_lint`, report counts, top issues, and the best next action; do not write unless asked
- `fill missing source notes`, `继续推进这份库`: use `kb_status` plus `kb_list_raw(changed_only=true)` with an explicit `limit`, prioritize `missing_source_note`, compile in small batches, then rebuild indexes
- `clean up these pages`, `fix placeholder titles`, `做一次维护清理`: start with `kb_lint`, then use `kb_search` plus `kb_read_notes` to target placeholder titles, open questions, related links, stale navigation, and other high-value health issues
- `add concept/entity/synthesis pages`, `what pages are missing?`: search first, read evidence, then run `kb_map_gaps`; use `kb_promote_gap` when the candidate can be landed directly
- `repair source ids`, `repair manifest drift`: run `kb_repair_source_ids` as a dry run first, explain the plan, then apply only if it looks correct
- `answer this from the wiki and save it back`: use `ask-and-file`; prefer `concept/entity/synthesis` over `output` when the result is reusable beyond the current query

Chinese routing hints:

- `看一下`, `检查一下`, `盘一下`, `总览`, `先看看`: inspection-first, usually `kb_status` plus `kb_lint`
- `先别改`, `只看不改`, `先给我报告`: read-only mode unless the user later asks for writes
- `补缺失`, `补书评`, `编译缺的 source`: `ingest-source` focused on `missing_source_note`
- `整理一下`, `清理一下`, `修一下占位内容`: `maintain-wiki` with placeholder cleanup and topic filters
- `补概念页`, `补 entity`, `补 synthesis`, `沉淀成页面`: derived-page flow; always read evidence before writing
- `修漂移`, `修 source id`, `修 manifest`, `先 dry run`: `kb_repair_source_ids` dry run first
- `继续推进这份库`, `接着跑一轮`: conservative continuation batch, not a giant rewrite

Continuation default when the request is underspecified:

1. `kb_status`
2. `kb_list_raw(changed_only=true)` with an explicit `limit`
3. `kb_lint`
4. optional topic-targeted `kb_search` plus `kb_read_notes`
5. choose one primary batch: either a small `missing_source_note` compile batch or a small placeholder-repair batch
6. optionally add one high-confidence derived page
7. `kb_rebuild_indexes`

Scenario presets:

- `整理一下 AI 相关内容`, `只修 AI 相关`, `补 AI 概念页`
  run `kb_lint`, then topic-focused `kb_search` plus `kb_read_notes`; repair a small batch of placeholder-heavy notes first, then optionally land one high-confidence derived page
- `补书评`, `继续编译书评`, `书评批处理`
  scope to `raw/书评 1/` text raw files, prioritize `missing_source_note`, compile up to 10 notes, then rebuild indexes
- `继续推进我的这份库`, `接着跑一轮`
  choose one primary batch only: either up to 10 source-note compiles, up to 5 placeholder repairs, or 1 derived page

When `继续推进这份库` is underspecified, prefer whichever of these is most clearly dominant in `kb_status` plus `kb_lint`.

One-line shortcuts that should be treated as complete enough requests:

- `用 $llm-knowledge-bases 检查一下我的 wiki，先别改`
- `用 $llm-knowledge-bases 补书评前 10 个`
- `用 $llm-knowledge-bases 整理一下 AI 相关内容`
- `用 $llm-knowledge-bases 补 3 个 concept pages`
- `用 $llm-knowledge-bases 修一下 source id 漂移，先 dry run`
- `用 $llm-knowledge-bases 继续推进我的这份库`

The same one-line requests should also work without the `$llm-knowledge-bases` prefix when the surrounding context is clearly about this wiki.

Always honor explicit scope like `top 5`, `first 10`, `only AI-related`, `only raw/书评 1/`, or `do not modify yet`.

Writing rules:

- source pages need `Summary`, `Key Points`, `Evidence`, `Open Questions`, `Related Links`
- multimodal source pages should keep `raw_kind`, `mime_type`, and `asset_paths` aligned with the reviewed asset trail
- PDF/image source pages should usually include `Visual Notes` when the review evidence is not already obvious from stored representations
- output pages need `Answer`, `Sources Used`, `Follow-up Questions`
- concept pages need `Summary`, `Definition`, `Key Points`, `Evidence`, `Open Questions`, `Related Notes`
- entity pages need `Summary`, `Who or What`, `Key Facts`, `Evidence`, `Open Questions`, `Related Notes`
- synthesis pages need `Summary`, `Thesis`, `Supporting Evidence`, `Tensions`, `Open Questions`, `Related Notes`

Finish by stating:

- what was ingested, answered, or maintained
- which MCP tools were used
- which pages were created or updated
- any unresolved ambiguity or weak evidence
