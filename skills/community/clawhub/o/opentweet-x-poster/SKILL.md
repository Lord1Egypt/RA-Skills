---
name: x-poster
description: Post to X (Twitter), Bluesky and LinkedIn using the OpenTweet API. Create posts, cross-post the same content to all three networks in one call, schedule posts, publish threads, write and schedule long-form X Articles from markdown, upload media, run an evergreen queue, search inspiration tweets, repurpose them with AI, run AI-qualified DM outreach campaigns with human-approved sending, and read engagement-weighted analytics, all autonomously.
version: 1.7.0
homepage: https://opentweet.io/features/openclaw-twitter-posting
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["OPENTWEET_API_KEY"]},"primaryEnv":"OPENTWEET_API_KEY"}}
---

# OpenTweet X Poster

You can post to X (Twitter), Bluesky and LinkedIn using the OpenTweet REST API. All requests go to `https://opentweet.io` with the user's API key.

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

## Cross-Posting (X, Bluesky and LinkedIn)

OpenTweet can publish the same content to X, Bluesky and LinkedIn. Every post-creating endpoint takes an optional `platforms` array, and every post response carries a per-network `results` array.

### Check cross-posting state first
```
GET https://opentweet.io/api/v1/cross-posting
```
Returns which networks are connected, which can actually publish right now, whether auto cross-post is on, and where a post that omits `platforms` would go:
```json
{
  "auto_cross_post": false,
  "default_targets": ["x"],
  "deliverable_targets": ["x"],
  "platforms": [
    { "platform": "x", "connected": true, "usable": true,
      "accounts": [{ "account_id": "...", "handle": "handle", "display_name": "Name", "is_primary": true }],
      "limits": { "max_text_length": 280, "text_unit": "weighted", "max_images": 4 } },
    { "platform": "bluesky", "connected": true, "usable": false, "needs_reconnect": true,
      "accounts": [...], "limits": {...} },
    { "platform": "linkedin", "connected": true, "usable": true,
      "accounts": [...],
      "limits": { "max_text_length": 3000, "text_unit": "codeunit", "max_images": 20, "max_videos": 0 } }
  ]
}
```
Read these two together before posting whenever the user has not said which network they mean:
- `default_targets` is what a post that omits `platforms` is ATTEMPTED on.
- `deliverable_targets` is the subset that will actually LAND, filtered to networks with a usable account.

Anything in `default_targets` but not in `deliverable_targets` is going to fail. That is deliberate: an unusable network stays in the attempt so the failure is recorded in `results`, instead of being quietly dropped and letting the post roll up as a clean success nobody questions. Reading only `default_targets` would have you tell the user their post goes to X and Bluesky while the Bluesky authorisation is dead. Say which networks will land and which are expected to fail.

`connected` and `usable` are DIFFERENT questions and you must not conflate them:
- `connected` only means an account row exists.
- `usable` means OpenTweet believes it can publish there right now.

A user whose Bluesky authorisation died is `connected: true, usable: false, needs_reconnect: true`. Telling them "Bluesky is connected" would be misleading. Say it needs reconnecting at https://opentweet.io/settings, and do not promise a publish that is going to fail. Targeting a network with `usable: false` comes back as a `failed` or `skipped` entry in `results`. The same applies to a LinkedIn account whose 60-day sign-in has lapsed.

### Targeting networks explicitly
```
POST https://opentweet.io/api/v1/posts
Body: { "text": "Shipped it.", "publish_now": true, "platforms": ["x", "bluesky", "linkedin"] }
```
`platforms` accepts any non-empty subset of `"x"`, `"bluesky"` and `"linkedin"`, so `["bluesky"]` posts to Bluesky only and `["x", "linkedin"]` skips Bluesky. Unknown ids are dropped. An explicit list is ALWAYS honoured exactly, whatever the auto cross-post setting says.

For bulk creates, `platforms` works per post inside the `posts` array and also at the top level as a default for the whole batch.

### What omitting `platforms` means
Leaving `platforms` out is NOT the same as sending `["x"]`. An unspecified post follows the user's server-side auto cross-post setting:
- Auto cross-post ON: the post goes to EVERY connected network.
- Auto cross-post OFF: the post goes to the single default network.

If the user asked for X only, send `"platforms": ["x"]`. Do not rely on the omission, because on an account with auto cross-post on that also posts to Bluesky and LinkedIn.

