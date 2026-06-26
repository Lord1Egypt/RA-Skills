---
name: notion-tools
description: Use for tasks that read or modify Notion pages, data sources, or blocks via the Notion API.
homepage: https://developers.notion.com
metadata: {"clawdbot":{"emoji":"📝"}}
---

# notion-tools

Use this skill when the user wants to read or modify Notion content through the Notion API.

This skill is for operational API work, not general product explanation. Prefer the workflow below instead of inventing request shapes from memory.

## When To Use

Use this skill for:
- Finding a page, database, or data source in a Notion workspace
- Reading page properties or page block content
- Creating pages inside an existing database
- Querying a data source with filters or sorts
- Updating page properties
- Trashing or restoring a page
- Appending block content to a page

Do not use this skill for:
- Changing Notion UI-only settings such as saved views, view filters, or layout configuration
- Tasks that require browser automation instead of the public API

## Quick Checks

Before making requests, confirm:
- Prefer `NOTION_KEY` if the runtime already provides it
- If `NOTION_KEY` is unset in a local shell workflow, optionally load it from `~/.config/notion/api_key`
- The target page or database has been shared with the integration
- The caller understands that this skill assumes `Notion-Version: 2025-09-03`

If the environment is not ready, read `references/setup.md`.

## Working Rules

Always:
- Start with search unless the user already provided a verified page ID or data source ID
- Read before writing when modifying an existing page, block tree, or database-backed item
- Inspect the live schema before creating or updating page properties in a database
- Keep secrets out of output; never print the full API key back to the user
- Read secrets only when needed to make a Notion API request, not during unrelated planning or explanation

Do not:
- Assume a property named `Name`, `Status`, or `Date` exists without checking
- Assume a database ID and a data source ID are interchangeable
- Overwrite page content when the task only requires appending blocks

## Workflow

### 1. Find the target

Use search first for pages and data sources. If the result is a database-like object, record both IDs when present:
- `id` or `database_id` for page creation parents
- `data_source_id` for querying via `/v1/data_sources/{id}/query`

See `references/examples.md` for the search request template.

### 2. Inspect before mutation

Read the current object before writing:
- `GET /v1/pages/{page_id}` for page properties
- `GET /v1/blocks/{page_id}/children` for page content
- `GET /v1/data_sources/{data_source_id}` for schema inspection

See `references/examples.md` for request templates.

### 3. Create or update with the live schema

Common write paths:
- `POST /v1/pages` to create a page in an existing database
- `PATCH /v1/pages/{page_id}` to update page properties
- `PATCH /v1/pages/{page_id}` with `in_trash: true|false` to trash or restore a page
- `PATCH /v1/blocks/{page_id}/children` to append blocks

Before writing properties, confirm the exact property names and types from the live schema.
Do not describe trashing a page as permanent deletion; this flow moves the page into or out of trash.

See:
- `references/examples.md` for create, update, trash, restore, append, and query payloads
- `references/property-patterns.md` for common property value shapes
- `references/blocks.md` for equation blocks, inline code, code blocks, and table-cell formatting limits

### 4. Query database-backed content through the data source API

Use `/v1/data_sources/{data_source_id}/query` for filters, sorts, and pagination. If results are paginated, continue with `start_cursor` from the previous response.

See `references/examples.md` for query payloads.

## API Notes For This Version

This skill assumes `Notion-Version: 2025-09-03`.

Important version-specific behavior:
- Databases are queried through `/v1/data_sources/{data_source_id}/query`
- Page creation still uses `parent.database_id`
- Search results may expose a data source object instead of older database terminology
- Page responses may include both `parent.database_id` and `parent.data_source_id`
- Page deletion through the API is a trash operation via `in_trash`, not a permanent delete

## Troubleshooting

If a request fails, check auth, sharing, object IDs, and schema mismatches before changing the payload. For common failure modes, read `references/troubleshooting.md`.

## Safety

- Never commit the API key or paste it into project files
- Prefer runtime-injected `NOTION_KEY` over reading a local token file
- If a local token file is used, treat it as a convenience fallback for local shells rather than the default credential source
- Prefer append operations for block content unless the user explicitly asks to replace content
- If a task may touch many pages, query and inspect a small sample first
- When the user request is underspecified, return the candidate pages or data sources and ask which one to modify
