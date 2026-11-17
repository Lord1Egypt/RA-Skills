---
name: go-zeroentropy
description: "Unofficial Go client for the ZeroEntropy retrieval API, generated with oapi-codegen from the full public OpenAPI spec. Package zeroentropy (github.com/psyb0t/go-zeroentropy) provides typed ...WithResponse methods on ClientWithResponses for collections, documents, top-documents, top-pages and top-snippets retrieval queries, reranking, embeddings, indexing status, usage and administration, with a bearer API key set through WithRequestEditorFn. Use when Go code needs ZeroEntropy search, reranking or embeddings, or a project already imports go-zeroentropy."
license: MIT
homepage: https://github.com/psyb0t/go-zeroentropy
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
  network: "`go get` fetches the module from the Go module proxy. Runtime requests use api.zeroentropy.dev or eu-api.zeroentropy.dev."
---

# go-zeroentropy

Unofficial, typed Go client for the ZeroEntropy API, in package `zeroentropy` at the module root.

Read [references/setup.md](references/setup.md) before choosing methods or writing requests. It lists authentication, all operations, pagination and response pitfalls.

## Security & safety

- Read the API key from `ZEROENTROPY_API_KEY`. The request editor sets `Authorization: Bearer <key>`. Never hardcode, commit or log the key, authorization header or document download tokens.
- Use `https://api.zeroentropy.dev/v1` or `https://eu-api.zeroentropy.dev/v1`. Select the region that holds the user's data. Keep `/v1` in the base URL.
- Creating or deleting collections, adding, updating or deleting documents, and changing organizations or API keys act on the account. Call them only when the user requested that action. Queries and model calls can incur usage charges.
- Use an `httptest` server for tests. Do not send test documents or keys to the live service.

## When to use

- Go code needs ZeroEntropy retrieval, reranking or embeddings.
- Go code needs collections, documents, indexing status, usage or administration.
- The project already imports `github.com/psyb0t/go-zeroentropy`.

## When not to use

- The code is not Go. This module ships only a Go package.
- The task requires a client maintained by ZeroEntropy. This client is unofficial and unaffiliated.
- The task changes the generated client itself. Read the repository's `AGENTS.md` instead.

## Finding endpoints and types

The usage below covers one call. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-zeroentropy`, from inside your module:

```bash
go doc github.com/psyb0t/go-zeroentropy ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-zeroentropy TopDocumentsRequest            # one method, params type or model
go doc -all github.com/psyb0t/go-zeroentropy                           # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-zeroentropy.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status.

## Usage

Install `github.com/psyb0t/go-zeroentropy`, create a `ClientWithResponses` with `WithRequestEditorFn`, and call `GetCollectionListCollectionsGetCollectionListPostWithResponse` with `EmptyRequest{}` to list collections. This is the repository's `example_test.go`:

```go
import (
	"context"
	"net/http"
	"os"

	"github.com/psyb0t/go-zeroentropy"
)

auth := zeroentropy.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
	req.Header.Set("Authorization", "Bearer "+os.Getenv("ZEROENTROPY_API_KEY"))

	return nil
})

client, err := zeroentropy.NewClientWithResponses("https://api.zeroentropy.dev/v1", auth)
if err != nil {
	return err
}

res, err := client.GetCollectionListCollectionsGetCollectionListPostWithResponse(
	context.Background(),
	zeroentropy.EmptyRequest{},
)
if err != nil {
	return err
}

_ = res.JSON200 // *zeroentropy.GetCollectionListResponse
```

The error return covers transport and decoding failures. HTTP errors require inspecting `StatusCode()` and `Body`; a nil Go error does not prove success. Read `JSON200.CollectionNames` only after checking `JSON200` for nil. Some successful calls use another status, such as 201 for a newly added document.

Method names retain the operation IDs, including their resource and HTTP verb suffixes. Most reads use POST. Scores and numeric embeddings use `float64`; nullable or optional fields can be pointers, while required fields can be values. Check the generated type before constructing a request.

Finish by compiling and testing the consumer's code, checking the selected host and ensuring every account mutation matches the user's request.
