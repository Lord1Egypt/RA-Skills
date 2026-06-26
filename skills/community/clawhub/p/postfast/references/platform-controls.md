# Platform-Specific Controls Reference

All controls are passed in the `controls` object of `POST /social-posts`.

## TikTok

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tiktokTitle` | string | — | Photo-carousel title, max 90 chars. When set, `content` becomes the description. Photo carousels only |
| `tiktokPrivacy` | string | `PUBLIC` | `PUBLIC`, `MUTUAL_FRIENDS`, `FOLLOWER_OF_CREATOR`, `ONLY_ME` |
| `tiktokAllowComments` | boolean | `true` | Allow comments |
| `tiktokAllowDuet` | boolean | `true` | Allow duets |
| `tiktokAllowStitch` | boolean | `true` | Allow stitches |
| `tiktokBrandOrganic` | boolean | `false` | Self-promotional content |
| `tiktokBrandContent` | boolean | `false` | Sponsored/partnership content |
| `tiktokAutoAddMusic` | boolean | `false` | Auto-add background music |
| `tiktokIsAigc` | boolean | `false` | Labels video as AI-generated. TikTok displays "Creator labeled as AI-generated" tag. Only effective for video posts |
| `tiktokIsDraft` | boolean | `false` | Pushes the post to the TikTok app's draft inbox so the user finishes editing on their phone. **Not** a PostFast draft state — the post still needs `scheduledAt`. For a regular PostFast draft (any platform, no scheduling), use top-level `status: "DRAFT"` instead and omit `scheduledAt`. |

**Media notes:**
- Video: MP4/MOV, H.264, ≤250MB, 3s-10min. Best: 15-30s, 1080×1920 (9:16)
- Carousels: 2-35 images (photo slideshows)
- `coverTimestamp` in mediaItems: milliseconds into video for thumbnail (e.g., `"5000"` = 5 seconds). No custom cover image upload for TikTok
- Caption: max 2,200 characters

## Instagram

| Parameter | Type | Default | Description |
|---|---|---|---|
| `instagramPublishType` | string | `TIMELINE` | `TIMELINE`, `STORY`, `REEL` |
| `instagramPostToGrid` | boolean | `true` | Show Reel on profile grid |
| `instagramCollaborators` | string[] | `[]` | Usernames (without @), max 3 |
| `instagramTrialReelStrategy` | string | — | Publishes reel as a trial (shown only to non-followers). `MANUAL` = creator graduates via Instagram app. `SS_PERFORMANCE` = auto-graduates after 72h if it performs well. Requires `instagramPublishType: "REEL"`. Cannot be combined with `instagramCollaborators` |
| `instagramLocationId` | string | — | Geotag a single-media post (image/video/reel/story, not carousels) with a place ID from `GET /social-media/search-places`. Same numeric ID as `facebookPlaceId` |
| `instagramLocationName` | string | — | Optional display-only place label. Stored for your dashboard; never sent to Meta |

**Content types:**
- **TIMELINE**: Feed posts. Single image, carousel (up to 10), or video
- **STORY**: 24-hour temporary content. Image or video
- **REEL**: Short-form video, 3-90 seconds, 9:16 recommended. Gets algorithm boost (2-3x reach vs feed)

**Media notes:**
- Video: ≤1GB for Reels
- Carousels: up to 10 images or videos
- **Cover images for Reels**: Use `coverImageKey` in mediaItems to set a custom cover (JPEG only, max 8MB). Upload the image via the standard 3-step flow first. `coverTimestamp` (milliseconds) works as fallback

## Facebook

| Parameter | Type | Default | Description |
|---|---|---|---|
| `facebookContentType` | string | `POST` | `POST`, `REEL`, `STORY` |
| `facebookReelsCollaborators` | string[] | `[]` | Facebook usernames for Reel collaboration |
| `facebookPlaceId` | string | — | Geotag a feed post (text/photo/carousel, not Reels/Stories/video) with a place ID from `GET /social-media/search-places`. Same numeric ID as `instagramLocationId` |
| `facebookPlaceName` | string | — | Optional display-only place label. Stored for your dashboard; never sent to Meta |
| `facebookTargetCountries` | string[] | — | Restrict a feed post to up to 25 ISO 3166-1 alpha-2 country codes (case-insensitive). Audience gating: hidden from everyone else and from logged-out users. Combinable with `facebookPlaceId` |

**Content types:**
- **POST**: Permanent feed content. Up to 10 images OR 1 video (not mixed). Text limit: 63,206 chars
- **REEL**: Short-form vertical video, 1 video only
- **STORY**: 24-hour temporary content, 1 image or 1 video

**Media notes:**
- Images: JPG/PNG, ≤30MB each, up to 10 per post
- Cannot mix images and videos in same post
- **Cover images for Reels**: Use `coverImageKey` in mediaItems to set a custom cover (any format, max 10MB). Upload the image via the standard 3-step flow first. `coverTimestamp` is NOT supported for Facebook Reels

**Geotagging & targeting (feed posts only):** Resolve a place with `GET /social-media/search-places`, then set `facebookPlaceId` (optionally `facebookPlaceName` for a display label). Optionally add `facebookTargetCountries` to limit the audience by country. All three are rejected on Reels, Stories, and video posts. See SKILL.md "Pattern 11" for the full flow.

## YouTube

| Parameter | Type | Default | Description |
|---|---|---|---|
| `youtubeIsShort` | boolean | `true` | Publish as YouTube Short |
| `youtubeTitle` | string | — | Video title (max 100 chars). Falls back to first 100 chars of content |
| `youtubePrivacy` | string | `PUBLIC` | `PUBLIC`, `UNLISTED`, `PRIVATE` |
| `youtubePlaylistId` | string | — | Add to playlist after publishing. Get IDs from `GET /social-media/{id}/youtube-playlists` |
| `youtubeMadeForKids` | boolean | `false` | COPPA compliance flag |
| `youtubeTags` | string[] | `[]` | Video tags |
| `youtubeCategoryId` | string | — | YouTube category ID |
| `youtubeThumbnailKey` | string | — | S3 media key for custom thumbnail image. Upload via `/file/get-signed-upload-urls` first. JPEG/PNG/GIF/BMP/WebP, max 2MB, recommended 1280x720 (16:9), min width 640px. Requires phone-verified YouTube channel. Set after video uploads; if thumbnail upload fails, video still publishes without it |

**Media notes:**
- Shorts: up to 3 minutes, 9:16 or 1:1
- Copyrighted music limits Shorts to 60 seconds
- H.264 video codec with AAC audio recommended

## LinkedIn

| Parameter | Type | Default | Description |
|---|---|---|---|
| `linkedinAttachmentKey` | string | — | S3 key for document post (from `/file/get-signed-upload-urls`). Format: `file/{uuid}.{ext}` |
| `linkedinAttachmentTitle` | string | `Document` | Display title for document |

**Content types:**
- Regular posts: text + images (up to 9) or video (up to 10 min)
- Document posts: PDF, PPTX, DOCX (display as swipeable carousels). Use `linkedinAttachmentKey` instead of `mediaItems`. ≤60MB
- Cannot mix documents with regular media

**Tips:**
- Character limit: 3,000 (under 1,300 performs better)
- Put links in comments, not post body (LinkedIn deprioritizes external links)
- 3-5 hashtags max

## X (Twitter)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `xRetweetUrl` | string | — | URL of tweet to retweet without changes. Content and media are ignored |

**URL formats accepted:** `x.com`, `twitter.com`, `mobile.twitter.com`. Example: `https://x.com/username/status/1234567890`

