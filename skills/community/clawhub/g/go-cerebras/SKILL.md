---
name: go-cerebras
description: Writes Go code with go-cerebras (package cerebras, github.com/psyb0t/go-cerebras), an unofficial client for the Cerebras Inference API generated with oapi-codegen. `cerebras.NewClientWithResponses("https://api.cerebras.ai", cerebras.WithRequestEditorFn(...))` gives typed methods for every path of the spec, including chat completions (`ChatV1ChatCompletionsPost`), text completions (`CompletionsV1CompletionsPost`), model listing and lookup, and TCP warming. Union schemas come with `As...`/`From...` helpers. Use when Go code needs to call Cerebras inference, or already imports go-cerebras.
license: MIT
homepage: https://github.com/psyb0t/go-cerebras
user-invocable: true
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the client sends HTTPS requests only to the base URL you give it, normally https://api.cerebras.ai."
---

# go-cerebras

Typed Go client for the Cerebras Inference API. Every operation in the spec is a method on `ClientWithResponses`, named after its operation ID.

For install, the method list, unions and error handling in detail, see [references/setup.md](references/setup.md).

## Security & safety

- Read the API key from an environment variable such as `CEREBRAS_API_KEY`. Never hardcode it, commit it or log it, and never print request headers.
- Requests go only to the base URL passed to `NewClientWithResponses`. Prompts sent through the client reach Cerebras.

## When to use

- Go code calls Cerebras for chat or text completions, or lists the models it serves.
- The project already imports `github.com/psyb0t/go-cerebras`.

## When NOT to use

- You need streaming. The generated client returns the whole body; for `stream: true` call the plain `Client` method and read the body of the `*http.Response` it returns yourself.
- The code is not Go. Use Cerebras's own SDKs.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-cerebras`, from inside your module:

```bash
go doc github.com/psyb0t/go-cerebras ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-cerebras ChatCompletionRequest         # one method, params type or model
go doc -all github.com/psyb0t/go-cerebras                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-cerebras.

Method names come from the spec's operation IDs, which include the path and HTTP method (`ChatV1ChatCompletionsPost`). `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON422` and so on, per declared status) holds the decoded body; it is nil for any other status. Chat and model list bodies are unions, decoded with their `As...` methods.

## Usage

```go
import (
	"context"
	"fmt"
	"net/http"
	"os"

	"github.com/psyb0t/go-cerebras"
)

auth := cerebras.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
	req.Header.Set("Authorization", "Bearer "+os.Getenv("CEREBRAS_API_KEY"))

	return nil
})

client, err := cerebras.NewClientWithResponses("https://api.cerebras.ai", auth)
if err != nil {
	return err
}

var content cerebras.UserMessageRequest_Content
if err := content.FromUserMessageRequestContent0("Say hi"); err != nil {
	return err
}

role := cerebras.UserMessageRequestRoleUser

var msg cerebras.ChatCompletionRequest_Messages_Item
if err := msg.FromUserMessageRequest(cerebras.UserMessageRequest{Content: content, Role: &role}); err != nil {
	return err
}

res, err := client.ChatV1ChatCompletionsPostWithResponse(ctx,
	&cerebras.ChatV1ChatCompletionsPostParams{},
	cerebras.ChatCompletionRequest{Model: "<model-id>", Messages: []cerebras.ChatCompletionRequest_Messages_Item{msg}},
)
if err != nil {
	return err // transport error
}

if res.JSON200 == nil {
	return fmt.Errorf("chat: status %d: %s", res.StatusCode(), res.Body)
}

completion, err := res.JSON200.AsChatCompletionResponse()
if err != nil {
	return err
}

fmt.Println(*completion.Choices[0].Message.Content)
```

Listing models:

```go
res, err := client.ListModelsV1ModelsGetWithResponse(ctx, &cerebras.ListModelsV1ModelsGetParams{})
if err != nil {
	return err
}

list, err := res.JSON200.AsModelMetadataList()
```

Check `JSON200` for nil before reading it. A non-2xx status is not a Go error; the status is in `StatusCode()` and the raw body in `Body`.
