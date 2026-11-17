# Jarsy: legacy public API

Base URL: `https://preipo.polyos.ai` (override with `PREIPO_API_BASE_URL` for
a compatible deployment). All endpoints below are public, read-only JSON and
may be cached. Research never calls protected endpoints.

## `GET /api/summary`

Returns freshness and dashboard aggregates. `stats` includes `total`,
`liveCount`, `presaleCount`, `buyEnabledCount`, `sellEnabledCount`,
`categorizedCount`, `returnCoverageCount`, `newInvestableCount`, and
`activeVolumeCount`. It also returns stage distribution, valuation Top 10,
primary category counts, tag counts, `lastImport`, and `latestSourceRecordAt`.

`lastImport.importedAt` is the latest successful site-wide import. It is not a
replacement for any asset's `sourceUpdatedAt`; `latestSourceRecordAt` is only
the maximum observed asset timestamp.

## `GET /api/discovery`

Optional filters: `category` and repeatable `tag` (OR matching). Returns:

| Field | Meaning |
| --- | --- |
| `newWindowDays` | Current first-observed window used for new listings |
| `topReturns` | Top 5 by historical valuation low-to-high return |
| `lowValuations` | Top 5 by current Jarsy valuation ascending |
| `nearHistoricalLows` | Top 5 nearest to their captured historical valuation low |
| `newInvestable` | Top 5 recently first-observed assets that are currently buyable or sellable |
| `activeTrading` | Top 5 by current Jarsy `volume` descending |

Every list item has the asset fields below. These are observation signals, not
recommendations, and `volume` has no stated fixed measurement period.

## `GET /api/assets`

Returns `{ items, total, page, pageSize }`.

| Parameter | Accepted values | Default |
| --- | --- | --- |
| `q` | company, token, underlying name, or ticker keyword | none |
| `market` | `live`, `presale` | all |
| `stage` | `Live`, `Locking Period`, `Presale`, `Early Access` | all |
| `trade` | `buy_sell`, `buy_only`, `sell_only`, `inactive` | all |
| `category` | one model-derived Chinese primary category | all |
| `tag` | repeatable model-derived sub-sector tag; matches any supplied tag | none |
| `new` | `1`; first observed in the current window and currently buyable or sellable | none |
| `sort` | `valuation_desc`, `valuation_asc`, `relative_low_asc`, `return_desc`, `volume_desc`, `first_seen_desc`, `price_desc`, `updated_desc`, `name_asc` | `valuation_desc` |
| `page` | integer 1–10000 | `1` |
| `pageSize` | integer 6–48 | `12` |

Each item can include:

| Field | Meaning |
| --- | --- |
| `token`, `market`, `stage`, `companyName`, `underlyingName`, `underlyingTicker` | Asset identity and Jarsy grouping |
| `buyActive`, `sellActive`, `priceUsd`, `priceDate`, `valuationMillions`, `volumeUsd` | Jarsy point-in-time market fields |
| `sourceUpdatedAt`, `sourceUrl`, `proofUrl`, `scanUrl` | Provenance and individual record freshness |
| `firstSeenAt`, `isNewlyDiscovered` | Observer lifecycle signal; the latter also requires current buy or sell availability |
| `primaryCategory`, `tags` | Model-derived primary category and persisted sub-sector tags |
| `valuationHistoryPointCount`, `valuationLowMillions`, `valuationLowLabel`, `valuationHighMillions`, `valuationHighLabel` | Captured historical valuation range |
| `valuationReturnPct` | `(historical high / historical low - 1) × 100`; null with fewer than two valid points |
| `valuationVsHistoricalLowPct` | `(current valuation / historical low - 1) × 100`; null without valid positive values |

Fields may be `null`; present them as unavailable rather than zero. Prices,
valuations, volumes, states, return signals, and listing signals are not
investment advice.

## `GET /api/assets/{token}/detail`

Returns data captured from the token's associated public Jarsy detail page once
an authorized detail refresh has completed. Important fields include company
identity (`legalName`, `displayName`, `slug`), profile (`headquarters`,
`foundedYear`, `overviewZh` and `overview` when present), `displayValuation`, historical `valuationHistory`,
the persisted range fields above, detail freshness (`detailFetchedAt`,
`sourceLastModifiedAt`, `detailStatus`), and model-derived Chinese fields
(`overviewZh`, `primaryCategory`, `tags`, `classificationReasonZh`,
`enrichmentFetchedAt`, `enrichmentModel`, `enrichmentStatus`).

`detailFetchedAt`, `sourceUpdatedAt`, and `lastImport.importedAt` describe
different snapshots. Detail-page text and charts are not current valuation or
investment advice; Chinese overview and classifications are model-derived.
