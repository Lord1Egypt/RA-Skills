# Mallary CLI

Mallary CLI is the official command-line interface for the https://mallary.ai social media scheduling/posting tool. It gives developers, operators, scripts, CI jobs, and AI agents a fast way to work with the same public platform that powers the Mallary.ai dashboard, REST API, and MCP server.

With the CLI you can:

- upload local media files to Mallary.ai
- create and schedule posts to your social media accounts
- inspect jobs and grouped posts
- fetch post analytics
- manage webhooks
- list dashboard profiles and target non-default profiles
- manage profile-scoped brand and AI auto-reply settings
- list connected platforms for a profile
- disconnect platforms from a profile

Mallary CLI is a direct client for the public Mallary.ai API. It does not bypass plan limits, feature gates, or platform rules. CLI access is available on paid plans only.

## Install

### npm

```bash
npm install -g @mallary/cli
```

### npx

```bash
npx @mallary/cli --help
```

### Update

```bash
npm install -g @mallary/cli@latest
```

### Uninstall

```bash
npm uninstall -g @mallary/cli
```

## Authentication

Mallary CLI uses environment-variable auth only. Get your API key at https://mallary.ai now.

```bash
export MALLARY_API_KEY="your_mallary_api_key"
```

The CLI is available on paid plans only: Starter, Pro, and Business.

## Quickstart

Check the health of Mallary.ai services:

```bash
mallary health
```

Upload a local file to Mallary.ai CDN:

```bash
mallary upload ./launch.mp4
```

Create a social media post from flags:

```bash
mallary posts create \
  --message "Check out my new product video!" \
  --platform facebook \
  --platform instagram \
  --media ./launch.mp4 \
  --thumbnail ./launch-cover.jpg
```

List your posts:

```bash
mallary posts list
```

Inspect one job:

```bash
mallary jobs get 123
```

List your connected platforms:

```bash
mallary platforms list
mallary profiles list
```

Use `mallary profiles list` to find a profile's ID. Pass it as `--profile-id` when you want a command to target a non-default Dashboard profile.

## Commands

### Health

```bash
mallary health
mallary health --json
```

### Upload

```bash
mallary upload ./image.png
mallary upload ./image.png ./video.mp4 --json
```

This command:

1. calls Mallary to create a presigned upload URL
2. uploads the local bytes for you
3. returns the final Mallary media URL

### Posts

Create from flags:

```bash
mallary posts create \
  --message "Hello from Mallary CLI" \
  --platform facebook \
  --platform linkedin \
  --profile-id AbC123xYz90 \
  --media ./launch-video.mp4 \
  --thumbnail ./launch-cover.jpg \
  --comment "Follow-up comment 1" \
  --comment "Follow-up comment 2" \
  --auto-reply-enabled \
  --scheduled-at 2026-03-30T15:00:00Z
```

Create with a local wall-clock schedule plus timezone:

```bash
mallary posts create \
  --message "Timezone-aware launch" \
  --platform threads \
  --scheduled-at 2026-04-06T09:30 \
  --scheduled-timezone America/Los_Angeles
```

Create from a JSON file:

```bash
mallary posts create --file ./post.json
```

Example `post.json`:

```json
{
  "message": "Launch update",
  "platforms": ["youtube", "facebook"],
  "media": [{ "url": "./launch.mp4", "thumbnail_url": "./launch-cover.jpg" }],
  "platform_options": {
    "youtube": {
      "title": "Launch update"
    }
  }
}
```

Notes:

- `--file` is for raw/advanced payloads and is mutually exclusive with payload-building flags.
- In flag mode, use `--scheduled-at` with an absolute timestamp like `2026-04-06T18:30:00Z`, or pair a local time like `2026-04-06T14:30` with `--scheduled-timezone America/New_York`.
- `--scheduled-timezone` requires `--scheduled-at`.
- In file mode, the CLI checks each `media[].url` value.
- If `media[].url` is a local file path like `./launch.png`, the CLI uploads that file to the Mallary CDN first, then replaces it with the final hosted Mallary CDN file URL before sending the post request.
- In file mode, local `media[].thumbnail_url` paths are also uploaded automatically.
- If `media[].url` is already a remote URL, it must already be hosted on `https://files.mallary.ai/...`. External media URLs are rejected by the CLI.
- Existing remote `media[].thumbnail_url` values must also already be hosted on `https://files.mallary.ai/...`.
- This is intentional because many social platforms only accept trusted media URLs. The CLI requires media to be uploaded to the Mallary CDN first.
- Platform-specific payloads are supported in file mode via `platform_options`.
- Each key in `platform_options` should match the platform name you put in `platforms`.

