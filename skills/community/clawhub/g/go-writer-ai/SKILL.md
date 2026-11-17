---
name: go-writer-ai
description: Unofficial Go client for the Writer (writer.com) API, generated from Writer's OpenAPI spec. `writer.NewClientWithResponses("https://api.writer.com", auth)` from `github.com/psyb0t/go-writer-ai` gives typed methods for chat (`ChatWithResponse`), text completions (`CompletionsWithResponse`), models (`ModelsWithResponse`), files (`GatewayGetFilesWithResponse`, `GatewayUploadFileWithBodyWithResponse`), Knowledge Graphs (`CreateGraphWithResponse`, `QuestionWithResponse`), no-code applications (`GenerateContentWithResponse`), the PDF parser, web search and vision, with responses decoded into `JSON200`. Auth is a Bearer API key set through a `RequestEditorFn`. Use when Go code needs to call the Writer API or already imports go-writer-ai.
license: MIT
homepage: https://github.com/psyb0t/go-writer-ai
user-invocable: true
metadata:
  openclaw:
    emoji: "✍️"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files; uploads send only the reader you pass."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the client sends requests only to the base URL you pass, `https://api.writer.com`, over HTTPS."
---

# go-writer-ai

Typed Go client for the Writer API. Package `writer`, generated with oapi-codegen; every operation in the spec is a method on `ClientWithResponses`.

For install, the full operation list and streaming, see [references/setup.md](references/setup.md).

## Security & safety

- Read the API key from the `WRITER_API_KEY` environment variable. Never hardcode it, commit it, or log it, and never print request headers.
- Requests go only to the base URL you pass. Use `https://api.writer.com`.
- Prompts and uploaded files are sent to Writer. Upload files, and delete files or graphs, only when the user asked for it and only ones the task owns.

## When to use

- Go code needs Writer chat, completions, Knowledge Graph questions, file uploads or no-code application runs.
- The project already imports `github.com/psyb0t/go-writer-ai`.

## When NOT to use

- The code is not Go. Use Writer's official SDKs instead.
- You need a parsed streaming client. The generated client returns the raw `*http.Response` for `stream: true`; it does not parse server-sent events.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-writer-ai`, from inside your module:

```bash
go doc github.com/psyb0t/go-writer-ai ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-writer-ai ChatRequest                    # one method, params type or model
go doc -all github.com/psyb0t/go-writer-ai                           # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-writer-ai.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. Operations without an operation ID are named from the HTTP method and path, such as `GetV1ApplicationsWithResponse`, and file upload has only the `GatewayUploadFileWithBodyWithResponse` and `GatewayUploadFileWithTextBodyWithResponse` variants.

## Usage

```go
import (
	"context"
	"fmt"
	"net/http"
	"os"

	"github.com/psyb0t/go-writer-ai"
)

auth := writer.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
	req.Header.Set("Authorization", "Bearer "+os.Getenv("WRITER_API_KEY"))

	return nil
})

client, err := writer.NewClientWithResponses("https://api.writer.com", auth)
if err != nil {
	return err
}

models, err := client.ModelsWithResponse(ctx)
if err != nil {
	return err // transport error
}

if models.JSON200 == nil {
	return fmt.Errorf("models: %s", models.Status()) // API error, see models.Body
}

for _, model := range models.JSON200.Models {
	fmt.Println(model.Id, model.Name)
}
```

Chat:

```go
var content writer.ChatMessage_Content
if err := content.FromChatMessageContent0("hello"); err != nil {
	return err
}

res, err := client.ChatWithResponse(ctx, writer.ChatRequest{
	Model: "<model-id>", // an Id from Models
	Messages: []writer.ChatMessage{{
		Content: &content,
		Role:    writer.ChatMessageRequestRoleUser,
	}},
})
if err != nil {
	return err
}

if res.JSON200 == nil || len(res.JSON200.Choices) == 0 {
	return fmt.Errorf("chat: %s", res.Status())
}

fmt.Println(res.JSON200.Choices[0].Message.Content)
```

Check `JSON200` for nil before using it. On an error status the raw body is in `Body`.
