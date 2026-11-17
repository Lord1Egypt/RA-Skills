# go-solana-tracker: setup and reference

This module is unofficial and not affiliated with Solana Tracker.

## Requirements

- Go 1.26.10 or newer, per `go.mod`.
- A Data API subscription key exported as `SOLANA_TRACKER_API_KEY`.
- Premium, Business or Enterprise access for Datastream.

## Install

```bash
go get github.com/psyb0t/go-solana-tracker
```

| Import path | Package | Endpoint |
| --- | --- | --- |
| `github.com/psyb0t/go-solana-tracker` | `solanatracker` | `https://data.solanatracker.io` |
| `github.com/psyb0t/go-solana-tracker/ws` | `solanatrackerws` | `wss://datastream.solanatracker.io/{apiKey}` |

## Auth

Pass `solanatracker.WithRequestEditorFn` to `solanatracker.NewClientWithResponses`. The editor sets `req.Header.Set("x-api-key", os.Getenv("SOLANA_TRACKER_API_KEY"))`. The full compiling example is in the repository's `example_test.go` and README.

Datastream uses the subscription key in the URL path. `solanatrackerws.ServerProductionURLWith(url.PathEscape(key))` fills that path. The generated helper substitutes its argument directly; escape it as a path segment first. Never log the resulting URL. The default `ServerProductionURL` contains a placeholder and must not be used as a real authenticated endpoint.

## REST client

- `NewClientWithResponses(server, opts...)` returns the parsed response client.
- `WithRequestEditorFn` adds authentication. `WithHTTPClient` accepts an `http.Client` with explicit timeouts. `WithBaseURL` overrides the base.
- Each operation also has a raw `Client` method and a `New...Request` builder.
- The spec has no operation IDs, so generated method names follow HTTP methods and paths.

Selected methods, verified against `client.gen.go`:

| Method | Endpoint |
| --- | --- |
| `GetSearchWithResponse` | `GET /search` |
| `GetTokensTokenAddressWithResponse` | `GET /tokens/{tokenAddress}` |
| `GetTokensByPoolPoolAddressWithResponse` | `GET /tokens/by-pool/{poolAddress}` |
| `GetTokensTokenAddressHoldersPaginatedWithResponse` | `GET /tokens/{tokenAddress}/holders/paginated` |
| `GetTokensTokenAddressAthWithResponse` | `GET /tokens/{tokenAddress}/ath` |
| `GetTokensLatestWithResponse` | `GET /tokens/latest` |
| `PostTokensMultiWithResponse` | `POST /tokens/multi` |
| `GetTokensTrendingWithResponse` | `GET /tokens/trending` |
| `GetTokensVolumeWithResponse` | `GET /tokens/volume` |
| `GetPriceWithResponse` | `GET /price` |
| `GetPriceHistoryWithResponse` | `GET /price/history` |
| `GetPriceHistoryRangeWithResponse` | `GET /price/history/range` |
| `GetPriceMultiWithResponse`, `PostPriceMultiWithResponse` | `GET`, `POST /price/multi` |
| `GetWalletOwnerWithResponse` | `GET /wallet/{owner}` |
| `GetWalletOwnerPagePageWithResponse` | `GET /wallet/{owner}/page/{page}` |
| `GetWalletOwnerTradesWithResponse` | `GET /wallet/{owner}/trades` |
| `GetTradesTokenAddressWithResponse` | `GET /trades/{tokenAddress}` |
| `GetChartTokenWithResponse` | `GET /chart/{token}` |
| `GetPnlWalletWithResponse` | `GET /pnl/{wallet}` |
| `GetPnlWalletTokenWithResponse` | `GET /pnl/{wallet}/{token}` |
| `GetTopTradersAllWithResponse` | `GET /top-traders/all` |
| `GetStatsTokenWithResponse` | `GET /stats/{token}` |
| `GetCreditsWithResponse` | `GET /credits` |
| `GetSubscriptionWithResponse` | `GET /subscription` |

The client has a method for every operation in the spec. Look up the rest with `go doc` as the skill describes, including holders, risk charts, pool-specific variants, timeframes, deployer data, first buyers and other operations.

## Responses

`JSON200` is the decoded success body and can be nil. `StatusCode()`, `Status()`, `Body` and `HTTPResponse` retain the HTTP response. HTTP 401, 403 and 429 do not automatically produce a Go error; the error return covers transport and decoding failures. Typed error fields exist only for statuses declared by that operation.

Number fields use `float64`; optional fields often use pointers. Check pointers before dereferencing. `PriceResponse.Price` is optional. Trade activity can contain either a swap or a liquidity event, so decode the generated union according to its event type.

## Pagination

- Search accepts `Page`, `Limit` and `Cursor`. The organic page limit is at most 500, or 100 with full format. Curated rows can make the returned array larger than that limit.
- Paginated holders return `Cursor` and `HasMore`. Pass the returned cursor unchanged until `HasMore` is false. The page limit ranges from 1 to 5000.
- Trade routes return `NextCursor`, whose wire value can be an integer, string or null. The generated union exposes `AsTokenTradesResponseNextCursor0` for integers and `AsTokenTradesResponseNextCursor1` for strings. Keep token, pool, wallet, events and sort filters unchanged between cursor requests.
- `GetWalletOwnerPagePageWithResponse` takes the page number as a path argument. Its page size is 250 tokens.

## WebSocket client

Supply an implementation of `github.com/psyb0t/gen-asyncapi/asyncapirt.Transport` to `solanatrackerws.NewClient(conn)`. It must implement `ReadMessage(context.Context) ([]byte, error)`, `WriteMessage(context.Context, []byte) error` and `Close() error`, allowing one reader while others write. Configure its dial and read timeouts. Redact connection paths and URLs from transport logs because the path contains the API key. Close the client with `Close()`.

`Run(ctx, handler)` reads and dispatches frames. Embed `solanatrackerws.UnimplementedHandler` and override the event handlers the integration needs. `DecodeReceivedMessage` decodes individual frames for offline processing.

Room methods use names such as `SubscribeToPriceToken`, `UnsubscribeFromPriceToken`, `SubscribeToTokenTx`, `SubscribeToWallet`, `SubscribeToHolders` and `SubscribeToJupiterDcaAllEvents`. Each takes a generated payload with a `Room` field. Inspect its room pattern or enum before constructing it. The payload marshaler supplies fixed protocol fields such as the command type.

The client covers every channel in the Datastream spec. It does not include the separate solana-rpc or raptor APIs. The source defines the server perspective; normalization swaps operation directions, hoists messages, constrains room matching and includes joined acknowledgements. Identical price-all and price-pool event schemas share the price-pool message and handler types.

`BalanceUpdate.Amount` uses `float64`. The source declares an integer, but its published balance examples contain fractions. The normalization accepts both forms.

DCA events require their `eventName`; position snapshots require `pubkey` and `writeVersion`. The source omits required fields on these union branches, so normalization adds the discriminating fields shown in the provider's examples.

The source describes `ping`, `left` and `error` envelopes in prose without defining global message schemas. Such frames can reach `HandleUnknownMessage`; inspect them without logging secrets. Handle cancellation and reconnect policy in the integration.
