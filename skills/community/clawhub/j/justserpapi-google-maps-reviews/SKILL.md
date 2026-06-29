---
name: Google SERP Maps Reviews API
description: Call GET /api/v1/google/maps/reviews for Google SERP Maps Reviews through Just Serp API with data_id.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_reviews&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_reviews&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_maps_reviews"}}
---

# Google SERP Maps Reviews

Use this focused Just Serp API skill for Google SERP Maps Reviews. It targets `GET /api/v1/google/maps/reviews`. Required inputs are `data_id`. OpenAPI describes it as: Get Google maps Reviews data, including ratings and reviewer metadata, for reputation analysis and review monitoring.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `maps/reviews`
- Group family: Google SERP
- Skill slug: `justserpapi-google-maps-reviews`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `mapsReviews` | `v1` | `GET` | `/api/v1/google/maps/reviews` | Reviews |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `data_id` | `query` | all | n/a | `string` | The unique Google Maps location ID (feature ID). You can get this from our Google Maps Search API |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `next_page_token` | `query` | n/a | all | `string` | Token for retrieving the next page of reviews |
| `results` | `query` | n/a | all | `integer` | The maximum number of reviews to return per page (range: 1-20) |
| `sort_by` | `query` | n/a | all | `string` | Sorting order for reviews. Supported values: 'qualityScore' (Relevance), 'newestFirst' (Newest), 'ratingHigh' (Highest rating), 'ratingLow' (Lowest rating) |
| `topic_id` | `query` | n/a | all | `string` | Filter reviews by a specific topic ID. Topic IDs are obtained from previous Maps Reviews API responses |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `mapsReviews` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `mapsReviews`.

```bash
node {baseDir}/bin/run.mjs --operation "mapsReviews" --api-key "$JUST_SERP_API_KEY" --params-json '{"data_id":"<data_id>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_reviews&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_reviews&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `mapsReviews` on `/api/v1/google/maps/reviews`.
- Echo the required lookup scope (`data_id`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google maps Reviews data, including ratings and reviewer metadata, for reputation analysis and review monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
