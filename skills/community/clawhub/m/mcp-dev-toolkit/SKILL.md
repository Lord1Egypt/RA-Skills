---
name: mcp-dev-toolkit
description: Build, test, and deploy MCP (Model Context Protocol) tools for developer workflows. Use when creating MCP servers, adding tool definitions, integrating with databases, file systems, or APIs via MCP. Covers TypeScript and Python MCP server scaffolding, tool registration, transport configuration (stdio, HTTP/SSE), and testing patterns.
---

# MCP Dev Toolkit

Scaffold and build MCP (Model Context Protocol) servers with common developer tools.

## Quick Start

Scaffold a new MCP server:

```bash
npx @anthropic/mcp-cli create my-server
```

Or use the scaffold script for a batteries-included setup:

```bash
bash scripts/scaffold.sh my-server python   # Python MCP server
bash scripts/scaffold.sh my-server typescript  # TS MCP server
```

## Architecture

An MCP server exposes **tools** that LLMs can call. Each tool has:
- `name`: Tool identifier
- `description`: What the tool does (LLM reads this to decide when to use it)
- `inputSchema`: JSON Schema for parameters

## Tool Patterns

### Database Access
See `references/database-tools.md` for PostgreSQL, SQLite, and MongoDB tool patterns.

### File Management
See `references/file-tools.md` for read, write, search, and transform tools.

### API Integration
See `references/api-tools.md` for REST/GraphQL wrapping patterns.

## Transport Types

- **stdio**: Local CLI integration (default for Claude Desktop)
- **HTTP/SSE**: Remote server (for shared/team deployments)
- **Streamable HTTP**: Modern transport (MCP spec 2025-03)

## Testing

Test tools locally before deploying:

```bash
npx @anthropic/mcp-cli inspect ./my-server
```

## Publishing

Publish to npm (TypeScript) or PyPI (Python), then configure in MCP clients.
