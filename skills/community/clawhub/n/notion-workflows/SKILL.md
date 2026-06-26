---
name: notion-workflows
description: Notion automations: Create/query/update pages/DBs, templates, summaries. Browser/playwright for UI. Triggers: \"notion db build\", \"notion page create\", \"notion summary\". Examples: Task DB, wiki pages.</description>
---

# Notion Workflows

## Examples
- \"Build Notion task DB\": browser → new DB, props (name/due/status).
- \"Summarize Notion page\": snapshot → markdown extract.
- \"Add tasks to DB\": canvas/A2UI form → insert rows.

## Workflow
1. browser action=open notion.so → auth if needed.
2. snapshot page/DB → parse structure.
3. act: click add row, fill fields.
4. Export: pdf/snapshot.

refs/notion-selectors.md: Common aria-refs.
scripts/notion-scrape.py: DB to CSV.

assets/templates/task-db.json: Import schema.