Video thumbnails:

- In flag mode, use `--thumbnail` with exactly one `--media` item.
- In file mode, put `thumbnail_url` on the video media item.
- YouTube regular videos, Facebook videos, and Instagram videos/Reels can use custom thumbnails/covers.
- YouTube accepts `jpg`, `jpeg`, or `png` thumbnails up to 2 MB. Recommended: `1280x720` 16:9. YouTube Shorts thumbnails are skipped.
- Facebook videos accept `jpg`, `jpeg`, or `png` thumbnails up to 10 MB.
- TikTok video posts do not accept arbitrary image thumbnails through Mallary; supplying `thumbnail_url` disables Mallary's `video_cover_timestamp_ms` behavior and lets TikTok use its default cover.
- TikTok photo posts can use `thumbnail_url` only when it exactly matches one of the supplied photo URLs and should become the cover photo.

Platform-specific payloads:

- These are available only in file mode with `mallary posts create --file payload.json`.
- The CLI does not validate platform-specific keys itself; it passes them through to the Mallary API.
- If you include `platform_options.instagram`, your `platforms` array should include `instagram`. The same rule applies to every platform.
- For the exact currently documented `platform_options` fields and examples by platform, see:
  `https://docs.mallary.ai/api-reference/endpoint/create#body-platform-options`

Platform-specific media rules:

- The CLI uses the same platform media validation as the Mallary API.
- YouTube requires exactly one video.
- Instagram currently works best with one image or one video in the public publisher implementation.
- LinkedIn currently supports text-only posts or one image attachment only.
- TikTok video posts require one video, and TikTok photo posts support up to 35 JPEG/WebP images.
- Pinterest requires exactly one image or GIF, or exactly one video, plus `boardId`.
- Reddit image posts require one image or GIF, and Reddit video upload is not supported by the current public API path.
- X allows up to 4 images, or 1 video, or 1 GIF.
- Full matrix:
  `https://docs.mallary.ai/api-reference/endpoint/create#platform-specific-media-rules`

Payload shape:

```json
{
  "profile_id": "AbC123xYz90",
  "message": "Launch update",
  "platforms": ["facebook", "youtube"],
  "scheduled_at": "2026-04-06T14:30",
  "scheduled_timezone": "America/New_York",
  "media": [{ "url": "./launch.mp4", "thumbnail_url": "./launch-cover.jpg" }],
  "platform_options": {
    "facebook": {
      "post_type": "feed"
    },
    "youtube": {
      "post_type": "shorts",
      "title": "Launch update",
      "visibility": "public"
    }
  }
}
```

Facebook:

- `post_type`: `feed` or `story`
- `link`: optional link URL for link-style feed posts without media
- `pageId`: optional advanced override if you need to target a specific connected Facebook Page

```json
{
  "message": "Read the full announcement",
  "platforms": ["facebook"],
  "platform_options": {
    "facebook": {
      "post_type": "feed",
      "link": "https://example.com/blog/launch"
    }
  }
}
```

Instagram:

- `post_type`: `feed`, `story`, `reel`, or `carousel`

```json
{
  "message": "Behind the scenes",
  "platforms": ["instagram"],
  "media": [{ "url": "./reel.mp4", "thumbnail_url": "./reel-cover.jpg" }],
  "platform_options": {
    "instagram": {
      "post_type": "reel"
    }
  }
}
```

LinkedIn:

- `author_urn`: optional advanced override for the LinkedIn author/org URN used when publishing

```json
{
  "message": "Company update from ACME co",
  "platforms": ["linkedin"],
  "media": [{ "url": "./update.png" }],
  "platform_options": {
    "linkedin": {
      "author_urn": "urn:li:organization:123456"
    }
  }
}
```

YouTube:

- `post_type`: `regular` or `shorts`
- `title`: optional custom title
- `visibility`: `public`, `unlisted`, or `private`
- `categoryId`: optional YouTube category id
- `madeForKids`: optional boolean

