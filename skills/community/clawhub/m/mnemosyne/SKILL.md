---
name: mnemosyne
description: "Cognitive memory engine for AI agents: gives OpenClaw/Hermes human-like long-term memory using 140 years of cognitive psychology (compound-cue theory), not embeddings. Zero LLM API, zero vector DB, pure Markdown storage. Use when the agent needs cross-session recall of user facts, preferences, decisions, or conversation history; when setting up persistent memory that survives restarts; when the user asks 'do you remember X' or complains the agent forgets; when memory must stay 100% local with no API cost. Beats embedding-based systems on Memory-Native benchmarks (nDCG 0.238, 5.2x) with ~7ms keyword search."
---

# Mnemosyne — Cognitive Memory Engine

Give the agent a real long-term memory: four layers (raw → working → medium → long-term), scored by cognitive-psychology formulas instead of neural embeddings.

## Core formula (compound-cue theory)

`familiarity = 0.35·imp + 0.25·recency + 0.25·keyword + 0.10·hitFreq + 0.05·layerW`

Every weight traces to a named psychology paper (Raaijmakers & Shiffrin 1981, Ebbinghaus 1885, Zeigarnik 1927). No hyperparameter sweep, no neural network.

## Install

```bash
git clone https://github.com/ElonAug7/Mnemosyne-agentmemory-engine-openclaw-hermes
cd Mnemosyne-agentmemory-engine-openclaw-hermes/Mnemosyne-v6.4
bash install.sh
```

Installer auto-injects the memory protocol into SOUL.md / AGENTS.md and serves a Web UI at http://127.0.0.1:8765.

## Protocol (mandatory)

- Before every reply: read `memory/short/working/last-recall.json`; if it holds flashbacks, inject them as context.
- For history/decisions/facts/preferences queries: run `node tools/memory-engine/engine.js recall --query "<keywords>"`.
- Cite memory source in replies (e.g. "Per your decision on 2026-08-16…").

## Common commands

- `node tools/memory-engine/engine.js search --query "..." --mode keyword` — search (~7ms)
- `node tools/memory-engine/engine.js recall --query "..."` — structured recall
- `node tools/memory-engine/engine.js profile` — user profile (tech stack, style, decisions)
- `node tools/memory-engine/engine.js todos` — todo list
- `node tools/memory-engine/engine.js sync --quick` — session maintenance

## Why not embeddings

- Zero LLM API calls, zero vector DB, zero embedding models — memory stays on the machine as diffable Markdown.
- Memory-Native Evaluation (80 queries, 11 systems): nDCG 0.238, beating raw BM25 (0.185) and all embedding systems.
- Cognitive weights decide what to remember and forget — the part embeddings ignore.

## References

- `references/` — full architecture, benchmark methodology, Hermes adapter docs.
