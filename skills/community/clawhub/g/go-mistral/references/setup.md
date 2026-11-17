# go-mistral: setup and reference

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.
- A Mistral AI API key, created in the API keys section of La Plateforme.

## Install

```bash
go get github.com/psyb0t/go-mistral
```

The package name is `mistral`:

```go
import "github.com/psyb0t/go-mistral"
```

## Auth

Mistral AI takes `Authorization: Bearer <api key>`. Add the header with a `RequestEditorFn`: for every request through `mistral.WithRequestEditorFn`, or for one call by passing it as the last argument of that method.

## Client options

| Option | Effect |
|---|---|
| `mistral.WithRequestEditorFn(fn)` | Runs `fn` on every request, used for the auth header. |
| `mistral.WithHTTPClient(doer)` | Replaces `http.DefaultClient`, for timeouts or transport settings. |
| `mistral.WithBaseURL(url)` | Overrides the server passed to the constructor. |

Base URL: `https://api.mistral.ai`. Paths in the spec already start with `/v1`.

## Calling operations

Method names come from the spec's operation IDs. Each operation `X` has:

- `client.XWithResponse(ctx, pathParams..., params, ...)` returning `*XResponse`.
- For operations with a JSON body, `client.XWithResponse(ctx, body)` takes the typed `XJSONRequestBody`, and `client.XWithBodyWithResponse(ctx, contentType, io.Reader)` takes raw bytes.

Some operations:

| Method | Request |
|---|---|
| `ListModelsV1ModelsGetWithResponse(ctx, *ListModelsV1ModelsGetParams)` | List models. |
| `ChatCompletionV1ChatCompletionsPostWithResponse(ctx, ChatCompletionRequest)` | Chat completion. |
| `EmbeddingsV1EmbeddingsPostWithResponse(ctx, EmbeddingsV1EmbeddingsPostJSONRequestBody)` | Embeddings. |

Run `go doc github.com/psyb0t/go-mistral ClientWithResponsesInterface` to find the rest. Do not guess a method name.

## Union types

Fields the spec types as one of several shapes are structs with `From<Variant>`, `As<Variant>` and `Merge<Variant>` methods:

- `ChatCompletionRequest_Messages_Item`: `FromUserMessage`, `FromSystemMessage`, `FromAssistantMessage`, `FromToolMessage`.
- `UserMessage_Content`: `FromUserMessageContent0` takes a plain `string`.
- `AssistantMessage_Content`: `AsAssistantMessageContent0` reads plain text as a `string`.

Run `go doc github.com/psyb0t/go-mistral <UnionType>` for the exact variant names of any other union.

## Responses

Every `XResponse` has:

- `Body []byte` and `HTTPResponse *http.Response`.
- `StatusCode()` and `Status()`.
- `JSON200` on success. Many operations also have `JSON422 *HTTPValidationError`, whose `Detail` lists `ValidationError` values with `Msg`, `Loc` and `Type`.

Other error statuses have no typed field; read `Body`. A method returns a non-nil error only for transport failures and bodies that do not decode.

## Regenerating

`client.gen.go` is generated. For changes to the client itself, see `AGENTS.md` in the repository.
