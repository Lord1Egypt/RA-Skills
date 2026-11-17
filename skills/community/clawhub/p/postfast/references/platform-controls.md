# Platform-Specific Controls Reference

All controls are passed in the `controls` object of `POST /social-posts`.

## TikTok

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tiktokTitle` | string | — | Photo-carousel title, max 90 chars. When set, `content` becomes the description. Photo carousels only |
| `tiktokPrivacy` | string | — | **Deprecated, no-op. Don't set it.** TikTok videos publish at the account's default privacy (no per-post control); photos default to public. Use a TikTok app draft (`tiktokIsDraft`) for a private post |
| `tiktokAllowComments` | boolean | `true` | Allow comments |
| `tiktokAllowDuet` | boolean | `true` | Allow duets |
| `tiktokAllowStitch` | boolean | `true` | Allow stitches |
| `tiktokBrandOrganic` | boolean | `false` | Self-promotional content |
| `tiktokBrandContent` | boolean | `false` | Sponsored/partnership content |
| `tiktokAutoAddMusic` | boolean | `false` | Let TikTok add background music. Photo posts only. Mutually exclusive with `tiktokMusicSoundId` (both set returns `tiktokMusic.conflictAutoAddMusic`) |
| `tiktokMusicSoundId` | string | — | A licensed trending track: the `musicSoundId` from `GET /social-media/{id}/tiktok-sounds` (max 128 chars). Photo carousels and videos, Business-API connections only. On a video the track and the original sound each play at 50% volume (no volume or trim controls). Ids rotate daily, so fetch fresh ones per session. Not applied to TikTok app drafts |
| `tiktokMusicSoundName` | string | — | Display-only label for the chosen sound (max 256 chars), never sent to TikTok. Set it whenever `tiktokMusicSoundId` is set |
| `tiktokIsAigc` | boolean | `false` | Labels video as AI-generated. TikTok displays "Creator labeled as AI-generated" tag. Only effective for video posts. Set at creation only |
| `tiktokIsDraft` | boolean | `false` | Pushes the post to the TikTok app's draft inbox so the user finishes editing on their phone. **Not** a PostFast draft state: the post still needs `scheduledAt`. For a regular PostFast draft (any platform, no scheduling), use top-level `status: "DRAFT"` instead and omit `scheduledAt`. |

**Media notes:**
- Video: MP4/MOV, H.264, ≤250MB, 3s-10min. Best: 15-30s, 1080×1920 (9:16)
- Carousels: up to 10 images per photo post (TikTok itself allows 35; PostFast takes 10)
- `coverTimestamp` in mediaItems: milliseconds into video for thumbnail (e.g., `"5000"` = 5 seconds). No custom cover image upload for TikTok
- Caption: max 2,200 characters
- Sound: with neither `tiktokMusicSoundId` nor `tiktokAutoAddMusic`, a photo post publishes silent and a video keeps its own audio

**TikTok Business account:** analytics watch-time, follower history, and `firstComment` all require a TikTok Business account. New connections and reconnects upgrade to Business automatically. On TikTok, `firstComment` is max 1,200 chars and needs comments enabled on the post; an account that can't post comments is rejected with `firstComment.tiktok.notSupported`.

## Instagram

| Parameter | Type | Default | Description |
|---|---|---|---|
| `instagramPublishType` | string | `TIMELINE` | `TIMELINE`, `STORY`, `REEL` |
| `instagramPostToGrid` | boolean | `true` | Show Reel on profile grid |
| `instagramCollaborators` | string[] | `[]` | Usernames (without @), max 3 |
| `instagramTrialReelStrategy` | string | — | Publishes reel as a trial (shown only to non-followers). `MANUAL` = creator graduates via Instagram app. `SS_PERFORMANCE` = auto-graduates after 72h if it performs well. Requires `instagramPublishType: "REEL"`. Cannot be combined with `instagramCollaborators` |
| `instagramLocationId` | string | — | Geotag a single-media post (image/video/reel/story, not carousels) with a place ID from `GET /social-media/search-places`. Same numeric ID as `facebookPlaceId` |
| `instagramLocationName` | string | — | Optional display-only place label. Stored for your dashboard; never sent to Meta |
| `instagramIsAiGenerated` | boolean | `false` | Adds Instagram's "AI info" label to images, videos, reels, stories and carousels (the whole post, not single slides). Set at creation only; it can't be removed after publishing |

**Content types:**
- **TIMELINE**: Feed posts. Single image, carousel (up to 10 images and videos, mixed), or video
- **STORY**: 24-hour temporary content. Image or video
- **REEL**: Short-form video, 3-90 seconds, 9:16 recommended. Gets algorithm boost (2-3x reach vs feed)

**Media notes:**
- Video: 1 per post outside carousels (PostFast's upload cap is 250MB per video)
- Carousels: up to 10 images and videos, mixed, Timeline only
- `instagramCollaborators`: up to 3 usernames. PostFast doesn't check them in advance, and Instagram rejects the post at publish if one is wrong
- Trial reels need a public Professional account with at least 1,000 followers, otherwise Instagram rejects the post at publish
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
- Images: JPG/PNG, up to 10 per post (PostFast's upload cap is 10MB per image)
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
| `youtubeThumbnailKey` | string | — | S3 media key for custom thumbnail image. Upload via `/file/get-signed-upload-urls` first. JPEG/PNG/GIF, max 2MB, recommended 1280x720 (16:9), min width 640px. Requires phone-verified YouTube channel. Set after video uploads; if thumbnail upload fails, video still publishes without it |
| `youtubeContainsSyntheticMedia` | boolean | `false` | Discloses realistic altered or synthetic content to YouTube (sent only when `true`). Set at creation only |
| `youtubeLanguage` | string | — | The video's language as a BCP-47 code (`en`, `en-GB`, `es`, `es-419`, `fr`, `pt-BR`). Sets both YouTube's "Video language" and "Title and description language"; PostFast normalizes the code (`pt-br` becomes `pt-BR`). Unknown code: `400 youtubeLanguage.invalid`. Set at creation only |
| `youtubeCaptionKey` | string | — | Key of an uploaded .srt or .vtt file (`file/{uuid}.srt` or `file/{uuid}.vtt`, from `contentType` `application/x-subrip` or `text/vtt`), added as a caption track in `youtubeLanguage` right after the video uploads. Needs `youtubeLanguage` (`400 youtubeCaptionKey.languageRequired`). One track per video. Set at creation only |

**Media notes:**
- 1 video per post, no images
- Shorts: under 3 minutes, 9:16 or 1:1
- Copyrighted music limits Shorts to 60 seconds
- H.264 video codec with AAC audio recommended

**Text:** the description (`content`) holds up to 5,000 characters. YouTube doesn't allow `<` or `>` in a title or description, and PostFast rejects the post before saving it if either appears. `firstComment` can be up to 10,000 characters.

**Captions:** the file must be timed SRT or WebVTT in plain UTF-8, at most 10MB. Creating the post checks it (`400 media.invalidMedia` when it's missing, empty, over 10MB, or not timed SRT/WebVTT in plain UTF-8; `400 youtubeCaptionKey.invalid` when the key isn't an .srt or .vtt upload, checked on every platform). YouTube's automatic captions stay available separately. If the captions still can't be added when the video publishes, the video publishes without them. If YouTube refuses the language at publish time (rare, since unknown codes stop at creation), the post fails once without retrying, and `lastError.message` reads "YouTube doesn't accept the video language set on this post. Pick another language, or clear it, and try again." Like every control, both keys apply to every post in the request, so videos in different languages go in separate requests.

## LinkedIn

| Parameter | Type | Default | Description |
|---|---|---|---|
| `linkedinAttachmentKey` | string | — | S3 key for document post (from `/file/get-signed-upload-urls`). Format: `file/{uuid}.{ext}` |
| `linkedinAttachmentTitle` | string | `Document` | Display title for document |

**Content types:**
- Regular posts: text + images (up to 10) or 1 video, not mixed
- Document posts: PDF, DOC, DOCX, PPT, PPTX (display as swipeable carousels). Use `linkedinAttachmentKey` instead of `mediaItems`. ≤60MB
- Cannot mix documents with regular media
- Personal profiles and company Pages both work; analytics are available for company Pages only, and `firstComment` isn't supported

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
- Retweets share the original tweet; any content/media provided will be ignored
- Character limit: 280 (4,000 with X Premium)
- Up to 4 images or 1 video per post, not mixed
- **Posting limits (PostFast Fair Usage Policy):** 6 posts per account per day (9 on Pro and Enterprise), plus a daily pool shared by every X account in the organization and a monthly allowance of posts that contain a link:

| Plan | X accounts | Per account/day | Per organization/day | Link posts/month |
|---|---|---|---|---|
| Starter | 2 | 6 | 8 | 14 |
| Creator | 6 | 6 | 14 | 32 |
| Growth | 12 | 6 | 32 | 44 |
| Pro | 36 | 9 | 96 | 60 |
| Enterprise | 45 | 9 | 280 | 120 |

A link in the text or the first comment counts toward the allowance, a link in both counts as two; retweets and link-free posts don't. The allowance resets on the 1st of each month (UTC). Source of truth: https://postfa.st/fair-usage

## Pinterest

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pinterestBoardId` | string | **required** | Board to pin to. Get IDs from `GET /social-media/{id}/pinterest-boards` |
| `pinterestLink` | string | — | Destination URL when pin is clicked |

