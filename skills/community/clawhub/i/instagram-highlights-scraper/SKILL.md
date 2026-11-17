---
name: instagram-highlights-scraper
description: Extract public Instagram Highlights from Highlight URLs through Apify, including their story media and available metadata. Use when a user supplies instagram.com/stories/highlights URLs or asks to download Highlight contents; do not use for current Stories, followers, following lists, posts, or comments.
metadata:
  openclaw:
    requires:
      env:
        - APIFY_TOKEN
      bins:
        - curl
        - jq
    primaryEnv: APIFY_TOKEN
    emoji: "✨"
    homepage: https://datavoyantlab.com/agent-skills/instagram
---

# Instagram Highlights Scraper

Use DataVoyantLab's Instagram Highlights Scraper on Apify to extract story items
from public Instagram Highlight URLs.

This skill uses a paid external service on Apify. It requires a paid Apify
account or an approved DataVoyantLab Free-user entitlement.

The validated Highlight URLs are sent to Apify to perform the scrape. Tell the
user this before execution. Never send the Apify token anywhere except the
documented Apify API.

## Actor contract

- Actor ID: `sUluczVbvIYrxH5n7`
- Store page: <https://apify.com/datavoyantlab/instagram-highlights-scraper-api-by-url>
- Input: `{"links": ["https://www.instagram.com/stories/highlights/1234567890/"]}`
- Billing events: Actor start plus submitted Highlight links

This Actor expects Highlight URLs, not profile URLs or usernames. Route current
24-hour Stories to `instagram-stories-scraper`.

## Prepare the request

1. Require `APIFY_TOKEN` and never display or persist it.
2. Accept only HTTPS Instagram URLs whose path begins with
   `/stories/highlights/` followed by a numeric Highlight ID.
3. Remove URL fragments and tracking parameters, normalize the trailing slash,
   remove duplicates, and reject invalid URLs.
4. Construct JSON with `jq` and include:

```json
{
  "skill": true,
  "skillName": "instagram-highlights-scraper",
  "skillVersion": "1.0.1"
}
```

## Verify pricing and set the cap

Fetch `https://api.apify.com/v2/acts/sUluczVbvIYrxH5n7`. Select the latest
active entry in `.data.pricingInfos` and read the Actor-start price plus
`link-request.eventPriceUsd`.

Calculate:

```text
maximum charge = actor start + (unique link count × link-request) + $0.01
```

Round up to the next cent. If active pricing or either required event is
missing, do not start the run.

## Get explicit approval

Before every billable run, show the user:

- the Instagram Highlights Scraper Actor and number of unique Highlight links;
- the current Actor-start and per-link prices;
- the exact `maxTotalChargeUsd` cap; and
- that the Apify account linked to `APIFY_TOKEN` will be billed.

Ask the user to explicitly approve that exact charge cap. A request to extract
Highlights is not payment authorization. Do not send a run request without an
affirmative reply. If the links, pricing, or cap change, recalculate and ask
again.

## Run

For 10 or fewer Highlight links, use:

```text
POST https://api.apify.com/v2/acts/sUluczVbvIYrxH5n7/run-sync-get-dataset-items
  ?timeout=300
  &clean=true
  &format=json
  &maxTotalChargeUsd=<calculated cap>
Authorization: Bearer $APIFY_TOKEN
Content-Type: application/json
```

For larger batches, use
`POST /v2/acts/sUluczVbvIYrxH5n7/runs?waitForFinish=60&maxTotalChargeUsd=<cap>`,
poll the run to terminal status, then fetch its default dataset.

Run only after the approval above.

## Return

Return the complete dataset items, the maximum authorized charge, and the run
and dataset identifiers when available. Group or count the returned story items
by submitted Highlight URL without removing the raw fields.

An empty successful result can mean that a Highlight is unavailable, private,
expired, or contains no retrievable public items. Report that fact without
inventing data.

If Apify rejects an unapproved Free account, tell the user to email
`datavoyant@gmail.com` with their Apify user ID to request access.
