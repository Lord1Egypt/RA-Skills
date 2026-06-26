# Google Maps Scraper Actor Input Guide

Default actor ID: `kLdarP5qiTvc9CwtP`

## Core Discovery

| Field | Type | Notes |
| --- | --- | --- |
| `searchStringsArray` | array of strings | Business categories or search terms. |
| `locationQuery` | string | Free-text location for the search. |
| `maxCrawledPlacesPerSearch` | integer | Target places per search term or URL. |
| `language` | string | Google Maps language code, usually `en`. |

Example:

```json
{
  "searchStringsArray": ["coffee shop"],
  "locationQuery": "Seattle, Washington, USA",
  "maxCrawledPlacesPerSearch": 50,
  "language": "en"
}
```

## URLs and Place IDs

Use `startUrls` for Google Maps search URLs or direct place URLs:

```json
{
  "startUrls": [
    {
      "url": "https://www.google.com/maps/search/restaurants+near+New+York,+NY"
    }
  ],
  "maxCrawledPlacesPerSearch": 100
}
```

Use `placeIds` for exact Google Place IDs:

```json
{
  "placeIds": ["ChIJN1t_tDeuEmsRUsoyG83frY4"],
  "scrapePlaceDetailPage": true
}
```

## Filters

| Field | Notes |
| --- | --- |
| `placeCategories` | Predefined Google Business Profile categories. |
| `customPlaceCategories` | Free-text category filters. |
| `searchMatching` | Match all, name includes query, or exact name match. |
| `minStars` | Minimum rating. |
| `website` | `allPlaces`, `withWebsite`, or `withoutWebsite`. |
| `skipClosedPlaces` | Exclude temporarily or permanently closed places when known. |

For email lead generation, combine:

```json
{
  "website": "withWebsite",
  "scrapeCompanyContacts": true
}
```

## Add-ons

### Place details

```json
{
  "scrapePlaceDetailPage": true,
  "scrapeTableReservationProviderData": true,
  "scrapeOrderOnlineWidgetData": true,
  "includeWebResults": true,
  "scrapeInsidePlaces": false
}
```

### Website contacts

```json
{
  "scrapeCompanyContacts": true
}
```

### Reviews

```json
{
  "maxReviews": 20,
  "reviewsSort": "newest",
  "reviewsStartDate": "2026-01-01",
  "reviewsOrigin": "all",
  "scrapeReviewsPersonalData": false
}
```

Valid `reviewsSort` values:

- `newest`
- `mostRelevant`
- `highestRanking`
- `lowestRanking`

### Images

```json
{
  "maxImages": 10,
  "scrapeImageAuthors": false
}
```

## Structured Search Area

Use these fields when `locationQuery` is empty or when the agent needs a bounded area:

| Field | Notes |
| --- | --- |
| `countryCode` | Country or region bias, for example `US`. |
| `city` | City name. |
| `state` | State, province, or region. |
| `county` | County or district. |
| `postalCode` | Postal or ZIP code. |
| `customGeolocation` | GeoJSON-like area; use longitude, latitude coordinate order. |
| `strictLocationBounds` | Keep results inside the resolved/custom area when coordinates are available. |

If `locationQuery` is present, treat it as the primary location input.

## All Visible Places

Use only for concrete local areas:

```json
{
  "locationQuery": "SoHo, New York, USA",
  "allPlacesNoSearchAction": "all_visible",
  "allPlacesZoom": 16,
  "maxCrawledPlacesPerSearch": 500
}
```

Avoid country-only or very broad locations.

## Budget Guard

When starting runs through the Apify API, pass `maxTotalChargeUsd` as a run option, not inside actor input. The script exposes it as `--budget-usd`.

## Dataset Output Fields

The actor saves one dataset item per place. The most important output groups are:

| Group | Fields |
| --- | --- |
| Identity | `title`, `subTitle`, `description`, `price`, `categoryName`, `categories`, `rank`, `isAdvertisement` |
| Address | `address`, `neighborhood`, `street`, `city`, `postalCode`, `state`, `countryCode`, `location`, `locatedIn`, `floor`, `plusCode` |
| Contacts | `website`, `phone`, `phoneUnformatted`, `emails`, `additionalPhones`, `facebooks`, `instagrams`, `linkedIns`, `twitters`, `youtubes`, `tiktoks` |
| Status | `claimThisBusiness`, `permanentlyClosed`, `temporarilyClosed` |
| Ratings and reviews | `totalScore`, `reviewsCount`, `reviewsDistribution`, `reviews`, `reviewsScraped`, `reviewsFetchStatus`, `reviewsFetchMethod`, `reviewsDateFilterStatus`, `reviewsTags` |
| Images | `imageUrl`, `imagesCount`, `images`, `imageFetchStatus`, `imageFetchMethod`, `imageAuthorsStatus`, `imageCategories` |
| Details | `openingHours`, `additionalOpeningHours`, `popularTimesLiveText`, `popularTimesLivePercent`, `popularTimesHistogram`, `menu`, `servicesLink`, `reserveTableUrl`, `googleFoodUrl`, `peopleAlsoSearch`, `placesTags`, `gasPrices` |
| Hotels | `hotelStars`, `hotelDescription`, `checkInDate`, `checkOutDate`, `hotelAds` |
| Google IDs | `placeId`, `fid`, `cid`, `kgmid`, `url`, `searchPageUrl`, `searchPageLoadedUrl`, `searchString`, `language`, `scrapedAt` |
| Nested add-ons | `additionalInfo`, including data such as `webResults`, `insidePlaces`, `companyContacts`, review metadata, and image lists when enabled |

The actor output schema also exposes `results` as the dataset URL and `summary` as the `RUN_SUMMARY` key-value-store URL.
