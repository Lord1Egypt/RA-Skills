# Mermail Composio tool contract

Read this reference when constructing Mermail MCP calls for Composio connection management, action discovery, schema inspection, execution, calendar identity, or disconnect.

## Tool map

| Tool | Role |
| --- | --- |
| `list_composio_toolkits` | Discover toolkits with `query.search`, `query.category`, `query.status`, `query.cursor`, and `query.limit` |
| `connect_composio_toolkit` | Start hosted OAuth/API-key authentication and return `redirectUrl` |
| `sync_composio_connections` | Pull provider connection state after the user finishes browser authentication |
| `list_composio_connections` | Inspect user-scoped connections and require status `ACTIVE` before execute |
| `search_composio_tools` | Find provider action slugs with `query.search`, optional `query.toolkit`, and bounded `query.limit` |
| `get_composio_tool_schema` | Return `inputSchema`, toolkit, `risk`, `allowed`, `connected`, and mode for one exact slug |
| `execute_composio_tool` | Execute one connected and allowed action with `body.slug` and `body.arguments` |
| `get_composio_calendar_account` | Return the connected Google Calendar account and email when available |
| `disconnect_composio_toolkit` | Revoke one toolkit connection using a matching destructive confirmation token |

External MCP uses these nine management tools. The in-app mailbox Assistant instead receives filtered direct provider actions for active toolkits. Do not invent direct provider tool names on the Mermail MCP surface; search, inspect, then call `execute_composio_tool`.

The Mermail CLI mirrors the same management operations under `mermail composio …`.

## Connection arguments and status

Use an exact toolkit `slug` returned by discovery. `connect_composio_toolkit` accepts optional `body.authMethod` of `oauth` or `api_key`; omit it when the hosted provider flow should choose. An optional `body.callbackUrl` must be same-origin with the Mermail app; do not invent or redirect it to a third-party origin.

The connect result returns `redirectUrl`. It is a browser-auth handoff, not proof of connection. After the user confirms completion, call `sync_composio_connections` once and then `list_composio_connections`. Require `ACTIVE` before executing provider actions.

Connections belong to `auth.user.id`. MCP OAuth acts as that OAuth user. A workspace API key acts as its creator or workspace owner, so a connection may appear under the key creator rather than another console viewer.

## Tool discovery and schema

Use a search string of at least three characters when possible. `search_composio_tools` returns the exact uppercase action slug, toolkit, risk, `allowed`, and `connected`. Search is discovery only; always call `get_composio_tool_schema` for the selected exact slug before execution.

Risk values are `read`, `write`, or `destructive`. Server mode may be `full`, `read_only`, or `off`:

- `full`: read and write actions may be allowed; destructive actions still require explicit server allowlisting.
- `read_only`: only read-risk provider actions are allowed.
- `off`: provider discovery/execution is disabled.

An explicit server allowlist or blocklist may further restrict actions. Treat the returned `allowed` value as authoritative.

## Execute contract

Use the exact live schema:

```json
{
  "body": {
    "slug": "GITHUB_LIST_ISSUES",
    "arguments": {
      "owner": "example",
      "repo": "project"
    }
  }
}
```

`body.connectedAccountId` is optional. Supply it only when the user selected an exact account returned by Mermail; never guess or expose it.

Execution requires the toolkit to be active and the action to be allowed. Typical results contain:

- `configured`: whether Mermail Composio is configured.
- `successful`: whether Composio reported success.
- `data`: redacted and bounded provider result.
- `error`: provider or execution failure summary.
- `risk`: classified action risk.

Common boundaries:

- `403`: action or execution mode is not allowed; stop.
- `404`: tool/toolkit is disabled or not found; do not work around it.
- `409`: toolkit is not connected; return to the connection workflow.
- `502`: provider execution failed; do not retry a write automatically.

## Disconnect contract

Disconnect is a destructive Mermail tool, separate from a provider action:

1. Read the exact connection.
2. Obtain explicit user approval.
3. Call `prepare_destructive_action` for `disconnect_composio_toolkit` with the exact slug arguments.
4. Call `disconnect_composio_toolkit` once with the same arguments and returned single-use, five-minute confirmation token.

Do not use `prepare_destructive_action` for `execute_composio_tool`, and never use it to override `allowed: false`.
