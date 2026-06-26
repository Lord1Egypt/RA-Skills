---
name: keyapi-twitter-content-analytics
description: Explore and analyze Twitter/X content at scale — retrieve user profiles, tweets, comments, replies, media, search across content types, monitor trending topics, and analyze follower/following networks.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"🐦"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-twitter-content-analytics

> Explore and analyze Twitter/X content at scale — from user profiles and tweet threads to search, trending topics, and social graph analysis.

This skill provides comprehensive Twitter/X intelligence using the KeyAPI MCP service. It enables detailed tweet inspection, user profile retrieval, comment and reply thread analysis, media library enumeration, multi-type search (Top, Latest, Media, People, Lists), trending topic monitoring across countries, and follower/following network exploration — all through a cache-first workflow.

Use this skill when you need to:
- Retrieve full tweet details including engagement metrics, media, and quoted content
- Fetch user profiles with follower counts, bio, verification status, and account metadata
- Analyze a user's tweet timeline, replies, and media library
- Read comment threads under any tweet with pagination support
- Search Twitter by keyword across multiple result types (Top, Latest, Media, People, Lists)
- Monitor trending topics and hashtags by country or globally
- Explore social graphs — analyze who a user follows and who follows them
- Identify users who retweeted a specific tweet

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

All tool calls in this skill target the KeyAPI Twitter MCP server:

```
Server URL : https://mcp.keyapi.ai/twitter/mcp
Auth Header: Authorization: Bearer $KEYAPI_TOKEN
```

**Setup (one-time):**

```bash
# 1. Install dependencies
npm install

# 2. Set your API token (get one free at https://keyapi.ai/)
export KEYAPI_TOKEN=your_token_here

# 3. List all available tools to verify the connection
node scripts/run.js --platform twitter --list-tools
```

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Analysis Scenarios

### Tweet & User Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Full tweet details (metrics, media, quoted content) | `get_single_tweet_data` | Tweet audit, engagement snapshot — requires `tweet_id` from URL |
| User profile with bio, follower counts, verification | `get_user_profile` | Profile overview — accepts `screen_name` or `rest_id` |
| User's tweet timeline | `get_user_post` | Content inventory, posting cadence analysis — accepts `screen_name` or `rest_id` |
| User's tweet replies | `get_user_tweet_replies` | Reply activity, conversation participation — requires `screen_name` only |
| User's media library (photos/videos) | `get_user_media` | Visual content audit — requires `screen_name` only |

### Comment & Engagement Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Comments under a tweet | `get_comments` | Audience sentiment, comment volume analysis |
| Users who retweeted a tweet | `retweet_user_list` | Amplification analysis, retweet network mapping |

### Search & Discovery Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Search by keyword (multi-type) | `search` | Broad discovery — filter by Top, Latest, Media, People, Lists |
| Trending topics by country | `trending` | Real-time trend monitoring — supports 50+ countries |

### Social Graph Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Users a profile is following | `user_followings` | Network affinity, brand partnership signals — requires `screen_name` only |
| Users following a profile | `user_followers` | Audience sampling, follower demographics — requires `screen_name` only |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify the Analysis Objective and Select Nodes

Clarify the research goal and map it to one or more nodes. Common patterns:

- **Tweet analysis**: Extract `tweet_id` from URL → `get_single_tweet_data` → deepen with `get_comments` + `retweet_user_list`.
- **User profile audit**: Use `get_user_profile` with `screen_name` → layer `get_user_post` + `get_user_tweet_replies` + `get_user_media`.
- **Search research**: Use `search` with keyword and `search_type` filter → paginate with `cursor` for more results.
- **Trend monitoring**: Use `trending` with `country` parameter → cross-reference with `search` for content depth.
- **Social graph analysis**: Use `user_followings` + `user_followers` with `screen_name` → paginate with `cursor`.

> **User identification**
>
> Most endpoints accept either `screen_name` (e.g., `elonmusk`) or `rest_id` (numeric user ID, e.g., `44196397`) — pass one, not both.
> - `get_user_profile` and `get_user_post` accept both `screen_name` and `rest_id`.
> - `get_user_tweet_replies`, `get_user_media`, `user_followings`, and `user_followers` require **`screen_name` only** — no `rest_id` option.

> **Tweet ID extraction**
>
> Extract the tweet ID from the URL:
> - `https://x.com/elonmusk/status/1808168603721650364` → `1808168603721650364`

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters and available options:

```bash
node scripts/run.js --platform twitter --schema <tool_name>

# Examples
node scripts/run.js --platform twitter --schema get_single_tweet_data
node scripts/run.js --platform twitter --schema search
```

### Step 3 — Call APIs and Cache Results Locally

Execute tool calls and persist responses to the local cache.

**Calling a tool:**

```bash
node scripts/run.js --platform twitter --tool <tool_name> \
  --params '<json_args>' --pretty

# Skip cache for fresh results
node scripts/run.js --platform twitter --tool <tool_name> \
  --params '<json_args>' --no-cache --pretty
```

**Example — get tweet details:**

```bash
node scripts/run.js --platform twitter --tool get_single_tweet_data \
  --params '{"tweet_id":"1808168603721650364"}' --pretty
```

**Example — get user profile:**

```bash
node scripts/run.js --platform twitter --tool get_user_profile \
  --params '{"screen_name":"elonmusk"}' --pretty
```

**Example — get user tweets (first page):**

```bash
node scripts/run.js --platform twitter --tool get_user_post \
  --params '{"screen_name":"elonmusk"}' --pretty
```

