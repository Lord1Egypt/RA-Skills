---
name: google-maps-scraper-apify
description: Use this skill when the user needs Google Maps business data through an Apify actor, including local business leads, place URLs, Place IDs, websites, phones, addresses, coordinates, reviews, images, opening hours, and optional website contact enrichment.
version: 1.0.0
required_env_vars:
  - APIFY_TOKEN
required-env-vars:
  - APIFY_TOKEN
primary_credential: APIFY_TOKEN
primary-credential: APIFY_TOKEN
metadata:
  short-description: Run Google Maps scraping with Apify
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
        description: Apify API token used to run the Google Maps Scraper actor.
    primaryCredential: APIFY_TOKEN
    emoji: "🗺️"
    homepage: https://github.com/hundevmode/apify-google-maps-scraper-agent-skill
---

# Google Maps Scraper Apify Skill

## Overview

This skill helps an AI agent run the Apify Google Maps Scraper actor for local business collection and enrichment.

Default actor:
- Actor ID: `kLdarP5qiTvc9CwtP`
- Actor name: `x_guru/google-maps-scraper`
- Store page: `https://apify.com/x_guru/google-maps-scraper`

Use this skill when a user asks to:
- collect Google Maps places by search term and location
- scrape direct Google Maps search URLs or place URLs
- enrich existing Google Place IDs
- build local lead lists with websites, phones, addresses, ratings, and coordinates
- add public website contact extraction
- extract Google Maps reviews or images
- create Apify-ready JSON payloads for n8n, CRM, Sheets, or API workflows

## Quick Workflow

1. Clarify the target: business type, location, desired count, and whether add-ons are needed.
2. Build the smallest useful payload first.
3. Set a budget guard with Apify `maxTotalChargeUsd` when the user cares about spend.
4. Run the actor through `scripts/google_maps_scraper_actor.py` or the Apify API.
5. Return summary metrics and dataset rows.
6. Explain missing fields as normal best-effort behavior when Google Maps or the business website does not expose data.

## Payload Rules

- Standard discovery uses `searchStringsArray`, `locationQuery`, and `maxCrawledPlacesPerSearch`.
- Exact Google Maps URLs use `startUrls` as objects: `[{"url": "https://www.google.com/maps/..."}]`.
- Exact Google Place IDs use `placeIds`.
- Structured search area uses `countryCode`, `city`, `state`, `county`, `postalCode`, `customGeolocation`, and `strictLocationBounds`; `locationQuery` has priority when present.
- Broad visible-map collection uses `allPlacesNoSearchAction="all_visible"` and optional `allPlacesZoom`; use it only for concrete local areas.
- Paid filters include `placeCategories`, `customPlaceCategories`, `searchMatching`, `minStars`, `website`, and `skipClosedPlaces`.
- Use `scrapeCompanyContacts` only when the user needs public website emails, phones, or social links.
- Use `maxReviews` only when the user explicitly needs review rows or review fields.
- Use `maxImages` only when the user needs image URLs beyond the main image.
- Use `scrapePlaceDetailPage` for richer opening hours, menu links, plus code, inside places, web results, and detailed place metadata.
- Place details can be extended with `scrapeTableReservationProviderData`, `scrapeOrderOnlineWidgetData`, `includeWebResults`, and `scrapeInsidePlaces`.
- Image extraction can be extended with `scrapeImageAuthors`.
- Keep initial tests small: 10-50 places before scaling.

## Authentication

Use the Apify API token from the environment:

```bash
export APIFY_TOKEN='apify_api_xxx'
```

Never hardcode or print the full token in user-facing output.

## Script Usage

Install requirements if your runtime expects a requirements step:

```bash
pip install -r requirements.txt
```

Run a quick search:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_scraper_actor.py quick-search \
  --query "bike repair shop" \
  --location "Portland, Oregon, USA" \
  --limit 25 \
  --budget-usd 1
```

Run with reviews:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_scraper_actor.py quick-search \
  --query "dentist" \
  --location "Austin, Texas, USA" \
  --limit 20 \
  --reviews 10 \
  --reviews-sort newest \
  --budget-usd 1
```

Run with website contacts:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_scraper_actor.py quick-search \
  --query "roofing contractor" \
  --location "Denver, Colorado, USA" \
  --limit 50 \
  --with-contacts \
  --only-with-website \
  --budget-usd 2
