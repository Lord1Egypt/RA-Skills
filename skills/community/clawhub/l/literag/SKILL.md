---
name: literag
version: 0.2.2
description: "Local retrieval skill for large documentation corpora using independent SQLite knowledge libraries with keyword plus vector hybrid search. Use when searching Blender manuals, API references, SDK docs, framework docs, product docs, blog/article archives, exported markdown doc sets, or any other large external documentation that should not live in OpenClaw's main memory index. Also use when indexing, reindexing, debugging retrieval quality, checking index compatibility/status, or inspecting LiteRAG sqlite metadata. Usage: /literag search <library> <query> | /literag inspect <library> <path> [--start N --end N] | /literag index <library> | /literag status <library> | /literag meta <library> | /literag benchmark <library> --query ..."
user-invocable: true
homepage: https://github.com/little-jax/literag
metadata: { "openclaw": { "emoji": "📚", "requires": { "bins": ["python3"] } } }
---

# LiteRAG

Use this skill when the target corpus is too large or too noisy for main agent memory.

## Install

Packaged dependency install:

```bash
python3 -m pip install -r {baseDir}/requirements.txt
```

## Layout

- Config + databases live under `<workspace>/.literag/`
- Main config: `<workspace>/.literag/knowledge-libs.json`
- Default workspace resolution order: `OPENCLAW_WORKSPACE` → `WORKSPACE` → walk upward from the current path until the OpenClaw workspace sentinel files are found
- Core scripts live under `skills/literag/scripts/`
- Skill bin entrypoint: `skills/literag/bin/literag`
- Workspace convenience wrappers live at `scripts/literag-query.py`, `scripts/literag-index.py`, `scripts/literag-status.py`, `scripts/literag-meta.py`, and `scripts/lq`

## Rules

- Keep personal/work memory in OpenClaw builtin memory
- Keep large external corpora in LiteRAG, not `memory_search`
- Treat each knowledge base as an independent library with its own SQLite
- Search first, inspect second
- Prefer grouped document hits over raw chunk spam
- Prefer source-relative paths when citing files back to the user
- Use local OpenAI-compatible embeddings by default unless explicitly changed in config

## Read these files when needed

- Always read `<workspace>/.literag/knowledge-libs.json` when targeting a library or changing config
- Read `references/usage.md` when you need command examples, output schema, or the intended search → inspect workflow
- Read `references/configuration.md` when adding libraries, source roots, excludes, chunking overrides, or ranking overrides
- Read `references/agent-prompts.md` when another agent / ACP harness needs a ready-made LiteRAG prompt template
- Read `references/optimization-playbook.md` when a specific library needs retrieval-quality tuning, ranking cleanup, or indexing-throughput tuning
- Read scripts under `skills/literag/scripts/` only when editing behavior or diagnosing bugs

## Slash / user-invocable usage

When invoked as `/literag ...`, parse the remaining argument string as a subcommand.

Supported forms:

- `/literag search <library> <query>`
- `/literag inspect <library> <path> [--start N --end N]`
- `/literag index <library> [--limit-files N] [--embedding-batch-size N]`
- `/literag index-all [--limit-files N] [--embedding-batch-size N]`
- `/literag status <library>`
- `/literag meta <library>`
- `/literag benchmark <library> --query ...`

If the user gives a natural-language request instead of a strict subcommand, translate it to the nearest supported operation instead of being pedantic.

## Supported commands

- `index_library.py` — index one library
- `index_all.py` — index all configured libraries
- `search_library.py` — grouped hybrid/fts/vector retrieval
- `inspect_result.py` — expand a hit by file path + chunk range
- `status_library.py` — show index health / compatibility / counts
- `meta_library.py` — dump raw sqlite `meta` records
- `benchmark_library.py` — benchmark hybrid/fts/vector latency + hit shape across fixed query sets
- `bin/literag` — packaged CLI entrypoint for search / inspect / index / status / meta / benchmark
- `scripts/literag-query.py` — query/search/inspect wrapper
- `scripts/literag-index.py` — index wrapper for one library or all libraries
- `scripts/literag-status.py` — status wrapper
- `scripts/literag-meta.py` — meta wrapper
- `scripts/literag-benchmark.py` — benchmark wrapper
- `scripts/lq` — tiny shell alias for `literag-query.py`

## Operating workflow

1. Read `<workspace>/.literag/knowledge-libs.json`
2. Resolve the target library
3. Run `search_library.py` for grouped retrieval
4. If needed, run `inspect_result.py` on the top hit or chosen range
5. For quick operator use, prefer `scripts/literag-query.py` or `scripts/lq`
6. Use `scripts/literag-index.py` when you need a short indexing entrypoint
7. Use `scripts/literag-status.py` before debugging weird retrieval or after config changes
8. Use `scripts/literag-meta.py` when you need the raw stored metadata
9. Use `scripts/literag-benchmark.py` or `skills/literag/scripts/benchmark_library.py` when you need repeatable retrieval latency / hit-shape comparisons
10. Keep LiteRAG separate from builtin memory unless the user explicitly wants a durable summary copied into workspace memory

## Current intent

Use LiteRAG for:
- Blender manual + Blender Python reference
- Future blog/article/site knowledge bases
- Any large external docs where hybrid retrieval is needed without polluting builtin memory
