# Memoria — Module Guide for Contributors

> Quick reference to understand each file's role, inputs/outputs, and how modules connect.
> For the full pipeline flow, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Overview

```
26 TypeScript files · ~10,500 LOC · 21 layers
SQLite database with FTS5 · Local embeddings (768d)
5 LLM providers supported · Fallback chain architecture
```

---

## Core Modules

### `db.ts` (644 LOC) — Layer 1: Database
**The foundation.** Manages SQLite connection, schema, migrations, and CRUD.

- **Key types**: `Fact`, `Entity`, `Relation` (all exported)
- **Tables**: facts, facts_fts, embeddings, entities, relations, topics, fact_topics, observations, procedures, cluster_members, chunks, identity_cache, meta
- **Key methods**: `storeFact()`, `getFact()`, `searchFacts()` (FTS5), `getActiveFacts()`, `supersedeFact()`, `raw` (direct sqlite3 access)
- **Migrations**: auto-run on construction; `migrateAddProcedures()`, `migrateAddClusterMembers()`, etc.
- **Important**: `storeFact()` uses `Omit<Fact, ...> & Partial<Fact>` — you must provide id, fact, category, confidence, source, tags, agent, created_at, updated_at, fact_type. Other columns have defaults.

### `index.ts` (1777 LOC) — Plugin Entry Point
**The orchestrator.** Registers all hooks, creates all managers, wires everything together.

- **Hooks registered**: `before_prompt_build` (recall), `message_received` + `llm_output` (continuous learning), `after_tool_call` (procedural), `agent_end` (capture), `after_compaction` (safety net)
- **Key internal functions**: `postProcessNewFacts()` (runs 8 post-capture steps), `doContinuousExtraction()`, `parseConfig()`
- **Config parsing**: raw plugin config → `MemoriaConfig` interface
- **LLM wiring**: `layerLLM()` function resolves per-layer overrides or falls back to main chain

### `fallback.ts` (249 LOC) — Layer 12: Fallback Chain
**Resilience.** Wraps multiple LLM/embed providers with automatic failover.

- **Exports**: `FallbackChain` (implements both `LLMProvider` and `EmbedProvider`)
- **Behavior**: tries providers in order; if one fails, tries next; if all fail, throws
- **Config**: `FallbackProviderConfig[]` — each entry has provider type, model, baseUrl, apiKey
- **Used by**: every module that needs LLM — selective, graph, topics, observations, clusters, procedural, revision, patterns

---

## Recall Pipeline (before_prompt_build)

### `scoring.ts` (187 LOC) — Layer 2: Temporal Scoring
Calculates decay-based scores for facts.

- **Input**: array of facts
- **Output**: facts with `temporalScore` attached
- **Key formula**: `confidence × decayFactor × recencyBoost × accessBoost × freshnessBoost × stalePenalty`
- **Hot Tier**: facts with `access_count >= 5` are always included (bypass budget)
- **Decay rates**: vary by category × fact_type (semantic vs episodic). Error facts are immune.

### `budget.ts` (184 LOC) — Layer 7: Adaptive Budget
Decides how many facts to inject based on context usage.

- **Input**: current context token count, max context tokens
- **Output**: `BudgetResult` with `maxFacts` (2-12) and `tier`
- **Tiers**: empty (12), light (10), medium (8), heavy (5), critical (2)

### `context-tree.ts` (337 LOC) — Layer 6: Context Tree
Organizes facts into a hierarchical tree for better prompt injection.

- **Input**: array of scored facts + query
- **Output**: tree of `ContextNode` with facts grouped by category/topic
- **Method**: heuristic regex-based grouping (no LLM needed)

### `identity-parser.ts` (213 LOC) — Layer 17: Identity Parser
Parses SOUL.md, USER.md, COMPANY.md to know what matters to the user.

- **Input**: workspace path
- **Output**: identity context (human name, agent name, company, projects, priorities)
- **Method**: `calculateRelevance(fact, category)` → 0.0-1.0 score
- **Caches**: parsed identity in SQLite `identity_cache` table

### `expertise.ts` (144 LOC) — Layer 18: Expertise Specialization
Boosts recall score for topics the user frequently asks about.

- **Input**: fact + topic access counts
- **Output**: boosted score (up to 1.5x)
- **Data source**: `topics.access_count` (incremented on each recall)

---

## Capture Pipeline (agent_end / continuous)

### `selective.ts` (611 LOC) — Layer 3: Selective Memory
**Gatekeeper.** Decides if a new fact should be stored, merged, or rejected.

