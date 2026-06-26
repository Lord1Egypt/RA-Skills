---
name: GraphRAGBuilderSkill
description: >
  Builds a fully runnable MCP (Model Context Protocol) knowledge server from any website or
  documentation URL. Crawls the site, extracts concepts using Claude, organizes them into a
  knowledge graph, generates vector embeddings, and produces a ready-to-install MCP server
  with 8 semantic search and graph traversal tools. Use this skill whenever the user wants
  to: build an MCP server from a website or docs, create a semantic search index over
  documentation, make a knowledge graph from a library or framework's docs, turn a tutorial
  site into a Claude-searchable knowledge base, index learning materials for AI retrieval, or
  build a "smart docs" assistant for any topic. Trigger even if the user just mentions
  "scraping docs", "indexing a site", "building a knowledge graph", or "making docs
  searchable in Claude".
---

# GraphRAG Builder Skill

Turns any documentation website into a runnable MCP knowledge server in 5 pipeline steps,
each run on the user's local machine using scripts in the `scripts/` folder.

## Quick Reference

| Step | Script                   | What it does                                |
|------|--------------------------|---------------------------------------------|
| M1   | `crawl.py`               | BFS crawl → raw HTML + metadata per page    |
| M2   | `extract_concepts.py`    | HTML → chunks → LLM concept extraction      |
| M3   | `build_graph.py`         | Concepts + links → networkx knowledge graph |
| M4   | `build_embeddings.py`    | Chunks + concepts → numpy vector index      |
| M5   | `generate_mcp_server.py` | Graph + embeddings → standalone `server.py` |

All scripts require Python 3.10+ and auto-install their own dependencies on first run.

---

## Step 0: Clarify Requirements

Before running anything, ask the user:
- **URL**: Which site to crawl (required — starting page)
- **Depth**: How many link-hops to follow (default 3; suggest 2 for large sites)
- **Model**: Which Claude model for concept extraction — `haiku` (fast/cheap) or `sonnet` (higher quality). Default: `haiku`

Set the output slug from the URL: `https://strudel.cc` → `strudel-cc-mcp`.

---

## Step 1: Crawl (M1)

Provide this command for the user to run locally:

```bash
python scripts/crawl.py \
  --url <URL> \
  --max-depth <DEPTH> \
  --output ./output
```

**What to expect:**
- Creates `output/<slug>/raw_content/*.json` (one per page)
- Creates `output/<slug>/crawl.json` (state tracking)
- Prints a summary: pages crawled, JS fallbacks used, failures

**Common issues:**
- JS-heavy single-page apps → many Playwright fallbacks (normal, just slower)
- Rate limiting → add `--rate-limit 1.5` to slow down
- First run needs: `pip install playwright && playwright install chromium`

---

## Step 2: Extract Concepts (M2)

The user must set `ANTHROPIC_API_KEY` first. Provide this command:

```bash
ANTHROPIC_API_KEY=sk-ant-... python scripts/extract_concepts.py \
  --input ./output/<slug>-mcp \
  --model haiku
```

**Dry-run first (no API cost):**
```bash
python scripts/extract_concepts.py --input ./output/<slug>-mcp --dry-run
```
This validates chunking quality before spending API budget. Show them chunk counts and section names from dry-run output.

**What to expect:**
- Processes ~2–5 pages/minute on haiku
- Creates `output/<slug>-mcp/extracted/*.json` (one per page)
- Each file contains chunks with: concepts, tags, code examples, prerequisites, relationships
- Skips already-extracted pages (safe to re-run after interruption)

**Common issues:**
- Pages showing `no_chunks` → likely JS-rendered content not captured; acceptable for a minority of pages
- API rate limiting → script retries automatically with exponential backoff
- `--max-pages 10` flag to test on a small sample first

**Re-running after a partial run:**
```bash
python scripts/extract_concepts.py --input ./output/<slug>-mcp --model haiku
# (automatically skips already-extracted pages)
```

**Force re-extraction of everything:**
```bash
python scripts/extract_concepts.py --input ./output/<slug>-mcp --force
```

---

## Step 3: Build Graph (M3)

```bash
python scripts/build_graph.py --input ./output/<slug>-mcp
```

**What to expect:**
- Reads all non-dry-run `extracted/*.json` files
- Deduplicates concept names (case-insensitive, strips trailing `()`)
- Creates `output/<slug>-mcp/graph.json`
- Prints node/edge counts by type