### Reading per-network results
Post responses include `results`, one entry per network the post was sent to:
```json
"results": [
  { "platform": "x", "status": "published", "url": "https://x.com/handle/status/123" },
  { "platform": "bluesky", "status": "skipped", "skip_reason": "No Bluesky account connected" },
  { "platform": "linkedin", "status": "published", "post_id": "urn:li:share:7300000000000000000",
    "url": "https://www.linkedin.com/feed/update/urn:li:share:7300000000000000000/" }
]
```
`status` is `"published"`, `"failed"`, or `"skipped"`.
- `skipped` is NOT a failure. The post went out, one target was dropped, and `skip_reason` says why. Read `skip_reason` under both spellings: `skip_reason` and `skipReason`.
- `failed` carries `error` with the network's rejection reason.
- Report the outcome per network. A post that published on X and failed on Bluesky is a partial success, never a clean success. Give the user the `url` from each published entry.

Character limits differ: X allows 280 (up to 25,000 with X Premium), Bluesky caps at 300 graphemes, LinkedIn allows 3,000 characters (an emoji counts as 2). Text that fits X can still be rejected by Bluesky, which comes back as a `failed` entry for Bluesky while X publishes fine.

### LinkedIn
- Personal profile only. Company Pages are not supported.
- 3,000 characters, counted in code units, so an emoji counts as 2.
- A thread goes to LinkedIn as ONE post, with the parts joined by a blank line.
- Video is not supported. A post with video comes back as a `skipped` LinkedIn entry with a `skip_reason`. Up to 20 images work.
- Hashtags and mentions publish as plain text.
- No LinkedIn analytics. Auto-retweet and communities are X only.
- In `results`, LinkedIn's `post_id` is a URN like `urn:li:share:7300000000000000000` and `url` is `https://www.linkedin.com/feed/update/<urn>/`.
- The account is connected in the web dashboard (Settings > Accounts > Connect LinkedIn), not through the API. The sign-in lasts 60 days, then needs a one-click reconnect; until then `GET /api/v1/cross-posting` shows LinkedIn as `usable: false, needs_reconnect: true`.

## Post Management

### Create a tweet
```
POST https://opentweet.io/api/v1/posts
Body: { "text": "Your tweet text" }
```
Optionally add `"scheduled_date": "2026-05-01T10:00:00Z"` to schedule it (requires active subscription, date must be in the future). Add `"platforms": ["x", "bluesky", "linkedin"]` (or any subset) to pin which networks it goes to. See Cross-Posting above for what happens when you leave `platforms` out.

### Create and publish immediately (one step)
```
POST https://opentweet.io/api/v1/posts
Body: { "text": "Hello from the API!", "publish_now": true }
```
Creates the post AND publishes in one request. Cannot combine with `scheduled_date` or bulk posts. Response includes `status: "posted"`, `x_post_id`, and `url` (the real X post URL) on success, plus a `results` array with the outcome for every network it went to. Add `"platforms": ["x", "bluesky", "linkedin"]` to publish to all three at once.

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
No body needed. Publishes right now to the networks the post was created with, or to whatever auto cross-post resolves to if it was created without `platforms`. Response includes `status: "posted"`, `x_post_id`, `url` (the real X post URL), and a `results` array with the per-network outcome.

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

## X Articles (Long-Form Posts)

Write and publish long-form X Articles from markdown. OpenTweet converts markdown to X's rich-text article format at publish time: `#`/`##`/`###` headings, **bold**, *italic*, ~~strikethrough~~, links, bullet/numbered lists, `>` quotes, inline images via `![caption](url)` (uploaded to X automatically), a cover image, and embedded posts (an x.com status URL on its own line). Fenced code blocks are preserved as plain text.

Requires an active paid subscription (not trial). The connected X account must have X Premium (any tier since January 2026) to publish Articles — if not, publishing fails and `failed_reason` carries X's exact error.

Article statuses: `draft`, `scheduled`, `publishing`, `published`, `failed`.

### Create an article (draft, scheduled, or publish now)
```
POST https://opentweet.io/api/v1/articles
Body: {
  "title": "How We Grew to 10k Users",
  "content_markdown": "# The short version\n\nWe shipped **every week**...",
  "cover_image_url": "https://url-from-upload-endpoint",
  "scheduled_date": "2026-07-15T14:00:00Z"
}
```
- `title` and `content_markdown` are required.
- `scheduled_date` schedules it; `"publish_now": true` publishes immediately (mutually exclusive with `scheduled_date`).
- Omit both to save a draft.
- Optional `x_account_id` for multi-account users.

Returns 201 with the article object. A published article includes `article_url` (the live X link) and `x_post_id`.

