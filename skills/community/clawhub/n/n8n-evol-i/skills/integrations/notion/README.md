---
name: integration-notion
description: Notion nodes — internal integration tokens, database / page IDs.
user-invocable: false
---

# Notion

## Node type

`n8n-nodes-base.notion`.

## Credential type

`notionApi` — Internal Integration token from `notion.so/profile/integrations`.

For setup, see [`skills/manage-credentials.md`](../../manage-credentials.md). Path A: paste the `secret_...` token into `.env.<env>` and run.

## Database / page IDs

Notion URLs encode IDs without dashes; the API expects dashes. Example:

- URL: `https://www.notion.so/Workspace/MyDB-abc123def456789012345678901234`
- API: `abc123de-f456-7890-1234-5678901234`

The n8n Notion node accepts either form. Store the with-dashes version in env YAML.

## Sharing the integration

Database / page operations only work if the page is **shared with the integration** (top-right "Share" → invite the integration). This is a common foot-gun — the API returns 404 for unshared pages.

## Per-property field shape

Each property type (title, rich_text, multi_select, …) has a different JSON shape. The n8n Notion node abstracts this for common types but for complex inserts you may need a Code node that builds the body manually. See Notion's API docs for the exact field shapes.
