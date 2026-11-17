---
name: oo-fastmoss-mcp
description: "FastMoss MCP (fastmoss.com). Use this skill for ANY FastMoss MCP request — reading, creating, updating, and deleting data. Whenever a task involves FastMoss MCP, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "FastMoss MCP"
  author: "OOMOL"
  version: "1.0.3"
  services: ["fastmoss_mcp"]
  icon: "https://static.oomol.com/logo/third-party/fastmoss_mcp.svg"
---

# FastMoss MCP

Operate **FastMoss MCP** through your OOMOL-connected account. This skill calls the `fastmoss_mcp` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected FastMoss MCP. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "fastmoss_mcp" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "fastmoss_mcp" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `ad_data_overview` — Read a video's advertising spend, ROAS and engagement over a date range.
- `ad_search` — Search advertisements by category, spend, ROAS and activity dates.
- `agency_creator_analysis` — Analyze creators associated with an MCN agency.
- `agency_product_analysis` — Analyze an MCN agency's product performance.
- `agency_product_list` — List an MCN agency's products by category and price.
- `agency_profile_overview` — Read an MCN agency's profile and performance overview.
- `agency_rank_top` — Rank MCN agencies for a completed week or month.
- `agency_search` — Search MCN agencies by name and region.
- `agency_shop_analysis` — Analyze shops associated with an MCN agency.
- `call_tool` — Call any current FastMoss MCP tool after inspecting list_tools. Arguments must match the live schema. Calls may consume FastMoss Credits; inspect behavior annotations before invoking newly added tools. [destructive]
- `creator_cargo_summary` — Read a creator's commerce performance summary.
- `creator_data_trends` — Read a creator's metric trends over a date range.
- `creator_fans_distribution` — Read a creator's audience demographics and distribution.
- `creator_product_list` — List products promoted by a creator and their sales performance.
- `creator_profile_overview` — Read a creator's profile and account overview.
- `creator_rank_top_ecommerce` — Rank commerce creators for a completed period.
- `creator_rank_top_growth` — Rank creators by growth for a completed period.
- `creator_rank_top_potential` — Rank promising creators by category and audience for a completed period.
- `creator_search` — Search creators by identity, category, audience and commerce activity.
- `creator_video_analysis` — Analyze a creator's videos over a date range.
- `credit_usage_summary` — Read the connected account's FastMoss Credits usage.
- `fastmoss_detail_url_examples` — Read FastMoss detail-page URL examples for research results.
- `list_tools` — Discover current FastMoss MCP tools, live argument schemas and behavior annotations for TikTok Shop product, creator, shop, advertising, agency and market research.
- `live_detail_analysis` — Analyze a live session's audience and commerce performance.
- `live_products_list` — List products promoted in a live session.
- `live_search` — Search live sessions by start time, audience and commerce performance.
- `market_category_analysis` — Analyze a market category by region and period.
- `market_category_author_sales_matrix` — Read the creator sales matrix for a market category.
- `market_category_ranking` — Rank market categories by performance for a completed period.
- `product_category_info` — Read the product category tree. Use search_category_by_words to resolve category names.
- `product_creator_analysis` — Analyze the creators selling a product, including audience and sales contributions.
- `product_detail_info` — Read a product's price, shop, ratings, logistics and media.
- `product_investment` — Analyze a product's advertising spend, ROAS and paid-traffic trends.
- `product_overview` — Read a product's sales channels, momentum and paid-versus-organic performance.
- `product_rank_new_listed` — Rank recently listed products by sales performance in a completed period.
- `product_rank_top_selling` — Rank bestselling products in a market or category for a completed period.
- `product_review_list` — Read one page of product reviews and buyer feedback.
- `product_sales_trend` — Read daily product GMV and units sold for a selected period.
- `product_search` — Find products by keyword, category, price, sales and fulfilment filters.
- `product_sku` — Read product SKU sales and inventory shares.
- `product_video_list` — List videos promoting a product, optionally filtered by publish time and ad traffic.
- `search_category_by_words` — Resolve category names or keywords to FastMoss category IDs.
- `search_fastmoss_documents` — Search FastMoss documentation for metrics, filters and research guidance.
- `shop_base_info` — Read a shop's profile and basic information.
- `shop_creator_analysis` — Analyze creators promoting a shop's products.
- `shop_data_trends` — Read a shop's performance trends over a date range.
- `shop_investment_analysis` — Analyze a shop's advertising investment over a date range.
- `shop_live_analysis` — Analyze live sessions associated with a shop.
- `shop_product_analysis` — Analyze a shop's products by category and listing age.
- `shop_rank_top_selling` — Rank shops by sales for a completed period.
- `shop_sale_analysis` — Analyze a shop's sales over a date range.
- `shop_search` — Search shops by name, region, category and creator relationships.
- `shop_video_analysis` — Analyze videos promoting a shop's products.
- `video_data_trends` — Read a video's performance trends over a date range.
- `video_detail_analysis` — Analyze a video's engagement and commerce performance.
- `video_script_info` — Read the script or transcript of a video.
- `video_search` — Search videos by creation time, creator, engagement and commerce activity.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change FastMoss MCP state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — FastMoss MCP is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/fastmoss_mcp
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- FastMoss MCP homepage: https://www.fastmoss.com/zh
- API documentation: https://developer.fastmoss.com/zh/docs/mcp/setup
