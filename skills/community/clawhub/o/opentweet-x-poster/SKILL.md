---
name: x-poster
description: Post to X (Twitter) using the OpenTweet API. Create tweets, schedule posts, publish threads, upload media, run an evergreen queue, search inspiration tweets, repurpose them with AI, and read engagement-weighted analytics — all autonomously.
version: 1.4.0
homepage: https://opentweet.io/features/openclaw-twitter-posting
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["OPENTWEET_API_KEY"]},"primaryEnv":"OPENTWEET_API_KEY"}}
---

# OpenTweet X Poster

You can post to X (Twitter) using the OpenTweet REST API. All requests go to `https://opentweet.io` with the user's API key.

## Authentication

Every request needs this header:
```
Authorization: Bearer $OPENTWEET_API_KEY
Content-Type: application/json
```

For file uploads, use `Content-Type: multipart/form-data` instead.

## Before You Start

ALWAYS verify the connection first:
```
GET https://opentweet.io/api/v1/me
```
Returns subscription status, daily post limits, post counts, and connected X accounts. Check `subscription.has_access` is true and `limits.remaining_posts_today` > 0 before scheduling or publishing.

## Multi-Account Support

Pro users get 1 X account, Advanced 3, Agency 10. Use the `x_account_id` parameter to target a specific account.

### List connected accounts
```
GET https://opentweet.io/api/v1/accounts
```
Returns: `{ "accounts": [{ "id": "...", "x_handle": "@handle", "x_name": "Display Name", "is_primary": true, "nickname": null }] }`

### Using x_account_id
Add `x_account_id` to any POST/PUT body or GET query parameter to target a specific X account:
- **Creating posts**: `{ "text": "...", "x_account_id": "account_id_here" }`
- **Listing posts**: `GET /api/v1/posts?x_account_id=account_id_here`
- **Batch schedule**: `{ "schedules": [...], "x_account_id": "account_id_here" }`
- **Analytics**: `GET /api/v1/analytics/overview?x_account_id=account_id_here`
- **Evergreen**: `GET /api/v1/evergreen/posts?x_account_id=account_id_here`
- **Best-times analyze**: `POST /api/v1/analytics/best-times/analyze` body `{ "x_account_id": "..." }`

When `x_account_id` is omitted, the primary account is used. Single-account users never need to specify it.

## Post Management

### Create a tweet
```
POST https://opentweet.io/api/v1/posts
Body: { "text": "Your tweet text" }
```
Optionally add `"scheduled_date": "2026-05-01T10:00:00Z"` to schedule it (requires active subscription, date must be in the future).

### Create and publish immediately (one step)
```
POST https://opentweet.io/api/v1/posts
Body: { "text": "Hello from the API!", "publish_now": true }
```
Creates the post AND publishes to X in one request. Cannot combine with `scheduled_date` or bulk posts. Response includes `status: "posted"`, `x_post_id`, and `url` (the real X post URL) on success.

### Create a tweet with media
```
POST https://opentweet.io/api/v1/posts
Body: {
  "text": "Check out this screenshot!",
  "media_urls": ["https://url-from-upload-endpoint"]
}
```
Upload media first via `POST /api/v1/upload`, then pass the returned URL(s) in `media_urls`.

### Create a thread
```
POST https://opentweet.io/api/v1/posts
Body: {
  "text": "First tweet of the thread",
  "is_thread": true,
  "thread_tweets": ["Second tweet", "Third tweet"]
}
```

### Create a thread with per-tweet media
```
POST https://opentweet.io/api/v1/posts
Body: {
  "text": "Thread intro with image",
  "is_thread": true,
  "thread_tweets": ["Second tweet", "Third tweet"],
  "media_urls": ["https://intro-image-url"],
  "thread_media": [["https://img-for-tweet-2"], []]
}
```
`thread_media` is an array of arrays. Each inner array contains media URLs for the corresponding tweet in `thread_tweets`. Use `[]` for tweets with no media.

### Post to an X Community
```
POST https://opentweet.io/api/v1/posts
Body: {
  "text": "Shared with the community!",
  "community_id": "1234567890",
  "share_with_followers": true
}
```

