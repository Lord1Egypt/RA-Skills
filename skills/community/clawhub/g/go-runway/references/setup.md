# go-runway: setup and reference

## Requirements

- Go 1.26.11 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.
- A Runway API key, created in the Runway developer portal, in `RUNWAYML_API_SECRET`.

## Install

```bash
go get github.com/psyb0t/go-runway
```

The package name is `runway`:

```go
import "github.com/psyb0t/go-runway"
```

## Client and auth

- Base URL: `https://api.dev.runwayml.com`.
- `runway.NewClientWithResponses(baseURL, opts...)` returns the typed client. `runway.NewClient` returns the lower level one whose methods return `*http.Response`.
- Options: `runway.WithRequestEditorFn(fn)` runs `fn` on every request; `runway.WithHTTPClient(doer)` swaps the `http.Client`; `runway.WithBaseURL(url)` overrides the URL.
- Every request needs `Authorization: Bearer <key>` and `X-Runway-Version: 2024-11-06`. The spec declares the version header on each operation; the generator drops it from the method signatures, so the request editor sets both.

## Method names

The spec has no operation IDs, so names come from the HTTP method and path:

| Path | Methods |
|---|---|
| `/v1/organization` | `GetV1Organization` |
| `/v1/organization/usage` | `PostV1OrganizationUsage` |
| `/v1/tasks/{id}` | `GetV1TasksId`, `DeleteV1TasksId` |
| `/v1/text_to_image` | `PostV1TextToImage` |
| `/v1/image_to_video` | `PostV1ImageToVideo` |
| `/v1/text_to_video` | `PostV1TextToVideo` |
| `/v1/uploads` | `PostV1Uploads` |

Each has a `...WithResponse` variant on `ClientWithResponses`. Operations with a JSON body also have `...WithBody` / `...WithBodyWithResponse` variants that take a content type and an `io.Reader`. Look up the rest in `client.gen.go`; the method set is exactly the spec's 49 paths.

## Union types

Most request bodies and many responses are a `oneOf`. The generated Go type holds raw JSON with:

- `From<Variant>(v)` to set it from one variant struct.
- `As<Variant>()` to decode it as one variant. The spec's discriminators are dropped at generation time, so `As...` does not check which variant the JSON is; read the discriminating field first (`status`, `model`, `type`) and then decode the matching variant.
- `MarshalJSON` / `UnmarshalJSON`.

Variants are numbered in spec order: `PostV1TextToImageJSONBody0`, `...Body1` and so on. The variant's `Model` enum constants name the model, for example `PostV1TextToImageJSONBody1ModelGen4Image`.

The typed body methods (`PostV1TextToImageWithResponse(ctx, body)`) take a `...JSONRequestBody`, a named type without the union's `MarshalJSON`, so a union body is sent as `{}`. Marshal the `...JSONBody` value yourself and use `...WithBodyWithResponse(ctx, "application/json", reader)`.

## Tasks

Generation endpoints return a task id and an estimated cost. `GetV1TasksId` returns one of six variants, in this order:

| Variant | `status` | Extra fields |
|---|---|---|
| `GetV1TasksId200JSONResponseBody0` | `PENDING` | `EstimatedCost` |
| `GetV1TasksId200JSONResponseBody1` | `THROTTLED` | `EstimatedCost` |
| `GetV1TasksId200JSONResponseBody2` | `CANCELLED` | `Cost` |
| `GetV1TasksId200JSONResponseBody3` | `RUNNING` | `Progress`, `EstimatedCost` |
| `GetV1TasksId200JSONResponseBody4` | `FAILED` | `Failure`, `FailureCode`, `Cost` |
| `GetV1TasksId200JSONResponseBody5` | `SUCCEEDED` | `Output` (file URLs), `Cost` |

Poll with a delay between calls until the status is `SUCCEEDED`, `FAILED` or `CANCELLED`. `DeleteV1TasksId` cancels a running task or deletes a finished one.

## Errors

- A Go `error` from a method means the request did not complete or the response could not be read.
- An HTTP error status is not a Go error. Check `res.StatusCode()` and the matching field: `JSON400`, `JSON404`, `JSON429` and so on where the spec declares them. `res.Body` holds the raw response.
