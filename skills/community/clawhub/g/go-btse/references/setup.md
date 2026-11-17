# go-btse: setup and reference

This module is unofficial and not affiliated with BTSE.

## Requirements

- Go 1.26.10 or newer, per `go.mod`.
- Private endpoints need an API key and secret with the permissions required by the endpoint. Read them from `BTSE_API_KEY` and `BTSE_API_SECRET` in application code.

## Install

```bash
go get github.com/psyb0t/go-btse
```

## Products and environments

| Import suffix | Operations | Production base URL | Testnet base URL |
|---|---|---|---|
| root, package `btse` | Spot orders, fills, account fees | `https://api.btse.com/spot` | `https://testapi.btse.io/spot` |
| `/futures` | Futures orders, positions, leverage, risk and margin | `https://api.btse.com/futures` | `https://testapi.btse.io/futures` |
| `/markets` | Exchange metadata, prices, order books, trades, candles and funding | `https://api.btse.com` | `https://testapi.btse.io` |
| `/wallet` | Assets, deposit addresses, history, withdrawals, transfers and conversions | `https://api.btse.com` | `https://testapi.btse.io` |
| `/earn` | Investment products, deposits, renewals, redemptions and history | `https://api.btse.com/spot` | `https://testapi.btse.io/spot` |
| `/otc` | Markets, quotes and quote acceptance | `https://api.btse.com` | `https://testapi.btse.io` |

## Auth

Import `github.com/psyb0t/go-btse/auth` and call `btseauth.NewSigner(key, secret)`. Each generated REST package accepts `WithRequestEditorFn(signer.RequestEditor)`. The signer implements BTSE's three-header HMAC-SHA384 scheme. The nonce is a timestamp in milliseconds that increases for each call on that signer. Concurrent calls can arrive out of order on the network; control request dispatch if strict arrival ordering is needed.

Public market data endpoints work without authentication. Optional signing can provide account-aware market data. The client does not automatically retry, rate-limit requests or reconcile orders.

## REST client

Each package has `NewClientWithResponses(server, opts...)`, `WithRequestEditorFn`, `WithHTTPClient` and `WithBaseURL`. Supply an `http.Client` with timeouts appropriate to the application.

An operation has a raw `Client.X`, a parsed `ClientWithResponses.XWithResponse`, and a `NewXRequest` builder. Operations with a body also support raw body variants. Use the types from the same product package as the client.

| Spot method | Endpoint |
|---|---|
| `CreateOrderWithResponse` | `POST /api/v3.3/order` |
| `GetOrderWithResponse` | `GET /api/v3.3/order` |
| `AmendOrderWithResponse` | `PUT /api/v3.3/order` |
| `CancelOrderWithResponse` | `DELETE /api/v3.3/order` |
| `CancelAllAfterWithResponse` | `POST /api/v3.3/order/cancelAllAfter` |
| `GetOpenOrdersWithResponse` | `GET /api/v3.3/user/open_orders` |
| `GetUserTradesFillsWithResponse` | `GET /api/v3.3/user/trade_history` |
| `GetAccountFeesWithResponse` | `GET /api/v3.3/user/fees` |

## Responses and pagination

`JSON200` and other status fields hold decoded bodies. `Body`, `StatusCode()`, `Status()` and `HTTPResponse` expose the raw result. Check pointer fields before dereferencing them, and inspect non-2xx responses even when the Go error is nil.

Pagination parameters differ across products. Read each generated params type and operation comment for its limits and cursor or time bounds. The client does not walk pages automatically.

## Rate limits

The spot and futures specs distinguish query limits of 15 requests per second per endpoint and 30 per second per user from order limits of 75 per second per endpoint and per user. Markets, wallet and OTC specs list 50 requests per two seconds per IP. Check the operation documentation and back off on 429 responses.

## Regeneration

REST sources are `https://docs.btse.com/specs/{product}-rest.openapi.yaml`. WebSocket sources are `https://docs.btse.com/specs/{spot,futures,otc}-websocket.asyncapi.yaml`. `make generate` downloads the documents into gitignored `api/` and runs the pinned generators. WebSocket generation converts AsyncAPI 2.6 to 3.0 first. Generated files must not be hand-edited.

## WebSocket clients

Import `ws/spot` as `spotsws`, `ws/futures` as `futuresws`, and `ws/otc` as `otcws`. Each client takes an `asyncapirt.Transport`. For spot and futures, wrap it with `btsews.HeartbeatTransport{Transport: transport}`, importing `github.com/psyb0t/go-btse/ws` as `btsews`. BTSE sends heartbeat frames as plain text; the wrapper translates the generator's JSON string representation.

| Connection | Production URL | Testnet URL |
|---|---|---|
| Spot public order books | `wss://ws.btse.com/ws/oss/spot` | `wss://testws.btse.io/ws/oss/spot` |
| Spot trades and private topics | `wss://ws.btse.com/ws/spot` | `wss://testws.btse.io/ws/spot` |
| Futures public order books | `wss://ws.btse.com/ws/oss/futures` | `wss://testws.btse.io/ws/oss/futures` |
| Futures trades and private topics | `wss://ws.btse.com/ws/futures` | `wss://testws.btse.io/ws/futures` |
| OTC | `wss://ws.btse.com/ws/otc` | `wss://testws.btse.io/ws/otc` |

Authenticate private topics on the main connection by sending an `authKeyExpires` frame. This is message authentication, not HTTP handshake authentication. The signature is lowercase hexadecimal `HMAC-SHA384(secret, "/ws/<product>" + nonce)`, where the product is `spot`, `futures` or `otc`.

Use `signer.Headers("/ws/spot", nil)` for spot, or the corresponding futures or OTC path. Read the returned values through `btseauth.HeaderAPIKey`, `btseauth.HeaderNonce` and `btseauth.HeaderSignature`, in that order, into the owning package's `AuthRequest.Args` slice. Call its generated client's `Authenticate` method with that request. `AuthRequest` marshaling fills the constant `op` value `authKeyExpires` automatically. Wait for successful authentication before subscribing to private topics. The OSS connections serve public order books.

The conversion tool retains every source channel, moves AsyncAPI 2.6 operations to the 3.0 operation map, converts server and channel references, repairs payload schemas misplaced under messages, supplies schemas for example-only L1/L2 subscriptions and constrains received topics to their channels. Snapshot and delta messages use `/data/type` as the discriminator.
