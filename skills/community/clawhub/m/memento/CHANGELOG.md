# Changelog

## v0.6.0 — 2026-03-01

### Added
- **Phase 1 — History-agnostic extraction**: LLM no longer receives existing facts during extraction. Prompt loaded from `prompts/extraction.md` at runtime (editable without recompile). New durability filter: "would this still matter in 6 months?"
- **Phase 2 — Embedding-based deduplication**: `deduplicator.ts` fully rewritten. Each extracted fact is compared against existing DB facts using cosine similarity (BGE-M3): ≥0.97 = duplicate (increment occurrence), ≥0.82 = update/supersede, <0.82 = new fact. LLM `duplicate_of`/`supersedes` hints no longer used.
- **Immediate embedding**: New facts are embedded immediately after insertion (no async backfill needed going forward). `EmbeddingEngine` now passed through `ExtractionTrigger` → `deduplicator`.
- **Phase 3 — Relation sweep** (`src/consolidation/relation-sweep.ts`): Background job that builds the knowledge graph from embedding similarity. Three tiers: same-category ≥0.85 auto-linked, cross-category ≥0.88 auto-linked, cross-category 0.72–0.88 → Haiku batch classification. Runs on-demand or can be scheduled nightly. Secret facts are never included.
- **Relation classify prompt** (`prompts/relation-classify.md`): Haiku prompt for batch relation type classification (6 types: caused_by, precondition_of, part_of, related_to, contradicts, superseded_by) with rationale field for auditability.
- **New DB helpers**: `ConversationDB.getAllRelations()` and `getDistinctAgentIds()`.
- **Dedup sweep script** (`src/storage/dedup-sweep.ts`): One-shot pairwise similarity sweep for existing facts — flags pairs 0.88–0.97 for review, auto-merges ≥0.97.
- **Backfill script** (`src/storage/backfill-embeddings.ts`): Populates embeddings for facts added before embedding support was introduced.

### Changed
- `extractFacts()` no longer passes existing facts to the LLM. `_existingFacts` parameter kept for API compatibility (prefixed `_`, unused).
- `processExtractedFacts()` is now `async` — all call sites updated.
- Batch/CLI tools (`migrate.ts`, `ingest.ts`, `process-raw-sessions.ts`) pass `null` for `embeddingEngine` (graceful fallback to new-fact insertion without embedding dedup).
- `includeExistingFactsCount` config option is now deprecated (dedup moved to Phase 2 embeddings).

### Fixed
- Removed hardcoded personal path (`~/greg/.engram/`) from `backfill-embeddings.ts`.

### Security
- All Phase 3 relation sweep operations exclude `secret`-visibility facts — they are never sent to any LLM for classification.
- No new env vars required for core plugin operation; `CLAUDE_CODE_OAUTH_TOKEN` is an OpenClaw internal token (auto-used when running inside OpenClaw, never required by users).

## v0.5.1 — 2026-02-28

### Added
- **Causality edges in knowledge graph** — new `precondition_of` relation type alongside existing `caused_by`; extraction prompt instructs the LLM to prefer causal relation types when a clear cause-and-effect or prerequisite relationship exists
- **Causal weight field** — `causal_weight` column added to `fact_relations` (schema v7); deduplicator sets `causal_weight = 1.5` for `caused_by` and `precondition_of` edges vs. `1.0` for associative edges
- **1.5× graph traversal boost for causal edges** — `search.ts` now applies a `1.5×` score multiplier (vs. `0.4×` for non-causal edges) when traversing `caused_by` / `precondition_of` graph edges during recall
- **Query planning** — new `planQuery()` function in `search.ts` runs an LLM pre-pass to expand the query with synonyms and identify relevant categories/entities before FTS search
- **`recall.autoQueryPlanning` config option** — opt-in (default `false`); when enabled, calls the LLM once per recall turn to improve search precision
- **Temporal state transitions** — `previous_value` column added to `facts` table (schema v7); `db.supersedeFact()` automatically captures the old fact's content as `previous_value` on the new fact
- **Previous value shown in recall context** — `context-builder.ts` appends `_(previously: ...)_` to recalled facts that carry a `previous_value`
- **Schema v7 migration** — `MIGRATE_V6_TO_V7` adds `causal_weight` to `fact_relations` and `previous_value` to `facts`; migration is safe to re-run (duplicate column errors are caught)

### Fixed
- **OpenClaw model routing not invoked during extraction** — `ExtractionTrigger` was constructing with `openClawConfig` but not passing it through to `extractFacts()`; this meant every extraction silently fell back to direct API calls, bypassing the v0.5.0 model routing feature entirely

## v0.5.0 — 2026-02-28

### Changed
- **OpenClaw model routing**: Extraction now delegates to OpenClaw's `runEmbeddedPiAgent` instead of making direct HTTP calls to LLM providers. Memento transparently inherits the agent's configured model, fallback chain, and auth profile.
- **No more standalone API key management**: `MEMENTO_API_KEY` / provider-specific env vars are no longer needed when running inside OpenClaw. Direct API fallback remains for CLI/standalone usage.
- **New module**: `src/extraction/embedded-runner.ts` — thin wrapper around `runEmbeddedPiAgent`.
- **README**: Updated privacy note and model config docs to reflect OpenClaw routing behaviour.

## v0.4.0 — 2026-02-XX

### Changed
- ClawHub trust score improvements: honest messaging, `optionalEnv` + `dataFiles` declarations
- `@anthropic-ai/sdk` removed from dependencies
- `autoExtract: false` default (opt-in extraction)
- Hardcoded paths removed → auto-discovery via `os.homedir()`
- Secret-filtering security comments expanded
- Published to ClawHub as `memento@0.4.0`

### Added
- Side-learning: ingest pipeline from Claude Code JSONL sessions
- Knowledge graph: `fact_relations` table with 6 typed relation types, 1-hop recall traversal
- Fact clusters: `fact_clusters` + `cluster_members` tables, incremental + deep consolidation
- Mission Control tab: Knowledge Graph SVG visualisation (force-directed, cluster hulls)
- Deep consolidation: soft confidence decay, cluster merging, runs at 3 AM via cron

## v0.3.0

- Renamed from Engram → Memento
- Git history rewritten (no personal data)
- Pushed to GitHub: https://github.com/braibaud/Memento

## v0.2.0

- Provider-agnostic refactor: Anthropic, OpenAI, Mistral, Ollama, OpenAI-compatible
- Configurable extraction model
- Temporal recency weighting in recall
- Category priority weights (decisions > routine)
- Confidence threshold (0.6 minimum)
- Per-agent memory + master KB (shared facts)

## v0.1.0

- Initial release: fact extraction, SQLite storage, FTS5 search, auto-recall hook
