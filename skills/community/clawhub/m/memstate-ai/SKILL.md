---
name: memstate-ai
description: >
  Versioned, structured memory for AI agents. 
  Every fact is tracked, every change is logged, and your agent 
  always gets the current answer — not a pile of outdated context. Requires MEMSTATE_API_KEY.
metadata: {"openclaw": {"requires": {"bins": ["python3"], "env": ["MEMSTATE_API_KEY"]}, "primaryEnv": "MEMSTATE_API_KEY", "homepage": "https://memstate.ai"}}
---

# Memstate AI Memory Management

This skill provides a full-featured alternative to the Memstate MCP plugin by
interacting directly with the Memstate REST API. It gives agents a persistent,
structured, and versioned knowledge base with conflict detection, semantic
search, and full version history.

## Core Concepts

| Concept | Description |
|---|---|
| **Project** | Top-level container for memories (e.g., `myapp`, `backend-api`). Auto-created on first write. |
| **Keypath** | Dot-separated hierarchical path (e.g., `auth.method`). Auto-prefixed with `project.{project_id}.` |
| **Memory** | A single fact or markdown summary stored at a keypath with full version history. |
| **Versioning** | Writing to an existing keypath supersedes the old value. History is always preserved. |
| **Tombstone** | Deleting a keypath creates a tombstone version — history is never destroyed. |

## Input Formats

### Direct keypath = value assignment
```
config.port = 8080
database.engine = PostgreSQL 16
auth.method = JWT with httpOnly cookies
status.deployment = production
```

### Markdown (preferred for task summaries)
```markdown
## Architecture Decision
- Database: PostgreSQL 16
- Auth: JWT with httpOnly cookies
- Deploy: Docker on AWS ECS
- API style: REST with OpenAPI 3.1
```

## Workflows

### Before Starting a Task (Recall)

Always check what already exists before making decisions or modifying code.

```bash
# 1. Semantic search — find relevant facts by meaning
python3 {baseDir}/scripts/memstate_search.py \
  --project "myapp" \
  --query "how is authentication configured"

# 2. Browse the full project tree (all domains and keypaths)
python3 {baseDir}/scripts/memstate_get.py \
  --project "myapp"

# 3. Get a specific subtree with full content
python3 {baseDir}/scripts/memstate_get.py \
  --project "myapp" --keypath "database" --include-content
```

### After Completing a Task (Remember)

```bash
# Store a single fact (config, status, version numbers)
python3 {baseDir}/scripts/memstate_set.py \
  --project "myapp" \
  --keypath "config.port" \
  --value "8080" \
  --category "fact"

# Store a rich markdown summary (AI extracts keypaths automatically)
python3 {baseDir}/scripts/memstate_remember.py \
  --project "myapp" \
  --content "## Auth Migration\n- Changed from JWT to server-side sessions\n- Added MFA via TOTP\n- Files: auth.go, middleware.go" \
  --source "agent"
```

### Manage History and Cleanup

```bash
# View how a fact changed over time
python3 {baseDir}/scripts/memstate_history.py \
  --project "myapp" --keypath "database.engine"

# Soft-delete an outdated keypath (history preserved)
python3 {baseDir}/scripts/memstate_delete.py \
  --project "myapp" --keypath "config.old_setting"

# Soft-delete an entire project
python3 {baseDir}/scripts/memstate_delete_project.py \
  --project "myapp"
```

## Script Reference

### `memstate_set.py` — Set a single keypath value

Stores one fact at a specific keypath. Synchronous, immediately available.
Supersedes the previous value if the keypath already exists.

```bash
python3 {baseDir}/scripts/memstate_set.py \
  --project PROJECT_ID \
  --keypath KEYPATH \
  --value VALUE \
  [--category CATEGORY]  # decision | fact | config | requirement | note | code | learning
  [--topics TAG1,TAG2]
```

**Response keys:** `action` (created|superseded), `memory_id`, `version`