**Example — paginate to next page:**

```bash
node scripts/run.js --platform twitter --tool get_user_post \
  --params '{"screen_name":"elonmusk","cursor":"<next_cursor_from_previous_response>"}' --pretty
```

**Example — get comments under a tweet:**

```bash
node scripts/run.js --platform twitter --tool get_comments \
  --params '{"tweet_id":"1808168603721650364"}' --pretty
```

**Example — search by keyword (Top results):**

```bash
node scripts/run.js --platform twitter --tool search \
  --params '{"keyword":"AI","search_type":"Top"}' --pretty
```

**Example — search for latest tweets:**

```bash
node scripts/run.js --platform twitter --tool search \
  --params '{"keyword":"ChatGPT","search_type":"Latest"}' --pretty
```

**Example — get trending topics (United States):**

```bash
node scripts/run.js --platform twitter --tool trending \
  --params '{"country":"UnitedStates"}' --pretty
```

**Example — get trending topics (Japan):**

```bash
node scripts/run.js --platform twitter --tool trending \
  --params '{"country":"Japan"}' --pretty
```

**Example — get user's followings:**

```bash
node scripts/run.js --platform twitter --tool user_followings \
  --params '{"screen_name":"elonmusk"}' --pretty
```

**Example — get user's followers:**

```bash
node scripts/run.js --platform twitter --tool user_followers \
  --params '{"screen_name":"elonmusk"}' --pretty
```

**Example — get retweet user list:**

```bash
node scripts/run.js --platform twitter --tool retweet_user_list \
  --params '{"tweet_id":"1835124037934367098"}' --pretty
```

**Pagination:**

All paginated endpoints use `cursor` from the `next_cursor` field in the previous response.

| Endpoint | Pagination parameter | Notes |
|---|---|---|
| `get_user_post`, `search`, `get_comments`, `get_user_tweet_replies`, `get_user_media`, `retweet_user_list`, `user_followings`, `user_followers` | `cursor` | Pass `next_cursor` value from previous response |
| `get_single_tweet_data`, `get_user_profile`, `trending` | — | Single-call; no pagination |

**Cache directory structure:**

```
.keyapi-cache/
└── YYYY-MM-DD/
    ├── get_single_tweet_data/
    │   └── {params_hash}.json
    ├── get_user_profile/
    │   └── {params_hash}.json
    ├── get_user_post/
    │   └── {params_hash}.json
    ├── search/
    │   └── {params_hash}.json
    ├── get_comments/
    │   └── {params_hash}.json
    ├── get_user_tweet_replies/
    │   └── {params_hash}.json
    ├── get_user_media/
    │   └── {params_hash}.json
    ├── retweet_user_list/
    │   └── {params_hash}.json
    ├── trending/
    │   └── {params_hash}.json
    ├── user_followings/
    │   └── {params_hash}.json
    └── user_followers/
        └── {params_hash}.json
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists. If valid, load from disk and skip the API call.

### Step 4 — Synthesize and Report Findings

**For tweet analysis:**
1. **Tweet Overview** — Text content, author, publish date, view count, like count, retweet count, reply count, quote count.
2. **Engagement Analysis** — Like-to-view ratio, retweet amplification, comment depth.
3. **Media & Links** — Attached images/videos, external links, quoted tweets.
4. **Comment Insights** — Top comment themes, sentiment signals, key discussion points.
5. **Retweet Network** — Who amplified the tweet, account types, reach estimation.

**For user analysis:**
1. **Profile Overview** — Screen name, display name, bio, follower count, following count, tweet count, verification status, account creation date.
2. **Content Patterns** — Posting frequency, media usage, reply activity, content themes.
3. **Social Graph** — Follower-to-following ratio, notable followings/followers where available.
4. **Engagement Quality** — Average engagement per tweet, reply rate, retweet rate.

**For search / discovery:**
1. **Search Results Overview** — Result count, top tweets/users, engagement distribution.
2. **Trending Topics** — Current trending hashtags and topics by country, volume indicators.
3. **Content Themes** — Common topics, hashtags, and discussion patterns.

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Common Rules

| Rule | Detail |
|------|--------|
| **User identification** | `get_user_profile` and `get_user_post` accept `screen_name` or `rest_id`. `get_user_tweet_replies`, `get_user_media`, `user_followings`, and `user_followers` require **`screen_name` only**. |
| **Tweet ID extraction** | Extract from URL: `x.com/user/status/TWEET_ID` or `twitter.com/user/status/TWEET_ID`. |
| **Search types** | `search` supports: `Top` (default), `Latest`, `Media`, `People`, `Lists`. |
| **Trending countries** | `trending` supports 50+ countries including: `UnitedStates`, `China`, `India`, `Japan`, `Russia`, `Germany`, `UnitedKingdom`, `France`, `Brazil`, `Canada`, `Australia`, `SouthKorea`, `Mexico`, `Spain`, `Italy`, `Turkey`, `Indonesia`, `SaudiArabia`, `Egypt`, `Argentina`, `Philippines`, `Singapore`, and more. See schema for full list. |
| **Pagination** | All paginated endpoints use `cursor` from the `next_cursor` field in the previous response. |
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
| `400` | Bad request — invalid or missing parameters | Validate input against the tool schema; check `tweet_id` format, `screen_name` vs `rest_id` requirements, and search type values |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `404` | Resource not found — tweet or user may be deleted, suspended, or private | Verify the tweet ID or screen name; the content may no longer be available |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry up to 3 times with a 2–3 second pause; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
