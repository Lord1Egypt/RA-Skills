---
name: keyapi-reddit-content-analytics
description: Explore and analyze Reddit content at scale — retrieve post details (single, batch, or large batch), comments, sub-comment threads, user activity, and curated feeds including home, popular, games, news, subreddit, and community highlights.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"📰"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-reddit-content-analytics

> Explore and analyze Reddit content at scale — from individual post deep-dives and threaded comment traversal to curated feed monitoring and user activity research.

This skill provides comprehensive Reddit content intelligence using the KeyAPI MCP service. It enables retrieval of post details (single or batch), comment threads with sub-comment traversal, user-published posts and comments, and curated feed content across home, popular, games, news, subreddit, and community highlight feeds — all through a unified, cache-first workflow.

Use this skill when you need to:
- Retrieve full details for one or more Reddit posts by ID
- Traverse comment threads including nested sub-comments
- Analyze a specific user's post and comment history
- Monitor trending content across Reddit's home, popular, games, and news feeds
- Explore subreddit-specific content streams
- Surface community highlights and pinned content from specific subreddits

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
| Full details for a single post | `fetch_single_reddit_post_details` | Post audit, content analysis, comment context |
| Batch details for up to 5 posts | `fetch_reddit_post_details_in_batch_max_5` | Small-scale comparative analysis |
| Batch details for up to 30 posts | `fetch_reddit_post_details_in_large_batch_max_30` | Large-scale content harvesting |
| Top-level comments on a post | `fetch_reddit_app_post_comments` | Sentiment analysis, community reaction |
| Sub-comments / nested replies | `fetch_reddit_app_comment_replies_sub-comments` | Deep thread traversal, reply chain analysis |
| Posts published by a user | `fetch_user_posts` | User content audit, posting behavior |
| Comments published by a user | `fetch_user_comments` | User engagement patterns, opinion tracking |
| Reddit home feed (personalized) | `fetch_reddit_app_home_feed` | Trending content monitoring |
| Popular / trending feed | `fetch_reddit_app_popular_feed` | Viral content discovery, trend detection |
| Gaming community feed | `fetch_reddit_app_games_feed` | Gaming trend monitoring |
| News feed | `fetch_reddit_app_news_feed` | Current events, news discussion tracking |
| Subreddit content stream | `fetch_reddit_app_subreddit_feed` | Community-specific content monitoring |
| Community highlights and pinned content | `fetch_reddit_app_community_highlights` | Featured posts, important announcements |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify Analysis Targets and Select Nodes

Clarify the research objective and map it to one or more nodes. Typical entry points:

- **Post research**: Use `fetch_single_reddit_post_details` for one post, or batch endpoints for multiple.
- **Comment thread traversal**: Use `fetch_reddit_app_post_comments` for top-level comments, then `fetch_reddit_app_comment_replies_sub-comments` for nested replies when `more.cursor` is present.
- **User activity audit**: Combine `fetch_user_posts` + `fetch_user_comments` for a full activity profile.
- **Feed monitoring**: Choose the appropriate feed endpoint based on content category.
- **Subreddit deep-dive**: Use `fetch_reddit_app_subreddit_feed` + `fetch_reddit_app_community_highlights`.

> **Critical: Reddit ID Type Prefixes**
>
> The Reddit APP API requires type prefixes on all IDs — this is mandatory:
> - **Post IDs**: must use `t3_` prefix (e.g., `t3_1ojnh50`)
> - **Comment IDs**: must use `t1_` prefix (e.g., `t1_abcd123`)
>
> Passing a bare ID without the prefix will result in an error. Always include the prefix.

> **Sub-comment Traversal**
>
> When a comment node in `fetch_reddit_app_post_comments` response contains a `more.cursor` field, it indicates nested replies exist. Use `fetch_reddit_app_comment_replies_sub-comments` with:
> - `post_id`: the parent post ID (with `t3_` prefix)
> - `cursor`: the value from `more.cursor` (format: `commenttree:ex:(xxx)`)
>
> Path to cursor: `$.data.postInfoById.commentForest.trees[*].more.cursor`

> **`need_format` Parameter**
>
> Most endpoints accept an optional `need_format` boolean. Set to `true` to receive sanitized/cleaned response data. Defaults to `false` (raw data). Use `true` when downstream processing requires cleaner output.

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters and available options:

```bash
node scripts/run.js --platform reddit --schema <tool_name>

# Examples
node scripts/run.js --platform reddit --schema fetch_single_reddit_post_details
node scripts/run.js --platform reddit --schema fetch_reddit_app_post_comments
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

**Example — get single post details:**

```bash
node scripts/run.js --platform reddit --tool fetch_single_reddit_post_details \
  --params '{"post_id":"t3_1ojnh50"}' --pretty
```

**Example — batch fetch up to 5 posts:**

```bash
node scripts/run.js --platform reddit --tool fetch_reddit_post_details_in_batch_max_5 \
  --params '{"post_ids":"t3_1ojnh50,t3_1ok432f,t3_1nwil8j"}' --pretty
```

**Example — get post comments:**

```bash
node scripts/run.js --platform reddit --tool fetch_reddit_app_post_comments \
  --params '{"post_id":"t3_1ojnvca","sort_type":"TOP"}' --pretty
