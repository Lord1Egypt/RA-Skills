# go-vercel: setup and reference

## Requirements

- Go 1.26.11 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.
- A Vercel access token, created under Account Settings, Tokens.

## Install

```bash
go get github.com/psyb0t/go-vercel
```

The package name is `vercel`. The module path ends in `go-vercel`, so import it with an explicit name:

```go
import vercel "github.com/psyb0t/go-vercel"
```

## Creating the client

`vercel.NewClientWithResponses(server string, opts ...vercel.ClientOption)` returns a `*vercel.ClientWithResponses`. The server is `https://api.vercel.com`.

Options:

- `vercel.WithRequestEditorFn(fn)` runs `fn` on every request. Use it to set `Authorization: Bearer <token>` and, for team resources, the `teamId` query parameter.
- `vercel.WithHTTPClient(doer)` swaps the `*http.Client`, for timeouts or a test transport.

Every method also takes trailing `reqEditors ...vercel.RequestEditorFn` that apply to that call only.

## Teams

Requests act on the token owner's personal account by default. To act on a team, send `teamId`. Most operations have `TeamId *string` (and `Slug *string`) on their params struct, so it can be set per call:

```go
teamID := os.Getenv("VERCEL_TEAM_ID")

res, err := client.GetProjectsWithResponse(ctx, &vercel.GetProjectsParams{
	TeamId: &teamID,
})
```

## Responses

Each `XWithResponse` method returns `*XResponse` with:

| Field or method | Holds |
|---|---|
| `JSON200` (or `JSON201` and so on) | The decoded success body, nil for any other status |
| `StatusCode()` | The HTTP status |
| `Body` | The raw response body |
| `HTTPResponse` | The `*http.Response`, body already read |

Many bodies are `oneOf` unions. They are opaque types with `As<Member>()` methods that decode the raw JSON into one member, for example `res.JSON200.User.AsAuthUser()` or `AsAuthUserLimited()` on `GetAuthUserWithResponse`. Pick the member the response shape matches. `GetProjectsWithResponse` returns `AsGetProjects200JSONResponseBody1()` for the `{projects, pagination}` page.

## Errors

- A non-nil `err` from a method is a transport or decode failure.
- A Vercel error status (400, 403, 404, 429 and so on) is not an `err`. `JSON200` is nil; read `StatusCode()` and `Body`, which holds Vercel's JSON error.
- On 429, back off before retrying.

## Regenerating

The client is generated, never edited by hand. `make generate` downloads the spec, patches it with `scripts/patch-spec.sh`, runs oapi-codegen and splits the output into `client_NNN.gen.go` files. See the repo's README.
