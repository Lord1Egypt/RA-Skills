# go-julep: setup and reference

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`. UUID fields use `github.com/google/uuid` through it.

## Install

```bash
go get github.com/psyb0t/go-julep
```

The package name is `julep`:

```go
import "github.com/psyb0t/go-julep"
```

## Client

- `julep.NewClientWithResponses(server string, opts ...ClientOption)` returns a `*ClientWithResponses`. Each method returns a typed response struct.
- `julep.NewClient` is the lower-level variant returning `*http.Response`.
- Options: `WithRequestEditorFn` (runs on every request, used for auth), `WithHTTPClient` (your own `*http.Client`, for timeouts and proxies), `WithBaseURL`.
- Every method also takes trailing `reqEditors ...RequestEditorFn` for per-call headers.
- Models are in `models.gen.go`, client methods in `client.gen.go`. Both are the same package.

## Auth

The spec's security scheme is an API key in the `Authorization` header. Julep's official SDKs send it as `Authorization: Bearer <key>`. Keys come from the Julep dashboard.

| Environment | Base URL |
|---|---|
| Production | `https://api.julep.ai/api` |
| Dev | `https://dev.julep.ai/api` |

## Method names

Method names are the spec's operation IDs, which repeat the path and HTTP method. Each has three forms: `X` (raw `*http.Response`), `XWithResponse` (typed), and for endpoints with a body `XWithBodyWithResponse` (raw body plus content type).

| Area | Typed methods (`...WithResponse`) |
|---|---|
| Agents | `ListAgentsAgentsGet`, `CreateAgentAgentsPost`, `GetAgentDetailsAgentsAgentIdGet`, `PatchAgentAgentsAgentIdPatch`, `UpdateAgentAgentsAgentIdPut`, `CreateOrUpdateAgentAgentsAgentIdPost`, `DeleteAgentAgentsAgentIdDelete`, `ListModelsAgentsModelsGet` |
| Agent docs | `ListAgentDocsAgentsAgentIdDocsGet`, `CreateAgentDocAgentsAgentIdDocsPost`, `DeleteAgentDocAgentsAgentIdDocsDocIdDelete`, `BulkDeleteAgentDocsAgentsAgentIdDocsDelete`, `SearchAgentDocsAgentsAgentIdSearchPost`, `GetDocDocsDocIdGet` |
| Agent tools | `ListAgentToolsAgentsAgentIdToolsGet`, `CreateAgentToolAgentsAgentIdToolsPost`, `PatchAgentToolAgentsAgentIdToolsToolIdPatch`, `UpdateAgentToolAgentsAgentIdToolsToolIdPut`, `DeleteAgentToolAgentsAgentIdToolsToolIdDelete` |
| Tasks | `ListTasksAgentsAgentIdTasksGet`, `CreateTaskAgentsAgentIdTasksPost`, `CreateOrUpdateTaskAgentsAgentIdTasksTaskIdPost`, `GetTaskDetailsTasksTaskIdGet` |
| Executions | `CreateTaskExecutionTasksTaskIdExecutionsPost`, `ListTaskExecutionsTasksTaskIdExecutionsGet`, `GetExecutionDetailsExecutionsExecutionIdGet`, `UpdateExecutionExecutionsExecutionIdPut`, `ListExecutionTransitionsExecutionsExecutionIdTransitionsGet`, `GetExecutionTransitionExecutionsExecutionIdTransitionsTransitionIdGet`, `StreamExecutionStatusExecutionsExecutionIdStatusStreamGet`, `StreamTransitionsEventsExecutionsExecutionIdTransitionsStreamGet` |
| Sessions | `ListSessionsSessionsGet`, `CreateSessionSessionsPost`, `GetSessionSessionsSessionIdGet`, `PatchSessionSessionsSessionIdPatch`, `UpdateSessionSessionsSessionIdPut`, `CreateOrUpdateSessionSessionsSessionIdPost`, `DeleteSessionSessionsSessionIdDelete`, `ChatSessionsSessionIdChatPost`, `GetSessionHistorySessionsSessionIdHistoryGet`, `RenderSessionsSessionIdRenderPost` |
| Users | `ListUsersUsersGet`, `CreateUserUsersPost`, `GetUserDetailsUsersUserIdGet`, `PatchUserUsersUserIdPatch`, `UpdateUserUsersUserIdPut`, `CreateOrUpdateUserUsersUserIdPost`, `DeleteUserUsersUserIdDelete` |
| User docs | `ListUserDocsUsersUserIdDocsGet`, `CreateUserDocUsersUserIdDocsPost`, `DeleteUserDocUsersUserIdDocsDocIdDelete`, `BulkDeleteUserDocsUsersUserIdDocsDelete`, `SearchUserDocsUsersUserIdSearchPost` |
| Files | `ListFilesFilesGet`, `CreateFileFilesPost`, `GetFileFilesFileIdGet`, `DeleteFileFilesFileIdDelete` |
| Secrets | `ListDeveloperSecretsSecretsGet`, `CreateDeveloperSecretSecretsPost`, `UpdateDeveloperSecretSecretsSecretIdPut`, `DeleteDeveloperSecretSecretsSecretIdDelete` |
| Other | `ListProjectsProjectsGet`, `CreateProjectProjectsPost`, `EmbedEmbedPost`, `GetJobStatusJobsJobIdGet`, `CheckHealthHealthzGet`, `DecodePayloadsTemporalDecodePost` |

Check `models.gen.go` and `client.gen.go` for the exact parameter and body types of a method before using it.

## Types

- Path IDs are `openapi_types.UUID`, an alias of `uuid.UUID`, so `uuid.Parse` produces one.
- Optional fields are pointers. Plain numbers are `float64`.
- Unions (`oneOf`/`anyOf`, common in task steps and chat content) are structs with `As...`/`From...` methods.
- List endpoints return a `ListResponse...` struct with `Items`.

## Errors

| Case | What you get |
|---|---|
| Network failure, bad URL, undecodable JSON | non-nil `err` |
| 200 or 201 | `JSON200` or `JSON201` set, per the endpoint |
| 422 | `JSON422` (`*HTTPValidationError`, list of `ValidationError` in `Detail`) |
| Any other status | `StatusCode()` and raw `Body`, typed fields nil |
