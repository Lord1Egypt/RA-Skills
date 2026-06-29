# MeiliSearch Memory

Local full-text search for OpenClaw memory recall. Self-hosted.

This skill does more than passive search. It also indexes content, distills facts into MEMORY.md, and manages background cron jobs.

## Security Model

- **Credentials**: MeiliSearch master key is loaded from `~/.openclaw/workspace/.env` — never hardcoded in scripts
- **Sensitive data filtering**: Indexer and distillation skip content containing tokens, passwords, API keys, private keys, and credentials
- **Safe defaults**: Distillation defaults to `--dry-run`; destructive operations require `--force`
- **Secure temp files**: All temporary files use `mktemp` with `chmod 600` and are cleaned up on exit

## Capabilities

- **Read**: `MEMORY.md`, `memory/*.md` (daily notes)
- **Write**: MeiliSearch indexes (`core`, `working`, `archive`), `MEMORY.md` (distillation only with `--apply`)
- **Execute**: `curl` to localhost MeiliSearch, `python3` for document processing

## Architecture

Three-tier indexing system:

- **Core** — MEMORY.md sections (highest importance, always current)
- **Working** — Daily notes from the last 7 days (recent context)
- **Archive** — Older daily notes (lower priority)

## Features

- **Tag-based query understanding** — Natural language queries map to relevant tag filters
- **Sensitive data exclusion** — Credentials, tokens, keys are never indexed or distilled
- **Fallback search** — Falls back to plain full-text if tag filters return nothing
- **Typo tolerance** — Built-in fuzzy matching via MeiliSearch

## Configuration

Requires `~/.openclaw/workspace/.env`:

```bash
MEILI_HOST=http://127.0.0.1:7700
MEILI_KEY=your-master-key-here
```

## Usage

```bash
bash scripts/search.sh "your query" [limit] [tier]
bash scripts/indexer.sh                # Incremental update
bash scripts/indexer.sh --full --force # Full reindex (destructive)
bash scripts/distill.sh --dry-run      # Preview distillation
bash scripts/distill.sh --apply        # Write to MEMORY.md
```

## License

MIT
