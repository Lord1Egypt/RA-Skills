---
name: go-vectara
description: Unofficial Go client for the Vectara API v2. Package vectara (github.com/psyb0t/go-vectara) has typed methods for corpora, documents, search, RAG queries, chats, agents, tools, pipelines and account administration. Use when Go code needs Vectara or already imports go-vectara.
license: MIT
homepage: https://github.com/psyb0t/go-vectara
user-invocable: true
metadata:
  openclaw:
    emoji: "💹"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the code you write talks HTTPS to api.vectara.io only."
---

# go-vectara

Unofficial, typed Go client for the Vectara API v2, in package `vectara` at the module root.

For installation, operations, pagination and response fields, see [references/setup.md](references/setup.md).

## Security & safety

- Read an API key from `VECTARA_API_KEY` and send it in `x-api-key`. Never hardcode, commit or log credentials or authentication headers.
- Use `https://api.vectara.io` as the base URL. Generated paths include `/v2`.
- OAuth uses a bearer access token. Visitor tokens and federated bearer credentials work only on operations declaring those schemes.
- Creating, updating, deleting or resetting resources changes account data. Run those operations only when the user requests them. Queries and agent execution may consume account resources or invoke configured tools.

## When to use

- Go code needs Vectara corpora, documents, retrieval or RAG queries.
- Go code needs Vectara chats, agents, tools or pipelines.
- The project imports `github.com/psyb0t/go-vectara`.

## When not to use

- The code is not Go. This module ships only a Go package.
- You need a client maintained by Vectara. This client is unofficial.
- You want to change the generated client. See `AGENTS.md` in the repo.

## Finding endpoints and types

The usage below covers one call. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-vectara`, from inside your module:

```bash
go doc github.com/psyb0t/go-vectara ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-vectara ListCorporaParams              # one method, params type or model
go doc -all github.com/psyb0t/go-vectara                           # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-vectara.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. Almost every operation takes a params struct, because the spec declares request timeout headers on them; pass `nil` when you set none. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status.

## Usage

Set `x-api-key` with a request editor, create the client, then call an operation. This is the repo's `example_test.go`:

```go
import (
	"context"
	"net/http"
	"os"

	"github.com/psyb0t/go-vectara"
)

auth := vectara.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
	req.Header.Set("x-api-key", os.Getenv("VECTARA_API_KEY"))

	return nil
})

client, err := vectara.NewClientWithResponses("https://api.vectara.io", auth)
if err != nil {
	return err
}

res, err := client.ListCorporaWithResponse(context.Background(), nil)
if err != nil {
	return err
}

_ = res.JSON200 // *vectara.ListCorporaResponse
```

Check `err` for request construction, transport and decoding failures. Check `StatusCode()` and the expected success field such as `JSON200` for API failures. A non-2xx response can have a nil Go error. Optional fields may be pointers; check before dereferencing.

The client does not paginate, retry or refresh OAuth tokens automatically. For server-sent events, call the raw method, decode the stream yourself and close the response body. Parsed response methods read the full body.
