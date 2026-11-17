---
name: "go-roark"
description: "Unofficial Go client for the Roark voice AI agent testing and monitoring API. Package roark (github.com/psyb0t/go-roark), generated with oapi-codegen, has typed methods for agents, calls and transcripts, chats, simulations, run plans, personas, metrics, webhooks and projects, authenticated with a bearer key. Use when Go code needs Roark API access or already imports github.com/psyb0t/go-roark."
license: MIT
homepage: https://github.com/psyb0t/go-roark
user-invocable: true
metadata:
  openclaw:
    emoji: "☎️"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the code you write talks HTTPS to api.roark.ai."
---

# go-roark

Unofficial, typed Go client for the Roark API, in package `roark` at the module root.

Read [references/setup.md](references/setup.md) before choosing an operation. It covers installation, project selection, operation names, pagination and response handling.

## Security & safety

- Read the bearer credential from `ROARK_API_KEY`. Never hardcode, commit or log it, and never print a request with its `Authorization` header.
- Use `https://api.roark.ai`. Project-scoped API keys are bound to one project. User-scoped credentials can select an accessible project through `X-Roark-Project-Id` in the request editor.
- Creating or deleting resources, starting simulations, collecting metrics, changing configuration and promoting a revision affect the project. Call those operations only when the user requested the action.
- Calls, transcripts, recordings and credentials may contain private data. Return only the data needed for the task.

## When to use

- Go code needs Roark agents, call or chat monitoring, transcripts, metrics or usage data.
- Go code needs to run voice AI simulations or manage Roark test resources, at the user's request.
- The project already imports `github.com/psyb0t/go-roark`.

## When NOT to use

- The code is not Go. This module ships only a Go package.
- You need a client maintained by Roark. This one is unofficial and not affiliated with Roark.
- You want to change the generated client itself. See `AGENTS.md` in the repository.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-roark`, from inside your module:

```bash
go doc github.com/psyb0t/go-roark ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-roark GetV1CallParams               # one method, params type or model
go doc -all github.com/psyb0t/go-roark                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-roark.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. The spec's operation IDs spell out the method and route, so `GET /v1/call/{callId}/transcript` is `GetV1CallByCallIdTranscriptWithResponse`.

## Usage

```go
package main

import (
	"context"
	"net/http"
	"os"

	"github.com/psyb0t/go-roark"
)

func main() {
	auth := roark.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
		req.Header.Set("Authorization", "Bearer "+os.Getenv("ROARK_API_KEY"))

		return nil
	})

	client, err := roark.NewClientWithResponses("https://api.roark.ai", auth)
	if err != nil {
		panic(err)
	}

	res, err := client.GetV1ProjectsWithResponse(context.Background())
	if err != nil {
		panic(err)
	}

	_ = res.JSON200
}
```

The example is also compiled in `example_test.go`. Inspect the current generated signatures before adding another operation. Supply a context and check the transport error, HTTP status and expected decoded response field. Finish by compiling and testing the calling project without making live API requests unless the user requested them.

The error return covers transport and decoding failures. An API error may return a nil `error` with `JSON200` nil. Check `StatusCode()` and the relevant error field or `Body`. Optional and nullable properties may be pointers; check them before dereferencing.
