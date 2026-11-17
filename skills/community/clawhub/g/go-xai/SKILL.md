---
name: go-xai
description: Unofficial Go client for the xAI (Grok) REST API at https://api.x.ai. `xai.NewClientWithResponses` from `github.com/psyb0t/go-xai` gives one typed method per endpoint, generated with oapi-codegen from xAI's OpenAPI document - chat completions, the Responses API, Anthropic style messages, embeddings, tokenization, image and video generation, files, skills, document search, models and API key info - with JSON 200 bodies decoded into Go structs. Auth is a bearer API key set through a request editor. Use when Go code needs to call the xAI API or already imports go-xai.
license: MIT
homepage: https://github.com/psyb0t/go-xai
user-invocable: true
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the client sends requests only to the base URL you pass, https://api.x.ai."
---

# go-xai

Typed Go client for the xAI API. Every endpoint in xAI's OpenAPI document is a method on `ClientWithResponses`.

For install, the method list, union types and error handling, see [references/setup.md](references/setup.md).

## Security & safety

- Read the API key from an environment variable such as `XAI_API_KEY`. Never hardcode it, commit it or log it, and never print request headers.
- Requests go only to the base URL passed to `NewClientWithResponses`. Use `https://api.x.ai`.
- Calls cost money and some change account state (file and skill uploads and deletes, stored response deletes, public file URLs). Make those calls only when the user asked for them, and only on resources the task created or named.

## When to use

- Go code needs Grok chat, responses, embeddings, image or video generation, or another xAI endpoint.
- The project already imports `github.com/psyb0t/go-xai`.

## When NOT to use

- The code is not Go.
- You need streaming. The generated methods read the whole response body; for server-sent events, use the plain `Client` method, which returns the `*http.Response` with the body unread, and parse the stream yourself.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-xai`, from inside your module:

```bash
go doc github.com/psyb0t/go-xai ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-xai ChatRequest                    # one method, params type or model
go doc -all github.com/psyb0t/go-xai                           # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-xai.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field holds the decoded body; it is nil for any other status, since the spec declares only 200 bodies. Most operation IDs follow `handle_<name>_request`, so the methods read `HandleModelsListRequestWithResponse`.

## Usage

```go
import (
	"context"
	"fmt"
	"net/http"
	"os"

	"github.com/psyb0t/go-xai"
)

auth := xai.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
	req.Header.Set("Authorization", "Bearer "+os.Getenv("XAI_API_KEY"))

	return nil
})

client, err := xai.NewClientWithResponses("https://api.x.ai", auth)
if err != nil {
	return err
}

models, err := client.HandleModelsListRequestWithResponse(ctx)
if err != nil {
	return err // transport error
}

if models.JSON200 == nil {
	return fmt.Errorf("list models: status %d: %s", models.StatusCode(), models.Body)
}

for _, model := range models.JSON200.Data {
	fmt.Println(model.Id)
}
```

A chat completion. Messages and message content are unions, built with `From...` helpers (`Message2` is the user message, `Content0` is plain text):

```go
var content xai.Content
if err := content.FromContent0("Say hello"); err != nil {
	return err
}

var msg xai.Message
if err := msg.FromMessage2(xai.Message2{Content: content, Role: xai.Message2RoleUser}); err != nil {
	return err
}

model := "<model-id>" // pick one from the models list
messages := []xai.Message{msg}

res, err := client.HandleGenericCompletionRequestWithResponse(ctx, xai.ChatRequest{
	Model:    &model,
	Messages: &messages,
})
if err != nil {
	return err
}

if res.JSON200 == nil {
	return fmt.Errorf("chat: status %d: %s", res.StatusCode(), res.Body)
}

if len(res.JSON200.Choices) > 0 && res.JSON200.Choices[0].Message.Content != nil {
	fmt.Println(*res.JSON200.Choices[0].Message.Content)
}
```
