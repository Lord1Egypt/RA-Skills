# go-supabase-management: setup and reference

## Requirements

- Go 1.26.11 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.
- A Supabase personal access token (dashboard, Account, Access Tokens) or an OAuth access token from a Supabase OAuth app, in `SUPABASE_ACCESS_TOKEN`.

## Install

```bash
go get github.com/psyb0t/go-supabase-management
```

The package name is `supabase`. The module path ends in `go-supabase-management`, so import it with an explicit name:

```go
import supabase "github.com/psyb0t/go-supabase-management"
```

## Client and auth

- Base URL: `https://api.supabase.com`.
- `supabase.NewClientWithResponses(baseURL, opts...)` returns the typed client. `supabase.NewClient` returns the lower level one whose methods return `*http.Response`.
- Options: `supabase.WithRequestEditorFn(fn)` runs `fn` on every request; `supabase.WithHTTPClient(doer)` swaps the `http.Client`; `supabase.WithBaseURL(url)` overrides the URL.
- Both token kinds go in `Authorization: Bearer <token>`. An OAuth token reaches only the endpoints its approved scopes allow (`projects:read`, `database:write` and so on); a personal access token reaches everything its user can.

## Method names

Names come from the spec's operation IDs and all start with `V1`. Each has a `...WithResponse` variant on `ClientWithResponses`, and operations with a body also have `...WithBody` / `...WithBodyWithResponse` variants that take a content type and an `io.Reader`. Project endpoints take the 20 character project `ref` after the context.

| Area | Examples |
|---|---|
| Organizations | `V1ListAllOrganizations`, `V1GetAnOrganization`, `V1ListOrganizationMembers` |
| Projects | `V1ListAllProjects`, `V1GetProject`, `V1CreateAProject`, `V1PauseAProject`, `V1DeleteAProject` |
| Branches | `V1ListAllBranches`, `V1CreateABranch`, `V1MergeABranch`, `V1ResetABranch`, `V1DeleteABranch` |
| API keys and secrets | `V1GetProjectApiKeys`, `V1ListAllSecrets`, `V1BulkCreateSecrets` |
| Database | `V1GetPoolerConfig`, `V1GetPostgresConfig`, `V1ListMigrationHistory`, `V1RunAQuery`, `V1ReadOnlyQuery` |
| Auth config | `V1GetAuthServiceConfig`, `V1UpdateAuthServiceConfig` |
| Edge functions | `V1ListAllFunctions`, `V1GetAFunction`, `V1DeployAFunction` |
| Health and logs | `V1GetServicesHealth`, `V1GetProjectLogs` |

Look up the rest with `go doc`, as the skill's "Finding endpoints and types" section shows; every operation in the spec has a method.

Write endpoints (create, update, delete, pause, restore, reset, merge, `V1RunAQuery`) act on live projects. Use them only when the user asked for that change on that project.

## Generation notes

- `V1GetServicesHealthParams.Services` is a slice of service names. The spec also allows a comma-separated string; the generator keeps only the array form, sent as repeated `services=` query parameters.
- The pooler config response has both `connection_string` and the deprecated `connectionString`. They decode into `ConnectionString` and `DeprecatedConnectionString`.

## Errors

- A Go `error` from a method means the request did not complete or the response could not be read.
- An HTTP error status is not a Go error. Check `res.StatusCode()` and the matching field (`JSON200`, `JSON201` and others where the spec declares them). `res.Body` holds the raw response.
