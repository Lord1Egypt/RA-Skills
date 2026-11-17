# go-skyvern: setup and reference

This module is unofficial and not affiliated with Skyvern.

## Requirements

- Go 1.26.11 or newer, per `go.mod`.
- A Skyvern API key from `https://app.skyvern.com/settings`, exported as `SKYVERN_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-skyvern
```

## Environments

| Environment | Base URL |
| --- | --- |
| Cloud | `https://api.skyvern.com` |
| Staging | `https://api-staging.skyvern.com` |
| Local | `http://localhost:8000` |

## Auth

The spec declares `ApiKeyAuth`, an API key in the `x-api-key` header. Use `WithRequestEditorFn` to set that header, as shown in the skill.

## Client

- `skyvern.NewClientWithResponses(server, opts...)` creates a parsed client. Options include `WithRequestEditorFn`, `WithHTTPClient` and `WithBaseURL`.
- Every operation has a raw `Client` method, a parsed `ClientWithResponses` method ending in `WithResponse`, and a `New...Request` function.
- Body operations also accept a raw `io.Reader` through their `WithBodyWithResponse` methods. File uploads use the spec's multipart media type, so use the raw body variant with a multipart writer.

## Main operations

| Operation | Endpoint |
| --- | --- |
| API version | `GET /v1/version` |
| Start a task | `POST /v1/run/tasks` |
| Start an agent | `POST /v1/run/agents` |
| List and inspect runs | `GET /v1/runs`, `GET /v1/runs/{run_id}` |
| Cancel a run | `POST /v1/runs/{run_id}/cancel` |
| Create and list agents | `POST /v1/agents`, `GET /v1/agents` |
| Browser sessions | `POST /v1/browser_sessions`, `GET /v1/browser_sessions` |
| Browser profiles | `POST /v1/browser_profiles`, `GET /v1/browser_profiles` |
| Credentials | `POST /v1/credentials`, `GET /v1/credentials` |
| Scripts | `POST /v1/scripts`, `GET /v1/scripts` |
| Schedules | `GET /v1/schedules` and `/v1/agents/{workflow_permanent_id}/schedules` |
| Artifacts | `GET /v1/runs/{run_id}/artifacts` |
| Audit exports | `GET /v1/audit-events/export` |

Operation IDs determine generated method names. Some retain `Workflow` in the name even though their route uses `/v1/agents`.

## Responses and pitfalls

- `JSON200` and other status fields hold decoded bodies when the response matches that status and media type. Check for nil before dereferencing pointer fields.
- `Body`, `StatusCode()`, `Status()` and `HTTPResponse` expose the raw response, including API errors.
- Number fields use `float64`.
- Starting a task or agent returns a run resource. Poll the relevant run endpoint to follow execution; the generated client does not wait for completion.
- Pagination parameters differ by endpoint. Inspect the generated params type and continue using the endpoint's documented pagination fields.
- The generated client does not add retries. Handle 429 and transient errors in the calling application.
