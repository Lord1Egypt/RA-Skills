---
name: maverick-monday-mcp
description: Search, read, and update Monday.com boards, workspaces, items, updates, and columns via Monday.com's hosted MCP server (https://mcp.monday.com/mcp). Use when the user asks about Monday.com boards, items, workspaces, updates, or column values.
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins:
        - mcporter
      env:
        - MAVERICK_MONDAY_MCP_ACCESS_TOKEN
    primaryEnv: MAVERICK_MONDAY_MCP_ACCESS_TOKEN
    install:
      - id: node
        kind: node
        package: mcporter
        bins:
          - mcporter
        label: Install mcporter (node)
---

# Monday.com

## How to use this skill

This skill is a thin pass-through to Monday.com's hosted MCP server at `https://mcp.monday.com/mcp`. The live server is the source of truth for what tools exist, what they're called, what arguments they take, and any per-server instructions the server publishes.

**Step 1 - Discover the live tool catalog and any server-published usage instructions.** Always run this first; do not rely on tool names from memory:

```sh
mcporter --config {baseDir}/mcporter.json list maverick-monday --schema
```

The output includes the server's `Instructions:` field, if published, and a JSON Schema for every tool's parameters. Treat this as the authoritative reference for the rest of the session.

**Step 2 - Call any tool from the catalog** using the form `maverick-monday.<tool>`:

```sh
mcporter --config {baseDir}/mcporter.json call maverick-monday.<tool> <arg>=<value> ...
```

Add `--output json` for structured output and transport-error envelopes:

```sh
mcporter --config {baseDir}/mcporter.json call --output json maverick-monday.<tool> ...
```

## Safety

Write operations that create, update, delete, archive, publish, or modify boards, items, updates, columns, and workspaces affect Monday.com data visible to the connected account. Confirm clear user intent before invoking write tools - search and read tools are safe to call freely while exploring. Resolve board and workspace IDs first, read the board's column schema before writing column values, and fetch item state before updating or commenting.

## Authentication

This skill expects `MAVERICK_MONDAY_MCP_ACCESS_TOKEN` to be set in the agent runtime environment. mcporter sends it as `Authorization: Bearer <value>` on every request.

If calls fail with auth errors, the token is invalid, expired, or revoked - re-issue and re-set `MAVERICK_MONDAY_MCP_ACCESS_TOKEN`. There is no automatic refresh; bearer tokens are static.

## Data flow

Tool calls travel to Monday.com's hosted MCP service at `https://mcp.monday.com/mcp` over HTTPS, authenticated with a bearer token. Monday.com sees the board, workspace, item, update, and column data referenced by each call. Use this skill for Monday.com-related work only; do not pass unrelated sensitive content through these tools.

## Dependencies

- **`mcporter`** ([github.com/openclaw/mcporter](https://github.com/openclaw/mcporter)) - MCP CLI used to invoke Monday.com's hosted MCP server. Auto-installed via `npm install -g --ignore-scripts mcporter` if missing on PATH (see `install` spec in frontmatter). The install spec uses unpinned `mcporter` (npm `latest`); operators with strict supply-chain controls should override the install to pin a specific version (e.g. `mcporter@<version>`).
