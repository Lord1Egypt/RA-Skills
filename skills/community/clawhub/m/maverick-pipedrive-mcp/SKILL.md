---
name: maverick-pipedrive-mcp
description: Search, read, and update Pipedrive deals, contacts, organizations, activities, pipelines, and sales workflows through a local MCP wrapper. Use when the user asks about Pipedrive CRM work.
metadata:
  openclaw:
    emoji: "💼"
    requires:
      bins:
        - mcporter
        - uv
      env:
        - MAVERICK_PIPEDRIVE_MCP_ACCESS_TOKEN
        - MAVERICK_PIPEDRIVE_MCP_REFRESH_TOKEN
        - MAVERICK_PIPEDRIVE_MCP_CLIENT_ID
        - MAVERICK_PIPEDRIVE_MCP_CLIENT_SECRET
        - MAVERICK_PIPEDRIVE_MCP_API_BASE
    primaryEnv: MAVERICK_PIPEDRIVE_MCP_REFRESH_TOKEN
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

# Pipedrive

## Quick start

This skill is a thin pass-through to a local stdio MCP server. mcporter spawns the skill's Python server on each call, refreshes the OAuth access token when needed, and injects the fresh token into the server env.

```sh
mcporter --config {baseDir}/mcporter.json list maverick-pipedrive --schema
```

For structured output:

```sh
mcporter --config {baseDir}/mcporter.json call --output json maverick-pipedrive.<tool> key=value
```

## Safety

Write operations that create records, update properties, change deal stages, mark activities done, create notes, or delete data modify Pipedrive CRM state visible to the connected account. Confirm clear user intent before invoking write tools — search and read tools are safe to call freely while exploring. Search deals, people, organizations, and activities before assuming IDs, and read current deal stage, owner, value, and activity history before updating.

## Authentication

Credentials are provisioned at setup time by `scripts/setup.sh` (a thin delegator to `scripts/init-mcporter-oauth.sh`) and stored in mcporter's local vault. The setup hook requires these credential env vars:

- `MAVERICK_PIPEDRIVE_MCP_REFRESH_TOKEN`
- `MAVERICK_PIPEDRIVE_MCP_CLIENT_ID`
- `MAVERICK_PIPEDRIVE_MCP_CLIENT_SECRET`
- `MAVERICK_PIPEDRIVE_MCP_ACCESS_TOKEN`
- `MAVERICK_PIPEDRIVE_MCP_API_BASE`

For refresh-aware seeding, setup also reads optional expiry metadata env vars when the provisioner supplies them:

- `MAVERICK_PIPEDRIVE_MCP_EXPIRES_AT`
- `MAVERICK_PIPEDRIVE_MCP_EXPIRES_IN`
- `MAVERICK_PIPEDRIVE_MCP_REFRESH_TOKEN_EXPIRES_AT`

mcporter refreshes expired Pipedrive access tokens through Pipedrive's token endpoint before spawning the stdio server, then injects the token into `MAVERICK_PIPEDRIVE_MCP_ACCESS_TOKEN`. If calls keep returning auth errors after retry, the OAuth grant has likely been revoked or expired; reconnect the integration.

## Data flow

Tool calls run locally: mcporter spawns this skill's Python MCP server as a subprocess, and that server forwards Pipedrive API requests with the refreshed OAuth bearer token. Pipedrive sees the deal, person, organization, activity, pipeline, and sales-workflow data referenced by each call. Use this skill for Pipedrive-related work only; do not pass unrelated sensitive content through these tools.

## Dependencies

- **`mcporter`** ([github.com/steipete/mcporter](https://github.com/steipete/mcporter)) — MCP CLI used to invoke the local MCP server. Auto-installed via `npm install -g --ignore-scripts mcporter` if missing on PATH (see `install` spec in frontmatter). The install spec uses unpinned `mcporter` (npm `latest`); operators with strict supply-chain controls should override the install to pin a specific version.
- **`uv`** ([docs.astral.sh/uv](https://docs.astral.sh/uv/)) — runs the Python wrapper and local MCP server from their inline dependency metadata.
