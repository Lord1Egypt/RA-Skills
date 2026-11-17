---
name: go-postgrid
description: "Unofficial Go client for the PostGrid print and mail and address verification APIs. Package postgrid (github.com/psyb0t/go-postgrid), generated with oapi-codegen, has typed methods for contacts, templates, letters, postcards, cheques, self mailers, campaigns, mailing lists, reports, webhooks and address verification, authenticated with an API key in the X-API-Key header. Use when Go code needs to send physical mail, manage PostGrid print and mail resources or verify addresses, or already imports go-postgrid."
license: MIT
homepage: https://github.com/psyb0t/go-postgrid
user-invocable: true
metadata:
  openclaw:
    emoji: "📬"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to Go source in the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from the Go module proxy. At runtime the written code calls https://api.postgrid.com."
---

# go-postgrid

Unofficial, typed Go client for PostGrid print and mail and address verification, in package `postgrid` at the module root.

Read [references/setup.md](references/setup.md) for installation, operation groups, pagination and response handling. Inspect the generated method signatures before writing a call.

## Security & safety

- Set `X-API-Key` through `WithRequestEditorFn`. Read the key from `POSTGRID_API_KEY`; never hardcode, commit or log it.
- Use `https://api.postgrid.com`. The spec has separate print and mail and address verification security schemes. Select the key for the API being called.
- Print and mail test or live behavior depends on the key. Use a test key while developing. Creating mail with a live key can send physical mail and incur charges.
- Create, send, cancel or delete resources only when the user requested that action. Do not retry mail creation after an uncertain response without checking whether the first request succeeded.

## When to use

- Go code needs PostGrid contacts, templates, letters, postcards, cheques, self mailers, campaigns, mailing lists, reports or webhooks.
- Go code needs standard, international, batch or bulk address verification.
- The project already imports `github.com/psyb0t/go-postgrid`.

## When NOT to use

- The code is not Go. This module ships only a Go package.
- A PostGrid-maintained client is required. This client is unofficial.
- The task changes the generated client itself. Read `AGENTS.md` in the repository.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-postgrid`, from inside your module:

```bash
go doc github.com/psyb0t/go-postgrid ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-postgrid ContactsListParams            # one method, params type or model
go doc -all github.com/psyb0t/go-postgrid                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-postgrid.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. Operations that accept both JSON and multipart bodies have combined operation IDs and so longer names, such as `LettersCreateJSONLettersCreateMultipartWithResponse`.

## Usage

```go
import (
    "context"
    "net/http"
    "os"

    "github.com/psyb0t/go-postgrid"
)

auth := postgrid.WithRequestEditorFn(
    func(_ context.Context, req *http.Request) error {
        req.Header.Set("X-API-Key", os.Getenv("POSTGRID_API_KEY"))

        return nil
    },
)

client, err := postgrid.NewClientWithResponses(
    "https://api.postgrid.com",
    auth,
)
if err != nil {
    return err
}

res, err := client.ContactsListWithResponse(
    context.Background(),
    &postgrid.ContactsListParams{},
)
if err != nil {
    return err
}

_ = res.JSON200
```

Check `StatusCode()` and the status-specific response fields before consuming a response. The Go error covers transport and decoding failures; an HTTP error can return a nil Go error. Optional model fields may be pointers, so check them before dereferencing.

Finish by compiling the calling code and testing it against a local HTTP server. Tests must not create live mail or call PostGrid.
