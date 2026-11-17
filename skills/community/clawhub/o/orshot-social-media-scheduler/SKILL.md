---
name: orshot-social-media-scheduler
description: Social media scheduler and social media automation for AI agents. Schedule posts, post to Instagram, post to LinkedIn, post to X (Twitter), TikTok, Facebook, Pinterest, Threads, Bluesky, Reddit, YouTube, Telegram, Snapchat and Google Business with Orshot, with the image, carousel or video rendered from a template in the same call. Use to schedule a social post, run a weekly content calendar, cross-post to every platform, queue drafts for review, read post analytics and follower growth, find the best time to post, or build an agent that posts and learns. Everything runs over the hosted Orshot MCP server (OAuth, no key); REST with an API key for headless jobs.
homepage: https://orshot.com/agents/openclaw
license: MIT-0
metadata:
  author: Orshot
  version: "1.0.0"
  openclaw:
    emoji: "📣"
    homepage: https://orshot.com/agents/openclaw
    primaryEnv: ORSHOT_API_KEY
    requires:
      env: []
      bins: []
    envVars:
      - name: ORSHOT_API_KEY
        required: false
        description: Orshot API key from Workspace Settings > API Keys. Only for REST. Not needed over the hosted MCP server with OAuth.
---

# Orshot Social Media Scheduler: render, post, schedule, learn

Orshot renders an image, carousel or video from a template and posts it to 13+ platforms in one request. It also holds drafts, schedules, edits and reports analytics, so an agent can run a whole content calendar without a second tool. Posts can also attach any public media URL, so it works with images made elsewhere.

Platforms: X (Twitter), Instagram, Facebook, LinkedIn (profile and page), TikTok, YouTube, Pinterest, Reddit, Bluesky, Threads, Telegram, Snapchat, Google Business.

## Step 1: connect the Orshot MCP server

Nothing works before this. The MCP route has no key to paste, shows every post as a visual card, and is the one to use from an agent.

```bash
openclaw mcp add orshot --url https://mcp.orshot.com/mcp --transport streamable-http --auth oauth
openclaw mcp login orshot
```

Claude Code: `claude mcp add --transport http orshot https://mcp.orshot.com/mcp`. Other MCP clients take the same URL.

Headless jobs only (cron, n8n, a server script): `export ORSHOT_API_KEY=...` and call REST with `Authorization: Bearer $ORSHOT_API_KEY`.

## Step 2: check the connected accounts

```
orshot_list_social_accounts            # MCP
GET /v1/social/accounts?include_health=true   # REST
# [{ "id": 1, "platform": "linkedin", "account_name": "Acme", "account_username": "acme", "health": { "status": "ok" } }]
```

A list with accounts means you can post. Note the numeric `id` of each one and any `health` flag that says reconnect.

