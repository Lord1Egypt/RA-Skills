# go-tinker: setup and reference

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.
- A Tinker API key in `TINKER_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-tinker
```

The package name is `tinker`:

```go
import "github.com/psyb0t/go-tinker"
```

## Client

- `tinker.NewClientWithResponses(server string, opts ...tinker.ClientOption)` builds the typed client. `server` is the base URL without a trailing path, for example `https://tinker.thinkingmachines.dev/services/tinker-prod`, the default of the official Python SDK.
- `tinker.WithRequestEditorFn(fn)` runs `fn` on every request. Set the `X-API-Key` header there, the only scheme the spec declares.
- `tinker.WithHTTPClient(c)` swaps in your own `*http.Client`, for timeouts or a proxy.
- Every method also takes trailing `reqEditors ...tinker.RequestEditorFn` for per-call headers.

## Endpoints

| Method | HTTP | Request body | `JSON200` |
|---|---|---|---|
| `CreateModelWithResponse` | `POST /api/v1/create_model` | `CreateModelRequest` | `*UntypedAPIFuture` |
| `UnloadModelWithResponse` | `POST /api/v1/unload_model` | `UnloadModelRequest` | `*UntypedAPIFuture` |
| `ForwardWithResponse` | `POST /api/v1/forward` | `ForwardJSONRequestBody` | `*UntypedAPIFuture` |
| `ForwardBackwardWithResponse` | `POST /api/v1/forward_backward` | `ForwardBackwardJSONRequestBody` | `*UntypedAPIFuture` |
| `OptimStepWithResponse` | `POST /api/v1/optim_step` | `OptimStepRequest` | `*UntypedAPIFuture` |
| `SaveWeightsWithResponse` | `POST /api/v1/save_weights` | `SaveWeightsRequest` | `*UntypedAPIFuture` |
| `LoadWeightsWithResponse` | `POST /api/v1/load_weights` | `LoadWeightsRequest` | `*UntypedAPIFuture` |
| `SaveWeightsForSamplerWithResponse` | `POST /api/v1/save_weights_for_sampler` | `SaveWeightsForSamplerRequest` | `*UntypedAPIFuture` |
| `SampleWithResponse` | `POST /api/v1/sample` | `SampleRequest` | `*SampleResponse` |
| `AsampleWithResponse` | `POST /api/v1/asample` | `SampleRequest` | `*UntypedAPIFuture` |
| `RetrieveFutureWithResponse` | `POST /api/v1/retrieve_future` | `UntypedAPIFuture` | union, see below |
| `GetInfoWithResponse` | `POST /api/v1/get_info` | `GetInfoRequest` | `*GetInfoResponse` |
| `GetServerCapabilitiesWithResponse` | `GET /api/v1/get_server_capabilities` | none | `*GetServerCapabilitiesResponse` |
| `ReceiveTelemetryWithResponse` | `POST /api/v1/telemetry` | `TelemetryBatch` | none, `JSON202` is `*TelemetryResponse` |
| `HealthCheckWithResponse` | `GET /api/v1/healthz` | none | `*HealthResponse` |

`ForwardJSONRequestBody` and `ForwardBackwardJSONRequestBody` are inline schemas with the input and `model_id`; the other bodies are aliases of the named schema types.

Response wrappers end in `HTTPResponse` (`CreateModelHTTPResponse`), because the spec's schema names already end in `Response`. Each wrapper has `Body []byte`, `HTTPResponse *http.Response`, `StatusCode()` and one field per documented status.

## Futures

1. A work call returns `UntypedAPIFuture{RequestId, ModelId}`.
2. Pass that value to `RetrieveFutureWithResponse`.
3. `JSON408` (`TryAgainResponse`) means the result is not ready. Call again later.
4. `JSON200` is a union. Decode it with the `As...` method for the call you made: `AsCreateModelResponse`, `AsForwardBackwardOutput`, `AsOptimStepResponse`, `AsSaveWeightsResponse`, `AsLoadWeightsResponse`, `AsSaveWeightsForSamplerResponse`, `AsUnloadModelResponse` and the others on `RetrieveFuture200JSONResponseBody`. The union holds raw JSON, so an `As...` call for the wrong kind can still succeed with empty fields. Decode with the method that matches the call that created the future.

## Errors

- A non-nil `error` from a method is a transport failure or a body that did not decode.
- An API error leaves `JSON200` nil and sets the status field, usually `JSON400` or `JSON404` with an `ErrorResponse` (`Error` code, `Message`, optional `Details`).
- A status the spec does not list leaves every typed field nil. Read `StatusCode()` and `Body`.

## Numbers

Every `number` in the spec is `float64` in Go, including the ones the spec marks `format: float`.
