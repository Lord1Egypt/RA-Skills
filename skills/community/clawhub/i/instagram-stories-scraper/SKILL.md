---
name: instagram-stories-scraper
description: Scrape current public Instagram Stories by username through Apify, including media URLs and rich story metadata. Use when a user needs live Stories, story downloads, mentions, links, music, locations, or paid-partnership signals; do not use for Highlights, followers, following lists, posts, or comments.
metadata:
  openclaw:
    requires:
      env:
        - APIFY_TOKEN
      bins:
        - curl
        - jq
    primaryEnv: APIFY_TOKEN
    emoji: "📖"
    homepage: https://datavoyantlab.com/agent-skills/instagram
---

# Instagram Stories Scraper

Use DataVoyantLab's Advanced Instagram Stories Scraper on Apify. It retrieves
current Stories from public profiles and returns the complete dataset response,
including available photo or video URLs, timestamps, mentions, link stickers,
music, locations, and paid-partnership metadata.

This skill uses a paid external service on Apify. It requires a paid Apify
account or an approved DataVoyantLab Free-user entitlement.

The requested usernames are sent to Apify to perform the scrape. Tell the user
this before execution. Never send the Apify token anywhere except the documented
Apify API.

## Actor contract

- Actor ID: `dLL7b34nRrgN6ZV24`
- Store page: <https://apify.com/datavoyantlab/advanced-instagram-stories-scraper>
- Input: `{"usernames": ["natgeo"]}`
- Maximum: 100 usernames per run
- Billing events: Actor start plus each submitted username

Do not route Highlight URLs, follower lists, following lists, posts, reels, or
comments to this Actor.

## Prepare the request

1. Require `APIFY_TOKEN`. Never print it, place it in a URL, or write it to a
   file.
2. Accept usernames, `@username` values, or Instagram profile URLs.
3. Convert each value to a username, trim whitespace, remove a leading `@`,
   preserve periods and underscores, remove duplicates, and reject empty values.
4. Stop if more than 100 unique usernames remain.
5. Construct JSON with `jq`; never interpolate user input into JSON manually.
6. Add these attribution fields:

```json
{
  "skill": true,
  "skillName": "instagram-stories-scraper",
  "skillVersion": "1.0.1"
}
```

## Verify pricing and set the cap

Fetch the public Actor record before every run:

```bash
curl -fsS "https://api.apify.com/v2/acts/dLL7b34nRrgN6ZV24"
```

From `.data.pricingInfos`, select the most recent entry whose `startedAt` is
not in the future. Read:

- `apify-actor-start.eventPriceUsd`, falling back to `actor-run.eventPriceUsd`;
- `username-request.eventPriceUsd`.

Calculate:

```text
maximum charge = actor start + (username count × username-request) + $0.01
```

Round up to the next cent and pass the result as `maxTotalChargeUsd`. If the
active price or either required event is missing, do not start the run.

## Get explicit approval

Before every billable run, show the user:

- the Advanced Instagram Stories Scraper Actor and validated usernames;
- the current Actor-start and per-username prices;
- the exact `maxTotalChargeUsd` cap; and
- that the Apify account linked to `APIFY_TOKEN` will be billed.

Ask the user to explicitly approve that exact charge cap. A request for Stories
is not payment authorization. Do not send a run request without an affirmative
reply. If the usernames, pricing, or cap change, recalculate and ask again.

## Run

For 10 or fewer usernames, use the synchronous dataset endpoint:

```text
POST https://api.apify.com/v2/acts/dLL7b34nRrgN6ZV24/run-sync-get-dataset-items
  ?timeout=300
  &clean=true
  &format=json
  &maxTotalChargeUsd=<calculated cap>
Authorization: Bearer $APIFY_TOKEN
Content-Type: application/json
```

For 11–100 usernames, start asynchronously:

```text
POST https://api.apify.com/v2/acts/dLL7b34nRrgN6ZV24/runs
  ?waitForFinish=60
  &maxTotalChargeUsd=<calculated cap>
```

Poll `GET /v2/actor-runs/<run ID>?waitForFinish=60` until the status is
`SUCCEEDED`, `FAILED`, `ABORTED`, or `TIMED-OUT`. On success, retrieve
`GET /v2/actor-runs/<run ID>/dataset/items?clean=true&format=json`.

Run only after the approval above.

## Return

Return:

- the complete dataset items, not only a summary;
- the maximum authorized charge;
- the run ID and dataset ID when using the asynchronous path;
- a short count by requested username.

An empty result is valid when a public profile currently has no active Stories.
Do not label an empty successful dataset as an Actor failure.

For `FAILED`, `ABORTED`, or `TIMED-OUT`, return the public run status and
run ID. Do not expose internal implementation details from logs.

If Apify reports that Free access is not enabled, tell the user to email
`datavoyant@gmail.com` with their Apify user ID to request an entitlement.
