# go-coolify: setup and reference

This module is unofficial and not affiliated with Coolify.

## Contents

- [Requirements](#requirements)
- [Install](#install)
- [Base URL](#base-url)
- [Auth](#auth)
- [Usage](#usage)
- [Client](#client)
- [Operations](#operations)
- [Responses](#responses)
- [Pagination and retries](#pagination-and-retries)

## Requirements

- Go 1.26.11 or newer, per the module's `go.mod`.
- A Coolify instance API URL, including `/api/v1`, exported as `COOLIFY_BASE_URL`.
- A token for that instance, exported as `COOLIFY_API_TOKEN`.

## Install

```bash
go get github.com/psyb0t/go-coolify
```

## Base URL

The user must supply the base URL; the generated client has no default. For a self-hosted instance it might be `https://coolify.example.com/api/v1`. The spec's only server entry is Coolify Cloud, `https://app.coolify.io/api/v1`; use it only when the user's account is on Coolify Cloud. The generated operation paths are relative to that API prefix. Never send the user's token to a different instance.

## Auth

The OpenAPI `bearerAuth` scheme is HTTP Bearer authentication. Create a token under `Keys & Tokens` / `API tokens` in your instance. Use `coolify.WithRequestEditorFn` to set `req.Header.Set("Authorization", "Bearer "+os.Getenv("COOLIFY_API_TOKEN"))`. The generated client does not add authentication or read environment variables itself.

## Usage

Set `COOLIFY_BASE_URL` and `COOLIFY_API_TOKEN` before running this example. The same example lives in the repository's README and `example_test.go`.

```go
package main

import (
	"context"
	"net/http"
	"os"

	"github.com/psyb0t/go-coolify"
)

func main() {
	auth := coolify.WithRequestEditorFn(
		func(_ context.Context, req *http.Request) error {
			req.Header.Set(
				"Authorization",
				"Bearer "+os.Getenv("COOLIFY_API_TOKEN"),
			)

			return nil
		},
	)

	client, err := coolify.NewClientWithResponses(
		os.Getenv("COOLIFY_BASE_URL"),
		auth,
	)
	if err != nil {
		panic(err)
	}

	res, err := client.ListProjectsWithResponse(context.Background())
	if err != nil {
		panic(err)
	}

	_ = res.JSON200
}
```

## Client

- `coolify.NewClientWithResponses(server, opts...)`. Options include `coolify.WithRequestEditorFn`, `coolify.WithHTTPClient` (your own `*http.Client`, for timeouts), and `coolify.WithBaseURL`.
- Each operation has a raw `Client.X` method, a parsed `ClientWithResponses.XWithResponse` method, and a `NewXRequest` constructor. Body operations also expose `XWithBodyWithResponse` for a raw `io.Reader`.
- Close the body returned by a raw client method. Parsed methods read and close it themselves.

## Operations

The generated client covers all operations in the published document. Selected operations are:

| Method | Endpoint relative to the base URL |
| --- | --- |
| `ListProjectsWithResponse` | `GET /projects` |
| `CreateProjectWithResponse` | `POST /projects` |
| `GetProjectByUuidWithResponse` | `GET /projects/{uuid}` |
| `ListApplicationsWithResponse` | `GET /applications`, takes `*ListApplicationsParams` with an optional `Tag` filter |
| `ListDeploymentsWithResponse` | `GET /deployments`, currently running deployments only |
| `ListDatabasesWithResponse` | `GET /databases` |
| `ListServersWithResponse` | `GET /servers` |
| `ListTeamsWithResponse` | `GET /teams` |

`ListDatabasesWithResponse` decodes `JSON200` as `*string`, matching the published response schema. Do not assume every list endpoint returns a slice of resources.

Other operation groups cover applications and deployments, databases and backups, services, servers, teams, environments, private keys and integrations. Method names follow the spec's operation IDs; use `client.gen.go` or Go documentation to check exact names and request types.

## Responses

| Field or method | Holds |
| --- | --- |
| `JSON200` and other `JSON...` fields | Decoded bodies for the declared status and content type, nil otherwise |
| `Body`, `StatusCode()`, `Status()`, `HTTPResponse` | Raw response bytes and HTTP metadata |

Unformatted number fields are `float64`; explicit `format: float` fields remain `float32`. Many optional fields are pointers. The error return covers request, transport and decoding failures; a 401, 403 or other HTTP error may have a nil error. Check the status and expected decoded field before using a result.

The source spec references a missing 403 component. Generation supplies only its `Forbidden.` description, so inspect `Body` for 403 responses rather than expecting a decoded schema.

## Pagination and retries

Log-line query parameters use the named `LogTailLines` union, which retains the spec's integer or `all` alternatives. Use its generated helpers to set the selected alternative.

Use the parameters and response schema of the selected endpoint. The generated client does not automatically paginate or retry. Handle 429 and transient failures according to your instance's policy, and avoid retrying operations that change infrastructure without checking whether the action already succeeded.
