---
name: new-openclaw-docs
description: Navigate and use OpenClaw documentation efficiently with cached doc fetch/search tooling, sitemap/category routing, and config snippet lookup. Use when answering OpenClaw setup/config/troubleshooting questions, checking docs updates, or extracting concrete configuration examples from docs.
---

# OpenClaw Docs

Use this skill to answer OpenClaw documentation questions with reproducible script-assisted evidence.

## Quick workflow

1. Route by intent (setup, config, troubleshooting, automation, platform).
2. Search or fetch docs via scripts.
3. Pull exact config patterns from snippets/docs.
4. Cite source URL/path in the final answer.

## Use bundled resources

- Intent routing and category map: `references/routing.md`
- Script usage and operational notes: `references/operations.md`
- Config patterns: `snippets/common-configs.md`
- Script preflight checks: `scripts/check_env.sh`

## Rules

- Prefer `search.sh` and `fetch-doc.sh` before freeform guessing.
- Keep answers anchored to specific doc paths.
- For uncertain or stale cache cases, refresh or state cache limitations.
- Provide concrete configuration examples when available.

## Commands

```bash
# Validate local script requirements
bash workspace/skills/new-openclaw-docs/scripts/check_env.sh

# Discover likely paths
bash workspace/skills/new-openclaw-docs/scripts/sitemap.sh
bash workspace/skills/new-openclaw-docs/scripts/search.sh discord mention

# Fetch a document
bash workspace/skills/new-openclaw-docs/scripts/fetch-doc.sh providers/discord

# Cache and update checks
bash workspace/skills/new-openclaw-docs/scripts/cache.sh status
bash workspace/skills/new-openclaw-docs/scripts/recent.sh 7
bash workspace/skills/new-openclaw-docs/scripts/track-changes.sh since 2026-02-01
```
