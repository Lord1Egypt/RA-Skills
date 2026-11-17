---
name: go-mem0
description: Unofficial Go client for the Mem0 Platform API, generated with oapi-codegen. Package `mem0` (`github.com/psyb0t/go-mem0`) provides `mem0.NewClientWithResponses` with a typed `...WithResponse` method for every endpoint, covering adding, searching, listing, updating and deleting memories (V1, V2 and V3), entities, events, exports, organizations, projects, webhooks, profiles and Dream operations. Auth is an API key in the `Authorization` header with a `Token` prefix, added through a request editor. Use when Go code needs Mem0 hosted memory or already imports go-mem0.
license: MIT
homepage: https://github.com/psyb0t/go-mem0
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to Go source in the current project. The library reads and writes no files."
  shell: "The Go toolchain to add and compile the dependency."
  network: "Module installation fetches dependencies through the configured Go module proxy. Runtime requests send memory content, queries and metadata to https://api.mem0.ai."
---

# go-mem0

Unofficial, typed Go client for the Mem0 Platform API, in package `mem0` at the module root.

For install, operations, pagination and response fields, see [references/setup.md](references/setup.md).

## Security & safety

- Set `Authorization: Token <key>` with a request editor. Read the key from `MEM0_API_KEY`; never hardcode, commit or log it, or print a request containing the header.
- Use `https://api.mem0.ai`. Memory content, queries and metadata leave the machine in API requests. Scope filters to the intended user, agent, app or run, and send only the data the task requires.
- Creating, updating and deleting memories, entities, organizations, projects, members, webhooks and profile jobs change hosted resources. Perform these operations only on task-owned resources when the user requested that action. Profile jobs can consume credits.

## When to use

- Go code needs to add, retrieve, search or manage Mem0 hosted memories.
- Go code needs Mem0 entities, events, exports, projects, webhooks, profiles or Dream operations.
- The project already imports `github.com/psyb0t/go-mem0`.

## When NOT to use

- The code is not Go. This module ships a Go package.
- You need Mem0's self-hosted memory library. This client targets the Platform API.
- You need an official Mem0 SDK. This module is unofficial and not affiliated with Mem0.
- You want to change the generated client itself. See `AGENTS.md` in the repository.

## Finding endpoints and types

The reference covers a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-mem0`, from inside your module:

```bash
go doc github.com/psyb0t/go-mem0 ClientWithResponsesInterface     # every endpoint method
go doc github.com/psyb0t/go-mem0 MemoriesSearchV3JSONRequestBody  # one method, params type or model
go doc -all github.com/psyb0t/go-mem0                             # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-mem0.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON202` and so on, per declared status) holds the decoded body; it is nil for any other status.

## Usage

Construct `mem0.NewClientWithResponses` with base URL `https://api.mem0.ai` and `mem0.WithRequestEditorFn` setting the `Authorization` header to `Token ` followed by the key from `MEM0_API_KEY`. The complete compiling example is in the root README and `example_test.go`.

Use `PingReadWithResponse` to check authentication. The error return covers transport and response-decoding failures. HTTP errors can return a nil Go error. Check `StatusCode()` and the expected success field before using data; for ping, `JSON200` is success and `JSON401` carries an authentication error.

For memory search, prefer `MemoriesSearchV3WithResponse` with `MemoriesSearchV3JSONRequestBody`. Its required `Query` is a string and `Filters` is `map[string]interface{}` containing at least one entity ID. A successful response has `JSON200.Results`. The V2 search endpoint is deprecated in the source spec and returns an array instead.

The client does not validate filters, implement retries or enforce authorization. Keep entity and organization scope explicit. Optional response fields are pointers; check for nil before dereferencing.
