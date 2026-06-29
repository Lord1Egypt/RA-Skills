---
name: Google SERP Scholar Cite Search API
description: Call GET /api/v1/google/scholar/cite/search for Google SERP Scholar Cite Search through Just Serp API with query.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_cite_search&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_cite_search&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_scholar_cite_search"}}
---

# Google SERP Scholar Cite Search

Use this focused Just Serp API skill for Google SERP Scholar Cite Search. It targets `GET /api/v1/google/scholar/cite/search`. Required inputs are `query`. OpenAPI describes it as: Get Google scholar Citations data, including export links, for bibliography automation and citation workflows.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `scholar/cite/search`
- Group family: Google SERP
- Skill slug: `justserpapi-google-scholar-cite-search`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `ScholarCiteSearch` | `v1` | `GET` | `/api/v1/google/scholar/cite/search` | Citations |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `query` | `query` | all | n/a | `string` | The unique ID of a Google Scholar search result to retrieve citation formats for. Found in the 'id' field of previous Scholar Search responses |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `ScholarCiteSearch` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `ScholarCiteSearch`.

```bash
node {baseDir}/bin/run.mjs --operation "ScholarCiteSearch" --api-key "$JUST_SERP_API_KEY" --params-json '{"query":"<query>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_cite_search&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_cite_search&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `ScholarCiteSearch` on `/api/v1/google/scholar/cite/search`.
- Echo the required lookup scope (`query`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google scholar Citations data, including export links, for bibliography automation and citation workflows.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
