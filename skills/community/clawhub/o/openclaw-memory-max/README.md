# openclaw-memory-max `v3.0.3`

> **SOTA Memory Suite for OpenClaw** — Turn your lobster into an agent that actually learns from experience, recalls relevant context automatically, and never forgets what matters.

## Why This Exists

Out of the box, OpenClaw retrieves memories by embedding similarity — a flat cosine score. That works for simple recall, but it breaks down fast:

- **The agent forgets useful context** because retrieval is passive — the agent has to explicitly search. Most turns get zero memory context.
- **The same low-quality memory keeps surfacing** because there's no feedback loop — retrieval never learns which memories actually helped.
- **Critical rules get buried** under hundreds of entries. "NEVER delete production data" has the same weight as a note about your editor theme.
- **The agent repeats mistakes** because it has no structured record of what it tried, what worked, and what failed.
- **Long conversations degrade** as the context window fills with stale turns. Important decisions get compacted away and lost.
- **Every session starts from zero** — no episodic awareness of past sessions, no accumulated wisdom.

Memory-max solves each of these with dedicated modules that work together as a single plugin.

## Architecture Overview

```
                    ┌─────────────────────────────────────┐
  User message ───► │         before_agent_start           │
                    │  Auto-Recall: FTS5 → Cross-Encoder   │
                    │  → Utility Weight → Inject Context    │
                    │  + Causal Graph Experience Lookup     │
                    └──────────────┬──────────────────────┘
                                   │ <relevant-memories> XML block
                                   ▼
                    ┌─────────────────────────────────────┐
                    │          Agent Conversation           │
                    │                                       │
                    │  8 tools available:                   │
                    │  • precision_memory_search (top-K)    │
                    │  • deep_memory_search (multi-hop)     │
                    │  • reward/penalize_memory_utility     │
                    │  • memory_graph_add/query/summary     │
                    │  • compress_context                   │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────┼──────────────────────┐
                    │              │                       │
              agent_end    before_compaction        session_end
                    │              │                       │
             Auto-Capture    Memory Rescue        Episode Archive
            (rules, prefs)  (save before evict)   (session summary)
                    │              │                       │
                    ▼              ▼                       ▼
              auto_captured.jsonl              episodes.jsonl
                    │
           ┌────────┴─────────┐
           │  Sleep Cycle 3AM  │
           │  • Merge → MEMORY │
           │  • Prune graph    │
           │  • Decay scores   │
           │  • Truncate logs  │
           └──────────────────┘
```

## What It Does

### Lifecycle Hooks (Proactive — No Agent Action Required)

#### Auto-Recall (`before_agent_start`)
Every time the agent starts a turn, memory-max automatically:
1. Takes the user's latest message
2. Runs an FTS5/BM25 pre-filter against the memory database (~0ms)
3. Cross-encoder reranks the top 20 candidates (~200ms, cached model)
4. Multiplies by utility scores (reinforcement-weighted)
5. Queries the causal knowledge graph for relevant past experience
6. Injects the top results as an XML block directly into the agent's context

The agent sees relevant memories **without calling any tool**. This is the single biggest improvement over v2 — the memory system is now proactive, not passive.

#### Auto-Capture (`agent_end`)
After every conversation, memory-max scans the user's messages for high-value content — rules ("always X", "never Y"), corrections ("actually, instead..."), preferences. These are deduplicated against existing memories and stored in `auto_captured.jsonl` for the nightly sleep cycle to consolidate.

#### Compaction Rescue (`before_compaction`)
When OpenClaw compresses the context window, important information can be lost. Memory-max intercepts the compaction event, scans messages about to be evicted, and rescues high-value content before it disappears.

#### Episodic Memory (`session_start` / `session_end`)
Every conversation session is logged as an episode with timestamps, tools used, key decisions, and a summary. This creates temporal awareness — the agent can reason about "what happened last time" and the sleep cycle can detect patterns across sessions.

### Tools (8 Active Tools)

#### 1. Precision Memory Search — `precision_memory_search`
**Problem**: Embedding similarity retrieves "close enough" results, not the best ones.

**Solution**: Two-stage retrieval pipeline:
1. **FTS5/BM25 pre-filter** — narrows to the top 20-30 candidates from the full database (~0ms, pure SQLite)
2. **Cross-encoder rerank** — `ms-marco-MiniLM-L-6-v2` reads query + candidate together as a single sequence, catching semantic relationships cosine similarity misses (negation, implication, multi-hop reasoning)
3. **Utility weighting** — final score = `semantic_score × utility_score`
4. **Returns top-K results** (default 5, configurable up to 10) — not just the single best match

The cross-encoder model loads once and stays cached for the process lifetime (~80 MB resident, eliminates the ~500ms reload that v2 paid on every call). Runs entirely locally via ONNX — no API calls.

#### 2. Deep Multi-Hop Search — `deep_memory_search`
**Problem**: Important information is often connected through intermediate memories that wouldn't match the original query.

