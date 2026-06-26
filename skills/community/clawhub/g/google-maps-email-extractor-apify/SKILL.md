---
name: google-maps-email-extractor-apify
description: "Use this skill when the user needs public business email leads from Google Maps through an Apify actor, including emails, email details, websites, phones, social profiles, ratings, addresses, coordinates, Google Place IDs, CIDs, and Google Maps URLs from keywords, locations, Google Maps URLs, Place IDs, categories, or map areas."
version: 1.0.0
required_env_vars:
  - APIFY_TOKEN
required-env-vars:
  - APIFY_TOKEN
primary_credential: APIFY_TOKEN
primary-credential: APIFY_TOKEN
metadata:
  short-description: Run Google Maps email lead extraction with Apify
  openclaw:
    requires:
      env:
        - APIFY_TOKEN
      bins:
        - python3
    primaryEnv: APIFY_TOKEN
    envVars:
      - name: APIFY_TOKEN
        required: true
        description: Apify API token used to run the Google Maps Email Extractor actor.
    primaryCredential: APIFY_TOKEN
    emoji: "📩"
    homepage: https://github.com/hundevmode/apify-google-maps-email-extractor-agent-skill
---

# Google Maps Email Extractor Apify Skill

## Overview

This skill helps an AI agent run the Apify Google Maps Email Extractor actor for public business email lead generation from Google Maps.

Default actor:

- Actor ID: `f3dlnXVnBc6v8JMNK`
- Actor name: `x_guru/google-maps-email-extractor`
- Store page: `https://apify.com/x_guru/google-maps-email-extractor`
- Console source: `https://console.apify.com/actors/f3dlnXVnBc6v8JMNK/source`

Use this skill when a user asks to:

- build local business email lead lists from Google Maps
- find public emails for dentists, roofers, lawyers, photographers, gyms, clinics, restaurants, contractors, agencies, real estate offices, or other local niches
- enrich Google Maps places with websites, emails, phones, social links, ratings, reviews count, addresses, and coordinates
- run Google Maps searches by keyword and location with `emailsOnly` output
- run exact Google Maps URLs or Google Place IDs and return email lead rows
- control Apify spend with `maxTotalChargeUsd`
- export rows for Sheets, Airtable, n8n, CRM, BI, CSV, JSON, or agent workflows

## Quick Workflow

1. Clarify the niche, location, desired saved email lead count, and whether person-like emails are allowed.
2. Build a small payload first with `searchStringsArray`, `locationQuery`, `maxCrawledPlacesPerSearch`, `contactResultMode: "emailsOnly"`, `website: "withWebsite"`, and `language`.
3. Use `startUrls` or `placeIds` when the user already has exact Google Maps sources.
4. Increase `contactPagesLimit` only when a niche hides emails on team, staff, legal, imprint, or contact pages.
5. Use category/rating/website filters when the search is broad or noisy.
6. Set a budget guard with Apify `maxTotalChargeUsd` when spend matters.
7. Run `scripts/google_maps_email_extractor_actor.py` or call the Apify API directly.
8. Return compact metrics and email lead rows. Check `RUN_SUMMARY` for diagnostics when counts are lower than requested.

## Payload Rules

- Standard search uses `searchStringsArray`, `locationQuery`, `maxCrawledPlacesPerSearch`, and `language`.
- Default saved-output mode is `contactResultMode: "emailsOnly"`.
- Use `website: "withWebsite"` for email extraction because public emails usually come from business websites.
- `maxCrawledPlacesPerSearch` is the requested saved lead target. The actor may scan more Google Maps candidates internally to find enough email leads.
- `contactPagesLimit` defaults to `2`; use `3-5` for deeper email discovery.
- `includePersonalData=false` keeps mostly generic company contacts such as `info@`, `sales@`, `hello@`, and `contact@`.
- `startUrls` must be array objects: `[{"url": "https://www.google.com/maps/..."}]`.
- `placeIds` accepts raw Google Place IDs and compatible `place_id:` values.
- `contactResultMode` must be `emailsOnly`, `contactsOnly`, or `allPlaces`.
- Paid filters include `categoryFilterWords`, `placeCategories`, `customPlaceCategories`, `searchMatching`, `placeMinimumStars`, `website`, and `skipClosedPlaces`.
- Search area can use `locationQuery`, `countryCode`, `city`, `state`, `county`, `postalCode`, `customGeolocation`, `locationBounds`, or `strictLocationBounds`.
- Do not use review-row fields such as `maxReviews` here. Use the Google Maps Reviews Scraper skill for reviews.

