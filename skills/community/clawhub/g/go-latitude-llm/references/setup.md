# go-latitude-llm: setup and reference

This module is unofficial and not affiliated with Latitude.

## Requirements

- Go 1.26.10 or newer, per `go.mod`.
- An organization API key, available to the calling application as `LATITUDE_API_KEY`, or a user OAuth token for operations that require a user.

## Install

```bash
go get github.com/psyb0t/go-latitude-llm
```

## Environments and auth

The public API base URL is `https://api.latitude.so`. Generated paths already include `/v1`. A trusted self-hosted installation can supply its own base URL.

The spec defines `ApiKeyAuth` as HTTP Bearer auth. A request editor sets `req.Header.Set("Authorization", "Bearer "+key)`. There is no automatic auth setup. Use the same header form for a user OAuth token when the operation requires one. `CreateSavedSearch`, `InviteMember`, `UpdateMember` and `RemoveMember` require OAuth according to their descriptions. `UpdateMember` also requires an admin or owner.

The complete usage example is in the root [README](../../../../README.md#usage) and `example_test.go`. Both create a client with the Bearer request editor and call `ListProjectsWithResponse(context.Background())`.

## Client

- `latitude.NewClientWithResponses(server, opts...)` creates the parsed-response client. Options include `WithRequestEditorFn`, `WithHTTPClient` and `WithBaseURL`.
- Each operation has a raw `Client.X` method, a parsed `ClientWithResponses.XWithResponse` method and a request constructor `NewXRequest`.
- JSON body operations also expose `XWithBodyWithResponse` with a content type and raw `io.Reader`.
- The library adds no retries, pagination loop or default timeout. Use a custom `http.Client` and bound calls with a context.

## Operations

All names below have a `WithResponse` suffix on the parsed-response client.

| Area | Methods |
| --- | --- |
| Projects | `ListProjects`, `CreateProject`, `GetProject`, `UpdateProject`, `DeleteProject` |
| Scores and annotations | `CreateScore`, `CreateAnnotation`, `ListTraceAnnotations`, `GetTraceAnnotation` |
| Traces and spans | `ListTraces`, `GetTrace`, `ListTraceSpans`, `GetTraceSpan`, `ExportTraces` |
| Saved searches | `ListSavedSearches`, `CreateSavedSearch`, `GetSavedSearch`, `UpdateSavedSearch`, `DeleteSavedSearch`, `AssignSavedSearch`, `ListSavedSearchTraces` |
| Issues | `ListIssues`, `GetIssue`, `GetIssueTrend`, `ListIssueTraces`, `ResolveIssues`, `UnresolveIssues`, `IgnoreIssues`, `UnignoreIssues`, `MonitorIssue`, `UnmonitorIssue`, `ExportIssues` |
| API keys | `ListApiKeys`, `CreateApiKey`, `GetApiKey`, `UpdateApiKey`, `RevokeApiKey` |
| OAuth keys | `ListOAuthKeys`, `GetOAuthKey`, `RevokeOAuthKey` |
| Account and members | `GetAccount`, `ListMembers`, `InviteMember`, `GetMember`, `UpdateMember`, `RemoveMember` |
| Public metadata | `HealthGet`, `WellKnownOauthProtectedResource` |

Request bodies include `CreateProjectBody`, `UpdateProjectBody`, `ListTracesBody`, `CreateScoreBody`, `CreateAnnotationBody` and `CreateSavedSearchBody`. Score and filter unions use generated accessors. Check the method signature with `go doc github.com/psyb0t/go-latitude-llm ClientWithResponsesInterface` for the exact params and body type.

## Responses

| Field or method | Holds |
| --- | --- |
| `JSON200`, `JSON201` | Decoded success body for the matching status |
| `JSON400`, `JSON401`, `JSON404` | Typed errors where declared by the operation |
| `Body`, `StatusCode()`, `Status()`, `HTTPResponse` | Response bytes, status and headers |

Only transport or decoding failures return Go errors. Check HTTP status even when `err == nil`. Nullable properties become pointers. API-key `GetAccount` responses have nil `User` and `Role`. Number fields are `float64`.

## Pagination

The spec says project listing returns every project in one page, with nil `NextCursor` and false `HasMore`; `ListProjects` takes no cursor params. Other paginated collections expose `Items`, `HasMore` and `NextCursor`. Pass the opaque cursor back using the operation's generated params or request body, and stop when `HasMore` is false. The client does not fetch subsequent pages automatically.

## Pitfalls

- Renaming a project or saved search can change its slug. Use the returned slug for later path calls and keep stable IDs for stored references.
- Trace list rows omit message content. `GetTrace` returns the full conversation view.
- Export endpoints request emailed export links. Confirm recipients and export scope before calling them.
- Creating or fetching API keys can return the full token. Treat the response as sensitive.
- The spec does not declare a rate-limit quota. Inspect error statuses and apply bounded backoff where appropriate; do not assume retries are safe for every write.