---

### `memstate_remember.py` — Ingest markdown or text

Preferred for task summaries, meeting notes, or any multi-fact content.
The AI engine automatically extracts structured keypaths from your text.
Processing is async (~15–18 s); the script polls until completion.

```bash
python3 {baseDir}/scripts/memstate_remember.py \
  --project PROJECT_ID \
  --content "MARKDOWN_OR_TEXT" \
  [--source agent|readme|docs|meeting|code] \
  [--context "optional hint for extraction"]
```

**Response keys:** `status` (completed|failed), `job_id`, `memories_created`

---

### `memstate_get.py` — Browse and retrieve memories

```bash
# List all projects
python3 {baseDir}/scripts/memstate_get.py

# Full project tree (returns domains and keypaths)
python3 {baseDir}/scripts/memstate_get.py --project PROJECT_ID

# Subtree at a keypath
python3 {baseDir}/scripts/memstate_get.py \
  --project PROJECT_ID --keypath KEYPATH [--include-content] [--at-revision N]

# Single memory by UUID
python3 {baseDir}/scripts/memstate_get.py --memory-id UUID
```

**Response keys (project tree):** `domains`, `total_memories`
**Response keys (subtree):** `memories`, `total_count`
**Response keys (list projects):** `projects`

---

### `memstate_search.py` — Semantic search

Find memories by meaning when you don't know the exact keypath.

```bash
python3 {baseDir}/scripts/memstate_search.py \
  --query "NATURAL_LANGUAGE_QUERY" \
  [--project PROJECT_ID] \
  [--limit N]  # default 20, max 100
```

**Response keys:** `results` (array), `total_found`, `query`

---

### `memstate_history.py` — Version history

View all versions of a keypath or memory chain.

```bash
python3 {baseDir}/scripts/memstate_history.py \
  --project PROJECT_ID --keypath KEYPATH
# or
python3 {baseDir}/scripts/memstate_history.py \
  --memory-id UUID
```

**Response keys:** `versions` (array), `total_versions`

---

### `memstate_delete.py` — Soft-delete a keypath

Creates a tombstone version. History is always preserved.

```bash
python3 {baseDir}/scripts/memstate_delete.py \
  --project PROJECT_ID \
  --keypath KEYPATH \
  [--recursive]  # delete entire subtree
```

**Response keys:** `deleted_count`, `deleted_keypaths`

---

### `memstate_delete_project.py` — Soft-delete a project

```bash
python3 {baseDir}/scripts/memstate_delete_project.py \
  --project PROJECT_ID
```

**Response keys:** `project_id`, `deleted_count`

---

## Best Practices

1. **One keypath = one fact.** Use `api.style` not `api`. Be specific.
2. **Update, don't duplicate.** When a fact changes, call `memstate_set.py` with the SAME keypath and the NEW value. Do not create a new keypath.
3. **Trust `is_latest: true`.** Search results may show multiple versions. Only trust results where `is_latest` is `true`.
4. **Use Markdown for summaries.** `memstate_remember.py` excels at parsing Markdown lists, headings, and key-value pairs into structured keypaths.
5. **Search before browsing.** `memstate_search.py` is faster than browsing the tree when you know what you're looking for.
6. **Use categories.** Setting `--category decision` on architecture choices makes them easier to filter later.

## Authentication

Set the `MEMSTATE_API_KEY` environment variable before running any script:

```bash
export MEMSTATE_API_KEY="your_api_key_here"
```

Get your API key at [https://memstate.ai/dashboard](https://memstate.ai/dashboard).

## Resources

- **Documentation:** [https://memstate.ai/docs](https://memstate.ai/docs)
- **MCP Plugin (alternative):** [https://github.com/memstate-ai/memstate-mcp](https://github.com/memstate-ai/memstate-mcp)
- **Benchmark:** [https://github.com/memstate-ai/memstate-benchmark](https://github.com/memstate-ai/memstate-benchmark)
