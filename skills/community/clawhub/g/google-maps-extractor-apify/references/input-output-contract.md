# Google Maps Extractor Input and Output Contract

Default actor:

- Actor ID: `2A4RTA5PjN7McqJXx`
- Actor name: `x_guru/google-maps-extractor`
- Store page: `https://apify.com/x_guru/google-maps-extractor`
- Console source: `https://console.apify.com/actors/2A4RTA5PjN7McqJXx/source`

## Input Fields

### Core discovery

| Field | Type | Notes |
| --- | --- | --- |
| `searchStringsArray` | array of strings | Google Maps search terms such as `restaurant`, `dentist`, `hotel`, or `bike repair shop`. |
| `locationQuery` | string | Free-text location for all search terms. |
| `maxCrawledPlacesPerSearch` | integer | Target number of places per search term, URL, or source. Minimum `1`. |
| `language` | string | Google Maps language code, usually `en`. |

### URLs and Place IDs

| Field | Type | Notes |
| --- | --- | --- |
| `startUrls` | array | Google Maps search URLs, direct place URLs, CID URLs, or app/share URLs. Use objects: `[{"url":"https://www.google.com/maps/..."}]`. |
| `placeIds` | array | Google Place IDs, values prefixed with `place_id:`, or URLs containing `query_place_id`. |

### Filters

| Field | Type | Notes |
| --- | --- | --- |
| `categoryFilterWords` | array of strings | Free-text category keywords matched against `categoryName` and `categories`. |
| `placeCategories` | array of strings | Predefined Google Business Profile category filters. |
| `searchMatching` | string | `all`, `only_includes`, or `only_exact`. |
| `placeMinimumStars` | string | Empty, `two`, `twoAndHalf`, `three`, `threeAndHalf`, `four`, or `fourAndHalf`. |
| `website` | string | `allPlaces`, `withWebsite`, or `withoutWebsite`. |
| `skipClosedPlaces` | boolean | Exclude temporarily or permanently closed places when Google exposes status. |

### Add-ons

| Field | Type | Notes |
| --- | --- | --- |
| `scrapePlaceDetailPage` | boolean | Enrich saved places with extra Google Maps detail fields. |
| `scrapeTableReservationProvider` | boolean | Include table reservation provider data when exposed. |
| `scrapeOrderOnline` | boolean | Include order-online URL data when exposed. |
| `includeWebResults` | boolean | Include related web result links when exposed. |
| `scrapeDirectories` | boolean | Include inside places/directories when exposed. |
| `scrapeContacts` | boolean | Visit public business websites and extract emails, phones, and social links. |

### Search area

| Field | Type | Notes |
| --- | --- | --- |
| `countryCode` | string | Country or region bias, for example `US`; do not invent it when `locationQuery` is already specific. |
| `city`, `state`, `county`, `postalCode` | string | Structured search area fields. |
| `customGeolocation` | object | Custom map area or polygon input. |
| `strictLocationBounds` | boolean | Keep results inside resolved or custom bounds when coordinates are available. |
| `allPlacesNoSearchAction` | string | Empty or `all_visible`; legacy values are accepted but `all_visible` is preferred. |
| `allPlacesZoom` | integer | Optional zoom for all-visible-place mode. |

## Source Rules

- Use search terms plus location for normal Google Maps extraction.
- Use `startUrls` for Google Maps URLs and normalize string URLs into object form.
- Use `placeIds` for exact known places.
- If direct URLs or Place IDs are provided, do not keep default example search terms unless the user explicitly wants both.
- Use `allPlacesNoSearchAction: "all_visible"` only for concrete local areas.
- Avoid country-only all-visible runs. Split broad areas into city, postal code, or polygon runs.

## Add-on and Pricing Guidance

The actor uses pay-per-event pricing:

- saved place: Free `$0.003`, paid tiers `$0.0015`
- filter applied: Free `$0.0008`, paid tiers `$0.00035`
- place details: Free `$0.0015`, paid tiers `$0.00075`
- website contacts: Free `$0.0015`, paid tiers `$0.00045`

Pass `maxTotalChargeUsd` as an Apify run option, not inside actor input. The included script exposes it as `--budget-usd`.

## Dataset Output Fields

Each dataset item is one Google Maps place.

| Group | Fields |
| --- | --- |
| Identity | `title`, `subTitle`, `description`, `price`, `categoryName`, `categories`, `rank`, `isAdvertisement` |
| Address | `address`, `neighborhood`, `street`, `city`, `postalCode`, `state`, `countryCode`, `location`, `locatedIn`, `floor`, `plusCode` |
| Contacts | `website`, `phone`, `phoneUnformatted`, `emails`, `additionalPhones`, `facebooks`, `instagrams`, `linkedIns`, `twitters`, `youtubes`, `tiktoks` |
| Status | `claimThisBusiness`, `permanentlyClosed`, `temporarilyClosed` |
| Ratings | `totalScore`, `reviewsCount`, `reviewsDistribution`, `reviewsTags` |
| Images summary | `imageUrl`, `imagesCount`, `imageCategories` |
| Details | `openingHours`, `additionalOpeningHours`, `popularTimesLiveText`, `popularTimesLivePercent`, `popularTimesHistogram`, `menu`, `servicesLink`, `reserveTableUrl`, `googleFoodUrl`, `peopleAlsoSearch`, `placesTags`, `gasPrices` |
| Hotels | `hotelStars`, `hotelDescription`, `checkInDate`, `checkOutDate`, `hotelAds` |
| Google IDs | `placeId`, `fid`, `cid`, `kgmid`, `url`, `searchPageUrl`, `searchPageLoadedUrl`, `searchString`, `language`, `scrapedAt` |
| Nested add-ons | `additionalInfo`, including data such as `companyContacts`, `webResults`, and `insidePlaces` when enabled |

The actor output schema also exposes:

- `results`: default dataset URL
- `summary`: key-value store URL for `RUN_SUMMARY`

## Response Guidance

- If rows are empty, say the run succeeded but no matching places were saved, then suggest checking `RUN_SUMMARY`.
- If contact fields are empty and `scrapeContacts` was false, explain that website contact enrichment was not enabled.
- If `scrapeContacts` was true and fields are still empty, explain that public website contact extraction is best-effort.
- If detail fields are missing and `scrapePlaceDetailPage` was false, explain that the detail add-on was not enabled.
- Do not promise reviews or full image lists from this extractor. Use the main Google Maps Scraper or Reviews Scraper when the user explicitly needs reviews or review rows.
