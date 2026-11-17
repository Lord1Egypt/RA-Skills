---
name: go-weave
description: Unofficial Go client for the W&B Weave trace server API, generated with oapi-codegen. `weave.NewClientWithResponses(baseURL, auth)` from `github.com/psyb0t/go-weave` gives typed methods for every endpoint of the Weave trace server (start, end, read and query calls, objects, tables, files, feedback, costs, refs, threads, annotation queues, evaluations, agents, completions, OTel trace export, and the v2 datasets, models, ops, scorers, scores, predictions and evaluation runs). Auth is HTTP Basic with the W&B username and API key, set in a request editor. Use when Go code needs to log traces to Weave or read them back, or the project already imports go-weave.
license: MIT
homepage: https://github.com/psyb0t/go-weave
user-invocable: true
metadata:
  openclaw:
    emoji: "🐝"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the client sends HTTPS requests only to the trace server base URL you pass, by default https://trace.wandb.ai."
---

# go-weave

Typed Go client for the W&B Weave trace server. Every endpoint is a method on `*weave.ClientWithResponses`, and responses decode into `JSON200` and the other status fields.

For install, the endpoint groups, streaming responses and errors, see [references/setup.md](references/setup.md).

## Security & safety

- Read the credentials from `WANDB_USERNAME` and `WANDB_API_KEY`. Never hardcode them, commit them or log them, and never print request headers.
- Trace inputs and outputs you send go to the trace server base URL the code passes, `https://trace.wandb.ai` unless the user runs a dedicated or self-hosted W&B instance.
- The delete and purge endpoints (`CallsDelete`, `ObjDelete`, `CostPurge`, `FeedbackPurge` and the v2 `...Delete...` methods) remove project data. Call them only on data the task created or the user named, and only when the user asked.

## When to use

- Go code needs to record calls (spans) in Weave, attach feedback or costs, or query traces, objects and tables.
- The project already imports `github.com/psyb0t/go-weave`.

## When NOT to use

- The code is Python or TypeScript. Use the official `weave` package, which also wraps functions as ops automatically.
- You only export OpenTelemetry spans. An OTLP exporter pointed at the Weave OTel endpoint does that without this client.

## Finding endpoints and types

The example below covers a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-weave`, from inside your module:

```bash
go doc github.com/psyb0t/go-weave ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-weave StartedCallSchemaForInsert     # one method, params type or model
go doc -all github.com/psyb0t/go-weave                           # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-weave.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. The operation IDs are FastAPI's, so names repeat the handler, path and method, as described under the example.

## Usage

```go
import (
	"context"
	"net/http"
	"os"
	"time"

	"github.com/psyb0t/go-weave"
)

auth := weave.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
	req.SetBasicAuth(os.Getenv("WANDB_USERNAME"), os.Getenv("WANDB_API_KEY"))

	return nil
})

client, err := weave.NewClientWithResponses("https://trace.wandb.ai", auth)
if err != nil {
	return err
}

started, err := client.CallStartCallStartPostWithResponse(ctx, weave.CallStartReq{
	Start: weave.StartedCallSchemaForInsert{
		ProjectId:  "<entity>/<project>",
		OpName:     "my-op",
		StartedAt:  time.Now().UTC(),
		Inputs:     map[string]interface{}{"prompt": "hello"},
		Attributes: map[string]interface{}{},
	},
})
if err != nil {
	return err // transport error
}

if started.JSON200 == nil {
	return fmt.Errorf("call start: status %d: %s", started.StatusCode(), started.Body)
}

read, err := client.CallReadCallReadPostWithResponse(ctx, weave.CallReadReq{
	ProjectId: "<entity>/<project>",
	Id:        started.JSON200.Id,
})
if err != nil {
	return err
}

if read.JSON200 != nil && read.JSON200.Call != nil {
	_ = read.JSON200.Call.OpName
}
```

Method names come from FastAPI operation IDs: handler name, path, HTTP method. `CallReadCallReadPost` is `POST /call/read`, `ServerInfoServerInfoGet` is `GET /server_info`. Most bodies carry `ProjectId` as `<entity>/<project>`.

Errors come back two ways: a non-nil `err` is a transport or decode failure, and an API error is a nil `JSON200` with `JSON422` (`HTTPValidationError`) or no typed field set. Always check `StatusCode()` before using `JSON200`.
