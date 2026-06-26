# Google Maps Reviews Scraper Input and Output Contract

Default actor:

- Actor ID: `V2kIsQs3Ta9C9kkEt`
- Actor name: `x_guru/google-maps-reviews-scraper`
- Store page: `https://apify.com/x_guru/google-maps-reviews-scraper`

## Input Fields

| Field | Type | Notes |
| --- | --- | --- |
| `startUrls` | array | Direct Google Maps place URLs, `cid` URLs, or Google review detail URLs. Use objects: `[{"url":"https://www.google.com/maps/..."}]`. |
| `placeIds` | array | Google Place IDs, `place_id:` values, or URLs containing `query_place_id`. |
| `maxReviews` | integer | Maximum reviews to save per place. |
| `reviewsSort` | string | `newest`, `mostRelevant`, `highestRanking`, or `lowestRanking`. |
| `reviewsStartDate` | string | Optional absolute date like `2026-01-01` or relative value like `3 months`. |
| `reviewsOrigin` | string | `google` or `all`; `all` is compatibility mode and currently returns Google reviews when third-party sources are not exposed. |
| `language` | string | Google Maps interface language for returned labels, URLs, and relative dates. |
| `personalData` | boolean | Include public reviewer profile fields when Google exposes them. |

## Source Rules

- Use this actor for exact places only.
- Do not use broad Google Maps search URLs when the user expects many places.
- For discovery, run the main Google Maps Scraper first, then pass exact place URLs or Place IDs here.
- Normalize string `startUrls` into object form before calling Apify.
- Use `reviewsSort: "newest"` when `reviewsStartDate` is active.

## Budget Guard

Pass `maxTotalChargeUsd` as an Apify run option, not inside actor input. The included script exposes it as `--budget-usd`.

The actor uses the `review-scraped` PPE event and reduces the requested target when a run-level budget cannot cover all requested reviews.

## Dataset Output Fields

Each dataset item is one Google Maps review.

| Group | Fields |
| --- | --- |
| Source | `searchString`, `inputStartUrl`, `inputPlaceId`, `rank`, `searchPageUrl`, `searchPageLoadedUrl` |
| Review | `reviewId`, `reviewUrl`, `text`, `textTranslated`, `publishAt`, `publishedAtDate`, `likesCount`, `reviewOrigin`, `stars`, `rating`, `originalLanguage`, `translatedLanguage` |
| Owner response | `responseFromOwnerDate`, `responseFromOwnerText` |
| Review extras | `reviewImageUrls`, `reviewContext`, `reviewDetailedRating`, `visitedIn`, `isAdvertisement` |
| Reviewer | `reviewerId`, `reviewerUrl`, `name`, `reviewerNumberOfReviews`, `isLocalGuide`, `reviewerPhotoUrl` |
| Place | `title`, `placeId`, `fid`, `cid`, `kgmid`, `categoryName`, `categories`, `totalScore`, `reviewsCount`, `url`, `imageUrl`, `price` |
| Address | `address`, `neighborhood`, `street`, `city`, `postalCode`, `state`, `countryCode`, `location` |
| Status/runtime | `permanentlyClosed`, `temporarilyClosed`, `scrapedAt`, `language` |

The actor output page also exposes:

- `results`: default dataset URL
- `summary`: key-value store URL for `RUN_SUMMARY`

## Response Guidance

- If `personalData=false`, reviewer profile fields can be null by design.
- Missing owner responses, review images, detailed ratings, visit context, and normalized dates are normal when Google does not expose them.
- If a run succeeds with zero rows, explain that the source was processed but no matching reviews were saved or the budget/filters prevented saving.
- Use `RUN_SUMMARY` for diagnostics when source-level errors occur.
