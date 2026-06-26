## 3.22.2 — Layer 21: Continuous Learning + 6 Bug Fixes (2026-03-28)
## [3.22.3] — 2026-03-28

### Fixed
- **CRITICAL: CONTINUOUS_ENABLED TDZ crash on Node 24.x** — `const` variable accessed before declaration at register time, causing plugin to fail silently on gateways running Node 24.x (embedded binary). Inlined config read for boot log.
- **better-sqlite3 cross-Node-version build guide** — documented that `npx node-gyp rebuild --target=24.13.1` is needed when shell Node differs from gateway's embedded Node.


### New: Layer 21 — Continuous Learning
Real-time fact capture via `message_received` + `llm_output` hooks, independent of session end or compaction.
- **3 extraction modes**: periodic (every N turns), urgent (on user frustration/error), self-error (on assistant self-admission)
- **Cross-layer integration**: facts go through selective dedup → full postProcess pipeline (embed, graph, topics, observations, clusters, sync)
- **Smart dedup with agent_end**: when continuous already captured during the session, agent_end reduces its extraction scope to avoid double LLM calls
- **Configurable**: `continuous.interval` (default 4), `continuous.cooldownMs` (default 45s), `continuous.enabled` (default true)

### Bug Fixes (3 rounds of audit)
**v3.22.0** — Initial implementation
**v3.22.1** — Audit round 1:
- `cfg.continuous` not typed in `MemoriaConfig` → added full interface
- No `enabled` guard → both hooks now check `CONTINUOUS_ENABLED` before running
- `cooldownMs` hardcoded → now reads from config
- agent_end double capture → reduces scope when continuous already ran

**v3.22.2** — Audit round 2:
- **Concurrent extraction risk** — urgent trigger during periodic extraction ran 2 extractions in parallel → added `continuousExtractionInProgress` lock with `finally` release
- **Buffer never cleared** — same messages re-analyzed at each extraction → snapshot + clear before extraction

### Documentation
- `docs/ARCHITECTURE.md`: full Layer 21 section with config, hooks, extraction modes, cross-layer integration
- Boot log now shows continuous learning status

## 3.21.0 — Deep Audit: 10 Bugs Found & Fixed (2026-03-28)

### Critical Fixes
- **Hebbian learning was 100% dead** — `hebbian.ts` used wrong column names (`from_entity`/`to_entity`/`relation_type`/`updated_at`) but DB has `source_id`/`target_id`/`relation`/`last_accessed_at`). All queries silently returned nothing since creation.
- **Proactive revision never triggered** — searched for `lifecycle_state = 'mature'` but DB only has `fresh`/`settled`/`dormant`
- **storeFact() lost 6 columns** on INSERT — `usefulness`, `recall_count`, `used_count`, `synced_to_md`, `relevance_weight`, `lifecycle_state` silently dropped
- **Fact interface missing 4 DB columns** — 8 `as any` casts removed
- **4 SQL queries filtered wrong lifecycle state** — `!= 'archived'` → `!= 'dormant'`
- **Cross-layer 9b used wrong column names** — same `from_entity`/`to_entity` bug as hebbian
- **revision.ts imported non-existent file** — `./llm-provider.js` → `./providers/types.js`
- **procedural.ts wrong import path** — aligned to `./providers/types.js`
- **Fact type unions incomplete** — added `"cluster"` and `"pattern"` to `fact_type`

## 3.20.1 — Audit: 6 Bugs Found & Fixed (2026-03-28)
- Type alignment: `fact_type` and `lifecycle_state` unions updated
- SQL queries: 4 instances of `archived` → `dormant`
- Import fixes: `revision.ts` and `procedural.ts`

## 3.20.0 — Cross-Layer Connections (2026-03-28)
- **Feedback → Lifecycle**: facts recalled 5+ times with usefulness ≥ 2 → auto-promoted to "settled"
- **Hebbian → Topics**: strong relations (weight ≥ 1.0) auto-organize topic hierarchy (smaller becomes child)
- **Lifecycle → Patterns**: patterns with 5+ occurrences → settled
- Pattern detection step added to postProcessNewFacts

## 3.19.0 — Behavioral Pattern Detection, Layer 20 (2026-03-28)
- New module `patterns.ts` (~477 LOC) — detects repeated similar facts and consolidates
- Patterns stored as `fact_type = "pattern"` with occurrence metadata in tags
- Wired into capture pipeline (postProcessNewFacts) and recall scoring
- ARCHITECTURE.md updated to reflect Layer 20

