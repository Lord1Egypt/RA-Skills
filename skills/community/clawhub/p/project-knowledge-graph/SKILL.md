---
name: project-knowledge-graph
description: >-
  Cross-project knowledge graph powered by local FalkorDB. Indexes all project
  artifacts (recaps, plans, project memory files, architecture docs, skills) across
  multiple projects and lets you query by concept. "What did we learn about
  FalkorDB replication?" returns the matching skill, relevant recaps, and
  architecture context — regardless of which project they came from.
version: 3.0.0
author: Alejandro Del Villar
metadata:
  hermes:
    homepage: https://github.com/adelvillar1
    tags: [knowledge-graph, cross-project, falkordb, search, project-memory]
    related_skills: [project-warmup, pipeline-script-verification, session-wrapup, project-wrapup, write-session-recap, draft-feature-plan]
security:
  scope:
    persistence:
      - "Reads project memory files (e.g. .md), docs/recaps/*.md, docs/plans/*.md, docs/architecture/*.md, docs/features/*.md, TECHNICAL-DOCUMENTATION.md, FUNCTIONAL-SPECIFICATIONS.md across all configured project directories"
      - "Reads all SKILL.md files under ~/.hermes/skills/"
      - "Writes to local FalkorDB Docker container (port 16379) — MERGE operations, no deletions"
      - "Does NOT modify any project files. Read-only on your source documents."
  safety:
    - "Indexing is content-hash-gated: unchanged documents skip MERGE"
    - "Glob patterns explicitly exclude node_modules, .next, .git, venv"
    - "Full purge: docker stop knowledge-graph && docker rm knowledge-graph && docker volume rm knowledge-graph-data"
    - "Port bound to 127.0.0.1 (localhost only) — not reachable from other machines"
    - "Non-localhost guard: script prompts for confirmation before sending data to a remote FalkorDB host via KNOWLEDGE_FALKORDB_HOST env var"
    - "Docker image: falkordb/falkordb:latest (digest-pinning instructions included in setup)"
    - "Python package pinned: falkordb==1.6.1"
triggers:
  - "knowledge.*graph"
  - "cross.project.*knowledge"
  - "what.*did.*we.*learn"
  - "find.*pattern.*across"
  - "search.*across.*project"
  - "project.*knowledge.*query"
  - "how.*did.*we.*in.*project"
---

# Project Knowledge Graph

> A local FalkorDB-backed semantic index over all project artifacts. Query by
> concept across 8 projects: "show me everything about FalkorDB replication"
> returns the matching skill, the recaps that mention it, and the architecture
> docs — ranked by TF-IDF relevance with Cypher CONTAINS primary filter.

## Architecture

```
knowledge index
    │
    ▼
Scans project directories for .md artifacts
    ├── docs/recaps/, docs/daily-recaps/
    ├── docs/plans/
    ├── project memory file
    ├── docs/architecture/, docs/features/, docs/operations/, docs/pipeline/
    ├── TECHNICAL-DOCUMENTATION.md, FUNCTIONAL-SPECIFICATIONS.md
    └── **/SKILL.md (Hermes skills)
    │
    ▼
Chunks by heading-2 boundaries + paragraphs (max 2000 chars)
    │
    ▼
MERGE into FalkorDB graph as :Chunk nodes
    │
    ▼
knowledge query "concept"
    │
    ▼
Stage 1: Cypher CONTAINS (fast primary filter)
Stage 2: TF-IDF re-ranking
    │
    ▼
Ranked results with project, file, heading, snippet
```

## Setup (one-time)

### 1. Start the FalkorDB container

```bash
docker run -d \
  --restart=unless-stopped \
  -p 127.0.0.1:16379:6379 \
  -v knowledge-graph-data:/data \
  --name knowledge-graph \
  falkordb/falkordb:latest
```

