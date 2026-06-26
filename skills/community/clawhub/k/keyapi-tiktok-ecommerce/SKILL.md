---
name: keyapi-tiktok-ecommerce
description: Comprehensive TikTok Shop market intelligence — analyze products, shops, and categories with GMV, sales trends, reviews, creator attribution, and competitive ranking data across the full e-commerce ecosystem.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"🛒"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-tiktok-ecommerce

> Comprehensive TikTok Shop market intelligence — analyze products, shops, categories, pricing, GMV, reviews, and competitive dynamics across the entire e-commerce ecosystem.

This skill provides deep market intelligence on TikTok Shop using the KeyAPI MCP service. It covers the full e-commerce data spectrum: individual product analytics, shop-level performance, category hierarchy navigation, creator-driven sales attribution, and live-stream commerce data — all backed by large-scale historical datasets.

Use this skill when you need to:
- Research product opportunities by analyzing sales trends, GMV, pricing, and competition
- Evaluate specific products or shops with comprehensive performance metrics
- Understand TikTok Shop category structures and identify high-growth niches
- Analyze customer reviews and sentiment for product intelligence
- Identify top shops and products in a category for competitive benchmarking
- Attribute sales to specific creators or live-stream events

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **KEYAPI_TOKEN** | A valid API token from [keyapi.ai](https://keyapi.ai/). If you don't have one, register at the site to obtain your free token. Set it as an environment variable: `export KEYAPI_TOKEN=your_token_here` |
| **Node.js** | v18 or higher |
| **Dependencies** | Run `npm install` in the skill directory to install `@modelcontextprotocol/sdk` |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## MCP Server Configuration

All tool calls in this skill target the KeyAPI MCP server:

```
Server URL : https://mcp.keyapi.ai
Auth Header: Authorization: Bearer $KEYAPI_TOKEN
```

**Setup (one-time):**

```bash
# 1. Install dependencies
npm install

# 2. Set your API token (get one free at https://keyapi.ai/)
export KEYAPI_TOKEN=your_token_here

# 3. List all available tools to verify the connection
node scripts/run.js --list-tools
```

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Analysis Scenarios

### Product Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Resolve product_id from a TikTok Shop share link | `get_product_id_from_share_link` | Entry point when user provides a product URL |
| Get real-time product details (price, stock, seller) | `get_product_detail` | Live product snapshot |
| Read customer reviews for a product | `get_product_reviews` | Voice-of-customer, review sentiment |
| Search and filter products with analytics metrics | `product_list_analytics` | Market scan, product opportunity discovery |
| Deep analytics on one or more products (sales, trends, creators) | `product_detail_analytics` | Comprehensive product performance audit |
| Historical sales volume and GMV trends for a product | `product_trends_analytics` | Trend analysis, seasonality detection |
| Aggregated historical review data and rating distribution | `product_reviews_analytics` | Reputation analysis, quality signals |
| Creators who promoted a product and their performance | `product_creators_analytics` | Creator attribution, partnership discovery |
| Videos associated with a product and their conversions | `product_videos_analytics` | Content-commerce attribution |
| Live streams that featured a product | `product_livestreams_analytics` | Live commerce performance |
| Ranked product list by sales, GMV, or other metrics | `product_ranking_analytics` | Top-N products in category, competitive ranking |
| Find visually similar products using an image | `product_image_search_analytics` | Visual search, competitor product matching |

### Shop Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Get live product listings from a specific shop | `get_shop_products` | Real-time shop catalog snapshot |
| Search and filter shops with analytics data | `shop_list_analytics` | Shop discovery and shortlisting |
| Comprehensive shop performance audit | `shop_detail_analytics` | GMV history, product mix, creator network |
| Historical GMV and sales trends for a shop | `shop_trends_analytics` | Shop growth trajectory |
| Product list for a shop with sales analytics | `shop_products_analytics` | Shop's product performance breakdown |
| Creators affiliated with a shop and their contributions | `shop_creators_analytics` | Creator network and revenue attribution |
| Videos promoting a shop's products | `shop_videos_analytics` | Video commerce effectiveness |
| Historical live streams for a shop | `shop_livestreams_analytics` | Live commerce history and GMV |
| Ranked shop list by GMV, product count, or sales | `shop_ranking_analytics` | Top shops in category, competitive landscape |

### Category Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| List top-level product categories | `primary_categories_analytics` | Category hierarchy entry point |
| List subcategories under a primary category | `secondary_categories_analytics` | Drill-down to L2 categories |
| List subcategories under a secondary category | `tertiary_categories_analytics` | Drill-down to L3 categories |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify the Research Objective and Select Nodes

Clarify the user's goal and identify the appropriate entry point and supporting nodes.

**Common entry points:**

- **User provides a product share link** → Start with `get_product_id_from_share_link` to resolve `product_id`.
- **User provides a product name or keyword** → Use `product_list_analytics` to discover matching products.
- **User asks about a category** → Resolve the full category hierarchy first (see Step 1a below).
- **User provides a shop name or ID** → Use `shop_list_analytics` or `shop_detail_analytics`.
- **Competitive market analysis** → Combine `product_ranking_analytics` + `shop_ranking_analytics` + category filters.

**Step 1a — Resolve Category IDs**

> **⚠️ When the user asks about a product category or wants to filter by category, always resolve the full category hierarchy first:**
>
> 1. Call `primary_categories_analytics` → obtain `category_id` (L1)
> 2. Call `secondary_categories_analytics` with `category_id` → obtain `category_l2_id` (L2)
> 3. Call `tertiary_categories_analytics` with `category_l2_id` → obtain `category_l3_id` (L3)
>
> Use the appropriate level of category ID as a filter in subsequent product or shop queries.

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters and valid values:

```bash
node scripts/run.js --schema <tool_name>

# Examples
node scripts/run.js --schema product_list_analytics
node scripts/run.js --schema get_product_id_from_share_link
```

For analytics nodes, pay particular attention to filter parameters such as `category_id`, `category_l2_id`, `category_l3_id`, `region`, `min_spu_avg_price`, `max_spu_avg_price`, `product_sort_field`, `sort_type`, and `page_num`/`page_size`.

### Step 3 — Call APIs and Cache Results Locally

Execute the required tool calls and persist all responses to the local cache.

**Calling a tool (using `scripts/run.js`):**

```bash
# Single page call — result is cached automatically
node scripts/run.js --tool <tool_name> --params '<json_args>' --pretty

# Fetch all pages at once (auto-pagination)
node scripts/run.js --tool <tool_name> --params '<json_args>' --all-pages --page-size 50

# Force a fresh call, skip cache
node scripts/run.js --tool <tool_name> --params '<json_args>' --no-cache
```

**Example — resolve product_id from share link:**

```bash
node scripts/run.js --tool get_product_id_from_share_link \
  --params '{"share_url":"https://www.tiktok.com/t/ZPH7PbVhQDwt7-vS8eu/"}' --pretty
```

**Example — get product analytics (all pages):**

```bash
node scripts/run.js --tool product_list_analytics \
  --params '{"region":"US","category_id":"600001"}' \
  --all-pages
```

**Pagination for analytics endpoints:**

All `*_analytics` endpoints use `page_num` (1-indexed) and `page_size` (max 10). `run.js` injects these automatically if not specified. Use `--all-pages` to iterate all pages automatically.

```
--page-num 1  --page-size 10   → first page (default)
--all-pages                    → all pages merged into one result
```

**Cache directory structure:**

```
.keyapi-cache/
├── products/
│   └── {product_id}/
│       ├── detail.json              # get_product_detail / product_detail_analytics
│       ├── reviews.json             # get_product_reviews / product_reviews_analytics
│       ├── trends.json              # product_trends_analytics
│       ├── creators.json            # product_creators_analytics
│       ├── videos.json              # product_videos_analytics
│       └── livestreams.json         # product_livestreams_analytics
├── shops/
│   └── {shop_id}/
│       ├── detail.json              # shop_detail_analytics
│       ├── products.json            # get_shop_products / shop_products_analytics
│       ├── creators.json            # shop_creators_analytics
│       ├── videos.json              # shop_videos_analytics
│       ├── livestreams.json         # shop_livestreams_analytics
│       └── trends.json              # shop_trends_analytics
├── categories/
│   ├── primary.json                 # primary_categories_analytics
│   ├── secondary_{category_id}.json # secondary_categories_analytics
│   └── tertiary_{category_l2_id}.json # tertiary_categories_analytics
├── searches/
│   ├── products/
│   │   └── {md5_of_query_params}.json  # product_list_analytics
│   └── shops/
│       └── {md5_of_query_params}.json  # shop_list_analytics
└── rankings/
    ├── products_{params_hash}.json   # product_ranking_analytics
    └── shops_{params_hash}.json      # shop_ranking_analytics
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists for the given entity and node. If a valid cache file exists, load from disk and skip the API call. Category data is especially stable and should be aggressively cached.

**Cover image processing:**

After each API call, scan all response image URLs. If any URL's host matches `echosell-images.tos-ap-southeast-1.volces.com`, collect those URLs and call `batch_download_cover_images` in a single batch request. Replace the original URLs in your working dataset with the converted URLs returned by this node.

### Step 4 — Synthesize and Report Findings

After collecting all API responses, produce a structured market intelligence report tailored to the user's objective:

**For product analysis:**
1. **Product Overview** — Title, price range, seller info, category path (L1 → L2 → L3), rating.
2. **Sales Performance** — Historical sales volume, GMV trend, growth rate, seasonality patterns.
3. **Customer Sentiment** — Review volume, rating distribution, key positive/negative themes from reviews.
4. **Creator & Content Attribution** — Top creators promoting the product, video and live-stream conversion rates.
5. **Competitive Position** — Ranking within category, price positioning vs. competing products.

**For shop analysis:**
1. **Shop Profile** — Shop name, category focus, total products, seller tier.
2. **Revenue Intelligence** — GMV history, monthly sales trend, growth trajectory.
3. **Product Portfolio** — Top-performing products, category distribution, price range strategy.
4. **Creator Ecosystem** — Associated creators, their individual GMV contributions, collaboration patterns.
5. **Market Position** — Category ranking, competitive comparison.

**For category/market analysis:**
1. **Category Landscape** — Category hierarchy, total market size estimate, top sub-categories.
2. **Top Products & Shops** — Ranking leaders, their metrics, and differentiation factors.
3. **Trend Analysis** — Rising vs. declining sub-categories, emerging product types.
4. **Opportunity Signals** — Underserved niches, high-growth segments, pricing white spaces.

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Common Rules

| Rule | Detail |
|------|--------|
| **Pagination** | All `*_analytics` endpoints use `page_num` (starts at `1`) and `page_size`. Never use page `0`. |
| **Cover images** | Batch-convert all image URLs from `echosell-images.tos-ap-southeast-1.volces.com` via `batch_download_cover_images` before storing or displaying. |
| **Success check** | `code = 0` → success. Any other value → failure. Always check the response code before processing data. |
| **Retry on 500** | If `code = 500`, retry the identical request once after a brief pause before reporting the error. |
| **Cache first** | Always check the local `.keyapi-cache/` directory before issuing a live API call. Category data is especially cacheable. |
| **Category resolution** | When filtering by category, always resolve the full hierarchy (L1 → L2 → L3) using the category analytics nodes before applying category filters. |
| **Product ID from link** | When the user provides a product share URL, always call `get_product_id_from_share_link` first to extract the `product_id`. |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| `0` | Success | Continue workflow normally |
| `400` | Bad request — invalid or missing parameters | Validate input against the tool schema; check category IDs and product IDs are correct |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `404` | Resource not found — product or shop not indexed | Verify IDs are correct; try a search-based node to locate the resource |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry once after 2–3 seconds; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
