---
name: keyapi-youtube-video-analysis
description: Analyze YouTube videos at depth — retrieve full metadata, comments, sub-comment threads, stream formats, related video recommendations, Shorts, search results, and trending content across categories.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"🎬"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-youtube-video-analysis

> Analyze YouTube videos at depth — from full metadata and stream formats to comment threads, related recommendations, Shorts discovery, and trending video intelligence.

This skill provides comprehensive YouTube video intelligence using the KeyAPI MCP service. It enables detailed video inspection (metadata, views, engagement), layered comment analysis (top-level comments + nested replies), playback stream retrieval, related content discovery, Shorts-specific search, keyword-based video search, and trending video monitoring — all through a cache-first workflow.

Use this skill when you need to:
- Retrieve complete metadata, engagement metrics, and raw player data for any YouTube video
- Read and analyze top-level comments and their nested reply threads
- Obtain all available playback stream URLs and quality levels for a video
- Discover related and recommended videos as surfaced by the YouTube algorithm
- Search YouTube Shorts by keyword with category and time-based filtering
- Find videos by keyword with advanced sort and recency filters
- Monitor trending videos globally or by category (Music, Gaming, Movies)

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

All tool calls in this skill target the KeyAPI YouTube MCP server:

```
Server URL : https://mcp.keyapi.ai/youtube/mcp
Auth Header: Authorization: Bearer $KEYAPI_TOKEN
```

**Setup (one-time):**

```bash
# 1. Install dependencies
npm install

# 2. Set your API token (get one free at https://keyapi.ai/)
export KEYAPI_TOKEN=your_token_here

# 3. List all available tools to verify the connection
node scripts/run.js --platform youtube --list-tools
```

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Analysis Scenarios

### Video Data Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Full video metadata, stats, and raw player data | `get_video_information` | Complete video audit — title, description, views, likes, tags, chapters, `playerResponse` + `initialData` |
| Video comments (top-level) | `get_video_comments` | Audience sentiment, comment volume analysis — sortable by `top` or `newest` |
| Replies to a specific comment | `get_video_sub_comments` | Nested conversation thread analysis — requires `reply_continuation_token` from a comment |
| All playback stream URLs and quality levels | `get_video_streams_info` | Download URL extraction, quality enumeration (standard merged + adaptive formats) |
| Related / recommended videos | `get_related_videos` | Algorithm-surfaced content map — returns 20–30 recommendations in one call |

### Search & Discovery Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Search YouTube Shorts by keyword | `youtube_shorts_search` | Shorts-specific content research — use `continuation_token` for pure Shorts after first call |
| Search regular videos by keyword | `search_video` | General video discovery with recency filter (this_week / this_month / this_year / last_hour / today) |
| Get trending videos by category | `get_trending_videos` | Market pulse — categories: Now (default), Music, Gaming, Movies |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify the Video Analysis Objective and Select Nodes

Clarify the research goal and map it to one or more nodes. Common patterns:

- **Video deep-dive**: Start with `get_video_information` (set `need_format: true` for clean structured output), then layer `get_video_comments` and `get_video_streams_info`.
- **Comment thread analysis**: `get_video_comments` → collect `reply_continuation_token` from comments with replies → `get_video_sub_comments` per thread.
- **Related content mapping**: `get_related_videos` returns the full recommendation set in one call — no pagination needed.
- **Shorts research**: `youtube_shorts_search` with keyword → use `continuation_token` for pure Shorts on subsequent pages.
- **Trend monitoring**: `get_trending_videos` with section filter → cross-reference with `search_video` by keyword.

> **Video ID extraction**
>
> Extract the video ID from the URL:
> - `https://www.youtube.com/watch?v=oaSNBz4qMQY` → `oaSNBz4qMQY`
>
> Most endpoints accept either `video_id` (recommended) or `video_url` (full URL string) — use `video_id` where possible for reliability.

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters and available options:

```bash
node scripts/run.js --platform youtube --schema <tool_name>

# Examples
node scripts/run.js --platform youtube --schema get_video_information
node scripts/run.js --platform youtube --schema youtube_shorts_search
```

### Step 3 — Call APIs and Cache Results Locally

Execute tool calls and persist responses to the local cache.

**Calling a tool:**

```bash
node scripts/run.js --platform youtube --tool <tool_name> \
  --params '<json_args>' --pretty

# Skip cache for fresh results
node scripts/run.js --platform youtube --tool <tool_name> \
  --params '<json_args>' --no-cache --pretty
```

**Example — get full video information (formatted):**

```bash
node scripts/run.js --platform youtube --tool get_video_information \
  --params '{"video_id":"oaSNBz4qMQY","need_format":true,"language_code":"en-US"}' --pretty
```

**Example — get top comments:**

```bash
node scripts/run.js --platform youtube --tool get_video_comments \
  --params '{"video_id":"oaSNBz4qMQY","sort_by":"top","language_code":"en-US","country_code":"US"}' --pretty
```

**Example — paginate to next comment page:**

```bash
node scripts/run.js --platform youtube --tool get_video_comments \
  --params '{"video_id":"oaSNBz4qMQY","continuation_token":"<token_from_previous_response>"}' --pretty
```

**Example — get replies to a comment:**

```bash
# Extract reply_continuation_token from a comment in get_video_comments response
node scripts/run.js --platform youtube --tool get_video_sub_comments \
  --params '{"continuation_token":"<reply_continuation_token>","language_code":"en-US"}' --pretty
```

