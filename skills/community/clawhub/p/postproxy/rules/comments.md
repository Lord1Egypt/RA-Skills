# Comments

Two separate APIs:
- **Post Comments** (`/api/posts/:post_id/comments`) — comments on a published post (Instagram, Facebook, Threads, YouTube, LinkedIn).
- **Profile Comments** (`/api/profiles/:profile_id/comments`) — feedback scoped to a profile/location rather than a single post. Today this exposes **Google Business reviews** (reviews live on a location, not a post).

All comment endpoints under a post require the `profile_id` query parameter.

## Post Comments

### Platform Support for Comment Actions

| Action | Instagram | Facebook | Threads | YouTube | LinkedIn |
|--------|-----------|----------|---------|---------|----------|
| List | Yes | Yes | Yes | Yes | Yes |
| Reply | Yes | Yes | Yes | Yes | Yes |
| Delete | Yes | Yes | No | Yes | Yes |
| Hide/Unhide | Yes | Yes | Yes | No | No |
| Like/Unlike | No | Yes | No | No | No |

Attempting an unsupported action returns `405 Method Not Allowed`.

### List Comments
Retrieves paginated top-level comments for a published post. Each top-level comment includes a flat `replies` array.
```bash
curl -X GET "https://api.postproxy.dev/api/posts/{post_id}/comments?profile_id={profile_id}&page=0&per_page=20" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

Query parameters:
- `profile_id` (required): Profile ID
- `page` (optional): Page number, zero-indexed (default: `0`)
- `per_page` (optional): Top-level comments per page (default: `20`)

Pagination applies to top-level comments only. All replies are flattened into the `replies` array of their root comment, sorted by `created_at` ascending. Each reply retains `parent_external_id` so the client can reconstruct the tree.

### Get Comment
```bash
curl -X GET "https://api.postproxy.dev/api/posts/{post_id}/comments/{comment_id}?profile_id={profile_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

The `comment_id` can be a Postproxy ID (e.g. `cmt_abc123`) or the platform's native external ID.

### Create Comment
Creates a comment or reply on a published post. Processed asynchronously — returns `status: "pending"` initially.
```bash
curl -X POST "https://api.postproxy.dev/api/posts/{post_id}/comments?profile_id={profile_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Thanks for the feedback everyone!"
  }'
```

To reply to an existing comment, add `parent_id`:
```bash
curl -X POST "https://api.postproxy.dev/api/posts/{post_id}/comments?profile_id={profile_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Glad you liked it!",
    "parent_id": "cmt_abc123"
  }'
```

Parameters:
- `text` (required): Comment text content
- `parent_id` (optional): Postproxy ID or external ID of comment to reply to. Omit to comment on the post itself.

### Delete Comment

> ⚠️ **Irreversible** — removes the comment from the platform. Confirm the comment (show its text/author) with the user first.

```bash
curl -X DELETE "https://api.postproxy.dev/api/posts/{post_id}/comments/{comment_id}?profile_id={profile_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

### Hide Comment
```bash
curl -X POST "https://api.postproxy.dev/api/posts/{post_id}/comments/{comment_id}/hide?profile_id={profile_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

### Unhide Comment
```bash
curl -X POST "https://api.postproxy.dev/api/posts/{post_id}/comments/{comment_id}/unhide?profile_id={profile_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

### Like Comment
```bash
curl -X POST "https://api.postproxy.dev/api/posts/{post_id}/comments/{comment_id}/like?profile_id={profile_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

### Unlike Comment
```bash
curl -X POST "https://api.postproxy.dev/api/posts/{post_id}/comments/{comment_id}/unlike?profile_id={profile_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

### Private Reply to Comment
Sends a **direct message** to the comment's author in response to that specific comment (Meta "Private Replies"). **Instagram and Facebook only.** Returns `202 Accepted` with a message in `status: "pending"`.
```bash
curl -X POST "https://api.postproxy.dev/api/posts/{post_id}/comments/{comment_id}/private_reply?profile_id={profile_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Thanks for your comment — DM-ing you the details."
  }'
