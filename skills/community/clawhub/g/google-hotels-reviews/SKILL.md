---
name: google-hotels-reviews
description: "Google Hotels review TEXT is not available through StayingAPI — /v1/reviews returns 400 platform_not_enabled for google. This skill tells an agent what to use instead: the aggregate rating from /v1/search, or reviews from Booking.com, Airbnb or Vrbo. Powered by StayingAPI."
version: "1.0.0"
license: MIT-0
author: StayingAPI
homepage: https://stayingapi.com
repository: https://github.com/stayingapi/google-hotels-skills
user-invocable: true
compatibility: Requires internet access to reach api.stayingapi.com. No additional runtimes or dependencies needed.
required_environment_variables:
  - name: STAYINGAPI_KEY
    prompt: Your StayingAPI key (starts with stay_)
    help: Free key at https://stayingapi.com/signup — no card. A stay_test_ sandbox key returns fixtures at zero cost.
    required_for: all API requests
tags: ["google-hotels", "google-hotels-api", "reviews", "ratings", "travel", "accommodation"]
metadata: {"openclaw":{"emoji":"🚫","requires":{"env":["STAYINGAPI_KEY"]},"primaryEnv":"STAYINGAPI_KEY","homepage":"https://stayingapi.com"},"hermes":{"tags":["google-hotels","google-hotels-api","reviews","ratings","travel","accommodation"],"category":"integrations"}}
---

# Google Hotels reviews — not available (use another platform)

**Google Hotels does not expose review text through StayingAPI.** This skill exists so an agent asked for Google Hotels reviews gives the right answer immediately instead of retrying a call that always fails.

> [!IMPORTANT]
> `GET /v1/reviews?platform=google` returns `400 platform_not_enabled`, and no parameter combination changes that.
> **Aggregate rating IS available:** `GET /v1/search` returns `guestRating`, `ratingScale`, `starRating` and `reviewCount` for Google Hotels properties — enough for "how well rated is this hotel?" (see the `google-hotels-search` skill).
> **For review text**, call `/v1/reviews` with `platform=booking`, `airbnb` or `vrbo` (skills: `booking-com-reviews`, `airbnb-reviews`, `vrbo-reviews`).
> **For Google Hotels pricing**, use `google-hotels-compare`; for discovery, `google-hotels-search`.

## Setup

If `$STAYINGAPI_KEY` is not set, read [references/auth-setup.md](references/auth-setup.md) and follow it to get and store the key. A `stay_test_` sandbox key works for evaluation at zero cost.

## When to use this skill

**DO use when the user asks:**

- "What do reviews say about this Google Hotels place?" — answer that review text is unavailable and offer the alternatives below
- "How well rated is this Google Hotels hotel?" — the aggregate rating comes from /v1/search

**Do NOT use when:**

- You want review text from a platform that supports it — install `booking-com-reviews`, `airbnb-reviews` or `vrbo-reviews`
- You want Google Hotels search or price comparison — use `google-hotels-search` or `google-hotels-compare`

## Required headers

Every request needs:

- **Authorization:** `Bearer $STAYINGAPI_KEY`
- **User-Agent:** your agent's name (e.g. `ClaudeCode/1.0`).

Base URL: `https://api.stayingapi.com/v1`.


## Platform × endpoint support

Not every endpoint supports every platform. Verified:

| platform | search | availability | price | price-compare | listing | reviews |
|---|---|---|---|---|---|---|
| `airbnb` | yes | yes | yes | yes | yes | yes |
| `booking` | yes | yes | yes | yes | yes | yes |
| `vrbo` | yes | yes | yes | yes | yes | yes |
| `google` | yes | yes | yes | yes | **no** | **no** |

`GET /v1/listing/google/…` and `GET /v1/reviews?platform=google` return
`400 platform_not_enabled` ("google is not enabled for this endpoint"). Use `booking`,
`airbnb` or `vrbo` for listing detail and reviews; use `google` for search, price and
cross-OTA price-compare.

## The cross-OTA advantage

StayingAPI is **cross-platform**: Google Hotels data comes back in the *same unified schema* as Airbnb, Booking.com and Vrbo, so one integration covers them all. `/v1/price-compare` resolves a property through the Google Hotels backbone and returns the offers it exposes plus a StayingAPI-computed **min** and **median** over those offers, as first-class fields.

> Coverage varies by property and by what the backbone returns: some properties come back with several OTA offers, others with a single aggregated-lowest offer (in which case `min` equals `median` and `offers` has one entry, sometimes a direct-supplier rate rather than an OTA). Read `offers.length` before describing a result as a multi-platform comparison.

## Async & partial failures

A live call that has to scrape returns `202` with `data.jobId`, `data.pollUrl` and
`data.estimatedSeconds` (the `202` itself charges 0). Poll `GET /v1/jobs/{jobId}` (free)
until `data.status` is TERMINAL — `completed` **or** `failed`.

- **`completed`** → the payload is at `data.result` (the same schema the sync call returns;
  `data` itself is just `{jobId, result, status}`). `meta` carries `partial`,
  `platformResults[]` and `warnings[]`. A completed job may still return an **empty**
  result (`data.result: []`) — the reason is in `meta.warnings[]` (e.g. `no_results`), and
  empty results charge 0.
- **`failed`** → HTTP is still **200**, not an HTTP error. The failure is nested at
  `data.error` (`code`, `type`, `message`, `retryable`). Detect it with
  `data.status === "failed"`, **not** a top-level `error`. `creditsCharged` is 0, and `meta`
  carries only `{requestId, creditsCharged, platforms}` — do **not** read `partial`,
  `platformResults` or `warnings` on a failed job.

Pace your polling: honour the `Retry-After` header, back off between attempts, and cap the
number of attempts. A tight loop hits `429 rate_limit_exceeded` (120 requests/minute).

## Known limitations

- **Pagination:** `limit`/`cursor` are accepted where documented, but availability depends on the endpoint and the upstream source — treat `meta.pagination` as authoritative and stop when `hasMore` is false or `nextCursor` is null.
- **Externally-sourced ids:** a Vrbo id obtained somewhere other than `/v1/search` may not resolve upstream and can produce a failed job (`all_actors_failed`). Prefer ids from `/v1/search` (`platformListingId`).
- **Platform gaps:** see the support matrix above — `google` has no listing or reviews endpoint.

## Credits

Number-free by design — **failed, empty and blocked calls are never billed**, and `stay_test_` sandbox calls are always free. Current costs: <https://stayingapi.com/pricing> · full contract: <https://api.stayingapi.com/openapi.json>.

## Trademark

StayingAPI is an independent service and is not affiliated with, endorsed by, or sponsored by Google Hotels. Google Hotels is a trademark of its respective owner.

---

**Get your free key → https://stayingapi.com/signup** · Docs: https://stayingapi.com/docs
