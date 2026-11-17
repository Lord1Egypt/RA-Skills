---
name: instagram-followers-scraper
description: Extract follower lists from public Instagram profiles through Apify. Use when a user asks who follows one or more Instagram accounts or needs follower usernames and public profile fields; do not use for following lists, Stories, Highlights, posts, or comments.
metadata:
  openclaw:
    requires:
      env:
        - APIFY_TOKEN
      bins:
        - curl
        - jq
    primaryEnv: APIFY_TOKEN
    emoji: "👥"
    homepage: https://datavoyantlab.com/agent-skills/instagram
---

# Instagram Followers Scraper

Use DataVoyantLab's Instagram Followers Scraper on Apify to return public
follower accounts and the profile fields available in the Actor dataset.

This skill uses a paid external service on Apify. It requires a paid Apify
account or an approved DataVoyantLab Free-user entitlement.

The requested usernames are sent to Apify to perform the scrape. Tell the user
this before execution. Never send the Apify token anywhere except the documented
Apify API.

## Actor contract

- Actor ID: `TESQ47dR6CqaVdLh8`
- Store page: <https://apify.com/datavoyantlab/instagram-followers-scraper>
- Input: `{"usernames": ["natgeo"]}`
- Maximum: 10 usernames per run
- Billing events: Actor start plus each follower item written to the dataset
- Default maximum charge: 5 USD

Do not use this Actor to find accounts that the target follows. That is the
`instagram-following-scraper` skill.

## Prepare the request

1. Require `APIFY_TOKEN` and never display or persist it.
2. Accept usernames, `@username` values, or Instagram profile URLs.
3. Normalize to usernames, remove duplicates, and reject empty values.
4. Stop if more than 10 unique usernames remain.
5. Construct JSON with `jq` and include:

```json
{
  "skill": true,
  "skillName": "instagram-followers-scraper",
  "skillVersion": "1.0.1"
}
```

## Verify pricing and set the cap

Fetch `https://api.apify.com/v2/acts/TESQ47dR6CqaVdLh8`. Select the latest
active entry in `.data.pricingInfos`, then read:

- `minimalMaxTotalChargeUsd`;
- the Actor-start event price;
- `follower-item-fetched.eventPriceUsd`.

Use the budget explicitly supplied by the user. Otherwise use 5 USD. Reject a
user budget below `minimalMaxTotalChargeUsd`; never silently raise it.

Estimate the maximum result count as:

```text
floor((maximum charge - Actor-start price) / follower-item price)
```

Treat this as an estimate, not a promised result count. If the active pricing or
required events cannot be read, do not start the run.

## Get explicit approval

Before every billable run, show the user:

- the Instagram Followers Scraper Actor and validated usernames;
- the current Actor-start and per-follower prices;
- the estimated maximum result count;
- the proposed charge cap, using the user's budget or proposing 5 USD; and
- that the Apify account linked to `APIFY_TOKEN` will be billed.

Ask the user to explicitly approve that exact charge cap. A request for
followers is not payment authorization. Do not start the run without an
affirmative reply. If the usernames, pricing, or cap change, recalculate and ask
again.

## Run asynchronously

Start:

```text
POST https://api.apify.com/v2/acts/TESQ47dR6CqaVdLh8/runs
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

Return:

- all retrieved follower items;
- run ID and dataset ID;
- the requested usernames;
- the applied maximum charge;
- whether the result may be partial because the charge limit was reached.

Do not claim a complete follower list when the charge cap stopped collection.
For a failed terminal status, return the public status and run ID without
revealing private implementation details.

If Apify rejects an unapproved Free account, tell the user to email
`datavoyant@gmail.com` with their Apify user ID to request access.
