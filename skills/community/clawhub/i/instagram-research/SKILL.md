---
name: instagram-research
description: Researches Instagram profiles, posts, and Reels via the Crawlora API, returning clean JSON. Use when the user wants a public Instagram profile's stats, a specific post's media/engagement, or a user's Reels feed — instead of scraping the app.
---

# Instagram research

Look up public Instagram profiles, posts, and Reels — all as normalized JSON
from the Crawlora API, no app scraping or unofficial client libraries.

## When to use this skill

- "What's <username>'s Instagram profile / follower count?"
- "Pull the details for this Instagram post."
- "Get <username>'s recent Reels."
- Competitor social audits, influencer vetting, or brand-mention monitoring
  scoped to Instagram.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Profile** — `/instagram/profile/{username}` returns public profile
   details for a given Instagram username.
2. **Reels** — `/instagram/reels/{id}` returns a feed of Reels for an
   Instagram user ID, paginated via the optional `max_id` cursor.
3. **Post detail** — `/instagram/post/{id}/{post_id}` returns the media
   details of a specific post, keyed by Instagram user ID and post ID.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Profile:
scripts/crawlora.sh /instagram/profile/nasa | jq '.'

# Reels feed (paginate with max_id from the previous response):
scripts/crawlora.sh /instagram/reels/528817151 | jq '.'
scripts/crawlora.sh /instagram/reels/528817151 max_id=<cursor> | jq '.'

# Post detail (requires both the user ID and the post ID):
scripts/crawlora.sh /instagram/post/528817151/3123456789012345678 | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Instagram
endpoint this skill uses.

## Examples

- **Influencer vetting:** profile + Reels feed to check follower count,
  posting cadence, and content mix before a partnership.
- **Competitor social audit:** pull a competitor's profile stats and recent
  Reels to gauge follower growth and content strategy over time.
- **Post-level engagement check:** given a known post URL, extract the user
  ID and post ID, then call `/instagram/post/{id}/{post_id}` for that post's
  media details.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public profiles/posts; no login, no private content.
  Respect Instagram's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Numeric user ID, not username, for Reels and post lookups** —
  `/instagram/reels/{id}` and `/instagram/post/{id}/{post_id}` both key off
  Instagram's internal numeric user ID, not the `@username`; get it from the
  `/instagram/profile/{username}` response first if you only have a handle.
- **Narrow public surface** — this skill covers profile lookup, Reels feed,
  and single-post detail only; there is no keyword/hashtag search or
  trending endpoint for Instagram.
- **Reels pagination** is cursor-based via `max_id` — follow the cursor
  returned in the response to walk beyond the first page.
