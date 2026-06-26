---
name: jszesze-openclaw-docs
description: OpenClaw documentation helper that caches the live docs index, searches page titles and URLs, fetches raw markdown docs, builds a local docs cache for full-text grep, and tracks index snapshots over time. Use when answering OpenClaw setup, configuration, CLI, channel, automation, architecture, or troubleshooting questions and you want grounded docs links or current page text.
---

# OpenClaw docs

Use this skill for **OpenClaw product docs**, not for general repo spelunking.

## What this skill is good at

- finding the right OpenClaw doc page quickly
- fetching raw markdown from `docs.openclaw.ai`
- caching the live docs index from `https://docs.openclaw.ai/llms.txt`
- downloading docs locally for full-text search
- tracking page additions/removals across snapshots of the docs index

## What it does not do

- it does **not** inject the whole docs site into context automatically
- it does **not** guarantee config snippets are current unless you verify them against fetched docs
- it does **not** replace local repo inspection when the answer depends on the user’s actual workspace state

## Workflow

1. Start with the live docs index.
2. Search by keyword to find the most likely page.
3. Fetch the raw markdown page.
4. Quote or summarize the relevant section.
5. Link the exact docs URL in the answer.
6. For broad questions, build a local docs cache and run a full-text search.

## Commands

Run scripts with `bash`.

### Index and cache

```bash
bash ./scripts/cache.sh status
bash ./scripts/cache.sh refresh
```

### Search and discovery

```bash
bash ./scripts/search.sh telegram
bash ./scripts/search.sh "group.*policy"
bash ./scripts/sitemap.sh
bash ./scripts/fetch-doc.sh gateway/configuration
bash ./scripts/fetch-doc.sh https://docs.openclaw.ai/channels/telegram
```

### Local full-text cache

```bash
bash ./scripts/build-index.sh fetch
bash ./scripts/build-index.sh build
bash ./scripts/build-index.sh search "requireMention"
# optional smoke-test limit:
OPENCLAW_DOCS_FETCH_LIMIT=25 bash ./scripts/build-index.sh fetch
```

### Change tracking

```bash
bash ./scripts/track-changes.sh snapshot
bash ./scripts/track-changes.sh list
bash ./scripts/track-changes.sh since 2026-05-01
bash ./scripts/recent.sh 7
```

## Heuristics

- **setup or install**: check `start/`, `install/`, `channels/`, `gateway/`
- **config fields or JSON5 shape**: check `gateway/configuration`, `gateway/configuration-reference`, `gateway/configuration-examples`
- **CLI questions**: check `cli/`
- **channel behavior**: check `channels/<provider>` and `channels/troubleshooting`
- **architecture or concepts**: check `concepts/`
- **automation**: check `automation/`
- **control UI, dashboard, web surfaces**: check `web/`
- **node/device questions**: check `nodes/`

## Good defaults

- Prefer fetched raw markdown over guessing from memory.
- Prefer the smallest relevant page instead of dumping a broad overview page.
- If a snippet matters operationally, verify it against the fetched page before giving it to the user.
- For ambiguous terms, search first, then fetch.

## Verified snippet notes

See `./snippets/common-configs.md` for a few small, verified patterns copied from current docs pages. Treat them as helpers, not as a schema reference.
