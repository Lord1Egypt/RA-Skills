# Posts

Create, schedule, update, publish, and delete posts. For platform-specific parameters (Instagram formats, YouTube titles, Telegram `chat_id`, Google Business `location_id`, …) see [platforms.md](platforms.md). For queue-based scheduling see [queues.md](queues.md). For performance metrics see [analytics.md](analytics.md).

## List Posts
```bash
curl -X GET "https://api.postproxy.dev/api/posts" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

## Get Post
```bash
curl -X GET "https://api.postproxy.dev/api/posts/{id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

## Create Post (JSON with media URLs)

> Posts publish **immediately and publicly** unless `post[draft]=true` or `scheduled_at` is set. Confirm content and target profiles with the user first. For Facebook/LinkedIn/Pinterest/Telegram/Google Business, specify the placement explicitly — Facebook otherwise posts to a **random connected page** (see [profiles.md](profiles.md)).
```bash
curl -X POST "https://api.postproxy.dev/api/posts" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "post": {
      "body": "Post content here"
    },
    "profiles": ["twitter", "linkedin", "threads"],
    "media": ["https://example.com/image.jpg"]
  }'
```

## Create Post (File Upload)
Use multipart form data to upload local files:
```bash
curl -X POST "https://api.postproxy.dev/api/posts" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -F "post[body]=Check out this image!" \
  -F "profiles[]=instagram" \
  -F "profiles[]=twitter" \
  -F "media[]=@/path/to/image.jpg" \
  -F "media[]=@/path/to/image2.png"
```

## Create Draft
Add `post[draft]=true` to create without publishing:
```bash
curl -X POST "https://api.postproxy.dev/api/posts" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -F "post[body]=Draft post content" \
  -F "profiles[]=twitter" \
  -F "media[]=@/path/to/image.jpg" \
  -F "post[draft]=true"
```

## Publish Draft
```bash
curl -X POST "https://api.postproxy.dev/api/posts/{id}/publish" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

Profile options: `facebook`, `instagram`, `tiktok`, `linkedin`, `youtube`, `twitter`, `threads`, `pinterest`, `bluesky`, `telegram`, `google_business` (or use profile IDs)

## Schedule Post
Add `scheduled_at` to post object:
```bash
curl -X POST "https://api.postproxy.dev/api/posts" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "post": {
      "body": "Scheduled post",
      "scheduled_at": "2026-06-16T09:00:00Z"
    },
    "profiles": ["twitter"]
  }'
```

To schedule via a posting queue instead of a fixed time, pass `queue_id` (see [queues.md](queues.md)). Do not pass `scheduled_at` together with `queue_id`.

## Create Thread (Tweet Chain / Thread Post)
Threads allow you to create a sequence of posts published as replies. Supported on X (Twitter), Threads, and Bluesky.
```bash
curl -X POST "https://api.postproxy.dev/api/posts" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "post": {
      "body": "1/ Here is a thread about our product launch"
    },
    "profiles": ["twitter", "threads"],
    "thread": [
      { "body": "2/ First, we built the foundation..." },
      { "body": "3/ Then we added the key features..." },
      { "body": "4/ And finally, we launched! Check it out at example.com" }
    ]
  }'
```

With media in thread posts:
```bash
curl -X POST "https://api.postproxy.dev/api/posts" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "post": {
      "body": "1/ Here is a thread with screenshots"
    },
    "profiles": ["twitter"],
    "thread": [
      {
        "body": "2/ First feature",
        "media": ["https://example.com/screenshot1.jpg"]
      },
      {
        "body": "3/ Second feature",
        "media": ["https://example.com/screenshot2.jpg"]
      }
    ]
  }'
```

### Supported Platforms
- **X (Twitter)** — each post is published as a reply to the previous tweet
- **Threads** — each post is published as a reply to the previous Threads post
- **Bluesky** — each post is published as a reply to the previous Bluesky post

Attempting to create a thread with other platforms (Instagram, Facebook, LinkedIn, etc.) will return a `422` error.

### How Threads Work
1. The parent post (`post[body]`) is published first on each platform
2. Each child post in the `thread` array is published sequentially as a reply to the previous post
3. Per-platform chains are independent — the X, Threads, and Bluesky chains run in parallel
4. Position is determined by the array order (first item = first reply, etc.)

### Thread Parameter Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `body` | string | Yes | Text content for this thread post |
| `media` | array | No | Array of media URLs (same format as top-level `media`) |

### Thread Error Handling
- If a post in the thread chain fails, subsequent posts in that chain will **wait** (they are not published)
- Each platform chain is independent — a failure on X does not block the Threads chain

## Update Post
Updates an existing post. Only drafts and scheduled posts more than 5 minutes before publish time can be updated. All body fields are optional — only send what you want to change.
```bash
curl -X PATCH "https://api.postproxy.dev/api/posts/{id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "post": {
      "body": "Updated post content!"
    }
  }'
