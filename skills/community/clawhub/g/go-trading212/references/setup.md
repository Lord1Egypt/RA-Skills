# go-trading212: setup and reference

This module is unofficial and not affiliated with Trading 212.

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- A Trading 212 API key and secret from the API section of the account settings in the Trading 212 app, exported as `TRADING212_API_KEY` and `TRADING212_API_SECRET`.

## Install

```bash
go get github.com/psyb0t/go-trading212
```

## Environments

| Environment | Base URL |
|---|---|
| Demo (paper trading) | `https://demo.trading212.com` |
| Live (real money) | `https://live.trading212.com` |

Keys are tied to one environment.

## Auth

HTTP Basic auth in a request editor: `req.SetBasicAuth(key, secret)`. The spec also lists a legacy scheme where the bare API key is the `Authorization` header; to use it, set `req.Header.Set("Authorization", key)` in the editor instead.

## Client

- `trading212.NewClientWithResponses(server, opts...)`. Options: `trading212.WithRequestEditorFn`, `trading212.WithHTTPClient` (your own `*http.Client`, for timeouts), `trading212.WithBaseURL`.
- Each operation has `Client.X` (raw `*http.Response`), `ClientWithResponses.XWithResponse` (parsed) and `NewXRequest` (request only). Operations with a body also have `XWithBodyWithResponse` taking a raw `io.Reader`.

## Operations

| Method | Endpoint |
|---|---|
| `GetAccountSummaryWithResponse` | `GET /api/v0/equity/account/summary` |
| `GetPositionsWithResponse` | `GET /api/v0/equity/positions` |
| `OrdersWithResponse` | `GET /api/v0/equity/orders` (open orders) |
| `OrderByIdWithResponse` | `GET /api/v0/equity/orders/{id}` |
| `PlaceMarketOrderWithResponse` | `POST /api/v0/equity/orders/market` |
| `PlaceLimitOrderWithResponse` | `POST /api/v0/equity/orders/limit` |
| `PlaceStopOrder1WithResponse` | `POST /api/v0/equity/orders/stop` |
| `PlaceStopOrderWithResponse` | `POST /api/v0/equity/orders/stop_limit` |
| `CancelOrderWithResponse` | `DELETE /api/v0/equity/orders/{id}` |
| `Orders1WithResponse` | `GET /api/v0/equity/history/orders` |
| `DividendsWithResponse` | `GET /api/v0/equity/history/dividends` |
| `TransactionsWithResponse` | `GET /api/v0/equity/history/transactions` |
| `GetReportsWithResponse`, `RequestReportWithResponse` | `GET`, `POST /api/v0/equity/history/exports` |
| `ExchangesWithResponse` | `GET /api/v0/equity/metadata/exchanges` |
| `InstrumentsWithResponse` | `GET /api/v0/equity/metadata/instruments` |
| `GetAllWithResponse`, `CreateWithResponse` | `GET`, `POST /api/v0/equity/pies` |
| `GetDetailedWithResponse`, `UpdateWithResponse`, `DeleteWithResponse` | `GET`, `POST`, `DELETE /api/v0/equity/pies/{id}` |
| `DuplicatePieWithResponse` | `POST /api/v0/equity/pies/{id}/duplicate` |

Request bodies: `MarketRequest`, `LimitRequest`, `StopRequest`, `StopLimitRequest`, `PieRequest`, `DuplicateBucketRequest`, `PublicReportRequest`.

## Responses

| Field or method | Holds |
|---|---|
| `JSON200` | The decoded body on success, nil otherwise |
| `Body`, `StatusCode()`, `Status()`, `HTTPResponse` | The raw response |

Number fields are `float64`; most fields are pointers.

## Pagination

The history endpoints (`Orders1`, `Dividends`, `Transactions`) take `Cursor` and `Limit` params and return a paginated response with `Items` and `NextPagePath`. Keep requesting with the cursor from `NextPagePath` until it is nil.

## Rate limits

Trading 212 limits each endpoint separately, some to one request every few seconds, and the generated method's doc comment states its limit. Over the limit the API answers 429. Back off on 429 instead of retrying in a tight loop.
