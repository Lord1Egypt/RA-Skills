---
name: mindgardener
description: Local-first long-term memory for autonomous agents. Built for OpenClaw. Creates wiki knowledge graph from conversations, scores events by surprise, detects conflicts, and assembles token-budget context. Complements OpenClaw's built-in memory_search.
metadata:
  clawdbot:
    requires:
      bins: ["garden"]
    install:
      - id: mindgardener
        kind: pip
        package: mindgardener
        bins: ["garden"]
        label: "Install MindGardener CLI (pip)"
---

# MindGardener 🌱

**Your agents forget everything. This fixes it.**

*Built for OpenClaw. Complements the built-in `memory_search` tool.*

## How It Complements OpenClaw

| OpenClaw built-in | MindGardener adds |
|-------------------|-------------------|
| Search existing memory | **Create** memory from conversations |
| Manual MEMORY.md edits | **Auto-extract** entities → wiki pages |
| Flat text search | **Knowledge graph** (triplets + wikilinks) |
| — | **Surprise scoring** (unexpected = important) |
| — | **Conflict detection** (new info vs old) |
| — | **Multi-agent sync** |

## Features (v1.1)

- 🔍 **Provenance tracking** — know where every fact came from
- ⚔️ **Conflict detection** — flags when new info contradicts old
- 🚀 **Auto-injection** — context ready at session start
- ⏰ **Temporal decay** — old facts fade unless reinforced
- 🔒 **Concurrency** — file locks for multi-agent safety
- 🔮 **Associative recall** — follow wikilinks + graph traversal
- 📊 **Confidence levels** — not all facts are equally reliable
- 🤝 **Multi-agent sync** — merge per-agent memories to shared

## Quick Start

```bash
pip install mindgardener
garden init
```

Add to your nightly cron:
```bash
garden extract && garden surprise && garden consolidate
```

Add to session start (BOOTSTRAP.md or heartbeat):
```bash
garden inject --output RECALL-CONTEXT.md
```

## What Changes From Default OpenClaw?

- New folder: `memory/entities/` (wiki pages)
- New file: `graph.jsonl` (knowledge triplets)
- New file: `RECALL-CONTEXT.md` (auto-generated context)
- New file: `garden.yaml` (configuration)

Everything is markdown files. No database. Works offline.

## Requirements

- Python 3.10+
- No external APIs required
- For fully local: use `garden init --provider ollama`

## Links

- [GitHub](https://github.com/widingmarcus-cyber/mindgardener)
- [PyPI](https://pypi.org/project/mindgardener/)
- 172 tests passing
