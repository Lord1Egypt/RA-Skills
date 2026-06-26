---
name: keyapi-instagram-user-analysis
description: Discover, profile, and deeply analyze Instagram users — explore follower and following networks, posts, Reels, Stories, Highlights, tagged content, reposts, and similarity-based recommendations.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"👤"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-instagram-user-analysis

> Discover, profile, and deeply analyze Instagram users — from identity resolution and content inventory to social graph exploration and audience similarity mapping.

This skill provides comprehensive Instagram user intelligence using the KeyAPI MCP service. It enables retrieval of detailed user profiles, content libraries (posts, Reels, Stories, Highlights), social connections (followers, following), tagged appearances, reposts, and algorithmic similarity matches — all through a unified, cache-first workflow.

Use this skill when you need to:
- Retrieve full profile details for an Instagram user by username or user ID
- Inventory a creator's published posts, Reels, and active Stories
- Explore a user's Highlights and the Stories archived within them
- Analyze social graph relationships — followers, following, similar accounts
- Research tagged appearances and reposted content for influencer attribution
- Build user shortlists based on Instagram's native similarity recommendations

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

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Resolve user ID to username (or vice versa) | `get_user_info_by_user_id` | ID-to-handle translation, data normalization |
| Full profile snapshot (by username or user ID) | `get_user_info` | Profile audit, follower/following counts, bio, verification status |
| All published posts with metadata | `get_user_posts` | Content inventory, posting cadence analysis |
| Reels library with engagement data | `get_user_reels` | Short-video strategy, Reels performance overview |
| Follower list sampling | `get_user_followers` | Audience quality sampling, fan demographics |
| Following list exploration | `get_user_following` | Network affinity, brand partnership signals |
| Active Stories (last 24 hours) | `get_user_stories` | Real-time content monitoring — expires after 24 hours |
| Highlights index | `get_user_highlights` | Curated content categories, evergreen story topics |
| Stories inside a specific Highlight | `get_highlight_stories` | Deep-dive into a pinned content collection |
| Posts where user is tagged | `get_user_tagged_posts` | Influencer attribution, UGC discovery |
| Reposted / shared content list | `get_user_reposts_list` | Content amplification patterns, cross-promotion signals |
| Algorithmically similar users | `get_similar_users` | Audience lookalike discovery, competitive mapping |
| Related / recommended profiles | `get_related_profiles` | Expanded creator discovery beyond keyword search |
| Search users by keyword | `search_users` | Initial user discovery by name or handle fragment |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify Analysis Targets and Select Nodes

Clarify the research objective and map it to one or more nodes. Typical entry points:

- **Profile lookup by handle**: Use `get_user_info` with `username`. If you only have a numeric user ID, use `get_user_info_by_user_id` first.
- **Content audit**: Combine `get_user_posts` + `get_user_reels` + `get_user_stories` for a full content snapshot.
- **Social graph research**: Use `get_user_followers` + `get_user_following` with `pagination_token` to traverse the network.
- **Highlights deep-dive**: Call `get_user_highlights` first to retrieve Highlight IDs, then `get_highlight_stories` for each ID.
- **Similarity mapping**: Use `get_similar_users` or `get_related_profiles` to expand a creator list.

> **User Identification**
>
> Most endpoints accept either `username` (e.g., `instagram`) or `user_id` (numeric, e.g., `25025320`) — pass one, not both.
> - Use `get_user_info` with `username` to resolve the numeric `user_id` when downstream nodes require it.
> - `get_user_reposts_list` and `get_related_profiles` accept **only** `user_id` — resolve it first if you start from a handle.

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters, data types, and available options:

```bash
node scripts/run.js --platform instagram --schema <tool_name>

# Examples
node scripts/run.js --platform instagram --schema get_user_info
node scripts/run.js --platform instagram --schema get_user_highlights
```

### Step 3 — Call APIs and Cache Results Locally

Execute tool calls and persist responses to the local cache to avoid redundant API calls.

**Calling a tool:**

```bash
# Single call with pretty output
node scripts/run.js --platform instagram --tool <tool_name> \
  --params '<json_args>' --pretty

# Force fresh data, skip cache
node scripts/run.js --platform instagram --tool <tool_name> \
  --params '<json_args>' --no-cache --pretty
```

**Example — get full user profile:**

```bash
node scripts/run.js --platform instagram --tool get_user_info \
  --params '{"username":"instagram"}' --pretty
```

**Example — get user posts (first page):**

```bash
# Use user_id to avoid the "username " (with space) schema quirk
node scripts/run.js --platform instagram --tool get_user_posts \
  --params '{"user_id":"25025320"}' --pretty
```

