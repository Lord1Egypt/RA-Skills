---
name: postproxy
description: Create, schedule, update, and manage social media posts, comments, and direct messages across Facebook, Instagram, TikTok, LinkedIn, YouTube, X/Twitter, Threads, Pinterest, Bluesky, Telegram, and Google Business using the Postproxy API. Use when user wants to publish posts, schedule content, create drafts, upload media, manage posting queues, update existing posts, delete posts from social platforms, manage post comments, send or read direct messages (DMs/chats), reply to Google Business reviews, configure webhooks, or retrieve profile/follower stats.
version: 2.0.1
allowed-tools: Bash, Read
metadata:
  openclaw:
    emoji: 📣
    homepage: https://postproxy.dev
    primaryEnv: POSTPROXY_API_KEY
    requires:
      env:
        - POSTPROXY_API_KEY
      bins:
        - curl
    envVars:
      - name: POSTPROXY_API_KEY
        required: true
        description: Postproxy API key — create one at https://app.postproxy.dev/api_keys
---

# Postproxy API Skill

Call the [Postproxy](https://postproxy.dev/) API to manage social media posts across multiple platforms (Facebook, Instagram, TikTok, LinkedIn, YouTube, X/Twitter, Threads, Pinterest, Bluesky, Telegram, Google Business).

## Setup

API key must be set in environment variable `POSTPROXY_API_KEY`.
Get your API key at: https://app.postproxy.dev/api_keys

**Base URL:** `https://api.postproxy.dev`

All requests require a Bearer token:
```bash
-H "Authorization: Bearer $POSTPROXY_API_KEY"
```

## Quick Start

```bash
# 1. List connected profiles
curl -X GET "https://api.postproxy.dev/api/profiles" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"

# 2. Publish a post to multiple platforms
curl -X POST "https://api.postproxy.dev/api/posts" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "post": { "body": "Hello from Postproxy!" },
    "profiles": ["twitter", "linkedin", "threads"],
    "media": ["https://example.com/image.jpg"]
  }'

# 3. Schedule for later — add scheduled_at to the post object
curl -X POST "https://api.postproxy.dev/api/posts" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "post": { "body": "Scheduled post", "scheduled_at": "2026-06-16T09:00:00Z" },
    "profiles": ["twitter"]
  }'
```

`profiles` accepts network names (`facebook`, `instagram`, `tiktok`, `linkedin`, `youtube`, `twitter`, `threads`, `pinterest`, `bluesky`, `telegram`, `google_business`) or profile IDs.

## Rule Files

Read the rule file matching the task before calling the API — they contain required parameters, platform quirks, and error semantics:

- [rules/profiles.md](rules/profiles.md) — List profiles, profile stats (followers/engagement, latest + timeseries), placements (Facebook pages, LinkedIn orgs, Pinterest boards, Telegram channels, Google Business locations)
- [rules/posts.md](rules/posts.md) — Create posts (JSON or file upload), drafts, scheduling, threads (tweet chains), update, delete (DB and/or platform)
- [rules/queues.md](rules/queues.md) — Posting queues: timeslots, priorities, jitter, pausing, adding posts to queues
- [rules/analytics.md](rules/analytics.md) — Post stats snapshots and per-platform metric fields
- [rules/comments.md](rules/comments.md) — Post comments (list/reply/delete/hide/like), private replies, Google Business reviews (Profile Comments API)
- [rules/messages.md](rules/messages.md) — Direct messages: chats, send/read messages, reactions, edits, the Meta 24h window
- [rules/platforms.md](rules/platforms.md) — Platform-specific parameters: Instagram, TikTok, YouTube, Bluesky, Telegram, Google Business (events/offers/CTAs), character and media limits
- [rules/webhooks.md](rules/webhooks.md) — Webhook endpoints, all event types, HMAC signature verification, retries, delivery logs
- [rules/errors.md](rules/errors.md) — Error response formats, common status codes, async failure statuses
- [rules/sdks.md](rules/sdks.md) — Official SDKs for 7 languages

## Safety Rules

This skill publishes to, modifies, and deletes content on the user's real social media accounts, and can read/send private messages. Before any outward-facing or irreversible action, summarize exactly what will happen and get explicit user confirmation:

- **Publishing** (create post without `draft`, publish draft, comment, reply): content goes live publicly and immediately. State the exact text, media, and target profiles/placements first. Prefer creating a draft when intent is ambiguous.
- **Deleting**: deleting a post from the DB only (`DELETE /api/posts/{id}`) leaves it live on the platforms; `delete_on_platform=true` or `/delete_on_platform` removes it from the social networks **irreversibly**. Never delete on platform without the user explicitly confirming the post and scope.
- **Direct messages and private replies**: these are private communications with real people. Only read or send them when the user explicitly asks; don't quote DM contents into other posts, tools, or external services. Private replies bypass Meta's 24h window — confirm before initiating contact.
- **Placements**: when posting to Facebook without an explicit placement, the post goes to a **random connected page**; LinkedIn defaults to the personal profile. Always resolve and confirm the placement for placement networks.
- **Webhook secrets**: the `secret` returned when creating a webhook is a credential — never print it in output, log it, or commit it. Webhook payloads can contain private content (DMs, comments) and are sent to the configured URL — only register HTTPS endpoints the user controls and trusts.

## Key Behaviors

- **Async writes**: comments, DMs, and platform deletions return `pending` and transition to `published`/`deleted` (or `failed`) — poll the resource or subscribe to webhooks.
- **Placements**: Facebook, LinkedIn, Pinterest, Telegram, and Google Business post to a placement (page/org/board/channel/location). Telegram (`chat_id`), Pinterest, and Google Business (`location_id`) **require** one — see [rules/profiles.md](rules/profiles.md).
- **Queues vs schedule**: pass `scheduled_at` *or* `queue_id`, never both.
- **Editing**: only drafts and scheduled posts more than 5 minutes before publish time can be updated.

## User Request

$ARGUMENTS
