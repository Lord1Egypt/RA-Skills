# go-cerebras: setup and reference

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.
- A Cerebras API key.

## Install

```bash
go get github.com/psyb0t/go-cerebras
```

The package name is `cerebras`:

```go
import "github.com/psyb0t/go-cerebras"
```

## Auth and base URL

The spec's security scheme is HTTP Bearer. Send the API key as `Authorization: Bearer <key>` through a request editor:

```go
auth := cerebras.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
	req.Header.Set("Authorization", "Bearer "+os.Getenv("CEREBRAS_API_KEY"))

	return nil
})

client, err := cerebras.NewClientWithResponses("https://api.cerebras.ai", auth)
```

The spec lists no server, so the base URL is always passed in. `WithHTTPClient` swaps the `*http.Client`, for timeouts or a custom transport.

## Methods

| Path | Method on `ClientWithResponses` | Auth |
|---|---|---|
| `POST /v1/chat/completions` | `ChatV1ChatCompletionsPostWithResponse` | Bearer |
| `POST /v1/completions` | `CompletionsV1CompletionsPostWithResponse` | Bearer |
| `GET /v1/models` | `ListModelsV1ModelsGetWithResponse` | Bearer |
| `GET /v1/models/{model_id}` | `GetModelV1ModelsModelIdGetWithResponse` | Bearer |
| `GET /public/v1/models` | `ListPublicModelsEndpointPublicV1ModelsGetWithResponse` | none |
| `GET /public/v1/models/{model_id}` | `GetPublicModelPublicV1ModelsModelIdGetWithResponse` | none |
| `GET /v1/tcp_warming` | `TcpWarmingV1TcpWarmingGetWithResponse` | none |

Each POST also has a `...WithBodyWithResponse(ctx, params, contentType, io.Reader)` form for a raw body. The plain `Client` has the same methods returning `*http.Response`, which is the way to read a streamed body.

Most methods take a params struct with optional headers from the spec (`X-Amz-Cf-Id`, `CF-RAY`, `X-delay-time`). Pass an empty struct when you don't need them.

## Unions

Several schemas are `anyOf` unions. oapi-codegen makes each one a struct with `From<Variant>`, `As<Variant>` and `Merge<Variant>` methods:

- `ChatCompletionRequest_Messages_Item`: `FromSystemMessageRequest`, `FromDeveloperMessageRequest`, `FromUserMessageRequest`, `FromAssistantMessageRequest`, `FromToolMessageRequest`.
- `UserMessageRequest_Content`: `FromUserMessageRequestContent0` for a plain string, `FromUserMessageRequestContent1` for content parts.
- `CreateChatCompletionResponse` (the chat `JSON200`): `AsChatCompletionResponse`, `AsChatChunkResponse`, `AsErrorChunkResponse`.
- `ListModelsV1ModelsGet200JSONResponseBody`: `AsModelMetadataList`, `AsOpenRouterModelsResponse`, `AsHuggingFaceModelsResponse`, matching the `format` query parameter.

## Responses and errors

- `res.JSON200` holds the decoded body for 200, `res.JSON422` the validation error.
- `res.StatusCode()` and `res.Body` are always set.
- The `error` return covers only transport and decoding failures. An API error is a non-2xx status with `JSON200 == nil`.

## Number fields

Every plain `number` in the spec is `float64`.
