---
name: keyapi-tiktok-intelligence
description: Real-time TikTok trend intelligence — monitor trending hashtags, viral music, breakout videos, top-performing ads, and high-growth products to identify emerging opportunities and market movements before they become mainstream.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"📈"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-tiktok-intelligence

> Real-time TikTok trend intelligence — monitor trending hashtags, viral music, breakout videos, top-performing ads, and high-growth products to stay ahead of the curve.

This skill provides real-time and near-real-time intelligence on what is trending across TikTok using the KeyAPI MCP service. It covers trending hashtags, music tracks, videos, keyword-level market insights, top-performing shop products by category, and ad creative performance — enabling brands, creators, and analysts to rapidly identify emerging opportunities and high-signal market movements.

Use this skill when you need to:
- Monitor what hashtags, music, and videos are gaining momentum right now
- Get keyword-level insights into consumer interest, product demand, and creator activity
- Identify top-selling products in specific categories before they become mainstream
- Analyze high-performing TikTok ad creatives for inspiration and benchmarking
- Build a real-time market intelligence dashboard for a brand, category, or audience segment

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

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Get current trending hashtag list with growth metrics | `trending_hashtags` | Real-time trending topic discovery |
| Deep-dive into a specific trending hashtag | `trending_hashtag_detail` | Hashtag opportunity assessment, content strategy |
| Get current trending music tracks | `trending_music` | Sound discovery for content creation, audio trend monitoring |
| Deep-dive into a specific trending music track | `trending_music_detail` | Track adoption timeline, associated content themes |
| Get current trending video list with engagement data | `trending_videos` | Viral content discovery, format benchmarking |
| Market insights for a specific keyword (products, creators, demand) | `keyword_insights` | Keyword opportunity analysis, product-market fit signals |
| Top-performing products by category with sales rankings | `top_products_insights` | Category-level commerce intelligence, opportunity identification |
| Detailed breakdown of top products in a specific category | `top_product_insights_detail` | Product-level deep-dive within a high-performing category |
| Top-performing TikTok ad creatives with engagement metrics | `top_ads_insights` | Ad creative benchmarking, industry trend analysis |
| Detailed breakdown of a specific top-performing ad | `top_ad_insights_detail` | Creative analysis, performance metric breakdown |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify the Intelligence Objective and Select Nodes

Clarify the user's goal and map it to the appropriate nodes. Common research patterns:

- **Real-time trend monitoring**: Start with `trending_hashtags` + `trending_music` + `trending_videos` for a full trending snapshot.
- **Hashtag opportunity assessment**: Use `trending_hashtags` to identify candidates, then `trending_hashtag_detail` for the most promising ones.
- **Music trend analysis**: Use `trending_music` for the current top tracks, then `trending_music_detail` for adoption timelines and usage patterns.
- **Keyword market intelligence**: Use `keyword_insights` to map consumer interest, product demand, and creator activity around a keyword.
- **Product category intelligence**: Use `top_products_insights` for a category overview, then `top_product_insights_detail` for specific high-performers.
- **Ad creative research**: Use `top_ads_insights` for a landscape view, then `top_ad_insights_detail` for individual ad breakdowns.

Multiple nodes can be combined — for example, running `keyword_insights` alongside `top_products_insights` to correlate consumer search interest with actual purchase behavior in a category.

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters and valid values:

```bash
node scripts/run.js --schema <tool_name>

# Examples
node scripts/run.js --schema keyword_insights
node scripts/run.js --schema top_products_insights
```

### Step 3 — Call APIs and Cache Results Locally

Execute the required tool calls and persist all responses to the local cache. Intelligence data is time-sensitive — cache files should be timestamped to reflect their freshness.

**Calling a tool (using `scripts/run.js`):**

```bash
# Single call — result is cached automatically
node scripts/run.js --tool <tool_name> --params '<json_args>' --pretty

# Fetch all pages (for list endpoints)
node scripts/run.js --tool <tool_name> --params '<json_args>' --all-pages

# Force a fresh call to get the latest data
node scripts/run.js --tool <tool_name> --params '<json_args>' --no-cache
```

**Example — get trending hashtags:**

```bash
node scripts/run.js --tool trending_hashtags \
  --params '{"region":"US"}' --pretty
```

**Example — get keyword market insights:**

```bash
node scripts/run.js --tool keyword_insights \
  --params '{"search_keyword":"stanley cup","region":"US"}' --pretty
```

**Example — get top products in a category:**

```bash
node scripts/run.js --tool top_products_insights \
  --params '{"ecom_category_id":"600001","region":"US"}' --all-pages
```

**Cache directory structure:**

Intelligence data is time-sensitive. Cache files are keyed by date to preserve historical snapshots and allow trend comparison across sessions.

