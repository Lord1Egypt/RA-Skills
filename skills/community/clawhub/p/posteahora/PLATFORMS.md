# Supported Platforms

PosteAhora publishes and schedules across every major social network. Connect
accounts in the app (**Connections**), then target them from the CLI by their
account ID (`posteahora accounts`).

| Platform | Publish | Schedule | Analytics | Notes |
|----------|:------:|:--------:|:---------:|-------|
| **Instagram** | ✅ | ✅ | ✅ | Feed posts, reels, stories; single image, carousel, or video |
| **TikTok** | ✅ | ✅ | ✅ | Video and photo posts; **needs `platformOptions` → API/MCP only** (see below) |
| **YouTube** | ✅ | ✅ | ✅ | Video uploads (Shorts and standard) |
| **X (Twitter)** | ✅ | ✅ | ✅ | Text, images, video; shorter per-platform captions supported |
| **Facebook** | ✅ | ✅ | ✅ | Page posts, images, video, reels |
| **LinkedIn** | ✅ | ✅ | — | Text, single/multi-image, video (personal profiles) |
| **Threads** | ✅ | ✅ | ✅ | Text and media posts |
| **Bluesky** | ✅ | ✅ | ✅ | Text and images (no video yet) |
| **Mastodon** | ✅ | ✅ | ✅ | Text and media; your instance's own character limit applies |
| **Discord** | ✅ | ✅ | — | Channel messages via webhook |
| **Telegram** | ✅ | ✅ | — | Channel or group via a bot (make the bot an admin first) |
| **WordPress** | ✅ | ✅ | — | Blog posts; the title is a separate required field |
| **Dev.to** | ✅ | ✅ | — | Markdown articles; title + up to 4 tags |
| **Tumblr** | ✅ | ✅ | — | Posts with a title, body and images (no video yet) |
| **Pinterest** | ✅ | ✅ | ✅ | Image, carousel or video Pins; **a board is required → `platformOptions`, API/MCP only** |
| **Google Business** | ✅ | ✅ | — | Local Posts per location; events, offers and a CTA button need **`platformOptions` → API/MCP only**; no per-post analytics |

## Targeting platforms

Each post targets one or more channels as `platform:accountId` pairs:

```bash
posteahora post "Cross-posting everywhere" \
  --to instagram:a1b2 \
  --to twitter:c3d4 \
  --to linkedin:e5f6 \
  --to threads:g7h8
```

Get the IDs with:

```bash
posteahora accounts
```

## Per-platform options

The CLI exposes the format flags:

- `--post-type post|reel|story`
- `--media-type image|video`

Anything platform-specific beyond that — `platformOptions` and the per-platform
caption overrides in `platformCaptions` — is **REST API and MCP only**. The CLI
does not send those fields.

### TikTok needs `platformOptions`

Omit them entirely and the post falls back to safe defaults —
`privacyLevel: "SELF_ONLY"` — so it publishes **privately** and nobody sees it.
Send the object but leave out `privacyLevel` and it fails with
`Privacy level "undefined"`. Keys are camelCase; snake_case is silently ignored:

```json
{
  "tiktok": {
    "privacyLevel": "PUBLIC_TO_EVERYONE",
    "photoTitle": "≤90 characters",
    "disableComment": false,
    "disableDuet": false,
    "disableStitch": false,
    "autoAddMusic": true
  }
}
```

The photo title key is **`photoTitle`** — a `title` inside `platformOptions.tiktok`
is ignored, and the post's top-level `title` fills the *video* title instead.

Use `autoAddMusic: false` when the video already has its own audio. Also pass
`mediaType` explicitly — it decides the photo vs video endpoint — and note that
TikTok photos must be **JPEG** (PNG fails with `file_format_check_failed`) and
must be hosted by PosteAhora, since TikTok verifies URL ownership. Upload via
`create_upload_url` (the presigned URL expires after 300 seconds) and use the
returned `publicUrl`.

TikTok also publishes asynchronously: right after the scheduled time the post
stays `queued` for a few minutes. That is expected — check again rather than
retrying.

If a requested platform has no connected account, the CLI reports it — connect it
in the app first. Platform availability depends on each network's API and your
connected account's permissions.
