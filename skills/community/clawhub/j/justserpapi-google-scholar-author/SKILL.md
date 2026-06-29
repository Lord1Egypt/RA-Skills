---
name: Google SERP Scholar Author API
description: Call GET /api/v1/google/scholar/author for Google SERP Scholar Author through Just Serp API with author_id.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_author&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_author&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_scholar_author"}}
---

# Google SERP Scholar Author

Use this focused Just Serp API skill for Google SERP Scholar Author. It targets `GET /api/v1/google/scholar/author`. Required inputs are `author_id`. OpenAPI describes it as: Get Google scholar Author data, including publications, citation metrics, and research interests, for researcher analysis and academic profiling.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `scholar/author`
- Group family: Google SERP
- Skill slug: `justserpapi-google-scholar-author`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `ScholarAuthor` | `v1` | `GET` | `/api/v1/google/scholar/author` | Author |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `author_id` | `query` | all | n/a | `string` | The unique Google Scholar ID of the researcher/author (e.g., 'LSs6DR8AAAAJ') |
| `citation_id` | `query` | n/a | all | `string` | The citation ID to view details for (required when 'view_op' is 'view_citation') |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `results` | `query` | n/a | all | `integer` | The number of results to return per page |
| `sort` | `query` | n/a | all | `string` | Sorting criteria for the author's publications. Supported values: 'title', 'pubdate' |
| `view_op` | `query` | n/a | all | `string` | Specific view operation for the author profile. Use 'list_colleagues' to see co-authors or 'view_citation' for article details |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `ScholarAuthor` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `ScholarAuthor`.

```bash
node {baseDir}/bin/run.mjs --operation "ScholarAuthor" --api-key "$JUST_SERP_API_KEY" --params-json '{"author_id":"<author_id>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_author&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_author&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `ScholarAuthor` on `/api/v1/google/scholar/author`.
- Echo the required lookup scope (`author_id`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google scholar Author data, including publications, citation metrics, and research interests, for researcher analysis and academic profiling.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