**Example — get next page using pagination token:**

```bash
node scripts/run.js --platform instagram --tool get_user_posts \
  --params '{"user_id":"25025320","pagination_token":"<token_from_previous_response>"}' --pretty
```

**Example — get Highlights, then stories in one Highlight:**

```bash
# Step 1: get Highlight IDs
node scripts/run.js --platform instagram --tool get_user_highlights \
  --params '{"username":"instagram"}' --pretty

# Step 2: get Stories in a specific Highlight
node scripts/run.js --platform instagram --tool get_highlight_stories \
  --params '{"highlight_id":"17895069621772257"}' --pretty
```

**Pagination:**

Instagram endpoints use token-based pagination — not numeric page numbers.

| Endpoint group | Pagination parameter | Notes |
|---|---|---|
| `get_user_posts`, `get_user_reels`, `get_user_followers`, `get_user_following`, `get_user_tagged_posts` | `pagination_token` | Pass token from previous response |
| `get_user_reposts_list` | `max_id` | Pass cursor from previous response; leave empty for first call |
| `get_user_stories`, `get_user_highlights`, `get_similar_users`, `get_related_profiles` | — | No pagination; single-call response |

**Cache directory structure:**

```
.keyapi-cache/
└── YYYY-MM-DD/
    ├── get_user_info/
    │   └── {params_hash}.json
    ├── get_user_info_by_user_id/
    │   └── {params_hash}.json
    ├── get_user_posts/
    │   └── {params_hash}.json
    ├── get_user_reels/
    │   └── {params_hash}.json
    ├── get_user_followers/
    │   └── {params_hash}.json
    ├── get_user_following/
    │   └── {params_hash}.json
    ├── get_user_stories/
    │   └── {params_hash}.json
    ├── get_user_highlights/
    │   └── {params_hash}.json
    ├── get_highlight_stories/
    │   └── {params_hash}.json
    ├── get_user_tagged_posts/
    │   └── {params_hash}.json
    ├── get_user_reposts_list/
    │   └── {params_hash}.json
    ├── get_similar_users/
    │   └── {params_hash}.json
    ├── get_related_profiles/
    │   └── {params_hash}.json
    └── search_users/
        └── {params_hash}.json
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists for the given parameters. If a valid cache file exists, load from disk and skip the API call.

### Step 4 — Synthesize and Report Findings

After collecting all API responses, produce a structured user intelligence report:

**For individual profile analysis:**
1. **Profile Overview** — Username, display name, user ID, bio, follower count, following count, post count, verification status, account type (personal/creator/business).
2. **Content Inventory** — Post count breakdown (posts vs. Reels), posting frequency, most recent content dates, Stories availability.
3. **Highlights Summary** — Number of Highlight collections, topics covered, content age and freshness.
4. **Social Graph Signals** — Follower-to-following ratio, notable followers/followings where available.
5. **Tagged Appearances** — Frequency of third-party tags, top tagging accounts, brand mention patterns.
6. **Similarity Network** — Similar and related accounts for audience overlap estimation.

**For discovery / shortlist building:**
1. **Search Results** — Matched users, follower counts, verification status.
2. **Similarity Clusters** — Grouped similar accounts by niche or audience type.
3. **Comparative Overview** — Side-by-side profile metrics for shortlisted creators.

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Common Rules

| Rule | Detail |
|------|--------|
| **User identification** | Most endpoints accept `username` or `user_id` — pass one. `get_user_reposts_list` and `get_related_profiles` require `user_id` only; resolve it via `get_user_info` first if starting from a handle. |
| **`get_user_posts` username quirk** | The `get_user_posts` schema has a trailing space in the parameter name: `"username "` (with space). Use `user_id` instead of `username` when calling this endpoint to avoid potential parameter rejection. |
| **Pagination** | Use `pagination_token` for most user-list endpoints. Use `max_id` for `get_user_reposts_list`. Some endpoints (`get_user_stories`, `get_user_highlights`, `get_similar_users`, `get_related_profiles`) return all data in a single call. |
| **Highlights workflow** | Always call `get_user_highlights` first to obtain Highlight IDs before calling `get_highlight_stories`. The `highlight_id` may or may not include the `"highlight:"` prefix — pass it exactly as returned. |
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
| `400` | Bad request — invalid or missing parameters | Validate input against the tool schema; ensure at least one of `username` or `user_id` is provided |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `404` | Resource not found — user may not exist or account is private | Verify the username or user ID; private accounts may have restricted data |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry up to 3 times with a 2–3 second pause; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
