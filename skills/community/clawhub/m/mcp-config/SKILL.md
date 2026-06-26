---
name: mcp-config
metadata:
  author: es6kr
  version: "0.1.2"
description: |
  MCP server configuration and diagnostics. add - add server (scope selection + registration) [add.md], move - change server scope (project→local, local→user) [move.md], format - JSON format reference (differences per agent) [format.md], catalog - list of commonly used servers [catalog.md], diagnostics - connection failure diagnosis and troubleshooting [diagnostics.md].
  Use when: "add MCP", "mcp-config", "MCP server config", "add context7", "MCP format", "MCP server list", "move MCP", "MCP scope", "scope change", "MCP connection failed", "MCP error", "Failed to reconnect", "code-mode not working", "MCP server issue".
---

# MCP Server Configuration

Correctly add and manage MCP servers in the `.mcp.json` file.

## Topics

| Topic | Description | Guide |
|-------|-------------|-------|
| add | Add server (scope selection + registration + validation) | [add.md](./add.md) |
| catalog | Catalog of commonly used MCP servers | [catalog.md](./catalog.md) |
| diagnostics | Connection failure diagnosis and troubleshooting | [diagnostics.md](./diagnostics.md) |
| format | JSON format reference (differences per agent) | [format.md](./format.md) |
| move | Change server scope (project→local, local→user) | [move.md](./move.md) |

## Quick Reference

```text
"add MCP"              → add topic (scope selection → registration)
"add context7"         → add topic + refer to catalog for config
"move MCP"             → move topic (scope change: remove + re-add)
"MCP format"           → format topic (JSON differences per agent)
"MCP server list"      → catalog topic
"MCP connection failed" → diagnostics topic (connection troubleshooting)
"Failed to reconnect"  → diagnostics topic
```

## Core Rules

- **New MCP server = register as a separate key** (do not put inside an existing server's `env`)
- **Scope selection AskUserQuestion required** (global vs project, agent selection)
- **Antigravity requires `transport: "stdio"`**