**An empty list means a human still has to connect accounts.** The API cannot connect one. Send the user to their Orshot dashboard: Workspace > Socials > Accounts (https://orshot.com/dashboard, then the Socials section of the workspace), where each platform connects with its own OAuth login. Social publishing is an add-on on paid plans, $12 per connected account per month, with no extra credits per post; the free plan cannot connect accounts. Plans and the add-on are on https://orshot.com/pricing. Say this once, plainly, and wait for the user to come back; the next `orshot_list_social_accounts` call will show the new account.

## Core workflow

1. **Connect** and list accounts (above).
2. **Decide the media.** Render from a template (`templateId` + `modifications`) or use an existing `media_url`.
3. **Draft first.** Create the post with `status: "draft"` unless the user clearly said to post now.
4. **Show the user** the preview, caption, accounts and time. Over MCP `orshot_get_social_post` renders a visual card.
5. **Edit** what they change (`orshot_update_social_post`), then **publish** (`orshot_publish_social_draft`) or **schedule** (`status: "scheduled"` + `scheduled_for`).
6. **Check status** after an async platform (Instagram, TikTok) finishes: `processing` becomes `published` or `failed`.
7. **Read analytics** a day later, and the best-time insights before the next schedule.

## MCP tool map

| Job | Tool |
| --- | --- |
| list accounts | `orshot_list_social_accounts` |
| render + post in one call | `orshot_render_template` with `publish` |
| post a media URL | `orshot_publish_social_post` |
| list / read posts | `orshot_list_social_posts`, `orshot_get_social_post` (visual card) |
| edit / send / discard | `orshot_update_social_post`, `orshot_publish_social_draft`, `orshot_discard_social_post` |
| analytics | `orshot_get_social_analytics`, `orshot_get_social_analytics_daily`, `orshot_get_social_followers`, `orshot_get_social_post_analytics` |
| best time to post | `orshot_get_best_time_to_post` |

The MCP server defaults to `status: "draft"` short of an explicit go-ahead. Keep it that way.

## Essential calls

### Render and post (or draft, or schedule) in one call

Over MCP this is `orshot_render_template` with the same `publish` object.

```js
await fetch("https://api.orshot.com/v1/studio/render", {
  method: "POST",
  headers: { "Content-Type": "application/json", Authorization: `Bearer ${apiKey}` },
  body: JSON.stringify({
    templateId: 123,
    modifications: { headline: "Ship day", stat: "2,000 renders" },
    response: { type: "url", format: "png" },
    publish: {
      accounts: [1, 3],
      content: "Caption up to 5000 chars",
      status: "scheduled",               // published | draft | scheduled
      scheduled_for: "2026-11-01T14:00:00Z",
      timezone: "America/New_York",
      platformOptions: {
        "3": { firstComment: "https://orshot.com", disableLinkPreview: true }, // LinkedIn
      },
    },
  }),
});
```

Multi-page templates publish as a carousel on platforms that support it. The response has `data.content` (the render) and `publish[]` with one entry per account.

### Post media you already have

`orshot_publish_social_post`, or:

```bash
curl -s -X POST https://api.orshot.com/v1/social/publish \
  -H "Authorization: Bearer $ORSHOT_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "accounts": [2],
    "content": "Six things nobody tells you",
    "media_urls": ["https://.../1.png", "https://.../2.png", "https://.../3.png"],
    "status": "draft",
    "tiktokSettings": { "autoAddMusic": true }
  }'
```

| Field | Notes |
| --- | --- |
| `accounts` | required, numeric ids |
| `content` | caption, max 5000 chars |
| `media_url` / `media_urls` | one or many public URLs; many = carousel |
| `status` | `published` (default over REST), `draft`, `scheduled` |
| `scheduled_for` | ISO 8601, at least 60 s ahead, only with `scheduled` |
| `timezone` | IANA name |
| `platformOptions` | per account id: LinkedIn `firstComment`, `disableLinkPreview`; Pinterest `title`, `link` |
| `tiktokSettings.autoAddMusic` | root level, TikTok photo carousels |

Response: `{ post_id, status, platforms: [{ account_id, platform, status, url, error, action }] }`. `status` can be `published`, `scheduled`, `drafted`, `partial`, `processing` or `failed`. `action: "reconnect"` means the human must reconnect that account in the dashboard.

### Manage held posts

```bash
GET    /v1/social/posts?status=draft&limit=25        # also scheduled | published | processing | partial | failed, platform=, account_id=, cursor=
GET    /v1/social/posts/:id
PATCH  /v1/social/posts/:id                          # content, media_urls, accounts, status (draft|scheduled), scheduled_for, timezone, platformOptions
POST   /v1/social/posts/:id/publish                  # send a held post now
POST   /v1/social/posts/:id/sync                     # refresh provider status
DELETE /v1/social/posts/:id                          # discard; refused once any account went live
```

`is_editable` and `is_discardable` on each post tell you what is still allowed. Editing never re-renders and costs nothing.

### Analytics

```bash
GET /v1/social/analytics?platform=linkedin&source=orshot      # per post: impressions, engagement, clicks, rate; followers per account
GET /v1/social/analytics/daily?from=2026-10-01&to=2026-10-21  # day by day
GET /v1/social/analytics/accounts?from=2026-09-01             # follower history and growth per account
GET /v1/social/analytics/insights?platform=instagram          # best day-and-hour slots (UTC), frequency vs engagement, decay
```

`source` is `all`, `orshot` or `external` (posts synced from the platform, so history exists from day one). `refresh=1` bypasses the cache. Budget: 10 analytics requests per minute. Insights need posting history, so a new account returns empty slots.

## Common patterns

### Pattern 1: weekly content calendar as drafts

Render seven posts from one template with different `modifications`, create each with `status: "draft"`, list them for the user with `orshot_list_social_posts`, publish or schedule the approved ones. One update per change of caption or time.

### Pattern 2: schedule at the best time to post

`orshot_get_best_time_to_post` for the platform, take the top slot (UTC), convert to the user's timezone, pass it as `scheduled_for`. If slots are empty, ask the user for a time rather than inventing one.

### Pattern 3: cross-post, every platform, platform-specific extras

One `accounts` array with all ids. Put the link in `platformOptions[<linkedin id>].firstComment`, a `title` and `link` for Pinterest, and `tiktokSettings.autoAddMusic` for TikTok photo posts. Keep `content` under the shortest limit of the platforms you target (X is the tightest).

### Pattern 4: carousel from a multi-page template

Render a 5 to 10 page template with `pageN@` keys and add `publish`. Orshot uploads every page and posts a carousel on Instagram, LinkedIn, TikTok (photo mode), Threads and Bluesky. The `orshot-carousel` skill has the 6-slide formula.

### Pattern 5: learn from results

Daily: `orshot_get_social_analytics` with `source: "orshot"`, sort by engagement, keep the hook styles of the top quarter, drop the bottom quarter, write the next week's drafts. Record what changed so the user can read the log.

### Pattern 6: recover a failure

`partial` or `failed` with `action: "reconnect"`: tell the user which account to reconnect in the dashboard (Workspace > Socials > Accounts), keep the post as a draft, retry with `orshot_publish_social_draft` after they confirm. Any other `error`: show it verbatim; do not retry blindly.

## Safety rules

- Never publish without an explicit go-ahead for that post. "Prepare", "draft", "show me" mean `status: "draft"`.
- Repeat back the exact accounts (platform and username), the caption and the time before sending.
- Do not discard posts the user did not ask you to discard.
- Mention the $12 per account add-on once before suggesting the user connects more accounts.
- Over REST, keep the API key in the environment. Never echo it.

## Common gotchas

1. **Account ids are numeric and per account.** Two LinkedIn accounts have two ids. Publish by id, never by platform name.
2. **PDF cannot be posted anywhere.** Render `png`, `jpg` or `webp` (or `mp4` for video platforms).
3. **TikTok and YouTube take video, not single images.** TikTok accepts photo carousels (multiple images). Google Business takes images only.
4. **`scheduled_for` under 60 seconds ahead is rejected**, and it is invalid with `draft` or `published`.
5. **Instagram and TikTok publish asynchronously.** `processing` is not a failure. Sync or re-read the post before reporting.
6. **A failed publish never fails the render.** Read `publish[]` even when the render succeeded.
7. **Media URLs must be public.** Orshot render URLs are. Signed or localhost URLs are not.
8. **Captions over 5000 characters are rejected.** Platform limits are lower; X is the shortest.
9. **Analytics are capped at 10 requests per minute** across all analytics endpoints.
10. **Free plan workspaces cannot connect accounts.** A 403 on `/social/*` with a plan message is a billing state, not an auth bug. Point to https://orshot.com/pricing.

## Quick reference

```bash
openclaw mcp add orshot --url https://mcp.orshot.com/mcp --transport streamable-http --auth oauth && openclaw mcp login orshot

GET    /v1/social/accounts?include_health=true   # orshot_list_social_accounts
POST   /v1/studio/render            # + publish: { accounts, content, status, scheduled_for, timezone, platformOptions, tiktokSettings }   orshot_render_template
POST   /v1/social/publish           # { accounts, content, media_url | media_urls, status, scheduled_for, timezone, platformOptions, tiktokSettings }   orshot_publish_social_post
GET    /v1/social/posts?status=draft             # orshot_list_social_posts
GET    /v1/social/posts/:id                      # orshot_get_social_post
PATCH  /v1/social/posts/:id                      # orshot_update_social_post
POST   /v1/social/posts/:id/publish              # orshot_publish_social_draft
POST   /v1/social/posts/:id/sync
DELETE /v1/social/posts/:id                      # orshot_discard_social_post
GET    /v1/social/analytics                      # orshot_get_social_analytics
GET    /v1/social/analytics/daily?from=&to=      # orshot_get_social_analytics_daily
GET    /v1/social/analytics/accounts?from=       # orshot_get_social_followers
GET    /v1/social/analytics/insights?platform=   # orshot_get_best_time_to_post
```

Docs: https://orshot.com/docs/publish/introduction.md, https://orshot.com/docs/api-reference/social-publish.md, https://orshot.com/docs/api-reference/social-posts-list.md. Rendering details live in the `orshot` skill.
