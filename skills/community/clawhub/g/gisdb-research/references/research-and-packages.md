# Research and package selection

Author: Daniel Hallman

Use the current GISDB tool schemas. A county's directory entry does not mean its records are available to buy or that all leads are covered. Show the source date for saved records. The date a record was retrieved does not establish its tax year.

## Inspect records

Use `gisdb_search_records` with an explicit county, state and mode:

| Mode | Supported inputs beyond county and state | Meaning |
| --- | --- | --- |
| `property_records` | Optional `q` address, parcel or owner-label query; `signal=assessment`; limit 1–250; offset 0–1,000,000; optional `format=json` | Saved property records. Missing facts remain empty. |
| `owner_portfolios` | Limit 1–100; optional `format=json` | Repeated source owner-name labels, observed parcel counts and total county-appraised value. Query, signal and offset filters are unavailable for this mode. |

Keep missing facts unknown. Owner-name groups do not establish legal identity, ownership authority, cash purchases, buying activity, acquisition prices, debt, equity or sale intent. Public previews support JSON only; do not pass CSV as a format. A purchased CSV requires its separate reviewed offer and verified delivery. Honor unavailable results. Do not call retired research aliases or use notice, scoring, CAD, sample or cash-buyer tools outside the public catalog.

## Choose a lead package

For packaged leads, pass `answers.kind=lead_package` to `gisdb_guide_search`. Ask its questions in order, retaining explicit answers and skipped question IDs. Obtain the supported county, then the user's explicit `answers.lead_package` choice:

| Choice | Recorded classifications |
| --- | --- |
| `realtor-radar` | Residential single-family and condominium uses. |
| `wholesaler-pro` | Supported residential, rental, apartment and undeveloped uses. |
| `commercial-pro` | Commercial, industrial or designated vacant commercial/industrial uses. Development or assemblage feasibility is unknown. |

Preserve the explicit `answers.delivery` choice of `one_time` or `recurring`. Package selection uses fixed source classifications; a nonempty address or owner query is unavailable for these packages. Explain the returned source dates, parcel count, criteria, coverage and missing facts. Show exact offered price and terms before selecting a returned `answers.lead_offer_id` for the user's chosen purchase. Single dated packages, monthly plans and county-record downloads are separate products. Missing or stale sources and absent offers remain unavailable; do not invent prices.

Source update timing varies by county and dataset. Attribute Hamilton's approximately monthly change files only to that documented source; do not apply that interval to other counties. Keep source publication dates, retained snapshot dates and the offer's source-check cadence distinct. A check can find no new records, and an import date does not establish a current tax year. If no publication cadence is supplied, say it is unknown.

Added notice, delinquency, municipal and contact data are unavailable. So are CAD bundles, estimates of selling motivation and verified buyer directories. Do not substitute assessment leads for an unsupported notice request.
