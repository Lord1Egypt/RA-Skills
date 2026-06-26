# LiteRAG configuration reference

Config file:

- `<workspace>/.literag/knowledge-libs.json`

Workspace resolution order:

- `OPENCLAW_WORKSPACE` if set
- otherwise `WORKSPACE` if set
- otherwise LiteRAG walks upward from the current path/config path until it finds the OpenClaw workspace sentinel files (`AGENTS.md`, `SOUL.md`, `USER.md`, `MEMORY.md`)

## Rules

- Prefer omitting `sqlitePath` unless you have a real reason to place the DB elsewhere
- When `sqlitePath` is omitted, LiteRAG now defaults to:
  - `${WORKSPACE}/.literag/<library-id>.sqlite`
- Prefer `defaults` for global tuning
- Use per-library overrides only when a corpus truly behaves differently
- Prefer multiple `paths` under one library when they belong to the same searchable corpus
- Use `exclude` aggressively to skip junk, generated docs, changelogs, or duplicate mirrors

## Current supported shape

```json
{
  "version": 1,
  "defaults": {
    "chunking": {
      "maxChars": 2200,
      "overlapChars": 250,
      "minChars": 180,
      "preferHeadings": true
    },
    "retrieval": {
      "fts": { "enabled": true, "tokenizer": "unicode61" },
      "vector": { "enabled": true, "topK": 24 },
      "hybrid": { "enabled": true, "ftsWeight": 0.4, "vectorWeight": 0.6, "rrfK": 60 }
    },
    "ranking": {
      "referencesPenalty": 0.18,
      "navigationPenalty": 0.12,
      "tablePenalty": 0.08,
      "headingTermBoost": 0.03,
      "textTermBoost": 0.01
    }
  },
  "embedding": {
    "provider": "openai-compatible",
    "baseUrl": "http://localhost:11434/v1/",
    "apiKey": "local-noauth",
    "model": "qwen3-embedding:0.6b",
    "timeoutMs": 120000,
    "batchSize": 16,
    "maxConcurrency": 2,
    "maxRetries": 2,
    "retryBackoffMs": 750
  },
  "libraries": [
    {
      "id": "blender-docs",
      "name": "Blender Docs",
      "paths": [
        {
          "path": "/absolute/or/relative/source/path",
          "include": ["**/*.md", "**/*.mdx"],
          "exclude": ["**/changelog/**", "**/release_notes/**"]
        }
      ],
      "chunking": {
        "maxChars": 1800,
        "overlapChars": 220,
        "minChars": 140,
        "preferHeadings": true
      },
      "retrieval": {
        "vector": { "topK": 32 },
        "hybrid": { "ftsWeight": 0.35, "vectorWeight": 0.65, "rrfK": 50 }
      },
      "ranking": {
        "referencesPenalty": 0.25,
        "navigationPenalty": 0.15,
        "tablePenalty": 0.10,
        "headingTermBoost": 0.04,
        "textTermBoost": 0.01
      }
    }
  ]
}
```

## Index metadata and compatibility

LiteRAG now stores a few library-level metadata keys in the sqlite `meta` table during indexing, including:

- `schema_version`
- `embedding_model`
- `embedding_base_url`
- `embedding_fingerprint`
- `index_config_fingerprint`
- `vector_backend`
- `vector_backend_runtime`
- `vector_dimensions`
- `document_count`
- `chunk_count`
- `embedding_count`
- `last_indexed_at`

Runtime use:

- if the current embedding model/config differs from what produced the stored vectors, search/inspect/status emits a warning
- if indexing-relevant config changes (`paths`, chunking, retrieval knobs, ranking knobs), search/inspect/status emits a warning that reindex is recommended
- document rows also store per-document `chunking_fingerprint` and `embedding_fingerprint` so incremental indexing can detect config-driven reindex needs at file level
- vector retrieval prefers `sqlite-vec` when the runtime can load SQLite extensions; otherwise it falls back to the older Python-side cosine scan over stored JSON embeddings
- `vector_backend` records what the current DB was actually indexed with; `vector_backend_runtime` records what the current runtime can use right now
- `embedding.maxConcurrency` is honored by the indexer: changed files are chunked locally, then embedding batches are sent through a bounded concurrent pipeline instead of one-file-at-a-time blocking
- this is advisory; it does not force-delete the DB on its own

