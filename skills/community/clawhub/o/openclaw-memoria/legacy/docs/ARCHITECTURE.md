# Memoria — Architecture & Internals

> This document covers implementation details for contributors and advanced users.
> For installation and usage, see the main [README](../README.md).

## Hooks

Memoria integrates with OpenClaw via five hooks:
- `before_prompt_build` — Recall pipeline (inject relevant facts into context)
- `message_received` — Buffer user messages for continuous learning (Layer 21)
- `llm_output` — Buffer assistant responses + trigger extraction (Layer 21)
- `agent_end` — Capture pipeline (extract facts from conversation)
- `after_compaction` — Capture pipeline (extract facts from compacted summaries)

Additionally, `after_tool_call` is used for real-time procedural capture (Layer 13).

## Recall Pipeline

```
1. budget.compute() → determine max facts for current context usage
2. observationMgr.getRelevantObservations(query) → matching observations
3. embeddingMgr.hybridSearch(query) → FTS5 + cosine + scoring
4. scoreAndRank(results) → temporal sort (semantic vs episodic decay)
5. graph.findEntitiesInText(query) → mentioned entities
6. graph.getRelatedFacts(entities) → BFS 2 hops
7. graph.hebbianReinforce(entityIds) → reinforce weights
8. topicMgr.findRelevantTopics(query) → topics by keyword + cosine
9. treeBuilder.build(allCandidates, query) → hierarchical tree
10. treeBuilder.extractFacts(tree, limit) → final selection
11. formatRecallContext(facts, observationContext) → inject
```

## Capture Pipeline

```
1. LLM extract → JSON facts with {fact, category, type, confidence}
2. TODO filter → skip disposable tasks, keep learned processes
3. selective.processAndApply(fact, category, confidence, agent, factType)
4. postProcessNewFacts():
   a. embed batch → vectorize unembedded facts
   b. graph.extractAndStore → entities/relations
   c. topicMgr.onFactCaptured → keywords + association
   d. topicMgr.scanAndEmerge → emergence if threshold met
   e. observationMgr.onFactCaptured → match/create/update observations
   f. clusterMgr.generateClusters → entity-grouped summaries
   g. mdSync.syncToMd → append to .md files
   h. mdRegen.regenerate → auto if file > 200 lines
```

## Memory Types

| Type | Description | Decay |
|------|-------------|-------|
| **semantic** | Durable truths, patterns | Slow (30-90 days by category) |
| **episodic** | Dated events, milestones | Fast (7-14 days by category) |

### Decay half-lives by category × type

| Category | Semantic | Episodic |
|----------|----------|----------|
| erreur | ∞ (immune) | 30 days |
| savoir | 90 days | 14 days |
| preference | 90 days | 14 days |
| rh | 60 days | 14 days |
| client | 60 days | 14 days |
| outil | 30 days | 7 days |
| chronologie | 14 days | 7 days |

## Scoring Formula

`score = confidence × decayFactor × recencyBoost × accessBoost × freshnessBoost × stalePenalty`

- **Access boost**: `0.3 × log(accessCount + 1)` — frequently recalled facts score higher
- **Hot Tier**: facts accessed ≥5x are always injected

## Layers

