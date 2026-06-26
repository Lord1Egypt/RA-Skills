# PostFast Skill Examples

Ready-to-use request bodies for common social media scheduling scenarios.

## Examples Index

| File | Description |
|------|-------------|
| [cross-platform-post.json](cross-platform-post.json) | Post same content to LinkedIn, X, and Threads |
| [tiktok-video.json](tiktok-video.json) | TikTok video with privacy and brand settings |
| [tiktok-carousel.json](tiktok-carousel.json) | TikTok image carousel (2-35 images) |
| [tiktok-aigc-video.json](tiktok-aigc-video.json) | TikTok AI-generated video with AIGC label and follower-only privacy |
| [draft-post.json](draft-post.json) | **PostFast draft** (any platform): `status: "DRAFT"` + no `scheduledAt`. Saved in PostFast, scheduled later by the user. |
| [tiktok-app-draft.json](tiktok-app-draft.json) | **TikTok app draft** (`tiktokIsDraft: true`): pushes the post to the TikTok app's draft inbox. Different from a PostFast draft — still needs `scheduledAt`. |
| [instagram-reel.json](instagram-reel.json) | Instagram Reel with collaborators |
| [instagram-reel-cover.json](instagram-reel-cover.json) | Instagram Reel with custom cover image |
| [instagram-story.json](instagram-story.json) | Instagram Story (video) |
| [instagram-carousel.json](instagram-carousel.json) | Instagram carousel (up to 10 images) |
| [instagram-trial-reel.json](instagram-trial-reel.json) | Instagram trial reel (shown to non-followers first) |
| [facebook-reel.json](facebook-reel.json) | Facebook Reel with custom cover image |
| [facebook-story.json](facebook-story.json) | Facebook Story (image) |
| [youtube-short.json](youtube-short.json) | YouTube Short with tags and playlist |
| [youtube-video-thumbnail.json](youtube-video-thumbnail.json) | YouTube video with custom thumbnail image |
| [pinterest-pin.json](pinterest-pin.json) | Pinterest pin with board and destination link |
| [linkedin-document.json](linkedin-document.json) | LinkedIn document/carousel post (PDF) |
| [x-retweet.json](x-retweet.json) | X scheduled retweet (content ignored) |
| [x-first-comment.json](x-first-comment.json) | X post with automatic first comment |
| [threads-carousel.json](threads-carousel.json) | Threads image carousel (up to 10) |
| [batch-scheduling.json](batch-scheduling.json) | Schedule 5 posts across a week |
| [telegram-mixed-media.json](telegram-mixed-media.json) | Telegram post with mixed media |
| [gbp-standard.json](gbp-standard.json) | Google Business Profile standard update with CTA |
| [gbp-event.json](gbp-event.json) | Google Business Profile event post |
| [gbp-offer.json](gbp-offer.json) | Google Business Profile offer with coupon code |
| [facebook-geotag.json](facebook-geotag.json) | Facebook feed post geotagged with a place (`facebookPlaceId`) and limited to specific countries |
| [instagram-geotag.json](instagram-geotag.json) | Instagram single-media post geotagged with a place (`instagramLocationId`) |
| [post-analytics.json](post-analytics.json) | Fetch published post metrics (impressions, likes, etc.) |
| [pinterest-analytics.json](pinterest-analytics.json) | Pinterest pin analytics with extras (pin_clicks, outbound_clicks, save_rate, video metrics) |

## Usage

Each JSON file is a complete request body for `POST /social-posts`. Replace placeholder IDs with real values from `GET /social-media/my-social-accounts`.

For examples with media, complete the 3-step upload flow first (see [references/upload-flow.md](../references/upload-flow.md)) and replace the `key` values with your actual upload keys.
