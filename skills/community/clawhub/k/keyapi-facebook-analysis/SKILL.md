---
name: keyapi-facebook-analysis
description: Explore and analyze public Facebook data — profile details, posts, photos, Reels, group activity, group events, and identifier resolution for profiles and groups.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"👥"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-facebook-analysis

> Explore and analyze public Facebook profiles, pages, and groups — from profile details and content feeds to group activity, events, and identifier resolution.

This skill provides comprehensive public Facebook intelligence using the KeyAPI MCP service. It enables retrieval of profile details (by URL or numeric ID), published posts, photos, Reels, group details, group posts, future group events, and ID resolution for both profiles and groups — all through a unified, cache-first workflow.

Use this skill when you need to:
- Retrieve a public Facebook profile's details, posts, photos, or Reels by URL
- Resolve a profile URL to its numeric profile ID for downstream API calls
- Analyze public Facebook group activity — posts, member details, and upcoming events
- Resolve a group URL to its numeric group ID
- Research brand pages, public figures, or community groups on Facebook

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

All tool calls in this skill target the KeyAPI Facebook MCP server:

```
Server URL : https://mcp.keyapi.ai/facebook/mcp
Auth Header: Authorization: Bearer $KEYAPI_TOKEN
```

**Setup (one-time):**

```bash
# 1. Install dependencies
npm install

# 2. Set your API token (get one free at https://keyapi.ai/)
export KEYAPI_TOKEN=your_token_here

# 3. List all available tools to verify the connection
node scripts/run.js --platform facebook --list-tools
```

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Analysis Scenarios

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Full profile details from a URL | `profile_details_by_url` | Quick profile snapshot without knowing the numeric ID |
| Resolve profile URL → numeric ID | `get_profile_id` | ID resolution for use with `profile_posts`, `profiles_photos`, `profile_reels` |
| Profile details by numeric ID | `profiles_details_by_id` | Profile lookup when ID is already known |
| Published posts from a profile/page | `profile_posts` | Content feed analysis, posting cadence |
| Photos from a profile/page | `profiles_photos` | Visual content audit, photo library |
| Reels from a profile/page | `profile_reels` | Short-video content analysis |
| Group details from a URL | `get_group_details` | Group overview, member count, description |
| Resolve group URL → numeric group ID | `get_group_id` | ID resolution for `get_group_posts` and `get_group_future_events` |
| Posts from a public group | `get_group_posts` | Group activity monitoring, content analysis |
| Upcoming events in a group | `get_group_future_events` | Event discovery, community activity tracking |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify Analysis Targets and Select Nodes

Clarify the research objective and map it to one or more nodes. Typical entry points:

- **Profile research by URL**: Use `profile_details_by_url` for a quick snapshot, OR use `get_profile_id` to obtain the numeric `profile_id` then call `profiles_details_by_id`.
- **Profile content audit**: Call `get_profile_id` first, then use `profile_posts`, `profiles_photos`, `profile_reels` with the numeric ID.
- **Group research**: Use `get_group_details` with the full URL, then `get_group_id` to obtain `group_id` for `get_group_posts` and `get_group_future_events`.

> **Critical: Three Distinct Identifier Types**
>
> Facebook endpoints require different identifiers depending on the endpoint:
>
> | Identifier | Format | Used by |
> |---|---|---|
> | Profile URL | Full URL, e.g., `https://www.facebook.com/mantraindianfolsom` | `profile_details_by_url`, `get_profile_id` |
> | Numeric profile ID | Integer string, e.g., `100063669491743` | `profile_posts`, `profiles_photos`, `profiles_details_by_id` |
> | `reels_profile_id` | Base64 collection ID (opaque string) | `profile_reels` only |
> | Group URL | Full group URL, e.g., `https://www.facebook.com/groups/1270525996445602/` | `get_group_details`, `get_group_id` |
> | Numeric group ID | Integer string, e.g., `1439220986320043` | `get_group_posts`, `get_group_future_events` |

> **`profile_reels` — Special `reels_profile_id`**
>
> `profile_reels` uses a distinct `reels_profile_id` parameter that is **NOT** the same as the numeric `profile_id`. This opaque base64 collection ID is obtained from the `profile_details_by_url` or `profiles_details_by_id` response data. You cannot derive it from the numeric profile ID alone.
>
> Workflow: `profile_details_by_url` (or `get_profile_id` → `profiles_details_by_id`) → extract `reels_profile_id` from response → call `profile_reels`.

> **Public Content Only**
>
> All endpoints in this skill return data from **public** Facebook profiles, pages, and groups only. Private profiles, private groups, and content requiring login cannot be accessed.

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters and available options:

```bash
node scripts/run.js --platform facebook --schema <tool_name>

# Examples
node scripts/run.js --platform facebook --schema profile_details_by_url
node scripts/run.js --platform facebook --schema get_group_posts
```

### Step 3 — Call APIs and Cache Results Locally

Execute tool calls and persist responses to the local cache to avoid redundant API calls.

**Calling a tool:**

```bash
# Single call with pretty output
node scripts/run.js --platform facebook --tool <tool_name> \
  --params '<json_args>' --pretty

# Force fresh data, skip cache
node scripts/run.js --platform facebook --tool <tool_name> \
  --params '<json_args>' --no-cache --pretty
```

**Example — get profile details by URL:**

```bash
node scripts/run.js --platform facebook --tool profile_details_by_url \
  --params '{"url":"https://www.facebook.com/mantraindianfolsom"}' --pretty
```

**Example — resolve URL to profile ID, then get posts:**

