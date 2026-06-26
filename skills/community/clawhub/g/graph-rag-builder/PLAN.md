# GraphRAG Builder Skill — Project Plan

## Core Idea

Build a **Claude Cowork Skill** that takes a website (documentation, tutorial site, or course) and:

1. Crawls and extracts all learning content (pages, YouTube transcripts, PDFs)
2. Organizes that content into a **knowledge graph** — linked by hyperlink structure and LLM-generated concept relationships
3. Embeds the content for semantic search
4. Outputs a fully runnable **MCP (Model Context Protocol) server** that lets Claude answer expert questions about the topic

The first target: `https://strudel.cc/workshop/getting-started/` — a live-coding music library.

---

## CLI Interface

The skill is driven by a single orchestrator script. All options have sensible defaults.

```bash
python scripts/build.py \
  --url https://strudel.cc/workshop/getting-started/ \
  --max-depth 3 \
  --model haiku \
  --output ./output
```

| Flag | Default | Description |
|------|---------|-------------|
| `--url` | *(required)* | Seed URL to start crawling from |
| `--max-depth` | `3` | How many link-hops from the seed URL |
| `--model` | `haiku` | LLM model for concept extraction. Options: `haiku`, `sonnet` |
| `--output` | `./output` | Root output directory |
| `--incremental` | `true` | Skip URLs whose content hash hasn't changed |
| `--force` | `false` | Ignore checksums; re-crawl and re-process everything |

The `--model` flag controls concept extraction (Phase 3). `haiku` is fast and cheap for most sites; use `sonnet` for better relationship quality on complex technical content.

---

## Architecture Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | **requests-html first, Playwright fallback** | If the returned page is empty or contains "JavaScript is required", automatically re-fetch with Playwright/Chromium |
| 2 | **Default model: haiku; `--model sonnet` option** | Cost-effective default; sonnet available for precision work |
| 3 | **sentence-transformers (local)** | No API key required; `all-MiniLM-L6-v2` is fast and good quality. See TODO.md for future embedding API support |
| 4 | **Neo4j deferred** | Sufficient for <10,000 nodes with networkx + JSON. See TODO.md |
| 5 | **Incremental updates via SQLite + SHA256** | Per-URL content hashing enables efficient re-runs without full re-crawl |
| 6 | **`/output` folder, gitignored** | Full MCP package (server.py + graph.json + embeddings) lives here |

---

## Feasibility Assessment

**Yes, this is feasible.** All core pieces have well-maintained Python libraries:

| Task | Tool |
|------|------|
| Web crawling (static) | `requests-html` |
| Web crawling (JS-heavy) | `playwright` (auto-fallback) |
| YouTube transcripts | `youtube-transcript-api` |
| LLM concept extraction | Claude API (haiku/sonnet) |
| Incremental tracking | `sqlite3` (stdlib) |
| Graph construction | `networkx` → JSON |
| Semantic search index | `chromadb` + `sentence-transformers` |
| MCP server | Python `mcp` SDK (FastMCP) |

---

## Repository Structure

```
GraphRAGBuilderSkill/
├── SKILL.md                       ← Cowork skill instructions
├── PLAN.md                        ← This file
├── TODO.md                        ← Deferred features
├── .gitignore                     ← Includes /output/
├── scripts/
│   ├── build.py                   ← CLI orchestrator (main entry point)
│   ├── crawl.py                   ← Web crawler + JS fallback
│   ├── extract_youtube.py         ← YouTube transcript fetcher
│   ├── extract_concepts.py        ← LLM concept/tag extractor
│   ├── build_graph.py             ← Graph assembler
│   ├── build_embeddings.py        ← Chunk + embed content
│   └── generate_mcp_server.py     ← Output MCP server generator
├── references/
│   ├── graph_schema.md            ← Node/edge type documentation
│   └── mcp_server_template.py     ← Template used by generate_mcp_server.py
├── evals/
│   └── evals.json                 ← Test cases
└── output/                        ← Gitignored; generated MCP packages live here
    └── strudel-mcp/
        ├── server.py
        ├── graph.json
        ├── crawl.db
        ├── embeddings/
        ├── requirements.txt
        └── claude_config.json
```

`.gitignore` must include:
```
/output/
__pycache__/
*.pyc
.playwright/
```

---

## Phase-by-Phase Plan

### Phase 0 — Environment Setup

Install Python dependencies at runtime via the orchestrator:

```
requests-html
playwright (+ chromium via playwright install chromium)
youtube-transcript-api
pdfminer.six
networkx
chromadb
sentence-transformers
mcp
anthropic
```

The orchestrator checks for these at startup and installs any missing ones.

---

### Phase 1 — Content Discovery & Crawling

