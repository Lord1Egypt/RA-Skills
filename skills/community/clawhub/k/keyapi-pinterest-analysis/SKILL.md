---
name: keyapi-pinterest-analysis
description: Discover and analyze Pinterest users, pins, boards, followers, and following — search users, retrieve profile information, explore pin libraries and board collections, and traverse follower/following networks.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"📌"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-pinterest-analysis

> Discover and analyze Pinterest users, pins, boards, and social graphs — from profile lookup and content inventory to follower and following network traversal.

This skill provides comprehensive Pinterest user intelligence using the KeyAPI MCP service. It enables user search and profile retrieval, pin library exploration, board collection browsing, and follower/following network analysis — all through a unified, cache-first workflow.

Use this skill when you need to:
- Search for Pinterest users by name or keyword
- Retrieve a user's profile details, follower count, and bio
- Browse a user's pin library
- Explore a user's board collections
- Traverse a user's follower list with cursor-based pagination
- Analyze a user's following list with bookmark-based pagination

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

All tool calls in this skill target the KeyAPI Pinterest MCP server:

```
Server URL : https://mcp.keyapi.ai/pinterest/mcp
Auth Header: Authorization: Bearer $KEYAPI_TOKEN
```

**Setup (one-time):**

```bash
# 1. Install dependencies
npm install

# 2. Set your API token (get one free at https://keyapi.ai/)
export KEYAPI_TOKEN=your_token_here

# 3. List all available tools to verify the connection
node scripts/run.js --platform pinterest --list-tools
```

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Analysis Scenarios

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Search users by name or keyword | `search_users` | Creator discovery, influencer prospecting |
| User profile details and stats | `get_user_information` | Profile audit, follower count, bio |
| User's pin library | `get_pins` | Content inventory, pin theme analysis |
| User's board collections | `get_boards` | Board taxonomy, niche focus areas |
| Follower list with pagination | `get_followers_detail` | Audience sampling, follower network research |
| Following list with pagination | `get_following_detail` | Interest mapping, network affinity analysis |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify Analysis Targets and Select Nodes

Clarify the research objective and map it to one or more nodes. Typical entry points:

- **User discovery**: Use `search_users` with a keyword → select a target user.
- **Profile audit**: Use `get_user_information` with `username` to retrieve profile details and extract the numeric `userid`.
- **Content inventory**: Use `get_pins` + `get_boards` with `username` for a full content snapshot.
- **Social graph analysis**: Use `get_followers_detail` + `get_following_detail` with `userid` for network traversal.

> **Two Parameter Naming Conventions**
>
> Pinterest endpoints use different parameter names depending on the endpoint:
>
> | Parameter | Type | Used by |
> |---|---|---|
> | `username` | String (display name/handle) | `search_users`, `get_user_information`, `get_pins` |
> | `entry` | String (username or board path) | `get_boards` |
> | `userid` | Numeric string (e.g., `125186202050495625`) | `get_followers_detail`, `get_following_detail` |
>
> Obtain the numeric `userid` from the `get_user_information` response before calling `get_followers_detail` or `get_following_detail`.

> **`get_boards` — `entry` Parameter**
>
> `get_boards` uses an `entry` parameter (not `username`). This accepts a username (e.g., `broadstbullycom`) or a board URL path. Pass the username to retrieve all boards for that user.

> **`get_followers_detail` — Two Pagination Identifiers**
>
> `get_followers_detail` uses two separate identifiers:
> - `userid` — the numeric user ID of the target user
> - `node_id` — an internal node identifier used with `cursor` for multi-page traversal
>
> For the first call, pass only `userid`. Subsequent pages require both `node_id` and `cursor` values from the previous response.

> **`get_following_detail` — `bookmark` Pagination**
>
> `get_following_detail` uses `bookmark` (not `cursor`) for pagination. Pass the `bookmark` value from the previous response to fetch the next page. Omit for the first call.

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters and available options:

```bash
node scripts/run.js --platform pinterest --schema <tool_name>

# Examples
node scripts/run.js --platform pinterest --schema get_user_information
node scripts/run.js --platform pinterest --schema get_followers_detail
```

### Step 3 — Call APIs and Cache Results Locally

Execute tool calls and persist responses to the local cache to avoid redundant API calls.

**Calling a tool:**

