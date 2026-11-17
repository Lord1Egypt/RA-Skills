# go-intercom: setup and reference

This module is unofficial and not affiliated with Intercom.

## Requirements

- Go 1.26.11 or newer, per the module's `go.mod`.
- An Intercom access token with the scopes needed for the requested operations, exported as `INTERCOM_ACCESS_TOKEN`.

## Install

```bash
go get github.com/psyb0t/go-intercom
```

## Regions

| Region | Base URL |
|---|---|
| United States | `https://api.intercom.io` |
| Europe | `https://api.eu.intercom.io` |
| Australia | `https://api.au.intercom.io` |

Select the workspace's data region.

## Auth

The spec declares HTTP bearer authentication. In a request editor set `req.Header.Set("Authorization", "Bearer "+token)` and `req.Header.Set("Intercom-Version", "2.17")`. The version header is optional in the spec; omitting it uses the app's configured version rather than necessarily the version of these generated models.

## Client

- `intercom.NewClientWithResponses(server, opts...)`. Options: `intercom.WithRequestEditorFn`, `intercom.WithHTTPClient` (your own `*http.Client`, for timeouts), `intercom.WithBaseURL`.
- Each operation has a raw `Client.X` method, a parsed `ClientWithResponses.XWithResponse` method and a `NewXRequest` constructor. Operations with a body also have `XWithBodyWithResponse` taking a raw `io.Reader`.

## Main operations

The client covers all 258 operations in the spec (Intercom API 2.17). Representative generated methods:

| Method | Endpoint |
|---|---|
| `IdentifyAdminWithResponse` | `GET /me` |
| `ListAdminsWithResponse` | `GET /admins` |
| `ListContactsWithResponse`, `CreateContactWithResponse` | `GET`, `POST /contacts` |
| `ShowContactWithResponse`, `UpdateContactWithResponse`, `DeleteContactWithResponse` | `GET`, `PUT`, `DELETE /contacts/{contact_id}` |
| `SearchContactsWithResponse` | `POST /contacts/search` |
| `ListAllCompaniesWithResponse` | `POST /companies/list` |
| `ListConversationsWithResponse`, `CreateConversationWithResponse` | `GET`, `POST /conversations` |
| `RetrieveConversationWithResponse` | `GET /conversations/{conversation_id}` |
| `ReplyConversationWithResponse` | `POST /conversations/{conversation_id}/reply` |
| `ListArticlesWithResponse`, `CreateArticleWithResponse` | `GET`, `POST /articles` |
| `CreateTicketWithResponse` | `POST /tickets` |
| `ListTagsWithResponse` | `GET /tags` |
| `ListTeamsWithResponse` | `GET /teams` |

Operation IDs determine names. Reporting export operations without IDs receive names derived from their HTTP method and path. Read each endpoint's params and body types with `go doc github.com/psyb0t/go-intercom <Method>`, or list every method with `go doc github.com/psyb0t/go-intercom ClientWithResponsesInterface`.

## Responses

| Field or method | Holds |
|---|---|
| `JSON200` and other `JSON` status fields | The decoded response for that status, nil otherwise |
| `Body`, `StatusCode()`, `Status()`, `HTTPResponse` | The raw response |

Number fields are `float64`; many fields are pointers. HTTP failures such as 401, 403 and 429 do not become Go errors merely because of the status code.

## Pagination

Pagination depends on the endpoint. `ListConversationsParams` exposes `PerPage` and `StartingAfter`; pass the response's `Pages.Next.StartingAfter` cursor into the next request until `Pages.Next` is nil. Other schemas use page numbers or a `pages.next` URI instead.

The contacts list description mentions pagination, but its spec parameter list omits `per_page` and `starting_after`. `ListContactsParams` therefore does not expose them. Add those query values through a request editor when listing further contact pages. The client does not follow pagination links itself. Never attach the bearer token to an untrusted pagination host.

## Rate limits

Inspect the HTTP status and response headers. Back off on 429 rather than retrying in a tight loop. The generated client has no retry policy.