### Auto-retweet a post
```
POST https://opentweet.io/api/v1/posts
Body: {
  "text": "This will get a boost.",
  "scheduled_date": "2026-05-01T10:00:00Z",
  "auto_retweet_enabled": true,
  "auto_retweet_offset_minutes": 240
}
```
After the post publishes, OpenTweet automatically retweets it from the same account `auto_retweet_offset_minutes` later. Works on PUT too. Range: 1–10080 minutes (up to 7 days). Both fields can also be set via `PUT /api/v1/posts/{id}`.

### Auto-plug a post (reply when it goes viral)
```
POST https://opentweet.io/api/v1/posts
Body: {
  "text": "Hot take about AI agents.",
  "scheduled_date": "2026-05-01T10:00:00Z",
  "auto_plug_enabled": true,
  "auto_plug_threshold": 50,
  "auto_plug_text": "Enjoyed this? I share more every week → link.com/newsletter"
}
```
After the post publishes, OpenTweet checks its like count every 5 minutes. When `like_count >= auto_plug_threshold`, it automatically posts `auto_plug_text` as a reply to the original tweet — turning viral reach into subscribers or leads.

- `auto_plug_threshold` — likes needed to trigger (default: 20, no upper limit)
- `auto_plug_text` — the reply content, max 280 chars (required when `auto_plug_enabled: true`)
- Fires exactly once per post; `auto_plug_done: true` and `auto_plug_tweet_id` are set after sending
- Only checks posts published within the last 30 days
- Works on `PUT /api/v1/posts/{id}` too (set before or after publishing)

### Bulk create (up to 50 posts)
```
POST https://opentweet.io/api/v1/posts
Body: {
  "posts": [
    { "text": "Tweet 1", "scheduled_date": "2026-05-01T10:00:00Z" },
    { "text": "Tweet 2", "scheduled_date": "2026-05-01T14:00:00Z" }
  ]
}
```

### Schedule a post
```
POST https://opentweet.io/api/v1/posts/{id}/schedule
Body: { "scheduled_date": "2026-05-01T10:00:00Z" }
```
The date must be in the future. Use ISO 8601 format.

### Publish immediately
```
POST https://opentweet.io/api/v1/posts/{id}/publish
```
No body needed. Posts to X right now. Response includes `status: "posted"`, `x_post_id`, and `url` (the real X post URL).

### Batch schedule (up to 50 posts)
```
POST https://opentweet.io/api/v1/posts/batch-schedule
Body: {
  "schedules": [
    { "post_id": "id1", "scheduled_date": "2026-05-02T09:00:00Z" },
    { "post_id": "id2", "scheduled_date": "2026-05-03T14:00:00Z" }
  ],
  "community_id": "optional-community-id",
  "share_with_followers": true,
  "x_account_id": "optional-account-id"
}
```

### List posts
```
GET https://opentweet.io/api/v1/posts?status=scheduled&page=1&limit=20
```
Status options: `scheduled`, `posted`, `draft`, `failed`, `evergreen` (returns evergreen pool source posts).

### Get a post
```
GET https://opentweet.io/api/v1/posts/{id}
```

### Update a post
```
PUT https://opentweet.io/api/v1/posts/{id}
Body: {
  "text": "Updated text",
  "media_urls": ["https://..."],
  "scheduled_date": "2026-05-01T10:00:00Z",
  "auto_retweet_enabled": true,
  "auto_retweet_offset_minutes": 120
}
```
All fields optional. Cannot update already-published posts. Set `scheduled_date` to `null` to unschedule (convert back to draft).

### Delete a post
```
DELETE https://opentweet.io/api/v1/posts/{id}
```
Default: if the post was already published, OpenTweet also deletes it from X. To delete only locally and leave the X post live, append `?delete_from_x=false`. Response includes `x_deleted` and (if it failed) `x_delete_error`.

## Media Upload

### Upload an image or video
```
POST https://opentweet.io/api/v1/upload
Content-Type: multipart/form-data
Body: file=@your-image.png
```
Returns: `{ "url": "https://..." }`