- **Input**: new fact text, category, confidence, agent
- **Output**: `{ action: "store" | "enrich" | "supersede" | "skip", stored: boolean }`
- **Pipeline**: noise filter → too-short check → FTS candidates → Levenshtein dedup → prefix dedup → LLM contradiction check → store/enrich/supersede
- **Thresholds**: configurable per category (preferences have tighter dedup at 0.65)
- **LLM call**: only for contradiction detection (when similarity > threshold)

### `embeddings.ts` (347 LOC) — Layer 4: Embeddings
Manages vector embeddings for semantic search.

- **Input**: fact text
- **Output**: 768d float vector stored in `embeddings` table
- **Methods**: `embedFact()`, `embedBatch()`, `hybridSearch(query)` (FTS5 + cosine)
- **Batch embed**: processes unembedded facts on capture; called from `postProcessNewFacts()`

### `embed-fallback.ts` (62 LOC) — Embed Provider Wrapper
Wraps multiple embed providers with fallback (like `fallback.ts` but for embeddings only).

### `graph.ts` (427 LOC) — Layer 5: Knowledge Graph
Extracts entities and relations from facts using LLM.

- **Input**: fact text
- **Output**: entities (person/project/tool/concept/place) + relations stored in DB
- **LLM call**: entity/relation extraction prompt
- **Recall**: `findEntitiesInText(query)` → `getRelatedFacts(entityIds)` (BFS 2 hops)

### `hebbian.ts` (155 LOC) — Layer 16: Hebbian Reinforcement
Strengthens knowledge graph relations through co-occurrence.

- **Behavior**: when entities are recalled together, their relation weight increases by 0.1 (capped at 2.0); unused relations decay by 0.05 daily (minimum 0.1)
- **Called from**: recall pipeline (after graph entity lookup)

### `topics.ts` (825 LOC) — Layer 8: Emergent Topics
Discovers and manages topic clusters.

- **Input**: new fact
- **Output**: topic associations in `fact_topics` table
- **LLM call**: keyword extraction for new facts; topic naming for new clusters
- **Features**: parent_topic_id hierarchy, `scanAndEmerge()` for new topic creation (threshold: 3+ facts), boot-time reparenting of existing topics, access_count tracking

### `observations.ts` (482 LOC) — Layer 9: Observations
Living syntheses that evolve as new evidence appears.

- **Input**: new fact + existing observations
- **Output**: updated/created observation
- **LLM call**: synthesis when merging new evidence into existing observation
- **Lifecycle**: 3+ facts sharing a topic → auto-create observation; existing observation + new evidence → re-synthesize

### `fact-clusters.ts` (373 LOC) — Layer 10: Fact Clusters
Groups related facts by entity into summary "cluster facts."

- **Input**: entity ID
- **Output**: cluster fact (fact_type="cluster") + `cluster_members` links
- **LLM call**: generate cluster summary from member facts
- **Recall penalty**: clustered facts get 0.6x score (prefer the summary)

### `patterns.ts` (477 LOC) — Layer 20: Behavioral Patterns
Detects repeated similar facts and consolidates them.

- **Input**: all facts from capture batch
- **Output**: pattern facts (fact_type="pattern") with occurrence tracking
- **LLM call**: generate consolidated pattern from similar facts
- **Threshold**: 3+ similar facts → consolidate into pattern
- **Lifecycle**: 5+ occurrences → auto-promote to "settled"

---

## Learning & Lifecycle

### `lifecycle.ts` (223 LOC) — Layer 14: Lifecycle Management
Manages fact states: fresh → settled → dormant.

- **Input**: fact ID, current state
- **Output**: state transition
- **Rules**: fresh (new) → settled (confirmed by recalls/feedback) → dormant (unused for extended period)
- **Integration**: cross-layer promotion from feedback (recall_count ≥ 5 + usefulness ≥ 2)

### `feedback.ts` (326 LOC) — Layer 15: Feedback Loop
Tracks how useful recalled facts actually are.

- **Columns**: `usefulness`, `recall_count`, `used_count`
- **Method**: after response, check which recalled facts appeared in the answer → increment used_count
- **Data flows into**: lifecycle (promotion), scoring (access boost), patterns (consolidation)

### `revision.ts` (222 LOC) — Layer 19: Proactive Revision
Periodically reviews settled facts for staleness.

- **Input**: settled facts with high recall but potentially outdated info
- **Output**: updated fact text or supersession
- **LLM call**: ask if fact still accurate; if not, generate updated version
- **Trigger**: on boot staleness check (every 24h)

### `procedural.ts` (1281 LOC) — Layer 13: Procedural Memory
**The largest module.** Captures "how to do things" with steps, quality, gotchas.

