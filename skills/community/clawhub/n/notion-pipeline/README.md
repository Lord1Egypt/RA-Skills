# notion-pipeline

Versioned OpenClaw skill for the local-first idea factory's Notion workflows.

## What it includes

- `SKILL.md` instructions for OpenClaw
- low-level Notion API helpers
- higher-level factory workflow scripts
- env var reference docs

## Main commands

```bash
node scripts/notion_api.mjs check-env
node scripts/notion_api.mjs query-db research
node scripts/factory_ops.mjs list-ideas 2026-03-27
node scripts/factory_ops.mjs handle-approval approve <ideaId>
node scripts/factory_ops.mjs get-project <projectId>
```

## Required env

- `OPENCLAW_NOTION_TOKEN`
- `OPENCLAW_NOTION_DB_RESEARCH_SIGNALS`
- `OPENCLAW_NOTION_DB_PROJECT_IDEAS`
- `OPENCLAW_NOTION_DB_PROJECTS`
- `OPENCLAW_NOTION_DB_NIGHTLY_RUNS`

## Packaging note

This folder is ready to be versioned and published through ClawHub as a skill bundle.