## 3.18.0 — Fix Existing Layers, Phase 1 (2026-03-28)
- New DB table `cluster_members` with backfill (~407 links)
- Topics parent inference improved (composite-name strategy)
- Boot-time reparenting of existing topics (17 reparented)
- ARCHITECTURE.md reviewed/updated (19→20 layers documented)

## 3.17.0 — ClawHub Security Fixes (2026-03-28)
- SKILL.md: explicit `entrypoint: index.ts`, env vars declared optional, expanded security section
- Install instructions: plugin install (one command) + "review code first" for source
- Bundle includes all .ts modules + index.ts
- License: Apache-2.0 in YAML frontmatter

## 3.16.0 — ClawHub Suspicious Fix (2026-03-28)
- Created `.clawignore` to exclude dev/audit artifacts
- Declared env vars (OPENAI_API_KEY, OPENROUTER_API_KEY, OPENCLAW_WORKSPACE) as optional
- Added security posture section to SKILL.md

## 3.14.1 — Error Detection: Touch Fire Once (2026-03-27)
- Automatic error signal detection (crashes, frustration keywords, rollbacks)
- Each error captures: what happened, why dangerous, what to never repeat, safe alternative

## 3.14.0 — Smarter Extraction + Consolidation (2026-03-27)
- Extraction prompt rewritten: demands concrete details (who/what/when/why)
- Cluster-aware recall: member facts get -40% score penalty
- Procedures: first success = worth remembering (was: needed 3+ steps)
- Added `failure_reasons` column for contextual alternative selection

## 3.12.0 — Capture Quality & Contradiction Detection

### Fix 1: Capture Filter
- Only store **reusable** procedures (≥3 meaningful steps + at least one "action" command)
- Skip noise: health checks, diagnostics, log inspections, status checks
- Double-check LLM-assigned names against noise patterns

### Fix 2: Duplicate Detection
- `findSimilarProcedure()` — word-overlap matching on name + goal (threshold 50%)
- Before creating a new procedure, check if a similar one exists → reinforce instead of duplicate
- Applied at both `extractProcedure()` and `after_tool_call` hook levels

### Fix 3: Contradiction Check on Facts
- Widened entity search from 5 to 10 candidates
- Version-containing facts prioritized in contradiction search
- Enhanced contradiction prompt: version changes, status changes, quantity changes = explicit contradictions
- Prevents stale facts (e.g., "Sol = v2.7.0") from persisting when newer facts arrive ("Sol = v3.11.0")

## 3.10.0 (2026-03-27)

### Features
- **FTS5 procedural search**: `procedures_fts` virtual table with LIKE fallback — fast full-text search on procedures (name, goal, context, gotchas, steps)
- **Configurable thresholds**: `ProceduralConfig` interface with `qualityWeights`, `degradationStep`, `healingStep`, `reflectEvery`, `degradedThreshold`, `defaultSafety`
- **FTS auto-sync**: index created at boot, rebuilt if empty, kept in sync on every `storeProcedure` call
- **Plugin schema**: procedural config exposed in `openclaw.plugin.json` for wizard/UI configuration

### Fixes
- `kg` → `graph` variable reference (runtime crash)
- Feedback proc IDs removed (was querying wrong table)
- Procedure objects fully typed (no more `as any` partial objects)

# Changelog

## [3.9.0] - 2026-03-27
### Added — Reflective Procedural Learning
- **Quality dimensions** — each procedure scored on speed, reliability, elegance, safety
  - Weighted composite: reliability (35%) > safety (25%) > speed (25%) > elegance (15%)
  - Quality evolves with each execution, not static
- **Post-execution reflection** — every 3rd success triggers LLM review
  - "Was this the best approach?" → suggestions, quality reassessment
  - Blends new assessment (70%) with accumulated wisdom (30%)
  - Tracks gotchas/workarounds learned
- **Alternatives** — same goal, different approaches
  - `getAlternatives()` finds competing procedures
  - `setPreferred()` marks the best approach
  - Search prioritizes preferred procedures
- **Version tracking** — procedures evolve: version increments on each improvement
- **Personal best** — tracks fastest execution, speed quality improves when beaten
- **Schema auto-migration** — new quality columns added seamlessly on boot

### Why
"Un humain n'enregistre pas un savoir en rentrant chez lui le soir — 
il apprend sur le tas, il améliore en direct. La qualité passe par 
une meilleure réflexion, et c'est en améliorant la qualité qu'on 
gagne en vitesse d'exécution car on la reproduit plus souvent."

