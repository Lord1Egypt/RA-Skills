# MindClaw

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-0.3.1-green.svg)](#)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-server-orange.svg)](#mcp-server-native-agent-integration)
[![ClawHub](https://img.shields.io/badge/clawhub.ai-ready-blueviolet.svg)](https://clawhub.ai)

> **Remember everything, forget nothing.**

Persistent memory and knowledge graph for AI agents.

MindClaw is a **structured long-term knowledge layer** for OpenClaw agents. Where OpenClaw stores raw conversational memory in Markdown files, MindClaw stores *curated facts, decisions, and relationships* with full metadata — conflict detection, confirmation reinforcement, importance scoring, and a knowledge graph. Memories sync back to OpenClaw's `MEMORY.md` so they are also searchable via OpenClaw's native `memory_search` tool.

## Features

- Persistent memory store in SQLite (zero external dependencies for core)
- **MCP server** — expose all tools natively to Claude Desktop, OpenClaw, and any MCP runtime
- **OpenClaw Markdown bridge** — `sync` exports to `MEMORY.md`; `md-import` imports daily logs; in-place update preserves agent's own notes
- **BM25 full-text search** (zero deps, superior to TF-IDF) + **Ollama semantic embeddings** (auto-detected, no extra packages)
- **Temporal decay at recall** — `--decay` flag: recent memories rank higher (`score × e^(-λ × age)`, same as OpenClaw)
- **MMR diversity re-ranking** — `--mmr` flag: reduces near-duplicate results (same algorithm as OpenClaw)
- **Agent namespaces** — scope memories per agent with `--agent <name>`
- **Pinned memories** — mark critical facts as never-decayable
- **Conflict detection** — warns before storing contradictory information
- **Confirmation system** — reinforce memories to boost their importance score
- **Context window builder** — token-aware memory block ready for LLM prompt injection
- **Timeline view** — reconstruct what happened in any time window
- **Auto-consolidation** — deduplicate near-identical memories
- Knowledge graph relations between memories
- Auto-capture decisions, errors, preferences, TODOs from raw text
- Archiving/decay lifecycle (pinned memories are immune)
- JSON export/import for backup and portability

## Installation

### Requirements

- Python 3.10+

### One command — for agents (Claude Desktop)

```bash
pip install mindclaw[mcp] && mindclaw mcp install
```

This installs MindClaw with the MCP server and registers it with **Claude Desktop** automatically.
Restart Claude Desktop — MindClaw tools are immediately available.

To register with **OpenClaw** instead:

```bash
pip install mindclaw[mcp] && mindclaw mcp install --target openclaw
```

### One command — for humans (full setup)

```bash
pip install mindclaw[mcp] && mindclaw setup
```

The `setup` wizard asks for your OpenClaw workspace path, agent name, and DB path,
then optionally registers with Claude Desktop / OpenClaw and does an initial sync.
You will never need flags again after this step.

### Install for CLI use only

```bash
pip install mindclaw
```

### Optional extras

```bash
pip install mindclaw[semantic]   # (unused in v0.3 — Ollama is auto-detected, no install needed)
pip install mindclaw[all]        # Everything: MCP + legacy extras
pip install mindclaw[dev]        # Development tools (pytest)
```

## First-Run Setup

After installing, run the setup wizard once to configure MindClaw permanently.
You will never need to pass `--db`, `--agent`, or `--workspace` flags again.

### For humans — interactive terminal wizard

```bash
mindclaw setup
```

The wizard asks four questions (press Enter to accept the default):

```
════════════════════════════════════════════════════
  MindClaw Setup Wizard
════════════════════════════════════════════════════
  Press Enter to accept the default shown in [brackets].

  OpenClaw workspace path [~/.openclaw/workspace]:
  Default agent name (leave blank = shared namespace) [none]: mybot
  Database path [~/.mindclaw/memory.db]:

  ✓ Config saved → ~/.mindclaw/config.json

  Register with Claude Desktop MCP? [Y/n]: y
  ✓ Claude Desktop config updated → ~/AppData/Roaming/Claude/claude_desktop_config.json
    Restart Claude Desktop to activate.
  Register with OpenClaw MCP? [Y/n]: y
  ✓ OpenClaw tools config updated → ~/.openclaw/tools.json
  Do an initial sync to MEMORY.md now? [Y/n]: y
  ✓ Synced 8 memories → ~/.openclaw/workspace/MEMORY.md

  MindClaw is ready!  Run `mindclaw --help` to see all commands.
```

### For OpenClaw agents — `setup_mindclaw` MCP tool

OpenClaw agents can not run interactive prompts, so MindClaw exposes a
`setup_mindclaw` MCP tool that accepts all settings as parameters.
The agent should ask the user for values (or infer them from context)
before calling the tool:

```
Agent asks: “What is your OpenClaw workspace path?”  → ~/my-workspace
Agent asks: “Should I scope memories to this agent?  If so, what name?”  → planner
Agent calls: setup_mindclaw(openclaw_workspace="~/my-workspace", agent_name="planner")
```

The tool saves the config, registers MindClaw in OpenClaw's tools registry,
and does an initial sync — all in one call.

### Settings priority

Once configured, the priority chain for every setting is:

```
CLI flag  >  MINDCLAW_* env var  >  ~/.mindclaw/config.json  >  built-in default
```

Config is stored in `~/.mindclaw/config.json` and looks like:

```json
{
  "db_path": null,
  "agent_id": "mybot",
  "openclaw_workspace": "/home/alex/.openclaw/workspace"
}
```

## Quickstart

```bash
# Store memories
mindclaw remember "We decided to use PostgreSQL for production" -c decision -t backend,db --pin
mindclaw remember "User prefers concise answers" -c preference -t ux -i 0.8

# Search with recency boost and diversity
mindclaw recall "postgresql decision" --decay --mmr

# Sync to OpenClaw — memories appear in native memory_search
mindclaw sync

# Import from OpenClaw daily log
mindclaw md-import ~/.openclaw/workspace/memory/2026-03-03.md
mindclaw md-import ~/.openclaw/workspace/MEMORY.md

# Check for conflicts before storing
mindclaw conflicts "We are switching to MySQL"

# Reinforce a memory that was confirmed again
mindclaw confirm <id>

# Context block for your LLM prompt
mindclaw context "What stack decisions have we made?" --max-tokens 1500

# Timeline of last 2 hours
mindclaw timeline --hours 2

# Merge near-duplicates
mindclaw consolidate

mindclaw list --sort "importance DESC" -n 10
mindclaw stats
```

## OpenClaw Integration

MindClaw is designed as the **structured knowledge layer** that sits above OpenClaw's raw Markdown memory.

```
OpenClaw native memory  →  conversational context, daily notes, speech acts
MindClaw                →  curated facts, decisions, graph links, conflict tracking
```

The two layers are connected through the Markdown bridge:

```bash
# Export MindClaw's structured memories to OpenClaw's MEMORY.md.
# The MindClaw block is updated in-place — your agent's own notes are preserved.
mindclaw sync

# Or specify a custom path
mindclaw sync --to ~/.openclaw/workspace/MEMORY.md

# Import existing OpenClaw memory files into MindClaw
mindclaw md-import ~/.openclaw/workspace/MEMORY.md
mindclaw md-import ~/.openclaw/workspace/memory/2026-03-01.md
```

After `sync`, MindClaw's structured memories are part of `MEMORY.md` and are automatically
found by OpenClaw's `memory_search` — no agent code changes needed.

**Search compatibility**: MindClaw's search pipeline mirrors OpenClaw's:

| Feature | OpenClaw | MindClaw |
|---|---|---|
| BM25 keyword search | ✓ | ✓ |
| Semantic embeddings | local GGUF / OpenAI / Gemini | Ollama (auto-detect) |
| Temporal decay | `--temporalDecay` | `--decay` + `--halflife` |
| MMR diversity | `mmr.enabled` | `--mmr` + `--mmr-lambda` |
| Per-agent isolation | per-agentId SQLite | `--agent <name>` |

**What MindClaw adds on top of OpenClaw:**

| Feature | Description |
|---|---|
| Structured metadata | category, tags, importance, source per memory |
| Knowledge graph | explicit relations between memories (`link`, `graph`) |
| Conflict detection | warns before storing contradictions |
| Confirmation / reinforcement | `confirm` boosts importance; tracked as `confirmed×N` |
| Auto-capture | extracts memories from free text automatically |
| Deduplication | `consolidate` merges near-identical memories persistently |

## Command Reference

| Command | Aliases | Purpose | Example |
|---|---|---|---|
| `setup` | — | One-time setup wizard (workspace, agent, DB, MCP registration) | `mindclaw setup` |
| `remember` | `r`, `add` | Save a new memory | `mindclaw remember "text" -c note -t tag1,tag2 -i 0.6 --pin` |
| `recall` | `search`, `q` | BM25 + Ollama search; `--decay` for recency boost, `--mmr` for diversity | `mindclaw recall "query" -n 10 --decay --mmr` |
| `sync` | — | Export memories to OpenClaw's MEMORY.md (in-place update) | `mindclaw sync [--to PATH] [--workspace PATH]` |
| `md-import` | — | Import from OpenClaw MEMORY.md or daily log | `mindclaw md-import ~/.openclaw/workspace/MEMORY.md` |
| `get` | — | Fetch one memory by ID | `mindclaw get <id>` |
| `list` | `ls` | List memories with filters | `mindclaw list -c decision -t backend --pinned` |
| `forget` | `rm`, `del` | Archive or hard-delete | `mindclaw forget <id> --hard` |
| `pin` | — | Pin a memory (never decayed) | `mindclaw pin <id>` |
| `unpin` | — | Remove pin | `mindclaw unpin <id>` |
| `confirm` | — | Reinforce a memory | `mindclaw confirm <id>` |
| `conflicts` | — | Check content for conflicts | `mindclaw conflicts "new fact"` |
| `consolidate` | — | Merge near-duplicates | `mindclaw consolidate --threshold 0.85` |
| `timeline` | — | Chronological session view | `mindclaw timeline --hours 6` |
| `context` | — | Build LLM context block | `mindclaw context "query" --max-tokens 2000` |
| `link` | — | Create graph relation | `mindclaw link <source_id> <target_id> -r depends_on -b` |
| `graph` | — | Show connected subgraph | `mindclaw graph <id> -d 2 --json` |
| `capture` | `cap` | Extract memories from text | `mindclaw capture -f ./conversation.txt --dry-run` |
| `stats` | — | Show DB/store stats | `mindclaw stats` |
| `decay` | — | Apply decay + archive weak memories | `mindclaw decay --threshold 0.05` |
| `export` | — | Export all data to JSON | `mindclaw export -o backup.json` |
| `import` | — | Import JSON backup | `mindclaw import backup.json --replace` |
| `mcp install` | — | Register with Claude/OpenClaw | `mindclaw mcp install --target openclaw` |
| `mcp serve` | — | Start MCP stdio server | `mindclaw mcp serve` |
| `mcp config` | — | Print raw MCP config JSON | `mindclaw mcp config` |

## MCP Server — Native Agent Integration

MindClaw runs as a native MCP (Model Context Protocol) server, meaning Claude, OpenClaw agents,
and any MCP-compatible runtime can call its tools **directly**, without any shell wrappers.

### Register in one command

```bash
# Claude Desktop
pip install mindclaw[mcp] && mindclaw mcp install

# OpenClaw
pip install mindclaw[mcp] && mindclaw mcp install --target openclaw

# With a custom agent namespace + custom DB path
mindclaw mcp install --agent mybot --db ~/agents/mybot/memory.db
```

### Tools exposed to the agent

| MCP Tool | What the agent can do |
|---|---|
| `setup_mindclaw` | **One-shot setup**: configure MindClaw + register + initial sync |
| `remember` | Store facts, decisions, preferences, errors |
| `recall` | BM25 + Ollama hybrid search with temporal decay and MMR |
| `context_block` | Get a token-limited prompt injection block |
| `capture` | Auto-extract memories from any text |
| `confirm` | Reinforce an existing memory |
| `forget` | Archive or delete a memory |
| `pin_memory` | Mark memory as permanent (no decay) |
| `timeline` | Reconstruct what happened in the last N hours |
| `consolidate` | Merge near-duplicate memories |
| `link` | Connect two memories in the knowledge graph |
| `stats` | Check store health |
| `sync_openclaw` | Export to OpenClaw's MEMORY.md in one call |
| `import_markdown` | Import bullets from any OpenClaw Markdown file |

### Recommended agent loop

```
1. context_block(query)     → inject relevant context before answering
2. remember(content)        → store key facts and decisions after acting
3. capture(conversation)    → extract structured memories from session logs
4. confirm(id)              → reinforce memories that proved correct
5. sync_openclaw()          → push to OpenClaw's MEMORY.md (cross-tool visibility)
6. consolidate()            → periodic dedup maintenance
```

## Agent Namespaces

Isolate memories per agent with `--agent`:

```bash
mindclaw --agent planner remember "Sprint goal: ship auth module" -c decision
mindclaw --agent executor remember "auth module PR #42 merged" -c fact
mindclaw --agent planner recall "sprint goals"
```

Or set the environment variable for the whole session:

```bash
export MINDCLAW_AGENT=planner
mindclaw remember "..."    # scoped to 'planner'
```

## Architecture

Core modules:

| Module | Responsibility |
|---|---|
| `store.py` | SQLite persistence — memory CRUD, export/import, Markdown bridge, decay lifecycle |
| `search.py` | Hybrid BM25 + Ollama search engine with temporal decay and MMR re-ranking |
| `context.py` | Token-aware context block builder, conflict detection, cluster summarization |
| `graph.py` | Knowledge graph — edge CRUD, shortest-path, subgraph traversal |
| `capture.py` | Rule-based extraction of facts, decisions, errors, prefs from free text |
| `config.py` | Persistent config file — read/write `~/.mindclaw/config.json` |
| `cli.py` | Argument parser and all command handlers |
| `mcp_server.py` | FastMCP server factory, **15 MCP tools**, Claude Desktop + OpenClaw install helpers |

High-level flow:

```text
  CLI command                     MCP-compatible agent
       ↓                                  ↓
  cli.py (build_parser)        mcp_server.py (FastMCP)
            \                       /
             store / search / graph / capture
                         ↓
                  ~/.mindclaw/memory.db  (SQLite)
                         ↓
             export_to_markdown() / import_from_markdown()
                         ↓
             ~/.openclaw/workspace/MEMORY.md
```

## Configuration

Settings are resolved with the following priority chain:

```
CLI flag  >  MINDCLAW_* env var  >  ~/.mindclaw/config.json  >  built-in default
```

Run `mindclaw setup` once to write `~/.mindclaw/config.json` — afterwards all commands pick up your
workspace path, agent name, and DB path automatically.

| Setting | Default | Flag | Env var |
|---|---|---|---|
| DB path | `~/.mindclaw/memory.db` | `--db <path>` | `MINDCLAW_DB` |
| Agent namespace | `""` (shared) | `--agent <name>` | `MINDCLAW_AGENT` |
| OpenClaw workspace | `~/.openclaw/workspace` | `--workspace <path>` | `MINDCLAW_OPENCLAW_WORKSPACE` |
| Config file | `~/.mindclaw/config.json` | — | — |

```bash
# Use a flag (overrides config + env)
mindclaw --db ./data/memory.db stats

# Use env var (overrides config only)
export MINDCLAW_DB=./data/memory.db
mindclaw stats

# Or just run setup once and forget about flags
mindclaw setup
```

## Publishing to ClawHub

MindClaw ships with a [`clawhub.yaml`](clawhub.yaml) manifest that declares capabilities, config, and metadata for [clawhub.ai](https://clawhub.ai).

To publish:

1. Bump version in `pyproject.toml`, `clawhub.yaml`, and `src/mindclaw/__init__.py`
2. Update [`CHANGELOG.md`](CHANGELOG.md)
3. Tag: `git tag v0.x.x`
4. Push: `git push origin main --tags`
5. ClawHub picks up the release automatically from the tag

The manifest exposes all CLI commands and MCP tools as agent-consumable capabilities, so any OpenClaw-compatible runtime can discover and invoke them.

## Programmatic usage

MindClaw can also be used as a Python library:

```python
from mindclaw.store import MemoryStore, Memory

store = MemoryStore(db_path="./my_agent.db")

# Store a pinned memory (never decayed)
mem = Memory(content="User prefers dark mode", category="preference", tags=["ui"], pinned=True)
store.add(mem)

# Confirm an existing memory (boost importance)
store.confirm(mem.id)

# Check for conflicts before storing
conflicts = store.find_conflicts("User prefers light mode")

# Search — BM25 by default; Ollama semantic layer auto-detected
from mindclaw.search import SearchEngine
engine = SearchEngine(store)
engine.rebuild()

# Basic search
results = engine.search("dark mode", top_k=5)

# With recency boost and diversity (mirrors OpenClaw's pipeline)
results = engine.search(
    "dark mode",
    temporal_decay=True,
    temporal_halflife=30,   # score halves every 30 days
    mmr=True,
    mmr_lambda=0.7,          # 1.0=pure relevance, 0.0=max diversity
)

# Ollama status
print("Ollama available:", engine.ollama.available)

# Sync to OpenClaw's MEMORY.md
result = store.sync_openclaw()  # auto-detects ~/.openclaw/workspace
result = store.sync_openclaw("~/my-workspace")  # custom path

# Export to any Markdown file (in-place block update)
store.export_to_markdown("~/MEMORY.md", agent_id="mybot")

# Import from OpenClaw MEMORY.md or daily log
count = store.import_from_markdown("~/MEMORY.md", agent_id="mybot")
count = store.import_from_markdown("~/memory/2026-03-01.md")

# Build a context block for LLM prompt injection
from mindclaw.context import ContextBuilder
builder = ContextBuilder(store)
block = builder.build("user UI preferences", max_tokens=1500)
system_prompt = "You are a helpful assistant.\n\n" + block.text

# Timeline — what happened in the last hour?
recent = store.get_timeline(since=time.time() - 3600)

# Deduplicate
store.consolidate_duplicates()

# Graph
from mindclaw.graph import KnowledgeGraph
graph = KnowledgeGraph(store)
graph.link(mem.id, other_id, "related_to")
sub = graph.subgraph(mem.id, depth=2)

# Auto-capture
from mindclaw.capture import AutoCapture
capture = AutoCapture(store)
captured = capture.process("Meeting notes: deploy v2 Friday", source="agent")
```

## Project Structure

```text
.
├── pyproject.toml          # Package metadata & dependencies
├── clawhub.yaml            # ClawHub registry manifest
├── README.md
├── CONTRIBUTING.md         # Contribution guide
├── CHANGELOG.md            # Version history
├── LICENSE                 # MIT
└── src/
    └── mindclaw/
        ├── __init__.py     # Version & package init
        ├── capture.py      # Auto-extraction from text
        ├── cli.py          # CLI parser & command handlers
        ├── config.py       # Persistent config (~/.mindclaw/config.json)
        ├── context.py      # Context window builder & conflict detection
        ├── graph.py        # Knowledge graph (edges, subgraph)
        ├── mcp_server.py   # MCP server (FastMCP) + install helpers
        ├── search.py       # BM25 + Ollama hybrid search engine
        └── store.py        # SQLite memory store + Markdown bridge
```

## Roadmap

- [x] MCP (Model Context Protocol) server mode
- [x] Agent namespaces / memory isolation
- [x] Pinned memories (immune to decay)
- [x] Conflict detection on store
- [x] Context window builder
- [x] Memory confirmation / reinforcement
- [x] Timeline / episodic view
- [x] Auto-consolidation of duplicates
- [x] BM25 search (replaces TF-IDF)
- [x] Ollama semantic embeddings (zero extra deps)
- [x] Temporal decay at query time (`--decay`)
- [x] MMR diversity re-ranking (`--mmr`)
- [x] OpenClaw Markdown bridge (`sync` / `md-import`)
- [x] One-command setup wizard (`mindclaw setup` + `setup_mindclaw` MCP tool)
- [x] Persistent config (~/.mindclaw/config.json) — configure once, use everywhere
- [ ] Persistent Ollama embedding cache (avoid re-embedding on every search call)
- [ ] Web dashboard for memory visualization
- [ ] Multi-agent shared memory (read-across namespaces)
- [ ] Plugin system for custom capture rules
- [ ] ClawHub verified badge

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for setup, branching, and PR guidelines.

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for version history.

## License

MIT — see [`LICENSE`](LICENSE) for details.