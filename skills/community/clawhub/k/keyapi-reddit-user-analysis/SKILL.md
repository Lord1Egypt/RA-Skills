---
name: keyapi-reddit-user-analysis
description: Discover and analyze Reddit users and subreddits — retrieve user profiles, active communities, public trophies, subreddit rules, settings, post channels, and perform dynamic search with typeahead suggestions and trending search intelligence.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"🔎"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-reddit-user-analysis

> Discover and analyze Reddit users and subreddits — from user profiles and community activity to subreddit governance, search intelligence, and trending topic discovery.

This skill provides comprehensive Reddit user and community intelligence using the KeyAPI MCP service. It enables retrieval of user profiles, active subreddit memberships, public trophies, subreddit rules and style, post channels, settings, mute status, and powerful search capabilities including typeahead suggestions, dynamic multi-type search, and trending search topics — all through a unified, cache-first workflow.

Use this skill when you need to:
- Retrieve a Reddit user's public profile, karma breakdown, and account metadata
- Identify the subreddits a user is most active in
- Audit a user's public trophies and achievement history
- Research subreddit rules, style guidelines, and community settings
- Discover post channels and content categories within a subreddit
- Search Reddit for posts, communities, users, comments, and media
- Monitor trending search topics across the platform

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

All tool calls in this skill target the KeyAPI Reddit MCP server:

```
Server URL : https://mcp.keyapi.ai/reddit/mcp
Auth Header: Authorization: Bearer $KEYAPI_TOKEN
```

**Setup (one-time):**

```bash
# 1. Install dependencies
npm install

# 2. Set your API token (get one free at https://keyapi.ai/)
export KEYAPI_TOKEN=your_token_here

# 3. List all available tools to verify the connection
node scripts/run.js --platform reddit --list-tools
```

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Analysis Scenarios

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| User profile, karma, account age | `fetch_reddit_app_user_profile` | User identity research, credibility assessment |
| Most active subreddits for a user | `fetch_users_active_subreddits` | Community affiliation mapping, interest profiling |
| User's public trophies and achievements | `fetch_user_public_trophies` | Account reputation, milestone tracking |
| Subreddit rules and style info | `fetch_reddit_app_subreddit_rules_and_style_info` | Community governance research, moderation policy |
| Subreddit post channels / content categories | `fetch_reddit_app_subreddit_post_channels` | Content taxonomy, channel structure |
| Subreddit general info and metadata | `fetch_reddit_app_subreddit_info` | Community overview, subscriber count, description |
| Subreddit settings and moderation config | `fetch_reddit_app_subreddit_settings` | Admin/moderation research, policy analysis |
| Check if a subreddit is muted | `check_if_subreddit_is_muted` | Mute status verification |
| Search autocomplete suggestions | `fetch_reddit_app_search_typeahead_suggestions` | Query refinement, subreddit/user discovery |
| Dynamic multi-type search | `fetch_reddit_app_dynamic_search_results` | Posts, communities, comments, media, user search |
| Platform-wide trending searches | `fetch_reddit_app_trending_searches` | Trend intelligence, topic monitoring |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify Analysis Targets and Select Nodes

Clarify the research objective and map it to one or more nodes. Typical entry points:

- **User research**: Use `fetch_reddit_app_user_profile` → `fetch_users_active_subreddits` → `fetch_user_public_trophies`.
- **Subreddit audit**: Use `fetch_reddit_app_subreddit_info` → `fetch_reddit_app_subreddit_rules_and_style_info` → `fetch_reddit_app_subreddit_post_channels`.
- **Search workflow**: Use `fetch_reddit_app_search_typeahead_suggestions` to refine query, then `fetch_reddit_app_dynamic_search_results` for full results.
- **Trend monitoring**: Use `fetch_reddit_app_trending_searches` (no parameters required).

