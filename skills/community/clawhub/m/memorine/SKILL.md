---
name: memorine
description: Human-like memory for AI agents. Facts, events, procedures, contradiction detection, forgetting curve, and cross-agent sharing. Pure Python + SQLite.
version: 0.2.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: memorine
        bins: [memorine]
    entry: uv run python -m memorine.mcp_server
    homepage: https://github.com/osvfelices/memorine
---

# Memorine

Persistent memory for OpenClaw agents. No APIs, no Docker, no external services. Just Python and SQLite.

## What it does

- **Facts** -- store, recall, and search with full-text search (FTS5). Near-duplicates are reinforced, contradictions are flagged automatically.
- **Forgetting curve** -- memories decay over time if not accessed, just like human memory. Old garbage cleans itself up.
- **Events** -- log what happened with causal chains (this caused that, which caused this other thing).
- **Procedures** -- track multi-step workflows, learn which steps tend to fail, anticipate what you will need before starting a task.
- **Cross-agent sharing** -- agents share facts with each other or the whole team through the same database.
- **Semantic search** (optional) -- install `memorine[embeddings]` to add meaning-based search on top of keyword search.

## 14 MCP tools

Once installed, your agents get access to:

| Tool | What it does |
|------|-------------|
| `memorine_learn` | Store a fact. Detects contradictions. |
| `memorine_learn_batch` | Batch-learn multiple facts at once. |
| `memorine_recall` | Search memory by query. Ranked by importance and recency. |
| `memorine_log_event` | Record an event. Supports causal chains. |
| `memorine_events` | Search past events by text or tags. |
| `memorine_share` | Share a fact with another agent or the team. |
| `memorine_team_knowledge` | Get collective knowledge across agents. |
| `memorine_profile` | Full cognitive profile of what an agent knows. |
| `memorine_anticipate` | Predict what you need for a task before starting. |
| `memorine_procedure_start` | Start tracking a procedure. |
| `memorine_procedure_step` | Log a step result in a running procedure. |
| `memorine_procedure_complete` | Mark a procedure as done. |
| `memorine_correct` | Fix a fact that turned out to be wrong. |
| `memorine_stats` | Database stats: facts, events, procedures, db size. |

## Setup

Install Memorine:

```bash
pip install memorine
```

Add the MCP server to your OpenClaw config (`openclaw.json`):

```json
{
  "mcpServers": {
    "memorine": {
      "command": "python3",
      "args": ["-m", "memorine.mcp_server"]
    }
  }
}
```

Allow the tools for your agents:

```json
{
  "tools": {
    "allow": [
      "memorine_learn",
      "memorine_recall",
      "memorine_log_event",
      "memorine_events",
      "memorine_share",
      "memorine_team_knowledge",
      "memorine_profile",
      "memorine_anticipate",
      "memorine_procedure_start",
      "memorine_procedure_step",
      "memorine_procedure_complete",
      "memorine_correct",
      "memorine_stats",
      "memorine_learn_batch"
    ]
  }
}
```

Optional semantic search (adds meaning-based matching on top of keyword search):

```bash
pip install memorine[embeddings]
```

## Security

Each agent can only modify its own data. Forget, correct, link, and procedure operations all validate ownership. No agent can touch another agent's memories.

## How it works

Everything lives in a single SQLite file at `~/.memorine/memorine.db`. FTS5 handles keyword search, triggers keep indexes in sync, and WAL mode allows concurrent reads. The forgetting curve uses `retention = e^(-days / stability)` where stability grows each time a memory is accessed. No LLM needed for any of this.
