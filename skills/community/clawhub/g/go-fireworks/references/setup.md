# go-fireworks: setup and reference

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.
- A Fireworks AI API key.

## Install

```bash
go get github.com/psyb0t/go-fireworks
```

The package name is `fireworks`:

```go
import "github.com/psyb0t/go-fireworks"
```

## Auth

The spec's security scheme is HTTP Bearer. Send the API key as `Authorization: Bearer <key>` through a request editor:

```go
auth := fireworks.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
	req.Header.Set("Authorization", "Bearer "+os.Getenv("FIREWORKS_API_KEY"))

	return nil
})
```

`WithHTTPClient` swaps the `*http.Client`, for timeouts or a custom transport.

## Base URLs

One client has one base URL. The spec splits its paths over two:

| Base URL | Paths |
|---|---|
| `https://api.fireworks.ai` | everything under `/v1/accounts/...`, plus `/v1/accounts`, `/v1/auth/refresh`, `/v1/creditCodes:redeem`, `/v1/validateModelConfig` |
| `https://api.fireworks.ai/inference` | `/v1/chat/completions`, `/v1/completions`, `/v1/messages`, `/v1/responses`, `/v1/responses/{response_id}` |

Calling an inference method on the control plane client hits the wrong URL and returns 404.

## Method names

Names come from the spec's operation IDs:

- Control plane methods have a `Gateway` prefix: `GatewayGetAccount`, `GatewayListModels`, `GatewayCreateDeployment`, `GatewayListDeployments`.
- Inference methods carry the full ID: `CreateChatCompletionV1ChatCompletionsPost`, `CreateCompletionV1CompletionsPost`, `MessagesPost`, `CreateResponseV1ResponsesPost`, `ListResponsesV1ResponsesGet`, `GetResponseV1ResponsesResponseIdGet`, `DeleteResponseV1ResponsesResponseIdDelete`.

Each operation has these forms on `ClientWithResponses`:

- `<Op>WithResponse(ctx, pathArgs..., params, body)` returns a typed `*<Op>Response` (some end in `Response2` where a schema already took the plain name).
- `<Op>WithBodyWithResponse(ctx, ..., contentType, io.Reader)` for a raw body.

The plain `Client` has the same methods returning `*http.Response`, which is the way to read a streamed body.

Run `go doc github.com/psyb0t/go-fireworks ClientWithResponsesInterface` to list every method, and `go doc github.com/psyb0t/go-fireworks <Type>` for a request, response or params type.

## Responses and errors

- `res.JSON200` holds the decoded body for 200; other documented statuses get their own fields such as `JSON422`.
- `res.StatusCode()` and `res.Body` are always set.
- The `error` return covers only transport and decoding failures. An API error is a non-2xx status with `JSON200 == nil`.

## Union fields

Fields that are one of several types (`ChatMessage_Content`) are structs with `From<Variant>`, `As<Variant>` and `Merge<Variant>` methods. A plain string message content is `ChatMessageContent0`.

## Number fields

Every plain `number` in the spec is `float64`.