Supported formats: JPG, PNG, GIF, WebP (max 5MB), MP4, MOV (max 20MB).

**Workflow**: Upload first, then use the returned URL in `media_urls` or `thread_media` when creating/updating posts.

## AI Media Generation

Generate images and videos with Grok Imagine (xAI) directly from a prompt. The generated file is permanently stored and the URL can be used in `media_urls` when creating a tweet. Requires `XAI_API_KEY` to be configured on the server.

### Generate an image
```
POST https://opentweet.io/api/v1/generate/image
Body: {
  "prompt": "A vibrant product launch announcement graphic",
  "aspect_ratio": "16:9",
  "resolution": "1k"
}
```
- `prompt` — required, max 1000 chars
- `aspect_ratio` — optional: `"1:1"` (default), `"16:9"`, `"9:16"`, `"4:3"`, `"3:4"`
- `resolution` — optional: `"1k"` (default) or `"2k"`

Returns: `{ "url": "https://...", "prompt": "...", "aspect_ratio": "16:9", "resolution": "1k" }`

Response is **synchronous** — the URL is ready to use immediately.

### Generate a video
```
POST https://opentweet.io/api/v1/generate/video
Body: {
  "prompt": "A product spinning on a pedestal with dramatic lighting",
  "aspect_ratio": "16:9",
  "resolution": "480p",
  "duration": 5
}
```
- `prompt` — required, max 1000 chars
- `aspect_ratio` — optional: `"16:9"` (default), `"9:16"`, `"1:1"`, `"4:3"`, `"3:4"`
- `resolution` — optional: `"480p"` (default) or `"720p"`
- `duration` — optional: `5` (default) to `10` seconds

Returns (202): `{ "job_id": "...", "status": "processing", "message": "..." }`

Video generation is **asynchronous** — poll the status endpoint until complete.

### Check video generation status
```
GET https://opentweet.io/api/v1/generate/video/{job_id}
```
Returns one of:
- `{ "job_id": "...", "status": "processing" }` — still generating, poll again in 10 seconds
- `{ "job_id": "...", "status": "completed", "url": "https://..." }` — ready, use the URL
- `{ "job_id": "...", "status": "failed", "error": "..." }` — generation failed

Typical generation time: 1–3 minutes. Poll every 10 seconds.

## Evergreen Queue

The evergreen queue keeps a pool of timeless tweets and republishes them on a schedule with cooldown gaps so the same post doesn't repeat too often. Source posts stay as templates; the scheduler clones them as regular posts at the configured times. Requires an active paid subscription (not available on trial). Pro: 10 pool / 2 per day. Advanced: 999 pool / 10 per day.

### Get queue settings + pool stats
```
GET https://opentweet.io/api/v1/evergreen/settings
```
Returns: `enabled`, `posts_per_day`, `posting_times` (`["09:00","17:00"]`), `default_cooldown_days`, plus pool counts and your plan limits.

### Update queue settings
```
PUT https://opentweet.io/api/v1/evergreen/settings
Body: {
  "enabled": true,
  "posts_per_day": 2,
  "posting_times": ["09:00", "17:00"],
  "default_cooldown_days": 14
}
```
All fields optional. `posting_times` must be `"HH:mm"` strings. `default_cooldown_days` is 1–90. `posts_per_day` capped to your plan's daily limit.

### List evergreen pool
```
GET https://opentweet.io/api/v1/evergreen/posts?page=1&limit=20&paused=false
```
Filter `paused=true` or `paused=false`. Each item includes `cooldown_days`, `last_posted_at`, `times_posted`, `paused`.

### Add to evergreen pool
Mode 1 — convert an existing post:
```
POST https://opentweet.io/api/v1/evergreen/posts
Body: { "post_id": "507f1f77bcf86cd799439011", "cooldown_days": 14 }
```
Mode 2 — create a new evergreen post directly:
```
POST https://opentweet.io/api/v1/evergreen/posts
Body: {
  "text": "Timeless tweet text",
  "category": "Tips",
  "cooldown_days": 21,
  "is_thread": false,
  "media_urls": ["https://..."]
}
```

