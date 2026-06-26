---
name: "Obsidian Semantic Search"
description: "Semantic search across your Obsidian vaults using local embeddings (Ollama + pgvector). 10 MCP tools: hybrid/semantic/keyword search, file CRUD, batch reads, live re-indexing, and a monitoring dashboard. Fully local — no API keys, no cloud, zero cost."
version: "1.0.0"
emoji: "🧠"
homepage: "https://github.com/celstnblacc/obsidian-semantic-mcp"
user-invocable: true
disable-model-invocation: false

requires:
  bins: ["docker", "uv"]
  anyBins: ["python3", "python"]
  env: ["OBSIDIAN_VAULT"]
---

# Obsidian Semantic Search

Search your Obsidian vault by **meaning**, not just keywords. This skill installs and configures [obsidian-semantic-mcp](https://github.com/celstnblacc/obsidian-semantic-mcp) — a local-first MCP server that indexes your vault with vector embeddings (Ollama + pgvector) and exposes 10 tools to any MCP-compatible AI assistant.

## What You Get

### 10 MCP Tools

| Tool | What it does |
|------|-------------|
| `search_vault` | Semantic, keyword, or hybrid search with similarity scores |
| `simple_search` | Fast exact-text search across all files |
| `list_files` | Browse vault directories |
| `get_file` | Read a single file |
| `get_files_batch` | Read multiple files in one call |
| `append_content` | Append text to a file (creates if missing) |
| `write_file` | Overwrite a file completely |
| `recent_changes` | List recently modified files |
| `list_indexed_notes` | See all indexed notes with timestamps |
| `reindex_vault` | Force a full re-index |

### Monitoring Dashboard (port 8484)

- Real-time service health (PostgreSQL, Ollama, embedding model)
- Indexed notes count, vault coverage %, database size
- Search testing UI — test queries without leaving your browser
- Manual re-index trigger

### Search Modes

- **Hybrid** (default): Combines semantic meaning + keyword matching for best results
- **Semantic**: Search by meaning only — finds related content even with different wording
- **Keyword**: Exact text matching via PostgreSQL full-text search

## Installation

### Prerequisites

- **Docker Desktop** (running)
- **uv** (Python package manager): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **An Obsidian vault** on your local filesystem

### One-Liner Install

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/celstnblacc/obsidian-semantic-mcp/main/install.sh) --mode 2 --vault /path/to/your/vault
```

This clones the repo to `~/.local/share/obsidian-semantic-mcp`, installs the `osm` CLI, and runs the setup wizard in Docker mode.

### Manual Install

```bash
git clone https://github.com/celstnblacc/obsidian-semantic-mcp.git
cd obsidian-semantic-mcp
uv sync
uv run osm init
```

The wizard detects your OS and offers setup modes:

**macOS (4 modes):**
- **Mode 1:** Native (Homebrew — no Docker needed)
- **Mode 2:** Docker + host Ollama (if Ollama already installed)
- **Mode 3:** Full Docker (recommended — everything in containers)
- **Mode 4:** Docker + remote Ollama (SSH tunnel to a GPU server)

**Linux (3 modes):**
- **Mode 1:** Docker + host Ollama
- **Mode 2:** Full Docker (recommended)
- **Mode 3:** Docker + remote Ollama

### Verify Installation

```bash
osm status
```

Should show: Docker containers running, Ollama healthy, embedding model loaded, vault indexed.

### Register with Claude Desktop

The wizard auto-configures this, but if you need to do it manually:

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `~/.config/Claude/claude_desktop_config.json` (Linux):

```json
{
  "mcpServers": {
    "obsidian-semantic": {
      "command": "docker",
      "args": ["exec", "-i", "obsidian-semantic-mcp-mcp-server-1", "python3", "src/server.py"]
    }
  }
}
```

Restart Claude Desktop after adding.

## Configuration

Set these in `.env` or as environment variables:

| Variable | Required | Default | Notes |
|----------|----------|---------|-------|
| `OBSIDIAN_VAULT` | Yes | — | Path to your vault |
| `OBSIDIAN_VAULTS` | No | — | Comma-separated paths for multi-vault |
| `POSTGRES_PASSWORD` | Yes (Docker) | — | Database password |
| `EMBEDDING_MODEL` | No | `nomic-embed-text` | Ollama model (~7GB) |
| `RERANK_MODEL` | No | — | Optional cross-encoder for better ranking |
| `DASHBOARD_PORT` | No | `8484` | Monitoring dashboard port |

## Usage Examples

Once installed, your AI assistant can use these tools naturally:

**Semantic search:**
> "Search my vault for notes about authentication patterns"
> → Uses `search_vault` with hybrid mode, returns top 5 matches ranked by meaning

**Find and read:**
> "Find my meeting notes from last week and summarize them"
> → Uses `recent_changes` to find files, `get_files_batch` to read them

**Append to a note:**
> "Add this action item to my project-x.md file"
> → Uses `append_content` to add text without overwriting

**Re-index after bulk changes:**
> "I just reorganized my vault, re-index everything"
> → Uses `reindex_vault` to rebuild the full index

## Maintenance

```bash
osm status       # Check health
osm rebuild      # Rebuild Docker images after updates
osm remove       # Stop and clean up everything
```

## Architecture

- **PostgreSQL 17 + pgvector**: Stores 768-dim vector embeddings, IVFFlat index for fast cosine similarity search
- **Ollama (nomic-embed-text)**: Local embedding model — no API keys, no cloud calls
- **Watchdog file watcher**: Auto-re-indexes when vault files change (0.5s debounce)
- **LRU cache**: 256 entries, 10-min TTL — skips redundant Ollama calls for repeated queries

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Ollama not responding" | Run `osm status` — if Ollama is down, the dashboard has a "Start Ollama" button |
| Slow first search | First query loads the model into memory (~5s). Subsequent queries are <1s |
| Missing notes in search | Run `osm status` to check indexing coverage. Use dashboard to trigger re-index |
| Docker errors | Ensure Docker Desktop is running. Try `osm rebuild` to rebuild images |
| VirusTotal "suspicious" warning on install | This is a false positive — the skill *describes* searching vault content, which triggers pattern detection. Use `clawhub install obsidian-semantic-search --force` to proceed. The skill is MIT-0 licensed and contains no executable code beyond documentation. |

## Links

- **Source:** https://github.com/celstnblacc/obsidian-semantic-mcp
- **Changelog:** https://github.com/celstnblacc/obsidian-semantic-mcp/blob/main/CHANGELOG.md
- **Architecture:** https://github.com/celstnblacc/obsidian-semantic-mcp/blob/main/docs/ARCHITECTURE.md
- **License:** Apache 2.0 (source repo) / MIT-0 (this skill)

---

*Built by [celstnblacc](https://github.com/celstnblacc) — 207 unit tests, Docker + native install, multi-vault support.*
