# MindClaw

> Persistent memory and knowledge graph for AI agents. Remember everything, forget nothing.

MindClaw is a **structured long-term knowledge layer** for OpenClaw agents. Where OpenClaw stores raw conversational memory in Markdown files, MindClaw stores *curated facts, decisions, and relationships* with full metadata — conflict detection, confirmation reinforcement, importance scoring, and a knowledge graph.

Memories sync back to OpenClaw's `MEMORY.md` so they are also searchable via OpenClaw's native `memory_search` tool.

## Install

```bash
pip install mindclaw[mcp] && mindclaw setup
```

The `setup` wizard configures your workspace path, agent name, and registers MindClaw with Claude Desktop and/or OpenClaw in one step.

## What agents can do

| MCP Tool | Purpose |
|---|---|
| `setup_mindclaw` | One-call setup: configure, register with OpenClaw, initial sync |
| `remember` | Store a fact, decision, preference, or error with metadata |
| `recall` | BM25 + semantic hybrid search with temporal decay and MMR diversity |
| `context_block` | Token-limited memory block ready to inject into any LLM prompt |
| `capture` | Auto-extract structured memories from conversation text |
| `confirm` | Reinforce a memory that proved correct (boosts importance) |
| `forget` | Archive or hard-delete a memory |
| `pin_memory` | Mark a memory as permanent — immune to decay |
| `timeline` | Reconstruct what happened in the last N hours |
| `consolidate` | Merge near-duplicate memories automatically |
| `link` | Connect two memories in the knowledge graph |
| `stats` | Check store health and memory breakdown |
| `sync_openclaw` | Export all memories to OpenClaw's MEMORY.md |
| `import_markdown` | Import from any OpenClaw MEMORY.md or daily log |
| `unpin_memory` | Remove a pin from a memory |

## OpenClaw integration

MindClaw mirrors OpenClaw's search pipeline exactly:

| Feature | OpenClaw | MindClaw |
|---|---|---|
| BM25 keyword search | ✓ | ✓ |
| Semantic embeddings | local GGUF / OpenAI / Gemini | Ollama (auto-detect, zero deps) |
| Temporal decay | `--temporalDecay` | `--decay` + `--halflife` |
| MMR diversity | `mmr.enabled` | `--mmr` + `--mmr-lambda` |
| Per-agent isolation | per-agentId SQLite | `--agent <name>` |

After `mindclaw sync`, all structured memories appear in `MEMORY.md` and are found by OpenClaw's native `memory_search` — no agent code changes needed.

## Recommended agent loop

```
1. context_block(query)   → inject relevant context before answering
2. remember(content)      → store key facts and decisions after acting
3. capture(conversation)  → extract structured memories from session logs
4. confirm(id)            → reinforce memories that proved correct
5. sync_openclaw()        → push to OpenClaw's MEMORY.md (cross-tool visibility)
6. consolidate()          → periodic dedup maintenance
```

## Configuration

Run once, never repeat flags:

```bash
mindclaw setup
```

Saves `~/.mindclaw/config.json` with your workspace path, agent name, and DB path.
Priority chain: `CLI flag > MINDCLAW_* env var > config file > built-in default`

## Requirements

- Python 3.10+
- Zero mandatory dependencies (core uses only stdlib)
- Optional: `pip install mindclaw[mcp]` for MCP server
- Optional: Ollama running locally for semantic search (auto-detected)

## Source

GitHub: https://github.com/Blue8x/MindClaw
