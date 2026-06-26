---
name: keyapi-threads-user-discovery
description: Discover and analyze Threads users and content — retrieve user profiles, posts, reposts, replies, post details, comments, and perform keyword-based search across top content, recent content, and user profiles.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"🧵"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-threads-user-discovery

> Discover and analyze Threads users and content — from profile resolution and content inventory to comment thread exploration and keyword-based search across the platform.

This skill provides comprehensive Threads user and content intelligence using the KeyAPI MCP service. It enables retrieval of user profiles (by username or user ID), published posts, reposts, replies, individual post details (by shortcode or full URL), post comments, and keyword search across top content, recent content, and user profiles — all through a unified, cache-first workflow.

Use this skill when you need to:
- Retrieve a Threads user's profile by username or numeric user ID
- Inventory a user's published posts, reposts, and reply activity
- Retrieve full details for a specific post using its shortcode or URL
- Explore comments on a Threads post
- Search for top or recent content by keyword
- Discover user profiles matching a search query

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

All tool calls in this skill target the KeyAPI Threads MCP server:

```
Server URL : https://mcp.keyapi.ai/threads/mcp
Auth Header: Authorization: Bearer $KEYAPI_TOKEN
```

**Setup (one-time):**

```bash
# 1. Install dependencies
npm install

# 2. Set your API token (get one free at https://keyapi.ai/)
export KEYAPI_TOKEN=your_token_here

# 3. List all available tools to verify the connection
node scripts/run.js --platform threads --list-tools
```

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Analysis Scenarios

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| User profile by username | `get_user_info` | Profile lookup, follower count, bio, verification |
| User profile by numeric user ID | `get_user_info_by_id` | ID-to-profile resolution, data normalization |
| User's published posts | `get_user_posts` | Content inventory, posting cadence analysis |
| User's reposts | `get_user_reposts` | Content amplification patterns, sharing behavior |
| User's replies | `get_user_replies` | Engagement behavior, conversation participation |
| Post details by shortcode or URL | `get_post_detail` | Post audit, content analysis, media retrieval |
| Comments on a post | `get_post_comments` | Sentiment analysis, community reaction (requires numeric post ID from `get_post_detail` response) |
| Search top content by keyword | `search_top_content` | Viral content discovery, trending topic research |
| Search recent content by keyword | `search_recent_content` | Real-time content monitoring, breaking topic tracking |
| Search user profiles by keyword | `search_profiles` | Creator discovery, influencer prospecting |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify Analysis Targets and Select Nodes

Clarify the research objective and map it to one or more nodes. Typical entry points:

- **Profile lookup by handle**: Use `get_user_info` with `username`. Returns `user_id` needed for content endpoints.
- **Profile lookup by ID**: Use `get_user_info_by_id` when only a numeric ID is available.
- **Content audit**: Combine `get_user_posts` + `get_user_reposts` + `get_user_replies` for a full activity snapshot.
- **Post deep-dive**: Use `get_post_detail` then `get_post_comments` for content + community reaction.
- **Content discovery**: Use `search_top_content` for viral content or `search_recent_content` for latest posts.
- **Creator discovery**: Use `search_profiles` to find users by keyword.

> **Critical: Two Identifier Types**
>
> Threads endpoints use two distinct identifiers:
> - `username` — the @handle from the profile URL (e.g., `https://www.threads.net/@lilbieber` → `lilbieber`). Used by `get_user_info` and `search_profiles`.
> - `user_id` — the numeric internal user ID (e.g., `63625256886`). Required by `get_user_posts`, `get_user_reposts`, `get_user_replies`, and `get_user_info_by_id`.
>
> **Always call `get_user_info` first** with the `username` to obtain the `user_id` before calling content endpoints.

> **`get_post_detail` vs. `get_post_comments` — Different `post_id` Formats**
>
> These two endpoints both use a `post_id` parameter but expect **different formats**:
> - `get_post_detail`: `post_id` = the **shortcode** from the URL (e.g., `DPVUglOjOUu` from `https://www.threads.com/@taylorswift/post/DPVUglOjOUu`)
> - `get_post_comments`: `post_id` = the **numeric post ID** (e.g., `3390920896561588969`)
>
> The numeric post ID is returned inside the `get_post_detail` response. The workflow is: call `get_post_detail` with the shortcode → extract the numeric `id` from the response → pass it to `get_post_comments`.

> **`get_post_detail` — Shortcode vs. Full URL**
>
> `get_post_detail` accepts either:
> - `post_id` — the shortcode extracted from the post URL (e.g., `https://www.threads.com/@taylorswift/post/DPVUglOjOUu` → shortcode is `DPVUglOjOUu`)
> - `url` — the full post URL
>
> Pass one, not both. The shortcode is preferred for caching consistency.

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters and available options:

```bash
node scripts/run.js --platform threads --schema <tool_name>

# Examples
node scripts/run.js --platform threads --schema get_user_info
node scripts/run.js --platform threads --schema get_post_detail
node scripts/run.js --platform threads --schema search_top_content
```

### Step 3 — Call APIs and Cache Results Locally

Execute tool calls and persist responses to the local cache to avoid redundant API calls.

**Calling a tool:**

```bash
# Single call with pretty output
node scripts/run.js --platform threads --tool <tool_name> \
  --params '<json_args>' --pretty

# Force fresh data, skip cache
node scripts/run.js --platform threads --tool <tool_name> \
  --params '<json_args>' --no-cache --pretty
```

