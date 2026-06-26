---
name: keyapi-instagram-content-discovery
description: Explore and discover Instagram content at scale — search posts, Reels, hashtags, music, locations, and Explore sections to surface trends, audience signals, and high-engagement content opportunities.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"🔎"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-instagram-content-discovery

> Explore and discover Instagram content at scale — search posts, Reels, hashtags, music, and locations to surface trends, audience signals, and content intelligence.

This skill enables deep content discovery on Instagram using the KeyAPI MCP service. It supports ID conversion between shortcodes and media IDs, detailed post inspection, comment and reply analysis, hashtag and music-based content search, Explore page browsing, and geo-targeted location discovery — all backed by real-time data.

Use this skill when you need to:
- Fetch full post details including engagement metrics, caption, and media data
- Analyze comments and nested replies for audience sentiment and topic signals
- Discover trending or niche content by hashtag, music track, or keyword
- Explore Instagram's Explore page to identify surfaced content categories
- Search for related hashtags, places, music, and Reels by keyword
- Identify content popularity signals for a specific song or audio track
- Perform geo-based location searches for hyper-local content research

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

All tool calls in this skill target the KeyAPI Instagram MCP server:

```
Server URL : https://mcp.keyapi.ai/instagram/mcp
Auth Header: Authorization: Bearer $KEYAPI_TOKEN
```

**Setup (one-time):**

```bash
# 1. Install dependencies
npm install

# 2. Set your API token (get one free at https://keyapi.ai/)
export KEYAPI_TOKEN=your_token_here

# 3. List all available tools to verify the connection
node scripts/run.js --platform instagram --list-tools
```

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Analysis Scenarios

### Post & Comment Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Convert post shortcode → media ID | `convert_shortcode_to_media_id` | ID normalization; shortcode is the string in `instagram.com/p/{shortcode}/` |
| Convert media ID → shortcode | `convert_media_id_to_shortcode` | Reverse lookup; construct post URL from a numeric media ID |
| Full post details (metrics, caption, media) | `get_post_info` | Post audit, engagement snapshot — accepts shortcode or full URL |
| Users who liked a post | `get_post_likes` | Engagement quality sampling, audience analysis |
| Top-level comments on a post | `get_post_comments` | Audience sentiment, comment volume analysis — sortable by `recent` or `popular` |
| Replies to a specific comment | `get_comment_replies` | Conversation thread depth, nested engagement analysis |

### Explore & Hashtag Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| List Explore page content sections | `get_explore_page_sections` | Discover available content categories on the Explore page |
| Posts inside a specific Explore section | `get_posts_by_section` | Browse curated Explore content by category — requires `section_id` from `get_explore_page_sections` |
| Posts under a hashtag | `get_posts_by_hashtag` | Hashtag content research — pass hashtag name without `#` |
| Posts / Reels using a specific music track | `get_posts_using_specific_music` | Music trend analysis, sound-to-content attribution |

### Search Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| General keyword search (users, hashtags, places) | `general_search` | Broad multi-category discovery from a single query |
| Search hashtags by keyword | `search_hashtags` | Hashtag discovery, volume and relevance ranking |
| Search places / locations by keyword | `search_places` | Location-based content strategy, venue discovery |
| Search Reels by keyword | `search_reels` | Reels trend research — keyword must be passed as a JSON array |
| Search music by keyword | `search_music` | Audio trend discovery, sound sourcing for content creation |
| Search locations near GPS coordinates | `search_locations_by_coordinates` | Hyperlocal content strategy, geo-targeted discovery |
| Get cities / regions for a country | `get_cities_by_country` | Geographic market mapping, city-level targeting |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify the Discovery Objective and Select Nodes

Clarify the user's goal and map it to one or more nodes. Common research patterns:

