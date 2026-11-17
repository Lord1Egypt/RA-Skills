# Platform rules

Check this before creating a post. Each post targets one social account, so the rules of that account's platform apply.

## Media and captions

| Platform | Media required? | Media limits | Max caption |
|---|---|---|---|
| Instagram | Yes | 1 to 10 images or videos (carousel). Story: exactly 1 | 2,200 |
| Facebook | No | Up to 10 images, or 1 video. No mixing. Story: exactly 1 | No strict limit |
| X | No | Up to 4 images or videos | No strict limit |
| LinkedIn | No | Up to 20 images, or 1 video, or 1 PDF. No mixing | No strict limit |
| TikTok | Yes | 1 video, or 1 or more images. No mixing | 2,200 |
| YouTube | Yes | Exactly 1 video | No strict limit |
| Pinterest | Yes | Exactly 1 image or video | 500 (description) |
| Threads | No | Up to 20 images or videos | 500 |
| Bluesky | No | Up to 4 images, or 1 video. No mixing | 300 |
| Google Business | No | Up to 1 image, no video | 1,500 |

Caption limits are enforced by the platform at publish time, so a too-long caption can be accepted on create and then fail when publishing. Keep captions within the limit up front. When posting the same message to several platforms, shorten it for Bluesky (300) and Threads (500).

Carousel order follows the order of `mediaIds`.

## Stories

`"isStory": true` posts a story. Instagram and Facebook only, exactly 1 media file.

## YouTube: `youtubeParams` (required)

| Field | Required | Notes |
|---|---|---|
| `title` | yes | Max 100 chars |
| `categoryId` | no | Default `"22"` (People & Blogs). Others: `"1"` Film & Animation, `"2"` Autos, `"10"` Music, `"15"` Pets & Animals, `"17"` Sports, `"19"` Travel & Events, `"20"` Gaming, `"23"` Comedy, `"24"` Entertainment, `"25"` News & Politics, `"26"` Howto & Style, `"27"` Education, `"28"` Science & Technology |
| `tags` | no | One comma-separated string, max 500 chars, e.g. `"tech,tutorial"` |
| `selfDeclaredMadeForKids` | no | Default `false` |

The caption becomes the video description.

```json
"youtubeParams": { "title": "Spring collection lookbook", "tags": "fashion,spring" }
```

## TikTok: `tiktokParams` (optional)

| Field | Default | Notes |
|---|---|---|
| `privacyLevel` | `PUBLIC_TO_EVERYONE` | `PUBLIC_TO_EVERYONE`, `FOLLOWER_OF_CREATOR`, `MUTUAL_FOLLOW_FRIENDS`, `SELF_ONLY` |
| `disableComment` | `false` | |
| `disableDuet` | `false` | |
| `disableStitch` | `false` | |
| `isDraftType` | `false` | `true` sends it to the TikTok inbox as a draft instead of publishing |
| `isCommercialContent` | `false` | Disclose commercial content |
| `isYourBrand` | `false` | Promotes your own business |
| `isBrandedContent` | `false` | Paid partnership. Not allowed with `SELF_ONLY` |
| `autoAddMusic` | `true` | Photo posts only |
| `photosPostTitle` | | Photo posts only, max 90 chars |

Ask the user before setting a privacy level other than the default, and before marking content as commercial or branded.

## Pinterest: `pinterestParams` (required)

| Field | Required | Notes |
|---|---|---|
| `boardId` | yes | From `GET /social-accounts/{id}/pinterest-boards`. If the user did not name a board, list them and ask |
| `title` | no | Max 100 chars |
| `link` | no | Destination URL when the pin is clicked |
| `altText` | no | Max 500 chars |

```json
"pinterestParams": { "boardId": "715376267631025391", "title": "Spring outfits", "link": "https://example.com/spring" }
```

## Google Business Profile: `googleBusinessParams` (optional)

`topicType` picks the post type:

- `STANDARD` (default): an update.
- `EVENT`: needs `eventTitle` (max 58 chars), `startDate`, `endDate` (ISO 8601, start before end).
- `OFFER`: needs `eventTitle`, `startDate`, `endDate`. Optional `couponCode` (max 58), `redeemOnlineUrl`, `termsConditions`. Gets an automatic "View offer" button, so do not set `actionType`.

Call-to-action button (`STANDARD` and `EVENT`): `actionType` is one of `BOOK`, `ORDER`, `SHOP`, `LEARN_MORE`, `SIGN_UP`, `CALL`. Every type except `CALL` needs `actionUrl`. `CALL` uses the profile's phone number.

```json
"googleBusinessParams": {
  "topicType": "OFFER",
  "eventTitle": "20% off this weekend",
  "startDate": "2026-04-03T09:00:00.000Z",
  "endDate": "2026-04-05T21:00:00.000Z",
  "couponCode": "SPRING20"
}
```

## X

- `xCommunityId` (optional): post into an X community.
- `xTaggedUsers` (optional): one comma-separated string of usernames to tag in the media, max 10, e.g. `"jack,acme"`. Needs media.

## Link shortening (all platforms)

`"shortenLinks": true` shortens links in the caption with the workspace's Bitly account when the post publishes (not on create). Each link gets `utm_source` (the platform) and `utm_medium=social`, plus `utm_campaign` from `utmCampaign` if set. If the workspace has no Bitly connected, or Bitly fails, the post still publishes with the original links and a warning is added to its `logs`.

## Platforms with comments

Reading and replying to comments works for Instagram, Facebook, LinkedIn and Google Business (reviews). Not for X, TikTok, YouTube, Threads, Pinterest or Bluesky.