> **🔒 Security:** The port is bound to `127.0.0.1` (localhost only) — FalkorDB is not reachable from other machines on your network. No authentication is configured because the service is only accessible to local processes.
>
> **📦 Docker image note:** `falkordb/falkordb:latest` is a mutable tag. To pin by digest (recommended for production), replace the tag with the current SHA256 after pulling:
> ```bash
> docker pull falkordb/falkordb:latest
> DIGEST=$(docker inspect --format='{{index .RepoDigests 0}}' falkordb/falkordb:latest)
> echo "Replace :latest with @${DIGEST#*@}"
> ```
> Then use `falkordb/falkordb@sha256:...` in the `docker run` command. Check for updates intentionally rather than relying on automatic pulls.

Auto-starts on Docker daemon start via `--restart=unless-stopped`. Data persists in the Docker volume.

> **ℹ️ Persistence note:** The container uses `--restart=unless-stopped` to survive Docker restarts but won't auto-restart after a manual `docker stop`. To disable persistence entirely, omit `--restart` and start the container manually when needed.

### 2. Install the Python dependency

```bash
pip install falkordb==1.6.1
```

### 3. Verify

```bash
python3 ~/.hermes/scripts/project-knowledge-index.py doctor
```

Should show all 8 project roots with document counts and a healthy FalkorDB connection.

## Usage

### Index all projects

```bash
# First index (~60s) — incremental thereafter (<1s)
python3 ~/.hermes/scripts/project-knowledge-index.py index

# Preview without writing
python3 ~/.hermes/scripts/project-knowledge-index.py index --dry-run
```

> **⚠️ Before first real run:** Use `--dry-run` to preview which files would be indexed. This is especially important when configuring `PROJECT_ROOTS` for the first time — it shows you exactly which files the scraper will read before any data is written to FalkorDB.
>
> ```bash
> python3 ~/.hermes/scripts/project-knowledge-index.py index --dry-run
> ```

### Query by concept

```bash
# Basic search
python3 ~/.hermes/scripts/project-knowledge-index.py query "FalkorDB replication"

# Filter by project
python3 ~/.hermes/scripts/project-knowledge-index.py query "batch writes" --project CI

# Filter by document type (recap, plan, skill, claude, architecture)
python3 ~/.hermes/scripts/project-knowledge-index.py query "soft delete" --type skill
```

### Stats and health

```bash
python3 ~/.hermes/scripts/project-knowledge-index.py stats
python3 ~/.hermes/scripts/project-knowledge-index.py doctor
```

## Query Algorithm

Two-stage ranking:

1. **Cypher CONTAINS** — finds all chunks whose text contains the search terms. Fast, exact-match primary filter. Supports filtering by `--project` and `--type` at this stage.
2. **TF-IDF re-ranking** — computes term frequency × inverse document frequency for each candidate against the query tokens. Scores are relative within the result set (best match = highest score).

This gives substantially better results than pure CONTAINS without needing LLM embeddings or API calls.

## How to use this in a session

When working on a problem you've seen before:

```bash
# How did we handle PostgreSQL migrations?
python3 ~/.hermes/scripts/project-knowledge-index.py query "PostgreSQL migration"

# What patterns exist for batch operations across projects?
python3 ~/.hermes/scripts/project-knowledge-index.py query "batch" --type skill

# Did we ever document Ollama rate limiting?
python3 ~/.hermes/scripts/project-knowledge-index.py query "Ollama rate limit"

# What did we learn about soft deletes?
python3 ~/.hermes/scripts/project-knowledge-index.py query "soft delete" --project MyApp
```

## What's indexed

