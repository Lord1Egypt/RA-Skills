# go-weave: setup and reference

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.
- A W&B username in `WANDB_USERNAME` and an API key in `WANDB_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-weave
```

The package name is `weave`:

```go
import "github.com/psyb0t/go-weave"
```

## Client

- `weave.NewClientWithResponses(server string, opts ...weave.ClientOption)` builds the typed client. `server` is the trace server base URL: `https://trace.wandb.ai` for W&B's hosted service, the default of the official SDK, or the trace server URL of a dedicated or self-hosted instance.
- `weave.WithRequestEditorFn(fn)` runs `fn` on every request. Set HTTP Basic auth there with `req.SetBasicAuth(username, apiKey)`, the scheme the official SDK uses. The spec itself lists HTTP Bearer.
- `weave.WithHTTPClient(c)` swaps in your own `*http.Client`, for timeouts or a proxy.
- Every method also takes trailing `reqEditors ...weave.RequestEditorFn` for per-call headers.

The generated code is split in two files: the models in `types.gen.go`, the client in `client.gen.go`.

## Endpoint groups

| Group | Paths | Example method |
|---|---|---|
| Calls | `/call/start`, `/call/end`, `/call/read`, `/call/update`, `/call/upsert_batch`, `/calls/*` | `CallStartCallStartPostWithResponse` |
| Objects | `/obj/create`, `/obj/read`, `/obj/delete`, `/objs/query` | `ObjReadObjReadPostWithResponse` |
| Tables | `/table/*` | `TableQueryTableQueryPostWithResponse` |
| Files | `/file/create`, `/file/content`, `/files/query_stats` | `FileContentFileContentPostWithResponse` |
| Feedback | `/feedback/*` | `FeedbackCreateFeedbackCreatePostWithResponse` |
| Costs | `/cost/*` | `CostQueryCostQueryPostWithResponse` |
| Refs, threads, usage | `/refs/read_batch`, `/threads/stream_query`, `/trace/usage` | `RefsReadBatchRefsReadBatchPostWithResponse` |
| Annotation queues | `/annotation_queues/*` | `AnnotationQueueReadAnnotationQueuesQueueIdGetWithResponse` |
| Evaluations | `/evaluations/*` | `EvaluationStatusEvaluationsStatusPostWithResponse` |
| OTel | `/otel/v1/traces` | `ExportTraceOtelV1TracesPostWithResponse` |
| Agents | `/agents/*` | `GenaiAgentsQueryAgentsQueryPostWithResponse` |
| Completions and images | `/completions/create`, `/completions/create_stream`, `/image/create` | `CompletionsCreateCompletionsCreatePostWithResponse` |
| v2 resources | `/v2/{entity}/{project}/...` | `DatasetListV2EntityProjectDatasetsGetWithResponse` |
| Service | `/health`, `/version`, `/server_info`, `/geolocate` | `ServerInfoServerInfoGetWithResponse` |

The v2 methods take `entity` and `project` as path arguments instead of a `ProjectId` body field.

## Streaming responses

`POST /calls/stream_query`, `POST /threads/stream_query`, `POST /annotation_queues/query`, `POST /completions/create_stream` and the v2 list endpoints (datasets, evaluations, evaluation runs, models, ops, predictions, scorers, scores) answer with JSONL (`application/jsonl` or `application/x-ndjson`), one JSON object per line. The generated wrapper has no typed field for it. Read `Body` and decode it line by line with a `json.Decoder`, or use the plain `Client` method (no `WithResponse` suffix) to get the `*http.Response` and stream its body yourself.

## Errors

- A non-nil `error` from a method is a transport failure or a body that did not decode.
- A request the server rejects as invalid leaves `JSON200` nil and sets `JSON422` (`HTTPValidationError` with `Detail`).
- Any other status, such as 401 for bad credentials, leaves every typed field nil. Read `StatusCode()` and `Body`.

## Free-form values

Inputs, outputs, attributes and summaries are `map[string]interface{}` or `interface{}`, because the spec allows any JSON there. Numbers inside them decode as `float64`. Typed `number` fields are `float64` too.
