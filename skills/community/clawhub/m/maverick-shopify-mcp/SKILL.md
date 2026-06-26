---
name: maverick-shopify-mcp
description: Search, read, and work with Shopify products, orders, customers, and shop data through a local MCP wrapper. Use when the user asks about Shopify commerce operations.
metadata:
  openclaw:
    emoji: "🛍️"
    requires:
      bins:
        - mcporter
        - uv
      env:
        - MAVERICK_SHOPIFY_MCP_ACCESS_TOKEN
        - MAVERICK_SHOPIFY_MCP_SHOP
    primaryEnv: MAVERICK_SHOPIFY_MCP_ACCESS_TOKEN
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

# Shopify

## Quick start

This skill is a thin pass-through to a local stdio MCP server. mcporter spawns the skill's Python server on each call and passes the configured Shopify env vars to the subprocess.

```sh
mcporter --config {baseDir}/mcporter.json list maverick-shopify --schema
```

For structured output:

```sh
mcporter --config {baseDir}/mcporter.json call --output json maverick-shopify.<tool> key=value
```

## Safety

Write operations that create, publish, update, or expose products, variants, orders, customers, or externally visible product links can affect customer-facing commerce flows. Confirm clear user intent before invoking write tools — search and read tools are safe to call freely while exploring. Search products before assuming product or variant IDs, and read product and variant details before recommending or linking items.

## Authentication

The deployment harness provides a Shopify access token and shop identifier. mcporter passes them into the stdio subprocess via `mcporter.json`; the local server sends the token to Shopify as the admin API access token.

This skill does not claim a refresh-token contract for Shopify. If Shopify rejects the token, reconnect the integration so the deployment harness can provision a new access token.

## Data flow

Tool calls run locally: mcporter spawns this skill's Python MCP server as a subprocess, and that server forwards Shopify Admin API requests with the configured access token. Shopify sees the product, order, customer, and shop data referenced by each call. Use this skill for Shopify-related work only; do not pass unrelated sensitive content through these tools.

## Dependencies

- **`mcporter`** ([github.com/steipete/mcporter](https://github.com/steipete/mcporter)) — MCP CLI used to invoke the local MCP server. Auto-installed via `npm install -g --ignore-scripts mcporter` if missing on PATH (see `install` spec in frontmatter). The install spec uses unpinned `mcporter` (npm `latest`); operators with strict supply-chain controls should override the install to pin a specific version.
- **`uv`** ([docs.astral.sh/uv](https://docs.astral.sh/uv/)) — runs the Python wrapper and local MCP server from their inline dependency metadata.
