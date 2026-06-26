# Hemlane MCP

Hemlane MCP is a local, public-safe automation layer for Hemlane workflows. It turns saved Hemlane browser HAR captures into repeatable MCP tools and scripts, with auth supplied only at runtime.

## What is included

- FastMCP server: `mcp/server.py`
- HAR-derived GraphQL catalog: `references/operation-catalog.json` and `.csv`
- Workflow references: `references/*.md`
- Replay/query scripts: `scripts/*.py`
- OpenClaw skill entrypoint: `SKILL.md`

## Current MCP tools

Read-oriented tools:

- `capture_auth` for read endpoints, from an authenticated Brave/CDP session
- `list_graphql_operations` to inspect HAR-derived operations
- `query_catalog_operation` to replay any read-only catalog query
- `get_context_values` for `ODGetContextValues`
- `get_tenant_groups` for `ODTenantsAndLeasesTenantGroups`
- `get_maintenance_requests` for `ODMaintenanceRequests`
- `get_transactions` for `TransactionsNextCursorQuery`
- `query_recurring_payment_requests`
- `query_financials_operation`
- `extract_rent_roll`

Write tools, fail-closed unless the runtime caller is verified:

- `send_tenant_reply`
- `submit_referral`
- `post_workorder_comment`
- `post_maintenance_comment`
- `capture_auth` for write endpoints

## Auth model

Do not commit live cookies, CSRF tokens, bearer tokens, or browser session material.

Use one of:

1. `capture_auth(endpoint_kind=..., out_file=/tmp/hemlane-auth.json)` from an authenticated Brave session.
2. Runtime env vars: `HEMLANE_COOKIE`, `HEMLANE_CSRF_TOKEN`, `HEMLANE_AUTHORIZATION`, `HEMLANE_USER_AGENT`, `HEMLANE_REFERER`, `HEMLANE_ORIGIN`.

## HAR reverse-engineering workflow

1. Place new Hemlane HAR files in a local-only path, usually `~/Downloads/har`.
2. Extract GraphQL operations with `scripts/extract_hemlane_graphql.py` against the HAR files.
3. Regenerate the catalog with `scripts/build_hemlane_catalog.py`.
4. Add or update a focused wrapper script if the operation is business-critical.
5. Expose it in `mcp/server.py` as a read-only tool or a guarded write tool.
6. Document the workflow in `references/` and `SKILL.md`.

## Generic read replay

Use `scripts/query_catalog_operation.py` with:

- `--operation-name ODGetContextValues`
- `--auth-file /tmp/hemlane-auth.json`
- `--variables-json '{}'`
- optional `--dry-run`

## Safety rules

- Generic catalog replay refuses non-query operations.
- Write tools require verified privileged caller metadata and otherwise fail closed.
- Secrets must be runtime-only.
- Prefer GraphQL replay over browser clicking.
- Start with `--dry-run` when adding a new HAR-derived operation.

## Current HAR coverage

Summaries live in `references/har-summary.md`, `references/graphql-operations.md`, `references/financials-har-summary.md`, `references/rent-roll-integration.md`, and `references/runbooks.md`.

Known captured areas include referrals, tenant replies, work orders, maintenance updates, requests, transactions, financials, rent roll, and lease generation.

Note: at the time this README was added, `~/Downloads/har` resolved to `/mnt/f/repos/openclaw/har`, which was unavailable with `Host is down`. Existing repository references/catalog were used, and only AppleDouble `._rent_roll*.har` files were visible directly in `~/Downloads`.
