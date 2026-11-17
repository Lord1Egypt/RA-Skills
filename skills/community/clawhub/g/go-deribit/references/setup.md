# go-deribit: setup and reference

This module is unofficial and not affiliated with Deribit.

## Requirements

- Go 1.26.11 or newer, per `go.mod`.
- An OAuth access token for private REST requests. The example reads `DERIBIT_ACCESS_TOKEN`; public REST market data and most public subscriptions need no credentials.

## Install

```bash
go get github.com/psyb0t/go-deribit
```

## Environments

| Environment | REST base URL | WebSocket URL |
|---|---|---|
| Testnet | `https://test.deribit.com/api/v2` | `wss://test.deribit.com/ws/api/v2` |
| Production | `https://www.deribit.com/api/v2` | `wss://deribit.com/ws/api/v2` |

## Auth

Set the HTTP header through `deribit.WithRequestEditorFn`: `req.Header.Set("Authorization", "Bearer "+token)`. The token comes from `/public/auth`, which supports client credentials, a client signature and refresh-token grants. The published OpenAPI document omits security schemes and marks parameters from different grant types required simultaneously. Generated auth params preserve that upstream contract. Consult the endpoint description when choosing grant values.

WebSocket private subscriptions and raw market-data channels require an authenticated connection. Raw channels can still use `public/subscribe`; the method name alone does not establish whether authentication is required. `block_rfq.trades.{currency}` is public, while user channels and the other block/RFQ channels use private subscriptions. The AsyncAPI document covers subscriptions only, so authentication, token refresh, unsubscribe requests and JSON-RPC command replies remain the caller's responsibility.

## REST client

- `deribit.NewClientWithResponses(server, opts...)` creates the parsed client.
- Options include `deribit.WithRequestEditorFn`, `deribit.WithHTTPClient` for a custom client with timeouts, and `deribit.WithBaseURL`.
- Each operation has `Client.X` returning `*http.Response`, `ClientWithResponses.XWithResponse` returning a parsed response and `NewXRequest` constructing a request.
- All 186 paths use GET query parameters, including state-changing operations. Treat order and account methods as actions even though the HTTP verb is GET.

## Main operations

| Method | Endpoint |
|---|---|
| `PublicGetTimeWithResponse` | `GET /public/get_time` |
| `PublicGetInstrumentsWithResponse` | `GET /public/get_instruments` |
| `PublicGetOrderBookWithResponse` | `GET /public/get_order_book` |
| `PublicTickerWithResponse` | `GET /public/ticker` |
| `PublicGetLastTradesByInstrumentWithResponse` | `GET /public/get_last_trades_by_instrument` |
| `PublicAuthWithResponse` | `GET /public/auth` |
| `PrivateGetAccountSummaryWithResponse` | `GET /private/get_account_summary` |
| `PrivateGetPositionsWithResponse` | `GET /private/get_positions` |
| `PrivateGetOpenOrdersByInstrumentWithResponse` | `GET /private/get_open_orders_by_instrument` |
| `PrivateBuyWithResponse`, `PrivateSellWithResponse` | `GET /private/buy`, `GET /private/sell` |
| `PrivateEditWithResponse`, `PrivateCancelWithResponse` | `GET /private/edit`, `GET /private/cancel` |

## Responses

`JSON200` holds the decoded success body when present. `Body`, `StatusCode()`, `Status()` and `HTTPResponse` expose the original response. Response models follow the spec's JSON-RPC envelopes, with `Result` carrying the payload. Check optional pointers before dereferencing. Numeric fields map to `float64` unless the spec declares an integer.

## Pagination and limits

Pagination varies by endpoint. Trade history can use trade IDs or timestamps and returns a `has_more` indicator where declared. Other endpoints use continuation tokens or offsets. Inspect the specific generated params and result types instead of sharing one pagination loop across all operations. Handle API rate-limit errors with bounded backoff; the client does not retry automatically.

## WebSocket client

Import `github.com/psyb0t/go-deribit/ws` as `deribitws`. `NewClient` accepts an `asyncapirt.Transport`, and `Run(ctx, handler)` reads notifications until cancellation or failure. Embed `UnimplementedHandler` for channels you do not consume. `DecodeReceivedMessage` decodes and validates one incoming frame.

`ServerProductionURL` and `ServerTestnetURL` contain the WSS endpoints. For platform state, call `SendSubscribePlatformState` with a `PlatformStateSubscribeRequestPayload`: set `ID` and `Params.Channels` to `[]string{"platform_state"}`. Its marshaler fills in the JSON-RPC version and method constants. Handle notifications with `HandlePlatformStateSubscriptionMessage(ctx, PlatformStateSubscriptionMessagePayload)`.

JSON-RPC notifications have `method: "subscription"`, a channel under `params.channel` and notification data under `params.data`. Channel matching chooses the generated message type. The source document has 43 channels and 86 operations; the patch preserves them all. Parameterized channels use the instrument, interval, group, depth or currency params declared by the spec.

The source document contains inline message definitions with incomplete JSON-RPC envelopes and reversed operation message references. `scripts/patch-asyncapi.sh` repairs those references and frames, restores subscription request schemas, replaces parenthesized channel parameters with braces and distinguishes raw user-order notifications from interval notifications. It fixes quote required-field typos, permits null in numeric fields the provider describes as nullable, and converts explicit float formats to double precision.

The patches reconcile schemas with published examples: repeated data, trades, orders, legs and makers become arrays while preserving item schemas; order flags become booleans; scalar maker values stay strings; documented null IDs remain nullable. Optional fields absent from notification schemas are retained, and incremental ticker statistics accept partial updates.

The patch makes `app_name` optional on block trade confirmations and `settlement_price` optional on spot position updates, as their descriptions state. Both spec patches normalize provider descriptions for generated comments without changing wire values.