```json
{
  "message": "Watch our latest product walkthrough",
  "platforms": ["youtube"],
  "media": [{ "url": "./walkthrough.mp4", "thumbnail_url": "./walkthrough-cover.jpg" }],
  "platform_options": {
    "youtube": {
      "post_type": "shorts",
      "title": "Acme Co walkthrough",
      "visibility": "unlisted",
      "categoryId": "28",
      "madeForKids": false
    }
  }
}
```

TikTok:

- `post_type`: `video` or `photo`
- `post_mode`: `DIRECT_POST` or `MEDIA_UPLOAD`
- `source`: `FILE_UPLOAD` or `PULL_FROM_URL` for video posts; photo posts always use `PULL_FROM_URL`
- TikTok `PULL_FROM_URL` media must already be hosted on Mallary CDN at `https://files.mallary.ai/...`
- TikTok photo posts currently accept only `jpg`, `jpeg`, or `webp` images; `png` files are rejected
- `privacy_level`: optional direct-post override, must match TikTok creator info
- `disable_comment`: optional for direct post
- `disable_duet`: optional for direct-post video
- `disable_stitch`: optional for direct-post video
- `video_cover_timestamp_ms`: optional direct-post video cover frame
- `thumbnail_url` on a TikTok video media item overrides Mallary's timestamp cover behavior; Mallary does not send arbitrary image thumbnails to TikTok video posts
- `title`: optional override; defaults to `message`
- `description`: optional for photo posts
- `auto_add_music`: optional for direct-post photo
- `brand_content_toggle`, `brand_organic_toggle`: optional TikTok disclosure toggles
- `is_aigc`: optional direct-post video AI-content label
- `photo_cover_index`: optional photo cover selection
- `thumbnail_url` on a TikTok photo media item selects the cover only when it exactly matches one of the supplied photo URLs

Defaults:

- Video posts default to `post_mode=MEDIA_UPLOAD` and `source=FILE_UPLOAD`.
- Photo posts default to `post_mode=MEDIA_UPLOAD`.
- If `privacy_level` is omitted for direct post, Mallary first tries the first allowed privacy level from TikTok creator info, preferring `PUBLIC_TO_EVERYONE`, then `MUTUAL_FOLLOW_FRIENDS`, then `FOLLOWER_OF_CREATOR`, then `SELF_ONLY`. If TikTok returns the private-account-only direct-post restriction, Mallary retries once with the most private allowed level.
- If `disable_comment`, `disable_duet`, or `disable_stitch` are omitted for direct post, Mallary falls back to the creator settings returned by TikTok.

```json
{
  "message": "New feature demo",
  "platforms": ["tiktok"],
  "media": [{ "url": "./demo.mp4" }],
  "platform_options": {
    "tiktok": {
      "post_type": "video",
      "post_mode": "DIRECT_POST",
      "source": "FILE_UPLOAD",
      "privacy_level": "FOLLOWER_OF_CREATOR",
      "disable_comment": false,
      "disable_duet": false,
      "disable_stitch": false,
      "video_cover_timestamp_ms": 1000,
      "brand_content_toggle": false,
      "brand_organic_toggle": false,
      "is_aigc": false
    }
  }
}
```

Photo post example:

```json
{
  "message": "Photo launch",
  "platforms": ["tiktok"],
  "media": [
    { "url": "https://files.mallary.ai/photo-1.webp" },
    { "url": "https://files.mallary.ai/photo-2.webp" }
  ],
  "platform_options": {
    "tiktok": {
      "post_type": "photo",
      "post_mode": "DIRECT_POST",
      "description": "Behind the scenes from launch day",
      "privacy_level": "PUBLIC_TO_EVERYONE",
      "disable_comment": false,
      "auto_add_music": true,
      "photo_cover_index": 1
    }
  }
}
```

Pinterest:

- `post_type`: `image` or `video`
- `boardId`: board id to publish into
- `link`: optional destination URL
- `alt_text`: optional alt text for the Pin image

```json
{
  "message": "Product launch",
  "platforms": ["pinterest"],
  "media": [{ "url": "./launch.png" }],
  "platform_options": {
    "pinterest": {
      "post_type": "image",
      "boardId": "920740542650170734",
      "link": "https://example.com/pricing",
      "alt_text": "Acme Co pricing page preview"
    }
  }
}
```

Reddit:

- `post_type`: `text`, `link`, or `image`
- `subreddit` or `subredditName`: target subreddit name