**Example — get user profile by username:**

```bash
node scripts/run.js --platform threads --tool get_user_info \
  --params '{"username":"zuck"}' --pretty
```

**Example — get user posts (first page):**

```bash
node scripts/run.js --platform threads --tool get_user_posts \
  --params '{"user_id":"63625256886"}' --pretty
```

**Example — get next page using end_cursor:**

```bash
node scripts/run.js --platform threads --tool get_user_posts \
  --params '{"user_id":"63625256886","end_cursor":"<cursor_from_previous_response>"}' --pretty
```

**Example — get post detail by shortcode (step 1 of comment workflow):**

```bash
node scripts/run.js --platform threads --tool get_post_detail \
  --params '{"post_id":"DPVUglOjOUu"}' --pretty
# Response contains numeric "id" field — use it for get_post_comments
```

**Example — get post comments using numeric post ID (step 2):**

```bash
node scripts/run.js --platform threads --tool get_post_comments \
  --params '{"post_id":"3390920896561588969"}' --pretty
```

**Example — get post detail by full URL:**

```bash
node scripts/run.js --platform threads --tool get_post_detail \
  --params '{"url":"https://www.threads.com/@taylorswift/post/DPVUglOjOUu"}' --pretty
```

**Example — search top content:**

```bash
node scripts/run.js --platform threads --tool search_top_content \
  --params '{"query":"AI"}' --pretty
```

**Example — search user profiles:**

```bash
node scripts/run.js --platform threads --tool search_profiles \
  --params '{"query":"mark"}' --pretty
```

**Pagination:**

Threads uses cursor-based pagination via `end_cursor`:

| Endpoint | Pagination parameter | Notes |
|---|---|---|
| `get_user_posts`, `get_user_reposts`, `get_user_replies` | `end_cursor` | Pass cursor from previous response; omit for first call |
| `get_post_comments` | `end_cursor` | Pass cursor from previous response; omit for first call |
| `search_top_content`, `search_recent_content` | `end_cursor` | Pass cursor from previous response; omit for first call |
| `get_user_info`, `get_user_info_by_id`, `get_post_detail` | — | Single-call response |
| `search_profiles` | — | No pagination; single-call response |

**Cache directory structure:**

```
.keyapi-cache/
└── YYYY-MM-DD/
    ├── get_user_info/
    │   └── {params_hash}.json
    ├── get_user_info_by_id/
    │   └── {params_hash}.json
    ├── get_user_posts/
    │   └── {params_hash}.json
    ├── get_user_reposts/
    │   └── {params_hash}.json
    ├── get_user_replies/
    │   └── {params_hash}.json
    ├── get_post_detail/
    │   └── {params_hash}.json
    ├── get_post_comments/
    │   └── {params_hash}.json
    ├── search_top_content/
    │   └── {params_hash}.json
    ├── search_recent_content/
    │   └── {params_hash}.json
    └── search_profiles/
        └── {params_hash}.json
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists for the given parameters. If a valid cache file exists, load from disk and skip the API call.

### Step 4 — Synthesize and Report Findings

After collecting all API responses, produce a structured user and content intelligence report:

**For individual user analysis:**
1. **Profile Overview** — Username, display name, user ID, bio, follower count, following count, verification status, account type.
2. **Content Inventory** — Post count, repost frequency, reply activity, posting cadence.
3. **Engagement Patterns** — Like counts, reply counts, repost counts on published content.
4. **Content Themes** — Recurring topics, hashtag usage, media type distribution.

**For post analysis:**
1. **Post Details** — Author, text content, media attachments, like count, reply count, repost count, timestamp.
2. **Comment Sentiment** — Top comment themes, community reaction, notable replies.
3. **Engagement Quality** — Like-to-reply ratio, repost amplification signals.

**For search and discovery:**
1. **Top Content Results** — Highest-engagement posts matching the query, author profiles.
2. **Recent Content Results** — Latest posts for real-time topic monitoring.
3. **Profile Discovery** — Matched user profiles with follower counts and verification status.

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Common Rules

| Rule | Detail |
|------|--------|
| **Identifier resolution** | `get_user_posts`, `get_user_reposts`, `get_user_replies` require `user_id`. Always call `get_user_info` first with `username` to obtain it. |
| **`get_post_comments` post_id** | Requires the **numeric post ID** (e.g., `3390920896561588969`), NOT the shortcode. Call `get_post_detail` first with the shortcode and extract the `id` field from the response. |
| **`get_post_detail` input** | Pass either `post_id` (shortcode) or `url` (full URL) — not both. Prefer `post_id` for caching consistency. |
| **Shortcode extraction** | Extract shortcode from post URL: `https://www.threads.com/@{username}/post/{shortcode}` |
| **Cursor pagination** | Use `end_cursor` from the previous response to fetch the next page. Omit for the first call. |
| **`search_profiles` pagination** | `search_profiles` does not support pagination — returns results in a single call. |
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
| `400` | Bad request — invalid or missing parameters | Validate input; ensure `user_id` is provided for content endpoints; check shortcode format |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `404` | Resource not found — user or post may not exist or account is private | Verify the username or post shortcode; private accounts may have restricted data |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry up to 3 times with a 2–3 second pause; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
