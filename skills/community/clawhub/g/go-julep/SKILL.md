---
name: go-julep
description: Unofficial Go client for the Julep API, generated with oapi-codegen. `julep.NewClientWithResponses(baseURL, opts...)` from `github.com/psyb0t/go-julep` gives a typed method for every endpoint in Julep's OpenAPI spec (agents, agent docs and search, tools, tasks, executions and transitions, sessions and chat, users, files, secrets, projects, embeddings, jobs, health), with request structs and decoded `JSON200`/`JSON201`/`JSON422` response fields. Auth is an API key in the `Authorization` header, added through a request editor. Use when Go code needs to call the Julep API, or already imports go-julep.
license: MIT
homepage: https://github.com/psyb0t/go-julep
user-invocable: true
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the client sends HTTPS requests only to the base URL you pass, normally https://api.julep.ai/api."
---

# go-julep

Typed Go client for the Julep API. Package `julep`, generated from the spec Julep publishes for its SDKs.

For install details, the method naming scheme and the operation list, see [references/setup.md](references/setup.md).

## Security & safety

- Read the API key from an environment variable such as `JULEP_API_KEY`. Never hardcode it, commit it, or log it, and never print request headers.
- Requests and their data go only to the base URL passed to `NewClientWithResponses`: `https://api.julep.ai/api`, or `https://dev.julep.ai/api` when the user asks for dev.
- Delete, update, secret and execution calls change the user's account or start billed work. Call them only when the user asked for that change, and only on agents, users, sessions, tasks and secrets the task owns.

## When to use

- Go code needs to manage Julep agents, users, sessions, tasks or docs, chat in a session, or start and inspect task executions.
- The project already imports `github.com/psyb0t/go-julep`.

## When NOT to use

- The code is not Go. Julep ships official Python and Node SDKs.
- You need the execution status or transition streams as parsed events. The client has no server-sent events parser; poll `GetExecutionDetailsExecutionsExecutionIdGet` instead.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-julep`, from inside your module:

```bash
go doc github.com/psyb0t/go-julep ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-julep ListAgentsAgentsGetParams      # one method, params type or model
go doc -all github.com/psyb0t/go-julep                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-julep.

Method names come from the spec's operation IDs, which repeat the path and HTTP method (`ListAgentsAgentsGet`). `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status.

## Usage

```go
import (
	"context"
	"fmt"
	"net/http"
	"os"

	"github.com/psyb0t/go-julep"
)

auth := julep.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
	req.Header.Set("Authorization", "Bearer "+os.Getenv("JULEP_API_KEY"))

	return nil
})

client, err := julep.NewClientWithResponses("https://api.julep.ai/api", auth)
if err != nil {
	return err
}

limit := 10

agents, err := client.ListAgentsAgentsGetWithResponse(
	ctx,
	&julep.ListAgentsAgentsGetParams{Limit: &limit},
)
if err != nil {
	return err // transport failure
}

if agents.JSON200 == nil {
	return fmt.Errorf("list agents: status %d: %s", agents.StatusCode(), agents.Body)
}

for _, agent := range agents.JSON200.Items {
	fmt.Println(*agent.Id, agent.Name)
}
```

Creating a user (the API answers 201, so read `JSON201`):

```go
name := "alice"

res, err := client.CreateUserUsersPostWithResponse(ctx, julep.CreateUserRequest{Name: &name})
if err != nil {
	return err
}

if res.JSON201 == nil {
	return fmt.Errorf("create user: status %d: %s", res.StatusCode(), res.Body)
}

fmt.Println(*res.JSON201.Id)
```

## Errors

- A non-nil `err` is a transport or decoding failure.
- An HTTP error status is not an `err`. Check `StatusCode()`: the matching `JSON200` or `JSON201` field is set on success, `JSON422` (`*HTTPValidationError`, with `Detail`) on a validation error, and `Body` always holds the raw response.
