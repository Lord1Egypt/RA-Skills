# go-llama-api: setup and reference

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.
- A Llama API key, from the API keys page of the Llama developer dashboard, in `LLAMA_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-llama-api
```

The package name is `llama`:

```go
import "github.com/psyb0t/go-llama-api"
```

## Client

- `llama.NewClientWithResponses(server string, opts ...llama.ClientOption)` returns the typed client.
- Base URL: `https://api.llama.com/v1`. The spec's own `servers` entry has no `/v1` prefix, so always pass the base URL.
- Options: `llama.WithRequestEditorFn(fn)` to add headers, `llama.WithHTTPClient(c)` for a custom `*http.Client` (timeouts, transport).
- Auth: a Bearer token in `Authorization`. The spec does not define the scheme, so the client never adds it on its own.

## Operations

| Method | HTTP |
|---|---|
| `CreateChatCompletionWithResponse(ctx, llama.CreateChatCompletionRequest)` | `POST /chat/completions` |
| `ListModelsWithResponse(ctx)` | `GET /models` |
| `RetrieveModelWithResponse(ctx, model)` | `GET /models/{model}` |
| `ModerationsWithResponse(ctx, llama.ModerationsJSONRequestBody)` | `POST /moderations` |
| `PostUploadsWithResponse(ctx, params, body)` | `POST /uploads` |
| `GetUploadsUploadIdWithResponse(ctx, uploadID, params)` | `GET /uploads/{upload_id}` |
| `PostUploadsUploadIdWithBodyWithResponse(ctx, uploadID, params, contentType, body)` | `POST /uploads/{upload_id}` |

Each has a variant without `WithResponse` that returns the raw `*http.Response`. Operations with a request body also have a `WithBody` variant that takes a content type and any `io.Reader`.

## Unions

Messages and contents are `oneOf` unions held as raw JSON. Write them with `From...` and read them with `As...`:

- `llama.Message`: `FromUserMessage`, `FromSystemMessage`, `FromToolResponseMessage`, `FromAssistantMessage`. Each sets `role`.
- `llama.UserMessage_Content`: `FromUserMessageContent0(string)` for text, `FromUserMessageContent1([]llama.UserMessageContentItem)` for mixed text and images.
- `AssistantMessage.Content`: `AsAssistantMessageContent0()` for text, `AsAssistantMessageContentItem()` for a content item.

## Streaming

With `Stream: true` in the request the API answers with `text/event-stream`. Call `client.CreateChatCompletion(ctx, body)` from the embedded `ClientInterface` and read `resp.Body` line by line; each `data:` line decodes into `llama.CreateChatCompletionResponseStreamChunk`. Close the body when done.

## Errors

- A non-nil `err` is a transport or encoding failure.
- An API error is a response with `JSON200 == nil`. Check `StatusCode()` and read `JSON400`, `JSON429`, `JSON500` or `JSONDefault`, or the raw `Body`.
- HTTP 429 is rate limiting; back off before retrying.
