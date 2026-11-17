<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: api-standards.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: API Architecture | date: {generation-date} -->

# API Standards

## API Identity

**Style:** {REST/GraphQL}  |  **Format:** {JSON}  |  **Base path:** {/api/v1}  |  **Docs:** {OpenAPI 3.x}

## URL Conventions
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| API-URL-01 | {url pattern rule} |
| ... | ... |
<!-- end: AP-sourced -->

## HTTP Methods
<!-- begin: AP-sourced -->
| Method | Usage | Idempotent | Success Code |
|--------|-------|:----------:|:------------:|
| GET | Retrieve | Yes | 200 |
| POST | Create/Action | No | 201/200 |
| PUT | Full replace | Yes | 200 |
| PATCH | Partial update | No | 200 |
| DELETE | Remove | Yes | 204 |
<!-- end: AP-sourced -->

## Request Format
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| API-REQ-01 | {request format rules} |
| ... | ... |
<!-- end: AP-sourced -->

## Response Format
<!-- begin: AP-sourced -->
{JSON example structure}
| Rule | Standard |
|------|----------|
| API-RES-01 | {response format rules} |
| ... | ... |
<!-- end: AP-sourced -->

## Pagination
<!-- begin: AP-sourced -->
**Strategy:** {offset/cursor}
| Rule | Standard |
|------|----------|
| API-PAG-01 | Default page size: {n} |
| API-PAG-02 | Max page size: {n} |
| ... | ... |
<!-- end: AP-sourced -->

## Filtering & Sorting
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| API-FILT-01 | {filtering rules} |
| ... | ... |
<!-- end: AP-sourced -->

## Error Response Format
<!-- begin: AP-sourced -->
{JSON error schema}
| Code | When |
|:----:|------|
| 400 | Validation failure |
| 401 | Not authenticated |
| 403 | Not authorized |
| 404 | Not found |
| 409 | Conflict |
| 422 | Business rule violation |
| 429 | Rate limited |
| 500 | Server error |
<!-- end: AP-sourced -->

## Rate Limiting
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| API-RATE-01 | {rate limit rules} |
| ... | ... |
<!-- end: AP-sourced -->

## API Authentication
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| API-AUTH-01 | {auth mechanism} |
| ... | ... |
<!-- end: AP-sourced -->

## Documentation
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| API-DOC-01 | Every endpoint has OpenAPI docs |
| ... | ... |
<!-- end: AP-sourced -->
```

## Filling: Refer to `mapping/api-to-steering.md`.
