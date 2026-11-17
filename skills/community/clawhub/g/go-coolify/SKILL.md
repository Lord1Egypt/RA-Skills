---
name: go-coolify
description: "Writes Go code with go-coolify (package coolify, github.com/psyb0t/go-coolify), an unofficial generated client for the Coolify API covering applications, deployments, databases, services, projects, servers and teams. Use when Go code calls the Coolify API or already imports github.com/psyb0t/go-coolify."
license: MIT
homepage: https://github.com/psyb0t/go-coolify
user-invocable: true
metadata:
  openclaw:
    emoji: "☁️"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "Module installation uses your Go module proxy. Runtime requests go to the Coolify instance URL supplied by the user."
---

# go-coolify

Unofficial, typed Go client for the Coolify API, in package `coolify` at the module root.

Read [references/setup.md](references/setup.md) before adding the dependency or choosing operations. It covers authentication, base URLs, response handling and selected operations.

## Security & safety

- Read the user-supplied instance API URL from `COOLIFY_BASE_URL`, including `/api/v1`. There is no default host. Use HTTPS for remote instances and send credentials only to the intended instance.
- The spec's `bearerAuth` scheme uses `Authorization: Bearer <token>`. Read the token from `COOLIFY_API_TOKEN` in a request editor. Never hardcode, commit or log it, or print requests containing the authorization header.
- Creating, updating, deleting, deploying, restarting or stopping resources changes the user's infrastructure. Call these operations only when the user asked for the action.

## When to use

- Go code needs to inspect Coolify applications, deployments, databases, services, projects, servers or teams.
- Go code needs to change Coolify resources at the user's request.
- The project already imports `github.com/psyb0t/go-coolify`.

## When not to use

- The code is not Go. This module ships only a Go package.
- You need a client maintained by Coolify. This one is unofficial and not affiliated with Coolify.
- You want to change the generated client itself. Read the repository's `AGENTS.md` instead.

## Finding endpoints and types

The examples cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-coolify`, from inside your module:

```bash
go doc github.com/psyb0t/go-coolify ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-coolify ListApplicationsParams        # one method, params type or model
go doc -all github.com/psyb0t/go-coolify                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-coolify.

Method names come from the spec's operation IDs, which are short action names (`ListProjects`, `GetProjectByUuid`). `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status.

## Usage

Use the complete example in [references/setup.md](references/setup.md#usage). Construct `coolify.NewClientWithResponses` with the user's API URL and `coolify.WithRequestEditorFn`, then call `ListProjectsWithResponse(context.Background())` to list projects.

Check the error return for request, transport and decoding failures. HTTP errors may have a nil error, so also check `StatusCode()`, the expected `JSON...` field and `Body`. Check pointer fields before dereferencing. Close raw response bodies, and use `coolify.WithHTTPClient` with an explicit timeout.

Complete the change by compiling the caller and testing its request and response handling against a local HTTP test server. Do not contact the user's instance to validate an example without authorization.
