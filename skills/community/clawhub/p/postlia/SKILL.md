---
name: postlia
description: Publish and schedule social media posts across LinkedIn, Bluesky, Instagram, TikTok, Pinterest, YouTube Shorts and Mastodon, then verify delivery with per-post receipts. Uses the Postlia REST API.
homepage: https://postlia.com
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["POSTLIA_API_KEY"] },
        "primaryEnv": "POSTLIA_API_KEY",
      },
  }
---

# Postlia: social publishing for agents

Postlia posts to 7 social networks through one API and gives you a delivery
receipt for every post, so you can verify a post actually went live instead
of assuming. A free account is enough: create an API key at
https://postlia.com (Settings -> Developers) and set it as
`POSTLIA_API_KEY`.

Base URL: `https://postlia.com/api/v1`
Auth header on every request: `Authorization: Bearer $POSTLIA_API_KEY`

## When to use this skill

Use it whenever the user asks to post, schedule, or queue social content,
check whether a post went out, look at posting history or analytics, or
manage drafts.

## Core workflows

### Post now

```
POST /posts
{"content": "text of the post", "platforms": ["linkedin", "bluesky"]}
```

Publishes within about 5 minutes. The response includes the post id. Keep
that id: it is how you verify delivery later.

### Schedule or queue

Add `"scheduledAt": "2026-08-12T09:00:00Z"` (ISO, future) to schedule for
an exact time, or `"queue": true` to drop it into the next open slot of the
user's posting schedule. Never send both.

### Post with media (Instagram, TikTok, Pinterest, YouTube Shorts)

Media platforms need an image or video. Two steps:

1. Import the file into Postlia storage (public https URL, served directly):

```
POST /media
{"url": "https://example.com/photo.jpg"}
```

Returns `{"mediaUrl": "...", "mediaType": "image"}`. Allowed: PNG, JPEG,
WebP, GIF, MP4, WebM, MOV, max 25 MB.

2. Create the post with that storage URL:

```
POST /posts
{"content": "caption", "platforms": ["instagram"],
 "mediaUrl": "<mediaUrl from step 1>", "mediaType": "image"}
```

Notes: create_post only accepts media URLs from Postlia storage, so always
run step 1 first. TikTok also requires `tiktokOptions`, Pinterest
`pinterestOptions` (board), YouTube `youtubeOptions` (title); if one is
missing the API answers 400 with the exact requirement. Image carousels:
send `mediaUrls` (1-4 storage URLs) instead of `mediaUrl`.

### Verify delivery (do this instead of assuming)

The MCP server exposes `get_post_receipt`; over REST, list recent posts:

```
GET /posts
```

Each post carries an honest status (published, partial, failed) and the
platform's real error text when something failed. Report failures to the
user with the platform's own error message; do not invent reasons.

### Other calls

- `GET /me` - account sanity check
- `GET /accounts` - connected social accounts (post only to platforms that
  appear here)
- `DELETE /posts/:id` - cancel a scheduled post

## MCP alternative

If the runtime supports MCP, prefer connecting the Postlia MCP server (15
tools including receipts, quota, drafts, queue info and analytics):

```
claude mcp add postlia --transport http https://postlia.com/api/mcp --header "Authorization: Bearer $POSTLIA_API_KEY"
```

## Rules

- Check `GET /accounts` before posting; if a platform is not connected,
  tell the user to connect it at https://postlia.com/settings instead of
  guessing.
- Media platforms (Instagram, TikTok, Pinterest, YouTube Shorts) require
  media: always run the POST /media import step first and pass the returned
  storage URL. Arbitrary external URLs are rejected by design.
- Respect the quota errors (HTTP 402): relay the message; a free account
  has a small free allowance and paid plans raise it.
- One piece of content counts as one post no matter how many platforms it
  targets. Drafts cost no quota.