## Authentication

Use the Apify API token from the environment:

```bash
export APIFY_TOKEN='apify_api_xxx'
```

Never hardcode or print the full token in user-facing output.

## Script Usage

The bundled script uses only Python standard library.

Run a quick email-lead search:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_email_extractor_actor.py quick-search \
  --query "wedding photographer" \
  --location "Austin, Texas, USA" \
  --limit 25 \
  --budget-usd 1
```

Run by Google Maps URL:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_email_extractor_actor.py quick-url \
  --url "https://www.google.com/maps/search/roofing+contractor+Dallas,+TX" \
  --limit 50 \
  --budget-usd 1
```

Run by Place ID:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_email_extractor_actor.py quick-place-id \
  --place-id "ChIJE2Flwy-1RIYRWqJr_ZiMGc" \
  --budget-usd 1
```

Run custom JSON:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_email_extractor_actor.py run \
  --input-file references/sample_input.json \
  --budget-usd 1
```

## Recommended Inputs

### Local email leads

```json
{
  "searchStringsArray": ["wedding photographer"],
  "locationQuery": "Austin, Texas, USA",
  "maxCrawledPlacesPerSearch": 100,
  "contactResultMode": "emailsOnly",
  "contactPagesLimit": 2,
  "includePersonalData": true,
  "website": "withWebsite",
  "skipClosedPlaces": true,
  "language": "en"
}
```

### Generic company emails only

```json
{
  "searchStringsArray": ["commercial electrician"],
  "locationQuery": "Denver, Colorado, USA",
  "maxCrawledPlacesPerSearch": 100,
  "contactResultMode": "emailsOnly",
  "includePersonalData": false,
  "website": "withWebsite"
}
```

### Exact sources

```json
{
  "startUrls": [
    {
      "url": "https://www.google.com/maps/search/marketing+agency+near+Chicago,+IL"
    }
  ],
  "maxCrawledPlacesPerSearch": 50,
  "contactResultMode": "emailsOnly",
  "website": "withWebsite"
}
```

## Output Contract

The runner returns JSON:

- `ok`
- `actorId`
- `fetchedAt`
- `inputUsed`
- `itemCount`
- `rows[]`

Rows are actor dataset items. Important groups:

- Business: `title`, `categoryName`, `categories`, `rank`, `searchString`
- Emails: `emails`, `emailDetails.email`, `emailDetails.type`, `emailDetails.sourceUrl`, `emailDetails.domainMatch`
- Contacts: `website`, `phone`, `phoneUnformatted`, `additionalPhones`, social profile arrays
- Address: `address`, `street`, `city`, `state`, `postalCode`, `countryCode`, `location`, `plusCode`
- Google metrics: `totalScore`, `reviewsCount`, `reviewsDistribution`, closed flags
- Google IDs: `placeId`, `fid`, `cid`, `kgmid`, `url`, `searchPageUrl`
- Diagnostics: `contactSignals`, `contactStatus`, `additionalInfo.companyContacts`, `scrapedAt`

For the full contract, read `references/input-output-contract.md`.

## Agent Response Rules

- If rows are empty, say the run succeeded but no email leads were saved, then suggest checking `RUN_SUMMARY`.
- If fewer rows than requested are returned, explain that the niche/area had fewer public emails or the budget/filter stopped saving.
- If `emails` is empty in `contactsOnly` or `allPlaces`, explain that the row was saved due to other contact data.
- Explain public email extraction as best-effort because each business controls what its website publishes.
- Use `maxTotalChargeUsd` for any user concerned about spend.
- Do not promise review text or full review datasets from this actor. Use the separate Google Maps Reviews Scraper for reviews.

## References

- `references/input-output-contract.md`
- `references/sample_input.json`
- `references/troubleshooting.md`
