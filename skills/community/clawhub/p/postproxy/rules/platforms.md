# Platform-Specific Parameters

For Instagram, TikTok, YouTube, Telegram, etc., add a `platforms` object keyed by network when creating or updating a post:
```json
{
  "platforms": {
    "instagram": { "format": "reel", "first_comment": "Link in bio!" },
    "youtube": { "title": "Video Title", "privacy_status": "public" },
    "tiktok": { "privacy_status": "PUBLIC_TO_EVERYONE" },
    "telegram": { "chat_id": "-1001234567890", "parse_mode": "HTML", "disable_link_preview": true }
  }
}
```

On update, `platforms` is merged per network — sending one key updates only that key (see [posts.md](posts.md)).

## Bluesky
- No custom parameters.
- **Character limit:** 300 graphemes (emoji + combining sequences count as one).
- **Rich text auto-detection** — Postproxy scans the body and converts mentions, hashtags, and URLs to AT Protocol facets. Write the post normally, no special markup:
  - `@handle.bsky.social` → clickable mention (custom-domain handles work too; resolution cached 24h; unresolvable handles fall through as plain text).
  - `#hashtag` → clickable tag feed link (letters/digits/underscores, up to 64 chars).
  - `https://...` URLs → clickable links (trailing punctuation stripped).
- **Link card previews** — when the post contains a URL **and no media attachments**, Postproxy auto-generates a Bluesky link card embed by reading OG meta (`og:title`, `og:description`, `og:image`). Image is skipped if > ~950 KB. Link cards and media attachments are mutually exclusive — if media is attached, the URL is still rendered as a clickable link but no preview card is generated. Place the URL at the end of the post for the best preview.
- **Media:** images ≤ 1 MB (jpg/png/webp/gif, max 4), video ≤ 100 MB (mp4/mov, max 1, 1–60s). Cannot mix video + image.

Example:
```json
{
  "post": {
    "body": "Hey @jay.bsky.team — new #release out: https://example.com/post"
  },
  "profiles": ["bluesky"]
}
```