```bash
# Step 1: resolve URL to numeric profile_id
node scripts/run.js --platform facebook --tool get_profile_id \
  --params '{"url":"https://www.facebook.com/mantraindianfolsom"}' --pretty

# Step 2: get posts using numeric profile_id
node scripts/run.js --platform facebook --tool profile_posts \
  --params '{"profile_id":"100063669491743"}' --pretty
```

**Example — get next page of posts using cursor:**

```bash
node scripts/run.js --platform facebook --tool profile_posts \
  --params '{"profile_id":"100063669491743","cursor":"<cursor_from_previous_response>"}' --pretty
```

**Example — get profile Reels (requires reels_profile_id from profile details):**

```bash
# Step 1: get profile details to obtain reels_profile_id
node scripts/run.js --platform facebook --tool profile_details_by_url \
  --params '{"url":"https://www.facebook.com/examplepage"}' --pretty
# Extract reels_profile_id from response

# Step 2: get reels using reels_profile_id
node scripts/run.js --platform facebook --tool profile_reels \
  --params '{"reels_profile_id":"<reels_profile_id_from_response>"}' --pretty
```

**Example — resolve group URL, then get posts:**

```bash
# Step 1: resolve group URL to numeric group_id
node scripts/run.js --platform facebook --tool get_group_id \
  --params '{"url":"https://www.facebook.com/groups/1270525996445602/"}' --pretty

# Step 2: get group posts
node scripts/run.js --platform facebook --tool get_group_posts \
  --params '{"group_id":"1439220986320043","sorting_order":"CHRONOLOGICAL"}' --pretty
```

**Example — get group details and future events:**

```bash
node scripts/run.js --platform facebook --tool get_group_details \
  --params '{"url":"https://www.facebook.com/groups/1270525996445602/"}' --pretty

node scripts/run.js --platform facebook --tool get_group_future_events \
  --params '{"group_id":"1571965316444595"}' --pretty
```

**Pagination:**

| Endpoint | Pagination parameter | Notes |
|---|---|---|
| `profile_posts`, `get_group_posts`, `get_group_future_events` | `cursor` (string) | Pass cursor from previous response; omit for first call |
| `profiles_photos` | `cursor` (string) | Also accepts optional `collection_id` to scope to a specific album |
| `profile_reels` | `cursor` (string) | Pass cursor from previous response; omit for first call |
| `profile_details_by_url`, `profiles_details_by_id`, `get_profile_id`, `get_group_details`, `get_group_id` | — | Single-call response |

**`get_group_posts` sorting options:**

| Value | Description |
|---|---|
| `CHRONOLOGICAL` | Most recent posts first (default) |
| `TOP_POSTS` | Highest engagement posts first |
| `RECENT_ACTIVITY` | Posts with recent activity (comments/reactions) |
| `CHRONOLOGICAL_LISTINGS` | Chronological order for listing-type posts |

**Cache directory structure:**

```
.keyapi-cache/
└── YYYY-MM-DD/
    ├── profile_details_by_url/
    │   └── {params_hash}.json
    ├── profile_posts/
    │   └── {params_hash}.json
    ├── profiles_photos/
    │   └── {params_hash}.json
    ├── profile_reels/
    │   └── {params_hash}.json
    ├── profiles_details_by_id/
    │   └── {params_hash}.json
    ├── get_profile_id/
    │   └── {params_hash}.json
    ├── get_group_posts/
    │   └── {params_hash}.json
    ├── get_group_details/
    │   └── {params_hash}.json
    ├── get_group_id/
    │   └── {params_hash}.json
    └── get_group_future_events/
        └── {params_hash}.json
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists for the given parameters. If a valid cache file exists, load from disk and skip the API call.

### Step 4 — Synthesize and Report Findings

After collecting all API responses, produce a structured intelligence report:

**For profile/page analysis:**
1. **Profile Overview** — Name, numeric ID, profile type (personal/page), bio, follower count, verification status, category.
2. **Content Inventory** — Post count, photo count, Reels count, posting frequency, content type distribution.
3. **Engagement Signals** — Reaction counts, comment counts, share counts on posts.
4. **Visual Content** — Photo collections, album topics, Reels themes.

**For group analysis:**
1. **Group Overview** — Name, numeric group ID, member count, privacy type (public), description, creation date.
2. **Activity Profile** — Post frequency, top contributors, discussion themes.
3. **Event Calendar** — Upcoming events, event type, organizer, date/time distribution.

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Common Rules

| Rule | Detail |
|------|--------|
| **Profile ID resolution** | `profile_posts`, `profiles_photos`, `profiles_details_by_id` require the numeric `profile_id`. Use `get_profile_id` or `profile_details_by_url` to obtain it from a URL. |
| **`profile_reels` identifier** | Requires `reels_profile_id` (a base64 collection ID), NOT the numeric `profile_id`. Extract it from `profile_details_by_url` or `profiles_details_by_id` response. |
| **Group ID resolution** | `get_group_posts` and `get_group_future_events` require numeric `group_id`. Use `get_group_id` with the full group URL to obtain it. |
| **Public content only** | All endpoints return data from public profiles, pages, and groups only. Private content is inaccessible. |
| **Cursor pagination** | Use `cursor` from the previous response for all paginated endpoints. Omit for the first call. |
| **`profiles_photos` collection** | Pass optional `collection_id` to scope photo results to a specific album. Leave empty to fetch all photos. |
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
| `400` | Bad request — invalid or missing parameters | Validate URL format; ensure numeric IDs are strings, not integers; check `reels_profile_id` source |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `404` | Resource not found — profile or group may be private or deleted | Verify the URL; private profiles and groups cannot be accessed |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry up to 3 times with a 2–3 second pause; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
