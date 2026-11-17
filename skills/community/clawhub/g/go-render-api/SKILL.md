---
name: go-render-api
description: Unofficial Go client for the Render public REST API, generated with oapi-codegen. Package render (github.com/psyb0t/go-render-api) has render.NewClientWithResponses, which returns a client with one typed method per endpoint (services, deploys, env vars, Postgres, Key Value, custom domains, jobs and more). Auth is a bearer API key set through render.WithRequestEditorFn, list endpoints page with cursors, and responses decode into JSON200 and per-status error fields. Use when Go code needs to call the Render API or already imports go-render-api.
license: MIT
homepage: https://github.com/psyb0t/go-render-api
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
  network: "HTTPS to the Render API at api.render.com, and `go get` to your Go module proxy."
---

# go-render-api

Typed Go client for the Render API. Every endpoint in Render's OpenAPI document is a method on `ClientWithResponses`.

For install, client options, more operations, paging and response handling, see [references/setup.md](references/setup.md).

## Security & safety

- Read the API key from an environment variable such as `RENDER_API_KEY`. Never hardcode it, commit it or log it, and never print request headers.
- Requests go only to the base URL you pass, `https://api.render.com/v1`.
- Deploy, suspend, scale, update and delete endpoints change live infrastructure. Call them only on services the user named and only when the user asked for that action.

## When to use

- Go code needs to list or inspect Render services, trigger or list deploys, or manage other Render resources.
- The project already imports `github.com/psyb0t/go-render-api`.

## When NOT to use

- A one-off change in the Render Dashboard or with the Render CLI is enough.
- The code is not Go.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-render-api`, from inside your module:

```bash
go doc github.com/psyb0t/go-render-api ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-render-api ListServicesParams            # one method, params type or model
go doc -all github.com/psyb0t/go-render-api                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-render-api.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. The package name is `render` while the module path ends in `go-render-api`, so import it as `render "github.com/psyb0t/go-render-api"`.

## Usage

```go
import (
	"context"
	"fmt"
	"net/http"
	"os"

	render "github.com/psyb0t/go-render-api"
)

auth := render.WithRequestEditorFn(
	func(_ context.Context, req *http.Request) error {
		req.Header.Set(
			"Authorization",
			"Bearer "+os.Getenv("RENDER_API_KEY"),
		)

		return nil
	},
)

client, err := render.NewClientWithResponses(
	"https://api.render.com/v1",
	auth,
)
if err != nil {
	return err
}

limit := render.LimitParam(20)

res, err := client.ListServicesWithResponse(
	ctx,
	&render.ListServicesParams{Limit: &limit},
)
if err != nil {
	return err // transport failure
}

if res.JSON200 == nil {
	return fmt.Errorf("render: status %d", res.StatusCode())
}

for _, item := range *res.JSON200 {
	fmt.Println(item.Service.Id, item.Service.Name, item.Cursor)
}
```

Listing deploys of one service:

```go
deploys, err := client.ListDeploysWithResponse(ctx, serviceID, nil)
if err != nil {
	return err
}

if deploys.JSON200 != nil {
	for _, item := range *deploys.JSON200 {
		if item.Deploy != nil && item.Deploy.Status != nil {
			fmt.Println(item.Deploy.Id, *item.Deploy.Status)
		}
	}
}
```

A method returns an error only when the request could not be sent or the body could not be decoded. An API error is a normal response: check `StatusCode()` and read the matching field, such as `JSON401`, a `*render.Error` with optional `Message`, `Code` and `Id`.