**Important:**
- Retweets share the original tweet — any content/media provided will be ignored
- Character limit: 280
- Up to 4 images per post
- **API limit: 5 posts per account per day** — exceeding risks account restrictions

## Pinterest

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pinterestBoardId` | string | **required** | Board to pin to. Get IDs from `GET /social-media/{id}/pinterest-boards` |
| `pinterestLink` | string | — | Destination URL when pin is clicked |

**Content parsing:**
- First line of `content` → pin title (max 100 chars)
- Remaining lines → pin description (max 800 chars)

**Media notes:**
- Ideal aspect ratio: 2:3 (1000×1500)
- Carousels: 2-5 static images only (no video in carousels)
- **Cover images for video pins**: Use `coverImageKey` in mediaItems to set a custom cover (JPEG/PNG). `coverTimestamp` (milliseconds) works as fallback

## Google Business Profile

| Parameter | Type | Default | Description |
|---|---|---|---|
| `gbpLocationId` | string | **required** | Location resource name from `GET /social-media/{id}/gbp-locations` |
| `gbpTopicType` | string | `STANDARD` | `STANDARD`, `EVENT`, or `OFFER` |
| `gbpCallToActionType` | string | — | `BOOK`, `ORDER`, `SHOP`, `LEARN_MORE`, `SIGN_UP`, or `CALL` |
| `gbpCallToActionUrl` | string | — | URL for the CTA button. Not needed for `CALL`. Ignored for OFFER posts |
| `gbpEventTitle` | string | — | Title for EVENT/OFFER posts (max 58 chars). Defaults to first line of content |
| `gbpEventStartDate` | string (ISO 8601) | — | Required for EVENT and OFFER posts |
| `gbpEventEndDate` | string (ISO 8601) | — | Required for EVENT and OFFER posts |
| `gbpOfferCouponCode` | string | — | Coupon code (OFFER only) |
| `gbpOfferRedeemUrl` | string | — | Redemption URL (OFFER only) |
| `gbpOfferTerms` | string | — | Terms and conditions (OFFER only) |

**Post types:**
- **STANDARD**: General business update with optional CTA button
- **EVENT**: Promotes a time-bound event. Requires `gbpEventTitle`, `gbpEventStartDate`, `gbpEventEndDate`
- **OFFER**: Promotes a deal/discount. Requires `gbpEventTitle`, `gbpEventStartDate`, `gbpEventEndDate`. Optionally add coupon code, redeem URL, and terms

**Media notes:**
- 1 image only (no video, no carousel)
- JPEG/PNG, max 5MB
- Caption: max 1,500 characters

**Limits:**
- 5 posts per account per day
- Standard posts expire after 6 months. Event/Offer posts expire at end date

## Bluesky

No platform-specific controls.

**Notes:**
- Character limit: 300
- Up to 4 images
- No video support via API
- URLs auto-generate link cards
- No edit after publishing

## Threads

No platform-specific controls.

**Notes:**
- Text + images + video supported
- Carousels: up to 10 images

## Telegram

No platform-specific controls.

**Notes:**
- Character limit: 4,096
- Up to 10 images, videos, or mixed media per post
- Supports channels and groups
