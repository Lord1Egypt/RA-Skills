---
name: propertyguru-sg-sale-browser-crawl
description: extract around 50 Singapore for-sale listings from a PropertyGuru search results URL using a real browser session after Cloudflare verification. use when the target is a PropertyGuru Singapore search page, direct HTTP fetch may return 403, the reliable source is `window.__NEXT_DATA__.props.pageProps.pageData.data.listingsData`, and results should be deduplicated by listing id across sequential pages until the target count is reached.
license: MIT-0
metadata: { "openclaw": { "emoji": "🏘️", "homepage": "https://www.propertyguru.com.sg/property-for-sale?listingType=sale&page=1&isCommercial=false&maxPrice=1400000" } }
---

# PropertyGuru SG Sale Browser Crawl

Use this skill for PropertyGuru Singapore search results pages when the job is to collect roughly 50 listing cards from one filtered search URL.

This target is browser-backed.

- A direct fetch may return a Cloudflare verification page or `403`.
- Prefer a real browser session and extract from the page's hydrated Next.js data.
- Do not treat DOM card scraping as the primary source when `__NEXT_DATA__` is available.

## Required skill

This skill depends on `playwright`.

- Use a real browser page.
- Let the browser complete PropertyGuru's Cloudflare verification first.
- Only extract after the page title and result page content have loaded.

## Workflow

1. Read `{baseDir}/references/source-notes.md`.
2. Start from the user-provided search URL. If no URL is supplied, use the default URL from the source notes.
3. Open the page in a real browser.
4. Wait until the search results page is actually loaded, not the initial verification screen.
5. Read `window.__NEXT_DATA__.props.pageProps.pageData`.
6. Use `pageData.data.listingsData` as the canonical listing collection for that page.
7. For each item in `listingsData`, use `listingData.id` as the stable dedupe key.
8. Preserve the raw `listingData` object whenever possible.
9. Optionally add lightweight wrapper fields such as:
   - `source_url`
   - `page`
   - `collected_at`
   - `listing_id`
10. Continue page-by-page until one of these conditions is met:
   - 50 unique listings have been collected
   - `paginationData.currentPage >= paginationData.totalPages`
   - `listingsData` is empty
   - the next page repeats only ids already seen
11. For the default PropertyGuru URL observed on March 18, 2026, the page payload contained 25 listings per page, so pages 1 and 2 were enough to reach 50 listings.

## Canonical data location

Prefer:

```js
window.__NEXT_DATA__.props.pageProps.pageData.data.listingsData
```

Related pagination data:

```js
window.__NEXT_DATA__.props.pageProps.pageData.data.paginationData
```

Useful search context:

```js
window.__NEXT_DATA__.props.pageProps.pageData.searchParams
```

## Recommended extraction shape

Prefer keeping the raw listing payload plus a few convenience fields:

```json
{
  "source_url": "https://www.propertyguru.com.sg/property-for-sale?listingType=sale&page=1&isCommercial=false&maxPrice=1400000",
  "page": 1,
  "collected_at": "2026-03-18T04:40:00Z",
  "listing_id": 500044843,
  "raw": {
    "id": 500044843,
    "localizedTitle": "780B Woodlands Crescent",
    "url": "https://www.propertyguru.com.sg/listing/hdb-for-sale-780b-woodlands-crescent-500044843",
    "price": {
      "value": 500000,
      "pretty": "S$ 500,000"
    },
    "bedrooms": 2,
    "bathrooms": 2
  }
}
```

If the caller wants a flatter convenience export, these fields are usually available:

- `listingData.id`
- `listingData.localizedTitle`
- `listingData.url`
- `listingData.price.value`
- `listingData.price.pretty`
- `listingData.area.localeStringValue`
- `listingData.bedrooms`
- `listingData.bathrooms`
- `listingData.fullAddress`
- `listingData.property`
- `listingData.psfText`
- `listingData.postedOn`
- `listingData.agent`
- `listingData.agency`
- `listingData.mrt`
- `listingData.isVerified`

## Operating rules

- Use browser extraction as the default path.
- Do not rely on `curl`, plain HTTP, or static HTML parsing as the primary strategy.
- Do not scrape promo widgets, "Explore around" cards, or other injected recommendation blocks from the visible DOM.
- Use only `listingsData` for the main dataset.
- Crawl one page at a time.
- Deduplicate strictly on `listingData.id`.
- Stop as soon as the requested target count is reached.
- Preserve the search URL and page number with every saved record.
- If the page falls back to a Cloudflare challenge and does not recover, report the block explicitly instead of pretending the page is empty.

## Output target

Default target: about 50 unique listings.

- Prefer pages 1 and 2 first.
- If one page returns fewer rows than expected, continue to page 3 and beyond until the target count is reached.

## Notes

- PropertyGuru may change the page structure, build id, or anti-bot behavior at any time.
- When the page changes, re-check `__NEXT_DATA__` before changing extraction logic.
- For this skill, the in-page Next.js payload is more stable than card-by-card DOM parsing.