```

Body parameters (all optional):
- `post[body]`: Updated text content
- `post[scheduled_at]`: Updated ISO 8601 schedule timestamp
- `post[draft]`: Set/unset draft status
- `profiles`: **Full replace** — array of profile IDs or network names
- `platforms`: **Merged** with existing platform params (per network)
- `media`: **Full replace** — array of URLs (send `[]` to remove all)
- `thread`: **Full replace** — array of thread children (send `[]` to remove all)
- `queue_id`: Assign post to a queue
- `queue_priority`: `high`, `medium`, or `low`

Update behavior:
- `post` fields are merged with existing values
- `profiles`, `media`, `thread` are full-replace — omitted = unchanged, `[]` = clear
- `platforms` is merged into existing params per network. Sending `{"platforms": {"youtube": {"privacy_status": "unlisted"}}}` updates only that field
- Thread children inherit parent's profiles, scheduling, draft status

Example: replace profiles and media:
```bash
curl -X PATCH "https://api.postproxy.dev/api/posts/{id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "profiles": ["twitter", "threads"],
    "media": ["https://example.com/new-image.jpg"]
  }'
```

Example: update platform params only:
```bash
curl -X PATCH "https://api.postproxy.dev/api/posts/{id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": {
      "youtube": { "privacy_status": "unlisted" }
    }
  }'
```

Errors:
- `422` "Post cannot be edited" — post is published or within 5min of scheduled publish
- `422` "Profile not found for {id}"
- `422` "Invalid platform params for {network}: {key}"
- `404` "Not found"

## Delete Post

> ⚠️ **Destructive.** DB-only deletion leaves the post live on the social networks; `delete_on_platform=true` removes it from the platforms **irreversibly**. Confirm the post (show its body/ID) and the scope with the user before deleting.

By default removes only from DB. Pass `delete_on_platform=true` to also remove from social platforms first.
```bash
curl -X DELETE "https://api.postproxy.dev/api/posts/{id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

Delete from DB AND from all published platforms:
```bash
curl -X DELETE "https://api.postproxy.dev/api/posts/{id}?delete_on_platform=true" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

Query parameter:
- `delete_on_platform` (optional, default `false`): If `true`, deletes from all published platforms before removing from DB

## Delete on Platform

> ⚠️ **Irreversible.** This removes live content from the user's social accounts and cannot be undone. Get explicit confirmation of post and scope (all platforms vs one network/profile) first.

Async deletes a published post from social platforms WITHOUT removing it from the DB. Optionally scope to a specific platform/profile. If no scope is given, deletes from all published platforms.
```bash
curl -X POST "https://api.postproxy.dev/api/posts/{id}/delete_on_platform" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

Scope by network:
```bash
curl -X POST "https://api.postproxy.dev/api/posts/{id}/delete_on_platform" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"network": "twitter"}'
```

Scope by profile ID:
```bash
curl -X POST "https://api.postproxy.dev/api/posts/{id}/delete_on_platform" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"profile_id": "prof_abc123"}'
```

Scope by post profile ID (covers entire thread for that profile):
```bash
curl -X POST "https://api.postproxy.dev/api/posts/{id}/delete_on_platform" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"post_profile_id": "pp_abc123"}'
```

Body parameters (all optional, omit all = delete from every published platform):
- `post_profile_id`: ID of a specific post profile. Resolves to the underlying profile, deletes across the entire thread
- `profile_id`: ID of a profile. Deletes all post profiles for this profile on the post
- `network`: Network name. Deletes all post profiles for this network on the post

Supported platforms: `facebook`, `threads`, `twitter`, `linkedin`, `pinterest`, `youtube`, `bluesky`, `telegram`, `google_business`.
NOT supported: `instagram`, `tiktok` — request returns `422` if scoped to one of these.

Response (200):
```json
{
  "success": true,
  "deleting": [
    { "post_profile_id": "pp_abc123", "platform": "twitter" }
  ]
}
```

After triggering, platform status transitions: `published` → `pending_deletion` → `deleted`.

## Webhook Events
- `post.processed` / `post.imported` — post-level lifecycle
- `platform_post.published` / `platform_post.failed` / `platform_post.failed_waiting_for_retry` — per-platform publish results
- `platform_post.insights` — new per-post stats snapshot
- `media.failed` — media processing failure

See [webhooks.md](webhooks.md) for subscription setup.
