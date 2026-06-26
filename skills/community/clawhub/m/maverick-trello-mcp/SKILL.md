---
name: maverick-trello-mcp
description: Search, read, and update Trello boards, lists, cards, checklists, members, and comments through a local MCP wrapper. Use when the user asks about Trello task workflows.
metadata:
  openclaw:
    emoji: "🗂️"
    requires:
      bins:
        - mcporter
        - uv
      env:
        - MAVERICK_TRELLO_MCP_ACCESS_TOKEN
        - MAVERICK_TRELLO_MCP_API_KEY
    primaryEnv: MAVERICK_TRELLO_MCP_ACCESS_TOKEN
    install:
      - id: node
        kind: node
        package: mcporter
        bins:
          - mcporter
        label: Install mcporter (node)
      - id: brew-uv
        kind: brew
        formula: uv
        bins:
          - uv
        label: Install uv (brew)
---

# Trello

## Quick start

This skill is a thin pass-through to a local stdio MCP server. mcporter spawns the skill's Python server on each call and passes the configured Trello env vars to the subprocess.

```sh
mcporter --config {baseDir}/mcporter.json list maverick-trello --schema
```

For structured output:

```sh
mcporter --config {baseDir}/mcporter.json call --output json maverick-trello.<tool> key=value
```

## Safety

Write operations that create, move, update, archive, delete, assign, comment on, or checklist-edit Trello cards modify shared board state. Confirm clear user intent before invoking write tools, and read current board/list/card state before changing it.

## Authentication

The deployment harness provides a Trello access token and API key. mcporter passes them into the stdio subprocess via `mcporter.json`; the local server sends Trello API requests with the configured API key and token.

This skill does not claim a refresh-token contract for Trello. If Trello rejects the token, reconnect the integration so the deployment harness can provision a new access token.

## Data flow

Tool calls run locally: mcporter spawns this skill's Python MCP server as a subprocess, and that server forwards Trello API requests with the configured API key and token. Trello sees the board, list, card, checklist, member, and comment data referenced by each call. Use this skill for Trello-related work only; do not pass unrelated sensitive content through these tools.

## Dependencies

- **`mcporter`** ([github.com/steipete/mcporter](https://github.com/steipete/mcporter)) — MCP CLI used to invoke the local MCP server. Auto-installed via `npm install -g --ignore-scripts mcporter` if missing on PATH (see `install` spec in frontmatter). The install spec uses unpinned `mcporter` (npm `latest`); operators with strict supply-chain controls should override the install to pin a specific version.
- **`uv`** ([docs.astral.sh/uv](https://docs.astral.sh/uv/)) — runs the Python wrapper and local MCP server from their inline dependency metadata.
