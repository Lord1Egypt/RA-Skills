# Google Maps Email Extractor Input and Output Contract

Default actor:

- Actor ID: `f3dlnXVnBc6v8JMNK`
- Actor name: `x_guru/google-maps-email-extractor`
- Store page: `https://apify.com/x_guru/google-maps-email-extractor`

## Input Fields

| Field | Type | Notes |
| --- | --- | --- |
| `searchStringsArray` | array | Google Maps business search terms such as `dentist`, `wedding photographer`, or `roofing contractor`. |
| `locationQuery` | string | Concrete search area for all terms. Prefer one city, metro, county, postal code, or neighborhood per run. |
| `maxCrawledPlacesPerSearch` | integer | Target saved email leads per search term or URL. In `emailsOnly`, the actor can scan extra candidates internally. |
| `contactResultMode` | string | `emailsOnly`, `contactsOnly`, or `allPlaces`. Default/recommended mode is `emailsOnly`. |
| `contactPagesLimit` | integer | Number of business website pages to check. Default is `2`; use `3-5` for deeper email discovery. |
| `includePersonalData` | boolean | Include person-like emails and personal LinkedIn URLs found on public websites. |
| `website` | string | `allPlaces`, `withWebsite`, or `withoutWebsite`; use `withWebsite` for email extraction. |
| `startUrls` | array | Google Maps search URLs, place URLs, CID URLs, or prepared Google Maps links. Use objects: `[{"url":"https://www.google.com/maps/..."}]`. |
| `placeIds` | array | Google Place IDs or compatible `place_id:` values. |
| `language` | string | Google Maps language code for returned place data. |
| `categoryFilterWords` | array | Free-text category keywords matched against categories. |
| `placeCategories` | array | Predefined Google Business Profile category filters. |
| `customPlaceCategories` | array | Custom category text matched against categories. |
| `searchMatching` | string | `all`, `only_includes`, or `only_exact`. |
| `placeMinimumStars` | string | `two`, `twoAndHalf`, `three`, `threeAndHalf`, `four`, or `fourAndHalf`. |
| `skipClosedPlaces` | boolean | Exclude closed businesses when Google exposes the status. |
| `countryCode`, `city`, `state`, `county`, `postalCode` | strings | Structured search area fields. |
| `customGeolocation`, `locationBounds`, `strictLocationBounds` | objects/boolean | Custom map area controls for bounded extraction. |

## Source Rules

- Use `searchStringsArray` plus `locationQuery` for normal lead generation.
- Use `startUrls` for Google Maps URLs already prepared by another system.
- Use `placeIds` for exact known Google Place IDs.
- Keep `website: "withWebsite"` when the user wants emails.
- If the user asks for broad review scraping, use a reviews-specific actor instead.

## Budget Guard

Pass `maxTotalChargeUsd` as an Apify run option, not inside actor input. The included script exposes it as `--budget-usd`.

The actor uses the `contact-lead-saved` PPE event for saved email leads and respects available run budget. It finishes successfully and writes `RUN_SUMMARY` when budget, filters, or source exhaustion stop the run.

## Dataset Output Fields

Each dataset item is one Google Maps place/contact lead.

| Group | Fields |
| --- | --- |
| Business | `title`, `subTitle`, `description`, `categoryName`, `categories`, `rank`, `searchString`, `isAdvertisement` |
| Emails | `emails`, `emailDetails.email`, `emailDetails.type`, `emailDetails.sourceUrl`, `emailDetails.domainMatch` |
| Contacts | `website`, `phone`, `phoneUnformatted`, `additionalPhones`, `facebooks`, `instagrams`, `linkedIns`, `twitters`, `youtubes`, `tiktoks` |
| Address | `address`, `neighborhood`, `street`, `city`, `postalCode`, `state`, `countryCode`, `location`, `plusCode` |
| Ratings | `totalScore`, `reviewsCount`, `reviewsDistribution`, `reviewsTags` |
| Google IDs | `placeId`, `fid`, `cid`, `kgmid`, `url`, `searchPageUrl`, `searchPageLoadedUrl` |
| Status/runtime | `contactStatus`, `contactSignals`, `additionalInfo.companyContacts`, `permanentlyClosed`, `temporarilyClosed`, `scrapedAt`, `language` |

The actor output page also exposes:

- `results`: default dataset URL
- `summary`: key-value store URL for `RUN_SUMMARY`

## Response Guidance

- Missing emails are normal in `contactsOnly` and `allPlaces`; in `emailsOnly`, they should not be saved unless budget or fallback behavior changed.
- `emailDetails.type` can be `role`, `personal`, or `unknown`.
- `domainMatch=false` means the email was found on a source whose domain does not clearly match the business website.
- If a run returns fewer rows than requested, check `RUN_SUMMARY` for `exhaustionReason`, budget, and enrichment counters.
- Public website contact extraction is best-effort because every business website is different.
