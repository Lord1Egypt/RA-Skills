---
name: pontx-notion
description: Use for Notion API integration, pages, blocks, databases or data sources, comments, views, file uploads, workspace search, OAuth connections, and safe preview-first read or mutation workflows through @pontx/notion.
---

# Notion API

Start with live Pontx discovery instead of copying API fields into an
application. Use the universal CLI to resolve the current product, Endpoint,
Schema, and package guidance:

```bash
pontx-hub search "list pages in a database" --type endpoint --json
pontx-hub show <returned-resource-id>
pontx-hub sdk notion
```

Use `@pontx/notion` in application code and `pontx-notion` for an optional
local script. The Notion API is caller-directed: workspace content is private
End User data, and Pontx Hub does not proxy, cache, or aggregate it. Keep
requests and responses in the caller’s own process with the caller’s own
credentials.

## Credentials and versioning

Requests need a bearer token (internal connection token or personal access
token) and the required `Notion-Version` header (use `2026-03-11`). Inject
the token from `NOTION_ACCESS_TOKEN` or the `auth` option; never log it.
Public connections complete OAuth and use the client id/secret via HTTP Basic
on the `/v1/oauth` endpoints (create, introspect, and revoke token).

## Respect limits and retries

Each connection averages three requests per second and is also subject to the
workspace plan’s shared quota. On `429` (`rate_limited`) or `529`
(`service_overload`), respect the `Retry-After` header and retry with
exponential backoff and jitter. Only retry `5xx` for idempotent `GET`/`DELETE`.
Use `start_cursor` and `page_size` for pagination and treat cursors as opaque:
pass them back verbatim, never parse or store their format.

## Stay mutation-safe

The API includes deletes and other irreversible writes (delete blocks, delete
comments, delete views, revoke tokens). Always preview the exact request
first, confirm the target ID and payload before sending, and never auto-delete
or auto-revoke in an agent loop. Reads like `users.getSelf`, `search`, and
`retrievePage` are safe starting points.

## Webhooks

Notion webhooks are provider-to-caller HTTP callbacks carrying signed event
payloads (page, database, data source, comment, file upload, view events).
Verify the webhook signature from the current official documentation before
processing events; they are not callable API Endpoints.

## Few-shot workflows

### Scenario 1: Find and read a page

**User:** "What is the title of my latest page in the product docs database?"

**Approach:** Discover the current search and data-source query Endpoints,
preview a narrow read with the connection token, and return the page title
without caching workspace content.

### Scenario 2: Create a page with content

**User:** "Create a page in the product docs database with an example block."

**Approach:** Resolve the create-page contract, build the parent, property,
and child block payload from the current Schema, preview the exact mutation,
and send it only after the caller confirms the target database and payload.

### Scenario 3: Adopt it in a multi-tenant app

**User:** "Let users connect their own Notion workspaces to our app."

**Approach:** Implement the public-connection OAuth flow with the caller’s
client credentials, store tokens only as session or caller-owned secrets,
never log tokens or workspace content, and keep each workspace’s data isolated
to the connection that authorized it.
