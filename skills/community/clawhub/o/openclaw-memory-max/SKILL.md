---
name: openclaw-memory-max
description: SOTA Memory Suite — auto-recall, cross-encoder reranking, multi-hop deep search, causal knowledge graph, episodic memory, and nightly sleep-cycle consolidation.
metadata:
  openclaw:
    emoji: "🧠"
    homepage: "https://github.com/stanistolberg/openclaw-memory-max"
---

# OpenClaw Memory Max

You have the **Memory Max** SOTA memory system. It upgrades your memory capabilities far beyond the default memory-core plugin.

## What's Active

### Automatic (no action needed)
- **Auto-Recall**: Before every turn, your most relevant memories are automatically injected into your context as `<relevant-memories>` XML blocks. You don't need to search — relevant context appears automatically.
- **Auto-Capture**: After conversations, high-value user messages (rules, corrections, preferences) are automatically captured for the nightly consolidation cycle.
- **Compaction Rescue**: When the context window is compressed, important content is rescued before it's evicted.
- **Episodic Memory**: Each session is logged as an episode with timestamps, tools used, and key decisions.
- **Sleep Cycle**: An in-process scheduler runs maintenance every ~24h — prunes the causal graph, decays stale utility scores, truncates old logs, and writes consolidation context for the next session.

### Tools Available

#### `precision_memory_search`
Cross-encoder reranked search with utility weighting. Returns the top K most relevant memories.
```json
{"query": "deployment configuration", "topK": 5}
```
Use this when you need to find specific information in memory. More precise than the default memory search — uses a cross-encoder model that reads query + candidate together, not just cosine similarity.

#### `deep_memory_search`
Multi-hop retrieval. Searches once, extracts key concepts from results, searches again with those concepts, then merges everything.
```json
{"query": "why did the migration fail last time"}
```
Use this for complex questions where the answer might be spread across multiple related memories.

#### `reward_memory_utility`
Reinforce a memory that proved useful. Increases its future retrieval priority.
```json
{"memoryId": "abc-123", "rewardScalar": 0.2}
```
Call this after a memory helped you give a correct answer.

#### `penalize_memory_utility`
Penalize a memory that caused a hallucination or was irrelevant.
```json
{"memoryId": "abc-123", "penaltyScalar": 0.2}
```
Call this when a retrieved memory led you astray.

#### `memory_graph_add`
Log a cause-action-effect chain. Automatically deduplicates against existing chains.
```json
{"cause": "nginx misconfigured", "action": "added proxy_pass", "effect": "site loaded", "outcome": "success", "tags": ["nginx"]}
```
Call this AFTER completing any meaningful action to build your experience database.

#### `memory_graph_query`
Search past experience using semantic matching.
```json
{"query": "website not loading", "outcomeFilter": "success"}
```
Call this BEFORE taking major actions to check what worked or failed in the past.

#### `memory_graph_summary`
Get a digest of all learned causal knowledge — success/failure counts, most-frequent patterns, recent outcomes.
```json
{}
```
Useful at the start of a session to bootstrap your awareness.

#### `compress_context`
Signal that context compression is needed. Returns what was rescued from the last compaction.
```json
{"compression_reason": "context window approaching limit after long debugging session"}
```

## Rules

1. **Auto-recall is always on** — you will see `<relevant-memories>` blocks in your context. Use them. Don't ignore injected memories.
2. **Reward useful memories** — when a memory helps you answer correctly, call `reward_memory_utility`. This trains the retrieval system.
3. **Penalize bad memories** — when a memory causes a hallucination, call `penalize_memory_utility`. This prevents future mistakes.
4. **Log causal chains** — after significant actions (tool use, decisions, fixes), call `memory_graph_add`. Your future self will thank you.
5. **Check experience before acting** — before major actions, call `memory_graph_query` to see if you've encountered this situation before.
6. **Use deep search for complex questions** — if `precision_memory_search` doesn't find what you need, try `deep_memory_search` which follows concept chains across memories.

## Configuration

All features are controlled via `configSchema` in the plugin manifest. Users configure these in their OpenClaw settings:

| Option | Default | Description |
|---|---|---|
| `enableRulePinning` | `false` | YAML rule pinning from MEMORY.md into system prompt. **Off by default** — must be explicitly opted in. |
| `enableAutoCapture` | `false` | Automatic capture of high-value user messages to sidecar files. **Off by default** — opt in if you want persistent message logging. |
| `enableAutoRecall` | `true` | Automatic memory injection before each agent turn. |

## YAML Rule Pinning (opt-in)

**Disabled by default.** Must be enabled via `enableRulePinning: true` in plugin config.

When enabled, users can pin critical constraints into the system prompt by adding a YAML block to MEMORY.md:

```markdown
<!--yaml
rules:
  - weight: 1.0
    constraint: "Never delete production data"
  - weight: 0.5
    preference: "Prefer TypeScript over JavaScript"
-->
```

Rules with weight >= 1.0 appear as CRITICAL CONSTRAINTs in your prompt. Always obey them.

**Security note**: Only enable this if you control write access to your `~/.openclaw/memory/MEMORY.md` file. Any process that can write to that file could influence agent behavior when pinning is enabled.
