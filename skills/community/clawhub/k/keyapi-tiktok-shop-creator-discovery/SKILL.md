---
name: keyapi-tiktok-shop-creator-discovery
description: Discover and analyze TikTok Shop creators — identify top-performing commerce sellers, evaluate GMV and sales metrics, understand audience demographics, and track creator growth trends within the TikTok e-commerce ecosystem.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"🛍️"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-tiktok-shop-creator-discovery

> Discover and analyze TikTok Shop creators — identify top-performing sellers, evaluate sales metrics, and understand audience demographics for commerce-focused creator partnerships.

This skill provides deep intelligence on TikTok Shop creators using the KeyAPI MCP service. Unlike standard influencer analysis, this skill is specifically scoped to the **TikTok e-commerce ecosystem**, surfacing creators' actual sales performance, GMV contribution, product promotion behavior, and follower demographics — data that is only available within the TikTok Shop commercial platform.

Use this skill when you need to:
- Find TikTok Shop creators who actively sell products in a specific category
- Evaluate a creator's sales track record, GMV output, and product promotion effectiveness
- Understand a creator's audience profile (age, gender, geography) for commerce targeting
- Monitor trends in creator sales activity and follower growth over time
- Compare multiple shop creators to select the best-fit commercial partners

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

Select one or more nodes based on the research objective.

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Find a TikTok Shop creator by their @handle | `search_shop_creator` | ID resolution — obtaining `creator_oecuid` from a known `unique_id` |
| View a creator's shop profile and key performance metrics | `get_shop_creator_detail` | Overview of followers, GMV, and commerce activity |
| Analyze a creator's product sales and GMV breakdown | `get_shop_creator_sales` | Evaluating sales effectiveness, top-selling items, revenue contribution |
| Understand a creator's audience demographics | `get_shop_creator_audience` | Age, gender, and geographic distribution for targeting fit |
| Track a creator's growth and sales trends over time | `get_shop_creator_trends` | Trend monitoring — follower growth velocity, view and sales trajectory |
| Review a creator's product promotion videos with sales data | `get_shop_creator_videos` | Content-commerce analysis — which videos drove conversions |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify the Creator and Select Nodes

Clarify the user's objective and determine which nodes to invoke. Typical entry points:

- **Starting from a @handle**: Always begin with `search_shop_creator` to resolve the `creator_oecuid`.
- **Full creator audit**: Use `get_shop_creator_detail` + `get_shop_creator_sales` + `get_shop_creator_trends`.
- **Audience analysis**: Use `get_shop_creator_audience` for demographic profile.
- **Content-commerce analysis**: Use `get_shop_creator_videos` to identify which content formats drive the most sales.

> **⚠️ Critical: Resolving `creator_oecuid`**
>
> The `creator_oecuid` is the unique identifier used by TikTok's commercial/e-commerce platform (OEC = Overseas E-Commerce system). It is **required by all nodes except `search_shop_creator`**.
>
> Users will typically provide a creator's `unique_id` (@handle). Always call `search_shop_creator` first to obtain the `creator_oecuid` before making any other calls.
>
> **All endpoints require a `region` parameter** (one of: `US`, `DE`, `TH`, `MY`, `ID`, `PH`, `VN`). Always include it in every call.

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters and valid values:

```bash
node scripts/run.js --schema <tool_name>

# Example
node scripts/run.js --schema get_shop_creator_sales
```

### Step 3 — Call APIs and Cache Results Locally

Execute the required tool calls and persist all responses to the local cache.

**Calling a tool (using `scripts/run.js`):**

```bash
# Single call — result is cached automatically
node scripts/run.js --tool <tool_name> --params '<json_args>' --pretty

# Force a fresh call, skip cache
node scripts/run.js --tool <tool_name> --params '<json_args>' --no-cache
```

**Example — find a shop creator by unique_id:**

```bash
node scripts/run.js --tool search_shop_creator \
  --params '{"unique_id":"example_creator","region":"US"}' --pretty
```

**Example — get creator sales data:**

```bash
node scripts/run.js --tool get_shop_creator_sales \
  --params '{"creator_oecuid":"7494008088472553296","region":"US"}' --pretty
```

**Cache directory structure:**

```
.keyapi-cache/
└── shop_creators/
    └── {creator_oecuid}/
        ├── detail.json        # get_shop_creator_detail
        ├── sales.json         # get_shop_creator_sales
        ├── audience.json      # get_shop_creator_audience
        ├── trends.json        # get_shop_creator_trends
        └── videos.json        # get_shop_creator_videos
└── searches/
    └── shop_creators/
        └── {unique_id}.json   # search_shop_creator (keyed by unique_id for direct lookup)
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists. If a valid cache file exists for the given `creator_oecuid` and node, load from disk and skip the API call.

**Recommended call sequence:**

```
1. search_shop_creator(unique_id, region)          → obtains creator_oecuid
2. get_shop_creator_detail(creator_oecuid, region) → profile overview and key KPIs
3. get_shop_creator_sales(creator_oecuid, region)  → product sales and GMV breakdown
4. get_shop_creator_audience(creator_oecuid, region) → audience demographics
5. get_shop_creator_trends(creator_oecuid, region)   → time-series growth and sales trends
6. get_shop_creator_videos(creator_oecuid, region)   → promotion video performance
```

**Cover image processing:**

After each API call, scan all response image URLs. If any URL's host matches `echosell-images.tos-ap-southeast-1.volces.com`, collect those URLs and call `batch_download_cover_images` in a single batch request. Replace the original URLs in your working dataset with the converted URLs returned by this node.

### Step 4 — Synthesize and Report Findings

After collecting all API responses, produce a structured creator evaluation report:

1. **Creator Commerce Profile** — Name, @handle, follower count, total GMV, active product categories, and TikTok Shop tenure.
2. **Sales Performance Analysis** — Total items sold, GMV breakdown by product, top-selling products, video-driven vs. live-stream-driven revenue split.
3. **Audience Intelligence** — Age and gender distribution, top geographic markets, audience-product category alignment.
4. **Growth and Trend Analysis** — Follower growth trajectory, correlation between video/live activity and sales spikes.
5. **Content-Commerce Effectiveness** — Highest-converting video formats, average views per promotion video, CTR signals.
6. **Partnership Recommendations** — Best-fit collaboration formats (product seeding, affiliate, exclusive collab), risk signals (declining trends, audience mismatch), estimated deal value benchmarks based on GMV history.

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
| **Cache first** | Always check the local `.keyapi-cache/` directory before issuing a live API call. |
| **ID resolution** | Users provide `unique_id` (@handle). Always call `search_shop_creator` first to resolve the `creator_oecuid` required by all other nodes. |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| `0` | Success | Continue workflow normally |
| `400` | Bad request — invalid or missing parameters | Validate input against the tool schema; correct and retry |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `404` | Resource not found — creator may not be a TikTok Shop creator | Verify the `unique_id`; confirm the creator has an active TikTok Shop account |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry once after 2–3 seconds; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