### Get / update / remove an evergreen post
```
GET    https://opentweet.io/api/v1/evergreen/posts/{id}
PUT    https://opentweet.io/api/v1/evergreen/posts/{id}    # body: { "cooldown_days": 30, "paused": true }
DELETE https://opentweet.io/api/v1/evergreen/posts/{id}    # converts back to a draft (does not hard-delete)
```
GET also returns `recent_posts` — the last 5 published clones with their X URLs.

### Evergreen publish history
```
GET https://opentweet.io/api/v1/evergreen/history?page=1&limit=20&source_id=optional
```
Lists published clones. Filter by `source_id` to see the history of a single evergreen post.

## Inspiration (Search + Repurpose)

Search X for tweets and have AI rewrite them in the user's voice. Both endpoints require an active subscription. Search has a daily cap (Pro: 50/day, Advanced: 200/day, trial: 2/day). Repurpose counts against the AI generation daily quota.

### Search inspiration tweets
```
GET https://opentweet.io/api/v1/inspiration/search?q=AI%20agents&max_results=20&sort_order=relevancy&lang=en&has_media=true&min_likes=100&min_retweets=10
```
Required: `q`. Optional filters: `max_results`, `sort_order` (`relevancy` or `recency`), `lang`, `has_media`, `min_likes`, `min_retweets`. Response includes `data` (tweets), `meta.result_count`, and `usage` (searches_used / remaining / daily_limit).

### Repurpose a tweet with AI
```
POST https://opentweet.io/api/v1/inspiration/repurpose
Body: {
  "tweet_text": "Original tweet text to remix",
  "tweet_author": "@someone",
  "instructions": "Make it punchier and add a call to action",
  "tone": "casual",
  "save_as_draft": true
}
```
Returns `repurposed.text`, `category`, `key_topics`, plus `draft.id` when `save_as_draft` is true (default). Honors the user's voice profile and content pillars automatically. Optional `x_account_id` tags the saved draft.

## Analytics

### Account overview
```
GET https://opentweet.io/api/v1/analytics/overview
```
Returns posting stats (total posts, publishing rate, active days, avg posts/week, most active day/hour, threads, media posts), streaks (current, longest), trends (this week vs last, this month vs last, best month), category breakdown, and recent activity (daily counts for last 7 and 30 days).

### Tweet engagement metrics (Advanced plan only)
```
GET https://opentweet.io/api/v1/analytics/tweets?period=30
```
Returns per-tweet engagement: likes, retweets, replies, quotes, impressions, bookmarks, engagement rate. Also includes top/worst performers, content type stats, engagement timeline, and best hours/days. Period: 7-365 days or "all".

### Best posting times
```
GET https://opentweet.io/api/v1/analytics/best-times
```
Two analysis modes:
- **`engagement_weighted`** — uses real per-tweet engagement to score every hour×day cell. Returns `heatmap`, `confidence`, `top_windows`, `best_day`, `best_hour`, `worst_day`, `worst_hour`, `insights`. Only available after running an analysis.
- **`frequency_only`** — fallback based purely on when the user has posted. Returned when no engagement profile exists yet (needs ≥3 published posts).

Both modes also return legacy `hour_distribution`, `day_distribution`, `best_hours`, `best_days` keys for backward compatibility.

### Trigger fresh best-times analysis
```
POST https://opentweet.io/api/v1/analytics/best-times/analyze
Body: {}    # optional: { "x_account_id": "..." }
```
Pulls the user's recent published tweets from X, computes engagement-weighted windows, and stores the profile. Has a built-in cooldown — if a recent analysis is still fresh, returns `429` with `next_available_at`. Returns `success`, `profile` (status `ready` / `analyzing` / `insufficient_posts`).

## Common Workflows

**First: verify your connection works:**
1. `GET /api/v1/me` — check `authenticated` is true, `subscription.has_access` is true

**Post a tweet right now (one step):**
1. `GET /api/v1/me` — check `limits.can_post` is true
2. `POST /api/v1/posts` with `{ "text": "...", "publish_now": true }`