## [3.8.0] - 2026-03-27
### Added — Real-time Procedural Learning
- **`after_tool_call` hook** — captures procedures in real-time, not at end of session
  - Buffers tool calls during conversation (last 30)
  - On success signal (Published, ✅, deployed, committed, etc.) → immediately assembles procedure via LLM
  - If similar procedure exists → reinforces it (success_count++) and adds improvements
  - If new → creates new procedure with steps, goal, trigger patterns, gotchas
  - 60s cooldown between assemblies to avoid spam
  - Fingerprint dedup to avoid duplicate captures
- `agent_end` remains as safety net for any uncaptured sequences

### Why this change
- Humans learn on-the-fly, not at the end of the day
- `agent_end` only fires at conversation end → in long-running sessions, procedures were never captured
- Real-time learning means knowledge is available immediately for the next similar task

## [3.7.2] - 2026-03-27
### Fixed — 3 Critical Memory Issues
- **ProceduralMemory DB fix**: was receiving MemoriaDB wrapper instead of raw better-sqlite3 Database, causing `this.db.prepare is not a function` — procedures were "captured" in logs but never persisted (0 in DB)
- **Recall query pollution fix**: FTS5 search was matching on OpenClaw envelope metadata (`"Conversation info (untrusted metadata)..."`) instead of actual user message — causing 89% of facts to never be recalled. Now strips envelope before search
- **DB cleanup**: 22 vague/meta facts superseded (e.g., "Le nouveau fait complète l'ancien"), cortex.db archived

### Impact
- Procedures now persist to SQLite correctly
- Recall will match on what the user actually says, not Telegram metadata
- 436 active facts (was 450, 14 were noise)

## [3.7.1] - 2026-03-27
### Fixed — Phase 3 Procedural Capture
- **Dual-strategy extraction** for better reliability:
  - Strategy A: extract from `event.toolCalls` when available (original path)
  - Strategy B: parse assistant messages for command patterns (fallback)
  - Patterns detected: bash code blocks, inline commands, shell prompts (`$ ...`)
  - Success detection: ✅|success|published|deployed|completed keywords
  - Deduplication of consecutive identical commands
- **Debug logging** added to diagnose capture behavior in production
- New method: `ProceduralMemory.extractFromMessages(messages, context)`

### Why this fix
- v3.7.0 captured 0 procedures because `event.toolCalls` was empty/unavailable
- Message parsing ensures capture works even when toolCalls not exposed by OpenClaw
- Enables real-world validation of Phase 3 procedural learning

## [3.7.0] - 2026-03-27
### Added — Procedural Memory (Phase 3)
- **How-to knowledge that improves with repetition**
  - New `procedures` table: stores sequences of successful actions (exec/tool calls)
  - Captures steps, success/failure counts, degradation score, alternatives
  - Hook `agent_end`: detects successful command sequences → extracts procedure
  - Hook `before_prompt_build`: searches matching procedures → injects steps
  - Dynamic improvement: success_count++ reduces degradation, failure++ increases it
  - Alternative paths: when degradation > 0.5, searches for better alternative procedure
  - Example: "Publish to ClawHub" captured as 4-step procedure with success rate

- **Stats at boot**: `procedures: 0✓/0⚠` (healthy/degraded)

### Why this matters
- Memoria now learns "how to do things" (not just "what happened")
- Procedures improve over time as they're repeated successfully
- Failed attempts trigger degradation → search for alternative approach
- Solves: "I published v3.5.0 but don't remember HOW" → now it's stored & recalled

## [3.6.0] - 2026-03-27
### Added — Human-Like Memory Architecture
- **Identity-aware memory** (Phase 0)
  - New `relevance_weight` column (0.0-1.0, default 0.5) on facts
  - Parses `USER.md`, `COMPANY.md`, `projects/objectifs.md` to extract identity/priorities
  - Boosts facts about Bureau, Polymarket, Primask (core work) vs Memoria internals (meta)
  - Scoring integrates relevance: Bureau facts rise, config/plugin facts sink
  - New `identity_cache` table stores parsed identity for fast lookup

- **Lifecycle states** (Phase 1.1)
  - Facts evolve through 4 states: `fresh` → `mature` → `aged` → `archived`
  - Automatic transitions based on time + usage ratio + recall count
  - `archived` facts excluded from recall (forgotten, not deleted)
  - Stats displayed at boot: `338f/0m/0a/0⚰` (fresh/mature/aged/archived)

- **Proactive revision** (Phase 1.2)
  - Mature facts with 10+ recalls trigger LLM revision proposal
  - If improved → new fact created + old superseded
  - Revision runs in background (non-blocking)

