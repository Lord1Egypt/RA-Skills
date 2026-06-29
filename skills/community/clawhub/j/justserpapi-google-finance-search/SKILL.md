---
name: Google SERP Finance Search API
description: Call GET /api/v1/google/finance/search for Google SERP Finance Search through Just Serp API with query.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_finance_search&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_finance_search&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_finance_search"}}
---

# Google SERP Finance Search

Use this focused Just Serp API skill for Google SERP Finance Search. It targets `GET /api/v1/google/finance/search`. Required inputs are `query`. OpenAPI describes it as: Get Google finance Search data, including market summaries, company details, and related finance results, for finance monitoring and market research.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `finance/search`
- Group family: Google SERP
- Skill slug: `justserpapi-google-finance-search`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `financeSearch` | `v1` | `GET` | `/api/v1/google/finance/search` | Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `html` | `query` | n/a | all | `boolean` | Set to true to return the raw HTML of the Google search results page alongside the structured data |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `query` | `query` | all | n/a | `string` | The stock symbol, company name, or index you want to search for on Google Finance (e.g., 'AAPL', 'Tesla', 'S&P 500') |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `financeSearch` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `financeSearch`.

```bash
node {baseDir}/bin/run.mjs --operation "financeSearch" --api-key "$JUST_SERP_API_KEY" --params-json '{"query":"<query>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_finance_search&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_finance_search&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `financeSearch` on `/api/v1/google/finance/search`.
- Echo the required lookup scope (`query`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google finance Search data, including market summaries, company details, and related finance results, for finance monitoring and market research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
