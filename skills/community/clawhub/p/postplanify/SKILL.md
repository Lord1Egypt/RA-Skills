---
name: postplanify
description: Schedule and manage social media posts on Instagram, Facebook, X, LinkedIn, TikTok, YouTube, Threads, Pinterest, Bluesky and Google Business Profile through the PostPlanify API. Upload images and videos, read post and account analytics, and reply to comments.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - POSTPLANIFY_API_KEY
      bins:
        - curl
    primaryEnv: POSTPLANIFY_API_KEY
    envVars:
      - name: POSTPLANIFY_API_KEY
        required: true
        description: PostPlanify API key (starts with sk_live_), created at https://postplanify.com/dashboard/api-keys
    emoji: "🗓️"
    homepage: https://postplanify.com/docs
---

# PostPlanify

Schedule, edit and review social media posts through the [PostPlanify](https://postplanify.com) REST API, upload media, read analytics, and reply to comments.

**Use this skill when** the user has a PostPlanify account and wants to: schedule or publish a post, upload an image or video for a post, see what is scheduled or published, edit, cancel or delete a scheduled post, check how posts or accounts are performing, or read and reply to comments and Google reviews.

**Do not use it for** writing captions with no intent to post, or general social media advice.

The only tool this skill uses is `curl`. Nothing is installed or run besides HTTPS requests to `https://api.postplanify.com`.

## Setup

1. Create an API key at https://postplanify.com/dashboard/api-keys. Keys start with `sk_live_`.
2. Set it as `POSTPLANIFY_API_KEY` in the agent's environment. Never print the key or paste it into a post, a log, or a reply.
3. API access needs a PostPlanify plan with API access (Premium or higher), on your own account or on a workspace you belong to. Without it every call returns `403 SUBSCRIPTION_INACTIVE`.

Check the key works:

```bash
curl -s https://api.postplanify.com/api/v1/me \
  -H "Authorization: Bearer $POSTPLANIFY_API_KEY"
```

## Basics

- **Base URL:** `https://api.postplanify.com/api/v1`
- **Auth header:** `Authorization: Bearer $POSTPLANIFY_API_KEY` on every request
- **Success:** `{ "ok": true, "data": ... }`, plus `pagination` on list endpoints
- **Error:** `{ "ok": false, "error": { "code": "...", "message": "..." } }`. Show the `message` to the user; it says exactly what is wrong.
- **Times are UTC**, ISO 8601 (`2026-03-15T20:00:00.000Z`). Convert the user's local time to UTC before sending. If you do not know the user's timezone, ask.
- **Limits:** 100 requests per minute per key. Per social account: 6 posts per hour and 100 per day, counted by scheduled time.

## Safety rules

1. **Confirm before publishing.** Before creating a post, show the user the account(s), the exact caption, the media, and the publish time in their timezone, and wait for a yes. An earlier approval does not cover a new or changed post.
2. **Confirm before destructive actions.** Deleting a post or media, or cancelling a scheduled post, needs an explicit yes for that specific item.
3. **Replies are public and immediate.** Replying to a comment posts it on the platform right away; there is no scheduling or undo. Show the reply text and get a yes first.
4. **Start small.** When asked to schedule many posts, create one or two first, show the result, then continue.
5. **No silent retries.** If a create fails with `400`, fix the cause from the error message or ask the user. Never resend the same post in a loop; that risks duplicates.
6. **`403` is final.** `SUBSCRIPTION_INACTIVE` (no API access) or `FORBIDDEN` (the user's workspace role does not allow it) will not change on retry. Tell the user and stop.
7. **`429`:** "Too many requests" means wait a minute and retry. "Maximum 6 posts per hour / 100 per day per social account" means pick a different time; do not retry the same time.

## Core workflow

### 1. Find the workspace and account

```bash
curl -s https://api.postplanify.com/api/v1/workspaces \
  -H "Authorization: Bearer $POSTPLANIFY_API_KEY"
```

Each workspace includes its `socialAccounts` (`id`, `platform`, `accountName`, `customLabel`). You need a `workspaceId` and a `socialAccountId` to post. If the user names an account ("our Instagram", "the Downtown page"), match on `platform`, `accountName` and `customLabel`. If more than one matches, ask.

### 2. Add media (if any)

From a public URL (preferred, no local file needed):

```bash
curl -s -X POST https://api.postplanify.com/api/v1/media/from-url \
  -H "Authorization: Bearer $POSTPLANIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/photo.jpg"}'
```

From a local file:

```bash
curl -s -X POST https://api.postplanify.com/api/v1/media/upload \
  -H "Authorization: Bearer $POSTPLANIFY_API_KEY" \
  -F "file=@/path/to/video.mp4"
```

Both return `data.id`. Allowed: JPEG, PNG, GIF, WebP, MP4, MOV, PDF, up to 100 MB. For carousels, upload in the order the items should appear.

To reuse files already in the user's PostPlanify media library: `GET /media?workspaceId=...` (without `workspaceId` you only see API uploads).

### 3. Create the post

```bash
curl -s -X POST https://api.postplanify.com/api/v1/posts \
  -H "Authorization: Bearer $POSTPLANIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workspaceId": "WORKSPACE_ID",
    "socialAccountId": "SOCIAL_ACCOUNT_ID",
    "caption": "Our spring collection is live!",
    "scheduledAt": "2026-03-15T20:00:00.000Z",
    "mediaIds": ["MEDIA_ID"]
  }'
```

- One post goes to one social account. To post to several accounts, create one post per account (adapt the caption to each platform's limits).
- `scheduledAt` is required and must be in the future. For "post now", use a time 2 to 5 minutes ahead.
- A post needs a caption, media, or both. Some platforms need media or extra fields; check `references/platform-configs.md` before posting to Instagram, TikTok, YouTube, Pinterest or Google Business.
- The response is the created post with `status: "SCHEDULED"`. It publishes automatically at `scheduledAt`.

### 4. Check the result

```bash
curl -s https://api.postplanify.com/api/v1/posts/POST_ID \
  -H "Authorization: Bearer $POSTPLANIFY_API_KEY"
```

`status` becomes `PUBLISHED` after publishing. `logs` holds success, warning and error messages from the publish attempt; read them if the user asks why a post failed. `metrics` has the latest views, likes, comments and shares once analytics have synced (`null` means no data yet, not zero).

## Other tasks

| Task | Request |
|---|---|
| List posts | `GET /posts?workspaceId=...` with optional `status`, `platform`, `socialAccountId`, `from`, `to`, `includeMetrics=true`, `page`, `limit` (max 100) |
| Edit a scheduled post | `PATCH /posts/{id}` with only the fields to change (`caption`, `scheduledAt`, platform params) |
| Cancel (keep it, stop publishing) | `POST /posts/{id}/cancel` |
| Delete permanently | `DELETE /posts/{id}` |
| Delete uploaded media | `DELETE /media/{id}` |
| Pinterest boards | `GET /social-accounts/{id}/pinterest-boards` |
| Workspace analytics (last 7 days) | `GET /analytics/{workspaceId}/overview` |
| One account's analytics | `GET /analytics/{workspaceId}/{socialAccountId}` |
| Trends over time | `GET /analytics/{workspaceId}/{socialAccountId}/trends?days=30` (1 to 365) |
| Comments and reviews | `GET /comments?workspaceId=...` with optional `platform`, `socialAccountId`, `unreadOnly=true` |
| Replies to a comment | `GET /comments/{platformCommentId}/replies` |
| Reply to a comment | `POST /comments/{platformCommentId}/reply` with `{"message": "..."}` |

Only `SCHEDULED` and `RESCHEDULED` posts can be edited or cancelled. Draft posts are not available through the API.

Comments cover Instagram, Facebook, LinkedIn and Google Business (reviews have a `rating`). LinkedIn comment IDs are URNs: URL-encode them in the path.

## References

- `references/api-reference.md`: every endpoint with parameters, request bodies, responses and error codes.
- `references/platform-configs.md`: media rules, caption limits and platform-specific fields (YouTube, TikTok, Pinterest, Google Business, X, stories, link shortening).
- Full OpenAPI spec: https://postplanify.com/openapi.yaml
