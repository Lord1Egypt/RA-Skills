# openclaw-sage

An [OpenClaw](https://openclaw.ai) skill that makes any agent an expert on [OpenClaw](https://docs.openclaw.ai) documentation — with live doc fetching, BM25 ranked search, section extraction, full-text indexing, and change tracking.

## Requirements

- `bash`
- `curl`
- `xargs` *(standard on macOS/Linux; used for parallel `build-index.sh fetch`)*
- `python3` *(optional, recommended — enables BM25 ranked search, `--toc`/`--section` extraction, JSON output, and `recent.sh` date parsing)*

## Environment Variables

All variables are optional. Defaults work out of the box.

| Variable | Default | Description |
|---|---|---|
| `OPENCLAW_SAGE_SOURCE` | `github` | Doc source: `github` (fetch from GitHub) or `local:/path/to/openclaw/docs` (use local repo clone) |
| `OPENCLAW_SAGE_DOC_TTL` | `86400` | Doc page cache TTL in seconds (24hr) |
| `OPENCLAW_SAGE_FETCH_JOBS` | `8` | Parallel worker count for `build-index.sh fetch` (`1` restores sequential behavior) |
| `OPENCLAW_SAGE_CACHE_DIR` | `<skill_root>/.cache/openclaw-sage` | Cache directory |
| `OPENCLAW_SAGE_LANGS` | `en` | Languages to fetch: comma-separated codes (`en,zh`) or `all` |
| `OPENCLAW_SAGE_OUTPUT` | *(unset)* | Set to `json` for machine-readable output from `search.sh` and `sitemap.sh` |
| `OPENCLAW_SAGE_DOCS_BASE_URL` | `https://docs.openclaw.ai` | Override the base docs URL (useful for testing or private mirrors) |

Examples:
```bash
OPENCLAW_SAGE_DOC_TTL=60 ./scripts/fetch-doc.sh gateway/configuration
OPENCLAW_SAGE_LANGS=en,zh ./scripts/build-index.sh fetch
OPENCLAW_SAGE_FETCH_JOBS=4 ./scripts/build-index.sh fetch
OPENCLAW_SAGE_OUTPUT=json ./scripts/search.sh webhook
OPENCLAW_SAGE_SOURCE=local:/path/to/openclaw/docs ./scripts/build-index.sh fetch
```

## Version Support

All scripts accept a `--version <tag>` flag to work with docs at a specific OpenClaw release. Omitting it defaults to `latest` (fetched from `main`).

```bash
./scripts/cache.sh tags                                          # list available release tags
./scripts/build-index.sh fetch --version v2026.4.22             # fetch docs at a tag
./scripts/build-index.sh build --version v2026.4.22             # build index for that version
./scripts/search.sh --version v2026.4.22 webhook                # search a specific version
./scripts/fetch-doc.sh --version v2026.4.22 gateway/configuration  # read from a specific version
```

Compare two versions:
```bash
diff <(./scripts/fetch-doc.sh --version v2026.4.9 gateway/configuration) \
     <(./scripts/fetch-doc.sh --version v2026.4.22 gateway/configuration)
```

Use a local clone instead of GitHub (no network required):
```bash
OPENCLAW_SAGE_SOURCE=local:/path/to/openclaw/docs ./scripts/build-index.sh fetch
```

## Scripts

All scripts live in `./scripts/` and cache results in `.cache/openclaw-sage/` inside the skill root.

### Core

```bash
./scripts/sitemap.sh              # List all docs grouped by category
./scripts/sitemap.sh --json       # Same, as JSON [{category, paths[]}]
./scripts/cache.sh status         # Show cache location, age, TTLs, and doc count
./scripts/cache.sh refresh        # Clear sitemap cache to force re-fetch
./scripts/cache.sh clear-docs     # Remove all cached docs, HTML, and index
```

### Search & Fetch

```bash
./scripts/search.sh discord                   # Search cached docs by keyword (BM25 ranked if index built)
./scripts/search.sh --max-results 3 webhook   # Limit output to the top N matches
./scripts/search.sh --json "webhook retry"    # Same, as JSON {query, mode, results[]}
./scripts/recent.sh 7                         # Docs updated in the last N days (default: 7)

./scripts/fetch-doc.sh gateway/configuration          # Fetch full doc as plain text
./scripts/fetch-doc.sh gateway/configuration --toc    # Show headings only
./scripts/fetch-doc.sh gateway/configuration --section "Retry Settings"  # Extract one section
./scripts/fetch-doc.sh gateway/configuration --max-lines 50              # Truncate output
```

`search.sh` is the default discovery command: it uses BM25 when an index exists, but can also fall back to cached-doc grep and sitemap path matches.

**Recommended workflow for long docs:**
```bash
./scripts/fetch-doc.sh gateway/configuration --toc         # 1. See available sections
./scripts/fetch-doc.sh gateway/configuration --section retry  # 2. Fetch just what you need
```

### Full-Text Index

Build a local BM25 index for ranked search across all docs:

```bash
./scripts/build-index.sh fetch                  # Download all docs to cache (parallel by default; respects OPENCLAW_SAGE_LANGS)
./scripts/build-index.sh build                  # Build or incrementally refresh BM25 index + index_meta.json
./scripts/build-index.sh search "webhook retry" # BM25-ranked search over the built index only
./scripts/build-index.sh search --max-results 5 "webhook retry"
./scripts/build-index.sh status                 # Show doc/index/meta counts
```

`build-index.sh search` is the index-only query tool: it requires `index.txt` and does not fall back to cached docs or sitemap matches.

### Version Tracking

```bash
./scripts/track-changes.sh snapshot            # Save a snapshot of the current doc list
./scripts/track-changes.sh list                # Show all saved snapshots
./scripts/track-changes.sh since 2026-01-01    # Show docs added/removed since a date
./scripts/track-changes.sh diff <snap1> <snap2> # Compare two specific snapshots
```

## Cache

Files are stored in `.cache/openclaw-sage/` inside the skill root by default (override with `OPENCLAW_SAGE_CACHE_DIR`):

Each version gets its own subdirectory (e.g. `latest/`, `v2026.4.22/`):

| File | Description |
|---|---|
| `<version>/docs.json` | Doc list fetched from repo (replaces sitemap.xml) |
| `<version>/doc_<path>.md` | Cached raw Markdown source |
| `<version>/doc_<path>.txt` | Cached doc as plain text (derived from .md) |
| `<version>/index.txt` | Full-text search index |
| `<version>/index_meta.json` | Pre-computed BM25 statistics |
| `<version>/snapshots/` | Timestamped doc-list snapshots |
| `github_tags.json` | Cached GitHub release tag list (from cache.sh tags) |

The `.cache/` directory is gitignored.

## Docs

All documentation is at [docs.openclaw.ai](https://docs.openclaw.ai).

## License

MIT