**Healthy output looks like:**
```
Pages:     46
Chunks:    357
Concepts:  200+
Total edges: 1000+
  MENTIONS       600+
  REQUIRES       100+
  HAS_CHUNK      357
  LINKS_TO       80+
  RELATED        40+
```

If concepts = 0 and "Skipped N dry-run files" appears, M2 hasn't been run with a real API key yet.

---

## Step 4: Build Embeddings (M4)

```bash
python scripts/build_embeddings.py --input ./output/<slug>-mcp
```

**First run downloads `all-MiniLM-L6-v2` (~80MB, cached after that).**

Add `--smoke-test` to query both collections immediately after building:
```bash
python scripts/build_embeddings.py --input ./output/<slug>-mcp --smoke-test
```

**What to expect:**
- Creates `output/<slug>-mcp/embeddings/` with 5 numpy files (no database needed)
- Two indexes: `chunks` (semantic search) and `concepts` (concept lookup)

---

## Step 5: Generate MCP Server (M5)

```bash
python scripts/generate_mcp_server.py --input ./output/<slug>-mcp
```

**Outputs:**
- `output/<slug>-mcp/server.py` — the runnable MCP server
- `output/<slug>-mcp/mcp_config.json` — Claude Desktop config snippet

**Install into Claude Desktop:**
1. Open `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Merge the contents of `mcp_config.json` into the `"mcpServers"` key
3. Restart Claude Desktop
4. The server name (e.g., `strudel-cc`) appears in Claude's available tools

**Test the server standalone:**
```bash
python output/<slug>-mcp/server.py
# Should print "Loading ... knowledge graph... Ready: N nodes, M edges"
```

---

## The 8 MCP Tools

Once installed, Claude can use these tools against the knowledge base:

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

## Complete Pipeline Command Sequence

For a fresh install, provide the user with all commands in order:

```bash
# 0. Install system deps (once)
pip install requests beautifulsoup4 lxml playwright anthropic \
    networkx numpy sentence-transformers mcp
playwright install chromium

# 1. Crawl
python scripts/crawl.py --url <URL> --max-depth 3 --output ./output

# 2. Extract concepts (dry-run first)
python scripts/extract_concepts.py --input ./output/<slug>-mcp --dry-run
# Then real run:
ANTHROPIC_API_KEY=sk-ant-... python scripts/extract_concepts.py \
  --input ./output/<slug>-mcp --model haiku

# 3. Build graph
python scripts/build_graph.py --input ./output/<slug>-mcp

# 4. Build embeddings
python scripts/build_embeddings.py --input ./output/<slug>-mcp --smoke-test

# 5. Generate server
python scripts/generate_mcp_server.py --input ./output/<slug>-mcp

# 6. Test server
python output/<slug>-mcp/server.py
```

---

## Output Directory Layout

```
output/<slug>-mcp/
├── crawl.json              State tracking (incremental re-runs)
├── raw_content/            One JSON per crawled page (HTML + links)
├── extracted/              One JSON per page (chunks + LLM concepts)
├── graph.json              networkx knowledge graph
├── embeddings/             numpy indexes (chunks.npy, concepts.npy + JSON)
├── server.py               The runnable MCP server ← share this
└── mcp_config.json         Claude Desktop config snippet ← install this
```

The entire `output/<slug>-mcp/` folder is the deliverable. The user can move it anywhere
as long as `server.py`, `graph.json`, and `embeddings/` stay together.

---

## Troubleshooting

**"No module named X"** → The script auto-installs deps, but if it fails:
```bash
pip install <package> --break-system-packages
```

**Crawl gets 0 pages** → Check robots.txt and try `--force` to bypass the crawl cache.

**extract_concepts produces tiny concepts count** → The page content may be JS-only.
Check `fetched_with` field in `raw_content/*.json` — pages fetched via `requests` with
very little text should have been picked up by Playwright. Re-crawl with `--force`.

**Server fails to start** → Run `python output/<slug>-mcp/server.py` directly and check
stderr for import errors. Most common cause: `mcp` package not installed.

**Claude Desktop doesn't show the server** → Verify the path in `mcp_config.json` is
absolute and the file exists. Restart Claude Desktop after any config change.

---

## Deferred Features

See `TODO.md` for planned improvements including:
- YouTube transcript fetching
- Neo4j export for large graphs
- OpenAI/Voyage embedding API support
- Scheduled re-crawls
- Graph visualization
