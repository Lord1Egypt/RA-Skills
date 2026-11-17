# go-hubspot: setup and reference

## Requirements

- Go 1.26.11 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.
- A HubSpot private app access token or OAuth access token with the scopes the endpoints you call need.

## Install

```bash
go get github.com/psyb0t/go-hubspot
```

The package name is `hubspot`:

```go
import "github.com/psyb0t/go-hubspot"
```

## Clients

- `hubspot.NewClientWithResponses(server, opts...)` returns `*ClientWithResponses`, whose `...WithResponse` methods decode the body into typed fields. Use this one.
- `hubspot.NewClient(server, opts...)` returns `*Client`, whose methods return the raw `*http.Response`.
- Options: `hubspot.WithRequestEditorFn(fn)` runs `fn` on every request (auth goes here), `hubspot.WithHTTPClient(doer)` swaps the `*http.Client`, for example to set a timeout.
- Every method also takes trailing `reqEditors ...RequestEditorFn` for per-call changes.

## Auth

The spec lists OAuth 2, private app keys and a developer API key. Private app and OAuth access tokens both go in a Bearer header:

| Scheme | How |
|---|---|
| Bearer (private app or OAuth token) | `req.Header.Set("Authorization", "Bearer "+token)` |
| Developer API key, some developer endpoints only | `hapikey` query parameter |

For the developer key, in the request editor:

```go
q := req.URL.Query()
q.Set("hapikey", os.Getenv("HUBSPOT_DEVELOPER_API_KEY"))
req.URL.RawQuery = q.Encode()
```

## Method names

Names come from the spec's operation IDs. They join the HTTP method, the path with the API version date, and an action, so they are long:

| Method | Request |
|---|---|
| `Getcrmobjects202603contactsContactIdGetByIdWithResponse` | `GET /crm/objects/2026-03/contacts/{contactId}` |
| `Postcrmobjects202603contactsCreateWithResponse` | `POST /crm/objects/2026-03/contacts` |
| `Patchcrmobjects202603contactsContactIdUpdateWithResponse` | `PATCH /crm/objects/2026-03/contacts/{contactId}` |
| `Deletecrmobjects202603contactsContactIdArchiveWithResponse` | `DELETE /crm/objects/2026-03/contacts/{contactId}` |
| `Postcrmobjects202603contactssearchDoSearchWithResponse` | `POST /crm/objects/2026-03/contacts/search` |
| `Postcrmobjects202603contactsbatchreadReadWithResponse` | `POST /crm/objects/2026-03/contacts/batch/read` |

To find the method for another path, filter the method listing by the path, for example `go doc github.com/psyb0t/go-hubspot ClientWithResponsesInterface | grep '/crm/objects/2026-03/companies'`. The doc comment above each method names its path and operation ID. Never guess a name: the version date in the path changes between spec releases.

Each operation with a JSON body has two forms: `XWithResponse(ctx, ..., body)` takes the typed body, `XWithBodyWithResponse(ctx, ..., contentType, io.Reader)` takes raw bytes.

Query parameters go in a `*XParams` struct; pass `nil` when you set none. Optional fields are pointers.

## Responses

Every `XResponse` has:

- `Body []byte`, the raw body, and `HTTPResponse *http.Response`.
- `StatusCode() int` and `Status() string`.
- One `JSON<code>` field per documented JSON response, for example `JSON200` or `JSON201`. It is nil when the status was different.

CRM records decode into structs with `Id string`, `Properties map[string]string`, `CreatedAt`, `UpdatedAt` and `Archived`. Search results come as `Results`, `Total` and `Paging`.

Numbers without a format in the spec are `float64`.

## Errors

- The returned `error` covers network failures, request building and JSON decoding only.
- HubSpot errors (401, 403, 404, 409, 429 and so on) come back with `err == nil`. Check `StatusCode()` and read `Body`.
- On 429, back off before retrying; HubSpot rate limits per app and per account.
