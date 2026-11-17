---
name: go-mistral
description: Unofficial Go client for the Mistral AI REST API, generated with oapi-codegen. `mistral.NewClientWithResponses("https://api.mistral.ai", opts...)` from `github.com/psyb0t/go-mistral` returns a `*mistral.ClientWithResponses` with one typed method per endpoint, named after the spec's operation IDs (`ChatCompletionV1ChatCompletionsPostWithResponse`, `ListModelsV1ModelsGetWithResponse`, `EmbeddingsV1EmbeddingsPostWithResponse` and more). Auth is a bearer API key set through `mistral.WithRequestEditorFn`; union fields such as message content use `From...` and `As...` methods. Use when Go code needs to call Mistral AI or already imports go-mistral.
license: MIT
homepage: https://github.com/psyb0t/go-mistral
user-invocable: true
metadata:
  openclaw:
    emoji: "🌬️"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "HTTPS to the Mistral AI API at api.mistral.ai, and `go get` to your Go module proxy."
---

# go-mistral

Typed Go client for the Mistral AI API. Every endpoint in Mistral AI's OpenAPI document is a method on `ClientWithResponses`.

For install, client options, more operations, union types and response handling, see [references/setup.md](references/setup.md).

## Security & safety

- Read the API key from an environment variable such as `MISTRAL_API_KEY`. Never hardcode it, commit it or log it, and never print request headers.
- Requests go only to the base URL you pass, `https://api.mistral.ai`. Prompts and files you send are processed by Mistral AI.
- Batch jobs cost money, and delete endpoints remove data. Call them only when the user asked for that action.

## When to use

- Go code needs Mistral AI chat completions, embeddings, model listing, files, fine-tuned models or other Mistral AI endpoints.
- The project already imports `github.com/psyb0t/go-mistral`.

## When NOT to use

- You want streaming token by token. The `...WithResponse` methods read the whole body; a streamed reply needs your own SSE reader on the `*http.Response` from the raw `Client`.
- The code is not Go.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-mistral`, from inside your module:

```bash
go doc github.com/psyb0t/go-mistral ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-mistral ChatCompletionRequest         # one method, params type or model
go doc -all github.com/psyb0t/go-mistral                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-mistral.

Method names come from the spec's operation IDs, which repeat the path and HTTP method (`ListModelsV1ModelsGet`). `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status.

## Usage

```go
import (
	"context"
	"fmt"
	"net/http"
	"os"

	"github.com/psyb0t/go-mistral"
)

auth := mistral.WithRequestEditorFn(
	func(_ context.Context, req *http.Request) error {
		req.Header.Set(
			"Authorization",
			"Bearer "+os.Getenv("MISTRAL_API_KEY"),
		)

		return nil
	},
)

client, err := mistral.NewClientWithResponses("https://api.mistral.ai", auth)
if err != nil {
	return err
}
```

A chat completion. Message content and the messages list are union types, built with `From...` methods:

```go
var content mistral.UserMessage_Content
if err := content.FromUserMessageContent0("hello"); err != nil {
	return err
}

role := mistral.UserMessageRoleUser

var message mistral.ChatCompletionRequest_Messages_Item
err = message.FromUserMessage(
	mistral.UserMessage{Content: &content, Role: &role},
)
if err != nil {
	return err
}

res, err := client.ChatCompletionV1ChatCompletionsPostWithResponse(
	ctx,
	mistral.ChatCompletionRequest{
		Model:    "<model-id>",
		Messages: []mistral.ChatCompletionRequest_Messages_Item{message},
	},
)
if err != nil {
	return err // transport failure
}

if res.JSON200 == nil {
	return fmt.Errorf("mistral: status %d", res.StatusCode())
}

for _, choice := range res.JSON200.Choices {
	if choice.Message.Content == nil {
		continue
	}

	text, err := choice.Message.Content.AsAssistantMessageContent0()
	if err == nil {
		fmt.Println(text)
	}
}
```

Listing models: `client.ListModelsV1ModelsGetWithResponse(ctx, &mistral.ListModelsV1ModelsGetParams{})`, with the result in `res.JSON200.Data`.

A method returns an error only when the request could not be sent or the body could not be decoded. An API error is a normal response: check `StatusCode()`; a 422 also fills `JSON422`, an `*HTTPValidationError`, and every status leaves the raw reply in `Body`.