```

Parameters:
- `text` (required): DM body

Notes:
- ⚠️ **This initiates a private conversation** with someone who has not messaged the account — it **bypasses the 24h messaging window** (comments up to 7 days old, Meta-enforced). Unexpected contact can trigger privacy complaints; confirm recipient and text with the user before sending.
- **One private reply per comment, ever** (Meta limit). The comment must already be published.
- No pre-existing chat needed: a chat is created (or reused) automatically, keyed by the comment author. The returned message has `external_comment_id` set. This is the same mechanism documented in [messages.md](messages.md).

### Comment Statuses
- `synced` — fetched from the platform during sync
- `pending` — created via API, being published to the platform
- `published` — successfully published to the platform
- `failed` — failed to publish to the platform

### Async Behavior
All write operations (create, delete, hide, unhide, like, unlike) are processed asynchronously. Create returns the comment with `status: "pending"` and `external_id: null`. Once published, status updates to `"published"` and `external_id` is populated.

### Comment Attachments
Synced comments carry an `attachments` array (empty when there's no media). When the platform returns media on a comment, Postproxy mirrors each asset to durable storage; the `url` is **stable** once `status` is `processed` (it does not depend on platform CDN tokens).

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Attachment hashid |
| `type` | string | `image`, `video`, `audio`, `gif`, `external`, `file` |
| `url` | string\|null | Stable storage URL. While `status` is `pending`, may temporarily fall back to the source URL |
| `status` | string | `pending` (mirroring), `processed` (ready), `failed` |
| `external_id` | string\|null | Platform-side attachment ID (omitted when not provided) |

Populated for: **Facebook** (photo/video/sticker/share), **Threads** (`IMAGE`/`VIDEO`/`AUDIO`/`GIF`), **Bluesky** (image embeds, video thumbnails/HLS, external-link thumbnails). **Instagram, YouTube, LinkedIn** comments are text-only — `attachments` is always empty. Attachments on API-created comments are not yet supported (always empty while `pending`).

### Comment Metadata Fields
The `metadata` object holds extra author signals fetched asynchronously after ingestion. It is `null` until the lookup completes; individual keys may be absent depending on platform support.

| Key | Platform | Type | Description |
|-----|----------|------|-------------|
| `author_fetched_at` | both | string | ISO 8601 timestamp of the last author-info refresh |
| `is_verified_user` | instagram, facebook | boolean | Author has a verified account |
| `is_user_follow_business` | instagram, facebook | boolean | Author follows the business profile |
| `is_business_follow_user` | instagram, facebook | boolean | The business profile follows the author |
| `follower_count` | instagram, facebook | integer | Author's follower count |

## Profile Comments (Google Business Reviews)

The Profile Comments API (`/api/profiles/:profile_id/comments`) is **separate from the post Comments API**. It surfaces feedback scoped to a profile/location rather than to a single post. Today it exposes **Google Business reviews** — reviews live on a location, not a post, so they cannot be expressed through the post-level Comments API.

### Platform Support

| Action | Google Business |
|--------|-----------------|
| List | Yes (reviews on the location) |
| Reply | Yes (reply to an existing review only — top-level authoring not allowed) |
| Delete | Yes (removes your reply; review remains) |

Other networks return `405 Method Not Allowed`.

### List Profile Comments
Retrieves reviews scoped to a profile (and optionally a placement/location). Each top-level comment includes a flat `replies` array.
```bash
curl -X GET "https://api.postproxy.dev/api/profiles/{profile_id}/comments?placement_id={location_path}&page=0&per_page=20" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

Query parameters:
- `placement_id` (optional): Filter to reviews on a single location (the `accounts/X/locations/Y` path returned by List Placements — see [profiles.md](profiles.md))
- `page` (optional): Page number, zero-indexed (default: `0`)
- `per_page` (optional): Top-level comments per page (default: `20`)

### Get Profile Comment
```bash
curl -X GET "https://api.postproxy.dev/api/profiles/{profile_id}/comments/{comment_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

The `comment_id` can be a Postproxy hashid (e.g. `cmt_abc123`) or the platform's native external ID (e.g. `accounts/.../locations/.../reviews/...`).

### Reply to Profile Comment
Creates a reply to an existing review. **Top-level comments are not allowed** — Google Business reviews come from end users, so `parent_id` is required (returns `422` if missing).
```bash
curl -X POST "https://api.postproxy.dev/api/profiles/{profile_id}/comments" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "parent_id": "accounts/1234/locations/5678/reviews/AbFvOq",
    "text": "Thanks for the kind words!"
  }'
```

Parameters:
- `parent_id` (required): Hashid or external_id of the review being replied to
- `text` (required): Reply body

Processed asynchronously — returns the new comment in status `pending`, then transitions to `published` (or `failed` / `failed_waiting_for_retry` with `error_message`).

### Delete Profile Comment
Deletes **your reply only** — the Google Business API does not let businesses delete the underlying review, so the original review row stays. Returns `{ "accepted": true }` while the delete is dispatched.
```bash
curl -X DELETE "https://api.postproxy.dev/api/profiles/{profile_id}/comments/{comment_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

### Statuses
- `synced` — fetched from Google during sync (incoming reviews)
- `pending` — reply created via API, being published to Google
- `published` — reply successfully posted to Google
- `failed` / `failed_waiting_for_retry` — reply publish failed; `error_message` populated

### Comment ID Resolution
Both `:comment_id` and `parent_id` accept either:
- Postproxy hashid (e.g. `abc123xyz`)
- External ID — the platform's native resource path (e.g. `accounts/.../locations/.../reviews/...`)

### Errors
- `404` — profile/comment/parent not found, or profile group mismatch
- `405` — action not supported for this profile's network (e.g. reply on a non-`google_business` profile)
- `422` — missing `parent_id` (top-level authoring forbidden), or replying before the parent has been published

## Webhook Events
- `comment.created` / `comment.failed` / `comment.failed_waiting_for_retry` — post comments
- `profile_comment.created` / `profile_comment.failed` / `profile_comment.failed_waiting_for_retry` — profile comments. Subscribe to `profile_comment.created` (or `*`) to receive events for both newly-synced incoming reviews and outgoing replies once published. Payload contains the same fields as a single comment fetch (`id`, `profile_id`, `platform`, `placement_id`, `external_id`, `parent_external_id`, `body`, `status`, `author_username`, `author_avatar_url`, `platform_data`, `posted_at`, `created_at`).

See [webhooks.md](webhooks.md) for subscription setup.
