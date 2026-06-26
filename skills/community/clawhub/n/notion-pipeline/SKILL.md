---
name: notion-pipeline
description: Use when the night-shift agents need to validate Notion env, query a Notion database, create or update pages, or append blocks in the idea-factory databases.
metadata: { "openclaw": { "emoji": "🗂️", "requires": { "bins": ["node"] } } }
---

# notion-pipeline

Use the helper script at `{baseDir}/scripts/notion_api.mjs` for all low-level Notion operations.
Use `{baseDir}/scripts/factory_ops.mjs` for higher-level factory workflows such as signal writes, librarian reviews, idea writes, evaluations, approvals, and HPD project packs.
Local runtime env is loaded from `/Users/dellymac/.openclaw/secrets/notion.env` when present.

## Expected env

- `OPENCLAW_NOTION_TOKEN`
- `OPENCLAW_NOTION_DB_RESEARCH_SIGNALS`
- `OPENCLAW_NOTION_DB_PROJECT_IDEAS`
- `OPENCLAW_NOTION_DB_PROJECTS`
- `OPENCLAW_NOTION_DB_NIGHTLY_RUNS`

See `{baseDir}/references/env-vars.md` for alias names and usage.

## Commands

```bash
OPENCLAW_NOTION_TOKEN=... node {baseDir}/scripts/bootstrap_factory.mjs
node {baseDir}/scripts/notion_api.mjs check-env
node {baseDir}/scripts/notion_api.mjs query-db research
node {baseDir}/scripts/notion_api.mjs query-db ideas filters.json
node {baseDir}/scripts/notion_api.mjs create-page research payload.json
node {baseDir}/scripts/notion_api.mjs update-page <page-id> payload.json
node {baseDir}/scripts/notion_api.mjs append-blocks <page-id> blocks.json
node {baseDir}/scripts/notion_api.mjs retrieve-page <page-id>
node {baseDir}/scripts/factory_ops.mjs write-signals signals.json
node {baseDir}/scripts/factory_ops.mjs list-signals trend inbox
node {baseDir}/scripts/factory_ops.mjs apply-signal-reviews reviews.json
node {baseDir}/scripts/factory_ops.mjs list-archived-signals mechanical
node {baseDir}/scripts/factory_ops.mjs write-ideas ideas.json
node {baseDir}/scripts/factory_ops.mjs list-ideas 2026-03-27
node {baseDir}/scripts/factory_ops.mjs apply-evaluations evaluations.json
node {baseDir}/scripts/factory_ops.mjs handle-approval approve <ideaId>
node {baseDir}/scripts/factory_ops.mjs record-report-delivery report_delivery.json
node {baseDir}/scripts/factory_ops.mjs get-project <projectId>
node {baseDir}/scripts/factory_ops.mjs update-project-pack <projectId> pack.json
```

## Rules

- Fail fast if `OPENCLAW_NOTION_TOKEN` is missing.
- Use `bootstrap_factory.mjs` to create or recover the 4 factory databases under an accessible parent page and persist the IDs into the local env file.
- Prefer database aliases `research`, `ideas`, `projects`, and `runs`.
- Keep payload files in JSON.
- Return the raw JSON response and inspect it before claiming success.
- If required env is missing, report only the missing variable names and stop. Do not invent setup commands.
