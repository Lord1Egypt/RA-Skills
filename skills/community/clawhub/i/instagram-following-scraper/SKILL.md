---
name: instagram-following-scraper
description: Extract the accounts followed by public Instagram profiles through Apify. Use when a user asks who an Instagram account follows or needs following-list usernames and public profile fields; do not use for follower lists, Stories, Highlights, posts, or comments.
metadata:
  openclaw:
    requires:
      env:
        - APIFY_TOKEN
      bins:
        - curl
        - jq
    primaryEnv: APIFY_TOKEN
    emoji: "🔎"
    homepage: https://datavoyantlab.com/agent-skills/instagram
---

# Instagram Following Scraper

Use DataVoyantLab's Instagram Following Scraper on Apify to return the public
accounts followed by one or more Instagram profiles.

This skill uses a paid external service on Apify. It requires a paid Apify
account or an approved DataVoyantLab Free-user entitlement.

The requested usernames are sent to Apify to perform the scrape. Tell the user
this before execution. Never send the Apify token anywhere except the documented
Apify API.

## Actor contract

- Actor ID: `xDzzMiRH9Ha4YgBUy`
- Store page: <https://apify.com/datavoyantlab/instagram-following-scraper>
- Input: `{"usernames": ["natgeo"]}`
- Maximum: 50 usernames per run
- Billing events: Actor start plus each following item written to the dataset
- Default maximum charge: 5 USD

Do not use this Actor to find who follows the target. That is the
`instagram-followers-scraper` skill.

## Prepare the request

1. Require `APIFY_TOKEN` and never display or persist it.
2. Accept usernames, `@username` values, or Instagram profile URLs.
3. Normalize to usernames, remove duplicates, and reject empty values.
4. Stop if more than 50 unique usernames remain.
5. Construct JSON with `jq` and include:

```json
{
  "skill": true,
  "skillName": "instagram-following-scraper",
  "skillVersion": "1.0.1"
}
```

## Verify pricing and set the cap

Fetch `https://api.apify.com/v2/acts/xDzzMiRH9Ha4YgBUy`. Select the latest
active entry in `.data.pricingInfos`, then read:

- `minimalMaxTotalChargeUsd`;
- the Actor-start event price;
- `following-item-fetched.eventPriceUsd`.

Use the budget explicitly supplied by the user. Otherwise use 5 USD. Reject a
user budget below `minimalMaxTotalChargeUsd`; never silently raise it.

Estimate the maximum result count as:

```text
floor((maximum charge - Actor-start price) / following-item price)
```

Treat this as an estimate. The actual public following list can be smaller. If
the active price or required events cannot be read, do not start the run.

## Get explicit approval

Before every billable run, show the user:

- the Instagram Following Scraper Actor and validated usernames;
- the current Actor-start and per-following-item prices;
- the estimated maximum result count;
- the proposed charge cap, using the user's budget or proposing 5 USD; and
- that the Apify account linked to `APIFY_TOKEN` will be billed.

Ask the user to explicitly approve that exact charge cap. A request for a
following list is not payment authorization. Do not start the run without an
affirmative reply. If the usernames, pricing, or cap change, recalculate and ask
again.

## Run asynchronously

Start:

```text
POST https://api.apify.com/v2/acts/xDzzMiRH9Ha4YgBUy/runs
  ?waitForFinish=60
  &maxTotalChargeUsd=<user budget or 5>
Authorization: Bearer $APIFY_TOKEN
Content-Type: application/json
```

Poll `GET /v2/actor-runs/<run ID>?waitForFinish=60` until terminal status. On
`SUCCEEDED`, retrieve:

```text
GET /v2/actor-runs/<run ID>/dataset/items?clean=true&format=json
```

Run only after the approval above.

## Return

Return all retrieved items, run ID, dataset ID, requested usernames, applied
maximum charge, and whether the result may be partial because the charge limit
was reached.

Do not claim completeness when the cap stopped collection. For a failed terminal
status, return the public status and run ID without disclosing private
implementation details.

If Apify rejects an unapproved Free account, tell the user to email
`datavoyant@gmail.com` with their Apify user ID to request access.
