# go-mem0: setup and reference

This module is unofficial and not affiliated with Mem0.

## Contents

- [Requirements](#requirements)
- [Install](#install)
- [Base URL and auth](#base-url-and-auth)
- [Client](#client)
- [Operations](#operations)
- [Responses](#responses)
- [Memory versions](#memory-versions)
- [Pagination](#pagination)
- [Profile jobs](#profile-jobs)
- [Rate limits](#rate-limits)

## Requirements

- Go 1.26.10 or newer, per `go.mod`.
- A Mem0 Platform API key, exported as `MEM0_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-mem0
```

## Base URL and auth

Use `https://api.mem0.ai`. The spec declares `ApiKeyAuth`, an `Authorization` header with the value `Token <key>`. Set it through `mem0.WithRequestEditorFn`, as shown in the root README.

## Client

- `mem0.NewClientWithResponses(server, opts...)`. Options include `mem0.WithRequestEditorFn`, `mem0.WithHTTPClient` for an HTTP client with timeouts, and `mem0.WithBaseURL`.
- Each operation has a raw method on `Client`, a parsed `XWithResponse` method on `ClientWithResponses`, and a `NewXRequest` constructor. JSON body operations also have `XWithBodyWithResponse` for a raw `io.Reader`.
- The complete spec is generated, including deprecated endpoints. Paths keep their trailing slashes.

## Operations

The client covers all 47 paths and 68 operations in the Mem0 spec.

| Method | Endpoint |
|---|---|
| `AgentsCreateWithResponse` | `POST /v1/agents/` |
| `AppsCreateWithResponse` | `POST /v1/apps/` |
| `EntitiesListWithResponse` | `GET /v1/entities/` |
| `EntitiesFiltersListWithResponse` | `GET /v1/entities/filters/` |
| `EntitiesDeleteV1WithResponse` | `DELETE /v1/entities/{entity_type}/{entity_id}/` (deprecated) |
| `EntitiesReadWithResponse` | `GET /v2/entities/{entity_type}/{entity_id}/` |
| `EntitiesDeleteWithResponse` | `DELETE /v2/entities/{entity_type}/{entity_id}/` |
| `EventsListWithResponse` | `GET /v1/events/` |
| `EventReadWithResponse` | `GET /v1/event/{event_id}/` |
| `ExportsCreateWithResponse` | `POST /v1/exports/` |
| `ExportsListWithResponse` | `POST /v1/exports/get/` |
| `MemoriesListWithResponse` | `GET /v1/memories/` (deprecated) |
| `MemoriesCreateWithResponse` | `POST /v1/memories/` (deprecated) |
| `MemoriesDeleteAllWithResponse` | `DELETE /v1/memories/` |
| `MemoriesListV2WithResponse` | `POST /v2/memories/` (deprecated) |
| `MemoriesEventsListWithResponse` | `GET /v1/memories/events/` |
| `MemoriesSearchCreateWithResponse` | `POST /v1/memories/search/` (deprecated) |
| `MemoriesSearchV2WithResponse` | `POST /v2/memories/search/` (deprecated) |
| `MemoriesListV3WithResponse` | `POST /v3/memories/` |
| `MemoriesAddV3WithResponse` | `POST /v3/memories/add/` |
| `MemoriesSearchV3WithResponse` | `POST /v3/memories/search/` |
| `MemoriesEntityReadWithResponse` | `GET /v1/memories/{entity_type}/{entity_id}/` |
| `MemoriesReadWithResponse` | `GET /v1/memories/{memory_id}/` |
| `MemoriesUpdateWithResponse` | `PUT /v1/memories/{memory_id}/` |
| `MemoriesDeleteWithResponse` | `DELETE /v1/memories/{memory_id}/` |
| `MemoriesHistoryListWithResponse` | `GET /v1/memories/{memory_id}/history/` |
| `RunsCreateWithResponse` | `POST /v1/runs/` |
| `StatsListWithResponse` | `GET /v1/stats/` |
| `PingReadWithResponse` | `GET /v1/ping/` |
| `SummaryCreateWithResponse` | `POST /v1/summary/` |
| `UsersCreateWithResponse` | `POST /v1/users/` |
| `SubmitFeedbackWithResponse` | `POST /v1/feedback/` |
| `OrganizationsReadWithResponse` | `GET /api/v1/orgs/organizations/` |
| `CreateOrganizationWithResponse` | `POST /api/v1/orgs/organizations/` |
| `GetOrganizationWithResponse` | `GET /api/v1/orgs/organizations/{org_id}/` |
| `DeleteOrganizationWithResponse` | `DELETE /api/v1/orgs/organizations/{org_id}/` |
| `GetOrganizationMembersWithResponse` | `GET /api/v1/orgs/organizations/{org_id}/members/` |
| `UpdateOrganizationMemberRoleWithResponse` | `PUT /api/v1/orgs/organizations/{org_id}/members/` |
| `AddOrganizationMemberWithResponse` | `POST /api/v1/orgs/organizations/{org_id}/members/` |
| `RemoveOrganizationMemberWithResponse` | `DELETE /api/v1/orgs/organizations/{org_id}/members/` |
| `GetProjectsWithResponse` | `GET /api/v1/orgs/organizations/{org_id}/projects/` |
| `CreateProjectWithResponse` | `POST /api/v1/orgs/organizations/{org_id}/projects/` |
| `GetProjectWithResponse` | `GET /api/v1/orgs/organizations/{org_id}/projects/{project_id}/` |
| `UpdateProjectWithResponse` | `PATCH /api/v1/orgs/organizations/{org_id}/projects/{project_id}/` |
| `DeleteProjectWithResponse` | `DELETE /api/v1/orgs/organizations/{org_id}/projects/{project_id}/` |
| `GetProjectMembersWithResponse` | `GET /api/v1/orgs/organizations/{org_id}/projects/{project_id}/members/` |
| `AddProjectMemberWithResponse` | `POST /api/v1/orgs/organizations/{org_id}/projects/{project_id}/members/` |
| `UpdateProjectMemberWithResponse` | `PUT /api/v1/orgs/organizations/{org_id}/projects/{project_id}/members/` |
| `DeleteProjectMemberWithResponse` | `DELETE /api/v1/orgs/organizations/{org_id}/projects/{project_id}/members/` |
| `MemoriesBatchUpdateWithResponse` | `PUT /v1/batch/` |
| `MemoriesBatchDeleteWithResponse` | `DELETE /v1/batch/` |
| `GetProjectWebhooksWithResponse` | `GET /api/v1/webhooks/projects/{project_id}/` |
| `CreateWebhookWithResponse` | `POST /api/v1/webhooks/projects/{project_id}/` |
| `UpdateWebhookWithResponse` | `PUT /api/v1/webhooks/{webhook_id}/` |
| `DeleteWebhookWithResponse` | `DELETE /api/v1/webhooks/{webhook_id}/` |
| `GetDreamConfigWithResponse` | `GET /api/v1/orgs/organizations/{org_id}/projects/{project_id}/dream/config/` |
| `UpdateDreamConfigWithResponse` | `PATCH /api/v1/orgs/organizations/{org_id}/projects/{project_id}/dream/config/` |
| `GetDreamStatsWithResponse` | `GET /api/v1/orgs/organizations/{org_id}/projects/{project_id}/dream/stats/` |
| `GetDreamActivityWithResponse` | `GET /api/v1/orgs/organizations/{org_id}/projects/{project_id}/dream/activity/` |
| `GetDreamRunsWithResponse` | `GET /api/v1/orgs/organizations/{org_id}/projects/{project_id}/dream/runs/` |
| `GetDreamRunMemoriesWithResponse` | `GET /api/v1/orgs/organizations/{org_id}/projects/{project_id}/dream/runs/{run_id}/memories/` |
| `GetDreamMemorySourcesWithResponse` | `GET /api/v1/orgs/organizations/{org_id}/projects/{project_id}/dream/memory/{memory_id}/sources/` |
| `DreamPreviewWithResponse` | `POST /api/v1/orgs/organizations/{org_id}/projects/{project_id}/dream/preview/` |
| `ProfilesReadWithResponse` | `GET /v2/entities/{entity_type}/{entity_id}/profile/` |
| `ProfilesSettingsReadWithResponse` | `GET /v2/profiles/settings/` |
| `ProfilesSettingsUpdateWithResponse` | `POST /v2/profiles/settings/` |
| `ProfilesCreateJobWithResponse` | `POST /v2/profiles/jobs/` |
| `ProfilesGetJobWithResponse` | `GET /v2/profiles/jobs/{job_id}/` |

## Responses

The success field follows the documented HTTP status, such as `JSON200` or `JSON202`. `Body`, `StatusCode()`, `Status()` and `HTTPResponse` expose the raw response. Some errors have typed status fields, while others have only the raw body. A nil Go error does not mean the HTTP status succeeded.

Unformatted numbers map to `float64`. Explicit `format: float` fields, including some search scores, remain `float32`. Optional properties are often pointers. Dates and UUIDs use the types emitted by oapi-codegen.

## Memory versions

Prefer V3 for new memory list, add and search calls. V3 list and search require filters containing at least one of `user_id`, `agent_id`, `app_id` or `run_id`. V3 search takes `MemoriesSearchV3JSONRequestBody` with `Query` and `Filters`, and returns an object with `Results`. V2 search returns an array and is deprecated in the spec. Several V1 memory operations remain the way to retrieve, update or delete a specific memory.

V3 list responses call the run scope `SessionId`, while V3 search responses call it `RunId`. Expired memories are hidden by default; `ShowExpired` includes them.

## Pagination

`MemoriesListV3WithResponse` takes `*MemoriesListV3Params` with `Page` and `PageSize`, plus a request body containing filters. Pages start at 1; page size is at most 200. The response includes `Count`, `Next`, `Previous` and `Results`. Continue while `Next` is non-nil, preserving the filters and incrementing the page. Query pagination parameters take precedence over those in the body.

Dream run pagination uses an opaque cursor instead. Pass the previous response's `next_cursor` to `GetDreamRunsParams.Cursor`. Other endpoints have their own generated params; inspect the operation before assuming a common pagination shape.

## Profile jobs

`ProfilesCreateJobWithResponse` requires an `Idempotency-Key` header through its generated params. The spec requires 8 to 128 characters. Reuse the same key for retries of the same job. Success is HTTP 202; inspect `JSON202` rather than `JSON200`.

## Rate limits

Inspect HTTP status and headers for rate limiting. The client does not retry automatically. Apply bounded backoff to retryable failures and preserve idempotency keys where the endpoint supports them.