| # | Layer | File | LLM? |
|---|-------|------|------|
| 1 | SQLite Core + FTS5 | `db.ts` | ❌ |
| 2 | Temporal Scoring + Hot Tier | `scoring.ts` | ❌ |
| 3 | Selective Memory (dedup, contradiction) | `selective.ts` | ✅ |
| 4 | Embeddings + Hybrid Search | `embeddings.ts` | ❌ (embed only) |
| 5 | Knowledge Graph + Hebbian | `graph.ts` | ✅ |
| 6 | Context Tree | `context-tree.ts` | ❌ (heuristic) |
| 7 | Adaptive Budget | `budget.ts` | ❌ |
| 8 | Emergent Topics | `topics.ts` | ✅ |
| 9 | Observations | `observations.ts` | ✅ |
| 10 | Fact Clusters | `fact-clusters.ts` | ✅ |
| 11 | .md Sync + Regen | `sync.ts`, `md-regen.ts` | ❌ |
| 12 | Fallback Chain | `fallback.ts` | all |
| 13 | Procedural Memory | `procedural.ts` | ✅ |
| 14 | Lifecycle | `lifecycle.ts` | ❌ |
| 15 | Feedback Loop | `feedback.ts` | ❌ |
| 16 | Hebbian Reinforcement | `hebbian.ts` | ❌ |
| 17 | Identity Parser | `identity-parser.ts` | ❌ |
| 18 | Expertise Specialization | `expertise.ts` | ❌ |
| 19 | Proactive Revision | `revision.ts` | ✅ |
| 20 | Behavioral Patterns | `patterns.ts` | ✅ |
| 21 | Continuous Learning | `index.ts` (hooks) | ✅ |

## Continuous Learning (Layer 21)

Real-time fact capture via `message_received` + `llm_output` hooks, independent of context window size, compaction, or session end.

**Hooks:**
- `message_received` → buffers user messages, detects urgent signals (frustration, error keywords)
- `llm_output` → buffers assistant responses, triggers extraction

**3 extraction modes:**
- **Periodic** — every N turns (default 4), with 45s cooldown between extractions
- **Urgent** — immediate on frustration/error signals (bypasses cooldown): "ne fais plus", "crash", "doublon", "putain"...
- **Self-error** — immediate when assistant acknowledges its own mistake: "par erreur", "j'aurais dû"...

**Cross-layer integration:**
- Uses same `extractLlm` + `LLM_EXTRACT_PROMPT` as agent_end
- Facts go through `selective.processAndApply()` → dedup/contradiction/enrichment
- Triggers full `postProcessNewFacts()` → embed, graph, topics, observations, clusters, sync
- `agent_end` reduces its scope when continuous already captured (avoids double LLM calls)

**Config (`continuous` in plugin config):**
- `interval` (default 4): extract every N turns
- `cooldownMs` (default 45000): minimum gap between periodic extractions
- `enabled` (default true when autoCapture is true): toggle on/off

## Procedural Memory

- Short fact (<60 chars) + TODO pattern → skip
- Long fact (≥60 chars) → always keep
- Contains explanation markers (car, sinon, pour, because, →) → always keep

## Observations Lifecycle

1. New fact → search for matching observation (embedding similarity or keywords)
2. Match found → re-synthesize with new evidence
3. No match → accumulate; 3+ facts sharing a topic → create observation
4. Recall injects observations FIRST (priority over individual facts)

## Database Schema

- `facts` — main table with `fact_type` (semantic/episodic/cluster)
- `facts_fts` — FTS5 index
- `embeddings` — float vectors (768d default)
- `entities`, `relations` — knowledge graph
- `topics`, `fact_topics` — emergent topic system
- `cluster_members` — maps cluster facts to their member facts
- `observations` — living syntheses
- `procedures` — procedural memory (how-to steps)

## Categories (7)

| Category | Maps to | Normalizations |
|----------|---------|----------------|
| savoir | MEMORY.md | architecture, mécanisme → savoir |
| erreur | MEMORY.md | sévérité, bug → erreur |
| outil | TOOLS.md | — |
| preference | USER.md | — |
| chronologie | MEMORY.md | — |
| rh | COMPANY.md | — |
| client | COMPANY.md | financier → client |

## Provider Support

| Provider | LLM | Embeddings | Notes |
|----------|-----|------------|-------|
| Ollama | ✅ | ✅ | Local, 0€, `thinking` field support |
| LM Studio | ✅ | ✅ | Local, `reasoning_content` support |
| OpenAI | ✅ | ✅ | Cloud, compatible APIs |
| OpenRouter | ✅ | ✅ | Multi-model gateway |
| Anthropic | ✅ | ❌ | Native `/v1/messages` API |
