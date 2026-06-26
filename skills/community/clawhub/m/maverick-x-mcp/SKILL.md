---
name: maverick-x-mcp
description: Search, read, and work with X posts, users, timelines, and search through a local XMCP wrapper. Use when the user asks about X posts, users, timelines, or search.
homepage: https://docs.x.com/tools/mcp
metadata:
  openclaw:
    emoji: "𝕏"
    requires:
      bins:
        - mcporter
        - uv
      env:
        - MAVERICK_X_MCP_ACCESS_TOKEN
        - MAVERICK_X_MCP_REFRESH_TOKEN
        - MAVERICK_X_MCP_CLIENT_ID
        - MAVERICK_X_MCP_CLIENT_SECRET
    primaryEnv: MAVERICK_X_MCP_REFRESH_TOKEN
    setup:
      script: scripts/setup.sh
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

# X

## Quick start

Always invoke through the local HTTP wrapper. The wrapper starts this skill's local XMCP server on loopback when needed, waits for readiness, and then calls `mcporter`. OAuth vault seeding happens separately through `scripts/setup.sh` before agent use.

```sh
uv run --script {baseDir}/scripts/local_http_invoke.py list maverick-x --schema
```

For structured output:

```sh
uv run --script {baseDir}/scripts/local_http_invoke.py call --output json maverick-x.<tool> key=value
```

## Safety

Write operations that post, delete posts, reply, repost, like, follow, edit, or otherwise publish externally visible X content require explicit user confirmation with the exact final text or action. Search and read tools are safe to call freely while exploring. Resolve user handles and post IDs before acting on them.

## Authentication

Credentials are provisioned at setup time by `scripts/setup.sh` (a thin delegator to `scripts/init-mcporter-oauth.sh`) and stored in mcporter's local vault. The setup hook requires these credential env vars:

- `MAVERICK_X_MCP_REFRESH_TOKEN`
- `MAVERICK_X_MCP_CLIENT_ID`
- `MAVERICK_X_MCP_CLIENT_SECRET`
- `MAVERICK_X_MCP_ACCESS_TOKEN`

For refresh-aware seeding, setup also reads optional expiry metadata env vars when the provisioner supplies them:

- `MAVERICK_X_MCP_EXPIRES_AT`
- `MAVERICK_X_MCP_EXPIRES_IN`
- `MAVERICK_X_MCP_REFRESH_TOKEN_EXPIRES_AT`

mcporter refreshes expired X access tokens through X's OAuth2 token endpoint before calling the local XMCP server. If calls keep returning HTTP 401 after retry, the OAuth grant has likely been revoked or expired; reconnect the integration.

## Data flow

Tool calls travel from the agent to mcporter, then to this skill's local XMCP server at `http://127.0.0.1:8765/mcp`. The local server forwards X API requests with the bearer token supplied on each MCP request. X sees the post, user, timeline, and search data referenced by each call. Use this skill for X-related work only; do not pass unrelated sensitive content through these tools.

## Dependencies

- **`mcporter`** ([github.com/steipete/mcporter](https://github.com/steipete/mcporter)) — MCP CLI used to invoke the local MCP server. Auto-installed via `npm install -g --ignore-scripts mcporter` if missing on PATH (see `install` spec in frontmatter). The install spec uses unpinned `mcporter` (npm `latest`); operators with strict supply-chain controls should override the install to pin a specific version.
- **`uv`** ([docs.astral.sh/uv](https://docs.astral.sh/uv/)) — runs the Python wrapper and local XMCP launcher from inline script metadata.
