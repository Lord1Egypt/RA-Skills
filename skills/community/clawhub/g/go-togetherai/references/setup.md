# go-togetherai: setup and reference

## Requirements

- Go 1.26.11 or newer, per the module's `go.mod`.
- A Together AI API key, created in the API keys section of the account settings.

## Install

```bash
go get github.com/psyb0t/go-togetherai
```

The package name is `together`. The module path ends in `go-togetherai`, so import it with an explicit name:

```go
import together "github.com/psyb0t/go-togetherai"
```

## Auth

Together AI takes `Authorization: Bearer <api key>`. The client sends no credentials by itself. Add the header with a `RequestEditorFn`, either for every request through `together.WithRequestEditorFn` or for one call by passing it as the last argument of that method.

## Client options

| Option | Effect |
|---|---|
| `together.WithRequestEditorFn(fn)` | Runs `fn` on every request, used for the auth header. |
| `together.WithHTTPClient(doer)` | Replaces `http.DefaultClient`, for timeouts or transport settings. |
| `together.WithBaseURL(url)` | Overrides the server passed to the constructor. |

Base URL: `https://api.together.ai`. The generated paths already include `/v1` or `/v2`, so one client reaches every operation.

## Calling operations

Each operation `X` in the spec has:

- `client.XWithResponse(ctx, pathParams..., params, ...)` returning a response struct.
- For operations with a JSON body, `client.XWithResponse(ctx, body)` takes the typed `XJSONRequestBody`, and `client.XWithBodyWithResponse(ctx, contentType, io.Reader)` takes raw bytes.

Some operations:

| Method | Request |
|---|---|
| `ModelsWithResponse(ctx, *ModelsParams)` | List models. `ModelsParams.Dedicated` filters to dedicated models; pass `nil` for all. |
| `ChatCompletionsWithResponse(ctx, ChatCompletionRequest)` | Chat completion. |
| `CompletionsWithResponse(ctx, CompletionsJSONRequestBody)` | Text completion. |
| `EmbeddingsWithResponse(ctx, EmbeddingsJSONRequestBody)` | Embeddings. Returns `*EmbeddingsResponse2`. |

Look up the rest with `go doc`, as the skill's "Finding endpoints and types" section shows. Do not guess a method name.

## Union types

Some spec fields are `oneOf` or `anyOf`, for example `ChatCompletionRequest.Messages` items (`ChatCompletionMessageParam`). oapi-codegen turns them into structs with `From<Variant>`, `As<Variant>` and `Merge<Variant>` methods, such as `FromChatCompletionUserMessageParam`. Building one by unmarshalling JSON, as in SKILL.md, also works and is usually shorter.

## Responses

Every response struct has:

- `Body []byte` and `HTTPResponse *http.Response`.
- `StatusCode()` and `Status()`.
- One `JSONnnn` field per documented status, set only when the response had that status. Error statuses (`JSON400`, `JSON401`, `JSON404`, `JSON429`, `JSON503` and so on) are mostly `*ErrorData`, with `Error.Message`, `Error.Type` and optional `Error.Code` and `Error.Param`. Some operations declare other error types, such as `*BatchErrorResponse` or `*QueueError`; check the field's type.

A method returns a non-nil error only for transport failures and bodies that do not decode.

## Regenerating

`client.gen.go` is generated. For changes to the client itself, see `AGENTS.md` in the repository.
