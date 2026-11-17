---
name: postlake-analytics
description: Read social media performance from PostLake: per-post results and normalised cross-platform analytics (impressions, reach, engagement, CTR, follower growth). Use to report on results or decide what to post next.
---

# PostLake: analytics

Two views: a single post's performance, and normalised cross-platform analytics
over a period so an agent can compare networks and decide what to post next.

## Auth

```
Authorization: Bearer $POSTLAKE_API_KEY
```

Base URL `https://api.postlake.dev`.

## Per-post analytics

```bash
curl https://api.postlake.dev/v1/posts/POST_ID/analytics \
 -H "Authorization: Bearer $POSTLAKE_API_KEY"
```

Returns per-platform metrics for that post (impressions, likes, comments, shares,
saves, clicks (whatever the platform exposes), in one normalised shape.

## Cross-platform analytics

```bash
curl "https://api.postlake.dev/v1/analytics?period=30d" \
 -H "Authorization: Bearer $POSTLAKE_API_KEY"
```

`period` is `7d`, `30d` (default), or `90d`. Returns totals plus a per-platform
breakdown (impressions, reach, engagement rate, CTR, saves, and follower growth) 
already normalised so you can benchmark networks against each other.

## How to use it well

- When asked "how did X do?", fetch per-post analytics and summarise the strongest
 metric per platform.
- When asked "what should I post next?", pull cross-platform analytics, find which
 network + content type has the best engagement/CTR, and recommend accordingly.
- Metrics are as fresh as each platform reports; some lag a few hours after posting.