> **Subreddit Identifier: `subreddit_name` vs. `subreddit_id`**
>
> Two different identifiers are used across subreddit endpoints:
> - `subreddit_name` — the display name (e.g., `technology`, `worldnews`). Used by `fetch_reddit_app_subreddit_rules_and_style_info`, `fetch_reddit_app_subreddit_post_channels`, `fetch_reddit_app_subreddit_info`.
> - `subreddit_id` — the internal ID with a **`t5_` prefix** (e.g., `t5_2qh0u`). Required by `fetch_reddit_app_subreddit_settings`, `check_if_subreddit_is_muted`, `fetch_reddit_app_community_highlights`.
>
> Call `fetch_reddit_app_subreddit_info` with `subreddit_name` first to obtain the `subreddit_id` when needed.

> **`fetch_reddit_app_trending_searches`**
>
> This endpoint requires no parameters. Call it directly to retrieve the current list of trending search topics across Reddit.

> **`need_format` Parameter**
>
> Most endpoints accept an optional `need_format` boolean. Set to `true` for sanitized/cleaned response data. Defaults to `false`.

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters and available options:

```bash
node scripts/run.js --platform reddit --schema <tool_name>

# Examples
node scripts/run.js --platform reddit --schema fetch_reddit_app_user_profile
node scripts/run.js --platform reddit --schema fetch_reddit_app_dynamic_search_results
```

### Step 3 — Call APIs and Cache Results Locally

Execute tool calls and persist responses to the local cache to avoid redundant API calls.

**Calling a tool:**

```bash
# Single call with pretty output
node scripts/run.js --platform reddit --tool <tool_name> \
  --params '<json_args>' --pretty

# Force fresh data, skip cache
node scripts/run.js --platform reddit --tool <tool_name> \
  --params '<json_args>' --no-cache --pretty
```

**Example — get user profile:**

```bash
node scripts/run.js --platform reddit --tool fetch_reddit_app_user_profile \
  --params '{"username":"spez"}' --pretty
```

**Example — get user's active subreddits:**

```bash
node scripts/run.js --platform reddit --tool fetch_users_active_subreddits \
  --params '{"username":"spez"}' --pretty
```

**Example — get subreddit post channels (with sort and range):**

```bash
node scripts/run.js --platform reddit --tool fetch_reddit_app_subreddit_post_channels \
  --params '{"subreddit_name":"technology","sort":"HOT","range":"DAY"}' --pretty
```

**Example — get subreddit settings (requires t5_ prefixed subreddit_id):**

```bash
node scripts/run.js --platform reddit --tool fetch_reddit_app_subreddit_settings \
  --params '{"subreddit_id":"t5_2qh0u"}' --pretty
```

**Example — get subreddit info:**

```bash
node scripts/run.js --platform reddit --tool fetch_reddit_app_subreddit_info \
  --params '{"subreddit_name":"technology"}' --pretty
```

**Example — dynamic search for posts:**

```bash
node scripts/run.js --platform reddit --tool fetch_reddit_app_dynamic_search_results \
  --params '{"query":"AI regulation","search_type":"post","sort":"RELEVANCE","time_range":"month"}' --pretty
```

**Example — get trending searches (no params):**

```bash
node scripts/run.js --platform reddit --tool fetch_reddit_app_trending_searches \
  --params '{}' --pretty
```

**`fetch_reddit_app_dynamic_search_results` options:**

| Parameter | Options | Description |
|---|---|---|
| `search_type` | `post`, `community`, `comment`, `media`, `user` | Type of content to search (singular form) |
| `sort` | `RELEVANCE`, `HOT`, `TOP`, `NEW`, `COMMENTS` | Sort order (uppercase) |
| `time_range` | `all`, `hour`, `day`, `week`, `month`, `year` | Time filter |
| `safe_search` | `"unset"`, `"on"`, `"off"` | Safe search setting (string, not boolean) |
| `allow_nsfw` | `"0"` (exclude), `"1"` (include) | NSFW content filter (string, not boolean) |
| `after` | cursor string | Pagination cursor |

**Pagination:**

| Endpoint | Pagination parameter | Notes |
|---|---|---|
| `fetch_reddit_app_dynamic_search_results` | `after` (cursor string) | Pass cursor from previous response |
| `fetch_reddit_app_user_profile`, `fetch_users_active_subreddits`, `fetch_user_public_trophies` | — | Single-call response |
| `fetch_reddit_app_subreddit_*` endpoints | — | Single-call response |
| `fetch_reddit_app_trending_searches` | — | No parameters, single-call response |

