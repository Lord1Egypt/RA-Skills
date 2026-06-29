---
name: Google SERP Patents Details API
description: Call GET /api/v1/google/patents/details for Google SERP Patents Details through Just Serp API with patent_id.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_patents_details&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_patents_details&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_patents_details"}}
---

# Google SERP Patents Details

Use this focused Just Serp API skill for Google SERP Patents Details. It targets `GET /api/v1/google/patents/details`. Required inputs are `patent_id`. OpenAPI describes it as: Get Google patent Details data, including abstracts, claims, and legal status, for patent review and IP due diligence.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `patents/details`
- Group family: Google SERP
- Skill slug: `justserpapi-google-patents-details`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `patentDetails` | `v1` | `GET` | `/api/v1/google/patents/details` | Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `html` | `query` | n/a | all | `boolean` | Set to true to return the raw HTML of the Google search results page alongside the structured data |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `patent_id` | `query` | all | n/a | `string` | The unique Google Patent ID (e.g., 'US1234567B1') |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `patentDetails` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `patentDetails`.

```bash
node {baseDir}/bin/run.mjs --operation "patentDetails" --api-key "$JUST_SERP_API_KEY" --params-json '{"patent_id":"<patent_id>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_patents_details&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_patents_details&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `patentDetails` on `/api/v1/google/patents/details`.
- Echo the required lookup scope (`patent_id`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google patent Details data, including abstracts, claims, and legal status, for patent review and IP due diligence.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
