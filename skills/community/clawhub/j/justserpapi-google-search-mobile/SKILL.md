---
name: Google SERP Search Mobile API
description: Call GET /api/v1/google/search/mobile for Google SERP Search Mobile through Just Serp API with query.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_search_mobile&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_search_mobile&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_search_mobile"}}
---

# Google SERP Search Mobile

Use this focused Just Serp API skill for Google SERP Search Mobile. It targets `GET /api/v1/google/search/mobile`. Required inputs are `query`. OpenAPI describes it as: Get Google mobile Search SERP data, including mobile-specific layouts and result features, for mobile SEO analysis and ranking checks.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `search/mobile`
- Group family: Google SERP
- Skill slug: `justserpapi-google-search-mobile`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchMobile` | `v1` | `GET` | `/api/v1/google/search/mobile` | Mobile Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `country` | `query` | n/a | all | `string` | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a> |
| `cr` | `query` | n/a | all | `string` | Limits results to search results from specific countries. Format: 'countryXX'. See <a href="/reference/google-cr-countries">Google CR Countries</a> |
| `domain` | `query` | n/a | all | `string` | The Google domain to use for the search (e.g., 'google.com', 'google.co.uk'). See <a href="/reference/google-domains">Google Domains</a> |
| `filter` | `query` | n/a | all | `string` | Toggle 'Similar Results' and 'Omitted Results' filters. Set to '1' (default) to enable, '0' to disable |
| `html` | `query` | n/a | all | `boolean` | Set to true to return the raw HTML of the Google search results page alongside the structured data |
| `ibp` | `query` | n/a | all | `string` | Parameter (ibp) used to control certain Google UI expansions or rendering modes (commonly in local/business result views). This is an advanced technical parameter — if you’re not familiar with it, you can leave it empty |
| `kgmid` | `query` | n/a | all | `string` | Knowledge Graph entity/listing ID (KGMID) used to retrieve details for a specific entity. This is an advanced technical parameter — if you’re not familiar with it, you can leave it empty |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `location` | `query` | n/a | all | `string` | The textual location name (e.g., 'New York, NY') to localize the search results |
| `lr` | `query` | n/a | all | `string` | Restrict results to one or more languages using the 'lang_{language_code}' format (e.g., 'lang_en'). See <a href="/reference/google-lr-language">Google LR Language</a> |
| `lsig` | `query` | n/a | all | `string` | Signature parameter (lsig) sometimes required for certain Knowledge Graph / local map view features. This is an advanced technical parameter — if you’re not familiar with it, you can leave it empty |
| `ludocid` | `query` | n/a | all | `string` | Google local business CID (place identifier). Used to target a specific Google Business Profile / local listing. Advanced parameter — if you don’t know it, you can omit it |
| `nfpr` | `query` | n/a | all | `string` | Controls Google's auto-correction. Set to '1' to exclude corrected results, '0' to include them |
| `page` | `query` | n/a | all | `integer` | The results page number. Use 0 for the first page, 1 for the second, and so on |
| `query` | `query` | all | n/a | `string` | The search query for Google Search (e.g., 'coffee shops', 'how to bake a cake') |
| `safe` | `query` | n/a | all | `string` | SafeSearch filter setting. Set to 'active' to filter adult content, or 'off' to disable it |
| `si` | `query` | n/a | all | `string` | Cached search context parameter (si) used to reproduce specific Google search result views/context (e.g. some Knowledge Graph tabs). This is an advanced technical parameter — if you’re not familiar with it, you can leave it empty |
| `tbs` | `query` | n/a | all | `string` | Advanced search filter parameter (tbs) used to apply Google result filters (e.g. time range). This is an advanced parameter — if you’re not familiar with it, you can leave it empty |
| `uds` | `query` | n/a | all | `string` | Advanced filter token (uds) used for specific Google search sub-filters. This is an advanced technical parameter, usually provided by Google in filter options/results — if you’re not familiar with it, you can leave it empty |
| `uule` | `query` | n/a | all | `string` | Encoded location string (UULE) used to precisely localize Google search results. This is an advanced/technical parameter — if you’re not familiar with it, you can leave it empty and omit it |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchMobile` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchMobile`.

```bash
node {baseDir}/bin/run.mjs --operation "searchMobile" --api-key "$JUST_SERP_API_KEY" --params-json '{"query":"<query>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_search_mobile&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_search_mobile&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchMobile` on `/api/v1/google/search/mobile`.
- Echo the required lookup scope (`query`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google mobile Search SERP data, including mobile-specific layouts and result features, for mobile SEO analysis and ranking checks.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
