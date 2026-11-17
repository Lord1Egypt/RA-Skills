# go-label-studio: setup and reference

This module is unofficial and not affiliated with HumanSignal.

## Requirements

- Go 1.26.11 or newer, per the module's `go.mod`.
- A trusted Label Studio installation URL and user API token. The spec describes the token on Label Studio's User Account page.
- Export `LABEL_STUDIO_URL` and `LABEL_STUDIO_API_KEY` for the examples. These are application conventions; the client does not read environment variables itself.

## Install

```bash
go get github.com/psyb0t/go-label-studio
```

## Environments

Pass the origin of your self-hosted or cloud installation to `NewClientWithResponses`. The spec's example server is `http://localhost:8000`. Use HTTPS for remote installations and do not append `/api` to the origin.

## Auth

The `Token` scheme is an API key in the `Authorization` header. Use a request editor with `req.Header.Set("Authorization", "Token "+key)`. The generated client does not apply the spec's security scheme automatically.

## Client

- `labelstudio.NewClientWithResponses(server, opts...)`. Options include `labelstudio.WithRequestEditorFn`, `labelstudio.WithHTTPClient` for a custom `*http.Client` and timeouts, and `labelstudio.WithBaseURL`.
- Each operation has `Client.X` returning a raw `*http.Response`, `ClientWithResponses.XWithResponse` for a parsed response and `NewXRequest` to construct a request.
- Operations with bodies can also expose `XWithBodyWithResponse` for a raw `io.Reader`. Check the generated signature for JSON, form and multipart operations.

## Operations

The full provider spec has 376 paths and 592 operations. Its groups cover projects, tasks, annotations, predictions, imports, exports, storage backends, users, organizations, workspaces, webhooks, analytics and ML backends. Community Edition and Enterprise endpoint availability differs.

| Method | Endpoint |
|---|---|
| `ApiProjectsListWithResponse` | `GET /api/projects/` |
| `ApiProjectsRetrieveWithResponse` | `GET /api/projects/{id}/` |
| `ApiTasksListWithResponse` | `GET /api/tasks/` |
| `ApiTasksRetrieveWithResponse` | `GET /api/tasks/{id}/` |
| `ApiAnnotationsRetrieveWithResponse` | `GET /api/annotations/{id}/` |
| `ApiPredictionsListWithResponse` | `GET /api/predictions/` |
| `ApiUsersListWithResponse` | `GET /api/users/` |
| `ApiOrganizationsListWithResponse` | `GET /api/organizations/` |
| `ApiWorkspacesListWithResponse` | `GET /api/workspaces/` |
| `ApiWebhooksListWithResponse` | `GET /api/webhooks/` |
| `ApiMlListWithResponse` | `GET /api/ml/` |

## Responses

`JSON200` and other status fields hold decoded response bodies for the corresponding status and content type. `Body`, `HTTPResponse`, `StatusCode()` and `Status()` expose the raw response. Check the HTTP status even when the error return is nil. Not all endpoints return JSON; exports can return downloadable content.

Number fields map to `float64`. Optional fields are often pointers. Several response shapes depend on the caller's role, so check nullable fields before accessing them.

## Pagination

Project and task list params include `Page` and `PageSize`. Pagination differs across endpoint groups; inspect the operation's params and response instead of assuming a shared cursor. Request successive pages until the endpoint indicates there are no more results. The client makes one HTTP call per invocation and does not paginate automatically.

## Rate limits

The client does not retry automatically. Handle HTTP 429 and server errors in the calling application, respecting `Retry-After` when supplied. Avoid retrying data-changing operations unless you can establish that doing so is safe.
