---
name: keyapi-amazon-ecommerce
description: Explore and analyze Amazon e-commerce data at scale — product search, category browsing, product details, best sellers, deals, seller intelligence, influencer storefronts, reviews, and ASIN/GTIN conversion across 24 Amazon marketplaces.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"🛒"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-amazon-ecommerce

> Explore and analyze Amazon e-commerce data at scale — from product discovery and competitive pricing intelligence to seller profiling, review analysis, and influencer storefront research.

This skill provides comprehensive Amazon marketplace intelligence using the KeyAPI MCP service. It enables product search and discovery, category-level browsing, multi-ASIN detail retrieval, best seller and deal monitoring, seller profile and review analysis, influencer post and product research, and identifier conversion — all through a unified, cache-first workflow supporting 24 Amazon marketplaces.

Use this skill when you need to:
- Search and discover Amazon products by keyword, category, brand, price range, or seller
- Retrieve detailed product information, availability, and variant data for up to 10 ASINs per call
- Monitor best sellers, new releases, trending products, and active deals with rich filter options
- Analyze seller profiles, seller reviews, and seller product catalogs
- Research Amazon influencer storefronts — posts, creative lists, and recommended products
- Retrieve and analyze customer reviews with star rating and verified purchase filters
- Compare product offers across conditions (new, used, refurbished) and delivery options
- Convert Amazon ASINs to Global Trade Item Numbers (GTINs)

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **KEYAPI_TOKEN** | A valid API token from [keyapi.ai](https://keyapi.ai/). Register at the site to obtain your free token. Set it as an environment variable: `export KEYAPI_TOKEN=your_token_here` |
| **Node.js** | v18 or higher |
| **Dependencies** | Run `npm install` in the skill directory to install `@modelcontextprotocol/sdk` |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## MCP Server Configuration

All tool calls in this skill target the KeyAPI Amazon MCP server:

```
Server URL : https://mcp.keyapi.ai/amazon/mcp
Auth Header: Authorization: Bearer $KEYAPI_TOKEN
```

**Setup (one-time):**

```bash
# 1. Install dependencies
npm install

# 2. Set your API token (get one free at https://keyapi.ai/)
export KEYAPI_TOKEN=your_token_here

# 3. List all available tools to verify the connection
node scripts/run.js --platform amazon --list-tools
```

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Analysis Scenarios

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Keyword or ASIN-based product search | `product_search` | Product discovery, competitive research |
| Browse products in a specific category | `products_by_category` | Category-level analysis, assortment research |
| Detailed product info for 1–10 ASINs | `product_details` | Product audit, price/spec comparison |
| Top-level category list for a marketplace | `product_category_list` | Category hierarchy discovery |
| Best sellers, new releases, trending items | `best_seller` | Market trend monitoring, top-performer benchmarking |
| Convert ASIN to GTIN/EAN/UPC | `asin_to_gtin` | Cross-marketplace identifier mapping |
| Customer reviews for a product | `product_reviews` | Sentiment analysis, quality signals |
| Full details for a specific review | `product_review_details` | Deep review audit, reviewer profiling |
| Top-ranked helpful reviews | `top_product_reviews` | Quick quality pulse, best review sampling |
| Available purchase offers (new/used/refurb) | `product_offers` | Price comparison, buy box intelligence |
| Active deals with filters | `deals` | Deal monitoring, promotional intelligence |
| Products in a specific deal | `deal_products` | Deal content analysis |
| Promo code discount details | `promo_code_detail` | Coupon validation, discount research |
| Seller profile and business info | `seller_profile` | Seller credibility assessment |
| Seller customer reviews | `seller_reviews` | Seller reputation analysis |
| Seller product catalog | `seller_products` | Seller assortment research |
| Amazon influencer storefront profile | `influencer_profile` | Influencer discovery, follower/bio data |
| Influencer posts (lists, photos, videos) | `influencer_posts` | Content audit, product promotion patterns |
| Products in an influencer list post | `influencer_post_products` | Product attribution, affiliate research |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify Analysis Targets and Select Nodes

Clarify the research objective and map it to one or more nodes. Typical entry points:

- **Product discovery**: Use `product_search` with keyword + filters → deepen with `product_details` for specific ASINs.
- **Category analysis**: Use `product_category_list` to find `category_id` → `products_by_category` to browse listings.
- **Competitive pricing**: Combine `product_details` + `product_offers` to compare price and condition options.
- **Best seller research**: Use `best_seller` with `category` path and `type` parameter.
- **Deal monitoring**: Use `deals` with filters → `deal_products` for specific deal contents.
- **Seller intelligence**: Use `seller_profile` → `seller_reviews` + `seller_products` for full seller audit.
- **Review analysis**: Use `product_reviews` with `star_rating` and `verified_purchases_only` filters; `top_product_reviews` for quick sampling.
- **Influencer research**: Use `influencer_profile` → `influencer_posts` → `influencer_post_products` for product attribution.

> **Multi-ASIN Batch Calls**
>
> `product_details` and `product_offers` accept **comma-separated ASIN lists** in the `asin` parameter (up to 10 ASINs per call). This enables efficient bulk retrieval in a single request.
>
> Example: `"asin": "B07ZPKBL9V,B09SM24S8C,B08N5WRWNW"`

> **`country` Parameter — Multi-Marketplace Support**
>
> Most endpoints accept a `country` parameter (default: `us`). Set it to target a specific Amazon marketplace:
> `us`, `uk`, `de`, `fr`, `it`, `es`, `ca`, `jp`, `au`, `in`, `mx`, `br`, `sg`, `ae`, `sa`, `tr`, `nl`, `pl`, `se`, `be`, `eg`, `za`, `ng`, `ke`

> **`fields` Projection**
>
> Most endpoints accept an optional `fields` parameter — a comma-separated list of fields to return. Use it to reduce response payload size and focus on only the data you need.

> **`best_seller` Category Path**
>
> The `category` parameter uses the URL path from Amazon's Best Sellers page. For example, `software` maps to `https://www.amazon.com/Best-Sellers-Software/zgbs/software`. The `type` parameter controls the list: `BEST_SELLERS`, `NEW_RELEASES`, `MOVERS_AND_SHAKERS`, `MOST_WISHED_FOR`, `GIFT_IDEAS`.

> **`deals` Pagination**
>
> `deals` uses `offset` (not `page`) for pagination. Increment by 30 for each page: `0`, `30`, `60`, `90`, etc.

> **Influencer Post Workflow**
>
> To retrieve products from an influencer post:
> 1. Call `influencer_posts` with `influencer_name` to list posts — note the `post_id` values.
> 2. Call `influencer_post_products` with `influencer_name` + `post_id` (only works for posts of type `list`).

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters and available options:

```bash
node scripts/run.js --platform amazon --schema <tool_name>

# Examples
node scripts/run.js --platform amazon --schema product_search
node scripts/run.js --platform amazon --schema best_seller
node scripts/run.js --platform amazon --schema deals
```

### Step 3 — Call APIs and Cache Results Locally

Execute tool calls and persist responses to the local cache to avoid redundant API calls.

**Calling a tool:**

```bash
# Single call with pretty output
node scripts/run.js --platform amazon --tool <tool_name> \
  --params '<json_args>' --pretty

# Force fresh data, skip cache
node scripts/run.js --platform amazon --tool <tool_name> \
  --params '<json_args>' --no-cache --pretty
```

**Example — search products with filters:**

```bash
node scripts/run.js --platform amazon --tool product_search \
  --params '{"query":"wireless earbuds","country":"us","sort_by":"REVIEWS","min_price":20,"max_price":100,"is_prime":true}' --pretty
```

**Example — get details for multiple ASINs in one call:**

```bash
node scripts/run.js --platform amazon --tool product_details \
  --params '{"asin":"B07ZPKBL9V,B09SM24S8C","country":"us"}' --pretty
```

**Example — get best sellers:**

```bash
node scripts/run.js --platform amazon --tool best_seller \
  --params '{"category":"electronics","type":"BEST_SELLERS","country":"us","page":1}' --pretty
```

**Example — get active deals:**

```bash
node scripts/run.js --platform amazon --tool deals \
  --params '{"country":"us","discount_range":"3","min_product_star_rating":"4"}' --pretty
```

**Example — get product reviews filtered by star rating:**

```bash
node scripts/run.js --platform amazon --tool product_reviews \
  --params '{"asin":"B00939I7EK","sort_by":"TOP_REVIEWS","star_rating":"5_STAR","verified_purchases_only":true,"page":1}' --pretty
```

**Example — get seller profile and reviews:**

```bash
node scripts/run.js --platform amazon --tool seller_profile \
  --params '{"seller_id":"A02211013Q5HP3OMSZC7W","country":"us"}' --pretty

node scripts/run.js --platform amazon --tool seller_reviews \
  --params '{"seller_id":"A02211013Q5HP3OMSZC7W","star_rating":"NEGATIVE","country":"us"}' --pretty
```

**Example — get influencer posts then products:**

```bash
# Step 1: get posts
node scripts/run.js --platform amazon --tool influencer_posts \
  --params '{"influencer_name":"tastemade","limit":20}' --pretty

# Step 2: get products from a specific list post
node scripts/run.js --platform amazon --tool influencer_post_products \
  --params '{"influencer_name":"madison.lecroy","post_id":"amzn1.ideas.382NVFBNK3GGQ"}' --pretty
```

**Pagination reference:**

| Endpoint | Pagination method | Notes |
|---|---|---|
| `product_search`, `products_by_category`, `best_seller`, `deal_products` | `page` (int, 1-indexed) | Standard page-based pagination |
| `product_reviews` | `page` (int, 1-indexed) | Also supports `cookie` for session continuity |
| `product_offers` | `page` (int, 1-indexed) | Default `limit` is 100 offers |
| `seller_reviews`, `seller_products` | `page` (int) | Optional, starts at 1 |
| `deals` | `offset` (int) | Multiples of 30: 0, 30, 60, 90… |
| `influencer_posts`, `influencer_post_products` | `cursor` (string) | Pass cursor from previous response; omit for first call |
| `product_details`, `top_product_reviews`, `seller_profile`, `promo_code_detail`, `asin_to_gtin`, `product_category_list` | — | Single-call or no pagination |

**`product_search` and `products_by_category` sort options:**

| Value | Description |
|---|---|
| `RELEVANCE` | Default — most relevant results |
| `LOWEST_PRICE` | Cheapest first |
| `HIGHEST_PRICE` | Most expensive first |
| `REVIEWS` | Most reviewed |
| `NEWEST` | Most recently listed |
| `BEST_SELLERS` | Best-selling products first |

**`product_search` and `products_by_category` condition options (`product_condition`):**

| Value | Description |
|---|---|
| `ALL` | All conditions (default) |
| `NEW` | New products only |
| `USED` | Used products only |
| `RENEWED` | Renewed/refurbished products |
| `COLLECTIBLE` | Collectible items |

**`product_search` and `products_by_category` deals filter (`deals_and_discounts`):**

| Value | Description |
|---|---|
| `NONE` | No filter (default) |
| `ALL_DISCOUNTS` | Any discounted product |
| `TODAYS_DEALS` | Today's deals only |

**`product_offers` condition options (`product_condition`):**

Pass as comma-separated values: `NEW`, `USED_LIKE_NEW`, `USED_VERY_GOOD`, `USED_GOOD`, `USED_ACCEPTABLE`

**Cache directory structure:**

```
.keyapi-cache/
└── YYYY-MM-DD/
    ├── product_search/
    │   └── {params_hash}.json
    ├── products_by_category/
    │   └── {params_hash}.json
    ├── product_details/
    │   └── {params_hash}.json
    ├── product_category_list/
    │   └── {params_hash}.json
    ├── best_seller/
    │   └── {params_hash}.json
    ├── asin_to_gtin/
    │   └── {params_hash}.json
    ├── product_reviews/
    │   └── {params_hash}.json
    ├── product_review_details/
    │   └── {params_hash}.json
    ├── top_product_reviews/
    │   └── {params_hash}.json
    ├── product_offers/
    │   └── {params_hash}.json
    ├── deals/
    │   └── {params_hash}.json
    ├── deal_products/
    │   └── {params_hash}.json
    ├── promo_code_detail/
    │   └── {params_hash}.json
    ├── seller_profile/
    │   └── {params_hash}.json
    ├── seller_reviews/
    │   └── {params_hash}.json
    ├── seller_products/
    │   └── {params_hash}.json
    ├── influencer_profile/
    │   └── {params_hash}.json
    ├── influencer_posts/
    │   └── {params_hash}.json
    └── influencer_post_products/
        └── {params_hash}.json
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists for the given parameters. If a valid cache file exists, load from disk and skip the API call.

### Step 4 — Synthesize and Report Findings

After collecting all API responses, produce a structured e-commerce intelligence report:

**For product research:**
1. **Product Overview** — Title, ASIN, brand, category, price range, availability, Prime status, rating, review count.
2. **Competitive Landscape** — Price comparison across sellers and conditions, Buy Box holder, offer distribution.
3. **Review Intelligence** — Star rating distribution, top positive and critical themes, verified purchase ratio.
4. **Market Positioning** — Best seller rank, category placement, variant availability.

**For seller research:**
1. **Seller Profile** — Business name, overall rating, response rate, storefront description.
2. **Reputation Signals** — Review distribution (positive/neutral/negative), recurring feedback themes.
3. **Product Assortment** — Catalog size, category coverage, pricing patterns.

**For deal and promotion monitoring:**
1. **Active Deals** — Deal type distribution (Lightning, Prime Exclusive, Prime Early Access), discount depth, category distribution.
2. **Promo Intelligence** — Applicable products, discount amounts, validity periods.

**For influencer research:**
1. **Storefront Overview** — Influencer name, follower count, bio, post count.
2. **Content Analysis** — Post type breakdown (lists, photos, videos), keyword themes, scope categories.
3. **Product Attribution** — Products promoted, category alignment, affiliate depth.

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Common Rules

| Rule | Detail |
|------|--------|
| **Multi-ASIN calls** | `product_details` and `product_offers` accept up to 10 comma-separated ASINs in a single `asin` parameter. |
| **`country` parameter** | Defaults to `us`. Pass a two-letter country code to target other Amazon marketplaces (24 supported). |
| **`fields` projection** | Most endpoints accept `fields` (comma-separated field names) to reduce response size. Use it to fetch only the data you need. |
| **`best_seller` category** | Use the URL path from Amazon's Best Sellers page as the `category` value (e.g., `electronics`, `software`). |
| **`deals` pagination** | Uses `offset` (not `page`). Increment by 30 for each page: 0, 30, 60, 90… |
| **Influencer post type** | `influencer_post_products` only works for posts with type `list`. Check post type in `influencer_posts` response first. |
| **`product_offers` condition** | `product_condition` accepts comma-separated values: `NEW`, `USED_LIKE_NEW`, `USED_VERY_GOOD`, `USED_GOOD`, `USED_ACCEPTABLE`. |
| **Success check** | `code = 0` → success. Any other value → failure. Always check the response code before processing data. |
| **Retry on 500** | If `code = 500`, retry the identical request up to 3 times with a 2–3 second pause between attempts before reporting the error. |
| **Cache first** | Always check the local `.keyapi-cache/` directory before issuing a live API call. |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| `0` | Success | Continue workflow normally |
| `400` | Bad request — invalid or missing parameters | Validate ASIN format, check batch size limit (max 10), verify `country` code |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `404` | Resource not found — product, seller, or influencer may not exist | Verify ASIN, `seller_id`, or `influencer_name`; product may have been delisted |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry up to 3 times with a 2–3 second pause; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
