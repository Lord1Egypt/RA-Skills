# go-kalshi: setup and reference

This module is unofficial and not affiliated with Kalshi.

## Requirements

- Go 1.26.11 or newer, per the module's `go.mod`.
- A Kalshi API key: the key ID, exported as `KALSHI_API_KEY_ID`, and the private key PEM Kalshi gives you, exported as `KALSHI_PRIVATE_KEY` or read from a file. RSA (PKCS#1 or PKCS#8) and Ed25519 keys work.

## Install

```bash
go get github.com/psyb0t/go-kalshi
```

The WebSocket transport, `github.com/psyb0t/gen-asyncapi/asyncapirt/gorillaws`, comes in with the module's own dependency on `github.com/psyb0t/gen-asyncapi`; run `go mod tidy` after the first import.

| Import path | Package | Production | Demo |
|---|---|---|---|
| `github.com/psyb0t/go-kalshi` | `kalshi` | `https://external-api.kalshi.com/trade-api/v2` | `https://external-api.demo.kalshi.co/trade-api/v2` |
| `github.com/psyb0t/go-kalshi/ws` | `kalshiws` | `kalshiws.ServerProductionURL` | |
| `github.com/psyb0t/go-kalshi/perpsws` | `kalshiperpsws` | `kalshiperpsws.ServerProductionURL` | `kalshiperpsws.ServerDemoURL` |
| `github.com/psyb0t/go-kalshi/auth` | `kalshiauth` | | |

## Signing

- `kalshiauth.ParsePrivateKeyPEM(data)` returns a `crypto.Signer` from a PEM block.
- `kalshiauth.NewSigner(keyID, key)` returns a `*Signer`.
- `signer.RequestEditor` matches `kalshi.RequestEditorFn`; pass it with `kalshi.WithRequestEditorFn`. It signs timestamp + method + URL path (no query string) on every request.
- `signer.Headers(method, path)` returns the `KALSHI-ACCESS-KEY`, `KALSHI-ACCESS-TIMESTAMP` and `KALSHI-ACCESS-SIGNATURE` headers for a WebSocket handshake. `kalshiauth.WebSocketPath` is the market data path.

Public endpoints such as `GetMarketsWithResponse` work without the signer.

## REST client

- `kalshi.NewClientWithResponses(server, opts...)`. Options: `kalshi.WithRequestEditorFn`, `kalshi.WithHTTPClient` (your own `*http.Client`, for timeouts), `kalshi.WithBaseURL`.
- Each operation has `Client.X` (raw `*http.Response`), `ClientWithResponses.XWithResponse` (parsed) and `NewXRequest` (request only). Operations with a body also have `XWithBodyWithResponse`.
- Names come from Kalshi's operation IDs. Look one up with `go doc github.com/psyb0t/go-kalshi ClientWithResponsesInterface` rather than guessing.
- Response wrappers whose names clash with a schema get a `2` suffix: `GetBalanceWithResponse` returns `*kalshi.GetBalanceResponse2`, whose `JSON200` is the `*kalshi.GetBalanceResponse` schema.
- Money: `...Dollars` fields are `FixedPointDollars`, a decimal string such as `"0.5600"`. Plain integer fields such as `Balance` are cents.
- Lists page with `Cursor`: pass the previous response's `Cursor` in the params until it comes back empty.

### Reading a response

| Field or method | Holds |
|---|---|
| `JSON200` | The decoded body on success, nil otherwise |
| `JSON401`, `JSON500` and so on | `ErrorResponse` (`Code`, `Message`, `Details`), present only for the error statuses that operation declares (`GetBalance` declares 401 and 500, `GetMarkets` none) |
| `Body`, `StatusCode()`, `Status()`, `HTTPResponse` | The raw response |

## WebSocket clients

- Dial with `gorillaws.Dial(ctx, url, gorillaws.WithHeader(name, value)...)` using the signed headers, wrap with `NewClient(conn)`, close with `Close()`.
- Commands: `SendSubscribe`, `SendUnsubscribe`, `SendListSubscriptions`, `SendUpdateSubscription`, `SendUpdateSubscriptionDelete`, `SendUpdateSubscriptionSingleSid`. `kalshiws` also has `SendCfBenchmarksUpdateSubscription` and `SendPythUpdateSubscription`.
- `Run(ctx, handler)` reads frames until `ctx` ends or a read fails.
- Kalshi's heartbeat is a WebSocket ping control frame, which the transport answers on its own.

`kalshiws.Handler` methods (embed `kalshiws.UnimplementedHandler` to skip the ones you do not need):

| Group | Methods |
|---|---|
| Command responses | `HandleSubscribedResponse`, `HandleUnsubscribedResponse`, `HandleOkResponse`, `HandleListSubscriptionsResponse`, `HandleErrorResponse`, `HandleSubscribedUnderlyingsResponse`, `HandleSubscribedIndicesResponse` |
| Market data | `HandleOrderbookSnapshot`, `HandleOrderbookDelta`, `HandleTicker`, `HandleTrade`, `HandleMarketMetadataUpdated` |
| Lifecycle | `HandleMarketLifecycleV2`, `HandleEventLifecycle`, `HandleEventFeeUpdate`, `HandleMultivariateMarketLifecycle` |
| Account | `HandleFill`, `HandleMarketPosition`, `HandleUserOrder`, `HandleOrderGroupUpdates` |
| RFQ | `HandleRfqCreated`, `HandleRfqDeleted`, `HandleQuoteCreated`, `HandleQuoteAccepted`, `HandleQuoteExecuted` |
| Indices | `HandleCfbenchmarksValue`, `HandleCfbenchmarksIndexList`, `HandleCfbenchmarksValue5Hz`, `HandleCfbenchmarks5HzIndexList`, `HandlePythValue`, `HandlePythUnderlyingList` |
| Other | `HandleUnknownMessage` |

`kalshiperpsws.Handler` has the command responses, `HandleOrderbookSnapshot`, `HandleOrderbookDelta`, `HandleTicker`, `HandleTrade`, `HandleFill`, `HandleUserOrder`, `HandleOrderGroupUpdates` and `HandleUnknownMessage`.

Each push payload has `Type`, `Sid` (the subscription ID) and `Msg` with the data.

## Errors

| Error | When |
|---|---|
| `commerr.ErrParseFailed` | `ParsePrivateKeyPEM` got no PEM block or an unsupported one. |
| `commerr.ErrValidationFailed` | The key is neither RSA nor Ed25519 (`NewSigner`, or a PKCS#8 key in `ParsePrivateKeyPEM`). |
| `asyncapirt.ErrUnknownMessage` | Passed to `HandleUnknownMessage` for a frame whose type the spec does not list. `Run` keeps going unless the handler returns an error. |
| A validation error | A command you send, or a frame you receive, does not match Kalshi's schema. |
| `context.Canceled`, `context.DeadlineExceeded` | `Run` stopped because the context ended (wrapped). |

Use `errors.Is` to match them.