**Content parsing:**
- First line of `content` → pin title (max 100 chars)
- Remaining lines → pin description (max 800 chars)

**Media notes:**
- One image, one video, or 2-5 static images for a multi-image Pin (no GIFs, no video in carousels)
- Ideal aspect ratio: 2:3 (1000×1500)
- **Cover images for video pins**: Use `coverImageKey` in mediaItems to set a custom cover (JPEG/PNG, up to 8MB). `coverTimestamp` (milliseconds) works as fallback
- Requires a Pinterest Business account. Secret boards work like public ones; boards created after connecting appear after Sync Boards in the dashboard

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
- Up to 10 images (JPEG/PNG/GIF/WebP, 2MB each) or 1 MP4 video (up to 100MB), not both. Posts with 5-10 images show as a gallery; older and some third-party Bluesky apps may show only the text
- Bluesky-hosted accounts must verify their email before the first video upload, and Bluesky caps video uploads per account per day
- No `firstComment`, no reply chains, no per-post analytics
- URLs auto-generate link cards
- No edit after publishing

## Threads

| Parameter | Type | Default | Description |
|---|---|---|---|
| `threadsTopicTag` | string | — | The post's topic on Threads: one per post, 1-50 characters, no `.` or `&` (otherwise `400 threadsTopicTag.invalid`). If the text also has a #hashtag, the topic wins and the hashtag stays plain text. Shared by every post in the request, so posts with different topics go in separate requests |

**Notes:**
- Character limit: 500; `firstComment` up to 500
- One image, one video, or a carousel of up to 10 images and videos, mixed

## Telegram

No platform-specific controls.

**Notes:**
- Character limit: 4,096
- Up to 10 images, videos, or mixed media per post; videos up to 50MB
- Supports channels and groups (the PostFast bot must be an admin)
