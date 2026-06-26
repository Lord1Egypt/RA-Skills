# Profiles

List connected social profiles, fetch follower/engagement stats, and enumerate placements (pages, orgs, boards, channels, locations).

## List Profiles
```bash
curl -X GET "https://api.postproxy.dev/api/profiles" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```
Optional query parameter: `profile_group_id` to filter by profile group.

## Get Profile (with latest stats)
Returns the profile fields plus the latest stats snapshot per placement, and a `summary_stats` rollup for placement networks.
```bash
curl -X GET "https://api.postproxy.dev/api/profiles/{profile_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

Response shape:
- `latest_stats` — array of latest snapshots. One entry per placement for placement networks (Facebook/LinkedIn/Telegram); a single entry with `placement_id: null` for non-placement networks (Bluesky, Twitter, Instagram, Threads, YouTube, TikTok, Pinterest). Empty if no snapshots have been recorded yet.
- `latest_stats[].placement_id` — string or `null`.
- `latest_stats[].stats` — platform-specific metrics (see [Profile Stats Fields](#profile-stats-fields)).
- `latest_stats[].recorded_at` — ISO 8601 timestamp.
- `summary_stats` — for placement networks, numeric values summed across the latest snapshot of every placement (non-numeric values like `channel_title` are omitted). `null` for non-placement networks and when no snapshots exist.

Snapshots refresh roughly every 23 hours per profile. If `latest_stats` is empty, the profile is connected but hasn't been polled yet.

## Get Profile Stats (timeseries)
Retrieves the full stats timeseries for a profile. Use this to plot follower growth and engagement trends over time. Snapshots are captured roughly every 23 hours.
```bash
curl -X GET "https://api.postproxy.dev/api/profiles/{profile_id}/stats?placement_id={placement_id}&from=2026-04-01T00:00:00Z&to=2026-05-01T00:00:00Z" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

Query parameters:
- `placement_id` (conditional): **Required** for `facebook`, `linkedin`, and `telegram` profiles. The platform-specific ID returned by [List Placements](#list-placements). Omit (or ignored) for other networks.
- `from` (optional): ISO 8601 — only include snapshots at or after this time.
- `to` (optional): ISO 8601 — only include snapshots at or before this time.

Response shape: `data.profile_id`, `data.platform`, `data.placement_id` (echo of the request, `null` for non-placement networks), and `data.records` — snapshots ordered by `recorded_at` ascending. Each record has `stats` (platform-specific metrics) and `recorded_at`.

Missing `placement_id` for a placement network returns `400`.

For a non-placement network like Bluesky, omit `placement_id`:
```bash
curl -X GET "https://api.postproxy.dev/api/profiles/{profile_id}/stats" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

### Profile Stats Fields

The `stats` object's keys come straight from each platform's API — they are not normalized. A key only appears in a snapshot if the platform returned a value on that polling cycle, so fields can come and go between records.

| Network | Placement-scoped? | Typical fields |
|---------|-------------------|----------------|
| `facebook` | Yes (per page) | `fan_count`, `followers_count`, plus daily page insights (`page_impressions`, `page_views_total`, `page_fan_adds`, `page_fan_removes`, …) |
| `linkedin` | Yes (per organization) | `followerCount`, `shareCount`, `likeCount`, `commentCount`, `clickCount`, `engagement`, `allPageViews`, `overviewPageViews`, `aboutPageViews`, `careersPageViews`, `peoplePageViews`, `insightsPageViews` |
| `telegram` | Yes (per channel) | `followers_count`, `channel_title`, `channel_username` |
| `instagram` | No | `followers_count`, `follows_count`, `media_count`, `reach`, `profile_views`, `accounts_engaged`, `total_interactions`, `website_clicks`, `follower_count` |
| `threads` | No | `followers_count`, `views`, `likes`, `replies`, `reposts`, `quotes` |
| `youtube` | No | `subscriberCount`, `viewCount`, `videoCount` |
| `twitter` | No | `followers_count`, `following_count`, `tweet_count`, `listed_count`, `like_count` |
| `tiktok` | No | `follower_count`, `following_count`, `likes_count`, `video_count` |
| `pinterest` | No | `follower_count`, `following_count`, `pin_count`, `board_count`, `monthly_views`, `analytics_30d` |
| `bluesky` | No | `followersCount`, `followsCount`, `postsCount` |

Notes:
- Non-numeric fields (e.g. Telegram's `channel_title`) appear in `latest_stats[].stats` but are omitted from `summary_stats.stats`, which sums numeric values only.
- LinkedIn page-view metrics are filtered to rollups only (redundant mobile/desktop splits and dead sections like `productsPageViews` / `lifeAtPageViews` are dropped).

## List Placements
Retrieves available placements for a profile. For Facebook: business pages. For LinkedIn: personal profile and organizations. For Pinterest: boards. For Telegram: channels the bot has been added to as administrator. For Google Business: locations (full resource path `accounts/X/locations/Y`). Available for `facebook`, `linkedin`, `pinterest`, `telegram`, and `google_business` profiles.

If no placement is specified when creating a post: LinkedIn defaults to personal profile, Facebook defaults to a random connected page, Pinterest fails, Telegram fails (`chat_id` is always required), Google Business fails (`location_id` is always required).
```bash
curl -X GET "https://api.postproxy.dev/api/profiles/{profile_id}/placements" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

Response is a `data` array of placement objects with `id` (string, or `null` for the LinkedIn personal profile) and `name`. For Telegram, the placement `id` is the `chat_id` to pass in `platforms.telegram.chat_id` when creating a post. The Telegram list is empty until the user adds the bot as administrator to a channel — poll after connecting the bot.

## Webhook Events
- `profile.connected` / `profile.disconnected` — profile connection state changed
- `profile.stats` — a new stats snapshot was recorded

See [webhooks.md](webhooks.md) for subscription setup.