## Telegram
Telegram is a **bring-your-own-bot** integration. Each connected profile is one bot (created via [@BotFather](https://t.me/BotFather)) and can publish to any channel where that bot has been added as administrator. List target channels via the List Placements endpoint (see [profiles.md](profiles.md)).

Parameters (under `platforms.telegram`):
- `chat_id` (string, **required**) — ID of the destination channel/group. Get it from `/api/profiles/{profile_id}/placements`.
- `parse_mode` (string, optional) — `"HTML"`, `"MarkdownV2"`, or omit for plain text.
- `disable_link_preview` (boolean, optional) — suppress the URL preview card.
- `disable_notification` (boolean, optional) — send silently (no notification sound).

**Character limit:** 4,096 chars for text-only posts, 1,024 chars for captions when media is attached. Body content beyond the caption limit is truncated.

**Media:** images ≤ 10 MB (jpg/png/webp/gif, max 10), video ≤ 50 MB (mp4/mov, max 10), document ≤ 50 MB (pdf/doc/docx/zip/mp3/wav, max 1). Mixing video and image is allowed (sent as a media group).

The returned `external_id` is `"<chat_id>/<message_id>"`. For media groups, ids are comma-separated: `"<chat_id>/<id1>,<id2>,…"`.

Notes:
- Bot must be a member (preferably **administrator** with permission to post) of the target channel. Add it manually in Telegram.
- Channels appear in `/placements` after Telegram pushes a `my_chat_member` event. If a channel doesn't show up, ask the user to remove and re-add the bot to refire discovery.
- If the bot is kicked or its token is revoked in BotFather, the next publish fails with `inactive_profile_error` and the profile is deactivated.

Example:
```json
{
  "post": {
    "body": "<b>New release</b> — read more on our blog https://example.com/post"
  },
  "profiles": ["telegram"],
  "platforms": {
    "telegram": {
      "chat_id": "-1001234567890",
      "parse_mode": "HTML",
      "disable_link_preview": true,
      "disable_notification": false
    }
  }
}
```

## Google Business
Google Business publishes **local posts** to a Business Profile **location**. One profile may manage multiple accounts × multiple locations — the target location is selected via `location_id`. Use List Placements (see [profiles.md](profiles.md)) to enumerate locations.

### Formats

| Format | Description |
|--------|-------------|
| `standard` | Plain local post (default) |
| `event` | Event with a title and date range |
| `offer` | Promotion with a validity window and optional coupon |

Each format accepts only its relevant parameters — fields are scoped per format.

### Shared Parameters (all formats)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `location_id` | string | Yes | Full location resource path, e.g. `accounts/123456789/locations/987654321`. Get it from List Placements. |
| `language_code` | string | No | BCP 47 code (e.g. `en`, `de`). Defaults to `en`. Metadata only — does not translate the body. |
| `cta_action_type` | string | No | Call-to-action button. One of `LEARN_MORE`, `BOOK`, `ORDER`, `SHOP`, `SIGN_UP`, `CALL`. |
| `cta_url` | string | No | HTTPS URL the CTA button opens. **Required for every CTA except `CALL`**. |

### `event` Format — Additional Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `event_title` | string | Yes | Display title for the event. |
| `event_start_date` | string | Yes | `YYYY-MM-DD`. |
| `event_end_date` | string | Yes | `YYYY-MM-DD`. |
| `event_start_time` | string | No | `HH:MM` (24h). |
| `event_end_time` | string | No | `HH:MM` (24h). |

### `offer` Format — Additional Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `event_start_date` | string | Yes | `YYYY-MM-DD`. Start of the offer validity window. |
| `event_end_date` | string | Yes | `YYYY-MM-DD`. End of the offer validity window. |
| `event_start_time` | string | No | `HH:MM` (24h). |
| `event_end_time` | string | No | `HH:MM` (24h). |
| `event_title` | string | No | Offer headline. Defaults to `"Special Offer"` if blank. |
| `offer_coupon_code` | string | No | Promo code displayed with the offer. |
| `offer_redeem_url` | string | No | URL where the offer can be redeemed. |
| `offer_terms` | string | No | Terms and conditions for the offer. |

**Character limit:** 1,500 characters (post summary).

**Media:** image only — jpg/png ≤ 5 MB, max 1, minimum 400×300 px (recommended 1200×900, 4:3). **Video is not supported.** Text-only posts are allowed.

### Notes

- The `external_id` returned for a local post is the full Google resource path (e.g. `accounts/.../locations/.../localPosts/...`). Pass it back as-is for deletion.
- "Comments" on a Google Business profile map to **reviews on the location**, not per-post comments. They are exposed via the Profile Comments API (see [comments.md](comments.md)), not the post Comments API.
- Google has sunset local posts for some verticals (e.g. lodging). Publishing on a location whose category is no longer eligible returns a permission/validation error.

### Example — `standard`

```json
{
  "post": {
    "body": "We're now open on Sundays from 10am to 4pm — come visit!"
  },
  "profiles": ["google_business"],
  "platforms": {
    "google_business": {
      "format": "standard",
      "location_id": "accounts/123456789/locations/987654321",
      "cta_action_type": "LEARN_MORE",
      "cta_url": "https://acme.example.com/hours"
    }
  }
}
```

### Example — `event`

```json
{
  "post": {
    "body": "Join us for our 5-year anniversary party — live music, free coffee, prizes."
  },
  "profiles": ["google_business"],
  "platforms": {
    "google_business": {
      "format": "event",
      "location_id": "accounts/123456789/locations/987654321",
      "event_title": "Acme Coffee 5-Year Anniversary",
      "event_start_date": "2026-06-15",
      "event_start_time": "18:00",
      "event_end_date": "2026-06-15",
      "event_end_time": "22:00",
      "cta_action_type": "LEARN_MORE",
      "cta_url": "https://acme.example.com/anniversary"
    }
  }
}
```

### Example — `offer`

`offer` posts require a validity window (`event_start_date` and `event_end_date`). `event_title` is optional and defaults to `"Special Offer"` when blank.

```json
{
  "post": {
    "body": "20% off all whole-bean coffee through the end of the month."
  },
  "profiles": ["google_business"],
  "platforms": {
    "google_business": {
      "format": "offer",
      "location_id": "accounts/123456789/locations/987654321",
      "event_start_date": "2026-06-01",
      "event_end_date": "2026-06-30",
      "offer_coupon_code": "BEANS20",
      "offer_redeem_url": "https://acme.example.com/shop",
      "offer_terms": "One per customer. Cannot be combined with other offers."
    }
  }
}
```
