---
name: memory-qmd
description: "QMD memory backend — BM25 + vector search over indexed code and docs via the qmd CLI."
license: MIT
metadata:
  authors: "OpenClaw Memory Stack"
  version: "0.1.0"
---

# QMD — SKILL.md

## Overview

QMD is a BM25 + vector search engine for code and documentation. It indexes files into named collections using glob patterns and stores them in a local SQLite database with FTS5 full-text search. QMD supports three search modes: BM25 keyword search for exact symbol/name lookups, vector semantic search for concept-based queries, and hybrid search that combines both. It is the most versatile general-purpose memory backend in the OpenClaw Memory Stack, ideal for code search, documentation lookup, and finding specific symbols or behavioral patterns across a codebase.

**Free and open source (MIT)**. Note: requires Bun runtime and SQLite FTS5 extension (Bun's built-in SQLite includes FTS5, so no separate installation is needed).

## Prerequisites

| Dependency | Required | Notes |
|------------|----------|-------|
| [Bun](https://bun.sh) | Yes | JavaScript/TypeScript runtime. Not universally installed — users must install separately. |
| SQLite FTS5 | Yes | Full-text search extension. Bun's built-in SQLite driver includes FTS5 by default. |
| `qmd` CLI | Yes | Installed via `bun install -g qmd`. |

Bun is not as ubiquitous as Node.js. If the user does not have Bun installed, `setup.sh` will fail with exit code 2 and provide installation instructions.

## Configuration

Configuration is stored in `config.json` alongside this file. Key settings:

- `index_path`: Location of the SQLite index (`~/.cache/qmd/index.sqlite`)
- `search.default_mode`: Default search mode (`query` for hybrid)
- `search.modes`: Available search modes with their minimum score thresholds
- `relevance`: Normalization formula for raw BM25 scores

Per-project collections are configured via the `qmd` CLI, not through config.json.

## Usage

### Store

QMD indexes existing files on disk — "storing" means adding files to a collection via glob patterns, then generating vector embeddings.

**Step 1 — Create a collection:**
```bash
qmd collection add <name> --pattern "**/*.md" --path /project/path
```

**Step 2 — Generate embeddings:**
```bash
qmd embed <name>
```

**Step 3 — (Optional) Add context descriptions:**
```bash
qmd context add -c <name> "This collection contains API documentation for the auth module"
```

**Updating after file changes:**
```bash
qmd update <name>
```

Collections can use any glob pattern: `**/*.swift`, `src/**/*.ts`, `docs/**/*.md`, etc.

### Retrieve

Retrieve a specific indexed document by its QMD URI:

```bash
qmd get qmd://<collection>/path/to/file
```

Retrieve multiple documents in one call:

```bash
qmd multi_get qmd://<collection>/file1,qmd://<collection>/file2
```

Use `multi_get` when you need 3 or more files — never call `get` repeatedly.

### Search

QMD provides three search modes. Mode selection is critical for result quality.

#### Mode Selection Guide

| Signal | Mode | Command | minScore | When to use |
|--------|------|---------|----------|-------------|
| Exact name, symbol, error string | `search` | `qmd search "query" -c collection` | 0.1 | Function names, class names, error messages |
| Concept, behavior, "how does X work" | `vsearch` | `qmd vsearch "query" -c collection` | 0.3 | Understanding behavior, finding related code |
| Unclear, broad, first-time exploration | `query` | `qmd query "query" -c collection` | 0.3 | Cross-cutting concerns, initial exploration |

**Quick rule:** Know the exact word? Use `search`. Describing behavior? Use `vsearch`. Not sure? Use `query`.

#### Search Examples

```bash
# BM25 keyword — find a specific function
qmd search "handleAuthCallback" -c myproject --minScore 0.1

# Vector semantic — find code related to a concept
qmd vsearch "how does the payment flow handle retries" -c myproject --minScore 0.3

# Hybrid — broad exploration
qmd query "error handling middleware" -c myproject --minScore 0.3
```

#### Result Handling

- **< 2 results above minScore**: Broaden the search — try `query` mode, drop collection filter, or rephrase
- **2-5 results**: Ideal. Use `qmd get` to read the top hits
- **> 5 results**: Consider narrowing with a more specific query or higher minScore

Always specify `-c collection` when the project has per-layer collections.

## Interface Contract

### Input

- `store(key, content, metadata?)` — Maps to `qmd collection add` + `qmd embed`
- `retrieve(query, options?)` — Maps to `qmd get qmd://<collection>/path`
- `search(pattern, scope?)` — Maps to `qmd search|vsearch|query "pattern" -c scope`

### Output Format

All backends return the same JSON structure:

```json
{
  "query_echo": "original query string",
  "results": [
    {
      "content": "matched file content or excerpt",
      "relevance": 0.82,
      "source": "qmd",
      "timestamp": "2026-03-10T14:30:00Z"
    }
  ],
  "result_count": 2,
  "status": "success",
  "error_message": null,
  "error_code": null,
  "backend_duration_ms": 230,
  "normalized_relevance": 0.82,
  "backend": "qmd"
}
```

### Failure Codes

| Code | Meaning |
|------|---------|
| `BACKEND_UNAVAILABLE` | Bun or qmd not installed, or SQLite index missing |
| `QUERY_TIMEOUT` | Exceeded 5s (router-measured) |
| `EMPTY_RESULT` | Query succeeded but no matches above minScore |
| `PARTIAL_RESULT` | Collection exists but index is stale or incomplete |
| `BACKEND_ERROR` | Internal error (see error_message) |

### Relevance Normalization

BM25 raw scores are inherently low (typically 0.1-0.3 for good results) due to camelCase tokenization in code. This is normal, not a sign of poor results.

**Normalization formula:** `normalized = min(raw * 3, 1.0)`

| Raw BM25 Score | Normalized Score | Interpretation |
|----------------|------------------|----------------|
| 0.10 | 0.30 | Weak match |
| 0.20 | 0.60 | Good match |
| 0.33+ | 1.00 | Strong match (capped) |

Vector search (`vsearch`) scores are already in 0.0-1.0 range and do not need normalization.

### Router Integration

- Normalized relevance >= 0.4 -> "good enough", no fallback needed
- Normalized relevance < 0.4 or status = empty -> trigger fallback to next backend
- status = error -> immediate fallback, log error

## Limitations

- **Bun dependency**: Bun is not as widely installed as Node.js. Users must install it separately, which adds friction.
- **BM25 struggles with semantic queries**: Keyword search cannot understand meaning — "authentication flow" will not match "login process" unless both terms appear in the text.
- **Vector embedding startup cost**: First-time `qmd embed` on a large collection can take minutes. Subsequent updates are incremental.
- **Index staleness**: After file changes, the index must be updated with `qmd update`. If the user forgets, search results may be outdated or incomplete.
- **camelCase tokenization**: BM25 scores are naturally low because camelCase identifiers are split into tokens. A minScore of 0.1 is appropriate for `search` mode — do not set it higher or you will miss valid results.
- **No real-time indexing**: Unlike some backends, QMD does not watch for file changes. Reindexing is manual or hook-driven.

## Tier

**Free and open source (MIT).** Requires Bun runtime and no paid API keys. The only barrier to entry is installing Bun.
