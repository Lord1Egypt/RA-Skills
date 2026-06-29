---
name: Google SERP Immersive Product API
description: Call GET /api/v1/google/immersive/product for Google SERP Immersive Product through Just Serp API with page_token.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_immersive_product&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_immersive_product&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_immersive_product"}}
---

# Google SERP Immersive Product

Use this focused Just Serp API skill for Google SERP Immersive Product. It targets `GET /api/v1/google/immersive/product`. Required inputs are `page_token`. OpenAPI describes it as: Get Google immersive Product data, including features, specifications, and seller information, for product research and merchandising analysis.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `immersive/product`
- Group family: Google SERP
- Skill slug: `justserpapi-google-immersive-product`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `immersiveProduct` | `v1` | `GET` | `/api/v1/google/immersive/product` | Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `country` | `query` | n/a | all | `string` | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a> |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `page_token` | `query` | all | n/a | `string` | The unique token used to retrieve detailed product information in Google's immersive view. This token is typically found in Google Shopping or Search results |
| `sori` | `query` | n/a | all | `integer` | Pagination offset for seller results. Set this to the number of sellers already retrieved to get the next set |
| `stores` | `query` | n/a | all | `boolean` | If set to true, the API will retrieve a list of more sellers for the product. Use this together with the 'sori' parameter |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `immersiveProduct` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `immersiveProduct`.

```bash
node {baseDir}/bin/run.mjs --operation "immersiveProduct" --api-key "$JUST_SERP_API_KEY" --params-json '{"page_token":"<page_token>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_immersive_product&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_immersive_product&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `immersiveProduct` on `/api/v1/google/immersive/product`.
- Echo the required lookup scope (`page_token`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google immersive Product data, including features, specifications, and seller information, for product research and merchandising analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
