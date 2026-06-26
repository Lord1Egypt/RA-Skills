---
name: keyapi-youtube-channel-analysis
description: Discover, profile, and analyze YouTube channels — retrieve channel metadata, video libraries, convert between channel IDs and URLs, search channels by keyword, and explore advanced search with filters.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"📺"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-youtube-channel-analysis

> Discover, profile, and analyze YouTube channels — from identity resolution and metadata retrieval to video inventory, channel search, and advanced filtered discovery.

This skill provides comprehensive YouTube channel intelligence using the KeyAPI MCP service. It enables detailed channel profile retrieval (including a two-step process for full metadata), video library enumeration, bidirectional conversion between channel IDs and URLs, keyword-based channel search, within-channel content search, advanced filtered search across YouTube, and search suggestion retrieval — all through a cache-first workflow.

Use this skill when you need to:
- Retrieve full channel metadata including description, subscriber count, view count, join date, and social links
- Convert between channel URLs (various formats) and channel IDs, or resolve @username handles
- Enumerate a channel's published video library with pagination support
- Search for channels by keyword with result filtering to channel-type only
- Search within a specific channel's content by keyword
- Perform advanced YouTube searches with filters (upload time, duration, content type, features, sort order)
- Get real-time search suggestions for keyword research and autocomplete

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

### Channel Identity & Metadata Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Full channel metadata (two-step process) | `get_channel_description` | Complete channel audit — call twice: first with `channel_id`, then with `continuation_token` from response |
| Extract channel ID from any URL format | `get_channel_id_from_url` | URL normalization — supports @username, /channel/, /c/, /user/ formats |
| Get @username handle from channel ID | `get_channel_url_from_channel_id` | Reverse lookup — channel ID → @handle |
| Resolve channel name to channel ID | `get_channel_id` | Keyword-based ID lookup by channel name |

### Channel Content Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| List all videos from a channel | `get_channel_videos` | Video inventory, content cadence analysis — requires UC-format channel ID |

### Search & Discovery Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Search for channels by keyword | `search_channels` | Channel discovery — returns only channel-type results, filters out videos/playlists |
| Search within a specific channel | `search_channel` | In-channel content search by keyword — requires channel ID |
| Advanced filtered search across YouTube | `general_search_with_filters` | Precision discovery — filter by upload time, duration, content type, features, sort order |
| Get search suggestions / autocomplete | `get_search_suggestions` | Keyword research, query expansion — returns 10–20 suggestions in <1 second |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify the Channel Analysis Objective and Select Nodes

Clarify the research goal and map it to one or more nodes. Common patterns:

- **Channel profile deep-dive**: Use `get_channel_description` **twice** — first call with `channel_id` returns basic info + `continuation_token`; second call with that token returns advanced info (join date, social links, view count).
- **URL → ID conversion**: Use `get_channel_id_from_url` to normalize any channel URL format to a channel ID.
- **ID → @handle conversion**: Use `get_channel_url_from_channel_id` to get the user-friendly @username from a channel ID.
- **Channel discovery**: Use `search_channels` with keyword → optionally deepen with `get_channel_description` for each result.
- **Video inventory**: Use `get_channel_videos` with `channel_id` (must be UC-format) → paginate with `continuation_token`.
- **Advanced search**: Use `general_search_with_filters` with upload time, duration, content type, and sort filters.

> **Channel ID formats**
>
> - **UC-format**: 24-character string starting with `UC` (e.g., `UCeu6U67OzJhV1KwBansH3Dg`) — required for `get_channel_videos` and `get_channel_description`.
> - **@username format**: User-friendly handle (e.g., `@CozyCraftYT`) — use `get_channel_id_from_url` to convert to UC-format.
> - **URL formats**: Supports `youtube.com/@username`, `youtube.com/channel/UCxxxxxx`, `youtube.com/c/name`, `youtube.com/user/name`.

> **`get_channel_description` two-step process**
>
> This endpoint requires **two sequential calls** to retrieve complete channel information:
> 1. **First call**: Pass `channel_id` → returns basic info (name, description, subscriber count, video count, banner) + `continuation_token`.
> 2. **Second call**: Pass `continuation_token` from step 1 → returns advanced info (join date, social media links, featured sections, total view count).
>
> Do NOT call both simultaneously — the second call depends on the token from the first.

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters and available options:

```bash
node scripts/run.js --platform youtube --schema <tool_name>

# Examples
node scripts/run.js --platform youtube --schema get_channel_description
node scripts/run.js --platform youtube --schema general_search_with_filters
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

**Example — get full channel metadata (two-step):**

```bash
# Step 1: Get basic info + continuation_token
node scripts/run.js --platform youtube --tool get_channel_description \
  --params '{"channel_id":"UCeu6U67OzJhV1KwBansH3Dg","language_code":"en-US","country_code":"US","need_format":true}' --pretty

# Step 2: Get advanced info using continuation_token from Step 1
node scripts/run.js --platform youtube --tool get_channel_description \
  --params '{"continuation_token":"<token_from_step_1>","language_code":"en-US","country_code":"US","need_format":true}' --pretty
```

**Example — convert channel URL to ID:**

```bash
node scripts/run.js --platform youtube --tool get_channel_id_from_url \
  --params '{"channel_url":"https://www.youtube.com/@CozyCraftYT"}' --pretty
