# go-etoro: setup and reference

This module is unofficial and not affiliated with eToro.

## Requirements

- Go 1.26.11 or newer, per the module's `go.mod`.
- An eToro API key and user key from the API key section of your eToro account settings, exported as `ETORO_API_KEY` and `ETORO_USER_KEY`.

## Install

```bash
go get github.com/psyb0t/go-etoro
go get github.com/google/uuid
```

`github.com/google/uuid` is for the per-request `XRequestId` values. The WebSocket transport, `github.com/psyb0t/gen-asyncapi/asyncapirt/gorillaws`, comes in with the module's own dependency on `github.com/psyb0t/gen-asyncapi`; run `go mod tidy` after the first import.

| Import path | Package | Server |
|---|---|---|
| `github.com/psyb0t/go-etoro` | `etoro` | `https://public-api.etoro.com` |
| `github.com/psyb0t/go-etoro/ws` | `etorows` | `wss://ws.etoro.com/ws` (`etorows.ServerEtoroURL`) |

## REST client

- `etoro.NewClientWithResponses(server, opts...)` builds the client. Options: `etoro.WithRequestEditorFn` (adds the auth headers to every request), `etoro.WithHTTPClient` (your own `*http.Client`, for timeouts), `etoro.WithBaseURL`.
- Each operation has three forms: `Client.X` returns the raw `*http.Response`, `ClientWithResponses.XWithResponse` returns a parsed `*XResponse`, and `NewXRequest` builds the `*http.Request` only. Operations with a JSON body also have `XWithBodyWithResponse` for a raw `io.Reader` body.
- Method names come from eToro's operation IDs. List them with `go doc github.com/psyb0t/go-etoro ClientWithResponsesInterface` rather than guessing.
- Most params structs have a required `XRequestId openapi_types.UUID`, sent as the `x-request-id` header. `openapi_types.UUID` is `uuid.UUID`, so `uuid.New()` fills it.
- Where an operation's response type name clashes with a schema name, the response wrapper gets a `2` suffix: `GetBalancesWithResponse` returns `*etoro.GetBalancesResponse2`, whose `JSON200` is the `*etoro.GetBalancesResponse` schema.

### Reading a response

| Field or method | Holds |
|---|---|
| `JSON200`, `JSON400`, ... | The decoded body for that status, nil for any other status |
| `Headers200`, `Headers429` | Declared response headers: `RateLimitLimit`, `RateLimitRemaining`, `RateLimitReset`, and `RetryAfter` on 429 |
| `Body` | The raw body bytes |
| `StatusCode()`, `Status()` | The HTTP status |
| `HTTPResponse` | The underlying `*http.Response` |

The method's `error` is non-nil only when the request could not be sent or the body could not be read or decoded. Check `StatusCode()` for API errors.

## WebSocket client

- `gorillaws.Dial(ctx, etorows.ServerEtoroURL)` opens the connection; `etorows.NewClient(conn)` wraps it; `Close()` closes it.
- Send methods: `Authenticate`, `Subscribe`, `Unsubscribe`, each taking its envelope (`ID`, `Operation`, `Data`). Per-channel variants such as `InstrumentRatesSubscribe` and `PrivatePortfolioAuthenticate` send the same envelopes. Use a fresh `ID` per request, for example `rand.Text()` from `crypto/rand`.
- Topic helpers: `etorows.InstrumentRatesAddress(id)` gives `instrument:<id>`, `etorows.InstrumentCandlesAddress(id)` gives `candle:<id>`, and `etorows.PrivatePortfolioAddressTemplate` is `private` for the user's own order and position updates.
- `Run(ctx, handler)` reads frames until `ctx` ends or a read fails, and calls one method per frame.

`Handler` methods (embed `etorows.UnimplementedHandler` to skip the ones you do not need):

| Method | Payload |
|---|---|
| `HandleOperationResponse` | `OperationResponse`, the answer to an Authenticate, Subscribe or Unsubscribe |
| `HandleInstrumentRateMessage` | `InstrumentRateEnvelope` |
| `HandleInstrumentCandleMessage` | `InstrumentCandleEnvelope` |
| `HandleInstrumentMarketStatusMessage` | `InstrumentMarketStatusEnvelope` |
| `HandleOrderUpdateMessage` | `OrderUpdateEnvelope`, for both order update types |
| `HandlePositionOpenedMessage`, `HandlePositionClosedMessage` | `PositionOpenedEnvelope`, `PositionClosedEnvelope` |
| `HandleUnknownMessage` | The raw frame and why it matched nothing |

Each push envelope has `Messages`; each item has a `Topic`, a `Type` and a JSON-encoded content string. `item.ContentValue()` decodes and validates it. `InstrumentRate` values (`Ask`, `Bid`, `LastExecution`) are `*string` because eToro sends them as JSON strings.

## Errors

| Error | When |
|---|---|
| `asyncapirt.ErrUnknownMessage` | Passed to `HandleUnknownMessage` for a frame whose type the spec does not list. `Run` keeps going unless the handler returns an error. |
| A validation error | An envelope you send, or a frame you receive, does not match eToro's schema. |
| `context.Canceled`, `context.DeadlineExceeded` | `Run` stopped because the context ended (wrapped). |

Use `errors.Is` to match them.
