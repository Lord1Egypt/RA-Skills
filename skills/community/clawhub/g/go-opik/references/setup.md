# go-opik: setup and reference

This module is unofficial and not affiliated with Comet.

## Requirements

- Go 1.26.10 or newer, per `go.mod`.
- For Opik Cloud, an API key in `OPIK_API_KEY` and a workspace name in `OPIK_WORKSPACE`.

## Install

```bash
go get github.com/psyb0t/go-opik
```

## Environments

| Deployment | Base URL |
|---|---|
| Opik Cloud | `https://www.comet.com/opik/api` |
| Local self-hosted server | `http://localhost:5173/api` |

Keep `/api` in the base URL. Self-hosted deployments can use another host or authentication policy.

## Auth

Use `opik.WithRequestEditorFn` to set `req.Header.Set("Authorization", key)` and `req.Header.Set("Comet-Workspace", workspace)`. The authorization value is the bare key, without `Bearer `. The specification documents these headers in its introduction but does not declare a security scheme.

## Client

- `opik.NewClientWithResponses(server, opts...)` creates a typed response client.
- Options include `opik.WithRequestEditorFn`, `opik.WithHTTPClient` for a custom HTTP client and timeouts, and `opik.WithBaseURL`.
- Each operation has a raw `Client.X` method, a parsed `ClientWithResponses.XWithResponse` method and a `NewXRequest` request builder. Body operations also expose raw body variants.

## Operations

The complete published specification is generated, including UI and internal resources. Main operations include:

| Method | Endpoint |
|---|---|
| `FindProjectsWithResponse` | `GET /v1/private/projects` |
| `GetProjectByIdWithResponse` | `GET /v1/private/projects/{id}` |
| `CreateProjectWithResponse` | `POST /v1/private/projects` |
| `GetTracesByProjectWithResponse` | `GET /v1/private/traces` |
| `CreateTracesWithResponse` | `POST /v1/private/traces/batch` |
| `GetSpansByProjectWithResponse` | `GET /v1/private/spans` |
| `CreateSpansWithResponse` | `POST /v1/private/spans/batch` |
| `FindDatasetsWithResponse` | `GET /v1/private/datasets` |
| `FindExperimentsWithResponse` | `GET /v1/private/experiments` |
| `GetPromptsWithResponse` | `GET /v1/private/prompts` |

Names come from upstream operation IDs. Consult the generated method's parameters for required project IDs, filters and bodies.

## Responses

| Field or method | Holds |
|---|---|
| `JSON200` and other status fields | Decoded body for that status, nil otherwise |
| `Body`, `StatusCode()`, `Status()`, `HTTPResponse` | Raw response and HTTP status |

Unformatted number fields use `float64`. Optional fields can be nil. Check the HTTP status even when the Go error is nil.

## Pagination

Project listing takes `FindProjectsParams.Page` and `Size`, both optional integer pointers. The spec defaults to page 1 and size 10. The decoded project page has `Page`, `Size`, `Total` and `Content`; advance the page until the returned content covers the total. Other endpoints can use different pagination parameters, so inspect their generated types.

## Rate limits

The spec does not define one global request quota. Handle HTTP 429 and server errors in the calling application. The generated client adds no retry policy.