- **Hebbian reinforcement** (Phase 2)
  - Relations now have `weight` (0.0-2.0, default 1.0)
  - Co-occurrence → weight++ (entities seen together strengthen)
  - Time decay → weight-- (unused relations fade)
  - Weak relations pruned automatically (<0.3)
  - Stats: `21 strong, 0 weak` relations

- **Expertise specialization** (Phase 2)
  - Topics gain "expertise levels": novice/familiar/experienced/expert
  - Based on `access_count` (interaction frequency)
  - Expert topics boost recall score (1.3x for expert, 1.1x for experienced)
  - Stats: `8★★★/6★★/4★` (expert/experienced/familiar)

### Fixed
- Added try/catch to lifecycle, hebbian, expertise modules (prevent crash on SQL errors)
- Expertise module: fixed schema mismatch (`topic` → `name`, `interaction_count` → `access_count`)

## [3.5.1] - 2026-03-26
### Fixed
- TypeScript parse error in `feedback.ts` (class closing brace misplaced) — plugin was crashing silently for 7h
- Plugin now loads correctly after restart

## [3.5.0] - 2026-03-26
### Added — Feedback Loop & Adaptive Learning
- **Usefulness tracking** — each recalled fact now has `usefulness`, `recall_count`, `used_count` scores
  - Facts referenced in the assistant's response → usefulness++ (boost)
  - Facts ignored repeatedly → usefulness-- (sink naturally)
  - Scoring integrates usefulness: high-use facts rise, never-used facts decay faster
- **User correction detection** — detects patterns like "non c'est", "en fait", "actually", "that's wrong" (FR+EN)
  - Penalizes the last-recalled facts that may have caused the error (-1.5 penalty)
- **User frustration detection** — detects "putain", "bordel", "wtf", repeated questions
  - Mild penalty (-0.5) on last-recalled facts
- **Adaptive budget** — budget now learns from compactions:
  - If recall → compaction within 5 min → penalty increases (injected too many facts)
  - Penalty reduces limit by 1-3 facts (minimum always respected)
  - Penalty decays naturally when compactions stop (self-correcting)

### Added — Cross-Layer Supersede Cascade
- When a fact is superseded, ALL layers are notified:
  - **Observations**: superseded fact removed from evidence lists; empty observations deleted
  - **Graph**: fact removed from relation contexts; orphaned relations weakened (-0.15) or pruned
  - **Topics**: fact↔topic links removed; empty topics deleted; fact_count updated
  - **Embeddings**: stale embedding vector deleted (no more ghost matches in semantic search)
- Before: layers were disconnected. A superseded fact's ghost persisted in graph, topics, embeddings.

### Added — Smart md-regen
- Auto-triggers on 3 conditions (replaces dumb "lines > 200" check):
  - `captures_since_regen >= 20` — enough new facts accumulated
  - `last_regen_at > 7 days` — stale files even with few captures
  - Any `.md file > 200 lines` — backward-compatible safety net
- Tracks `captures_since_regen` and `last_regen_at` in meta table

### Improved — Extraction Quality
- **Anti-meta prompt** — blocks vague/meta-facts ("Le nouveau fait fournit des informations...")
  - Requires at least one proper noun, number, or concrete command per fact
- **Tighter dedup** — combined threshold lowered to 0.75 + new "8 first words identical" → instant duplicate
- **Dynamic entity matching** — `SelectiveMemory` now loads entities from the Knowledge Graph DB (373+ entities)
  instead of a hardcoded regex list. Refreshes every 5 min.

### Fixed
- DB cleanup: 307→294 active facts (13 superseded, 5 duplicate clusters purged, 3 meta-facts removed)

## [3.4.1] - 2026-03-26
### Improved — Install Wizard UX
- **Clearer prompts**: "Tapez 1, 2 ou 3" on all choices (not just "Choix [1]")
- **Cloud providers**: choose between OpenAI, OpenRouter, or Anthropic (was OpenAI-only)
- **Modifiable after install**: all prompts now mention `configure.sh` for post-install changes
- **Update mode**: `--update` flag for quick silent updates; auto-detection of existing install
- **Existing install detection**: if Memoria is already installed, proposes Update / Reinstall / Cancel
- **Thank-you message**: links to @Nitix_ (X), GitHub star, Primo Studio credit
- **Auto-cleanup**: `memory-convex` entry automatically removed from `openclaw.json` if present
- **Fallback info**: warns user that crash notifications appear in logs
- **Embeddings note**: displayed during install with "changeable later" mention