```
.keyapi-cache/
└── intelligence/
    ├── trending/
    │   ├── hashtags_{region}_{YYYY-MM-DD}.json      # trending_hashtags
    │   ├── music_{region}_{YYYY-MM-DD}.json         # trending_music
    │   └── videos_{region}_{YYYY-MM-DD}.json        # trending_videos
    ├── hashtag_detail/
    │   └── {hashtag}_{YYYY-MM-DD}.json              # trending_hashtag_detail
    ├── music_detail/
    │   └── {music_id}_{YYYY-MM-DD}.json             # trending_music_detail
    ├── keywords/
    │   └── {keyword}_{region}_{YYYY-MM-DD}.json     # keyword_insights
    ├── top_products/
    │   ├── {category_id}_{region}_{YYYY-MM-DD}.json              # top_products_insights
    │   └── detail_{category_id}_{region}_{YYYY-MM-DD}.json       # top_product_insights_detail
    └── top_ads/
        ├── {industry}_{region}_{YYYY-MM-DD}.json                 # top_ads_insights
        └── detail_{ad_id}_{YYYY-MM-DD}.json                      # top_ad_insights_detail
```

**Cache-first policy:**

Intelligence data has a natural staleness window. As a general guideline:
- **Trending data** (hashtags, music, videos): cache is valid for the current day; refresh daily.
- **Keyword insights**: cache is valid for 24 hours.
- **Top products/ads**: cache is valid for 24–48 hours.

If a cache file exists for the current date, load from disk. Otherwise, make a live API call and save to cache.

**Cover image processing:**

After each API call, scan all response image URLs. If any URL's host matches `echosell-images.tos-ap-southeast-1.volces.com`, collect those URLs and call `batch_download_cover_images` in a single batch request. Replace the original URLs in your working dataset with the converted URLs returned by this node.

### Step 4 — Synthesize and Report Findings

After collecting all API responses, produce a structured intelligence briefing:

**For trending analysis:**
1. **Trend Snapshot** — Top trending hashtags/music/videos at this moment, with video counts, usage figures, and growth rates.
2. **Breakout Signals** — Items showing unusually high growth velocity — new entrants to the trending list or those with accelerating metrics.
3. **Pattern Analysis** — Common themes, content formats, or creator types driving the trends.
4. **Strategic Implications** — Which trends represent short-term spikes vs. sustainable growth; recommended action windows.

**For keyword intelligence:**
1. **Search Demand** — Volume and trend direction for the keyword on TikTok.
2. **Product Landscape** — Top products associated with this keyword, their GMV, and sales volume.
3. **Creator Activity** — Active creators in this keyword space, their reach and engagement.
4. **Consumer Interest Signals** — Audience demographics engaging with this keyword content.
5. **Opportunity Score** — Assessment of competition level vs. demand strength.

**For top products intelligence:**
1. **Category Overview** — Total active product count, combined GMV, growth rate.
2. **Top Products Breakdown** — Ranked list of top performers with price, sales volume, GMV, and growth rate.
3. **Rising Stars** — Products with the highest month-over-month growth — emerging opportunities before mainstream awareness.
4. **Pricing Intelligence** — Price distribution, sweet spots, premium vs. budget segment dynamics.

**For ad creative intelligence:**
1. **Ad Landscape** — Top ad formats, industries, and creative types currently performing on TikTok.
2. **Creative Breakdown** — Hook types, video lengths, CTA strategies, and visual styles driving highest engagement.
3. **Industry Benchmarks** — Engagement rates and impression volumes by industry/category.
4. **Actionable Insights** — Creative elements to adopt, formats to test, and industries increasing ad spend.

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Common Rules

| Rule | Detail |
|------|--------|
| **Pagination** | Trending/insights list endpoints (`trending_hashtags`, `trending_music`, `trending_videos`, `keyword_insights`, `top_products_insights`, `top_ads_insights`) use `page` (starts at `1`) and `limit` (max 10). Never use page `0`. |
| **Keyword param** | `keyword_insights` and `trending_music` use `search_keyword` (not `keyword`) as the search parameter. `top_products_insights` uses `ecom_category_id` (not `category_id`) for category filtering. |
| **Cover images** | Batch-convert all image URLs from `echosell-images.tos-ap-southeast-1.volces.com` via `batch_download_cover_images` before storing or displaying. |
| **Success check** | `code = 0` → success. Any other value → failure. Always check the response code before processing data. |
| **Retry on 500** | If `code = 500`, retry the identical request once after a brief pause before reporting the error. |
| **Cache with timestamps** | Intelligence data is time-sensitive. Always include the date in cache filenames to preserve historical snapshots. |
| **Data freshness** | Trending data and keyword insights should be refreshed daily. Do not serve stale intelligence without surfacing the data age to the user. |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| `0` | Success | Continue workflow normally |
| `400` | Bad request — invalid or missing parameters | Validate input against the tool schema; check region codes, category IDs, and keyword format |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `404` | Resource not found | Verify the hashtag, music ID, or ad ID is correct |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry once after 2–3 seconds; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
