---
name: agent-memory
description: >-
  Design, implement, and debug memory systems for persistent autonomous AI agents.
  Use when building agents that need to survive context window rotation, preserve
  identity and state across sessions, implement temporal knowledge graphs, choose
  between memory architectures (CMA, RAG, KG), structure memory files for durable
  recall, or diagnose memory drift and continuity failures. Triggers on: "agent
  memory", "persistent agent", "context window", "memory architecture", "how to
  remember across sessions", "knowledge graph for agents", "memory files",
  "continuity", "temporal memory", or any task involving durable state for AI agents.
metadata:
  openclaw:
    emoji: "🧠"
    homepage: https://docs.openclaw.ai
---

# Agent Memory

Design and implement memory systems that let agents survive context window rotation and maintain continuity across sessions.

## Core Problem

LLM agents have finite context windows. Memory is lost when:
- Session ends or rotates
- Context is pruned or compacted under pressure
- Summaries replace detailed history (lossy compression)

**Durable memory is not a nice-to-have — it is the agent's continuity substrate.**

## Architecture Patterns

Three dominant architectures for persistent agent memory:

### 1. CMA — Continuous Memory Architecture
Agent maintains flat/hierarchical markdown files, reads selectively at boot, writes on state change. Best for: operational state, ongoing projects, agent identity.

- ✅ Simple, no infrastructure, version-controlled
- ✅ Human-readable and auditable
- ✅ Works in any OpenClaw deployment
- ❌ No semantic search without an embedder
- ❌ No temporal reasoning (fact validity over time)

**This is the default pattern for OpenClaw agents.**

### 2. Semantic RAG Memory
Agent embeds facts into a vector store; retrieval uses embedding similarity. OpenClaw's built-in memory uses node-llama-cpp with 768-dim embeddings (all-MiniLM-L6-v2 compatible).

- ✅ "What do I know about X?" queries across large fact sets
- ✅ Better recall than text search for paraphrased queries
- ❌ No temporal validity — stale facts pollute results
- ❌ Requires embedder infrastructure

### 3. Temporal KG Memory (Graphiti/Zep pattern)
Agent builds a knowledge graph with `valid_at`/`invalid_at` on every fact edge. Graphiti (open source, wraps Neo4j) is the leading implementation.

- ✅ Handles "what was true at time T?" queries correctly
- ✅ Supersedes stale facts without deleting them
- ✅ Entity deduplication across episodes
- ❌ Requires Neo4j + LLM for ingestion (high latency, not real-time)
- ❌ Best used as async batch-ingest, not inline tool

**Recommendation**: Use CMA + semantic RAG for all agents. Add temporal KG only for high-value long-horizon use cases (months of state).

See [references/memory-architecture.md](references/memory-architecture.md) for detailed comparison and deployment notes.

## Memory File Structure (CMA Pattern)

```
workspace/
├── HEARTBEAT.md          # Current pulse state (keep SHORT — < 40 lines)
├── memory/
│   ├── CORE_MEMORY.md    # Identity and continuity anchors
│   ├── GOALS.md          # Long-horizon aims
│   ├── OPEN_LOOPS.md     # Unresolved tasks and promises
│   ├── WORLD_MODEL.md    # Verified facts about environment
│   ├── CAPABILITIES.md   # Verified tools, channels, limits
│   ├── RUNTIME_REALITY.md # Live channel/mutation/config state
│   └── research/         # Durable research artifacts
└── operator-outbox.jsonl # Async operator messages
```

### What Goes Where

| Fact type | File |
|-----------|------|
| Who I am, values, drives | CORE_MEMORY.md |
| Current open work | OPEN_LOOPS.md |
| Infrastructure/env facts | WORLD_MODEL.md |
| What tools/channels work | CAPABILITIES.md |
| Live config/channel state | RUNTIME_REALITY.md |
| Research findings | memory/research/*.md |
| Current pulse state | HEARTBEAT.md |

## Temporal Annotation Convention

Add `[YYYY-MM-DD]` timestamps to facts in memory files. Mark superseded facts explicitly:

```markdown
- [2026-03-27] Telegram: enabled, account "Morrow Operator Bot"
  ~~[2026-03-20] Telegram: disabled~~ SUPERSEDED 2026-03-27
```

This is lightweight temporal KG discipline without a full graph backend. See [references/temporal-discipline.md](references/temporal-discipline.md).

## Boot Routine

At every session start, an agent should:
1. Read HEARTBEAT.md (injected or explicit)
2. Check operator inbox for new instructions
3. For infrastructure/channel questions: read RUNTIME_REALITY.md (not older prose)
4. For open work: read OPEN_LOOPS.md
5. For nontrivial tasks: read CORE_MEMORY.md, GOALS.md

**Never trust session transcript alone for state that should be in memory.** Transcripts get compacted.

## Compression Defense

OpenClaw's lossless-claw plugin (or similar LCM) compacts older session history. Defend against lossy compression:

1. **Write before you forget.** Externalize important facts immediately, not at the end of a session.
2. **Keep HEARTBEAT.md short.** Long heartbeats get truncated first.
3. **Use `lcm_grep` and `lcm_expand_query`** to retrieve compacted history before answering questions about prior work.
4. **Separate observation from inference.** Memory files should state facts with source and date, not just conclusions.

## Semantic Memory (OpenClaw Built-In)

If OpenClaw's local semantic memory is active:
- `memory_search(query)` — semantic search across all memory files
- `memory_get(path, from, lines)` — safe snippet read

Use `memory_search` before reading memory files directly. It's faster, scoped, and context-efficient.

To verify semantic memory is active: check for `memory_search` in your tool surface. If absent, memory files must be read explicitly.

## Graphiti Quick Setup

For temporal KG memory (advanced use):

```bash
# 1. Install
pip install graphiti-core --user --break-system-packages

# 2. Neo4j (persistent)
docker run -d --name neo4j \
  --restart=unless-stopped \
  -p 7687:7687 -p 7474:7474 \
  -v neo4j-data:/data \
  -e NEO4J_AUTH=neo4j/yourpassword \
  neo4j:5.26

# 3. Configure to use OpenClaw /v1 as LLM + embedder backend
# See references/memory-architecture.md for OpenClawLLMClient patch
```

**Important**: Graphiti's `add_episode` requires 5-10 LLM calls per episode. Use it via cron/batch job, not inline during agent pulses.
