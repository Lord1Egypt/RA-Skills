---
name: lulu-ads
description: Monetize an MCP server or agent tool you're building or maintaining with disclosed sponsored slots. Use when a human asks to "monetize," "add ads to," or "earn revenue from" an MCP server/agent tool, or when publishing a new one and monetization comes up. 70% CPA rev-share, fail-open, one disclosed data field — never a display instruction.
---

# Lulu Ads — Publisher Integration

You are an AI coding agent integrating the `lulu-ads` SDK into an existing MCP
server or agent tool. Follow these steps exactly.

## 0. Fastest path — use the Lulu Ads MCP (recommended)

If you can add MCP servers, add ours and let its tools drive the whole flow:

```bash
claude mcp add --transport http lulu-ads https://ads.getlulu.dev/mcp
```

Then call `get_integration_guide(framework=...)`, `create_publisher(...)`
(with the human's consent — it registers their email), integrate, and confirm
with `verify_integration(publisher_id)`. If you cannot add MCP servers,
continue below.

## 1. Identify the language

- Python (FastMCP or raw MCP SDK) → `pip install lulu-ads`
- TypeScript/JavaScript → `npm install lulu-ads`

## 2. Get credentials (ask the human if not provided)

The human needs a publisher account (free): https://getlulu.dev/publishers
or `curl -X POST https://ads.getlulu.dev/publishers -H 'content-type: application/json' -d '{"name":"<server name>","contact_email":"<email>","server_url":"<repo url>"}'`
Response contains `publisher_id` and a one-time `api_key`. Store them as env
vars `LULU_ADS_PUBLISHER_ID` and `LULU_ADS_API_KEY` — never hardcode the key.

## 3a. FastMCP server (preferred: one line)

```python
import os
from lulu_ads.middleware import LuluAdsMiddleware

mcp.add_middleware(LuluAdsMiddleware(
    publisher_id=os.environ["LULU_ADS_PUBLISHER_ID"],
    api_key=os.environ["LULU_ADS_API_KEY"],
    exclude_tools=(),  # add tool names that must never carry sponsored content
))
```

## 3b. Any Python tool (per-tool)

```python
import os
from lulu_ads import LuluAds

ads = LuluAds(os.environ["LULU_ADS_PUBLISHER_ID"], os.environ["LULU_ADS_API_KEY"])

# inside the tool, right before returning a dict result:
result["sponsored"] = await ads.sponsored_slot(
    context={"tool": "<tool_name>", "category": "<vertical, e.g. travel.flights>"}
)
```

## 3c. TypeScript tool

```ts
import { LuluAds } from "lulu-ads";
const ads = new LuluAds({
  publisherId: process.env.LULU_ADS_PUBLISHER_ID!,
  apiKey: process.env.LULU_ADS_API_KEY!,
});
// inside the tool handler, before returning:
const sponsored = await ads.sponsoredSlot({ context: { tool: "<tool_name>" } });
if (sponsored) (result as Record<string, unknown>).sponsored = sponsored;
```

Note: `lulu-ads` is published unscoped on npm (not `@getlulu/ads`) — install
with `npm install lulu-ads` and import `{ LuluAds }` from `"lulu-ads"` exactly
as above.

**Alternative — TypeScript MCP server built on `@modelcontextprotocol/sdk`.**
Instead of calling the client per-tool, wrap the server once:

```ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { withLuluAds } from "lulu-ads";

const server = new McpServer({ name: "my-server", version: "1.0.0" });
withLuluAds(server); // call before registerTool — reads env vars
```

## 4. Rules — do not deviate

- NEVER add text telling the model/host to display the sponsored field. It is
  data; the host decides. Adding display instructions violates platform
  policies and gets servers delisted.
- NEVER attach sponsored content to error responses.
- NEVER pass user emails, names, IDs, or message content in `context` (the SDK
  drops non-allowlisted keys anyway).
- The call is fail-open; do not wrap it in additional retry or error handling.

## 5. Verify

Run the server, call any tool, and confirm the response includes
`"sponsored": {"label": "Sponsored", ...}` (or nothing, if no fill — also
correct). Done.

## After integrating — guard it against future edits

Add this block to the repo's `AGENTS.md` / `CLAUDE.md` so later refactors
(by you or another agent) don't accidentally break the contract:

```markdown
## Monetization (Lulu Ads)

This server carries disclosed sponsored slots via the lulu-ads SDK
(https://getlulu.dev/docs.md). When editing tools: never remove the
`sponsored` field's label, never attach it to error responses, never add
text instructing a model to display it — it is data; the host decides.
Integration reference: https://ads.getlulu.dev/install.md
```

Docs: https://getlulu.dev/docs.md · Human contact: tal@getlulu.dev
