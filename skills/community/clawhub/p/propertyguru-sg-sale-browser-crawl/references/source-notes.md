# Source Notes

## Default target

Primary evaluated URL:

`https://www.propertyguru.com.sg/property-for-sale?listingType=sale&page=1&isCommercial=false&maxPrice=1400000`

This file contains PropertyGuru Singapore specific notes for that search flow.

## Observed behavior on March 18, 2026

- Initial navigation may show a Cloudflare verification page with title `Just a moment...`.
- A real browser session was able to pass verification and load the actual result page.
- The loaded page title was `Houses for Sale - Below S$ 1.4M, Mar 2026`.
- The search results were available in Next.js hydration data under `window.__NEXT_DATA__`.

## Canonical extraction source

Observed page path:

`window.__NEXT_DATA__.props.pageProps.pageData`

Observed listing collection:

`window.__NEXT_DATA__.props.pageProps.pageData.data.listingsData`

Observed pagination object:

`window.__NEXT_DATA__.props.pageProps.pageData.data.paginationData`

Observed search params object:

`window.__NEXT_DATA__.props.pageProps.pageData.searchParams`

## Observed page-level facts

On the evaluated result set:

- `resultCount`: `22564`
- page 1 `listingsData.length`: `25`
- page 2 `listingsData.length`: `25`
- page 2 `paginationData.currentPage`: `2`
- page 2 `paginationData.totalPages`: `1129`

For a 50-listing collection target, pages 1 and 2 were sufficient.

## Observed listing payload shape

Each `listingsData[]` item currently contains top-level keys such as:

- `metadata`
- `listingData`
- `verifiedListingBadgeConfig`
- `hideTooltipConfig`
- `cardConfig`
- `ga`
- `segment`
- `gaProduct`
- `listingCardV2Config`

The canonical fields for the dataset are inside `listingData`.

Observed `listingData` fields included:

- `id`
- `statusCode`
- `typeCode`
- `isVerified`
- `agent`
- `agency`
- `psfText`
- `listingFeatures`
- `property`
- `fullAddress`
- `localizedTitle`
- `mediaItems`
- `mrt`
- `price`
- `url`
- `recency`
- `thumbnail`
- `typeText`
- `postedOn`
- `area`
- `pricePerArea`
- `bedrooms`
- `bathrooms`

## Example observed records

Page 1 examples:

- `500044843` `780B Woodlands Crescent` `S$ 500,000`
- `500049151` `34 Cassia Crescent` `S$ 750,000`
- `25365142` `367 Woodlands Avenue 5` `S$ 778,000`
- `500076088` `Treasure at Tampines` `S$ 1,250,000`

Page 2 examples:

- `500072831` `126 Pasir Ris Street 11` `S$ 699,999`
- `500025294` `348C Yishun Avenue 11` `S$ 950,000`
- `500014669` `169 Lorong 1 Toa Payoh` `S$ 408,000`
- `60164488` `476 Jurong West Street 41` `S$ 418,000`

## Practical guidance

- Use sequential pagination.
- Prefer page URL navigation by changing the `page` query param.
- After each navigation, re-read `window.__NEXT_DATA__`; do not reuse stale handles.
- Deduplicate by `listingData.id`.
- Ignore recommendation widgets that appear between result cards in the rendered DOM.
- If the browser gets stuck on verification and does not recover, treat that as a block condition, not a zero-result page.