```

Run a custom payload:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_scraper_actor.py run \
  --input-file references/sample_input.json \
  --budget-usd 2
```

## Recommended Inputs

### Local business discovery

```json
{
  "searchStringsArray": ["bike repair shop"],
  "locationQuery": "Portland, Oregon, USA",
  "maxCrawledPlacesPerSearch": 100,
  "language": "en"
}
```

### Exact URLs

```json
{
  "startUrls": [
    {
      "url": "https://www.google.com/maps/search/restaurants+near+New+York,+NY"
    }
  ],
  "maxCrawledPlacesPerSearch": 100,
  "language": "en"
}
```

### Place IDs

```json
{
  "placeIds": ["ChIJN1t_tDeuEmsRUsoyG83frY4"],
  "maxCrawledPlacesPerSearch": 1,
  "scrapePlaceDetailPage": true
}
```

## Add-on Fields

- `scrapePlaceDetailPage`: extra place details.
- `scrapeCompanyContacts`: website contact enrichment.
- `maxReviews`: reviews per place.
- `reviewsStartDate`: optional `YYYY-MM-DD` review date filter.
- `reviewsSort`: `newest`, `mostRelevant`, `highestRanking`, or `lowestRanking`.
- `reviewsFilterString`: keyword filter for review text.
- `reviewsOrigin`: `all` or `google`.
- `scrapeReviewsPersonalData`: include reviewer profile data when allowed.
- `maxImages`: additional image URLs per place.

## Output Contract

The runner returns JSON with:
- `ok`
- `actorId`
- `fetchedAt`
- `inputUsed`
- `itemCount`
- `rows[]`

Rows are actor dataset items. Common fields include:
Core identity:
- `title`
- `subTitle`
- `description`
- `price`
- `categoryName`
- `categories`
- `rank`
- `isAdvertisement`

Address and geography:
- `address`
- `neighborhood`
- `street`
- `city`
- `state`
- `postalCode`
- `countryCode`
- `location`
- `locatedIn`
- `floor`
- `plusCode`

Contacts and web presence:
- `website`
- `phone`
- `phoneUnformatted`
- `emails`
- `additionalPhones`
- `facebooks`
- `instagrams`
- `linkedIns`
- `twitters`
- `youtubes`
- `tiktoks`

Ratings, reviews, and media:
- `totalScore`
- `reviewsCount`
- `reviewsDistribution`
- `reviews`
- `reviewsScraped`
- `reviewsFetchStatus`
- `reviewsFetchMethod`
- `reviewsDateFilterStatus`
- `imageUrl`
- `images`
- `imagesCount`
- `imageFetchStatus`
- `imageFetchMethod`
- `imageAuthorsStatus`
- `imageCategories`

Details and identifiers:
- `openingHours`
- `additionalOpeningHours`
- `popularTimesLiveText`
- `popularTimesLivePercent`
- `popularTimesHistogram`
- `menu`
- `servicesLink`
- `reserveTableUrl`
- `googleFoodUrl`
- `peopleAlsoSearch`
- `placesTags`
- `reviewsTags`
- `gasPrices`
- `hotelStars`
- `hotelDescription`
- `hotelAds`
- `placeId`
- `fid`
- `cid`
- `kgmid`
- `url`
- `searchPageUrl`
- `searchPageLoadedUrl`
- `searchString`
- `language`
- `scrapedAt`
- `additionalInfo`

The hosted actor output page also exposes:
- dataset link: `results`
- run diagnostics link: `summary`, pointing to `RUN_SUMMARY`

## Agent Response Rules

- If a run succeeds with zero rows, say that the actor finished but Google Maps returned no matching places for the requested input.
- If add-on fields are missing, explain that they are best-effort and depend on Google Maps or the business website exposing data.
- For lead generation requests, recommend `scrapeCompanyContacts` plus `website=withWebsite` when the user needs emails.
- For large jobs, split by city, keyword, or area and use budget limits per run.
- For compliance-sensitive review workflows, turn `scrapeReviewsPersonalData` off unless the user explicitly needs reviewer profile fields.

## References

- `references/actor-input-guide.md`
- `references/sample_input.json`
- `references/troubleshooting.md`
