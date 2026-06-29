---
name: Google SERP News Search API
description: Call GET /api/v1/google/news/search for Google SERP News Search through Just Serp API with query.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_news_search&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_news_search&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_news_search"}}
---

# Google SERP News Search

Use this focused Just Serp API skill for Google SERP News Search. It targets `GET /api/v1/google/news/search`. Required inputs are `query`. OpenAPI describes it as: Get Google news Search data, including headlines and source metadata, for media monitoring and news aggregation.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `news/search`
- Group family: Google SERP
- Skill slug: `justserpapi-google-news-search`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `newsSearch` | `v1` | `GET` | `/api/v1/google/news/search` | Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `country` | `query` | n/a | all | `string` | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a> |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `publication_token` | `query` | n/a | all | `string` | The Google News publication token to fetch results from a specific source (e.g., 'CNN', 'BBC'). Obtained from previous responses |
| `query` | `query` | all | n/a | `string` | The search query for Google News (e.g., 'artificial intelligence', 'climate change') |
| `section_token` | `query` | n/a | all | `string` | The Google News section token to access a specific subsection within a topic or publication |
| `so` | `query` | n/a | all | `string` | Sorting order for news results. Supported values: '0' (Relevance, default), '1' (Date). Only works with 'story_token' |
| `topic_token` | `query` | n/a | all | `string` | The Google News topic token to retrieve results for a specific category (e.g., 'World', 'Technology'). Obtained from previous responses |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `newsSearch` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `newsSearch`.

```bash
node {baseDir}/bin/run.mjs --operation "newsSearch" --api-key "$JUST_SERP_API_KEY" --params-json '{"query":"<query>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_news_search&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_news_search&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `newsSearch` on `/api/v1/google/news/search`.
- Echo the required lookup scope (`query`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google news Search data, including headlines and source metadata, for media monitoring and news aggregation.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
