---
name: keyapi-tiktok-influencer-discovery
description: Discover, profile, and deeply analyze TikTok influencers — from keyword-based search to multi-dimensional performance intelligence covering follower trends, engagement rates, live-stream GMV, video performance, and competitive rankings.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"🔍"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-tiktok-influencer-discovery

> Discover, profile, and deeply analyze TikTok influencers — from keyword-based search to multi-dimensional performance intelligence.

This skill powers end-to-end TikTok influencer research using the KeyAPI MCP service. It enables you to find creators by keyword or region, retrieve their profile and performance metrics, analyze historical growth trajectories, and benchmark them against ranking data — all through a single, orchestrated workflow.

Use this skill when you need to:
- Identify high-performing influencers for brand collaborations or affiliate campaigns
- Audit a creator's follower growth, engagement rate, and live-stream GMV history
- Build ranked shortlists and compare multiple creators across key performance dimensions
- Track historical trends for competitive intelligence and market positioning

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

Select one or more nodes based on the research objective. Multiple nodes can be combined for cross-dimensional analysis.

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Find influencers by keyword, category, or region | `search_influencers` | Initial discovery, broad prospecting |
| Verify an influencer's identity and resolve IDs | `get_influencer_detail` | ID resolution (user_id + unique_id), profile snapshot |
| Filter influencers with analytics (ER, GMV, followers, sales) | `influencer_list_analytics` | Data-driven shortlisting from large datasets |
| Full multi-dimensional performance audit | `influencer_detail_analytics` | Deep-dive due diligence on one or more creators |
| Analyze historical growth trends over time | `influencer_trends_analytics` | Growth velocity, follower trajectory, trend analysis |
| Review video content performance history | `influencer_videos_analytics` | Content strategy benchmarking, top-video analysis |
| Evaluate live-stream commerce history (GMV, viewers) | `influencer_livestreams_analytics` | Live commerce capability assessment |
| Examine promoted product portfolio and sales | `influencer_products_analytics` | Brand-fit assessment, niche/category alignment |
| Competitive ranking by followers, GMV, or ER | `influencer_ranking_analytics` | Leaderboard analysis, category benchmarks |
| Retrieve latest published videos with engagement stats | `get_influencer_videos` | Recent content monitoring, freshness check |
| Sample an influencer's follower list | `get_influencer_followers` | Audience quality sampling |
| Explore the accounts an influencer follows | `get_influencer_following` | Network and affinity analysis |
| Geographic breakdown of audience distribution | `get_influencer_region` | Geo-targeting fit for regional campaigns |
| Generate a shareable profile QR code | `get_influencer_qr_code` | Marketing material assets |
| Key milestone and achievement history | `get_influencer_milestones` | Growth storytelling, historical highlights |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify Analysis Targets and Select Nodes

Clarify the user's objective and map it to one or more nodes from the table above. Typical entry points:

- **Keyword discovery**: Start with `search_influencers`, then optionally deepen with `influencer_list_analytics` for richer filtering.
- **Direct profile lookup**: Use `get_influencer_detail` with a known `unique_id` (@handle).
- **Performance deep-dive**: Combine `influencer_detail_analytics` + `influencer_trends_analytics` + `influencer_videos_analytics`.
- **Live commerce evaluation**: Use `influencer_livestreams_analytics` + `influencer_products_analytics`.
- **Competitive ranking**: Use `influencer_ranking_analytics` with appropriate category/region filters.

> **⚠️ Critical: Resolving `user_id` vs. `unique_id`**
>
> Two distinct identifier types are used across endpoints:
> - `unique_id` — the user's public **@handle** (e.g., `charlidamelio`). User-visible, mutable.
> - `user_id` — TikTok's permanent, immutable **numeric UID** assigned to each account.
>
> When a workflow requires nodes that accept different identifier types, **always call `get_influencer_detail` first** using the `unique_id` to obtain both identifiers before proceeding.

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters, data types, and valid enumeration values:

```bash
node scripts/run.js --schema <tool_name>

# Example
node scripts/run.js --schema influencer_list_analytics
```

For analytics nodes, pay particular attention to filter parameters (region, category, date range, follower range, etc.) and confirm the expected `page_num`/`page_size` fields.

### Step 3 — Call APIs and Cache Results Locally

Execute the required tool calls and persist all responses to the local cache to enable result reuse across sessions and avoid redundant API calls.

