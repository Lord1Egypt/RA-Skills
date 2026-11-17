---
name: go-morphik
description: Unofficial Go client for the Morphik API. Package morphik (github.com/psyb0t/go-morphik) covers ingestion, document management, retrieval, queries, models, cloud apps and connectors. Use when Go code needs Morphik document search, retrieval or ingestion, or already imports go-morphik.
license: MIT
homepage: https://github.com/psyb0t/go-morphik
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to Go source in the current project. Callers choose any files uploaded to Morphik."
  shell: "The Go toolchain (go get, go build, go test) to add and compile the dependency."
  network: "go get fetches the module from the configured Go module proxy. Runtime requests send selected documents, queries and credentials over HTTPS to api.morphik.ai or a user-selected Morphik deployment."
---

# go-morphik

Unofficial, typed Go client for the Morphik API, in package `morphik` at the module root.

For installation, operations, pagination and response fields, see [references/setup.md](references/setup.md).

## Security & safety

- Use bearer auth from `MORPHIK_API_KEY` through `WithRequestEditorFn`. Never hardcode, commit or log the key, and never print a request with its `Authorization` header.
- Default to `https://api.morphik.ai`, the vendor SDK's default. Send credentials and document contents only to that host or a Morphik deployment the user selected.
- Ingesting, updating or deleting documents, changing cloud apps, rotating tokens and managing connectors change remote state. Perform these operations only on task-owned resources and only when requested.

## When to use

- Go code needs document ingestion, document search, retrieval or completion queries through Morphik.
- Go code needs to read Morphik models, document status, metadata, usage or chat history.
- The project already imports `github.com/psyb0t/go-morphik`.

## When NOT to use

- The code is not Go. This module ships only a Go package.
- You need a client maintained by Morphik. This one is unofficial and not affiliated with Morphik.
- You want to change the generated client itself. See `AGENTS.md` in the repository.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-morphik`, from inside your module:

```bash
go doc github.com/psyb0t/go-morphik ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-morphik RetrieveRequest               # one method, params type or model
go doc -all github.com/psyb0t/go-morphik                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-morphik.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. Almost every Morphik operation has a params struct because of its optional `authorization` header parameter, so pass `&morphik.<OperationId>Params{}` when you set nothing in it.

## Usage

```go
package main

import (
	"context"
	"net/http"
	"os"

	"github.com/psyb0t/go-morphik"
)

func main() {
	auth := morphik.WithRequestEditorFn(
		func(_ context.Context, req *http.Request) error {
			req.Header.Set(
				"Authorization",
				"Bearer "+os.Getenv("MORPHIK_API_KEY"),
			)

			return nil
		},
	)

	client, err := morphik.NewClientWithResponses(
		"https://api.morphik.ai",
		auth,
	)
	if err != nil {
		panic(err)
	}

	res, err := client.GetAvailableModelsModelsGetWithResponse(
		context.Background(),
		&morphik.GetAvailableModelsModelsGetParams{},
	)
	if err != nil {
		panic(err)
	}

	_ = res.JSON200
}
```

Method names follow the spec's operation IDs. `ListDocsDocumentsPostWithResponse` lists documents with a JSON body, and `RetrieveDocumentsRetrieveDocsPostWithResponse` searches relevant documents with a `RetrieveRequest` body.

The error return covers transport and decoding failures. HTTP error responses can arrive with a nil error: check `StatusCode()` and the expected `JSON200` field before using it. Optional response fields may be pointers; check for nil before dereferencing.

The spec declares optional `authorization` header parameters rather than a security scheme. Passing empty params does not add auth; the request editor does. Multipart uploads use raw body methods and need a multipart writer plus its generated content type. This client does not add retries, pagination loops or streaming event decoding.