**Post a tweet with an image:**
1. `GET /api/v1/me` — check limits
2. Upload: `POST /api/v1/upload` with the image file — get back a URL
3. Create + publish: `POST /api/v1/posts` with `{ "text": "...", "media_urls": ["<url>"], "publish_now": true }`

**Schedule a tweet:**
1. `GET /api/v1/me` — check `limits.remaining_posts_today` > 0
2. `POST /api/v1/posts` with `{ "text": "...", "scheduled_date": "2026-05-01T10:00:00Z" }` — you MUST make this HTTP call
3. Read the response JSON — confirm `posts[0].status === "scheduled"` and show the user the `id` and `scheduled_date` from the response

**Schedule a tweet with auto-retweet boost:**
1. `GET /api/v1/me` — check `limits.remaining_posts_today` > 0
2. `POST /api/v1/posts` with text, `scheduled_date`, `auto_retweet_enabled: true`, `auto_retweet_offset_minutes: 240`
3. Show the user the `id` and `scheduled_date` from the response

**Schedule a tweet with auto-plug (monetise viral reach):**
1. `GET /api/v1/me` — check `limits.remaining_posts_today` > 0
2. `POST /api/v1/posts` with text, `scheduled_date`, `auto_plug_enabled: true`, `auto_plug_threshold: 50`, `auto_plug_text: "..."`
3. Show the user the `id` and confirm auto-plug is armed
4. Once live, the scheduler fires the reply automatically when likes reach the threshold — no further action needed

**Schedule a week of content:**
1. `GET /api/v1/me` — check remaining limit
2. Bulk create: `POST /api/v1/posts` with `"posts": [...]` array, each with a scheduled_date
3. Show the user the list of created post IDs and their scheduled dates from the response

**Post a tweet with an AI-generated image:**
1. `GET /api/v1/me` — check limits
2. `POST /api/v1/generate/image` with `{ "prompt": "...", "aspect_ratio": "16:9" }` — get back a URL immediately
3. `POST /api/v1/posts` with `{ "text": "...", "media_urls": ["<url from step 2>"], "publish_now": true }`

**Post a tweet with an AI-generated video:**
1. `GET /api/v1/me` — check limits
2. `POST /api/v1/generate/video` with `{ "prompt": "...", "aspect_ratio": "16:9", "duration": 5 }` — get back a `job_id`
3. Poll `GET /api/v1/generate/video/{job_id}` every 10 seconds until `status` is `"completed"` — get the `url`
4. `POST /api/v1/posts` with `{ "text": "...", "media_urls": ["<url from step 3>"], "publish_now": true }`

**Find inspiration and repurpose it:**
1. `GET /api/v1/inspiration/search?q=...&min_likes=500` — pick a tweet
2. `POST /api/v1/inspiration/repurpose` with `tweet_text`, `tweet_author`, `save_as_draft: true`
3. The saved draft's `id` can then be scheduled with `POST /api/v1/posts/{id}/schedule`

**Set up an evergreen queue from existing drafts:**
1. `PUT /api/v1/evergreen/settings` with `{ "enabled": true, "posts_per_day": 2, "posting_times": ["09:00","17:00"] }`
2. For each draft to recycle: `POST /api/v1/evergreen/posts` with `{ "post_id": "...", "cooldown_days": 14 }`
3. `GET /api/v1/evergreen/history` later to see what got published

**Tune posting times based on engagement:**
1. `POST /api/v1/analytics/best-times/analyze` — wait for `profile.status: "ready"` (poll if `analyzing`)
2. `GET /api/v1/analytics/best-times` — read `top_windows` and `best_hour` / `best_day`
3. Schedule new posts at the suggested times