**Input**: `--url`, `--max-depth`

**Process**:
1. Attempt to fetch seed URL with `requests-html`
2. **JS detection**: If response body is empty or contains "JavaScript is required" / "enable JavaScript" → re-fetch with Playwright
3. Extract all internal links (same domain only) and enqueue them
4. Detect YouTube video embeds/links → enqueue separately
5. Detect PDF links → enqueue separately
6. BFS crawl to depth N with 0.5s polite delay between requests
7. Respect `robots.txt` (skip disallowed URLs with a warning)
8. Deduplicate URLs

**Incremental tracking** (see Phase 1.5): Before fetching, check SQLite for a stored hash. After fetching, compare. Skip processing if hash matches.

**Output**: `output/<slug>/raw_content/<url_hash>.json`
```json
{
  "url": "https://strudel.cc/workshop/getting-started/",
  "type": "html",
  "title": "Getting Started",
  "raw_html": "...",
  "outgoing_links": ["..."],
  "youtube_ids": ["abc123"],
  "fetched_with": "requests-html"
}
```

---

### Phase 1.5 — Incremental State Tracking (SQLite)

All state lives in `output/<slug>/crawl.db`. Schema:

```sql
CREATE TABLE pages (
  url           TEXT PRIMARY KEY,
  content_hash  TEXT,          -- SHA256 of raw content
  last_crawled  TIMESTAMP,
  title         TEXT,
  type          TEXT,          -- 'html' | 'youtube' | 'pdf'
  status        TEXT           -- 'crawled' | 'extracted' | 'embedded' | 'graphed' | 'complete'
);

CREATE TABLE concepts (
  id            TEXT PRIMARY KEY,
  name          TEXT,
  definition    TEXT,
  tags          TEXT,          -- JSON array
  last_updated  TIMESTAMP
);
```

**Re-run logic**:
- `--incremental` (default): Fetch each URL, compute SHA256 of the response body. If hash matches `crawl.db`, mark as skipped. If hash differs or URL is new, set status back to `'crawled'` and re-run downstream phases for that URL only.
- `--force`: Ignore all stored hashes; re-process everything from scratch.

**Status progression**: `crawled` → `extracted` → `embedded` → `graphed` → `complete`

Each phase only processes pages at or below the required status, making partial re-runs safe.

---

### Phase 2 — Content Extraction & Cleaning

**Process**:
1. For HTML pages: strip nav/footer boilerplate, extract main content as clean Markdown using `html2text`
2. For YouTube IDs: fetch transcript via `youtube-transcript-api`, merge segments into timestamped text blocks
3. For PDFs: extract text with `pdfminer.six`
4. **Chunk** long content into 300–500 word segments with 50-word overlap, preserving section headings in each chunk's metadata

**Output**: `output/<slug>/extracted/<url_hash>.json`
```json
{
  "url": "...",
  "title": "...",
  "type": "html",
  "chunks": [
    {
      "id": "abc123_chunk_001",
      "text": "...",
      "section": "Installation",
      "word_count": 342
    }
  ]
}
```

Pages update to status `extracted` in SQLite.

---

### Phase 3 — LLM Concept Extraction

**This is the core intelligence step.** For each chunk, call Claude (`--model` flag, default `haiku`) with a structured prompt to extract:

- **Concepts**: Named topics or skills taught in this chunk
- **Tags**: Broader category labels
- **Code examples**: Any code blocks with a 1-sentence description
- **Prerequisites**: Concepts that should be understood first
- **Relationships**: How concepts in this chunk relate to others

**Prompt pattern** (sent per chunk):
```
You are extracting structured knowledge from a documentation chunk.

Chunk title: {section}
Source URL: {url}
Content: {text}

Extract in JSON:
{
  "concepts": [{"name": "...", "definition": "..."}],
  "tags": ["..."],
  "code_examples": [{"code": "...", "description": "..."}],
  "prerequisites": ["..."],
  "relationships": [{"from": "...", "to": "...", "type": "requires|related_to|explains"}]
}
```

**Cost guidance**: For a 50-page site with ~3 chunks/page ≈ 150 API calls. With `haiku`, this is typically under $0.10. With `sonnet`, ~$1–2.

**Output**: `output/<slug>/concepts/<url_hash>.json` (structured extraction per chunk)

Pages update to status `extracted` (concepts done) in SQLite.

---

### Phase 4 — Graph Construction

**Graph Schema**:

*Node types:*

| Type | Fields | Example |
|------|--------|---------|
| `Page` | url, title, type, summary | `strudel.cc/workshop/intro` |
| `Concept` | name, definition, tags | `"mini notation"` |
| `Example` | code, description, language | `note('c3 e3')` |
| `Video` | youtube_id, title | `abc123` |