**Example — get related videos:**

```bash
node scripts/run.js --platform youtube --tool get_related_videos \
  --params '{"video_id":"dQw4w9WgXcQ","need_format":true}' --pretty
```

**Example — search Shorts:**

```bash
# First call (may return mixed content)
node scripts/run.js --platform youtube --tool youtube_shorts_search \
  --params '{"search_query":"cooking tips","filter_mixed_content":true,"language_code":"en-US","country_code":"US"}' --pretty

# Subsequent pages (pure Shorts via continuation_token)
node scripts/run.js --platform youtube --tool youtube_shorts_search \
  --params '{"search_query":"cooking tips","continuation_token":"<token>"}' --pretty
```

**Example — search videos with recency filter:**

```bash
node scripts/run.js --platform youtube --tool search_video \
  --params '{"search_query":"AI tutorial","order_by":"this_month","country_code":"US","language_code":"en"}' --pretty
```

**Example — get trending videos:**

```bash
node scripts/run.js --platform youtube --tool get_trending_videos \
  --params '{"section":"Music","country_code":"US","language_code":"en"}' --pretty
```

**Pagination:**

| Endpoint | Pagination | Notes |
|---|---|---|
| `get_video_comments` | `continuation_token` | From previous response |
| `get_video_sub_comments` | `continuation_token` | Must use `reply_continuation_token` field from a comment — NOT the video comment pagination token |
| `youtube_shorts_search`, `search_video` | `continuation_token` | From previous response |
| `get_video_information`, `get_video_streams_info`, `get_related_videos`, `get_trending_videos` | — | Single-call; no pagination |

> **`get_video_sub_comments` critical note**: This endpoint requires the `reply_continuation_token` field extracted from a specific comment in the `get_video_comments` response — it is different from the comment-level `continuation_token` used to paginate comments. Do NOT pass the video_id to this endpoint.

> **`get_video_streams_info` time limit**: Returned playback URLs are valid for approximately 6 hours. Use them promptly. HD video (720p+) streams require separate audio and video downloads that must be merged locally.

> **`youtube_shorts_search` mixed content**: The first request may return a mix of Shorts and regular videos. Use `continuation_token` on subsequent calls for pure Shorts results. Set `filter_mixed_content: true` (default) to filter long videos from the first response.

**Cache directory structure:**

```
.keyapi-cache/
└── YYYY-MM-DD/
    ├── get_video_information/
    │   └── {params_hash}.json
    ├── get_video_comments/
    │   └── {params_hash}.json
    ├── get_video_sub_comments/
    │   └── {params_hash}.json
    ├── get_video_streams_info/
    │   └── {params_hash}.json
    ├── get_related_videos/
    │   └── {params_hash}.json
    ├── youtube_shorts_search/
    │   └── {params_hash}.json
    ├── search_video/
    │   └── {params_hash}.json
    └── get_trending_videos/
        └── {params_hash}.json
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists. If valid, load from disk and skip the API call.

### Step 4 — Synthesize and Report Findings

**For video analysis:**
1. **Video Overview** — Title, channel, publish date, view count, like count, comment count, duration, tags, description summary.
2. **Engagement Quality** — Like-to-view ratio, comment depth (replies per top-level comment), engagement rate estimate.
3. **Comment Intelligence** — Top themes from most-liked comments, sentiment signals, key community questions or reactions.
4. **Related Content Map** — Algorithm-recommended videos, common topics and channels in the recommendation cluster.
5. **Stream Quality Summary** — Available resolutions, format types (merged vs. adaptive), playback URL validity window.

**For search / discovery:**
1. **Search Results Overview** — Video count returned, top titles, channel distribution, view spread.
2. **Shorts Landscape** — Trending Shorts topics, creator diversity, engagement patterns.
3. **Trending Signals** — Top trending videos by category, creator names, view velocity indicators.

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Common Rules

| Rule | Detail |
|------|--------|
| **Video ID extraction** | Extract from URL: `youtube.com/watch?v=VIDEO_ID`. Use `video_id` parameter where available; `video_url` is also accepted by `get_video_streams_info` and `get_related_videos`. |
| **`get_video_sub_comments`** | Requires `continuation_token` from the `reply_continuation_token` field of a comment returned by `get_video_comments` — not the video-level pagination token and not the video ID. |
| **Shorts first-call behavior** | The first `youtube_shorts_search` call may return mixed content. Use `continuation_token` for subsequent pages to receive pure Shorts. Use `filter_mixed_content: true` to auto-filter on the first call. |
| **Stream URL validity** | `get_video_streams_info` returns time-limited URLs (~6 hours). Process immediately after retrieval. |
| **`need_format` parameter** | Available on `get_video_information`, `get_related_videos`, and `get_video_comments`. Set to `true` for structured, cleaned output; `false` for raw YouTube API data useful for debugging. |
| **Language / region params** | `language_code` and `country_code` influence result language and regional content bias. Use `en-US` / `US` for English-language global results. |
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
| `400` | Bad request — invalid or missing parameters | Validate input against the tool schema; check `video_id` format, `continuation_token` source, and required fields |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `404` | Resource not found — video may be deleted, private, or region-restricted | Verify the video ID; the content may no longer be available |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry up to 3 times with a 2–3 second pause; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
