# GraphRAG Builder Skill

Turn any documentation site into a runnable **MCP (Model Context Protocol) knowledge server** that Claude can query with semantic search and graph traversal.

Packaged as a [Claude Skill](https://www.anthropic.com/news/skills) — invoke it with prompts like *"build an MCP server from https://strudel.cc/workshop/"* and it walks you through a 5-stage pipeline that crawls the site, extracts concepts with an LLM, builds a knowledge graph, generates embeddings, and emits a standalone `server.py` you can drop into Claude Desktop.

First target site: [strudel.cc](https://strudel.cc/workshop/getting-started/) — a live-coding music library.

---

## Pipeline

| Stage | Script                          | Output                                    |
|-------|---------------------------------|-------------------------------------------|
| M1    | `scripts/crawl.py`              | `raw_content/*.json` — HTML + links/metadata per page |
| M2    | `scripts/extract_concepts.py`   | `extracted/*.json` — chunks + LLM-extracted concepts, tags, code, prerequisites |
| M3    | `scripts/build_graph.py`        | `graph.json` — networkx knowledge graph (concepts + relationships) |
| M4    | `scripts/build_embeddings.py`   | `embeddings/` — numpy vector indexes (chunks + concepts) |
| M5    | `scripts/generate_mcp_server.py`| `server.py` + `mcp_config.json` — runnable MCP server |

The final `output/<slug>-mcp/` folder is the deliverable — move `server.py`, `graph.json`, and `embeddings/` anywhere together.

---

## Quick Start

```bash
# 0. Install deps (once)
pip install -r requirements.txt
playwright install chromium

# 1. Crawl
python scripts/crawl.py --url https://strudel.cc/workshop/getting-started/ \
  --max-depth 3 --output ./output

# 2. Extract concepts (dry-run first, no API cost)
python scripts/extract_concepts.py --input ./output/strudel-cc-mcp --dry-run
ANTHROPIC_API_KEY=sk-ant-... python scripts/extract_concepts.py \
  --input ./output/strudel-cc-mcp --model haiku

# 3. Build graph
python scripts/build_graph.py --input ./output/strudel-cc-mcp

# 4. Build embeddings
python scripts/build_embeddings.py --input ./output/strudel-cc-mcp --smoke-test

# 5. Generate MCP server
python scripts/generate_mcp_server.py --input ./output/strudel-cc-mcp
```

Install into Claude Desktop by merging `output/strudel-cc-mcp/mcp_config.json` into `~/Library/Application Support/Claude/claude_desktop_config.json` under `"mcpServers"` and restarting Claude.

See [`SKILL.md`](./SKILL.md) for the full step-by-step skill instructions Claude follows, including troubleshooting, incremental re-runs, and dry-run validation.

---

## The 8 MCP Tools

Once installed, Claude can call these tools against the generated knowledge base:

| Tool | Description |
|------|-------------|
| `search(query, n=5)` | Semantic search over all content chunks |
| `get_concept(name)` | Concept details + chunks where it appears |
| `get_related(concept, n=5)` | Related concepts via graph edges |
| `get_learning_path(start, goal)` | Shortest concept path between topics |
| `get_prerequisites(concept)` | What must be understood first |
| `get_examples(concept)` | Code examples for a concept |
| `list_concepts(tag?, limit=20)` | Browse all indexed concepts |
| `get_page(url)` | All chunks for a specific doc page |

---

## Architecture Notes

- **Crawler**: `requests` first, automatic Playwright/Chromium fallback for JS-rendered pages. Incremental via SHA256 content hashes in SQLite.
- **Concept extraction**: Claude Haiku by default (fast/cheap), Sonnet opt-in for complex technical content. Chunks at ~500 words with section-aware splitting.
- **Graph**: `networkx` + JSON. Edge types: `MENTIONS`, `REQUIRES`, `HAS_CHUNK`, `LINKS_TO`, `RELATED`. Neo4j export planned for >10k nodes.
- **Embeddings**: Local `sentence-transformers` (`all-MiniLM-L6-v2`, ~80MB) — no API key, no database. Pure numpy index.
- **MCP server**: Self-contained generated Python file, reads the graph + embeddings from disk at startup.

---

## Project Layout

```
.
├── SKILL.md                  Claude Skill definition (the orchestration prompt)
├── scripts/
│   ├── crawl.py              M1: BFS crawler with JS fallback
│   ├── extract_concepts.py   M2: Chunking + LLM concept extraction
│   ├── build_graph.py        M3: networkx knowledge graph builder
│   ├── build_embeddings.py   M4: sentence-transformers index
│   └── generate_mcp_server.py M5: Self-contained MCP server emitter
├── evals/evals.json          Eval queries for checking server quality
├── references/               Reference materials (sample docs, etc.)
├── examples/                 Example outputs
├── output/                   Generated MCP packages (gitignored)
├── requirements.txt
├── IDEA.md                   Original project pitch
├── PLAN.md                   Architecture plan
└── TODO.md                   Deferred features & roadmap
```

---

## Status & Roadmap

Implemented end-to-end for text-based documentation sites. Verified on `strudel.cc`.

Deferred (see [`TODO.md`](./TODO.md)):

- **YouTube transcript ingestion** — `crawl.py` already collects video IDs in `youtube_ids`; M2 needs the fetch + chunk step using `youtube-transcript-api`.
- **Neo4j export** — for graphs exceeding ~10k nodes.
- **API-based embeddings** — optional OpenAI / Voyage backends.
- **Incremental graph merging** with orphan cleanup.
- **Graph visualization** — static HTML via `pyvis`.
- **Additional sources** — GitHub repos, Confluence/Notion, RSS feeds.

---

## Requirements

- Python 3.10+
- `ANTHROPIC_API_KEY` (only needed for M2 concept extraction)
- ~200MB disk for the sentence-transformers model cache (first run)

---

## License

MIT — see below. Use, modify, and redistribute freely.