**Solution**: Three-stage retrieval:
1. **Hop 1** — Standard precision search for the query (top 5)
2. **Entity extraction** — Pull key terms from hop 1 results that aren't in the original query
3. **Hop 2** — Search again using extracted concepts (top 5)
4. **Merge + deduplicate** — Combine and rank all unique results

This finds information that is connected through intermediate memories — e.g., querying "deployment issues" might surface a memory about "nginx config" through a hop-1 result about "reverse proxy errors".

#### 3. Reward Memory Utility — `reward_memory_utility`
Increment a memory's utility score (+0.1 to +0.3) after it proved useful. Creates a reinforcement loop: memories that help get surfaced more, memories that mislead get buried.

#### 4. Penalize Memory Utility — `penalize_memory_utility`
Decrement a memory's utility score (-0.1 to -0.3) after it caused a hallucination or was irrelevant.

#### 5. Causal Knowledge Graph — `memory_graph_add`
Log a `cause → action → effect` chain tagged with `success`, `failure`, or `unknown`. The graph automatically **deduplicates**: if a semantically similar chain exists (cross-encoder score > 0.85), it merges instead of creating a duplicate — bumping the frequency counter and updating the outcome.

#### 6. Graph Query — `memory_graph_query`
Search the causal graph using **cross-encoder semantic matching** (not just keyword overlap). Supports tag-based pre-filtering for fast lookups. Returns the top 5 most relevant past experience chains.

#### 7. Graph Summary — `memory_graph_summary`
Digest of all learned causal knowledge: success/failure counts, most-frequent patterns, recent wins and failures. Useful for session bootstrapping.

#### 8. Context Compression — `compress_context`
Signal that the context window is overloaded. Returns what was rescued from the last compaction event and recent auto-captures — giving the agent visibility into what the memory system saved.

### Background Systems

#### Semantic YAML Weighter
Monitors `MEMORY.md` every 15s for YAML-fenced rule blocks. Rules with `weight >= 1.0` get pinned directly into the system prompt as `CRITICAL CONSTRAINT`s, bypassing retrieval entirely:

```markdown
<!--yaml
rules:
  - weight: 1.0
    constraint: "Never delete production data"
  - weight: 1.0
    constraint: "Always confirm before sending external messages"
  - weight: 0.5
    preference: "Prefer TypeScript over JavaScript"
-->
```

Only weight >= 1.0 rules get pinned. Everything else stays in normal retrieval.

#### In-Process Sleep Cycle
An in-process scheduler (no `child_process`, no shell exec) that runs maintenance every ~24 hours:
1. **Prune the causal graph** — remove nodes older than 90 days with frequency=1, hard cap at 500 nodes
2. **Decay utility scores** — multiply all scores by 0.99x, preventing stale high-scoring memories from dominating forever
3. **Truncate logs** — remove auto-captures and episodes older than 30 days
4. **Write consolidation context** — summarizes recent auto-captures and episodes to `consolidation_context.md` for the next agent session to reference

The scheduler checks every 6 hours but only runs maintenance once per 20-hour window (dedup guard). No external cron or shell commands needed — runs entirely within the plugin process.

## How It's Built

**Pure JavaScript/TypeScript** — no native binaries, no compilation dependencies. OpenClaw's plugin installer uses `npm install --ignore-scripts`, so native modules would fail silently.

| Component | Implementation | Why |
|---|---|---|
| Cross-encoder | `@huggingface/transformers` (ONNX) | Pure JS, runs locally, no API keys, singleton cached |
| SQLite access | `sql.js` (Emscripten/WASM) | Read-only against OpenClaw's DB, no native build step |
| FTS5 pre-filter | sql.js + JS fallback | Fast BM25 ranking, falls back to keyword matching if FTS5 unavailable |
| Utility scores | JSON sidecar file | Plugin-owned, no concurrent-write risk with OpenClaw |
| Knowledge graph | JSON file | Zero dependencies, human-readable, auto-pruned |
| Episodic memory | JSONL append-only | Low-overhead, auto-truncated |
| Auto-captures | JSONL append-only | Deduped against DB, auto-truncated |
| YAML parsing | `yaml` | Standard YAML 1.2 parser |

**Architecture principle**: This plugin is **read-only** against OpenClaw's `main.sqlite`. It never writes to, modifies, or locks the core memory database. All plugin state lives in sidecar files that only this plugin touches:

| File | Purpose | Max Size |
|---|---|---|
| `utility_scores.json` | Reinforcement scores per memory ID | ~100 KB |
| `causal_graph.json` | Cause→action→effect chains (500 node cap) | ~500 KB |
| `auto_captured.jsonl` | Auto-captured high-value messages (30-day cap) | ~2 MB |
| `episodes.jsonl` | Session episode summaries (30-day cap) | ~1 MB |

Total disk overhead: **< 4 MB**. RAM overhead: **~92 MB** (mostly the cross-encoder model singleton).

## Requirements

- OpenClaw `v2026.2.x` or later
- Node.js 18+
- ~100 MB RAM for the cross-encoder model
- ~800 MB disk for `node_modules` (first install)

## Installation