*Edge types:*

| Type | From → To | Meaning |
|------|-----------|---------|
| `links_to` | Page → Page | Hyperlink exists |
| `teaches` | Page → Concept | Page explains this concept |
| `requires` | Concept → Concept | Prerequisite relationship |
| `related_to` | Concept → Concept | Thematically related |
| `exemplifies` | Example → Concept | Code demonstrates concept |
| `appears_in` | Example → Page | Code found on this page |

**Implementation**: Built with `networkx`, serialized to `output/<slug>/graph.json`.

The graph JSON uses node-link format:
```json
{
  "directed": true,
  "nodes": [
    {"id": "concept:mini-notation", "type": "Concept", "name": "mini notation", "tags": ["syntax", "beginner"]}
  ],
  "links": [
    {"source": "page:workshop/intro", "target": "concept:mini-notation", "type": "teaches"}
  ]
}
```

Pages update to status `graphed` in SQLite.

---

### Phase 5 — Semantic Embedding Index

**Process**:
1. Collect all cleaned chunks from Phase 2
2. Generate embeddings using `sentence-transformers` with model `all-MiniLM-L6-v2`
3. Store in a persistent `chromadb` collection at `output/<slug>/embeddings/`
4. Each embedding is stored with metadata: `{url, title, section, chunk_id}`

On incremental re-run: only re-embed chunks from pages whose hash changed.

Pages update to status `embedded` in SQLite.

---

### Phase 6 — MCP Server Generation

The skill generates a self-contained Python MCP server. The server loads `graph.json` and the ChromaDB index at startup and exposes these tools to Claude:

| Tool | Signature | Description |
|------|-----------|-------------|
| `search` | `(query: str, top_k: int = 5)` | Semantic search across all content |
| `get_page` | `(url: str)` | Full content + metadata for a page |
| `list_concepts` | `()` | All concepts with brief definitions |
| `get_concept` | `(name: str)` | Concept detail + related pages + examples |
| `get_related` | `(concept: str, relation_type: str = None)` | Graph neighbors |
| `get_learning_path` | `(start: str, end: str)` | Shortest concept path (networkx BFS) |
| `get_examples` | `(concept: str)` | All code examples for a concept |
| `get_prerequisites` | `(concept: str)` | Ordered prerequisite chain |

**Output package** (`output/<slug>/`):
```
output/strudel-mcp/
├── server.py           ← MCP server (run with: python server.py)
├── graph.json          ← Serialized knowledge graph
├── embeddings/         ← ChromaDB vector store directory
├── crawl.db            ← Crawl state + incremental tracking
├── requirements.txt    ← pip install -r requirements.txt
└── claude_config.json  ← Paste this into claude_desktop_config.json
```

**`claude_config.json`** contains the ready-to-paste snippet:
```json
{
  "mcpServers": {
    "strudel-docs": {
      "command": "python",
      "args": ["/absolute/path/to/output/strudel-mcp/server.py"]
    }
  }
}
```

The entire `output/<slug>/` directory is the deployable package. All paths inside `server.py` are relative so the package is portable.

All pages update to status `complete` in SQLite.

---

### Phase 7 — Skill Packaging & Testing

1. Write `SKILL.md` with triggering instructions and step-by-step workflow
2. Create eval cases in `evals/evals.json`:
   - **Eval 1**: Strudel (`strudel.cc`) — JS-heavy, YouTube videos, creative coding docs
   - **Eval 2**: A static docs site (e.g., FastAPI docs) — simpler crawl, API reference
   - **Eval 3**: A single-page tutorial — tests shallow crawl and minimal graph
3. Run evals using the skill-creator workflow; iterate on SKILL.md
4. Package as `.skill` file

---

## Recommended Build Order (Milestones)

Each milestone is independently testable:

**M1 — Crawler**: `crawl.py` works on Strudel. Produces raw JSON files. SQLite tracking working. JS fallback triggered correctly.

**M2 — Extraction + Concepts**: `extract_concepts.py` produces structured JSON from Strudel pages. Chunks look right. LLM output is parseable.

**M3 — Graph**: `build_graph.py` produces a valid `graph.json` with reasonable nodes and edges. Can inspect it manually.

**M4 — Search**: `build_embeddings.py` works. Can run semantic queries against the ChromaDB from the command line and get relevant chunks back.

**M5 — MCP Server**: `generate_mcp_server.py` produces a `server.py` that starts cleanly. All 8 tools respond correctly. Claude Desktop can connect and answer Strudel questions.

**M6 — Skill + Evals**: Wrap in `SKILL.md`. Run evals. Iterate. Package.
