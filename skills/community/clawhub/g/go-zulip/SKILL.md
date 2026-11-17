---
name: go-zulip
description: "Unofficial Go client for the Zulip REST API, generated with oapi-codegen. Package zulip (github.com/psyb0t/go-zulip) provides typed ...WithResponse methods on ClientWithResponses for messages, users, channels (streams), subscriptions, events long polling, uploads and organization administration, with HTTP Basic auth (email and API key) set through WithRequestEditorFn. Use when Go code needs to send or read Zulip messages, manage a Zulip organization, or already imports go-zulip."
license: MIT
homepage: https://github.com/psyb0t/go-zulip
user-invocable: true
metadata:
  openclaw:
    emoji: "💬"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "Module installation uses the configured Go module proxy. Runtime requests send credentials and request data only to the user's trusted Zulip HTTPS server."
---

# go-zulip

Unofficial, typed Go client for the Zulip REST API, in package `zulip` at the module root.

For install, operation names, request encoding and pagination, see [references/setup.md](references/setup.md).

## Security & safety

- Read the server URL, account or bot email and API key from `ZULIP_SERVER`, `ZULIP_EMAIL` and `ZULIP_API_KEY`. Never hardcode, commit or log credentials, or print an `Authorization` header.
- Use only the user's trusted HTTPS Zulip server, with `/api/v1` in the base URL. Request content and credentials leave the machine for that server.
- Sending, editing or deleting messages and changing users, channels or organization settings affect the Zulip organization. Perform those actions only when the user requests them, on the resources they specify.

## When to use

- Go code needs Zulip users, messages, channels, subscriptions or events.
- Go code needs to send messages or administer Zulip at the user's request.
- The project already imports `github.com/psyb0t/go-zulip`.

## When NOT to use

- The code is not Go. This module ships only a Go package.
- You need a client maintained by Zulip. This client is unofficial.
- You want to modify generated code. Read the repository's `AGENTS.md` instead.

## Finding endpoints and types

The usage below covers one call. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-zulip`, from inside your module:

```bash
go doc github.com/psyb0t/go-zulip ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-zulip GetMessagesParams              # one method, params type or model
go doc -all github.com/psyb0t/go-zulip                           # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-zulip.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. Operations with a URL-encoded form body are `<OperationId>WithFormdataBodyWithResponse` (for example `SendMessageWithFormdataBodyWithResponse` with a `SendMessageFormdataRequestBody`), and multipart uploads use `<OperationId>WithBodyWithResponse`.

## Usage

```go
import (
	"context"
	"net/http"
	"os"

	"github.com/psyb0t/go-zulip"
)

auth := zulip.WithRequestEditorFn(
	func(_ context.Context, req *http.Request) error {
		req.SetBasicAuth(
			os.Getenv("ZULIP_EMAIL"),
			os.Getenv("ZULIP_API_KEY"),
		)

		return nil
	},
)

client, err := zulip.NewClientWithResponses(
	os.Getenv("ZULIP_SERVER"),
	auth,
)
if err != nil {
	return err
}

res, err := client.GetOwnUserWithResponse(context.Background())
if err != nil {
	return err
}

_ = res.JSON200
```

Set `ZULIP_SERVER` to a URL such as `https://your-server.example/api/v1`. Check `StatusCode()` and `JSON200` before consuming the response. The error return covers request, transport and decoding failures; an API rejection can return a nil Go error.

Read the generated signature for the operation before writing a call. Many endpoints use URL-encoded forms. Zulip's event API is REST long polling; this module has no WebSocket package.
