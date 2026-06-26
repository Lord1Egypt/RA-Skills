---
name: google-maps-reviews-scraper-apify
description: "Use this skill when the user needs Google Maps reviews from exact places through an Apify actor, including review text, ratings, dates, review URLs, reviewer profile data, owner replies, review context, detailed ratings, and place metadata from Google Maps place URLs, CID URLs, review URLs, or Place IDs."
version: 1.0.0
required_env_vars:
  - APIFY_TOKEN
required-env-vars:
  - APIFY_TOKEN
primary_credential: APIFY_TOKEN
primary-credential: APIFY_TOKEN
metadata:
  short-description: Run Google Maps reviews scraping with Apify
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
        description: Apify API token used to run the Google Maps Reviews Scraper actor.
    primaryCredential: APIFY_TOKEN
    emoji: "⭐"
    homepage: https://github.com/hundevmode/apify-google-maps-reviews-scraper-agent-skill
---

# Google Maps Reviews Scraper Apify Skill

## Overview

This skill helps an AI agent run the Apify Google Maps Reviews Scraper actor for exact-place review extraction.

Default actor:

- Actor ID: `V2kIsQs3Ta9C9kkEt`
- Actor name: `x_guru/google-maps-reviews-scraper`
- Store page: `https://apify.com/x_guru/google-maps-reviews-scraper`

Use this skill when a user asks to:

- export Google reviews from a known Google Maps place
- scrape reviews from Google Maps place URLs, CID URLs, review data URLs, or Place IDs
- collect review text, star ratings, dates, review IDs, and direct review URLs
- include public reviewer profile fields
- collect owner replies, review images, review context, detailed ratings, and place metadata
- build review datasets for local SEO, reputation monitoring, sentiment analysis, competitor research, or BI exports

## Quick Workflow

1. Confirm the user has exact sources: Google Maps place URLs, CID URLs, review URLs, or Place IDs.
2. If the user only has a keyword/location search, run the main Google Maps Scraper first to discover places.
3. Build input with `startUrls` or `placeIds`, `maxReviews`, `reviewsSort`, `language`, and `personalData`.
4. Set `reviewsStartDate` only when the user needs recent reviews.
5. Set a budget guard with Apify `maxTotalChargeUsd` when spend matters.
6. Run `scripts/google_maps_reviews_scraper_actor.py` or call the Apify API directly.
7. Return rows plus a compact summary. Mention `RUN_SUMMARY` for diagnostics.

## Payload Rules

- `startUrls` must be array objects: `[{"url": "https://www.google.com/maps/..."}]`.
- `placeIds` accepts raw Google Place IDs, `place_id:` values, or compatible URLs.
- `maxReviews` is required in practice and should be a positive integer.
- `reviewsSort` must be one of `newest`, `mostRelevant`, `highestRanking`, or `lowestRanking`.
- Use `reviewsSort: "newest"` with `reviewsStartDate`.
- `reviewsStartDate` accepts `YYYY-MM-DD` or relative values such as `8 days`, `3 months`, or `1 year`.
- `reviewsOrigin` should usually be `google`; `all` is accepted for compatibility.
- Set `personalData=false` when the user only needs review text, rating, date, and place metadata.

## Authentication

Use an Apify token:

```bash
export APIFY_TOKEN='apify_api_xxx'
```

Never hardcode or print the full token.

## Script Usage

The bundled script uses only Python standard library.

Run by Place ID:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_reviews_scraper_actor.py quick-place-id \
  --place-id "ChIJ8Q2WSpJZwokRQz-bYYgEskM" \
  --max-reviews 25 \
  --budget-usd 1
```

Run by Google Maps URL:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_reviews_scraper_actor.py quick-url \
  --url "https://www.google.com/maps/place/Joe%27s+Pizza/..." \
  --max-reviews 100 \
  --reviews-sort newest \
  --budget-usd 1
```

Run custom JSON:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_reviews_scraper_actor.py run \
  --input-file references/sample_input.json \
  --budget-usd 1
```

## Input Examples

### Place URL

```json
{
  "startUrls": [
    {
      "url": "https://www.google.com/maps/place/Joe%27s+Pizza/@40.7306597,-74.0021707,17z/data=!3m1!4b1!4m6!3m5!1s0x89c259924a960df1:0x43b20488619b3f43!8m2!3d40.7306597!4d-74.0021707!16s%2Fg%2F1tyyy0n3"
    }
  ],
  "maxReviews": 100,
  "reviewsSort": "newest",
  "language": "en",
  "personalData": true
}
```

### Place ID

```json
{
  "placeIds": ["ChIJ8Q2WSpJZwokRQz-bYYgEskM"],
  "maxReviews": 250,
  "reviewsSort": "mostRelevant",
  "reviewsOrigin": "google",
  "language": "en"
}
```

### Recent Reviews

```json
{
  "placeIds": ["ChIJ8Q2WSpJZwokRQz-bYYgEskM"],
  "maxReviews": 100,
  "reviewsSort": "newest",
  "reviewsStartDate": "3 months",
  "personalData": false
}
```

## Output Contract

The runner returns:

- `ok`
- `actorId`
- `fetchedAt`
- `inputUsed`
- `itemCount`
- `rows[]`

Rows are actor dataset items. Important groups:

- Source: `searchString`, `inputStartUrl`, `inputPlaceId`, `rank`, `searchPageUrl`, `searchPageLoadedUrl`
- Review: `reviewId`, `reviewUrl`, `text`, `textTranslated`, `publishAt`, `publishedAtDate`, `stars`, `rating`, `likesCount`, `reviewOrigin`, `originalLanguage`, `translatedLanguage`
- Owner response: `responseFromOwnerDate`, `responseFromOwnerText`
- Review extras: `reviewImageUrls`, `reviewContext`, `reviewDetailedRating`, `visitedIn`, `isAdvertisement`
- Reviewer: `reviewerId`, `reviewerUrl`, `name`, `reviewerNumberOfReviews`, `isLocalGuide`, `reviewerPhotoUrl`
- Place: `title`, `placeId`, `fid`, `cid`, `kgmid`, `categoryName`, `categories`, `totalScore`, `reviewsCount`, `url`, `imageUrl`, `price`
- Address/runtime: `address`, `city`, `state`, `countryCode`, `location`, `scrapedAt`, `language`

For the full contract, read `references/input-output-contract.md`.

## Agent Response Rules

- If the user provides a broad search URL, explain that this reviews actor needs exact places.
- If no rows are returned, say the run succeeded but no matching reviews were saved, then suggest checking `RUN_SUMMARY`.
- If reviewer profile fields are null, check whether `personalData=false` was used before treating it as missing data.
- If date filtering is active, describe it as best-effort because Google often returns relative dates.
- For large jobs, split by place list and use budget limits.

## References

- `references/input-output-contract.md`
- `references/sample_input.json`
- `references/troubleshooting.md`
