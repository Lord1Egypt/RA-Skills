# @openclaw-skill/poststash

Schedule posts and threads to [Threads](https://threads.net) and [X (Twitter)](https://x.com) from OpenClaw agents via [PostStash](https://poststash.com).

## Installation

```bash
clawhub install poststash
```

## Setup

1. Go to your [PostStash dashboard](https://poststash.com/dashboard/api-keys) and generate an API key
2. Set the environment variable:
   ```bash
   export POSTSTASH_API_KEY=ps_live_...
   ```

API key format: `ps_live_` followed by 64 hex characters.

---

## Tools

### `poststash.schedule_to_threads`

Schedule a single post to Threads.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | Yes | Post content (max 500 chars) |
| `scheduled_at` | string | No | ISO 8601 timestamp; defaults to now |
| `status` | `"Ready"` \| `"Draft"` | No | Defaults to `"Ready"` |

**Response:** `{ post_id, content, schedule, status, platforms }`

---

### `poststash.schedule_to_x`

Schedule a single post to X (Twitter).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | Yes | Post content (max 280 chars) |
| `scheduled_at` | string | No | ISO 8601 timestamp; defaults to now |
| `status` | `"Ready"` \| `"Draft"` | No | Defaults to `"Ready"` |

**Response:** `{ post_id, content, schedule, status, platforms }`

---

### `poststash.schedule_thread`

Schedule a thread (2–20 posts) to Threads or X.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `platform` | `"threads"` \| `"x"` | Yes | Target platform |
| `posts` | `{ text: string }[]` | Yes | 2–20 posts in the thread |
| `scheduled_at` | string | No | ISO 8601 timestamp; defaults to now |
| `status` | `"Ready"` \| `"Draft"` | No | Defaults to `"Ready"` |

**Response:** `{ thread_id, posts: [{ id, content, thread_position, schedule, status }] }`

---

### `poststash.get_post`

Fetch a post and its analytics.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `post_id` | string | Yes | Post UUID |

**Response:** `{ post, analytics }`

The `analytics` array contains per-platform metrics: `views`, `likes`, `replies`, `reposts`, `quotes`.

---

### `poststash.list_posts`

List posts scoped to your API key's context.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | `"Draft"` \| `"Ready"` \| `"Published"` \| `"Failed"` | No | Filter by status |
| `published` | boolean | No | Filter by published state |
| `limit` | number | No | Results per page (default: 20, max: 100) |
| `offset` | number | No | Pagination offset (default: 0) |

**Response:** `{ posts, total, limit, offset }`

---

## Examples

### Schedule a single post

```typescript
import { scheduleToThreads } from "@openclaw-skill/poststash";

const result = await scheduleToThreads.execute({
  text: "AI agents can now schedule posts via PostStash 🤖",
  scheduled_at: "2025-03-01T14:30:00Z",
});
console.log(result.post_id); // UUID of scheduled post
```

### Schedule a thread

```typescript
import { scheduleThread } from "@openclaw-skill/poststash";

const result = await scheduleThread.execute({
  platform: "x",
  posts: [
    { text: "1/ Here is a thread about building in public" },
    { text: "2/ Ship fast, learn faster" },
    { text: "3/ That's a wrap. Follow for more 👋" },
  ],
  scheduled_at: "2025-03-01T14:30:00Z",
});
console.log(result.thread_id);
```

### Check post status

```typescript
import { getPost } from "@openclaw-skill/poststash";

const { post, analytics } = await getPost.execute({
  post_id: "6b79ac1e-fc70-4a5e-a45f-4769f47300b5",
});
console.log(post.status);     // "Published"
console.log(analytics[0].metrics.views); // 2340
```

### List recent posts

```typescript
import { listPosts } from "@openclaw-skill/poststash";

const { posts, total } = await listPosts.execute({
  status: "Ready",
  limit: 10,
});
console.log(`${total} ready posts, showing first ${posts.length}`);
```

### Agent usage

```typescript
const result = await agent.invoke({
  tools: ["poststash.schedule_to_threads"],
  input: "Schedule a post about AI to Threads tomorrow at 2pm",
});
```

---

## Error Handling

All tools throw an `Error` with the API error message on failure. Common errors:

| Error | Fix |
|-------|-----|
| `POSTSTASH_API_KEY environment variable is not set` | Set the env var |
| `Unauthorized` | Check your API key format (`ps_live_...`) |
| `platform must be one of: threads, x` | Use `"threads"` or `"x"` |
| `text is required` | Add text to the post |
| `posts must have at least 2 posts` | Add more posts to the thread |
| `A thread can have at most 20 posts` | Reduce thread length |

---

## Development

```bash
npm run build   # Compile TypeScript
npm run test    # Run tests
```

---

## Links

- [PostStash](https://poststash.com)
- [API Documentation](https://poststash.com/docs/api)
- [Dashboard / API Keys](https://poststash.com/dashboard/api-keys)
- [OpenClaw](https://openclaw.ai)
