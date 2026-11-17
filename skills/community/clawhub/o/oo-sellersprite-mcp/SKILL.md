---
name: oo-sellersprite-mcp
description: "SellerSprite MCP (open.sellersprite.com). Use this skill for ANY SellerSprite MCP request — reading, creating, and updating data. Whenever a task involves SellerSprite MCP, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SellerSprite MCP"
  author: "OOMOL"
  version: "1.0.5"
  services: ["sellersprite_mcp"]
  icon: "https://static.oomol.com/logo/third-party/sellersprite_mcp.svg"
---

# SellerSprite MCP

Operate **SellerSprite MCP** through your OOMOL-connected account. This skill calls the `sellersprite_mcp` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SellerSprite MCP. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sellersprite_mcp" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sellersprite_mcp" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `aba_research_monthly` — Research monthly Amazon Brand Analytics keywords using rank, search, click, conversion, and market-pattern filters.
- `aba_research_trend` — Retrieve weekly or monthly Amazon Brand Analytics trend data for one keyword.
- `aba_research_weekly` — Research weekly Amazon Brand Analytics keywords using rank, search, click, conversion, and market-pattern filters.
- `asin_competitor` — Retrieve competing products identified for one Amazon ASIN.
- `asin_coupon_trend` — Retrieve the historical coupon trend for one Amazon ASIN.
- `asin_detail` — Retrieve SellerSprite product, sales, ranking, price, review, and seller data for one Amazon ASIN.
- `asin_detail_with_coupon_trend` — Retrieve ASIN details together with the product's historical coupon trend.
- `asin_prediction` — Retrieve SellerSprite sales predictions for one Amazon ASIN.
- `asin_sales_trend` — Retrieve the historical sales trend for one Amazon ASIN.
- `bsr_prediction` — Estimate Amazon product sales from a Best Sellers Rank and top-level category.
- `call_tool` — Call a current SellerSprite MCP tool with JSON arguments after inspecting its live schema and behavior annotations with list_tools. [write]
- `competitor_lookup` — Find competing Amazon products by marketplace, category, brand, seller, ASIN, keyword, and product filters.
- `google_trend` — Retrieve Google Trends interest data for an Amazon marketplace keyword.
- `keepa_info` — Retrieve SellerSprite's Keepa-style historical product trend data for one Amazon ASIN.
- `keyword_conversion` — Analyze Amazon keyword search, click, purchase, conversion, advertising, price, and budget performance.
- `keyword_miner` — Discover related Amazon keywords using search volume, purchase, competition, relevancy, PPC, price, and review filters.
- `keyword_order` — Reverse-search the weekly or monthly Amazon keywords that generated orders for selected ASINs.
- `keyword_research` — Research Amazon keywords using search, purchase, competition, price, review, growth, PPC, and demand filters.
- `keyword_research_trends` — Retrieve the historical SellerSprite trend for one Amazon keyword.
- `list_tools` — Discover the current SellerSprite Amazon research and market-data MCP tools with their live input schemas and behavior annotations.
- `market_brand_concentration` — Retrieve brand concentration for one Amazon category market.
- `market_ebc_distribution` — Retrieve the A+ content and video distribution for one Amazon category market.
- `market_listing_date_distribution` — Retrieve the listing-age distribution for one Amazon category market.
- `market_listing_trend_distribution` — Retrieve Amazon market listing-trend distribution data using the supplied optional market filters.
- `market_price_distribution` — Retrieve the price distribution for one Amazon category market.
- `market_product_concentration` — Retrieve product concentration for one Amazon category market.
- `market_product_demand_trend` — Retrieve the product-demand trend for one Amazon category market.
- `market_rating_distribution` — Retrieve the star-rating distribution for one Amazon category market.
- `market_ratings_count_distribution` — Retrieve the review-count distribution for one Amazon category market.
- `market_research` — Research Amazon categories and market segments using demand, competition, concentration, fulfillment, seller, and new-product filters.
- `market_research_statistics` — Retrieve summary statistics for one Amazon category market.
- `market_seller_concentration` — Retrieve seller concentration for one Amazon category market.
- `market_seller_country_distribution` — Retrieve the seller-country distribution for one Amazon category market.
- `market_seller_type_concentration` — Retrieve the fulfillment and seller-type distribution for one Amazon category market.
- `product_node` — Find Amazon category nodes by marketplace, category path, keyword, or historical month.
- `product_research` — Research Amazon products using sales, revenue, price, ranking, review, fulfillment, brand, seller, and category filters.
- `review` — Retrieve Amazon reviews for one ASIN with optional star-rating and review-type filters.
- `trademark_country_list` — Retrieve the countries and trademark offices covered by SellerSprite's global trademark database.
- `trademark_detail` — Retrieve one global trademark record by trademark office and SellerSprite brand ID.
- `trademark_list` — Search SellerSprite's global trademark records by text, office, brand, status, applicant, class, and year filters.
- `trademark_stats` — Retrieve aggregate global trademark statistics for search text and selected trademark offices.
- `traffic_extend` — Expand the traffic keywords shared by a set of Amazon ASINs using search, purchase, competition, and conversion filters.
- `traffic_keyword` — Retrieve the search and conversion keywords that drive traffic to one Amazon ASIN.
- `traffic_keyword_stat` — Retrieve aggregate traffic-keyword statistics for one Amazon ASIN.
- `traffic_listing` — Retrieve Amazon listings related to selected ASINs by the requested traffic relationship types.
- `traffic_listing_stat` — Retrieve aggregate related-listing traffic statistics for selected Amazon ASINs.
- `traffic_source` — Trace Amazon keyword traffic from a query to the listings receiving that traffic.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SellerSprite MCP state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SellerSprite MCP is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/sellersprite_mcp
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- SellerSprite MCP homepage: https://open.sellersprite.com/mcp
- API documentation: https://open.sellersprite.com/mcp/16
