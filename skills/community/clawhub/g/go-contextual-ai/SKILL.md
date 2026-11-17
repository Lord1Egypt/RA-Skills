---
name: go-contextual-ai
description: Writes Go code with go-contextual-ai (package contextual, github.com/psyb0t/go-contextual-ai), an unofficial client for the Contextual AI API generated with oapi-codegen. `contextual.NewClientWithResponses(baseURL, opts...)` gives a typed method for every endpoint in Contextual AI's OpenAPI spec (agents, agent queries, datastores, documents, extraction, generate, LMUnit, parse jobs, rerank, billing, users), with request structs and decoded `JSON200`/`JSON422` response fields. Auth is a bearer API key added through a request editor. Use when Go code needs to call the Contextual AI API, or already imports go-contextual-ai.
license: MIT
homepage: https://github.com/psyb0t/go-contextual-ai
user-invocable: true
metadata:
  openclaw:
    emoji: "🔎"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the client sends HTTPS requests only to the base URL you pass, normally https://api.contextual.ai/v1."
---

# go-contextual-ai

Typed Go client for the Contextual AI API. Package `contextual`, generated from the spec Contextual AI publishes for its SDKs.

For install details, the method naming scheme and the operation list, see [references/setup.md](references/setup.md).

## Security & safety

- Read the API key from an environment variable such as `CONTEXTUAL_API_KEY`. Never hardcode it, commit it, or log it, and never print request headers.
- Requests and their data go only to the base URL passed to `NewClientWithResponses`. Use `https://api.contextual.ai/v1` unless the user names another Contextual AI host.
- Delete, reset, user removal and ingestion calls change the user's account. Call them only when the user asked for that change, and only on agents, datastores and documents the task owns.

## When to use

- Go code needs to query a Contextual AI agent, manage agents or datastores, ingest or list documents, or call generate, rerank, parse or LMUnit.
- The project already imports `github.com/psyb0t/go-contextual-ai`.

## When NOT to use

- The code is not Go. Contextual AI ships official Python and Node SDKs.
- You need streamed query output as parsed events. The client has no server-sent events parser; leave `Stream` unset to get one JSON response.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-contextual-ai`, from inside your module:

```bash
go doc github.com/psyb0t/go-contextual-ai ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-contextual-ai QueryRequestV1                # one method, params type or model
go doc -all github.com/psyb0t/go-contextual-ai                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-contextual-ai.

Method names come from the spec's operation IDs, which repeat the path and HTTP method (`ListDatastoresDatastoresGet`). `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. Multipart uploads (document ingestion, parse) only have the `<OperationId>WithBodyWithResponse` form, which takes a content type and an `io.Reader`. The `JSON200` field (or `JSON422` and so on, per declared status) holds the decoded body; it is nil for any other status.

## Usage

```go
import (
	"context"
	"fmt"
	"net/http"
	"os"

	"github.com/google/uuid"
	"github.com/psyb0t/go-contextual-ai"
)

auth := contextual.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
	req.Header.Set("Authorization", "Bearer "+os.Getenv("CONTEXTUAL_API_KEY"))

	return nil
})

client, err := contextual.NewClientWithResponses("https://api.contextual.ai/v1", auth)
if err != nil {
	return err
}

limit := 20

datastores, err := client.ListDatastoresDatastoresGetWithResponse(
	ctx,
	&contextual.ListDatastoresDatastoresGetParams{Limit: &limit},
)
if err != nil {
	return err // transport failure
}

if datastores.JSON200 == nil {
	return fmt.Errorf("list datastores: status %d: %s", datastores.StatusCode(), datastores.Body)
}

for _, ds := range datastores.JSON200.Datastores {
	fmt.Println(ds.Id, ds.Name)
}
```

Querying an agent:

```go
agentID, err := uuid.Parse(os.Getenv("CONTEXTUAL_AGENT_ID"))
if err != nil {
	return err
}

res, err := client.QueryAgentsAgentIdQueryPostWithResponse(
	ctx,
	agentID,
	&contextual.QueryAgentsAgentIdQueryPostParams{},
	contextual.QueryRequestV1{
		Messages: []contextual.MessageAndRole{
			{Role: contextual.SenderTypeUser, Content: "What is the refund policy?"},
		},
	},
)
if err != nil {
	return err
}

if res.JSON200 != nil && res.JSON200.Message != nil {
	fmt.Println(res.JSON200.Message.Content)
}
```

## Errors

- A non-nil `err` is a transport or decoding failure.
- An HTTP error status is not an `err`. Check `StatusCode()`: `JSON200` is set on success, `JSON422` (`*HTTPValidationError`, with `Detail`) on a validation error, and `Body` always holds the raw response.
