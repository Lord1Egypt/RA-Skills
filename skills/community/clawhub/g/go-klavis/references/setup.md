# go-klavis: setup and reference

This module is unofficial and not affiliated with Klavis AI.

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- A Klavis AI API key exported as `KLAVIS_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-klavis
```

## Regions

| Region | Base URL |
|---|---|
| US | `https://api.klavis.ai` |
| EU | `https://api.eu.klavis.ai` |

Choose the region for the account. The spec does not describe a test environment.

## Auth

The `HTTPBearer` scheme takes the Klavis API key in `Authorization: Bearer <key>`. Add it explicitly with a request editor:

```go
auth := klavis.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
	req.Header.Set("Authorization", "Bearer "+os.Getenv("KLAVIS_API_KEY"))

	return nil
})
```

This fragment uses `context`, `net/http`, `os` and `github.com/psyb0t/go-klavis`. Some OAuth authorization and refresh endpoints do not declare security. A global request editor still runs for every request made by that client.

## Client

- `klavis.NewClientWithResponses(server, opts...)`. Options: `klavis.WithRequestEditorFn`, `klavis.WithHTTPClient` (your own `*http.Client`, for timeouts), `klavis.WithBaseURL`.
- Each operation has `Client.X` (raw `*http.Response`), `ClientWithResponses.XWithResponse` (parsed) and `NewXRequest` (request only). JSON body operations also accept the typed request body; raw-body variants have `WithBody` in their names.
- The package covers all 203 paths and 212 operations. The table below lists common operations; run `go doc github.com/psyb0t/go-klavis ClientWithResponsesInterface` for the full set and exact signatures.

## Operations

| Method | Endpoint |
|---|---|
| `GetAllMcpServersWithResponse` | `GET /mcp-server/servers` |
| `GetServerToolsWithResponse` | `GET /mcp-server/tools/{serverName}` |
| `ListServerToolsWithResponse` | `POST /mcp-server/list-tools` |
| `CallServerToolWithResponse` | `POST /mcp-server/call-tool` |
| `CreateServerInstanceWithResponse` | `POST /mcp-server/instance/create` |
| `CreateSelfHostedServerInstanceWithResponse` | `POST /mcp-server/self-hosted/instance/create` |
| `GetServerInstanceWithResponse`, `UpdateServerInstanceWithResponse`, `DeleteServerInstanceWithResponse` | `GET`, `PATCH`, `DELETE /mcp-server/instance/{instanceId}` |
| `SetInstanceAuthWithResponse` | `POST /mcp-server/instance/set-auth` |
| `GetInstanceAuthDataWithResponse`, `DeleteInstanceAuthWithResponse` | `GET`, `DELETE /mcp-server/instance/{instanceId}/auth` |
| `GetAllUsersWithResponse` | `GET /user/` |
| `GetUserIntegrationsWithResponse` | `GET /user/{userId}/integrations` |
| `GetUserByUserIdWithResponse`, `DeleteUserByUserIdWithResponse` | `GET`, `DELETE /user/{userId}` |
| `GetStrataAuthWithResponse`, `DeleteStrataAuthWithResponse` | `GET`, `DELETE /mcp-server/strata/{strataId}/auth/{serverName}` |

Request bodies include `CreateServerRequest`, `ListToolsRequest` and `CallToolRequest`. `CreateServerRequest` requires `ServerName` and `UserId`; `IsReadOnly` defaults to false when omitted. Tool requests require `ServerUrl`; calls also require `ToolName` and accept `ToolArgs`.

Several instance path parameters use `github.com/oapi-codegen/runtime/types.UUID`, rather than plain strings. Other paths, including `ListRawActionsWithResponse`, accept strings. Follow each generated signature.

## Responses

| Field or method | Holds |
|---|---|
| `JSON200` | The decoded body on HTTP 200, nil otherwise |
| `JSON422` | Validation error details where the spec declares them |
| `Body`, `StatusCode()`, `Status()`, `HTTPResponse` | The raw response |

Number fields are `float64`. Optional fields are often pointers. `GetMcpServersResponse.Servers` contains `McpServer` records. `ListToolsResponse` and `CallToolResponse` have a required `Success` boolean and optional `Error`; inspect them even on HTTP 200. `CallToolResponse.Result.IsError` can report a tool error inside a successful API call.

## Pagination

`GetAllUsersWithResponse` accepts `GetAllUsersParams.PageSize` and `PageNumber` pointers. Page numbers start at one. Page size defaults to 50 and accepts one through 1000. The decoded result has `Users`, `Page`, `PageSize`, `TotalCount` and `TotalPages`. Request subsequent pages until `Page` reaches `TotalPages`.

## Rate limits

The spec does not declare numeric rate limits. Check status codes and raw response headers, and apply the application's retry policy. Do not automatically retry tool calls or other actions that can change remote state.