| Project | Typical docs | Sample content |
|---------|-------------|----------------|
| **Any project with a project memory file** | Recaps, plans, memory file | Session recaps, implementation plans, methodology rules |
| **Any project with docs/** | Architecture, features, operations, pipeline | Topical docs about every component |
| **Any project with TECHNICAL/FUNCTIONAL specs** | Full technical specs | Architecture decisions, schema docs |
| **Hermes skills** (`~/.hermes/skills/`) | All SKILL.md files | Every installed skill — procedures, tips, workflows |
| **Hermes Agent repo** | Built-in skills, docs, plans | Stock skills, plugin docs

## Why FalkorDB over SQLite

| Dimension | SQLite (hash) | FalkorDB (graph — chosen) |
|-----------|---------------|---------------------------|
| Primary filter | Simhash distance (fuzzy) | Cypher CONTAINS (exact match) |
| Cross-project query | Manual JOINs | `MATCH (c:Chunk {project:'CI'}) RETURN c` |
| Data model flexibility | Fixed SQL schema | Add node types, edges on the fly |
| Infrastructure | File on disk | Single Docker container (localhost-only, 200MB idle) |
| Query speed | Sub-second | Sub-second |

The Docker container is a one-time setup. After that, it starts on boot automatically (`--restart=always`) and uses <200MB RAM when idle.

## Configuring Your Projects

Edit `PROJECT_ROOTS` in `~/.hermes/scripts/project-knowledge-index.py` to point at your own project directories:

```python
PROJECT_ROOTS = {
    "MyApp": os.path.expanduser("~/Projects/myapp"),
    "Website": os.path.expanduser("~/Desktop/website"),
    "Skills": os.path.expanduser("~/.hermes/skills"),
    "Hermes": os.path.expanduser("~/.hermes/hermes-agent"),
}
```

The `Custom-Skills` and `Hermes-Agent` entries are optional but recommended — they index every Hermes skill you have (both installed and stock) so you can search across all known patterns.

**Pro tip:** Add your projects in priority order. The `find_documents()` function respects your glob patterns — it specifically scopes to `docs/recaps/*.md`, `docs/plans/*.md`, project memory files, `docs/architecture/*.md`, `docs/features/*.md`, `SKILL.md`, etc. It does NOT crawl `node_modules/`.

## Pitfalls

### 1. CONTAINS is case-sensitive

"FalkorDB" matches, "falkordb" does not. Use the casing you expect in documents. Document text preserves original casing from markdown files.

### 2. Short queries produce noisy results

"DB" or "pipeline" match too broadly. Mitigation: add `--project` or `--type` filters, or use more specific terms (e.g., "FalkorDB replication" not just "FalkorDB").

### 3. TF-IDF scores are relative within result set

A score of 0.06 on a 10-result query doesn't mean "6% match" — it means "the top result by far." Use scores to rank within a single query, not to compare across queries.

### 4. FalkorDB container must be running

```bash
docker start knowledge-graph  # if stopped
```

### 5. Massive node_modules directories hang rglob-based scans

The initial version used `Path.rglob("*.md")` to count files in `doctor`. Projects with large `node_modules` directories (Beacon-v2 had 775+ entries in one subdirectory with symlink loops) caused 30s+ hangs. **Fix:** never `rglob` a project root. Use targeted `root.glob(pattern)` with specific paths like `docs/recaps/*.md`, `docs/plans/*.md`. The `find_documents` function already does this correctly — the original `doctor` function was the only offender.

### 6. First index is slow (~60s)

Subsequent runs are <1s (only new/changed files are re-indexed). The indexer uses content hash + mtime for change detection.

### 6. The skill indexes itself

Since the project-knowledge-graph SKILL.md is in `~/.hermes/skills/`, it gets indexed. Query results may show matches from this skill's documentation — usually harmless.

## Data Retention & Purge

Indexed content persists in the Docker volume until explicitly removed. This means cross-project knowledge is available across sessions without re-indexing, but stale or sensitive content remains searchable until purged.

**Important: the indexer uses MERGE (upsert), not sync.** When a source file is modified, its chunks are re-indexed on the next `knowledge index` run. However, if a file is **deleted** or a chunk is **removed**, the old chunks remain in FalkorDB until the volume is purged. The indexer does not track deletions — it only adds and updates.

If you need to guarantee no stale content remains after removing source files:

```bash
# Full purge and rebuild
docker stop knowledge-graph && docker rm knowledge-graph && docker volume rm knowledge-graph-data
docker run -d --restart=unless-stopped -p 127.0.0.1:16379:6379 -v knowledge-graph-data:/data --name knowledge-graph falkordb/falkordb:latest
python3 ~/.hermes/scripts/project-knowledge-index.py index
```

Or use the `delete` command for targeted removal without stopping the container:

```bash
# Delete all chunks for a specific project
python3 ~/.hermes/scripts/project-knowledge-index.py delete --project CI

# Delete all chunks of a specific type across all projects
python3 ~/.hermes/scripts/project-knowledge-index.py delete --type recap

# Delete all chunks (rebuild from scratch)
python3 ~/.hermes/scripts/project-knowledge-index.py delete --all
python3 ~/.hermes/scripts/project-knowledge-index.py index
```

### Stop the service (keep data)

```bash
docker stop knowledge-graph
```

To re-enable: `docker start knowledge-graph`

### Clear all indexed data (stop + purge)

```bash
docker stop knowledge-graph && docker rm knowledge-graph && docker volume rm knowledge-graph-data
```

After purging, re-run `knowledge index` (first run will be ~60s to rebuild the index).

### Selective re-indexing (update specific projects)

The indexer uses content hashing — unchanged documents are skipped automatically. To force a full re-index of all projects (e.g. after changing `PROJECT_ROOTS`):

```bash
# Option A: Clear and re-index
docker stop knowledge-graph && docker rm knowledge-graph && docker volume rm knowledge-graph-data
docker run -d --restart=unless-stopped -p 127.0.0.1:16379:6379 -v knowledge-graph-data:/data --name knowledge-graph falkordb/falkordb:latest
python3 ~/.hermes/scripts/project-knowledge-index.py index

# Option B: Just re-index (updates changed files, retains unchanged)
python3 ~/.hermes/scripts/project-knowledge-index.py index
```

## CLI Reference

```
usage: knowledge index|query|stats|doctor|delete

Commands:
  index       Scan and index all project documents
              --dry-run  Preview without indexing

  query       Search the knowledge graph by concept
              terms            Search terms (required)
              --project, -p    Filter by project name
              --type, -t       Filter by doc type (recap/plan/skill/claude/architecture)
              --limit, -l      Max results (default: 10)

  stats       Show corpus statistics (chunks per project/type)

  doctor      Check environment and connectivity

  delete      Delete chunks from the graph
              --project, -p    Delete all chunks for a project
              --type, -t       Delete all chunks of a type
              --all            Delete ALL chunks (equivalent to docker volume purge)
```

## Indexed Document Types

| Type | What's included |
|------|----------------|
| `recap` | `docs/recaps/*.md`, `docs/daily-recaps/*.md` |
| `plan` | `docs/plans/*.md` |
| `claude` | Project memory files (e.g. PROJECT.md) |
| `architecture` | `docs/architecture/*.md`, `docs/features/*.md`, `docs/operations/*.md`, `docs/pipeline/*.md`, `TECHNICAL-DOCUMENTATION.md`, `FUNCTIONAL-SPECIFICATIONS.md` |
| `skill` | `**/SKILL.md` anywhere in project or `~/.hermes/skills/` |

## Auto-projection (via session-wrapup)

New knowledge is projected into the graph **automatically** at session end. The `session-wrapup` skill runs `knowledge index` as one of its steps, which picks up:

- **New recaps** — every session recap gets indexed automatically
- **Updated plans** — plan status changes and criteria updates get indexed
- **Modified project memory files** — any "Today's state" updates get indexed
- **New/changed skills** — any skill edited or created gets indexed

Additionally, wrapup queries the graph with key terms from the session's work and surfaces cross-project connections as "Did you know?" findings in the wrap-up report.

No manual steps needed. The knowledge graph stays current as a side effect of the normal session lifecycle.

- [ ] `knowledge doctor` shows all project roots and healthy FalkorDB connection
- [ ] `knowledge index` completes and reports chunk count
- [ ] `knowledge query "some concept"` returns ranked results with project/file/snippet
- [ ] `knowledge query --project CI --type plan` filters correctly
- [ ] Incremental: running `knowledge index` twice skips unchanged files
- [ ] Container auto-starts on Docker daemon restart
- [ ] Cross-project: query returns results from multiple projects
