---
name: Google SERP Images Search API
description: Call GET /api/v1/google/images/search for Google SERP Images Search through Just Serp API with query.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_images_search&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_images_search&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_images_search"}}
---

# Google SERP Images Search

Use this focused Just Serp API skill for Google SERP Images Search. It targets `GET /api/v1/google/images/search`. Required inputs are `query`. OpenAPI describes it as: Get Google images Search data, including image URLs and metadata, for filtered image discovery for research and monitoring workflows.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `images/search`
- Group family: Google SERP
- Skill slug: `justserpapi-google-images-search`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `imagesSearch` | `v1` | `GET` | `/api/v1/google/images/search` | Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `chips` | `query` | n/a | all | `string` | Additional suggested search terms (chips) to filter images. Values are obtained from previous responses |
| `country` | `query` | n/a | all | `string` | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a> |
| `cr` | `query` | n/a | all | `string` | Limits results to search results from specific countries. Format: 'countryXX'. See <a href="/reference/google-cr-countries">Google CR Countries</a> |
| `domain` | `query` | n/a | all | `string` | The Google domain to use for the search (e.g., 'google.com', 'google.co.uk'). See <a href="/reference/google-domains">Google Domains</a> |
| `end_date` | `query` | n/a | all | `string` | End date for restricting images to a time range. Format: 'YYYYMMDD' (e.g., '20241231') |
| `filter` | `query` | n/a | all | `string` | Toggle 'Similar Results' and 'Omitted Results' filters. Set to '1' (default) to enable, '0' to disable |
| `html` | `query` | n/a | all | `boolean` | Set to true to return the raw HTML of the Google search results page alongside the structured data |
| `image_color` | `query` | n/a | all | `string` | Filter images by a dominant color (e.g., 'red', 'blue', 'bw' for black and white, 'trans' for transparent) |
| `image_type` | `query` | n/a | all | `string` | Filter by image type. Supported values: 'face', 'photo', 'clipart', 'lineart', 'animated' |
| `imgar` | `query` | n/a | all | `string` | Filter by image aspect ratio. Supported values: 's' (Square), 't' (Tall), 'w' (Wide), 'xw' (Panoramic) |
| `imgsz` | `query` | n/a | all | `string` | Filter by image size. Supported values: 'l' (Large), 'm' (Medium), 'i' (Icon), and specific resolutions like '4mp', '10mp' |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `licenses` | `query` | n/a | all | `string` | Filter by usage rights and licenses. Supported values: 'f' (Free to use), 'fc' (Commercial use), 'cl' (Creative Commons) |
| `lr` | `query` | n/a | all | `string` | Restrict results to one or more languages using the 'lang_{language_code}' format (e.g., 'lang_en'). See <a href="/reference/google-lr-language">Google LR Language</a> |
| `nfpr` | `query` | n/a | all | `string` | Controls Google's auto-correction. Set to '1' to exclude corrected results, '0' to include them |
| `page` | `query` | n/a | all | `integer` | The results page number. Use 0 for the first page, 1 for the second, and so on |
| `period_unit` | `query` | n/a | all | `string` | Time unit for 'recent' image results. Supported values: 's' (Second), 'n' (Minute), 'h' (Hour), 'd' (Day), 'w' (Week), 'm' (Month), 'y' (Year) |
| `period_value` | `query` | n/a | all | `string` | Time duration value used with 'period_unit' (e.g., 15 for 15 days). Default: 1 |
| `query` | `query` | all | n/a | `string` | The search query for images (e.g., 'mountain landscape', 'luxury cars') |
| `safe` | `query` | n/a | all | `string` | SafeSearch filter setting. Set to 'active' to filter adult content, or 'off' to disable it |
| `start_date` | `query` | n/a | all | `string` | Start date for restricting images to a time range. Format: 'YYYYMMDD' (e.g., '20241201') |
| `tbs` | `query` | n/a | all | `string` | Advanced search filter parameter (tbs) used to apply Google result filters (e.g. time range). This is an advanced parameter — if you’re not familiar with it, you can leave it empty |
| `uule` | `query` | n/a | all | `string` | Encoded location string (UULE) used to precisely localize Google search results. This is an advanced/technical parameter — if you’re not familiar with it, you can leave it empty and omit it |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `imagesSearch` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `imagesSearch`.

```bash
node {baseDir}/bin/run.mjs --operation "imagesSearch" --api-key "$JUST_SERP_API_KEY" --params-json '{"query":"<query>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_images_search&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_images_search&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `imagesSearch` on `/api/v1/google/images/search`.
- Echo the required lookup scope (`query`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google images Search data, including image URLs and metadata, for filtered image discovery for research and monitoring workflows.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
