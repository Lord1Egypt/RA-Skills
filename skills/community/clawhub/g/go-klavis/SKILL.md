---
name: go-klavis
description: "Unofficial Go client for the Klavis AI API, generated with oapi-codegen. In package klavis (github.com/psyb0t/go-klavis), the client from klavis.NewClientWithResponses has a typed ...WithResponse method for every endpoint: MCP server discovery, listing and calling tools, MCP server instances and their auth, Strata, users and their integrations, OAuth, white labeling, sandboxes and universes. Auth is a Bearer API key added through a request editor, against the US or EU host. Use when Go code needs to call the Klavis AI API, manage Klavis MCP servers or tool calls, or already imports go-klavis."
license: MIT
homepage: https://github.com/psyb0t/go-klavis
user-invocable: true
metadata:
  openclaw:
    emoji: "🔌"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the code you write talks HTTPS to api.klavis.ai or api.eu.klavis.ai. Tool operations can make Klavis contact the requested MCP server."
---

# go-klavis

Unofficial, typed Go client for the Klavis AI API, in package `klavis` at the module root.

Read [references/setup.md](references/setup.md) before adding the dependency or choosing an operation. It covers authentication, regional hosts, operation names, pagination and response fields.

## Security & safety

- Read the Klavis API key from `KLAVIS_API_KEY`. Set `Authorization: Bearer <key>` in a request editor. Never hardcode, commit or log credentials, downstream authentication headers or returned authentication data.
- Choose `https://api.klavis.ai` or `https://api.eu.klavis.ai` for the account's region. Do not send credentials to another host.
- Tool calls can change external services. Creating or deleting instances, changing authentication, user deletion and sandbox execution also act on remote resources. Call them only when the user requested the action.
- Verify MCP server URLs and tool arguments before sending downstream credentials or running a tool.

## When to use

- Go code needs to discover MCP servers, list or call tools, or manage Klavis instances, Strata or user integrations.
- Go code needs Klavis OAuth, sandbox or universe REST endpoints.
- The project already imports `github.com/psyb0t/go-klavis`.

## When not to use

- The code is not Go. This module ships only a Go package.
- You need a client maintained by Klavis AI. This one is unofficial and not affiliated with Klavis AI.
- You want to change the generated client itself. Read `AGENTS.md` in the repository.

## Finding endpoints and types

The reference covers a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-klavis`, from inside your module:

```bash
go doc github.com/psyb0t/go-klavis ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-klavis CallToolRequest               # one method, params type or model
go doc -all github.com/psyb0t/go-klavis                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-klavis.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. The `SandboxSchemas...GoogleCalendarEvent...` types are deprecated aliases of `GoogleCalendarEvent`; use `GoogleCalendarEvent` in new code.

## Workflow

1. Check the installed module version and generated signature before editing. Operation IDs determine names, including long sandbox and Strata methods.
2. Read the regional host and key from application configuration. Add `WithRequestEditorFn` for Bearer auth and `WithHTTPClient` for the application's timeout policy.
3. Use `NewClientWithResponses` and the operation's `...WithResponse` method. Inspect transport errors, HTTP status and decoded fields before using the result.
4. For tool lists and calls, check `Success` and `Error` even on HTTP 200. A tool result can also carry `IsError`.
5. Compile the integration and test it against a local HTTP server. Finish when the request method, path, authentication and response handling match the generated API. Do not call the live service merely to verify compilation.

Optional fields are often pointers. Check for nil before dereferencing. The error return covers transport and decoding failures; API errors require checking `StatusCode()`, the status-specific fields and `Body`.
