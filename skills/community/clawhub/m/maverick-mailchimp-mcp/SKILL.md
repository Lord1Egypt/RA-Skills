---
name: maverick-mailchimp-mcp
description: Search and read Mailchimp Marketing API audiences, members, campaigns, content, and reports through a local MCP wrapper. Use when the user asks about Mailchimp marketing data.
metadata:
  openclaw:
    emoji: "📣"
    requires:
      bins:
        - mcporter
        - uv
      env:
        - MAVERICK_MAILCHIMP_MCP_ACCESS_TOKEN
        - MAVERICK_MAILCHIMP_MCP_API_BASE
    primaryEnv: MAVERICK_MAILCHIMP_MCP_ACCESS_TOKEN
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

# Mailchimp

## Quick start

This skill is a thin pass-through to a local stdio MCP server for the Mailchimp Marketing API. mcporter spawns the skill's Python server on each call. The live MCP schema is the source of truth for what tools exist, what they're called, and what arguments they take.

```sh
mcporter --config {baseDir}/mcporter.json list maverick-mailchimp --schema
```

For structured output:

```sh
mcporter --config {baseDir}/mcporter.json call --output json maverick-mailchimp.<tool> key=value
```

## Safety

This first implementation exposes read-only tools. Use them freely to inspect audiences, members, campaigns, campaign content, and reports. If write tools are added later, confirm clear user intent for the exact audience, member, campaign, tag, or schedule before invoking them.

## Authentication

Maverick provisions these env vars from the connected Mailchimp OAuth grant:

- `MAVERICK_MAILCHIMP_MCP_ACCESS_TOKEN`
- `MAVERICK_MAILCHIMP_MCP_API_BASE`

Mailchimp Marketing access tokens do not use refresh tokens in this skill. If calls return auth errors, reconnect the Mailchimp integration so Maverick can provision a fresh access token and API base.

## Data flow

Tool calls run locally: mcporter spawns this skill's Python MCP server as a subprocess, and that server forwards Mailchimp Marketing API requests with the OAuth bearer token. Mailchimp sees the audience, member, campaign, content, and report data referenced by each call. Use this skill for Mailchimp-related work only; do not pass unrelated sensitive content through these tools.

## Dependencies

- **`mcporter`** ([github.com/steipete/mcporter](https://github.com/steipete/mcporter)) - MCP CLI used to invoke the local MCP server. Auto-installed via `npm install -g --ignore-scripts mcporter` if missing on PATH (see `install` spec in frontmatter). The install spec uses unpinned `mcporter` (npm `latest`); operators with strict supply-chain controls should override the install to pin a specific version.
- **`uv`** ([docs.astral.sh/uv](https://docs.astral.sh/uv/)) - runs the Python wrapper and local MCP server from their inline dependency metadata.
