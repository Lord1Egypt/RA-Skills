# go-browser-use: setup and reference

This module is unofficial and not affiliated with Browser Use.

## Requirements

- Go 1.26.11 or newer, per `go.mod`.
- A Browser Use Cloud API key, provided as `BROWSER_USE_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-browser-use
```

## Base URL and auth

Use `https://api.browser-use.com/api/v4`. Paths below are relative to this URL. The spec's `APIKeyHeader` scheme uses the `X-Browser-Use-API-Key` header. Set it in `browseruse.WithRequestEditorFn` with `req.Header.Set("X-Browser-Use-API-Key", key)`. Read the full compilable example in the root README or `example_test.go`.

## Client

- `browseruse.NewClientWithResponses(server, opts...)` constructs the parsed client.
- Options include `WithRequestEditorFn`, `WithHTTPClient`, and `WithBaseURL`.
- Raw operations return `*http.Response`; their caller closes the body. Parsed `WithResponse` operations read and close it.
- Body operations also expose `WithBodyWithResponse` with a content type and `io.Reader`, useful for explicit null and multipart payloads.
- There is no automatic retry, polling, or pagination loop.

## Main operations

| Method | Endpoint |
| --- | --- |
| `CreateRunRunsPostWithResponse` | `POST /runs` |
| `ListRunsRunsGetWithResponse` | `GET /runs` |
| `GetRunRunsRunIdGetWithResponse` | `GET /runs/{run_id}` |
| `GetRunStatusRunsRunIdStatusGetWithResponse` | `GET /runs/{run_id}/status` |
| `GetRunEventsRunsRunIdEventsGetWithResponse` | `GET /runs/{run_id}/events` |
| `CancelRunRunsRunIdCancelPostWithResponse` | `POST /runs/{run_id}/cancel` |
| `ListRunAttachmentsRunsRunIdAttachmentsGetWithResponse` | `GET /runs/{run_id}/attachments` |
| `ListSessionsSessionsGetWithResponse` | `GET /sessions` |
| `GetSessionSessionsSessionIdGetWithResponse` | `GET /sessions/{session_id}` |
| `UpdateSessionSessionsSessionIdPatchWithResponse` | `PATCH /sessions/{session_id}` |
| `DeleteSessionSessionsSessionIdDeleteWithResponse` | `DELETE /sessions/{session_id}` |
| `PurgeSessionSessionsSessionIdPurgePostWithResponse` | `POST /sessions/{session_id}/purge` |
| `QueueSessionMessageSessionsSessionIdQueuePostWithResponse` | `POST /sessions/{session_id}/queue` |
| `ListSessionQueueSessionsSessionIdQueueGetWithResponse` | `GET /sessions/{session_id}/queue` |
| `GetSessionCostSessionsSessionIdCostGetWithResponse` | `GET /sessions/{session_id}/cost` |
| `CreateWorkspaceWorkspacesPostWithResponse` | `POST /workspaces` |
| `ListWorkspaceFilesWorkspacesWorkspaceIdFilesGetWithResponse` | `GET /workspaces/{workspace_id}/files` |
| `UploadWorkspaceFilesWorkspacesWorkspaceIdFilesUploadPostWithResponse` | `POST /workspaces/{workspace_id}/files/upload` |
| `CreateBrowserSessionBrowsersPostWithResponse` | `POST /browsers` |
| `ListBrowserSessionsBrowsersGetWithResponse` | `GET /browsers` |
| `GetBrowserSessionBrowsersSessionIdGetWithResponse` | `GET /browsers/{session_id}` |
| `UpdateBrowserSessionBrowsersSessionIdPatchWithResponse` | `PATCH /browsers/{session_id}` |
| `ListProfilesProfilesGetWithResponse` | `GET /profiles` |
| `CreateProfileProfilesPostWithResponse` | `POST /profiles` |
| `ListIntegrationsIntegrationsGetWithResponse` | `GET /integrations` |
| `ListExtensionsExtensionsGetWithResponse` | `GET /extensions` |

The generated package also covers session sharing, queue message lookup and cancellation, cost caps, workspace metadata and size, file deletion, extension uploads and deletion, downloads, wallets, Stripe Link status, and integration authorization, status, and disconnection. Path IDs use `github.com/google/uuid.UUID` through the runtime's UUID alias.

## Request types and responses

`RunCreateRequest` requires `Task`; optional fields include `Model`, `SessionId`, `WorkspaceId`, `BrowserSettings`, `OutputSchema`, and `MaxCostUsd`. Reuse `SessionId` for a follow-up run. Session queue calls take `QueueMessageRequest` with `Text` and optional `Interrupt`. Browser creation takes `CreateBrowserSessionRequest`.

Check the transport/decoding error first. Then check `StatusCode()` and the relevant success field: `JSON200` for most operations and `JSON201` for browser, profile, and extension creation. A 204 has no decoded JSON body. `Body`, `Status()`, and `HTTPResponse` expose the raw response. Only errors with JSON schemas have typed error fields; for example run creation exposes `JSON402` and `JSON422`.

Required fields are values, nullable and optional fields are often pointers. Optional nil pointers omit fields. For explicit null, call the raw-body variant, for example `UpdateSessionSessionsSessionIdPatchWithBodyWithResponse` with `{"title":null}`. Unformatted numbers are `float64`, but fixed-decimal cost response fields are strings. The `MaxCostUsd` union accepts either a numeric or decimal string value through its generated `FromRunCreateRequestMaxCostUsd0` and `FromRunCreateRequestMaxCostUsd1` helpers.

## Pagination and polling

Run and session lists take `Limit` and `Cursor`, returning `NextCursor` and `HasMore`. File lists and browser downloads also use cursor pagination. Browser, profile, and extension lists use `PageNumber`, `PageSize`, and `TotalItems`. Run events use `After` and `Limit`, returning `NextAfter` and `HasMore`; these are JSON pages, not a WebSocket stream.

Poll `GetRunStatusRunsRunIdStatusGetWithResponse` until `completed`, `failed`, or `cancelled`, then fetch the full run once. Treat HTTP 429 as a backoff signal; the generated client does not retry automatically.

## Uploads and secrets

Workspace uploads reserve files and return presigned PUT URLs. Send the bytes separately with matching content type and length; attach the returned file IDs to runs. Extension upload uses a multipart raw body. Use a separate client for storage transfers so request editors cannot forward API keys.

Secret bindings use a discriminated union of `InlineSecretSource` and `OnePasswordSecretSource`. Set its discriminator through the generated union helpers. Scope allowed domains to the requested task and never log the source values.
