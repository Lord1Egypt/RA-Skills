---
name: Google SERP Scholar Profiles API
description: Call GET /api/v1/google/scholar/profiles for Google SERP Scholar Profiles through Just Serp API with mauthors.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_profiles&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_profiles&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_scholar_profiles"}}
---

# Google SERP Scholar Profiles

Use this focused Just Serp API skill for Google SERP Scholar Profiles. It targets `GET /api/v1/google/scholar/profiles`. Required inputs are `mauthors`. OpenAPI describes it as: Get Google scholar Profiles data, including profile search results, affiliation and citation counts, and pagination tokens, for researcher discovery and academic directory building.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `scholar/profiles`
- Group family: Google SERP
- Skill slug: `justserpapi-google-scholar-profiles`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `ScholarProfiles` | `v1` | `GET` | `/api/v1/google/scholar/profiles` | Scholar Profiles |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `after_author` | `query` | n/a | all | `string` | Token used to retrieve the next page of author profiles |
| `before_author` | `query` | n/a | all | `string` | Token used to retrieve the previous page of author profiles |
| `mauthors` | `query` | all | n/a | `string` | The search query for author profiles (e.g., 'John Smith', 'Harvard University') |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `ScholarProfiles` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `ScholarProfiles`.

```bash
node {baseDir}/bin/run.mjs --operation "ScholarProfiles" --api-key "$JUST_SERP_API_KEY" --params-json '{"mauthors":"<mauthors>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_profiles&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_profiles&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `ScholarProfiles` on `/api/v1/google/scholar/profiles`.
- Echo the required lookup scope (`mauthors`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google scholar Profiles data, including profile search results, affiliation and citation counts, and pagination tokens, for researcher discovery and academic directory building.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