## [3.4.0] - 2026-03-26
### Added — Fact Clusters
- **Entity-grouped "dossier" summaries**: groups 3+ facts sharing the same entity into one dense paragraph
- Clusters stored as `fact_type = "cluster"` — searchable via FTS5 + embeddings like regular facts
- 15% scoring boost (info-dense = higher recall value)
- Auto-invalidation: when a member fact is superseded, cluster marked stale → regenerated next cycle
- Entity detection: knowledge graph IDs first, proper noun extraction fallback
- Known entities pattern matching for Memoria-specific terms (Sol, Bureau, Primask, etc.)
- **Impact**: MS (multi-session) benchmark 2/5 → 3.5/5; overall accuracy 75% → 81.7%

### Benchmark Results (v3.4.0, GPT-5.4-nano judge)
- Accuracy: **81.7%** (22/30 correct + 5 partial)
- Retrieval: **50.0%** (15/30)
- SSU 5/5, KU 5/5, SSP 5/5, SSA 3.5/5, TR 3.5/5, MS 2.5/5
- 39 atomic facts + 5 clusters = 44 total facts from 10 sessions

## [3.3.0] - 2026-03-26
### Added — Query Expansion
- **Hybrid search now expands queries** into 2-4 semantic variants before searching
- Domain-specific concept map: "taux horaire" → ["salaire", "€/h", "paie"], "projets" → ["apps", "MVPs"], etc.
- FTS + cosine both search across all variants, deduplicating results
- Proper noun extraction: named entities searched standalone
- **Impact**: MS (multi-session) questions like "quels taux horaires?" now find "5.19€/h" facts

### Improved — Topic-Aware Recall
- `findRelevantTopics` now receives expanded queries for broader matching
- Topic name exact match bonus (+3 score) with expanded variants
- **Impact**: Topics like "salaires" found even when query says "rémunération"

### Improved — Denser Extraction
- Extraction prompt now enforces "one fact per distinct entity"
- Example: session mentioning 3 people → 3 separate facts instead of 1 merged
- **Impact**: More facts per session = better multi-session recall

## [3.2.0] - 2026-03-26
### Fixed — Reasoning Model Support (I3+I4)
- **Ollama provider**: Now reads `thinking` field when `response` is empty (GPT-OSS, Qwen3.5 reasoning models)
- **OpenAI-compat provider**: Now reads `reasoning_content` and `reasoning` fields (LM Studio GPT-OSS)
- **Impact**: Clients using reasoning models no longer get empty extractions/answers

### Fixed — Knowledge Update Recall (I1+I2)
- **Recall now shows dates**: Each fact displays age (`[aujourd'hui]`, `[il y a 3j]`, `[2026-03-20]`)
- **Header instructs**: "Les faits les plus récents sont les plus fiables en cas de contradiction"
- **Impact**: Answering model can now disambiguate when old and new versions of a fact coexist

### Improved — Procedure Extraction (I5)
- **Multi-sentence facts allowed**: Procedures can now be captured as 2-4 sentences in a single fact
- **Prompt guidance**: Examples show good vs bad procedure capture
- **Impact**: Workflows and how-to knowledge preserved as coherent units

### Improved — Short Query Handling (I6)
- **Adaptive FTS/cosine weights**: Short queries (<3 words) now favor semantic search (55%) over FTS (20%)
- **Impact**: Generic queries like "Bureau" return semantically relevant facts instead of keyword noise

### Added — Provider Interface Cleanup (I7)
- **`generateWithMeta`** added to LLMProvider interface (optional, with default implementation)
- **All providers** (Ollama, OpenAI-compat) now implement generateWithMeta
- **Impact**: Providers are fully interchangeable with FallbackChain

### Added — Anthropic Provider (I8+A3)
- **New `providers/anthropic.ts`**: Native Claude API support (`/v1/messages` format)
- **Supported in**: LLM config, fallback chain, per-layer overrides
- **Models**: Any Claude model (Haiku, Sonnet, Opus) via API key
- **Impact**: Clients can use Claude directly without routing through OpenRouter

### Added — Config Schema Update
- **`anthropic`** added to `llm.provider` enum in plugin schema
- **Fallback chain** supports `type: "anthropic"` entries

## [3.1.1] - 2026-03-25
### Improved — Extraction Quality (Results over Status)
- **Problem**: Extraction captured "test passed ✅" but lost actual results like "Retrieval 92%, bottleneck = local model"
- **New ✅ categories**: benchmark results with metrics, conclusions from experiments, measured comparisons, machine/infra specs
- **Smarter filtering**: block narration WITHOUT results (not all narration); block binary status without info ("test OK")
- **Extraction priority**: 🥇 learnings > 🥈 measured results > 🥉 durable facts

