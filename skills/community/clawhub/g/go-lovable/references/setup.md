# go-lovable: setup and reference

This module is unofficial and not affiliated with Lovable.

## Requirements

- Go 1.26.10 or newer, per `go.mod`.
- A Lovable key created at `lovable.dev/settings/api-keys`, exported as `LOVABLE_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-lovable
```

## Base URL and auth

Use `https://api.lovable.dev`, without `/v1`, because generated paths include that prefix. In `lovable.WithRequestEditorFn`, set `req.Header.Set("Lovable-API-Key", os.Getenv("LOVABLE_API_KEY"))`. Alternatively set `Authorization` to `Bearer ` plus the key or session/OAuth token. Read credentials from the environment and keep them out of logs.

Keys are workspace-scoped. Each operation documents the required project or workspace scope. Write scopes include the corresponding read scope. Another workspace's resources return 404; insufficient scope returns 403. The optional `LovableVersion` params field sets the stable version header; `LovableBeta` selects beta revisions when available.

## Client

- `lovable.NewClientWithResponses(server, opts...)` returns the parsed client.
- Options include `WithRequestEditorFn`, `WithHTTPClient` and `WithBaseURL`.
- Each operation has a raw `Client.X` method, a parsed `XWithResponse` method and a `NewXRequest` constructor. Operations with a body also accept a raw reader through `XWithBodyWithResponse`.
- The README and `example_test.go` contain the same compiling usage example.

## Operations

| Parsed method | Endpoint |
| --- | --- |
| `ListProjectsWithResponse` | `GET /v1/projects` |
| `GetProjectWithResponse` | `GET /v1/projects/{project_id}` |
| `UpdateProjectWithResponse` | `PATCH /v1/projects/{project_id}` |
| `DeleteProjectWithResponse` | `DELETE /v1/projects/{project_id}` |
| `CreateEmbedUrlWithResponse` | `POST /v1/projects/{project_id}/embed-url` |
| `PublishProjectWithResponse` | `POST /v1/projects/{project_id}/publish` |
| `UpdatePublishSettingsWithResponse` | `PATCH /v1/projects/{project_id}/publish` |
| `UnpublishProjectWithResponse` | `DELETE /v1/projects/{project_id}/publish` |
| `GetDeploymentWithResponse` | `GET /v1/projects/{project_id}/publish/{deployment_id}` |
| `ListPiiLabelsWithResponse` | `GET /v1/projects/{project_id}/pii-labels` |
| `ListSecurityScansWithResponse` | `GET /v1/projects/{project_id}/security-scans` |
| `GetSecurityScanWithResponse` | `GET /v1/projects/{project_id}/security-scans/{scan_id}` |
| `ListSecurityScanFindingsWithResponse` | `GET /v1/projects/{project_id}/security-scans/{scan_id}/findings` |
| `GetProjectAnalyticsWithResponse` | `GET /v1/projects/{project_id}/analytics` |
| `GetProjectAnalyticsBreakdownsWithResponse` | `GET /v1/projects/{project_id}/analytics/breakdowns` |
| `GetProjectRealtimeAnalyticsWithResponse` | `GET /v1/projects/{project_id}/analytics/realtime` |
| `ListWorkspacesWithResponse` | `GET /v1/workspaces` |
| `GetWorkspaceWithResponse` | `GET /v1/workspaces/{workspace_id}` |
| `ListWorkspaceGroupsWithResponse` | `GET /v1/workspaces/{workspace_id}/groups` |
| `ListWorkspaceMembersWithResponse` | `GET /v1/workspaces/{workspace_id}/members` |
| `GetWorkspaceMemberWithResponse` | `GET /v1/workspaces/{workspace_id}/members/{user_id}` |
| `GetWorkspaceAnalyticsWithResponse` | `GET /v1/workspaces/{workspace_id}/analytics` |
| `GetSecurityInsightsWithResponse` | `GET /v1/workspaces/{workspace_id}/security-center/insights` |
| `ListSecurityInsightProjectsWithResponse` | `GET /v1/workspaces/{workspace_id}/security-center/insights/projects` |

`GetWorkspaceMember` takes `openapi_types.UUID` for the user ID. Request bodies include `UpdateProjectRequest`, `PublishProjectRequest`, `UpdatePublishSettingsRequest` and `CreateEmbedURLRequest`; the generated `...JSONRequestBody` aliases are accepted by the client.

## Responses

`JSON200` holds successful reads and updates, `JSON202` holds an accepted deployment, and an HTTP 204 has no JSON body. `Body`, `StatusCode()`, `Status()` and `HTTPResponse` expose the raw result. HTTP failures have typed status fields such as `JSON400`, `JSON401`, `JSON403`, `JSON404`, `JSON429` and `JSON503`. Inspect `ErrorResponse.Type` for a machine-readable reason and `RequestId` for support diagnostics. The Go error only covers transport or decoding failure.

Numbers use `float64` unless the schema specifies an integer. Nullable fields use `nullable.Nullable[T]`, whose `IsNull()` and `Get()` methods distinguish JSON null from a value. Optional fields are pointers. New enum values may arrive; handle unknown strings explicitly.

## Pagination and long-running operations

List responses contain `Data`, `Pagination.HasMore` and `Pagination.NextCursor`. Read the cursor with `Get()` and pass its value as `Cursor` on the next request until `HasMore` is false. Keep filters fixed. Project listing requires a `WorkspaceId` slice and serializes it as repeated query parameters. There is no automatic page traversal.

Publishing returns a deployment ID before completion. Poll `GetDeploymentWithResponse` no more than once every two seconds, back off toward ten seconds and stop at a bounded deadline. `completed` has a URL; `error` has diagnostic fields. Handle unknown values without assuming success or automatically retrying the mutation.

Honor `Retry-After` on HTTP 429. A 503 response timeout means the wait expired, and the mutation may still finish. Read the resource state before retrying a write.