- **Post analysis**: Resolve identifiers with `convert_shortcode_to_media_id` if needed → `get_post_info` → deepen with `get_post_likes` + `get_post_comments`.
- **Comment thread analysis**: `get_post_comments` → `get_comment_replies` for top comment threads.
- **Hashtag content research**: `search_hashtags` to discover relevant tags → `get_posts_by_hashtag` for content within each tag.
- **Music content attribution**: `search_music` to find a track → `get_posts_using_specific_music` with the returned `music_id`.
- **Explore page research**: `get_explore_page_sections` to list sections → `get_posts_by_section` to browse content in target sections.
- **Geo-local discovery**: `search_locations_by_coordinates` with latitude/longitude → `search_places` for city-level context.
- **Reels keyword research**: `search_reels` with keyword array → cross-reference with `get_posts_by_hashtag` for hashtag overlap.

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters, data types, and valid options:

```bash
node scripts/run.js --platform instagram --schema <tool_name>

# Examples
node scripts/run.js --platform instagram --schema get_post_comments
node scripts/run.js --platform instagram --schema search_reels
```

### Step 3 — Call APIs and Cache Results Locally

Execute tool calls and persist responses to the local cache.

**Calling a tool:**

```bash
node scripts/run.js --platform instagram --tool <tool_name> \
  --params '<json_args>' --pretty

# Skip cache for fresh results
node scripts/run.js --platform instagram --tool <tool_name> \
  --params '<json_args>' --no-cache --pretty
```

**Example — get post details:**

```bash
node scripts/run.js --platform instagram --tool get_post_info \
  --params '{"code_or_url":"DRhvwVLAHAG"}' --pretty
```

**Example — get comments (sorted by most popular):**

```bash
node scripts/run.js --platform instagram --tool get_post_comments \
  --params '{"code_or_url":"DRhvwVLAHAG","sort_by":"popular"}' --pretty
```

**Example — get replies to a specific comment:**

```bash
node scripts/run.js --platform instagram --tool get_comment_replies \
  --params '{"code_or_url":"DRhvwVLAHAG","comment_id":"18067775592012345"}' --pretty
```

**Example — get posts under a hashtag:**

```bash
node scripts/run.js --platform instagram --tool get_posts_by_hashtag \
  --params '{"hashtag":"travel"}' --pretty
```

**Example — search Reels (keyword as array):**

```bash
node scripts/run.js --platform instagram --tool search_reels \
  --params '{"keyword":["fitness"]}' --pretty
```

**Example — find posts using a music track:**

```bash
# First: search for the music to get music_id
node scripts/run.js --platform instagram --tool search_music \
  --params '{"keyword":"happy"}' --pretty

# Then: get posts using that track
node scripts/run.js --platform instagram --tool get_posts_using_specific_music \
  --params '{"music_id":"564058920086577"}' --pretty
```

**Pagination:**

Instagram content endpoints use token- or cursor-based pagination — not numeric page numbers.

| Endpoint | Pagination parameter | Notes |
|---|---|---|
| `get_post_comments`, `get_comment_replies`, `search_reels`, `general_search` | `pagination_token` | Pass token from previous response |
| `get_post_likes`, `get_posts_by_hashtag` | `end_cursor` | Pass cursor from previous response |
| `get_posts_using_specific_music`, `get_posts_by_section` | `max_id` | Pass cursor from previous response; leave empty for first call |
| `get_cities_by_country` | `page` (integer) | Numeric, starts at 1 |
| `convert_*`, `get_post_info`, `get_explore_page_sections`, `search_hashtags`, `search_places`, `search_music`, `search_locations_by_coordinates` | — | Single-call or non-paginated |

> **`search_reels` keyword type**: The `keyword` parameter is a **JSON array**, not a plain string. Always pass it as an array: `["keyword"]`.

**Explore page workflow:**

```bash
# Step 1: list available sections
node scripts/run.js --platform instagram --tool get_explore_page_sections \
  --params '{}' --pretty

# Step 2: browse posts in a specific section (use section_id from Step 1)
node scripts/run.js --platform instagram --tool get_posts_by_section \
  --params '{"section_id":"10156104410190727","count":20}' --pretty
```

**Cache directory structure:**