```json
{
  "message": "We just launched a new agentic scheduling workflow",
  "platforms": ["reddit"],
  "platform_options": {
    "reddit": {
      "post_type": "text",
      "subreddit": "socialmedia"
    }
  }
}
```

X / Twitter:

- No additional platform-specific payload fields are currently consumed by the public API beyond the standard post body.

Canonical reference for platform-specific post fields:

- `https://docs.mallary.ai/api-reference/endpoint/create#body-platform-options`

```json
{
  "message": "Shipping a new feature today",
  "platforms": ["x"],
  "media": [{ "url": "./launch.png" }]
}
```

Comments under post:

- Use repeatable `--comment` flags in flag mode.
- In file mode, send `comments_under_post` as an array.
- The API currently limits `comments_under_post` to 3 items.
- TikTok does not currently support `comments_under_post`.

Example:

```bash
mallary posts create \
  --message "New launch today" \
  --platform facebook \
  --media ./launch.png \
  --comment "What do you think?" \
  --comment "Questions? Ask below."
```

File mode example:

```json
{
  "message": "New launch today",
  "platforms": ["facebook"],
  "media": [{ "url": "./launch.png" }],
  "comments_under_post": [
    { "content": "What do you think?" },
    { "content": "Questions? Ask below." }
  ]
}
```

AI auto reply:

- AI Auto Replies automatically detect new comments on your published posts and uses OpenAI (ChatGPT) to post helpful replies based on your settings in configured the Mallary dashboard or as described in the settings section below. AI Auto Replies are supported on YouTube, Facebook, Instagram, LinkedIn, X (Twitter), Reddit.
- AI Auto Replies are available on Pro and Business plans only.
- It depends on your saved profile-scoped brand settings, not just the current post payload.
- You can enable it for the selected profile in `mallary settings update`, or per post with `--auto-reply-enabled`.
- If you omit `--auto-reply-enabled`, the post uses the selected profile's saved setting.
- To enable it successfully, your settings must include: `business_name`, `website_url`, `business_description`, `services`, and `contact_info`.

Per-post example:

```bash
mallary posts create \
  --message "Ask us anything about agentic scheduling." \
  --platform facebook \
  --media ./hero.png \
  --auto-reply-enabled
```

File mode example:

```json
{
  "message": "Ask us anything about agentic scheduling.",
  "platforms": ["facebook"],
  "media": [{ "url": "./hero.png" }],
  "auto_reply_enabled": true
}
```

List grouped posts:

```bash
mallary posts list
mallary posts list --page 2 --per-page 25 --json
```

Delete a queued or scheduled post:

```bash
mallary posts delete 123
```

### Jobs

```bash
mallary jobs get 123
mallary jobs get 123 --json
```

### Analytics

```bash
mallary analytics list
mallary analytics list --post-id 123
mallary analytics list --profile-id AbC123xYz90
```

Analytics are profile-scoped. Omit `--profile-id` to use the default profile.

### Profiles

Profiles are used to group your social media accounts. You can create a profile for each of your businesses, and then connect your social media accounts for each business inside this profile. Your default profile will be used if you don't pass a `profile_id` when making requests.

Profiles group social platform connections, posts, analytics, and brand or AI auto-reply settings. The Mallary dashboard has one top-level **Dashboard profile** bar; everything underneath it belongs to the selected profile.

Every user has a default profile. Omit `--profile-id` to use it. For non-default profiles, list profiles and copy the random public profile ID:

```bash
mallary profiles list
mallary profiles list --json
```

Use that ID with profile-aware commands:

```bash
mallary posts create --message "Launch update" --platform linkedin --profile-id AbC123xYz90
mallary posts list --profile-id AbC123xYz90
mallary analytics list --profile-id AbC123xYz90
mallary settings get --profile-id AbC123xYz90
mallary settings update --file ./settings.partial.json --profile-id AbC123xYz90
mallary platforms list --profile-id AbC123xYz90
mallary platforms disconnect facebook --profile-id AbC123xYz90
```

In file mode, use `profile_id` in the payload. The CLI currently lists and targets profiles; create and rename profile workflows are handled in the dashboard or REST API. See [PROFILES.md](./PROFILES.md).

### Webhooks

List:

```bash
mallary webhooks list
```

Create:

```bash
mallary webhooks create \
  --url https://example.com/mallary \
  --event post.published \
  --event post.failed
```

