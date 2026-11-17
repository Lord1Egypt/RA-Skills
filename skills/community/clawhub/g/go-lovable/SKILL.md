---
name: go-lovable
description: Unofficial Go client for the Lovable API, generated with oapi-codegen. Package lovable (github.com/psyb0t/go-lovable) provides lovable.NewClientWithResponses with a typed ...WithResponse method for every endpoint, authenticated with a Lovable-API-Key header or Bearer token. Use when Go code needs to manage Lovable projects, publishing, deployment status, preview embed URLs, analytics, security scans, personal data findings, workspaces, groups or members, or already imports github.com/psyb0t/go-lovable.
license: MIT
homepage: https://github.com/psyb0t/go-lovable
user-invocable: true
metadata:
  openclaw:
    emoji: "🛠️"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain to add and compile the dependency."
  network: "Module installation uses the configured Go module proxy. Runtime requests go to https://api.lovable.dev."
---

# go-lovable

Unofficial, typed Go client for the Lovable API, in package `lovable` at the module root. I am not affiliated with Lovable.

Read [references/setup.md](references/setup.md) for install, auth, the operation list and response handling. The repository's `example_test.go` holds the compiled README example.

## Security & safety

- Load `LOVABLE_API_KEY` from the environment. Set `Lovable-API-Key` with `lovable.WithRequestEditorFn`; the spec also accepts `Authorization: Bearer <key>`. Never log credentials or request authorization headers.
- Use `https://api.lovable.dev` as the base URL. Generated paths already contain `/v1`.
- API keys belong to one workspace and have project or workspace read/write scopes. Write scopes include their corresponding read scope. A different workspace's resource returns 404, and insufficient scope returns 403.
- Updating or deleting projects, changing publishing settings, publishing, unpublishing and creating embed URLs affect account resources or access. Perform those operations only when the user requested them.
- Embed URLs contain an access token. Treat them as credentials and share them only with the intended recipient.

## When to use

- Go code needs Lovable project, workspace, membership, analytics or security data.
- Go code needs project updates or publishing actions at the user's request.
- The project already imports `github.com/psyb0t/go-lovable`.

## When not to use

- The code is not Go, or the user needs an official provider-maintained SDK.
- The task is to change this generated client. Read `AGENTS.md` for that workflow.
- The task needs app generation or chat operations absent from the downloaded public spec. Do not invent endpoints.

## Finding endpoints and types

The reference covers a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-lovable`, from inside your module:

```bash
go doc github.com/psyb0t/go-lovable ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-lovable ListProjectsParams            # one method, params type or model
go doc -all github.com/psyb0t/go-lovable                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-lovable.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON202` and so on, per declared status) holds the decoded body; it is nil for any other status.

## Usage

Construct `lovable.NewClientWithResponses("https://api.lovable.dev", auth)`, where `auth` is a `lovable.WithRequestEditorFn` setting the `Lovable-API-Key` header. Supply a custom `*http.Client` with `lovable.WithHTTPClient` when a timeout is needed.

`ListWorkspacesWithResponse(ctx, &lovable.ListWorkspacesParams{})` lists accessible workspaces. `ListProjectsWithResponse` requires `ListProjectsParams.WorkspaceId`, a slice of workspace IDs. `GetProjectWithResponse(ctx, projectID, nil)` reads one project. `UpdateProjectWithResponse` takes a project ID, optional params and `UpdateProjectJSONRequestBody`.

The Go error covers transport and decoding failures. For HTTP failures, check `StatusCode()` and the appropriate typed field, such as `JSON401` or `JSON403`. Success fields such as `JSON200` are nil on error responses.

Required nullable fields use `nullable.Nullable[T]`. Check `IsNull()` before `Get()`, which returns a value and an error. Optional request fields are pointers. Enum types accept future string values; do not reject unknown values solely because `Valid()` is false.

Lists return `Data` and `Pagination`. Follow `Pagination.NextCursor` while `Pagination.HasMore` is true, retaining the same filters. The client does not traverse pages or retry automatically. Honor `Retry-After` on 429 responses.

Publishing returns 202 and a deployment ID. Poll `GetDeploymentWithResponse` for `completed`, `error` or another status. Use a bounded deadline and backoff; do not assume an unknown status means success. A timeout does not prove a write was rolled back.
