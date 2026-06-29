---
name: Google SERP Scholar Search API
description: Call GET /api/v1/google/scholar/search for Google SERP Scholar Search through Just Serp API with query.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_search&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_search&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_scholar_search"}}
---

# Google SERP Scholar Search

Use this focused Just Serp API skill for Google SERP Scholar Search. It targets `GET /api/v1/google/scholar/search`. Required inputs are `query`. OpenAPI describes it as: Get Google scholar Search data, including papers, patents, and legal docs, citation and year filters, and versions and cited-by links, for literature review and academic result monitoring.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `scholar/search`
- Group family: Google SERP
- Skill slug: `justserpapi-google-scholar-search`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `ScholarSearch` | `v1` | `GET` | `/api/v1/google/scholar/search` | Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `as_rr` | `query` | n/a | all | `string` | Controls whether to show only review articles (topic overviews or discussions of the searched works/authors). Set to 1 to enable the filter, or 0 (default) to return all results |
| `as_sdt` | `query` | n/a | all | `string` | Advanced filter for specific document types or legal jurisdictions. E.g., '7' to include patents |
| `as_vis` | `query` | n/a | all | `string` | Controls whether citations are included in the results: 1 = exclude, 0 (default) = include |
| `as_yhi` | `query` | n/a | all | `string` | Maximum publication year filter (e.g., '2024') |
| `as_ylo` | `query` | n/a | all | `string` | Minimum publication year filter (e.g., '2020') |
| `cites` | `query` | n/a | all | `string` | Return articles that cite the article with the specified ID |
| `cluster` | `query` | n/a | all | `string` | The unique ID of an article cluster to retrieve all versions of a specific work |
| `filter` | `query` | n/a | all | `string` | Toggle 'Similar Results' and 'Omitted Results' filters. Set to '1' (default) to enable, '0' to disable |
| `html` | `query` | n/a | all | `boolean` | Set to true to return the raw HTML of the Google Scholar search page |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `lr` | `query` | n/a | all | `string` | Restrict results to one or more languages using the 'lang_{language_code}' format (e.g., 'lang_en'). See <a href="/reference/google-lr-language">Google LR Language</a> |
| `page` | `query` | n/a | all | `integer` | The results page number. Use 0 for the first page, 1 for the second, and so on |
| `query` | `query` | all | n/a | `string` | The academic search query (e.g., 'machine learning', 'CRISPR gene editing'). Supports advanced operators like 'author:' |
| `results` | `query` | n/a | all | `integer` | The number of search results to return per page |
| `safe` | `query` | n/a | all | `string` | SafeSearch filter setting. Set to 'active' to filter adult content, or 'off' to disable it |
| `scisbd` | `query` | n/a | all | `string` | Controls whether to return only abstract results (1) or all results (0) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `ScholarSearch` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `ScholarSearch`.

```bash
node {baseDir}/bin/run.mjs --operation "ScholarSearch" --api-key "$JUST_SERP_API_KEY" --params-json '{"query":"<query>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_search&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_search&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `ScholarSearch` on `/api/v1/google/scholar/search`.
- Echo the required lookup scope (`query`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google scholar Search data, including papers, patents, and legal docs, citation and year filters, and versions and cited-by links, for literature review and academic result monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
