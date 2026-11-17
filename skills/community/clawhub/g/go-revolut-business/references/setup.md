# go-revolut-business: setup and reference

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- Runtime dependencies: `github.com/oapi-codegen/runtime` and `github.com/google/uuid`.
- A Revolut Business API access token.

## Install

```bash
go get github.com/psyb0t/go-revolut-business
```

The package name is `revolut`. The module path ends in `go-revolut-business`, so import it with an explicit name:

```go
import revolut "github.com/psyb0t/go-revolut-business"
```

## Environments

| Environment | Base URL |
|---|---|
| Production | `https://b2b.revolut.com/api/1.0` |
| Sandbox | `https://sandbox-b2b.revolut.com/api/1.0` |

Sandbox uses test data and needs its own sandbox account and certificate.

## Auth

Every request carries `Authorization: Bearer <access_token>`. Revolut issues the token through OAuth2: a JWT client assertion signed with the private key whose certificate is uploaded in the Business API settings, exchanged together with an authorisation code or refresh token at `/auth/token`. Access tokens expire after 40 minutes.

The module does not implement that flow. Set the token with a `RequestEditorFn` passed as a client option (`revolut.WithRequestEditorFn`), as in the SKILL.md example. A `RequestEditorFn` can also be passed per call as the last arguments of any method. Read the token from the environment; when it expires, the editor can fetch a fresh one from wherever the program keeps it.

## Client options

| Option | Effect |
|---|---|
| `revolut.WithRequestEditorFn(fn)` | Runs `fn` on every request, used for the auth header. |
| `revolut.WithHTTPClient(doer)` | Replaces `http.DefaultClient`, for timeouts or transport settings. |
| `revolut.WithBaseURL(url)` | Overrides the server passed to the constructor. |

## Calling operations

Each operation `X` in the spec has:

- `client.XWithResponse(ctx, pathParams..., params, ...)` returning `*XResponse`.
- For operations with a JSON body, `client.XWithResponse(ctx, body)` takes the typed `XJSONRequestBody`, and `client.XWithBodyWithResponse(ctx, contentType, io.Reader)` takes raw bytes.

Some operations, by name in `client.gen.go`:

| Method | Endpoint |
|---|---|
| `GetAccountsWithResponse(ctx)` | `GET /accounts` |
| `GetAccountWithResponse(ctx, accountId)` | `GET /accounts/{account_id}` |
| `GetAccountDetailsWithResponse(ctx, accountId)` | `GET /accounts/{account_id}/bank-details` |
| `GetTransactionsWithResponse(ctx, *GetTransactionsParams)` | `GET /transactions` |
| `GetCounterpartiesWithResponse(ctx, *GetCounterpartiesParams)` | `GET /counterparties` |
| `CreatePaymentWithResponse(ctx, CreatePaymentJSONRequestBody)` | `POST /pay` |

Search `client.gen.go` for `WithResponse(` to find the rest. Do not guess a method name.

`GetTransactionsParams` fields are all optional pointers: `From`, `To`, `Account`, `Count`, `Type`, `RequestId`, `State`.

## Responses

Every `XResponse` has:

- `Body []byte` and `HTTPResponse *http.Response`.
- `StatusCode()` and `Status()`.
- One `JSONnnn` field per documented status, for example `JSON200` or `JSON201`, set only when the response had that status.
- `JSONDefault *revolut.Error` for any other status, with `Code int` and `Message string`.

A method returns a non-nil error only for transport failures and bodies that do not decode. A 4xx or 5xx is a normal response.

## Regenerating

`client.gen.go` is generated. For changes to the client itself, see `AGENTS.md` in the repository.
