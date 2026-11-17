---
name: go-opik
description: Unofficial Go client for the Opik REST API, generated with oapi-codegen from the specification Comet publishes. Package opik (github.com/psyb0t/go-opik) has typed methods for projects, traces, spans, datasets, experiments, prompts, feedback scores, annotation queues and the other published endpoints. Use when Go code needs Opik LLM observability data or already imports go-opik.
license: MIT
homepage: https://github.com/psyb0t/go-opik
user-invocable: true
metadata:
  openclaw:
    emoji: "🔎"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to Go source in the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "Module downloads use the configured Go module proxy. Runtime requests go to https://www.comet.com/opik/api or the self-hosted Opik API URL the user selected."
---

# go-opik

Unofficial, typed Go client for the Opik REST API, in package `opik` at the module root.

For installation, operations, pagination and response fields, see [references/setup.md](references/setup.md).

## Security & safety

- Read the API key from `OPIK_API_KEY` and workspace from `OPIK_WORKSPACE`. Never hardcode, commit or log credentials or request headers.
- Cloud requests use `https://www.comet.com/opik/api`. Put the bare key in `Authorization`, without a `Bearer ` prefix, and the workspace in `Comet-Workspace`.
- Use a self-hosted server only when the user selected its URL. Its authentication policy may differ.
- Trace and span payloads can contain prompts, model output and other sensitive data. Send, update or delete data only for the action the user requested.

## When to use

- Go code needs to ingest or query Opik traces and spans.
- Go code needs Opik projects, datasets, experiments, prompts or evaluation feedback.
- The project already imports `github.com/psyb0t/go-opik`.

## When NOT to use

- The code is not Go. This module ships a Go package.
- You need a client maintained by Comet. This module is unofficial.
- You want to modify generated code. Read the repository's `AGENTS.md`.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-opik`, from inside your module:

```bash
go doc github.com/psyb0t/go-opik ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-opik FindProjectsParams            # one method, params type or model
go doc -all github.com/psyb0t/go-opik                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-opik.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status.

## Usage

```go
import (
	"context"
	"net/http"
	"os"

	"github.com/psyb0t/go-opik"
)

auth := opik.WithRequestEditorFn(
	func(_ context.Context, req *http.Request) error {
		req.Header.Set("Authorization", os.Getenv("OPIK_API_KEY"))
		req.Header.Set("Comet-Workspace", os.Getenv("OPIK_WORKSPACE"))

		return nil
	},
)

client, err := opik.NewClientWithResponses(
	"https://www.comet.com/opik/api",
	auth,
)
if err != nil {
	panic(err)
}

res, err := client.FindProjectsWithResponse(
	context.Background(),
	&opik.FindProjectsParams{},
)
if err != nil {
	panic(err)
}

_ = res.JSON200
```

Check `StatusCode()` and the decoded response field before reading it. The Go error covers transport and decoding failures; an HTTP error status does not produce a Go error by itself. Optional response fields can be nil.

The spec describes cloud auth in prose and declares no security scheme. Install the request editor explicitly. Base URLs include `/api`, while the main resource paths start with `/v1/private/` and OAuth paths use `/oauth/`.