```

**Example — get @handle from channel ID:**

```bash
node scripts/run.js --platform youtube --tool get_channel_url_from_channel_id \
  --params '{"channel_id":"UCeu6U67OzJhV1KwBansH3Dg"}' --pretty
```

**Example — get channel videos (first page):**

```bash
node scripts/run.js --platform youtube --tool get_channel_videos \
  --params '{"channel_id":"UCJHBJ7F-nAIlMGolm0Hu4vg","language_code":"en-US","country_code":"US"}' --pretty
```

**Example — paginate to next video page:**

```bash
node scripts/run.js --platform youtube --tool get_channel_videos \
  --params '{"channel_id":"UCJHBJ7F-nAIlMGolm0Hu4vg","continuation_token":"<token>"}' --pretty
```

**Example — search channels by keyword:**

```bash
# First page
node scripts/run.js --platform youtube --tool search_channels \
  --params '{"keyword":"fitness","need_format":true}' --pretty

# Next page
node scripts/run.js --platform youtube --tool search_channels \
  --params '{"continuation_token":"<token>","need_format":true}' --pretty
```

**Example — search within a channel:**

```bash
node scripts/run.js --platform youtube --tool search_channel \
  --params '{"channel_id":"UCXuqSBlHAE6Xw-yeJA0Tunw","search_query":"AMD","language_code":"en","country_code":"US"}' --pretty
```

**Example — advanced filtered search:**

```bash
node scripts/run.js --platform youtube --tool general_search_with_filters \
  --params '{"search_query":"Python tutorial","upload_time":"month","duration":"medium","content_type":"video","feature":"hd","sort_by":"view_count","language_code":"en-US","country_code":"US"}' --pretty
```

**Example — get search suggestions:**

```bash
node scripts/run.js --platform youtube --tool get_search_suggestions \
  --params '{"keyword":"machine learning","language":"en","region":"US"}' --pretty
```

**Example — resolve channel name to ID:**

```bash
node scripts/run.js --platform youtube --tool get_channel_id \
  --params '{"channel_name":"LinusTechTips"}' --pretty
```

**Pagination:**

| Endpoint | Pagination | Notes |
|---|---|---|
| `get_channel_description` | `continuation_token` | Two-step: first call returns token for second call |
| `get_channel_videos` | `continuation_token` | From previous response |
| `search_channels`, `search_channel`, `general_search_with_filters` | `continuation_token` | From previous response |
| `get_channel_id_from_url`, `get_channel_url_from_channel_id`, `get_channel_id`, `get_search_suggestions` | — | Single-call; no pagination |

**Cache directory structure:**

```
.keyapi-cache/
└── YYYY-MM-DD/
    ├── get_channel_description/
    │   └── {params_hash}.json
    ├── get_channel_id_from_url/
    │   └── {params_hash}.json
    ├── get_channel_url_from_channel_id/
    │   └── {params_hash}.json
    ├── get_channel_videos/
    │   └── {params_hash}.json
    ├── get_channel_id/
    │   └── {params_hash}.json
    ├── search_channels/
    │   └── {params_hash}.json
    ├── search_channel/
    │   └── {params_hash}.json
    ├── general_search_with_filters/
    │   └── {params_hash}.json
    └── get_search_suggestions/
        └── {params_hash}.json
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists. If valid, load from disk and skip the API call.

### Step 4 — Synthesize and Report Findings

**For channel analysis:**
1. **Channel Overview** — Name, @handle, channel ID, subscriber count, total video count, total view count, join date, verification status.
2. **Channel Description** — Bio, featured links, social media connections, country/language.
3. **Content Inventory** — Video count, upload frequency, most recent video date, content categories.
4. **Audience Signals** — Subscriber-to-view ratio, engagement indicators from recent videos.
5. **Featured Sections** — Playlists, channels, or content highlighted by the creator.

**For channel discovery:**
1. **Search Results Overview** — Matched channels, subscriber counts, verification status, content focus.
2. **Comparative Analysis** — Side-by-side metrics for shortlisted channels.
3. **Keyword Expansion** — Search suggestions for related queries, trending topics.

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Common Rules

| Rule | Detail |
|------|--------|
| **Channel ID format** | `get_channel_videos` and `get_channel_description` require UC-format channel IDs (24 characters starting with `UC`). Use `get_channel_id_from_url` to convert @username or other URL formats. |
| **`get_channel_description` two-step** | **Critical**: This endpoint requires two sequential calls. First call with `channel_id` returns basic info + `continuation_token`. Second call with that token returns advanced info. Do NOT call both simultaneously. |
| **URL format support** | `get_channel_id_from_url` supports multiple formats: `@username`, `/channel/UCxxxxxx`, `/c/name`, `/user/name`. |
| **`search_channels` vs `search_channel`** | `search_channels` searches across YouTube for channels by keyword. `search_channel` searches within a specific channel's content. |
| **`need_format` parameter quirk** | The `get_channel_videos` schema has a trailing space in the parameter name: `"need_format "` (with space). However, the API accepts both forms. Omit this parameter in examples to avoid confusion. Available on `get_channel_description` and `search_channels` without the space issue. |
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
| `400` | Bad request — invalid or missing parameters | Validate input against the tool schema; check channel ID format (must be UC-format for some endpoints), URL format, and required fields |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `404` | Resource not found — channel may not exist or URL is invalid | Verify the channel ID or URL; the channel may have been deleted or made private |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry up to 3 times with a 2–3 second pause; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
