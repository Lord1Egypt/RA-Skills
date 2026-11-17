# go-writer-ai: setup and reference

## Requirements

- Go 1.26.11 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.
- A Writer API key, from the API keys page of AI Studio, in `WRITER_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-writer-ai
```

The package name is `writer`:

```go
import "github.com/psyb0t/go-writer-ai"
```

## Client

- `writer.NewClientWithResponses(server string, opts ...writer.ClientOption)` returns the typed client.
- Base URL: `https://api.writer.com`. Paths in the spec already start with `/v1`.
- Options: `writer.WithRequestEditorFn(fn)` to add headers, `writer.WithHTTPClient(c)` for a custom `*http.Client` (timeouts, transport).
- Auth: a Bearer token in `Authorization` (the spec's `bearerAuth` scheme). The client never adds it on its own.

## Operations

| Area | Methods |
|---|---|
| Chat and text | `ChatWithResponse`, `CompletionsWithResponse` |
| Models | `ModelsWithResponse` |
| Files | `GatewayGetFilesWithResponse`, `GatewayGetFileWithResponse`, `GatewayUploadFileWithBodyWithResponse`, `GatewayDownloadFileWithResponse`, `GatewayDeleteFileWithResponse`, `GatewayRetryFailedFilesWithResponse` |
| Knowledge Graphs | `FindGraphsWithFileStatusWithResponse`, `CreateGraphWithResponse`, `FindGraphWithFileStatusWithResponse`, `UpdateGraphWithResponse`, `DeleteGraphWithResponse`, `AddFileToGraphWithResponse`, `RemoveFileFromGraphWithResponse`, `QuestionWithResponse` |
| No-code applications | `GetV1ApplicationsWithResponse`, `GetV1ApplicationsApplicationIdWithResponse`, `GenerateContentWithResponse`, `GetV1ApplicationsApplicationIdJobsWithResponse`, `PostV1ApplicationsApplicationIdJobsWithResponse`, `GetV1ApplicationsJobsJobIdWithResponse`, `PostV1ApplicationsJobsJobIdRetryWithResponse`, `GetV1ApplicationsApplicationIdGraphsWithResponse`, `PutV1ApplicationsApplicationIdGraphsWithResponse` |
| Tools | `PostV1ToolsPdfParserFileIdWithResponse`, `PostV1ToolsWebSearchWithResponse`, `PostV1VisionWithResponse` |

Each has a variant without `WithResponse` that returns the raw `*http.Response`, and most have a `WithBody` variant that takes any `io.Reader`. Graph and application IDs are `openapi_types.UUID` in some methods and `string` in others, as the spec declares them.

## Uploading a file

`GatewayUploadFileWithBodyWithResponse(ctx, params, contentType, body)` sends the reader as the raw request body. Set `contentType` to the file's MIME type and fill `writer.GatewayUploadFileParams` (it carries the `Content-Disposition` header with the file name).

## Streaming

With `Stream: true` in a chat or completion request the API answers with `text/event-stream`. Call `client.Chat(ctx, body)` from the embedded `ClientInterface` and read `resp.Body` line by line; each `data:` line of a chat stream decodes into `writer.ChatCompletionChunk`. Close the body when done.

## Errors

- A non-nil `err` is a transport or encoding failure.
- An API error is a response with `JSON200 == nil`. Check `StatusCode()` and read the raw `Body`.