```
.keyapi-cache/
└── YYYY-MM-DD/
    ├── convert_shortcode_to_media_id/
    │   └── {params_hash}.json
    ├── convert_media_id_to_shortcode/
    │   └── {params_hash}.json
    ├── get_post_info/
    │   └── {params_hash}.json
    ├── get_post_likes/
    │   └── {params_hash}.json
    ├── get_post_comments/
    │   └── {params_hash}.json
    ├── get_comment_replies/
    │   └── {params_hash}.json
    ├── get_explore_page_sections/
    │   └── {params_hash}.json
    ├── get_posts_by_section/
    │   └── {params_hash}.json
    ├── get_posts_by_hashtag/
    │   └── {params_hash}.json
    ├── get_posts_using_specific_music/
    │   └── {params_hash}.json
    ├── general_search/
    │   └── {params_hash}.json
    ├── search_hashtags/
    │   └── {params_hash}.json
    ├── search_places/
    │   └── {params_hash}.json
    ├── search_reels/
    │   └── {params_hash}.json
    ├── search_music/
    │   └── {params_hash}.json
    ├── search_locations_by_coordinates/
    │   └── {params_hash}.json
    └── get_cities_by_country/
        └── {params_hash}.json
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists for the given parameters. If a valid cache file exists, load from disk and skip the API call.

### Step 4 — Synthesize and Report Findings

After collecting all API responses, produce a structured content intelligence report:

**For post analysis:**
1. **Post Overview** — Shortcode, media type (photo/video/carousel), caption, publish date, like count, comment count, views (if video).
2. **Engagement Analysis** — Like-to-comment ratio, top commenters, sentiment signals from comment keywords.
3. **Comment Thread Insights** — Most replied-to comments, key discussion themes, brand or product mentions.
4. **Audience Signals** — Who is engaging, public account patterns where available.

**For hashtag / topic research:**
1. **Hashtag Profile** — Name, post volume, top recent posts.
2. **Content Patterns** — Common media types, caption styles, co-occurring hashtags.
3. **Music Attribution** — Tracks driving Reels content within the hashtag.
4. **Opportunity Assessment** — Saturation vs. engagement quality, optimal posting windows.

**For music research:**
1. **Track Overview** — Title, artist, music ID, total usage count.
2. **Content Fit** — Types of posts using this track, associated hashtags, creator tier distribution.
3. **Trend Direction** — Growth or decline in adoption by comparing page depths.

**For location / geo research:**
1. **Location Index** — Place names, IDs, coverage radius.
2. **Local Content** — Top posts geotagged to target area, thematic clusters.
3. **City / Region Map** — Available cities per country for campaign geo-targeting.

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Common Rules

| Rule | Detail |
|------|--------|
| **`search_reels` keyword** | The `keyword` parameter is an **array type** — always pass as a JSON array: `["your_keyword"]`. Passing a plain string will cause a schema validation error. |
| **Post identification** | `get_post_info`, `get_post_likes`, `get_post_comments`, and `get_comment_replies` all accept either a shortcode (e.g., `DRhvwVLAHAG`) or a full post URL as `code_or_url`. |
| **Comment replies workflow** | Always call `get_post_comments` first to obtain `comment_id` values before calling `get_comment_replies`. |
| **Explore sections workflow** | Always call `get_explore_page_sections` first to obtain `section_id` values before calling `get_posts_by_section`. |
| **Hashtag format** | Pass hashtag names **without** the `#` symbol to `get_posts_by_hashtag` and `search_hashtags`. |
| **Music identification** | `get_posts_using_specific_music` accepts either `music_id` or `music_url` — pass one, not both. |
| **Pagination diversity** | Different endpoints use different pagination tokens (`pagination_token`, `end_cursor`, `max_id`). Always use the correct parameter for each endpoint. |
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
| `400` | Bad request — invalid or missing parameters | Validate input against the tool schema; check `keyword` array type for `search_reels`, `code_or_url` format, and required IDs |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `404` | Resource not found — post or hashtag may have been deleted or made private | Verify the shortcode/URL or hashtag name; the content may no longer be public |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry up to 3 times with a 2–3 second pause; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