Delete:

```bash
mallary webhooks delete 12
```

### Settings

Get current settings:

```bash
mallary settings get
mallary settings get --profile-id AbC123xYz90
```

Update settings from a partial JSON file:

```bash
mallary settings update --file ./settings.partial.json
mallary settings update --file ./settings.partial.json --profile-id AbC123xYz90
```

Example partial settings payload:

```json
{
  "auto_reply_enabled": true,
  "brand_profile": "Mallary helps brands schedule, publish, and manage social media content with AI-assisted workflows.",
  "business_name": "My Business",
  "business_description": "Local HVAC company",
  "website_url": "https://example.com",
  "services": "HVAC installation, repair, and maintenance",
  "features": "Same-day service, financing, weekend appointments",
  "contact_info": "Call (555) 555-5555 or email hello@example.com",
  "pricing": "Free estimates. Maintenance plans start at $29/month.",
  "faq": "Q: Do you offer emergency service? A: Yes, 24/7."
}
```

Accepted settings fields:

- `auto_reply_enabled`
- `brand_profile`
- `business_name`
- `business_description`
- `website_url`
- `services`
- `features`
- `contact_info`
- `pricing`
- `faq`

Notes:

- `mallary settings update --file ...` accepts partial updates, so you can send only the fields you want to change.
- Settings are profile-scoped. Omit `--profile-id` to use the default profile.
- `auto_reply_enabled` can only be turned on for paid plans that include AI auto reply.
- Enabling `auto_reply_enabled` also requires these settings fields to be populated: `business_name`, `website_url`, `business_description`, `services`, and `contact_info`.

### Platforms

Disconnect a platform:

```bash
mallary platforms list
mallary platforms list --profile-id AbC123xYz90
mallary platforms disconnect facebook
mallary platforms disconnect facebook --profile-id AbC123xYz90
```

## JSON Output

Human-readable output is the default.

Use `--json` for scripting:

```bash
mallary posts list --json
```

Output rules:

- direct API wrapper commands emit the API response body
- convenience flows like `upload` emit CLI-specific JSON
- `posts create` emits CLI-specific JSON when local file uploads occur before submission

Example:

```bash
mallary upload ./launch.png --json
```

```json
{
  "ok": true,
  "uploads": [
    {
      "source_path": "./launch.png",
      "filename": "launch.png",
      "media_url": "https://files.mallary.ai/uploads/launch.png",
      "storage_key": "uploads/launch.png",
      "content_type": "image/png",
      "size": 18293
    }
  ]
}
```

## Exit Codes

- `0`: success
- `1`: local CLI/config/input failure
- `2`: remote API or upload failure

## Automation and CI

Example shell script:

```bash
#!/usr/bin/env bash
set -euo pipefail

export MALLARY_API_KEY="${MALLARY_API_KEY:?missing}"

UPLOAD_JSON="$(mallary upload ./hero.png --json)"
MEDIA_URL="$(printf '%s' "$UPLOAD_JSON" | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s).uploads[0].media_url))')"

mallary posts create \
  --message "Deployed via CI" \
  --platform facebook \
  --platform linkedin \
  --media "$MEDIA_URL" \
  --json
```

GitHub Actions example:

```yaml
- name: Install Mallary CLI
  run: npm install -g @mallary/cli

- name: Publish post
  env:
    MALLARY_API_KEY: ${{ secrets.MALLARY_API_KEY }}
  run: |
    mallary posts create \
      --message "Release shipped." \
      --platform facebook \
      --platform linkedin \
      --profile-id AbC123xYz90
```

## AI Agent Notes

If you are an AI agent or building an agent integration:

- read [SKILL.md](./SKILL.md) first for the compact command and workflow summary
- read [PROFILES.md](./PROFILES.md) before targeting a non-default Dashboard profile
- use `--json` whenever the CLI is part of an automated toolchain
- prefer `mallary posts create --file payload.json` for complex platform-specific payloads

## Links

- Main site: https://mallary.ai/
- Dashboard: https://mallary.ai/dashboard
- Pricing: https://mallary.ai/pricing
- API docs: https://docs.mallary.ai/
- Profiles reference: [PROFILES.md](./PROFILES.md)
- MCP docs source: `docs/mcp.md`
- Support: mailto:support@mallary.ai

## Versioning

Mallary CLI uses semantic versioning.
