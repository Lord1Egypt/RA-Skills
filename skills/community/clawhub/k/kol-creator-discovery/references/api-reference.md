# WaveInflu API Reference

Use both endpoints through AIsa with bearer authentication:

```text
Authorization: Bearer $AISA_API_KEY
Content-Type: application/json
Base URL: https://api.aisa.one/apis/v1
```

## Email Lookup

```http
POST /waveinflu/email-lookup
```

Request:

```json
{
  "url": "https://www.instagram.com/onkimia/"
}
```

Supported profile platforms: TikTok, Instagram, YouTube.

Important response fields:

- `data.platform`, `data.username`, `data.profileLink`, `data.platformUserId`
- `data.region`
- `data.email`: primary email or `null`
- `data.emails`: all unique emails
- `data.contacts`: external contact links
- `data.quota.cost`, `data.quota.remainingQuota`

## Similar Creators

```http
POST /waveinflu/similar
```

Request:

```json
{
  "platform": "youtube",
  "limit": 10,
  "seedProfileUrl": "https://www.youtube.com/@mkbhd",
  "contentDirection": "consumer tech creators covering AI apps and honest product reviews",
  "filters": {
    "regions": ["US", "GB"],
    "languages": ["en"],
    "minFollowers": 10000,
    "maxFollowers": 500000,
    "minVideosAverageViews": 5000,
    "maxVideosAverageViews": 250000
  }
}
```

Rules:

- `platform` is required and accepts `youtube` or `tiktok`.
- `limit` defaults to 25 and accepts 1–100.
- `seedProfileUrl` accepts a YouTube or TikTok creator profile.
- `contentDirection` accepts up to 800 characters.
- Supply at least `seedProfileUrl` or `contentDirection`.
- For an Instagram seed, omit `seedProfileUrl` and require a user-supplied `contentDirection` plus target platform.

Important response fields:

- `data.requestId`, `data.platform`, `data.mode`, `data.total`
- `data.data[]`: matched creators, already sorted by `similarityScore`
- Creator fields: `username`, `platform`, `platformHandle`, `channelId`, `channelTitle`, `description`, `email`, `profileUrl`, `avatar`, `similarityScore`, `followerCount`, `averagePlayCount`, `averageLikeCount`, `lastPublishedTime`, `region`, `language`
- `data.quota`: total, used, remaining, reserved, charged, and refunded quota

## Failure Semantics

- A missing email is `Not found`, not an error.
- A failed HTTP call is `Lookup failed`; preserve the error without aborting other creator enrichments.
- Do not infer contact data from usernames, domains, or other creators.