### List articles
```
GET https://opentweet.io/api/v1/articles?status=scheduled&page=1&limit=20
```
Status filter options: `draft`, `scheduled`, `publishing`, `published`, `failed`.

### Get / update / delete an article
```
GET    https://opentweet.io/api/v1/articles/{id}
PUT    https://opentweet.io/api/v1/articles/{id}    # body: any of title, content_markdown, cover_image_url, scheduled_date, x_account_id
DELETE https://opentweet.io/api/v1/articles/{id}
```
Published articles cannot be edited. Set `scheduled_date` to `null` to unschedule back to draft. Updating a failed article resets it to draft/scheduled.

### Publish an article immediately
```
POST https://opentweet.io/api/v1/articles/{id}/publish
```
No body needed. Returns the article with `status: "published"` and `article_url`, or 502 with `code: "publish_failed"` and X's error in `failed_reason`.

## DM Campaigns (AI Lead Outreach)

Run outreach campaigns that find qualified X profiles, qualify them with AI, draft a personalized DM for each, and send only after a human approves. This is not a mass messenger: sending is human-in-the-loop, drip-scheduled, rate-limited, and honors opt-outs. Available on the Advanced and Agency plans only (403 on Pro). Requires a paid API key (not the free taste key).

How a campaign flows: you create it with an ideal-customer description and one or more lead sources, discovery finds and AI-qualifies candidates into leads, you review and approve the drafted messages, then the sender drips approved DMs from the connected X account within the campaign's caps. Replies are tracked and tagged, and opt-outs are auto-suppressed. Actual sending is gated server-side and paced, so approving a lead queues it, it does not fire instantly.

