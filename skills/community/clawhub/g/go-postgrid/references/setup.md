# go-postgrid: setup and reference

This module is unofficial and not affiliated with PostGrid.

## Requirements

- Go 1.26.10 or newer, per `go.mod`.
- A PostGrid API key for the API being called, exported as `POSTGRID_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-postgrid
```

## Base URL and auth

Use `https://api.postgrid.com`. Both `PrintMailApiKeyAuth` and `AddressVerificationApiKeyAuth` put the key in `X-API-Key`; they represent different APIs. Supply it with a request editor using `req.Header.Set("X-API-Key", key)`.

Test and live print and mail data depend on the key. Use test credentials for development. Live mail creation can send physical mail and incur charges. The spec describes bulk verification and targeted list builds as billable operations too.

## Client

- `postgrid.NewClientWithResponses(server, opts...)` creates the parsed-response client. Options include `postgrid.WithRequestEditorFn`, `postgrid.WithHTTPClient` and `postgrid.WithBaseURL`.
- Each operation has a raw `Client` method, a parsed `ClientWithResponses` method ending in `WithResponse`, and a request constructor.
- Operations with supported typed JSON bodies have typed body methods. Raw body variants accept a content type and an `io.Reader`; use these for multipart uploads when needed.
- The generator derives names from operation IDs. Combined JSON and multipart operation IDs can produce long method names. Use the generated signatures rather than guessing.

## Operations

The entire document is generated, including standard and international address verification and these print and mail resources:

- Contacts and HTML templates.
- Letters, postcards, cheques, self mailers, snap packs and boxes.
- Bank accounts and return envelopes.
- Campaigns, mailing lists, list imports and targeted list builds.
- Reports and report exports.
- Sub-organizations, template editor sessions and virtual mailboxes.
- Events, trackers and webhooks.

`ContactsListWithResponse(ctx, &postgrid.ContactsListParams{})` calls `GET /print-mail/v1/contacts`. The README example and `example_test.go` show this call with authentication.

## Responses

| Field or method | Holds |
|---|---|
| `JSON200` and other status-specific fields | The decoded body for that status, nil otherwise |
| `Body`, `StatusCode()`, `Status()`, `HTTPResponse` | The raw response and status |

Unformatted number fields map to `float64`; fields explicitly marked `format: float` retain the generated `float32` type. Check optional pointers before dereferencing. A nil Go error alone does not mean the HTTP request succeeded.

## Pagination

Print and mail list endpoints accept `skip` and `limit`. Responses include `data`, `totalCount`, `skip` and `limit`. Increase `skip` by the number of returned records and stop when no records remain or the total has been reached. Check each operation's params because not all endpoints use the same pagination shape.

## Rate limits and retries

The spec documents HTTP 429 responses. Back off when rate limited. The generated client does not add retries or pagination loops. After a transport failure on mail creation, check whether the resource was created before retrying.

## Spec source

The source is [PostGrid's published OpenAPI document](https://guides.postgrid.com/api/openapi.yaml). It identifies itself as PostGrid Address Verification API version 1.0, OpenAPI 3.0.0, and includes print and mail operations too. The document declares no license or terms-of-service field.

The generation pipeline collapses singleton reference unions and repeated identical `anyOf` references before code generation. This preserves direct response fields and avoids duplicate Go methods. No operations are removed.

The patch also names the shared search parameter's inline text branch. Use `ListParamsSearch.FromListSearchText` for text search; `FromStructuredSearchQuery` retains the structured branch.