**Calling a tool (using `scripts/run.js`):**

```bash
# Single page call — result is cached automatically
node scripts/run.js --tool <tool_name> --params '<json_args>' --pretty

# Fetch all pages at once (auto-pagination)
node scripts/run.js --tool <tool_name> --params '<json_args>' --all-pages --page-size 50

# Force a fresh call, skip cache
node scripts/run.js --tool <tool_name> --params '<json_args>' --no-cache
```

**Example — search influencers:**

```bash
node scripts/run.js --tool search_influencers \
  --params '{"keyword":"fitness","region":"US"}' --pretty
```

**Example — filter influencers with analytics (all pages):**

```bash
node scripts/run.js --tool influencer_list_analytics \
  --params '{"region":"US","influencer_category_name":"Fitness"}' --all-pages
```

**Example — get influencer's latest videos (cursor-based):**

```bash
# First page: offset=0
node scripts/run.js --tool get_influencer_videos \
  --params '{"unique_id":"charlidamelio","offset":"0"}' --pretty
# Next page: use max_cursor value from previous response as offset
```

**Pagination for analytics endpoints:**

All `*_analytics` endpoints use `page_num` (1-indexed) and `page_size` (max 10). `run.js` injects these automatically if not specified. Use `--all-pages` to let `run.js` iterate all pages and merge the results.

```
--page-num 1  --page-size 10   → first page (default)
--all-pages                    → all pages merged into one result
```

> **Note:** `get_influencer_videos`, `get_influencer_followers`, `get_influencer_following` use cursor-based pagination via an `offset` parameter — not `page_num`/`page_size`. Pass `"offset":"0"` to start, then use the `max_cursor` (or `min_time`) value from the response as the next `offset`.

**Cache directory structure:**

```
.keyapi-cache/
└── influencers/
    └── {unique_id}/
        ├── detail.json                  # get_influencer_detail
        ├── analytics.json               # influencer_detail_analytics
        ├── trends.json                  # influencer_trends_analytics
        ├── videos_analytics.json        # influencer_videos_analytics
        ├── livestreams_analytics.json   # influencer_livestreams_analytics
        ├── products_analytics.json      # influencer_products_analytics
        ├── latest_videos.json           # get_influencer_videos
        ├── followers.json               # get_influencer_followers
        ├── following.json               # get_influencer_following
        ├── region.json                  # get_influencer_region
        ├── qr_code.json                 # get_influencer_qr_code
        └── milestones.json              # get_influencer_milestones
└── searches/
    └── influencers/
        └── {md5_of_query_params}.json   # search_influencers, influencer_list_analytics
└── rankings/
    └── influencers_{params_hash}.json   # influencer_ranking_analytics
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists for the given entity and node. If a valid cache file exists, load from disk and skip the API call.

**Cover image processing:**

After each API call, scan all response image URLs. If any URL's host matches `echosell-images.tos-ap-southeast-1.volces.com`, collect those URLs and call `batch_download_cover_images` in a single batch request. Replace the original URLs in your working dataset with the converted URLs returned by this node.

### Step 4 — Synthesize and Report Findings

After collecting all API responses (from cache or live calls), produce a structured research report:

1. **Creator Profile Summary** — Name, @handle, follower count, engagement rate, primary niche, and operating region.
2. **Performance Analysis** — Follower growth curve, average video views, engagement benchmarks, and live-stream GMV history.
3. **Content Strategy Insights** — Top-performing video themes, posting cadence, product promotion patterns, and audience interaction quality.
4. **Competitive Positioning** — Ranking within category/region, peer comparisons when analyzing multiple creators.
5. **Actionable Recommendations** — Best fit use cases (brand sponsorship, affiliate, live commerce), audience-campaign alignment, risk signals (follower authenticity, trend consistency).

Cross-reference multiple data sources where available — for example, correlate `influencer_trends_analytics` with `influencer_livestreams_analytics` to identify whether GMV peaks align with follower growth events.

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
| **ID resolution** | When a workflow requires both `user_id` and `unique_id`, call `get_influencer_detail` first with the `unique_id` to resolve both. |

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
| `404` | Resource not found — influencer not indexed or ID incorrect | Verify `unique_id` / `user_id`; try `search_influencers` to locate the creator |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry once after 2–3 seconds; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
