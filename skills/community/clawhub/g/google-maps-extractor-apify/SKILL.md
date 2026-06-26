---
name: google-maps-extractor-apify
description: "Use this skill when the user needs Google Maps place and business data through an Apify actor, including Google Places data, local business listings, addresses, websites, phones, ratings, review counts, opening hours, coordinates, Place IDs, CIDs, Google Maps URLs, and optional public website contact enrichment from keywords, URLs, Place IDs, or map areas."
version: 1.0.0
required_env_vars:
  - APIFY_TOKEN
required-env-vars:
  - APIFY_TOKEN
primary_credential: APIFY_TOKEN
primary-credential: APIFY_TOKEN
metadata:
  short-description: Run Google Maps extraction with Apify
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
        description: Apify API token used to run the Google Maps Extractor actor.
    primaryCredential: APIFY_TOKEN
    homepage: https://github.com/hundevmode/apify-google-maps-extractor-agent-skill
---

# Google Maps Extractor Apify Skill

## Overview

This skill helps an AI agent run the Apify Google Maps Extractor actor for Google Maps place data, local business listings, and optional public website contact enrichment.

Default actor:

- Actor ID: `2A4RTA5PjN7McqJXx`
- Actor name: `x_guru/google-maps-extractor`
- Store page: `https://apify.com/x_guru/google-maps-extractor`
- Console source: `https://console.apify.com/actors/2A4RTA5PjN7McqJXx/source`

Use this skill when a user asks to:

- collect Google Maps places by search term and location
- scrape Google Maps search URLs or direct place URLs
- enrich known Google Place IDs
- build local business lead lists with websites, phones, addresses, ratings, coordinates, Place IDs, and CIDs
- extract public business website contacts such as emails, extra phone numbers, and social links
- create Google Maps datasets for local SEO, competitor research, store locator data, CRM enrichment, Sheets, n8n, Airtable, or API workflows

## Quick Workflow

1. Clarify the business type, location, desired count, and whether add-ons are needed.
2. Build the smallest useful payload first.
3. Use `searchStringsArray`, `locationQuery`, `maxCrawledPlacesPerSearch`, and `language` for normal search.
4. Use `startUrls` or `placeIds` for exact known sources.
5. Enable paid add-ons only when needed: filters, place details, or website contacts.
6. Set a budget guard with Apify `maxTotalChargeUsd` when spend matters.
7. Run `scripts/google_maps_extractor_actor.py` or call the Apify API directly.
8. Return compact summary metrics and dataset rows. Check `RUN_SUMMARY` for diagnostics.

## Payload Rules

- Standard discovery uses `searchStringsArray`, `locationQuery`, and `maxCrawledPlacesPerSearch`.
- Exact Google Maps URLs use `startUrls` as objects: `[{"url": "https://www.google.com/maps/..."}]`.
- Exact Google Place IDs use `placeIds`.
- Direct URLs and Place IDs can run without `locationQuery`.
- Structured search area uses `countryCode`, `city`, `state`, `county`, `postalCode`, `customGeolocation`, and `strictLocationBounds`.
- `locationQuery` has priority when it is present and specific.
- Broad visible-map collection uses `allPlacesNoSearchAction="all_visible"` and optional `allPlacesZoom`; use it only for concrete local areas.
- Paid filters include `categoryFilterWords`, `placeCategories`, `searchMatching`, `placeMinimumStars`, `website`, and `skipClosedPlaces`.
- Use `scrapeContacts` only when the user needs public website emails, phones, or social links.
- Use `scrapePlaceDetailPage` when the user needs richer opening hours, menu links, plus code, popular times, inside places, web results, or detailed place metadata.
- Place details can be extended with `scrapeTableReservationProvider`, `scrapeOrderOnline`, `includeWebResults`, and `scrapeDirectories`.
- Keep initial tests small: 10-50 places before scaling.

## Authentication

Use the Apify API token from the environment:

```bash
export APIFY_TOKEN='apify_api_xxx'
```

Never hardcode or print the full token in user-facing output.

## Script Usage

The bundled script uses only Python standard library.

Run a quick search:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_extractor_actor.py quick-search \
  --query "bike repair shop" \
  --location "Portland, Oregon, USA" \
  --limit 25 \
  --budget-usd 1
```

Run with public website contact enrichment:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_extractor_actor.py quick-search \
  --query "roofing contractor" \
  --location "Denver, Colorado, USA" \
  --limit 50 \
  --with-contacts \
  --only-with-website \
  --budget-usd 2
```

Run by Google Maps URL:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_extractor_actor.py quick-url \
  --url "https://www.google.com/maps/search/restaurants+near+New+York,+NY" \
  --limit 50 \
  --budget-usd 1
```

Run by Place ID:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_extractor_actor.py quick-place-id \
  --place-id "ChIJN1t_tDeuEmsRUsoyG83frY4" \
  --details \
  --budget-usd 1
```

Run custom JSON:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_extractor_actor.py run \
  --input-file references/sample_input.json \
  --budget-usd 1
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

### Contact lead generation

```json
{
  "searchStringsArray": ["roofing contractor"],
  "locationQuery": "Denver, Colorado, USA",
  "maxCrawledPlacesPerSearch": 50,
  "website": "withWebsite",
  "scrapeContacts": true
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

## Output Contract

The runner returns JSON:

- `ok`
- `actorId`
- `fetchedAt`
- `inputUsed`
- `itemCount`
- `rows[]`

Rows are actor dataset items. Important groups:

- Identity: `title`, `subTitle`, `description`, `price`, `categoryName`, `categories`, `rank`, `isAdvertisement`
- Address: `address`, `street`, `city`, `state`, `postalCode`, `countryCode`, `location`, `plusCode`
- Contacts: `website`, `phone`, `phoneUnformatted`, `emails`, `additionalPhones`, social profile arrays
- Ratings: `totalScore`, `reviewsCount`, `reviewsDistribution`, `reviewsTags`
- Details: `openingHours`, `popularTimesHistogram`, `menu`, `servicesLink`, `reserveTableUrl`, `googleFoodUrl`, `peopleAlsoSearch`, `placesTags`
- Google IDs: `placeId`, `fid`, `cid`, `kgmid`, `url`, `searchPageUrl`, `searchPageLoadedUrl`
- Runtime: `searchString`, `language`, `scrapedAt`

For the full contract, read `references/input-output-contract.md`.

## Agent Response Rules

- If rows are empty, say the run succeeded but no matching places were saved, then suggest checking `RUN_SUMMARY`.
- If contact fields are empty, first check whether `scrapeContacts` was enabled.
- If detail fields are missing, first check whether `scrapePlaceDetailPage` was enabled.
- Explain missing fields as normal best-effort behavior when Google Maps or the business website does not expose data.
- Use `maxTotalChargeUsd` for any user concerned about spend.
- Do not promise review rows or large image lists from this extractor. Use the separate Google Maps Reviews Scraper for review datasets.

## References

- `references/input-output-contract.md`
- `references/sample_input.json`
- `references/troubleshooting.md`
