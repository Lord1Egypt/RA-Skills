---
name: go-skyvern
description: Unofficial Go client for the Skyvern API, generated with oapi-codegen from the published OpenAPI document. Package skyvern (github.com/psyb0t/go-skyvern) provides typed REST methods for tasks, agents, runs, browser sessions and profiles, credentials, scripts, schedules, tags, artifacts and audit exports. Use when Go code needs Skyvern browser automation or already imports go-skyvern.
homepage: https://github.com/psyb0t/go-skyvern
license: MIT
user-invocable: true
metadata:
  openclaw:
    emoji: "🌐"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to Go source in the current project. The library reads and writes no files itself."
  shell: "The Go toolchain to add and compile the dependency."
  network: "Module installation fetches Go dependencies. Runtime requests send automation instructions and request data to api.skyvern.com, or an explicitly selected Skyvern deployment."
---

# go-skyvern

Unofficial, typed Go client for the Skyvern API, in package `skyvern` at the module root.

For setup, operations and response handling, see [references/setup.md](references/setup.md).

## Security & safety

- Read `SKYVERN_API_KEY` from the environment and send it in `x-api-key` with a request editor. Never hardcode, commit or log credentials or authenticated requests.
- Use `https://api.skyvern.com` for Skyvern Cloud. Use staging or a self-hosted deployment only when explicitly selected. Request bodies can contain browser instructions, URLs, credential references and sensitive data; send only what the requested task needs.
- Starting tasks, agents or scripts can interact with external websites and consume credits. Run, cancel, delete or change resources only when the user requested the action and only for resources owned by that task.

## When to use

- Go code needs to start or inspect Skyvern automation runs.
- Go code needs Skyvern agents, browser sessions, profiles, schedules or artifacts.
- The project already imports `github.com/psyb0t/go-skyvern`.

## When NOT to use

- The code is not Go. This module ships only a Go package.
- You need a client maintained by Skyvern. This client is unofficial.
- You want to change generated client code. See the repository's `AGENTS.md`.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-skyvern`, from inside your module:

```bash
go doc github.com/psyb0t/go-skyvern ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-skyvern RunTaskV1RunTasksPostParams   # one method, params type or model
go doc -all github.com/psyb0t/go-skyvern                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-skyvern.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. Many operations declare `x-api-key` as an optional header parameter, so their params type has an `XApiKey` field; pass nil params and let the request editor set the header.

## Usage

```go
auth := skyvern.WithRequestEditorFn(
	func(_ context.Context, req *http.Request) error {
		req.Header.Set("x-api-key", os.Getenv("SKYVERN_API_KEY"))

		return nil
	},
)

client, err := skyvern.NewClientWithResponses("https://api.skyvern.com", auth)
if err != nil {
	return err
}

res, err := client.GetVersionV1VersionGetWithResponse(ctx)
if err != nil {
	return err
}

_ = res.JSON200
```

Imports are `context`, `net/http`, `os` and `github.com/psyb0t/go-skyvern`. The complete compiling example is `example_test.go`.

Check `StatusCode()` and the matching status field before reading a response. A nil error means the request and decoding succeeded; HTTP error statuses remain in the response. Supply an `http.Client` with a timeout through `WithHTTPClient` when needed. The generated client does not poll runs or retry rate limits automatically.