- **Input**: tool call sequences from `after_tool_call` hook
- **Output**: `Procedure` with steps, quality profile, gotchas, alternatives, doc sources
- **Features**: success/failure tracking, quality reflection via LLM, degradation scoring, alternative procedures, staleness/doc-check tracking, failure_reasons
- **Key methods**: `assembleProcedure()`, `matchExisting()`, `reflectOnExecution()`, `formatForRecall()`

---

## Support Modules

### `sync.ts` (258 LOC) — Layer 11a: .md Sync
Appends facts to workspace .md files based on category mapping.

- **Category → file**: savoir → MEMORY.md, erreur → MEMORY.md, outil → TOOLS.md, preference → USER.md, rh → COMPANY.md, client → COMPANY.md

### `md-regen.ts` (348 LOC) — Layer 11b: .md Auto-Regeneration
Rewrites .md sections when files exceed 200 lines.

- **Input**: file path, all facts for that category
- **Output**: regenerated file preserving manual content above injection point

### `migrate.ts` (79 LOC) — Migration Utilities
Helpers for one-time data migrations.

### `bootstrap-topics.ts` (88 LOC) — Topic Bootstrapper
One-time script to generate initial topics from existing facts.

### `audit-v25.ts` (255 LOC) — Test Suite
34 tests validating core functionality (FTS, scoring, embedding, facts, graph).

---

## Providers

### `providers/types.ts` — Interfaces
Defines `LLMProvider` and `EmbedProvider` interfaces that all providers implement.

```typescript
interface LLMProvider {
  generate(prompt: string, options?: GenerateOptions): Promise<string>;
  generateWithMeta?(prompt: string, options?: GenerateOptions): Promise<GenerateResult | null>;
}

interface EmbedProvider {
  embed(text: string): Promise<number[]>;
  embedBatch?(texts: string[]): Promise<number[][]>;
}
```

### `providers/ollama.ts` — Ollama Provider
Local Ollama API. Supports `thinking` field extraction, chat API with `think: false`.

### `providers/openai-compat.ts` — OpenAI / LM Studio / OpenRouter
OpenAI-compatible API. Works with any OpenAI-format endpoint.

### `providers/anthropic.ts` — Anthropic
Native Anthropic `/v1/messages` API. Supports Claude models.

---

## Data Flow Summary

```
User message
  ↓
message_received hook → buffer (Layer 21)
  ↓
LLM response
  ↓
llm_output hook → buffer (Layer 21)
  ↓ (every N turns or urgent)
Continuous extraction → LLM → selective → postProcess
  ↓
before_prompt_build hook (next turn):
  budget(7) → observations(9) → hybridSearch(4)
  → graph(5) → topics(8) → contextTree(6)
  → scoring(2) × lifecycle(14) × expertise(18)
  → identity(17) → format + inject
  ↓
agent_end hook:
  feedback(15) → LLM extract → selective(3) → postProcess:
    embed(4) → graph(5) → hebbian(16) → topics(8)
    → observations(9) → clusters(10) → sync(11)
    → patterns(20) → cross-layer(14,16,8,20)
  ↓
after_compaction hook (safety net):
  Same pipeline as agent_end but from compacted text
```

---

## Adding a New Layer

1. Create `your-layer.ts` in the root directory
2. Export a manager class with a clear interface
3. Import and instantiate in `index.ts` (after line ~450 where other managers are created)
4. Wire into `postProcessNewFacts()` if it runs on capture
5. Wire into `before_prompt_build` if it affects recall
6. Add to the layer table in `docs/ARCHITECTURE.md` and `README.md`
7. Update `CHANGELOG.md`
8. Bump version in `package.json` and `SKILL.md`

## Adding a New Provider

1. Create `providers/your-provider.ts`
2. Implement `LLMProvider` and/or `EmbedProvider` from `providers/types.ts`
3. Add to `buildProvider()` switch in `fallback.ts`
4. Add to `MemoriaConfig.llm.provider` and `embed.provider` union types in `index.ts`
5. Update provider support table in README and ARCHITECTURE

## Running Tests

```bash
npx tsx audit-v25.ts          # 34-test suite
npx tsx bootstrap-topics.ts   # one-time topic generation
```

## Database Inspection

```bash
# Connect to the DB
sqlite3 ~/.openclaw/workspace/memory/memoria.db

# Quick stats
SELECT COUNT(*) as facts FROM facts WHERE superseded=0;
SELECT COUNT(*) as embedded FROM embeddings;
SELECT COUNT(*) as entities FROM entities;
SELECT COUNT(*) as relations FROM relations;
SELECT COUNT(*) as topics FROM topics;
SELECT COUNT(*) as procedures FROM procedures;
SELECT lifecycle_state, COUNT(*) FROM facts WHERE superseded=0 GROUP BY lifecycle_state;
```
