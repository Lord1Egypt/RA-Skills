---
name: Google SERP Hotels Search API
description: Call GET /api/v1/google/hotels/search for Google SERP Hotels Search through Just Serp API with check_in_date, check_out_date, and query.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_hotels_search&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_hotels_search&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_hotels_search"}}
---

# Google SERP Hotels Search

Use this focused Just Serp API skill for Google SERP Hotels Search. It targets `GET /api/v1/google/hotels/search`. Required inputs are `check_in_date`, `check_out_date`, and `query`. OpenAPI describes it as: Get Google hotels Search data, including prices, ratings, and availability details, for travel comparison and hospitality market analysis.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `hotels/search`
- Group family: Google SERP
- Skill slug: `justserpapi-google-hotels-search`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `hotelsSearch` | `v1` | `GET` | `/api/v1/google/hotels/search` | Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `adults` | `query` | n/a | all | `integer` | The number of adults staying in the room |
| `amenities` | `query` | n/a | all | `string` | Filter by specific amenities (e.g., '35' for free Wi-Fi). <a href="/reference/hotels/google-hotels-amenities">Google Hotels Amenities</a> (hotel amenities). <a href="/reference/hotels/google-hotels-vacation-rentals-amenities">Google Hotels Vacation Rentals Amenities</a> (vacation rental amenities) |
| `bathrooms` | `query` | n/a | all | `string` | Minimum number of bathrooms required (applies to vacation rentals) |
| `bedrooms` | `query` | n/a | all | `string` | Minimum number of bedrooms required (applies to vacation rentals) |
| `brands` | `query` | n/a | all | `string` | Filter by specific hotel brand IDs. IDs can be comma-separated |
| `check_in_date` | `query` | all | n/a | `string` | The hotel check-in date in 'YYYY-MM-DD' format (e.g., '2026-05-20') |
| `check_out_date` | `query` | all | n/a | `string` | The hotel check-out date in 'YYYY-MM-DD' format (e.g., '2026-05-25') |
| `children` | `query` | n/a | all | `integer` | The number of children staying in the room |
| `children_ages` | `query` | n/a | all | `string` | The ages of the children, separated by commas (e.g., '5,10'). The number of ages must match the 'children' parameter |
| `country` | `query` | n/a | all | `string` | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a> |
| `currency` | `query` | n/a | all | `string` | The three-letter ISO currency code for displaying prices (e.g., 'USD', 'EUR'). See <a href="/reference/hotels/google-hotels-currency">Google Hotels Currency</a> |
| `eco_certified` | `query` | n/a | all | `string` | Filter for hotels that are eco-certified. Set to '1' or 'true' to enable |
| `free_cancellation` | `query` | n/a | all | `string` | Filter for hotels that offer free cancellation. Set to '1' or 'true' to enable |
| `hotel_class` | `query` | n/a | all | `string` | Filter by hotel star ratings. Supported values: '2', '3', '4', '5'. Can be comma-separated |
| `html` | `query` | n/a | all | `boolean` | Set to true to return the raw HTML of the Google search results page alongside the structured data |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `max_price` | `query` | n/a | all | `string` | Maximum price filter for the hotel stay |
| `min_price` | `query` | n/a | all | `string` | Minimum price filter for the hotel stay |
| `next_page_token` | `query` | n/a | all | `string` | The token used to retrieve the next page of hotel results. This token is found in the 'next_page_token' field of a previous response |
| `property_token` | `query` | n/a | all | `string` | The unique token for a specific hotel property to fetch detailed information |
| `property_types` | `query` | n/a | all | `string` | Filter by hotel property types. See the <a href="/reference/hotels/google-hotels-property-types">Google Property Types</a> for the full list of supported hotel property types. For vacation rentals, refer to the <a href="/reference/hotels/google-hotels-vacation-rentals-property-types">Google Hotels Vacation Rentals Property Types</a> |
| `query` | `query` | all | n/a | `string` | The destination or specific hotel name you are searching for (e.g., 'Paris', 'Hilton New York') |
| `rating` | `query` | n/a | all | `string` | Filter by minimum guest rating. Supported values: '7' (3.5+), '8' (4.0+), '9' (4.5+) |
| `sort_by` | `query` | n/a | all | `string` | The criteria to sort hotel results. Supported values: '3' (Lowest price), '8' (Highest rating), '13' (Most reviews) |
| `special_offers` | `query` | n/a | all | `string` | Filter for hotels currently offering special deals or discounts. Set to '1' or 'true' to enable |
| `vacation_rentals` | `query` | n/a | all | `boolean` | Set to true to search for vacation rentals instead of standard hotels |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `hotelsSearch` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `hotelsSearch`.

```bash
node {baseDir}/bin/run.mjs --operation "hotelsSearch" --api-key "$JUST_SERP_API_KEY" --params-json '{"query":"<query>","check_in_date":"<check_in_date>","check_out_date":"<check_out_date>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_hotels_search&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_hotels_search&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `hotelsSearch` on `/api/v1/google/hotels/search`.
- Echo the required lookup scope (`check_in_date`, `check_out_date`, and `query`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google hotels Search data, including prices, ratings, and availability details, for travel comparison and hospitality market analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
