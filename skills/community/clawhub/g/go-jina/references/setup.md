# go-jina: setup and reference

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.
- A Jina AI API key from https://jina.ai/api-dashboard/key-manager, read from `JINA_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-jina
```

```go
import (
	"github.com/psyb0t/go-jina"                    // package jina
	jinareader "github.com/psyb0t/go-jina/reader" // package jinareader
)
```

## Auth

Both APIs take `Authorization: Bearer <key>`. Set it with `jina.WithRequestEditorFn` or `jinareader.WithRequestEditorFn`, as the SKILL.md example shows. `GET /v1/models` and `GET /v1/models/{model_id}` work without a key, and the Reader answers without one at a lower rate limit.

## Operations in `jina`

Base URL `https://api.jina.ai`. Each method below also has a plain variant without `WithResponse` that returns `*http.Response`, and the body-taking ones have a `...WithBodyWithResponse` variant that takes a content type and an `io.Reader`.

| Method | HTTP |
|---|---|
| `EmbeddingsV1EmbeddingsPostWithResponse(ctx, jina.EmbeddingRequest)` | `POST /v1/embeddings` |
| `RerankV1RerankPostWithResponse(ctx, jina.RerankingRequest)` | `POST /v1/rerank` |
| `ListModelsV1ModelsGetWithResponse(ctx)` | `GET /v1/models` |
| `GetModelV1ModelsModelIdGetWithResponse(ctx, modelID)` | `GET /v1/models/{model_id}` |
| `ChatCompletionsV1ChatCompletionsPostWithResponse(ctx, jina.ChatCompletionRequest)` | `POST /v1/chat/completions` |
| `CreateBatchJobV1BatchEmbeddingsPostWithResponse(ctx, jina.BatchEmbeddingRequest)` | `POST /v1/batch/embeddings` |
| `GetBatchStatusV1BatchBatchIdGetWithResponse(ctx, batchID)` | `GET /v1/batch/{batch_id}` |
| `CancelBatchJobV1BatchBatchIdDeleteWithResponse(ctx, batchID)` | `DELETE /v1/batch/{batch_id}` |
| `ListBatchJobsV1BatchesGetWithResponse(ctx, *jina.ListBatchJobsV1BatchesGetParams)` | `GET /v1/batches` |
| `DownloadBatchOutputV1BatchBatchIdOutputGetWithResponse(ctx, batchID)` | `GET /v1/batch/{batch_id}/output` |
| `DownloadBatchErrorsV1BatchBatchIdErrorsGetWithResponse(ctx, batchID)` | `GET /v1/batch/{batch_id}/errors` |

## Union types

The spec uses `oneOf`/`anyOf` heavily. oapi-codegen turns each into a struct with `From<Variant>` (set), `Merge<Variant>` and `As<Variant>` (read) methods.

| Union | Variants |
|---|---|
| `EmbeddingRequest` | `EmbeddingsV2Request`, `EmbeddingsV3Request`, `EmbeddingsV4Request`, `EmbeddingsV5Request`, `CodeEmbeddings500MRequest`, `CodeEmbeddings1500MRequest`, `ClipV1Request`, `ClipV2Request`, `ColbertV1Request`, `ColbertV2Request` |
| `RerankingRequest` | `TextRerankerRequest`, `RerankerM0Request`, `RerankerV3Request` |
| `EmbeddingResponse_Data` | `AsEmbeddingResponseData0` (`[]SingleEmbeddingData`), `AsEmbeddingResponseData1` (`[]MultiEmbeddingData`, multi-vector models), `AsEmbeddingResponseData2` (sparse, `[]map[string]float64`) |
| `SingleEmbeddingData_Embedding` | `AsSingleEmbeddingDataEmbedding0` (base64 `string`), `AsSingleEmbeddingDataEmbedding1` (`[]float64`), `AsSingleEmbeddingDataEmbedding2` (sparse map) |
| `EmbeddingResponse_Usage` | `AsEmbeddingUsage`, `AsELSERV2EmbeddingUsage`, `AsBaseUsage` |

Each request variant has its own model enum, for example `EmbeddingsV3RequestModelJinaEmbeddingsV3` or `TextRerankerRequestModelJinaRerankerV2BaseMultilingual`. List them with `go doc -all github.com/psyb0t/go-jina | grep 'RequestModel'`. `embedding_type` takes one `EmbeddingType` value or a list of them.

## Reader (`jinareader`)

Base URL `https://r.jina.ai`.

| Method | HTTP |
|---|---|
| `GetTargetUrlWithResponse(ctx, targetURL, *GetTargetUrlParams)` | `GET /{url}` |
| `PostTargetUrlWithResponse(ctx, targetURL, *PostTargetUrlParams, PostTargetUrlJSONRequestBody)` | `POST /{url}` |
| `PostWithResponse(ctx, *PostParams, PostJSONRequestBody)` | `POST /` with the URL in the body's `Url` field |
| `GetWithResponse(ctx, *GetParams)` | `GET /` |
| `GetEphemeralEncodedFidWithResponse(ctx, encodedFid, *GetEphemeralEncodedFidParams)` | `GET /ephemeral/{encodedFid}` |
| `PostEphemeralEncodedFidWithResponse(ctx, encodedFid, *PostEphemeralEncodedFidParams, PostEphemeralEncodedFidJSONRequestBody)` | `POST /ephemeral/{encodedFid}` |

The params structs carry the Reader's header and query options (`Accept`, `XRespondWith`, `XTargetSelector`, `XWithLinksSummary`, `XNoCache` and many more). With `Accept: application/json`, `res.JSON200.Data` is a `FormattedPageDto0x41` with `Title`, `Url`, `Content`, `Links`, `Images` and the rest.

## Errors

| Situation | What you get |
|---|---|
| Network or encoding failure | non-nil `err` |
| HTTP 2xx with JSON | `res.JSON200` set |
| HTTP 4xx/5xx | `err == nil`, `res.JSON200 == nil`, the matching `res.JSONxxx` field set when the body was JSON, the raw body in `res.Body` |

In `jina` every error field is a `*ErrorResponse` with `Detail` and an optional `Code`. A 429 means the key's rate limit was hit.
