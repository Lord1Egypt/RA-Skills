---
name: go-tinker
description: Unofficial Go client for the Thinking Machines Tinker API, generated with oapi-codegen. `tinker.NewClientWithResponses(baseURL, auth)` from `github.com/psyb0t/go-tinker` gives typed methods for every endpoint of the Tinker training API (create and unload LoRA models, forward and forward-backward passes, optimizer steps, sampling, saving and loading weights, retrieving futures, server capabilities, health). Auth is an `X-API-Key` header set in a request editor. Use when Go code needs to call the Tinker API, or the project already imports go-tinker.
homepage: https://github.com/psyb0t/go-tinker
license: MIT
user-invocable: true
metadata:
  openclaw:
    emoji: "🧪"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the client sends HTTPS requests only to the Tinker base URL you pass, by default https://tinker.thinkingmachines.dev/services/tinker-prod."
---

# go-tinker

Typed Go client for the Thinking Machines Tinker API. Every endpoint is a method on `*tinker.ClientWithResponses`, and responses decode into `JSON200` and the other status fields.

For install, the endpoint table and the futures flow in detail, see [references/setup.md](references/setup.md).

## Security & safety

- Read the API key from the `TINKER_API_KEY` environment variable. Never hardcode it, commit it or log it, and never print request headers.
- Requests go only to the base URL the code passes to `NewClientWithResponses`. Use the default Tinker host unless the user names another one.
- Training calls (`CreateModel`, `ForwardBackward`, `OptimStep`, `SaveWeights`) use paid compute and `UnloadModel` drops a model's state. Make these calls only on models the task created or the user named, and only when the user asked for them.

## When to use

- Go code needs to train or sample from a model through the Tinker API.
- The project already imports `github.com/psyb0t/go-tinker`.

## When NOT to use

- The code is Python. Use Thinking Machines' official `tinker` package.
- You need the official SDK's extras: token-level training loops, retries, JWT credential exchange or the futures poller. This client sends single HTTP requests and leaves those to the caller.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-tinker`, from inside your module:

```bash
go doc github.com/psyb0t/go-tinker ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-tinker CreateModelRequest            # one method, params type or model
go doc -all github.com/psyb0t/go-tinker                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-tinker.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. The response wrappers are named `<OperationId>HTTPResponse`, not `<OperationId>Response`, because the spec's own schemas already use the `Response` names.

## Usage

```go
import (
	"context"
	"net/http"
	"os"

	"github.com/psyb0t/go-tinker"
)

auth := tinker.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
	req.Header.Set("X-API-Key", os.Getenv("TINKER_API_KEY"))

	return nil
})

client, err := tinker.NewClientWithResponses(
	"https://tinker.thinkingmachines.dev/services/tinker-prod",
	auth,
)
if err != nil {
	return err
}

caps, err := client.GetServerCapabilitiesWithResponse(ctx)
if err != nil {
	return err // transport error
}

if caps.JSON200 == nil {
	return fmt.Errorf("server capabilities: status %d: %s", caps.StatusCode(), caps.Body)
}

for _, model := range caps.JSON200.SupportedModels {
	_ = model.ModelName // *string
}
```

Most work calls return a future, not a result:

```go
created, err := client.CreateModelWithResponse(ctx, tinker.CreateModelRequest{
	BaseModel:  "<base-model-name>",
	LoraConfig: &tinker.LoraConfig{Rank: 16},
})
if err != nil {
	return err
}

if created.JSON200 == nil {
	return fmt.Errorf("create model: status %d", created.StatusCode())
}

result, err := client.RetrieveFutureWithResponse(ctx, *created.JSON200)
if err != nil {
	return err
}

if result.JSON408 != nil {
	// still running: call RetrieveFuture again later
}

if result.JSON200 != nil {
	model, err := result.JSON200.AsCreateModelResponse()
	if err != nil {
		return err
	}

	_ = model.ModelId // pass it to ForwardBackward, OptimStep, Sample and so on
}
```

Errors come back two ways: a non-nil `err` is a transport or decode failure, and an API error is a nil `JSON200` with `JSON400`, `JSON404` or another status field set (`ErrorResponse` with `Error` and `Message`). Always check `StatusCode()` or the matching field before using `JSON200`.