**Cache directory structure:**

```
.keyapi-cache/
└── YYYY-MM-DD/
    ├── fetch_reddit_app_user_profile/
    │   └── {params_hash}.json
    ├── fetch_users_active_subreddits/
    │   └── {params_hash}.json
    ├── fetch_user_public_trophies/
    │   └── {params_hash}.json
    ├── fetch_reddit_app_subreddit_rules_and_style_info/
    │   └── {params_hash}.json
    ├── fetch_reddit_app_subreddit_post_channels/
    │   └── {params_hash}.json
    ├── fetch_reddit_app_subreddit_info/
    │   └── {params_hash}.json
    ├── fetch_reddit_app_subreddit_settings/
    │   └── {params_hash}.json
    ├── check_if_subreddit_is_muted/
    │   └── {params_hash}.json
    ├── fetch_reddit_app_search_typeahead_suggestions/
    │   └── {params_hash}.json
    ├── fetch_reddit_app_dynamic_search_results/
    │   └── {params_hash}.json
    └── fetch_reddit_app_trending_searches/
        └── {params_hash}.json
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists for the given parameters. If a valid cache file exists, load from disk and skip the API call.

### Step 4 — Synthesize and Report Findings

After collecting all API responses, produce a structured user and community intelligence report:

**For user analysis:**
1. **User Profile** — Username, karma breakdown (post/comment), account age, verification status, premium status.
2. **Community Footprint** — Most active subreddits, participation frequency, community diversity.
3. **Achievement History** — Public trophies, milestone dates, recognition type.
4. **Behavioral Signals** — Activity patterns, community focus areas, engagement style.

**For subreddit research:**
1. **Community Overview** — Name, subscriber count, description, creation date, NSFW status.
2. **Governance Structure** — Rules, posting requirements, moderation policies, style guidelines.
3. **Content Architecture** — Post channels, content categories, flair taxonomy.
4. **Settings Profile** — Posting rules, badge configuration, moderation settings.

**For search intelligence:**
1. **Search Results** — Matched posts, communities, users, or comments with relevance scores.
2. **Trending Topics** — Current platform-wide trending searches and emerging discussions.
3. **Discovery Signals** — Subreddit recommendations, user suggestions from typeahead.

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Common Rules

| Rule | Detail |
|------|--------|
| **Subreddit identifier** | Use `subreddit_name` for info/rules/channels endpoints. Use `subreddit_id` (with `t5_` prefix, e.g., `t5_2qh0u`) for settings/mute/highlights endpoints. Call `fetch_reddit_app_subreddit_info` first to resolve it from name. |
| **`fetch_reddit_app_trending_searches`** | Requires no parameters. Call with empty params `{}`. |
| **`need_format`** | Set to `true` for sanitized output. Defaults to `false`. |
| **Dynamic search types** | `search_type` options: `post`, `community`, `comment`, `media`, `user` (singular form). `sort` options: `RELEVANCE`, `HOT`, `TOP`, `NEW`, `COMMENTS` (uppercase). |
| **Dynamic search string params** | `safe_search` is a string (`"unset"`, `"on"`, `"off"`). `allow_nsfw` is a string (`"0"` to exclude, `"1"` to include). Neither is a boolean. |
| **`fetch_reddit_app_subreddit_post_channels`** | Accepts a `range` param (default: `DAY`) in addition to `sort`. Valid range values: `HOUR`, `DAY`, `WEEK`, `MONTH`, `YEAR`, `ALL`. |
| **`fetch_user_comments` page_size** | Supports `page_size` (integer, default 25) to control how many comments are returned per page. |
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
| `400` | Bad request — invalid or missing parameters | Validate input; ensure correct identifier type (`subreddit_name` vs. `subreddit_id`) |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `404` | Resource not found — user or subreddit may not exist or be banned | Verify the username or subreddit name; banned/private subreddits may return no data |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry up to 3 times with a 2–3 second pause; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