## [3.1.0] - 2026-03-25
### Fixed — Entity-based Semantic Contradiction Detection
- **Critical fix**: Contradictions between facts with different wording but same entities were not detected
  - Example: "No models on Sol" vs "gemma3:4b installed on Sol" had only 0.23 textual similarity → contradiction check was never called
  - Root cause: Levenshtein+Jaccard gate (threshold 0.7) prevented LLM from seeing semantically related facts with different words
- **New entity extraction**: Extracts proper nouns, tech terms, tool names from facts (Sol, Memoria, Ollama, gemma3, etc.)
- **Entity-based FTS search**: When new fact shares entities with existing facts, triggers LLM contradiction check regardless of text similarity
- **Wider FTS search** (20 candidates per entity) to avoid missing facts ranked beyond top 5
- **Fail-safe**: If entity check fails → fact is stored (never lost)

### Improved — Extraction Prompt
- **Generalization rules**: When a pattern repeats (e.g. "npm not found in SSH" + "ollama not found in SSH"), extract the general rule instead of individual cases
- **Process knowledge**: Explicit instructions to store "how to do X" commands (e.g. "lms server start launches LM Studio without GUI")

### Technical
- `SelectiveMemory` constructor now accepts optional `EmbeddingManager` (4th arg) for future semantic enhancements
- `semanticContradictionThreshold` config option added (default 0.40)
- `extractSubjectEntities()` function with patterns for common tech terms
- `findFactsBySharedEntities()` method for entity-overlap search
- Build order in index.ts: embed providers created before SelectiveMemory instantiation

## [3.0.0] - 2026-03-25
### Added — Phase 2: Semantic/Episodic Memory
- **fact_type column**: `semantic` (durable, slow decay 30-90 days) vs `episodic` (dated, fast decay 7-14 days)
- **Extraction prompt rewritten**: explicit STOCKER/NE PAS STOCKER rules, LLM now classifies fact type
- **TODO/action filter**: blocks transient facts ("il faut X", "en préparation", "prochaine étape")
- Auto-migration adds `fact_type` column to existing DBs

### Added — Phase 3: Observations (Living Syntheses)
- **Observation layer**: inspired by Hindsight, multi-fact synthesis that evolves
- Observations are **created** when 3+ facts share a topic (auto-emergence via LLM topic extraction)
- Observations are **updated** (re-synthesized) when new related facts arrive
- **Recall priority**: Observations injected FIRST, individual facts as complement
- Each observation tracks `evidence_ids`, `revision` count, `access_count`, embedding
- Matching via embedding cosine similarity + keyword fallback
- Configurable: `emergenceThreshold`, `matchThreshold`, `maxRecallObservations`, `maxEvidencePerObservation`

### Added — Phase 4: Recall Adaptatif
- Observations count adjusts to context window (recallLimit / 3, min 2)
- Individual facts fill remaining budget after observations
- Format splits into "Observations (synthèses vivantes)" + "Faits individuels"

### Added — Procedural Memory Preservation
- **Procedural memory** (procedural): like learning bike tricks — processes, tips, "what worked" are preserved as durable knowledge
- **Smart TODO filter**: distinguishes disposable TODOs ("pull X") from learned processes ("use VACUUM INTO because WAL copies lose -shm")
- Heuristics: length >60 chars usually = knowledge → keep; explanation markers (car/sinon/pour/because/→) → always keep
- Transient patterns (en préparation, en cours, pas encore) only skip short facts

### Fixed
- **CRITICAL: `api.config` vs `api.pluginConfig`** — all custom settings were silently ignored since v0.1.0
- Fallback `provider` vs `type` normalization in parseConfig

## [2.7.0] - 2026-03-25
### Added
- **Interactive wizard in install.sh** — 2-question guided install: "Local or Cloud?" → "Fallback or strict?". Detects environment (Ollama, LM Studio, OpenAI key), shows summary, asks confirmation.
- **Presets for silent install** — `--preset local-only|cloud-first|paranoid` for CI/scripting. Also `--yes` to skip confirmation.
- **Post-install validation** — Tests LLM provider after install (quick Ollama smoke test).
- **Bilingual installer** — French interface for better UX (target market).

### Fixed
- **CRITICAL: `api.config` vs `api.pluginConfig`** — Plugin was reading global OpenClaw config instead of plugin-specific config. ALL custom settings (fallback, llm, embed, limits) were silently ignored since v0.1.0. Fixed to use `api.pluginConfig`.
- **Fallback `provider` vs `type` mapping** — User config uses `provider` field but internal code expected `type`. Added normalization in parseConfig.