## Field reference

### embedding

- `baseUrl`: OpenAI-compatible embedding endpoint base URL
- `apiKey`: bearer token; use `local-noauth` for local endpoints that ignore auth
- `model`: embedding model id
- `timeoutMs`: per-request timeout
- `batchSize`: texts per embedding request; separate from chunk/DB batch size
- `maxConcurrency`: how many embedding requests LiteRAG may keep in flight during indexing
- `maxRetries`: retry count for transient embedding failures like 429/5xx/timeouts
- `retryBackoffMs`: linear backoff base in milliseconds between retry attempts

### defaults.chunking

- `maxChars`: target chunk size
- `overlapChars`: overlap when splitting long sections
- `minChars`: tiny chunks below this may get merged into the previous chunk when sensible
- `preferHeadings`: split on markdown headings first

### defaults.retrieval

#### fts
- `enabled`: enable keyword retrieval
- `tokenizer`: currently informative only; SQLite FTS is using `unicode61`

#### vector
- `enabled`: enable embedding search
- `topK`: number of vector candidates kept before fusion
- runtime backend is auto-selected:
  - `sqlite-vec` when LiteRAG is running on a Python/SQLite build that supports extension loading
  - `python-scan` fallback otherwise

#### hybrid
- `enabled`: enable hybrid mode
- `ftsWeight`: RRF contribution for FTS candidates
- `vectorWeight`: RRF contribution for vector candidates
- `rrfK`: reciprocal-rank fusion constant

### defaults.ranking

- `referencesPenalty`: down-rank `References`
- `navigationPenalty`: down-rank `See also` / nav junk
- `tablePenalty`: down-rank table-like nav chunks
- `headingTermBoost`: boost when query terms hit the heading
- `textTermBoost`: smaller boost when query terms hit the body text

## Library-level overrides

Each library may override:

- `chunking.maxChars`
- `chunking.overlapChars`
- `chunking.minChars`
- `chunking.preferHeadings`
- `retrieval.vector.topK`
- `retrieval.hybrid.ftsWeight`
- `retrieval.hybrid.vectorWeight`
- `retrieval.hybrid.rrfK`
- `ranking.referencesPenalty`
- `ranking.navigationPenalty`
- `ranking.tablePenalty`
- `ranking.headingTermBoost`
- `ranking.textTermBoost`

## Path resolution rules

- Absolute paths stay absolute
- Relative paths are resolved relative to the config file directory
- `sqlitePath`, when present, also follows the same rule
- Source `paths[].path` can be absolute or relative
- Default sqlite placement is workspace-relative: `<workspace>/.literag/<library-id>.sqlite`
- The workspace root is used for default config/sqlite locations; source indexing paths still come only from the configured library `paths`

## Recommended presets

### API reference / generated docs

Use:
- `preferHeadings: true`
- lower `maxChars` like `1600-2200`
- higher `referencesPenalty`
- use `exclude` for changelogs, release notes, and duplicate mirrors

### Narrative docs / manuals / blogs

Use:
- `preferHeadings: true`
- larger `maxChars` like `2200-3200`
- slightly larger `overlapChars`
- lower penalties because references are often less dominant anyway

## Example: multiple source roots in one library

```json
{
  "id": "cloudflare-docs",
  "name": "Cloudflare Docs",
  "paths": [
    {
      "path": "/docs/cloudflare/workers",
      "include": ["**/*.md", "**/*.mdx"],
      "exclude": ["**/changelog/**"]
    },
    {
      "path": "/docs/cloudflare/durable-objects",
      "include": ["**/*.md", "**/*.mdx"]
    }
  ]
}
```

That keeps related corpora in one searchable library without manually stitching paths later.
