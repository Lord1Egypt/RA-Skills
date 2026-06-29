---
name: meili-memory
description: Local full-text search for OpenClaw memory recall using MeiliSearch. Self-hosted.
---

# MeiliSearch Memory

Local full-text search for memory recall. Self-hosted.

**Note**: This skill does more than passive search. It also indexes content, distills facts into MEMORY.md, and manages background cron jobs. See Capabilities and Security Model below.

## Security Model

- **Credentials**: MeiliSearch master key is loaded from `~/.openclaw/workspace/.env` — never hardcoded in scripts
- **Sensitive data filtering**: Indexer and distillation skip content containing tokens, passwords, API keys, private keys, and credentials
- **Safe defaults**: Distillation defaults to `--dry-run`; destructive operations require `--force`
- **Secure temp files**: All temporary files use `mktemp` with `chmod 600` and are cleaned up on exit

## Capabilities (declared)

- **Read**: `MEMORY.md`, `memory/*.md` (daily notes)
- **Write**: MeiliSearch indexes (`core`, `working`, `archive`), `MEMORY.md` (distillation only with `--apply`)
- **Execute**: `curl` to localhost MeiliSearch, `python3` for document processing

## Architecture

Three-tier indexing system that mimics human memory:

- **Core** — MEMORY.md sections (highest importance, always current)
- **Working** — Daily notes from the last 7 days (recent context)
- **Archive** — Older daily notes (lower priority)

Search queries hit all tiers in order: core → working → archive. Results are ranked by tier priority and importance score.

## Features

- **Tag-based query understanding** — Natural language queries like "what are my tasks" or "show my projects" automatically map to relevant tag filters for precise results
- **Relationship tags** — Each chunk is auto-tagged by topic (finance, projects, identity, infrastructure, etc.)
- **Tiered search** — Query core only for fast answers, or all tiers for deep recall
- **Auto-distillation** — Weekly cron extracts key facts from daily notes into MEMORY.md (requires `--apply`)
- **Typo tolerance** — Built-in fuzzy matching via MeiliSearch
- **Sensitive data exclusion** — Chunks containing credentials, tokens, or keys are never indexed or distilled
- **Fallback search** — If tag filters return no results, automatically falls back to plain full-text search

## Configuration

Requires `~/.openclaw/workspace/.env`:

```bash
MEILI_HOST=http://127.0.0.1:7700
MEILI_KEY=your-master-key-here
```

See `.env.example` for all options.

## Search

```bash
bash scripts/search.sh "your query" [limit] [tier]
```

Examples:
```bash
bash scripts/search.sh "your query"     # Search all tiers, top 5
bash scripts/search.sh "projects" 3      # Top 3 from all tiers
bash scripts/search.sh "setup" 5 core    # Core only (fast)
```

## Indexing

```bash
bash scripts/indexer.sh                # Incremental update (safe)
bash scripts/indexer.sh --full --force # Full reindex (destructive, requires --force)
```

## Distillation

```bash
bash scripts/distill.sh --dry-run      # Preview what would be added (default)
bash scripts/distill.sh --apply        # Actually write to MEMORY.md
```

**Note**: Distillation skips any content containing passwords, API keys, tokens, private keys, or credentials.

## Cron Jobs

- **Hourly** — Re-index new daily notes
- **Weekly (Sunday 2 AM)** — Distill facts into MEMORY.md

## Service

```bash
systemctl status meilisearch
journalctl -u meilisearch -f
```