### Create a campaign
```
POST https://opentweet.io/api/v1/dm-campaigns
Body: {
  "name": "Shopify founders Q3",
  "x_account_id": "account_id_here",
  "sources": [
    { "type": "search", "value": "shopify analytics", "max_candidates": 500 },
    { "type": "followers_of", "value": "somecompetitor", "max_candidates": 500 },
    { "type": "tweet_engagers", "value": "https://x.com/user/status/123", "max_candidates": 300 },
    { "type": "own_followers", "value": "", "max_candidates": 500 }
  ],
  "icp_prompt": "Shopify store owners or ecommerce founders, 200-20k followers, English, active in the last 2 weeks, complaining about ad costs or analytics. Not agencies.",
  "score_threshold": 60,
  "message_brief": { "offer": "a $29/mo analytics tool for Shopify", "tone": "casual", "cta": "worth a look?", "follow_up_enabled": false },
  "limits": { "dms_per_day": 25, "active_hours_start": 9, "active_hours_end": 18, "timezone": "America/New_York" },
  "accept_policy": true
}
```
`accept_policy` must be `true` (it records acceptance of X's acceptable-use terms; the connected account bears the outreach risk). Returns `{ "campaign": {...} }`. Source types: `search` (keyword query), `followers_of` (a handle), `tweet_engagers` (a tweet URL), `own_followers`.

### List campaigns
```
GET https://opentweet.io/api/v1/dm-campaigns
```
Returns `{ "campaigns": [...] }`, each with a `stats` funnel (found, qualified, approved, sent, replied).

### Get a campaign (with stats)
```
GET https://opentweet.io/api/v1/dm-campaigns/{id}
```

### Start discovery
```
POST https://opentweet.io/api/v1/dm-campaigns/{id}/discover
```
Sets the campaign to `discovering` and returns immediately. Discovery and AI qualification run in the background, then the campaign moves to `reviewing` with leads ready. Poll the campaign until its status is `reviewing`.

### List leads (the review queue)
```
GET https://opentweet.io/api/v1/dm-campaigns/{id}/leads?state=qualified&page=1
```
State filter includes `qualified` (awaiting approval), `approved`, `sent`, `replied`, `skipped`. Each lead has a `score`, a `reason`, an `angle_hook`, and a drafted `final_message`.

### Approve or skip a lead
```
PATCH https://opentweet.io/api/v1/dm-campaigns/{id}/leads/{leadId}
Body: { "action": "approve", "final_message": "optional edited message" }
```
`action` is `approve` (queues the drafted or provided message for drip sending), `skip`, or `edit` (change the draft without approving). Approving does NOT send immediately; the sender paces it within the campaign's daily cap and active hours.

### Read replies (inbox)
```
GET https://opentweet.io/api/v1/dm-campaigns/{id}/inbox
```
Returns `{ "conversations": [{ "lead": {...}, "reply_tag": "interested|question|not_interested|opt_out", "events": [...] }] }`. Opt-outs are auto-added to the do-not-contact list.

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

**Write and schedule a long-form X Article:**
1. `GET /api/v1/me` — check `subscription.has_access` is true (articles need a paid plan)
2. Optional cover: `POST /api/v1/upload` with an image — get back a URL
3. `POST /api/v1/articles` with `{ "title": "...", "content_markdown": "# ...", "cover_image_url": "<url>", "scheduled_date": "2026-07-15T14:00:00Z" }`
4. Confirm the response has `status: "scheduled"` and show the user the article `id`
5. After publish time, `GET /api/v1/articles/{id}` — `article_url` is the live X link

**Run a DM outreach campaign (human-approved):**
1. `GET /api/v1/me` — confirm the plan is Advanced or Agency (DM Campaigns return 403 otherwise)
2. `POST /api/v1/dm-campaigns` with the ICP, sources, message brief, limits, and `accept_policy: true`
3. `POST /api/v1/dm-campaigns/{id}/discover`, then poll `GET /api/v1/dm-campaigns/{id}` until status is `reviewing`
4. `GET /api/v1/dm-campaigns/{id}/leads?state=qualified` — show the user the qualified leads and their drafted messages
5. Only after the user approves specific leads: `PATCH .../leads/{leadId}` with `action: approve`. Never auto-approve every lead.
6. `GET /api/v1/dm-campaigns/{id}/inbox` later to read replies

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
- Omitting `platforms` does NOT mean "X only". It hands targeting to the user's auto cross-post setting. Send `"platforms": ["x"]` when the user asked for X only.
- An explicit `platforms` list is always honoured exactly, even when auto cross-post is on.
- Read the `results` array before reporting an outcome. A `skipped` entry is not a failure, a `failed` entry is, and a post can be published on one network and failed on another.
- Call `GET /api/v1/cross-posting` when you need to know where an unspecified post will land, or when the user asks what they are connected to. `default_targets` is what gets attempted, `deliverable_targets` is what actually lands, and the difference between them is a set of expected failures you should mention up front.
- On `GET /api/v1/cross-posting`, `connected` and `usable` are different. Never report a `connected: true, usable: false` network as working; it needs reconnecting first.
- Bluesky caps posts at 300 characters, below X's 280-plus-Premium ceiling on longer text. Check the shortest limit among the targeted networks before sending.
- LinkedIn allows 3,000 characters (an emoji counts as 2), takes a thread as ONE post, skips posts with video, and has no analytics. See the LinkedIn subsection under Cross-Posting.
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
- X Articles require a paid plan (not trial) AND X Premium (any tier) on the publishing X account. A 502 with `code: "publish_failed"` carries X's exact rejection reason.
- Article content is markdown. Do not send DraftJS or HTML — OpenTweet handles the rich-text conversion.
- `auto_retweet_offset_minutes` must be 1–10080 (up to 7 days) when `auto_retweet_enabled` is true.
- 403 = no subscription / X not connected, 429 = rate limit, daily post limit, URL post cap, or evergreen pool full.
- Check response status codes: 201=created, 200=success, 4xx=client error, 5xx=server error.

## Safety Guardrails

**Publishing is irreversible** — once a tweet is posted to X it cannot be undone via the API (DELETE removes it locally and from X, but reposts are not the same tweet).

### Confirm before publishing
- Before calling `/publish` or using `publish_now: true`, always tell the user which post(s) you are about to publish and ask for confirmation.
- Show the tweet text (truncated if long) and the post ID so the user can verify.
- The same applies to articles: before `POST /api/v1/articles/{id}/publish` or `publish_now: true` on an article, show the user the title and ask for confirmation. A published article cannot be edited.

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

### DM campaigns are opt-in outreach, not a blaster
- Never approve DM leads in bulk without the user reviewing them. Show the qualified leads and their drafted messages, and only approve the specific ones the user picks.
- X prohibits unsolicited automated bulk DMs. Keep the daily caps conservative, never try to bypass the pacing, and respect that approving a lead queues it for a drip send rather than firing immediately.
- Opt-outs and negative replies are auto-suppressed. Do not re-add or re-contact a suppressed profile.

### AI-generated content needs a review pass
- Before saving repurposed tweets as auto-scheduled posts, show the user the AI output and let them edit. The repurpose endpoint already saves to drafts by default — keep `save_as_draft: true` unless the user has reviewed.

## Full API docs
For complete documentation: https://opentweet.io/api/v1/docs
