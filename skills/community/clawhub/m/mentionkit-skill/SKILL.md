name mentionkit
description Query and manage Mentionkit social monitoring workflows. Use when the user wants to review brand mentions, find actionable reply opportunities, shortlist lead-gen conversations, inspect source links, or create tracked keywords inside Mentionkit.
Prefer the Mentionkit MCP server when available; otherwise use the Mentionkit Public API v1 for narrower read-only scripting and basic data access.
license MIT
metadata author version
mentionkit

0.1.0

compatibility Requires a Mentionkit workspace with MCP access or API access. MCP needs an MCP-capable agent. API v1 needs internet access and a Mentionkit API key.

# Mentionkit

Mentionkit is a social monitoring tool. A workspace tracks projects and keywords, collects matching mentions across platforms, scores them for relevance, and helps operators review, verify, and respond to the strongest conversations. Mentionkit MCP is built around a context-first workflow: load the workflow context first, shortlist the best mentions second, and inspect source links before making a final judgment.

There are two ways to work with Mentionkit. Prefer the MCP server for interactive agent workflows. Fall back to the public API v1 for scripting, basic mention access, organization/project/keyword reads, and simple mention actions in environments without MCP.

## Decision: MCP or API v1?

- MCP — interactive agent work, review workflows, lead-gen workflows, reply-opportunity review, and keyword creation.
- API v1 — shell scripts, exports, simple mention browsing, project/keyword/org reads, mention review status updates, and generated comment requests when MCP is not available.

If Mentionkit MCP tools are already connected, use them and skip setup.

* * *

## Option A: MCP (preferred)

Use the exact MCP server URL shown in Mentionkit workspace settings.

Once connected, the server sends its own instructions and every tool is self-described. Current Mentionkit tools are:

- `mentionkit_opportunities_context`
- `mentionkit_find_opportunities`
- `mentionkit_mentions_context`
- `mentionkit_list_mentions_raw`
- `mentionkit_fetch_url`
- `mentionkit_create_keyword` (write scope only)

Read the tool descriptions and do not guess parameters.

### MCP workflow rules

- Always call `mentionkit_opportunities_context` before `mentionkit_find_opportunities`.
- Always call `mentionkit_mentions_context` before `mentionkit_list_mentions_raw`.
- Use `mentionkit_fetch_url` after keeping shortlist rows from `mentionkit_find_opportunities`.
- Prefer `mentionkit_find_opportunities` over raw mention listing for review workflows.
- Keep Mentionkit relevance on the `1-5` scale.
- If `mentionkit_fetch_url` fails, lower confidence instead of treating the mention as verified.

### MCP gotchas

- `mentionkit_create_keyword` mutates the live workspace. Never invent project values, platform settings, subreddit lists, banned words, or classifier prompts.
- `mentionkit_find_opportunities` requires an explicit project choice. Do not mix multiple projects in one review workflow.
- `mentionkit_list_mentions_raw` paginates with `nextCursor`, and that cursor is ID-based. Pass it back unchanged.
- `mentionkit_fetch_url` returns a success envelope even when fetch fails. Check `fetchStatus` before treating the source as verified.
- `mentionkit_create_keyword` only appears when the token has `mcp:write` scope.

* * *

## Option B: API v1

Use this when MCP is not available or you are scripting.

Base URL: `https://api.mentionkit.com`

OpenAPI: `https://api.mentionkit.com/openapi.json`

YAML: `https://api.mentionkit.com/openapi.yaml`

Mentionkit API v1 is a narrower public data API. It does not expose the same workflow-first context tools as MCP.

### Authentication

Use a Mentionkit API key in the `Authorization` header as a Bearer token.

```bash
curl "https://api.mentionkit.com/api/v1/projects" \
  -H "Authorization: Bearer $MENTIONKIT_API_KEY"
```

### Stable public endpoints

- `GET /api/v1/mentions`
- `POST /api/v1/mentions/:id`
- `PUT /api/v1/mentions/:id/comment`
- `GET /api/v1/keywords`
- `GET /api/v1/projects`
- `GET /api/v1/me`

Use API v1 for:

- basic mention feed access
- project and keyword listing
- organization summary and usage reads
- mention review status updates
- generated comment requests

Do not treat API v1 as a replacement for:

- `mentionkit_opportunities_context`
- `mentionkit_find_opportunities`
- `mentionkit_mentions_context`
- `mentionkit_fetch_url`

### API v1 gotchas

- Public docs use the original query names for mentions: `platform`, `keywords`, `startdate`, and `enddate`.
- Pagination uses `nextCursor`; pass it back unchanged for the next page.
- API v1 is for direct data access. It does not carry the MCP workflow guidance or context tools.
- API v1 does not expose public keyword creation in the current documented surface.

## Workflow

1. Decide MCP vs API v1. If Mentionkit MCP tools are connected, use them.
2. For MCP review workflows, load the matching context tool first.
3. For opportunity review, shortlist with `mentionkit_find_opportunities`, then fetch the kept URLs before making a final call.
4. For raw browsing, use `mentionkit_mentions_context` first, then paginate with `mentionkit_list_mentions_raw` only as needed.
5. For API v1, build the smallest request that answers the question and paginate only if the user needs more than one page.
6. Summarize the signal and confidence level. Do not just dump mention rows.