```bash
# Single call with pretty output
node scripts/run.js --platform pinterest --tool <tool_name> \
  --params '<json_args>' --pretty

# Force fresh data, skip cache
node scripts/run.js --platform pinterest --tool <tool_name> \
  --params '<json_args>' --no-cache --pretty
```

**Example — search users:**

```bash
node scripts/run.js --platform pinterest --tool search_users \
  --params '{"username":"interior design"}' --pretty
```

**Example — get user profile:**

```bash
node scripts/run.js --platform pinterest --tool get_user_information \
  --params '{"username":"tastemade"}' --pretty
```

**Example — get user pins:**

```bash
node scripts/run.js --platform pinterest --tool get_pins \
  --params '{"username":"tastemade"}' --pretty
```

**Example — get user boards:**

```bash
node scripts/run.js --platform pinterest --tool get_boards \
  --params '{"entry":"tastemade"}' --pretty
```

**Example — get followers (first page):**

```bash
# Pass userid from get_user_information response
node scripts/run.js --platform pinterest --tool get_followers_detail \
  --params '{"userid":"125186202050495625"}' --pretty
```

**Example — get followers (subsequent pages):**

```bash
# Pass node_id and cursor from previous response
node scripts/run.js --platform pinterest --tool get_followers_detail \
  --params '{"userid":"125186202050495625","node_id":"987654321","cursor":"cursor_from_previous_response"}' --pretty
```

**Example — get following (first page):**

```bash
node scripts/run.js --platform pinterest --tool get_following_detail \
  --params '{"userid":"125186202050495625"}' --pretty
```

**Example — get following (subsequent pages):**

```bash
# Pass bookmark from previous response
node scripts/run.js --platform pinterest --tool get_following_detail \
  --params '{"userid":"125186202050495625","bookmark":"bookmark_from_previous_response"}' --pretty
```

**Pagination reference:**

| Endpoint | Pagination method | First call | Subsequent pages |
|---|---|---|---|
| `get_followers_detail` | `cursor` + `node_id` | Pass `userid` only | Pass `userid` + `node_id` + `cursor` from response |
| `get_following_detail` | `bookmark` | Pass `userid` only | Pass `userid` + `bookmark` from response |
| `search_users`, `get_user_information`, `get_pins`, `get_boards` | — | Single-call or server-managed | — |

**Cache directory structure:**

```
.keyapi-cache/
└── YYYY-MM-DD/
    ├── search_users/
    │   └── {params_hash}.json
    ├── get_user_information/
    │   └── {params_hash}.json
    ├── get_pins/
    │   └── {params_hash}.json
    ├── get_boards/
    │   └── {params_hash}.json
    ├── get_followers_detail/
    │   └── {params_hash}.json
    └── get_following_detail/
        └── {params_hash}.json
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists for the given parameters. If a valid cache file exists, load from disk and skip the API call.

### Step 4 — Synthesize and Report Findings

After collecting all API responses, produce a structured Pinterest intelligence report:

**For user profile analysis:**
1. **Profile Overview** — Username, display name, numeric user ID, bio, follower count, following count, monthly views.
2. **Content Summary** — Pin count, board count, content themes and categories.
3. **Board Taxonomy** — Board names, pin counts per board, topic diversity.
4. **Pin Analysis** — Pin type distribution (images, videos, articles), top engagement pins, recurring topics.

**For social graph analysis:**
1. **Follower Profile** — Sample follower demographics, active categories, engagement signals.
2. **Following Footprint** — Accounts followed, category interests, brand affiliations.
3. **Network Signals** — Follower-to-following ratio, audience quality indicators.

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Common Rules

| Rule | Detail |
|------|--------|
| **`get_boards` uses `entry`** | Pass the username as the `entry` parameter (not `username`). The parameter name differs from other endpoints. |
| **`userid` resolution** | `get_followers_detail` and `get_following_detail` require the numeric `userid`. Obtain it from `get_user_information` response. |
| **`get_followers_detail` pagination** | First call: pass `userid` only. Subsequent calls: pass `userid` + `node_id` + `cursor` from the previous response. |
| **`get_following_detail` pagination** | Uses `bookmark` (not `cursor`) for pagination. Pass `bookmark` from the previous response. |
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
| `400` | Bad request — invalid or missing parameters | Check `entry` vs `username` vs `userid` usage; verify numeric `userid` format |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `404` | Resource not found — user may not exist or account is private | Verify the username; private accounts may have restricted data |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry up to 3 times with a 2–3 second pause; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
