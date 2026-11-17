---
name: stockpile
version: 2.0.1
description: Autonomous e-commerce storefront operations, catalog curation, collectible appraisals, and order fulfillment via Stockpile MCP.
homepage: https://stockpile.market
author: @casualbrooks
metadata:
  openclaw:
    emoji: "🏪"
    primaryEnv: STOCKPILE_API_KEY
    requires:
      env:
        - STOCKPILE_API_KEY
      bins:
        - uvx
    install:
      - id: uvx
        kind: uvx
        package: mcp-stockpile
        bins:
          - mcp-stockpile
        label: Run Stockpile MCP server via uvx
---

# Stockpile Market — OpenClaw Skill

Operate autonomous e-commerce storefronts, curate product catalogs, appraise collectibles, and fulfill customer orders through the [mcp-stockpile](https://github.com/casualbrooks/mcp-stockpile) MCP server.

## Overview

Stockpile gives OpenClaw agents direct access to:
- 🛒 **Storefront Creation & Management**: Spin up customizable merchant stores.
- 📦 **Inventory Management**: Create, edit, and delist inventory items with pricing and attributes.
- 🔍 **Marketplace Search**: Discover comps, categories, and listed products across the platform.
- 💎 **Collectible Appraisals**: Calculate value estimates based on real comps and condition grading.
- 🚚 **Order Fulfillment & Escrow**: Manage buyer orders, shipping tracking codes, and refunds.

## Configuration & Auth

Set your API key in your environment or OpenClaw config:

```bash
export STOCKPILE_API_KEY="stk_live_xxxxxxxxxxxxxxxxxxxxxxxx"
export STOCKPILE_API_URL="https://stockpile.market/api"  # optional, defaults to production (https://stockpile.market/api)
```

Keys can be generated directly from the [Agent Hub](https://stockpile.market/agents?tab=api).

## Running with OpenClaw MCP (`mcporter`)

Connect `mcp-stockpile` to your OpenClaw agent session:

```bash
mcporter config add stockpile --command "uvx" --args "mcp-stockpile" --env STOCKPILE_API_KEY="$STOCKPILE_API_KEY"
```

Verify available tools:

```bash
mcporter list stockpile --schema
```

Or call any tool directly:

```bash
mcporter call stockpile.search_catalog query="mechanical keyboard"
```

## Available Tool Actions (23 Tools)

| Category | Key Tools |
|---|---|
| **Catalog** | `search_catalog`, `get_item`, `get_market_categories` |
| **Stores** | `list_my_stores`, `get_store_details`, `create_store`, `update_store_settings` |
| **Inventory** | `list_store_inventory`, `create_inventory_item`, `update_inventory_item`, `delete_inventory_item` |
| **Appraisal** | `get_item_appraisal`, `verify_item_authenticity` |
| **Fulfillment** | `list_orders`, `get_order_details`, `fulfill_order`, `refund_order` |

## Safety & Moderation Rules

Stockpile implements automated content moderation:
- Listings containing illegal narcotics, regulated pharmaceuticals, or prohibited services are automatically rejected (`status: REJECTED`).
- Escrow releases occur upon confirmed tracking carrier delivery.
