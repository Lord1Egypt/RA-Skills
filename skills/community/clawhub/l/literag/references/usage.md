# LiteRAG usage

## What exists

Core scripts live in `skills/literag/scripts/`:

- `index_all.py` — index all configured libraries
- `index_library.py` — index one library
- `search_library.py` — hybrid/fts/vector search
- `inspect_result.py` — expand a hit by file path + chunk range or chunk ids

Workspace convenience wrappers:

- `scripts/literag-query.py`
- `scripts/literag-index.py`
- `scripts/literag-status.py`
- `scripts/literag-meta.py`
- `scripts/lq` — tiny shell alias for `literag-query.py`

Runtime note:

- LiteRAG wrappers prefer `LITERAG_PYTHON`, then `/opt/homebrew/bin/python3`, then fall back to the current interpreter
- This matters because `sqlite-vec` needs a Python/SQLite build with extension loading enabled; on this Mac that means Homebrew Python, not the Xcode/system Python

Config lives at:

- `.literag/knowledge-libs.json`

Reference docs:

- `references/configuration.md` — config schema, overrides, source examples
- `references/agent-prompts.md` — high-level prompt templates for agents/ACP harnesses

## Slash-style usage

If LiteRAG is invoked via `/literag`, map subcommands to the same underlying operations:

- `/literag search blender-docs "Geometry Nodes simulation zone"`
- `/literag status blender-docs`
- `/literag index blender-docs --embedding-batch-size 32`
- `/literag benchmark blender-docs --query "bpy.types.Object constraints"`

## Default retrieval shape

`search_library.py` now defaults to agent-friendly output:

- `--format agent`
- `--group-by path`
- `--merge-adjacent`

That means results are grouped by document and include merged hit ranges instead of raw chunk spam.

## Typical workflow

### 1) Search

```bash
python skills/literag/scripts/search_library.py blender-docs "ThemeTextEditor cursor"
```

### 2) Inspect the best hit or a specific range

```bash
python skills/literag/scripts/inspect_result.py \
  blender-docs \
  /Users/jaxlocke/Documents/bl_manual/blender_python_reference/bpy.types.ThemeTextEditor.md \
  --start 0 --end 0
```

### 3) Use the workspace wrapper for one-shot search + inspect

```bash
python scripts/literag-query.py blender-docs "ThemeTextEditor cursor"
```

### 4) Search only

```bash
python scripts/literag-query.py search blender-docs "ThemeTextEditor cursor"
```

### 5) Inspect a specific file/range directly

```bash
python scripts/literag-query.py inspect \
  blender-docs \
  /Users/jaxlocke/Documents/bl_manual/blender_python_reference/bpy.types.ThemeTextEditor.md \
  --start 0 --end 0
```

### 6) Index one library or all libraries

Default behavior is incremental: unchanged files are skipped, changed files are re-chunked/re-embedded, and removed files are pruned.

```bash
python scripts/literag-index.py blender-docs
python scripts/literag-index.py --all

# override only the embedding request size when tuning throughput
python scripts/literag-index.py blender-docs --embedding-batch-size 32

# packaged skill bin
skills/literag/bin/literag index blender-docs --embedding-batch-size 32
```

Force a full rebuild only when you actually want to throw away the sqlite artifacts first:

```bash
python scripts/literag-index.py blender-docs --full-reindex
python scripts/literag-index.py --all --full-reindex
```

### 7) Check library status / compatibility

```bash
python scripts/literag-status.py blender-docs
python scripts/literag-status.py --format json
```

### 8) Dump raw sqlite meta

```bash
python scripts/literag-meta.py blender-docs
python scripts/literag-meta.py
```

### 9) Short alias

```bash
scripts/lq blender-docs "ThemeTextEditor cursor"
```

### 10) Benchmark retrieval speed + hit shape

Run repeatable latency checks across `hybrid`, `fts`, and `vector` with a fixed query set:

```bash
python scripts/literag-benchmark.py blender-docs \
  --query "ThemeTextEditor cursor" \
  --query "bpy.types.Object constraints" \
  --query "Geometry Nodes simulation zone" \
  --warmup --repeat 3

# packaged skill bin
skills/literag/bin/literag benchmark blender-docs --query "ThemeTextEditor cursor"
```

Or load queries from a text/json file:

```bash
python scripts/literag-benchmark.py blender-docs --queries-file ./queries.txt --warmup --repeat 3
```

## Output schemas

### Search

`literag.search.v2`

Top-level fields:

- `library`
- `query`
- `mode`
- `group_by`
- `merge_adjacent`
- `warning`
- `results[]`

Grouped result fields:

- `path`
- `source_rel_path`
- `score`
- `heading`
- `headings`
- `chunk_count`
- `range_count`
- `ranges[]`

Each `range` may contain:

- `start_chunk_index`
- `end_chunk_index`
- `chunk_ids`
- `heading`
- `headings`
- `score`
- `snippet`
- optional `text`

### Inspect

`literag.inspect.v1`

Fields:

- `path`
- `warning`
- `source_rel_path`
- `chunk_count`
- `start_chunk_index`
- `end_chunk_index`
- `chunk_ids`
- `headings`
- `text`
- `text_truncated`
- `chunks[]`

## Status behavior

- `literag-status.py` reports whether the sqlite exists, core meta counts, current runtime vector backend, and whether current config still matches the indexed config
- `literag-meta.py` dumps raw `meta` table records for auditing/debugging

## Indexing behavior

- Indexing is incremental by default
- Unchanged files are detected by `mtime + size + sha1`
- Removed files are pruned from the sqlite index
- The DB records metadata about the indexing run, including embedding model, index config fingerprint, vector backend, and vector dimensions
- When available, vector indexing/search uses `sqlite-vec`; otherwise LiteRAG falls back to Python-side cosine scanning over stored embeddings
- Changed files are chunked first, then embedding batches are sent through a bounded concurrent pipeline shared across files; this is much faster than old one-file-at-a-time blocking
- `embedding.batchSize` controls texts per embedding request and is now decoupled from `--batch-size`
- `embedding.maxConcurrency` controls how many embedding requests may be in flight during indexing
- Transient embedding failures (for example 429/5xx/timeouts from the local OpenAI-compatible endpoint) are retried with bounded backoff via `embedding.maxRetries` + `embedding.retryBackoffMs`
- Search/inspect can emit a warning when the current config no longer matches the indexed config

## Config behavior

- `sqlitePath` is now optional
- If omitted, the sqlite DB path defaults to:
  - `${WORKSPACE}/.literag/<library-id>.sqlite`
- Source paths may now use:
  - `include`
  - `exclude`
- Relative config paths are resolved relative to `.literag/knowledge-libs.json`
- Library-level overrides now exist for chunking, retrieval, and ranking
- Vector backend selection is runtime-driven; on this Mac, wrappers intentionally prefer Homebrew Python so `sqlite-vec` can load

## Wrapper behavior

`literag-query.py` supports three modes:

- `query` — search + inspect best chosen hit/range
- `search` — grouped search only
- `inspect` — inspect a specific path/range directly

If no subcommand is given, it defaults to `query`, so this works:

```bash
python scripts/literag-query.py blender-docs "cursor theme"
```

## Practical guidance for agents

- Use LiteRAG for large external docs, not personal memory
- Search first, inspect second
- Prefer grouped document hits over raw chunks
- Prefer source-relative paths when reporting citations
- Keep answers compact; include only the ranges actually used

## Current configured libraries

From `.literag/knowledge-libs.json` right now:

- `blender-docs` → Blender Docs
- `openclaw-docs` → OpenClaw Docs