## Important Rules
- ALWAYS call `GET /api/v1/me` before scheduling or publishing to check limits and connected accounts.
- For multi-account users, call `GET /api/v1/accounts` and pass `x_account_id` to target a specific account.
- CRITICAL: You MUST make the actual HTTP API call for every operation. Never skip the call and generate a response from memory or context.
- CRITICAL: Always parse and use the ACTUAL JSON response from the API. Never fabricate or assume response values.
- CRITICAL: A 4xx or 5xx HTTP status means the operation FAILED — never report success to the user on an error response.
- CRITICAL: After scheduling a post, always show the user the `id` field from the API response. If you cannot show a real 24-character MongoDB ObjectId from the response, the call was not made.
- Post IDs are always 24-character MongoDB ObjectIds (e.g. "507f1f77bcf86cd799439011"), never short strings.
- Every post response includes a `status` field: "draft", "scheduled", "posted", or "failed".
- Published posts include a `url` field with the real X post URL. Always use this URL — never construct your own.
- To verify a post was published, check: `status` is "posted" AND `url` is present.
- To verify a post was scheduled, check: `status` is "scheduled" AND `scheduled_date` is present in the response.
- Tweet max length: 280 characters (per tweet in a thread).
- Bulk limit: 50 posts per request (create or batch-schedule).
- Rate limit: 60 requests/minute, 1,000/day (Pro); 300/min, 10,000/day (Advanced).
- Dates must be ISO 8601 and in the future — past dates are rejected.
- Active subscription required to schedule, publish, use evergreen, search inspiration, or repurpose. Creating drafts is free.
- Including `scheduled_date` or `publish_now` in `POST /api/v1/posts` requires a subscription.
- Upload media before creating posts — use the returned URL in `media_urls` or `thread_media`.
- Media limits: 5MB for images (JPG, PNG, GIF, WebP), 20MB for videos (MP4, MOV).
- URL-containing posts have a separate, plan-based daily cap. A 429 with a `urlLimit` payload means the post was saved as a draft instead of published.
- Tweet engagement analytics require the Advanced plan (returns 403 on Pro).
- Evergreen queue is not available during trial.
- `auto_retweet_offset_minutes` must be 1–10080 (up to 7 days) when `auto_retweet_enabled` is true.
- 403 = no subscription / X not connected, 429 = rate limit, daily post limit, URL post cap, or evergreen pool full.
- Check response status codes: 201=created, 200=success, 4xx=client error, 5xx=server error.

## Safety Guardrails

**Publishing is irreversible** — once a tweet is posted to X it cannot be undone via the API (DELETE removes it locally and from X, but reposts are not the same tweet).

### Confirm before publishing
- Before calling `/publish` or using `publish_now: true`, always tell the user which post(s) you are about to publish and ask for confirmation.
- Show the tweet text (truncated if long) and the post ID so the user can verify.

### Scheduled posts ≠ ready to publish
- If a post has a `scheduled_date` in the future, it is meant to be published at that time by the scheduler — not right now.
- NEVER call `/publish` on a post that has a future `scheduled_date` unless the user explicitly asks you to publish it immediately.
- When the user asks to "publish" posts, clarify whether they want to publish NOW or schedule for later. Default to scheduling if dates are provided.

### Evergreen sources are not regular drafts
- A post with `isEvergreen: true` is a recurring template. The scheduler publishes clones, not the source itself.
- NEVER call `/publish` directly on an evergreen source post (the API will reject it). Add it to the queue with `POST /api/v1/evergreen/posts` and let the scheduler run.

### Batch operations — go slow
- When creating or scheduling more than 5 posts, summarize the batch (count, date range, first/last tweet previews) and ask the user to confirm before proceeding.
- Never bulk-create AND immediately publish in one go. Create as drafts or scheduled posts first, let the user review, then publish only on confirmation.
- When using batch-schedule, show the user the list of dates before sending the request.

### Don't loop publish calls
- Never loop through a list of posts calling `/publish` on each one without explicit user approval for the full list.
- If the user asks to "publish all my drafts" or similar, list them first and get confirmation.

### AI-generated content needs a review pass
- Before saving repurposed tweets as auto-scheduled posts, show the user the AI output and let them edit. The repurpose endpoint already saves to drafts by default — keep `save_as_draft: true` unless the user has reviewed.

## Full API docs
For complete documentation: https://opentweet.io/api/v1/docs