```bash
cd ~/.openclaw/extensions
git clone https://github.com/stanistolberg/openclaw-memory-max
cd openclaw-memory-max
npm install
npm run build
openclaw plugins enable openclaw-memory-max
# Restart the gateway to load the plugin
```

The plugin declares `kind: "memory"` which means it takes the exclusive memory slot. Enabling it automatically disables `memory-core` and `memory-lancedb`.

## Verify Installation

```bash
# Check plugin status
openclaw plugins list | grep memory-max

# Check sidecar files
npm run audit

# Check gateway logs for initialization
journalctl --user -u openclaw-gateway --since "5 min ago" | grep memory-max
```

You should see:
```
[openclaw-memory-max] Initializing SOTA Memory Cluster v3...
[openclaw-memory-max] ✓ Precision Reranker + Deep Multi-Hop Search active.
[openclaw-memory-max] ✓ Semantic Rule Weighter watching MEMORY.md.
[openclaw-memory-max] ✓ Context Compressor registered.
[openclaw-memory-max] ✓ Causal Knowledge Graph live (semantic + dedup).
[openclaw-memory-max] ✓ Lifecycle hooks registered (auto-recall, auto-capture, compaction-rescue).
[openclaw-memory-max] ✓ Episodic Memory hooks registered (session segmentation).
[openclaw-memory-max] All systems nominal. SOTA Memory Matrix ACTIVE.
```

## Project Structure

```
src/
  index.ts        — Plugin entrypoint, registers all modules + hooks
  reranker.ts     — Cross-encoder singleton, precision search, deep search, reward/penalize (4 tools)
  hooks.ts        — Lifecycle hooks: auto-recall, auto-capture, compaction rescue
  episodic.ts     — Session segmentation via session_start/session_end hooks
  graph.ts        — Causal knowledge graph with semantic search, dedup, pruning (3 tools)
  weighter.ts     — Semantic YAML rule pinner (watches MEMORY.md every 15s)
  compressor.ts   — Context compression tool with rescue data (1 tool)
  db.ts           — Read-only SQLite access, FTS5 pre-filter, utility score sidecar
  sleep-cycle.ts  — Nightly consolidation cron with decay, pruning, truncation
dist/             — Compiled CommonJS output (ships with repo)
```

## Research Basis

| Feature | Inspired By |
|---|---|
| Cross-encoder reranking | ColBERT, MS MARCO reranking benchmarks |
| Utility-weighted retrieval | MemRL (reinforcement-weighted memory), AgeMem (utility decay) |
| Multi-hop search | STORM (iterative retrieval), RAG-Fusion (reciprocal rank fusion) |
| Causal knowledge graph | ActMem (action-conditioned memory), CausalKG |
| Episodic memory | MemGPT/Letta (episodic vs semantic separation) |
| Auto-recall hooks | Zep, Mem0 (proactive memory injection) |
| Sleep cycle consolidation | Memory consolidation theory (Complementary Learning Systems) |
| Utility decay | Ebbinghaus forgetting curve applied to retrieval scores |

## Changelog

### 3.0.0

**Proactive memory system — the agent no longer needs to explicitly search.**

- **NEW: Lifecycle hooks** — `before_agent_start` (auto-recall), `agent_end` (auto-capture), `before_compaction` (memory rescue)
- **NEW: Episodic memory** — `session_start`/`session_end` hooks track sessions as episodes with summaries, tools used, and key decisions
- **NEW: `deep_memory_search` tool** — multi-hop retrieval: query → extract concepts → re-query → merge + deduplicate
- **NEW: FTS5/BM25 pre-filter** — narrows candidates before cross-encoder scoring (20 instead of 100), with JS keyword fallback
- **NEW: Cross-encoder model singleton** — loads once, stays cached (~500ms saved per search call)
- **NEW: Graph deduplication** — similar chains auto-merge (cross-encoder score > 0.85) with frequency tracking
- **NEW: Graph pruning** — removes old low-frequency nodes, hard cap at 500
- **NEW: Tag-based graph index** — fast pre-filtering when query matches known tags
- **NEW: Utility score decay** — scores decay by 0.99x nightly for inactive memories
- **NEW: Auto-truncation** — captures and episodes older than 30 days are cleaned up
- `precision_memory_search` now returns top-K results (was single result)
- Graph similarity upgraded from Jaccard token overlap to cross-encoder semantic matching
- `compress_context` now reports rescued content from last compaction event
- Sleep cycle enhanced: reads auto-captures + episodes, runs graph pruning + score decay
- `memory_graph_summary` now includes most-frequent patterns

### 2.0.0
- Migrated to current OpenClaw plugin API (`name`/`parameters`/`execute` with structured returns)
- Replaced native deps (`better-sqlite3`, `@xenova/transformers`) with pure-JS alternatives (`sql.js`, `@huggingface/transformers`)
- Utility scores moved from `main.sqlite` column to plugin-owned sidecar (`utility_scores.json`)
- Plugin is now read-only against OpenClaw's `main.sqlite`
- Added `configSchema` to manifest (required by current OpenClaw loader)
- Fixed template literal parse errors, YAML fence regex, destructive systemPrompt overwrite

### 1.1.0
- Initial release

## License

MIT
