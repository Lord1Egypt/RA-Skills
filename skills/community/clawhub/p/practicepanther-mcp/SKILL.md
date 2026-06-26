---
name: practicepanther-mcp
description: MCP server for the PracticePanther legal practice management API. Exposes PracticePanther's REST API as read-only MCP tools.
metadata: { "openclaw": { "requires": { "bins": ["mcporter", "practicepanther-mcp"], "env": ["NODE_MCP_SECRET_KEY"] } } }
---

# PracticePanther MCP Server

Read-only MCP server for the PracticePanther legal practice management API.

## Usage

Use mcporter to interact with this server via stdio:

- **List available tools:** `mcporter list --stdio practicepanther-mcp`
- **Call a tool:** `mcporter call --stdio practicepanther-mcp <tool_name> [args]`

## Links

- **npm:** https://www.npmjs.com/package/@mjquinlan2000/practicepanther-mcp
