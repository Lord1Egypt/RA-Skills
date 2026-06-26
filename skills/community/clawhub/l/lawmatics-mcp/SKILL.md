---
name: lawmatics-mcp
description: MCP server for the Lawmatics legal CRM API. Exposes Lawmatics' REST API as read-only MCP tools.
metadata: { "openclaw": { "requires": { "bins": ["mcporter", "lawmatics-mcp"], "env": ["NODE_MCP_SECRET_KEY"] } } }
---

# Lawmatics MCP Server

Read-only MCP server for the Lawmatics legal CRM API.

## Usage

Use mcporter to interact with this server via stdio:

- **List available tools:** `mcporter list --stdio lawmatics-mcp`
- **Call a tool:** `mcporter call --stdio lawmatics-mcp <tool_name> [args]`

## Links

- **npm:** https://www.npmjs.com/package/@mjquinlan2000/lawmatics-mcp