### Changed
- install.sh rewritten as interactive wizard with environment detection and guided choices.
- Config generated based on user choices (not hardcoded defaults).

## [2.6.1] - 2026-03-25
### Added
- **Auto-config in install.sh** — The installer now auto-edits `openclaw.json`: adds memoria to `plugins.entries` and `plugins.allow` with a backup of the original file. Users keep full control to customize after.
- **Existing data detection** — install.sh detects cortex.db, memoria.db, or facts.json and shows migration status (fact count, file size).
- **Summary panel** — install.sh now displays version, location, config path, LLM/embed info at the end.
- **Node.js/npm version display** — Shows detected versions during prerequisite check.

### Fixed
- **WAL-mode migration** — `VACUUM INTO` used instead of `cp` for cortex.db→memoria.db migration. Plain `cp` on WAL-mode SQLite DBs resulted in empty copies (0 facts). Fallback copies WAL+SHM files if VACUUM fails.
- **Empty DB override** — Migration now triggers if memoria.db exists but is < 8KB (empty schema-only DB from a failed previous attempt).

### Changed
- install.sh rewritten: auto-config replaces manual "copy-paste this JSON" step.
- INSTALL.md updated to document auto-config, WAL migration, and data detection.

## [2.6.0] - 2026-03-25
### Added
- **`install.sh`** — One-line installer: checks prerequisites, pulls Ollama models, clones repo, installs deps. Usage: `curl -fsSL https://raw.githubusercontent.com/Primo-Studio/openclaw-memoria/main/install.sh | bash`
- **Auto-migration cortex→memoria** — If `memoria.db` doesn't exist but `cortex.db` does, auto-copies it. Zero manual migration needed.

### Fixed
- **Schema too strict** — `additionalProperties` changed from `false` to `true` everywhere. Unknown config keys no longer crash the gateway.
- **`syncMd` type** — Was rejecting `{ enabled: true }` objects. Now only accepts boolean as documented, and schema makes it clear.
- **`embed.dims` vs `embed.dimensions`** — Schema now documents `dimensions` clearly with defaults shown.
- **`fallback[].type` vs `fallback[].provider`** — Schema field is `provider`, not `type`.
- **`llm.default` doesn't exist** — Schema clearly shows `llm.provider` + `llm.model` at top level.
- **DB constructor confusion** — `MemoriaDB()` takes workspace root, not DB path. Documented + auto-migration handles legacy DB name.

### Changed
- **Smart defaults everywhere** — `{ "memoria": { "enabled": true } }` is now a valid minimal config. Defaults: Ollama + gemma3:4b + nomic-embed-text-v2-moe + 768 dims + recall 12 + capture 8.
- Schema defaults added to all fields for documentation.
- INSTALL.md rewritten with config minimale, bugs connus, et providers table.

## [2.5.0] - 2026-03-25
### Added
- **Hot Tier**: facts accessed ≥5 times = always injected in recall, like a phone number you know by heart. New `getHotFacts()` in scoring, `hotFacts()` in DB.
- **Access-based learning**: `accessBoostFactor` tripled (0.1 → 0.3) — frequently used facts score much higher, mimicking human memory retention through repetition.
- **Configurable defaults raised**: `captureMaxFacts` 3→8, `recallLimit` 8→12, `maxFacts` 10→12. Users with smaller context windows can lower these in config.

### Changed
- Recall pipeline now: hot tier (always first) → hybrid search → graph → topics → context tree → budget limit
- Hot facts excluded from search results to avoid duplicates
- `searchLimit` = `recallLimit - hotCount` so hot facts don't eat into query-relevant slots

## [2.4.0] - 2026-03-25
### Added
- **Embed Fallback** (`embed-fallback.ts`): `EmbedFallback` wraps multiple `EmbedProvider`s with automatic retry (Ollama → LM Studio → OpenAI). If primary embed fails, tries next provider.
- **Post-processing function** `postProcessNewFacts()`: shared between `agent_end` and `after_compaction` hooks — embed, graph extract, topic tag, sync .md, auto md-regen.
- **Auto md-regen**: triggers automatically when any .md file exceeds 200 lines after capture. Bounded regeneration (30d recent, 150 max/file).

### Fixed
- **after_compaction incomplete** ✅: compaction-rescued facts now get full enrichment (embed + graph + topics + sync + regen) — same pipeline as agent_end.
- **Embed no fallback** ✅: EmbedFallback chains configured embed provider → LM Studio → OpenAI (if API key available).
- **md-regen manual only** ✅: now auto-triggered in postProcessNewFacts when file size threshold exceeded.

