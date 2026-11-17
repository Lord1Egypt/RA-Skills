---
name: go-vercel
description: Unofficial Go client for the Vercel REST API, generated with oapi-codegen from Vercel's OpenAPI spec. Package `vercel` from `github.com/psyb0t/go-vercel` gives `NewClientWithResponses` a typed `...WithResponse` method for every endpoint in the spec (projects, deployments, domains, DNS, env vars, teams and more), with typed params structs, `JSON200` response bodies and `As...` methods for oneOf unions. Auth is a bearer token added by a `RequestEditorFn`, with an optional `teamId` query parameter. Use when Go code needs to call the Vercel API, or the project already imports go-vercel.
license: MIT
homepage: https://github.com/psyb0t/go-vercel
user-invocable: true
metadata:
  openclaw:
    emoji: "▲"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the client sends HTTPS requests only to the base URL you give it, `https://api.vercel.com`."
---

# go-vercel

Typed Go client for the Vercel REST API. Every operation in Vercel's OpenAPI spec is a method on `*vercel.ClientWithResponses`.

For install, auth details, union responses and error handling, see [references/setup.md](references/setup.md).

## Security & safety

- Read the token from an environment variable such as `VERCEL_TOKEN`. Never hardcode it, commit it or log it, and never print request headers.
- Requests go only to the base URL passed to `NewClientWithResponses`. Use `https://api.vercel.com`.
- Many endpoints change or delete live resources (deployments, projects, domains, DNS records, env vars, teams). Call those only when the user asked for that change, and only on resources the task is about.

## When to use

- Go code needs to read or manage Vercel projects, deployments, domains, env vars or teams.
- The project already imports `github.com/psyb0t/go-vercel`.

## When NOT to use

- A shell script or CI step that the `vercel` CLI already covers.
- Code in a language other than Go.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-vercel`, from inside your module:

```bash
go doc github.com/psyb0t/go-vercel ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-vercel GetProjectsParams              # one method, params type or model
go doc -all github.com/psyb0t/go-vercel                           # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-vercel. The package is very large, so prefer the targeted `go doc` lines over `-all`.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status.

## Usage

```go
import (
	"context"
	"net/http"
	"os"

	vercel "github.com/psyb0t/go-vercel"
)

auth := vercel.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
	req.Header.Set("Authorization", "Bearer "+os.Getenv("VERCEL_TOKEN"))

	// Requests act on your personal account unless they name a team.
	if teamID := os.Getenv("VERCEL_TEAM_ID"); teamID != "" {
		query := req.URL.Query()
		query.Set("teamId", teamID)
		req.URL.RawQuery = query.Encode()
	}

	return nil
})

client, err := vercel.NewClientWithResponses("https://api.vercel.com", auth)
if err != nil {
	return err
}

res, err := client.GetAuthUserWithResponse(ctx)
if err != nil {
	return err // transport error
}

if res.JSON200 == nil {
	return fmt.Errorf("vercel: status %d: %s", res.StatusCode(), res.Body)
}

user, err := res.JSON200.User.AsAuthUser()
if err != nil {
	return err
}

fmt.Println(user.Id, user.Username, user.Email)
```

Listing projects with typed params:

```go
search := "site"

res, err := client.GetProjectsWithResponse(ctx, &vercel.GetProjectsParams{
	Search: &search,
})
if err != nil {
	return err
}

if res.JSON200 == nil {
	return fmt.Errorf("vercel: status %d: %s", res.StatusCode(), res.Body)
}

page, err := res.JSON200.AsGetProjects200JSONResponseBody1()
if err != nil {
	return err
}

for _, project := range page.Projects {
	fmt.Println(project.Id, project.Name)
}
```

Method names follow the spec's `operationId`: `getProjects` becomes `GetProjectsWithResponse`. Look the name up with `go doc` as shown above rather than guessing it.
