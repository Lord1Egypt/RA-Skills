# MCP Integration - Instacart

## What MCP Covers

Instacart's current MCP server exposes two tools:
- `create-recipe`
- `create-shopping-list`

That makes MCP ideal for LLM-native workflows that only need page creation and do not need custom retailer lookup or deeper REST diagnostics.

## Server URLs

| Environment | URL |
|-------------|-----|
| Development | `https://mcp.dev.instacart.tools/mcp` |
| Production | `https://mcp.instacart.com/mcp` |

## Validation Flow

1. Connect with MCP Inspector using Streamable HTTP.
2. Point to the development URL first.
3. Authenticate with a valid Developer Platform key.
4. Run `List Tools`.
5. Confirm both create tools are visible.

If the tools are not listed, do not continue with the agent integration.

## When MCP Is Better

- fast agent integration
- natural-language handoff to Instacart page creation
- minimal custom request assembly

## When REST Is Better

- retailer lookup
- request logging and payload diffing
- custom retry behavior
- cache-keyed idempotency
- unsupported or future endpoints

## Operating Rule

Default to MCP only when its tool surface fully covers the task. The moment the workflow needs retailer discovery, launch diagnostics, or tighter request control, switch to REST.