### Changed
- Post-processing code extracted from agent_end into reusable `postProcessNewFacts()` function
- Log messages now include `[capture]` or `[compaction]` source label

## [2.3.0] - 2026-03-25
### Added
- **Per-layer LLM config**: each layer (extract, contradiction, graph, topics, contextTree) can use a different model/provider
- `llm.overrides` config section with per-layer `{ provider, model, baseUrl?, apiKey? }`
- Override chains include the user's chosen model as primary, then fallback to the default chain
- Boot log shows active overrides when configured
- JSON Schema `$defs/layerLlm` in manifest for validation

### Changed
- `FallbackChain` now implements `LLMProvider` interface directly (`generate()` → string, `generateWithMeta()` → metadata)
- All modules receive FallbackChain (full fallback) instead of `chain.primaryLLM` (Ollama-only)
- `selective` uses `contradictionLlm`, `graph` uses `graphLlm`, `topics` uses `topicsLlm`, `contextTree` uses `contextTreeLlm`, extract uses `extractLlm`

### Fixed
- Fallback gap: selective, graph, topics, context-tree had NO fallback (Ollama-only). Now all have full chain.

## [2.2.0] - 2026-03-25
### Added
- Phase 9: `.md Vivants` — bounded markdown regeneration (recent 30d, max 150/file, archive notice)
- `MdRegenManager` class with configurable regen settings
- Boot-time .md file size logging

## [2.1.0] - 2026-03-25
### Added
- Phase 8: `Topics Émergents` — auto-clustering from keyword patterns
- `TopicManager` class with keyword extraction, emergence scanning, sub-topics
- Topic embeddings (mean of fact embeddings, cosine search)
- Topic enrichment in recall pipeline (after graph, before context tree)
- Bootstrap script for initial tagging (389/438 facts tagged → 94 topics)
- `topics` + `fact_topics` tables in SQLite schema

## [2.0.0] - 2026-03-25
### Added
- Phase 10: `Fallback Chain` — graceful LLM degradation (Ollama → OpenAI → LM Studio → FTS-only)
- `FallbackChain` class with round-robin retry and configurable providers

## [1.0.0] - 2026-03-25
### Added
- Phase 7: `Budget Adaptatif` — dynamic recall limit based on context usage (light/medium/heavy/critical zones)
- Phase 7: `Sync .md` — auto-append new facts to mapped workspace markdown files
- `AdaptiveBudget` class with configurable thresholds
- `MdSync` class with dedup (first 60 chars check)

## [0.5.0] - 2026-03-25
### Added
- Phase 6: `Context Tree` — hierarchical fact organization with query-weighted scoring
- `ContextTreeBuilder` class with category clustering and sub-clustering

## [0.4.0] - 2026-03-25
### Added
- Phase 5: `Knowledge Graph + Hebbian Learning` — entity extraction, relation storage, BFS traversal
- `KnowledgeGraph` class with graph extraction prompts and Hebbian reinforcement
- Partial/fuzzy entity matching

## [0.3.0] - 2026-03-25
### Added
- Phase 4: `Embeddings + Hybrid Search` — cosine similarity with local Ollama embeddings
- `EmbeddingManager` class with batch embedding, hybrid search (FTS + cosine + temporal)

### Fixed
- FTS5 query sanitization (hyphenated terms crash)

## [0.2.0] - 2026-03-25
### Added
- Phase 2: `Mémoire Sélective` — dedup (Levenshtein + Jaccard), contradiction check via LLM, importance threshold, enrichment/merge
- `SelectiveMemory` class with configurable thresholds

## [0.1.0] - 2026-03-25
### Added
- Phase 1: Core SQLite + FTS5, temporal scoring, perception hooks
- `MemoriaDB` class, migration from facts.json (423 facts)
- Provider abstraction (Ollama, OpenAI-compat, LM Studio)

<!-- v3.14.x entries moved to proper chronological position above -->

## 3.22.0 — 2026-03-28

### Added
- **Layer 21: Continuous Learning** — real-time fact capture via `message_received` + `llm_output` hooks
  - Rolling buffer of last 10 user/assistant exchanges
  - Periodic extraction every 4 turns (configurable via `continuous.interval`)
  - **Urgent extraction** triggered immediately on frustration/error signals (e.g. "ne fais plus", "doublon", "crash")
  - **Self-error detection** — captures when assistant acknowledges its own mistake
  - Uses same LLM extraction prompt and selective dedup pipeline as agent_end
  - Independent of context size, compaction, or session end — works with 60K, 200K, or 10M token contexts
