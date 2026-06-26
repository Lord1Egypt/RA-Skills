---
name: poststash
description: Schedule posts and threads to Threads and X via PostStash
version: 1.0.0
author: Julien / PostStash
homepage: https://poststash.com/docs/api
license: MIT
metadata: {
  "openclaw": {
    "emoji": "📮",
    "requires": {
      "env": ["POSTSTASH_API_KEY"]
    }
  }
}
---

# PostStash Skill

Schedule posts and threads to Threads and X directly from your OpenClaw agent.

## Setup

1. Get an API key from the [PostStash dashboard](https://poststash.com/dashboard/api-keys)
2. Set the environment variable:
   ```bash
   POSTSTASH_API_KEY=ps_live_...
   ```
3. Install: `clawhub install poststash`

API key format: `ps_live_` followed by 64 hex characters.

---

## Tools

### `poststash.schedule_to_threads`

Schedule a single post to Threads.

**Input:**
- `text` (string, required) — Post content (max 500 characters)
- `scheduled_at` (string, optional) — ISO 8601 timestamp; defaults to now
- `status` (string, optional) — `"Ready"` (publishes at scheduled_at) or `"Draft"` (saves without scheduling); defaults to `"Ready"`

**Output:**
- `post_id` — UUID of the scheduled post
- `content` — Post text
- `schedule` — Scheduled timestamp (ISO 8601)
- `status` — Post status (`Ready`, `Draft`, `Published`, `Failed`)
- `platforms` — Array of target platforms

---

### `poststash.schedule_to_x`

Schedule a single post to X (Twitter).

**Input:** Same as `schedule_to_threads`.

**Output:** Same as `schedule_to_threads`.

---

### `poststash.schedule_thread`

Schedule a thread (2–20 posts) to Threads or X.

**Input:**
- `platform` (string, required) — `"threads"` or `"x"`
- `posts` (array, required) — Array of `{ text: string }` objects (2–20 items)
- `scheduled_at` (string, optional) — ISO 8601 timestamp; defaults to now
- `status` (string, optional) — `"Ready"` or `"Draft"`; defaults to `"Ready"`

**Output:**
- `thread_id` — UUID grouping all thread posts
- `posts` — Array of scheduled post objects with `id`, `content`, `thread_position`

---

### `poststash.get_post`

Fetch a scheduled or published post along with its analytics.

**Input:**
- `post_id` (string, required) — Post UUID from a schedule response

**Output:**
- `post` — Full post object (`id`, `content`, `platforms`, `schedule`, `status`, `published`, `sent_at`)
- `analytics` — Array of per-platform analytics with `metrics` (views, likes, replies, reposts, quotes)

---

### `poststash.list_posts`

List posts for your account (scoped to the context of your API key).

**Input:**
- `status` (string, optional) — Filter by `"Draft"`, `"Ready"`, `"Published"`, or `"Failed"`
- `published` (boolean, optional) — `true` or `false`
- `limit` (number, optional) — Results per page (default: 20, max: 100)
- `offset` (number, optional) — Pagination offset (default: 0)

**Output:**
- `posts` — Array of post objects
- `total` — Total number of matching posts
- `limit` / `offset` — Pagination info

---

## Example Agent Usage

```typescript
const result = await agent.invoke({
  tools: ["poststash.schedule_to_threads"],
  input: "Schedule a post about AI to Threads tomorrow at 2pm",
});

const thread = await agent.invoke({
  tools: ["poststash.schedule_thread"],
  input: "Create a 3-part thread on building in public on X, schedule for Friday 10am",
});
```
