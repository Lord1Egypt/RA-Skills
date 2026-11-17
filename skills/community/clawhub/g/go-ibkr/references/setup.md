# go-ibkr: setup and reference

This module is unofficial and not affiliated with Interactive Brokers.

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- An Interactive Brokers account, and either a running Client Portal Gateway or OAuth access to `https://api.ibkr.com`.

## Install

```bash
go get github.com/psyb0t/go-ibkr
```

## Auth

### Client Portal Gateway

1. Download and run the gateway from Interactive Brokers.
2. Open `https://localhost:5000` in a browser and log in.
3. Point the client at `https://localhost:5000` (or wherever the gateway runs). The gateway keeps the brokerage session and authenticates every request it forwards, so the client sends no credentials.
4. Check `GetBrokerageStatusWithResponse` (`POST /v1/api/iserver/auth/status`): `JSON200.Authenticated` must be true.
5. Call `GetSessionTokenWithResponse` (`POST /v1/api/tickle`) about once a minute to keep the session alive. `LogoutWithResponse` ends it.

The gateway serves a self-signed certificate. Pass `ibkr.WithHTTPClient` with a transport that skips verification only for that local gateway.

### OAuth

Get the access token with your own OAuth code; the client has no OAuth flow. Use `https://api.ibkr.com` as the base URL and set `Authorization: Bearer <token>` in an `ibkr.WithRequestEditorFn`.

## Client

- `ibkr.NewClientWithResponses(server, opts...)`. Options: `ibkr.WithHTTPClient`, `ibkr.WithRequestEditorFn`, `ibkr.WithBaseURL`.
- `server` is scheme and host only. The generated paths include `/v1/api/...` and `/gw/api/v1/...`.
- Each operation has `Client.X` (raw `*http.Response`), `ClientWithResponses.XWithResponse` (parsed) and `NewXRequest` (request only). Operations with a body also have `XWithBodyWithResponse` taking a raw `io.Reader`.
- Method names are the spec's operation IDs. Each method's doc comment names its path, so look one up with `go doc github.com/psyb0t/go-ibkr ClientWithResponsesInterface | grep '/iserver/accounts'`. Duplicate operation IDs in the spec get a numeric suffix (`GetTradingSchedule2`).

## Common operations

| Method | Endpoint |
|---|---|
| `GetBrokerageStatusWithResponse` | `POST /v1/api/iserver/auth/status` |
| `GetSessionTokenWithResponse` | `POST /v1/api/tickle` |
| `GetBrokerageAccountsWithResponse` | `GET /v1/api/iserver/accounts` |
| `GetPaginatedPositionsWithResponse` | `GET /v1/api/portfolio/{accountId}/positions/{pageId}` |
| `GetContractSymbolsWithResponse` | `GET /v1/api/iserver/secdef/search` |
| `GetMdSnapshotWithResponse` | `GET /v1/api/iserver/marketdata/snapshot` |
| `GetOpenOrdersWithResponse` | `GET /v1/api/iserver/account/orders` |
| `GetOrderStatusWithResponse` | `GET /v1/api/iserver/account/order/status/{orderId}` |
| `SubmitNewOrderWithResponse` | `POST /v1/api/iserver/account/{accountId}/orders` |
| `ConfirmOrderReplyWithResponse` | `POST /v1/api/iserver/reply/{replyId}` |
| `ModifyOpenOrderWithResponse` | `POST /v1/api/iserver/account/{accountId}/order/{orderId}` |
| `CancelOpenOrderWithResponse` | `DELETE /v1/api/iserver/account/{accountId}/order/{orderId}` |
| `LogoutWithResponse` | `POST /v1/api/logout` |

`GetMdSnapshot` takes `Conids` as a comma-separated string and `Fields` as a comma-separated string of field codes. Its `JSON200` is a list of union items.

## Responses

| Field or method | Holds |
|---|---|
| `JSON200` | The decoded body on success, nil otherwise |
| `Body`, `StatusCode()`, `Status()`, `HTTPResponse` | The raw response |

Some response schemas are `oneOf` unions, such as the `GetMdSnapshot` items; read them with the generated `As...` methods, or decode `Body` into your own type.