```

**Example — get sub-comments using cursor:**

```bash
node scripts/run.js --platform reddit --tool "fetch_reddit_app_comment_replies_sub-comments" \
  --params '{"post_id":"t3_1qmup73","cursor":"commenttree:ex:(RjiJd","sort_type":"CONFIDENCE"}' --pretty
```

**Example — get popular feed:**

```bash
node scripts/run.js --platform reddit --tool fetch_reddit_app_popular_feed \
  --params '{"sort":"HOT","time":"WEEK"}' --pretty
```

**Example — get subreddit feed:**

```bash
node scripts/run.js --platform reddit --tool fetch_reddit_app_subreddit_feed \
  --params '{"subreddit_name":"technology","sort":"HOT"}' --pretty
```

**Example — get user posts:**

```bash
node scripts/run.js --platform reddit --tool fetch_user_posts \
  --params '{"username":"spez","sort":"NEW"}' --pretty
```

**Pagination:**

| Endpoint group | Pagination parameter | Notes |
|---|---|---|
| Feed endpoints (`home`, `popular`, `games`, `news`, `subreddit`) | `after` (cursor string) | Pass `after` value from previous response |
| `fetch_reddit_app_post_comments` | `after` (cursor string) | Found in last comment node |
| `fetch_user_posts`, `fetch_user_comments` | `after` (cursor string) | Pass cursor from previous response |
| `fetch_reddit_app_comment_replies_sub-comments` | `cursor` (from `more.cursor`) | Use cursor from comment node, not `after` |
| Batch post endpoints | — | No pagination; pass all IDs in one call |

**Batch endpoint limits:**

| Endpoint | Max posts per call |
|---|---|
| `fetch_reddit_post_details_in_batch_max_5` | 5 |
| `fetch_reddit_post_details_in_large_batch_max_30` | 30 |

Exceeding these limits returns an error. Split larger sets across multiple calls.

**Cache directory structure:**

```
.keyapi-cache/
└── YYYY-MM-DD/
    ├── fetch_single_reddit_post_details/
    │   └── {params_hash}.json
    ├── fetch_reddit_post_details_in_batch_max_5/
    │   └── {params_hash}.json
    ├── fetch_reddit_post_details_in_large_batch_max_30/
    │   └── {params_hash}.json
    ├── fetch_reddit_app_post_comments/
    │   └── {params_hash}.json
    ├── fetch_reddit_app_comment_replies_sub-comments/
    │   └── {params_hash}.json
    ├── fetch_user_posts/
    │   └── {params_hash}.json
    ├── fetch_user_comments/
    │   └── {params_hash}.json
    ├── fetch_reddit_app_home_feed/
    │   └── {params_hash}.json
    ├── fetch_reddit_app_popular_feed/
    │   └── {params_hash}.json
    ├── fetch_reddit_app_games_feed/
    │   └── {params_hash}.json
    ├── fetch_reddit_app_news_feed/
    │   └── {params_hash}.json
    ├── fetch_reddit_app_subreddit_feed/
    │   └── {params_hash}.json
    └── fetch_reddit_app_community_highlights/
        └── {params_hash}.json
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists for the given parameters. If a valid cache file exists, load from disk and skip the API call.

### Step 4 — Synthesize and Report Findings

After collecting all API responses, produce a structured content intelligence report:

**For post analysis:**
1. **Post Overview** — Title, subreddit, author, score, upvote ratio, comment count, post date, flair.
2. **Engagement Metrics** — Score distribution, comment volume, award count, cross-post activity.
3. **Comment Sentiment** — Top comment themes, sentiment distribution, notable replies.
4. **Thread Structure** — Depth of discussion, sub-comment density, most-engaged branches.

**For feed monitoring:**
1. **Trending Topics** — Top posts by score, common themes, subreddit distribution.
2. **Content Patterns** — Media type breakdown (text, image, video, link), posting cadence.
3. **Community Signals** — Subreddits driving the most engagement, emerging discussion topics.

**For user activity:**
1. **Activity Profile** — Post frequency, comment frequency, active subreddits.
2. **Content Themes** — Recurring topics, subreddit focus areas.
3. **Engagement Style** — Comment length patterns, upvote/downvote behavior where available.

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Common Rules

| Rule | Detail |
|------|--------|
| **ID prefixes** | Always include type prefixes: `t3_` for post IDs, `t1_` for comment IDs. Bare IDs will fail. |
| **Batch limits** | `fetch_reddit_post_details_in_batch_max_5` accepts max 5 IDs; `fetch_reddit_post_details_in_large_batch_max_30` accepts max 30. Split larger sets across multiple calls. |
| **Sub-comment traversal** | When a comment node has `more.cursor`, call `fetch_reddit_app_comment_replies_sub-comments` with that cursor to retrieve nested replies. |
| **`need_format`** | Set to `true` for sanitized output. Defaults to `false`. Use `true` when cleaner data is needed for downstream processing. |
| **Feed pagination** | Use `after` cursor from the previous response to fetch the next page of feed content. |
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
| `400` | Bad request — invalid or missing parameters | Validate ID format (check `t3_`/`t1_` prefixes); verify batch size limits |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `404` | Resource not found — post or comment may have been deleted | Verify the post ID; deleted or removed content may return empty results |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry up to 3 times with a 2–3 second pause; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
