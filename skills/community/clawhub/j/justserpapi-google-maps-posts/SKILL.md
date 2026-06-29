---
name: Google SERP Maps Posts API
description: Call GET /api/v1/google/maps/posts for Google SERP Maps Posts through Just Serp API with data_id.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_posts&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_posts&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_maps_posts"}}
---

# Google SERP Maps Posts

Use this focused Just Serp API skill for Google SERP Maps Posts. It targets `GET /api/v1/google/maps/posts`. Required inputs are `data_id`. OpenAPI describes it as: Get Google maps Posts data, including business post content, post dates and images, and profile-specific feeds, for local business monitoring and promotion tracking.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `maps/posts`
- Group family: Google SERP
- Skill slug: `justserpapi-google-maps-posts`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `mapsPosts` | `v1` | `GET` | `/api/v1/google/maps/posts` | Posts |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `data_id` | `query` | all | n/a | `string` | The unique Google Maps location ID (feature ID). You can get this from our Google Maps Search API |
| `next_page_token` | `query` | n/a | all | `string` | Token used to retrieve the next page of business posts |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `mapsPosts` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `mapsPosts`.

```bash
node {baseDir}/bin/run.mjs --operation "mapsPosts" --api-key "$JUST_SERP_API_KEY" --params-json '{"data_id":"<data_id>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_posts&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_posts&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `mapsPosts` on `/api/v1/google/maps/posts`.
- Echo the required lookup scope (`data_id`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google maps Posts data, including business post content, post dates and images, and profile-specific feeds, for local business monitoring and promotion tracking.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
