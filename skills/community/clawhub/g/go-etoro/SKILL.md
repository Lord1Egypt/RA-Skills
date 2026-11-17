---
name: go-etoro
description: Unofficial Go clients for the eToro public API, generated from the specs eToro publishes. The root package `etoro` (`github.com/psyb0t/go-etoro`) is an oapi-codegen REST client for `https://public-api.etoro.com` with a typed `...WithResponse` method per endpoint (balances, market data, instruments, rates, candles, feeds, portfolios, transfers, posts). The `etorows` package (`github.com/psyb0t/go-etoro/ws`) is a typed WebSocket client for `wss://ws.etoro.com/ws` that authenticates, subscribes to topics and decodes instrument rate, candle and market status pushes and order and position updates through a `Handler`. Use when Go code needs to call the eToro API or stream eToro market data, or already imports go-etoro.
license: MIT
homepage: https://github.com/psyb0t/go-etoro
user-invocable: true
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the code you write talks HTTPS to public-api.etoro.com and WSS to ws.etoro.com only."
---

# go-etoro

Unofficial, typed Go clients for the eToro public API: REST in the root package `etoro`, WebSocket in `etorows` under `ws/`.

For install details, the request ID header, rate limit headers and the WebSocket push types, see [references/setup.md](references/setup.md).

## Security & safety

- eToro authenticates with two keys, `x-api-key` and `x-user-key`. Read them from environment variables (`ETORO_API_KEY`, `ETORO_USER_KEY`). Never hardcode them, commit them or log them, and never print a request with its headers.
- Requests go only to `https://public-api.etoro.com` and `wss://ws.etoro.com/ws`. Do not point the client at another host with the keys attached.
- The API can move real money and publish content: transfers (`PostMoneyTransfer...`), posts, comments, likes and deletes. Call those only when the user asked for that exact action. Default to read-only endpoints.

## When to use

- Go code needs eToro account balances, instruments, rates, candles, feeds or portfolio data.
- Go code needs a live stream of eToro instrument rates, candles, market status or the user's order and position updates.
- The project already imports `github.com/psyb0t/go-etoro` or `github.com/psyb0t/go-etoro/ws`.

## When NOT to use

- The code is not Go. This module ships only Go packages.
- You need a broker other than eToro, or an SDK maintained by eToro. This one is unofficial and not affiliated with eToro.
- You want to change the generated client itself. `client.gen.go` and `ws/etorows.gen.go` are generated; see `AGENTS.md` in the repo.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-etoro`, from inside your module:

```bash
go doc github.com/psyb0t/go-etoro ClientWithResponsesInterface         # every endpoint method
go doc github.com/psyb0t/go-etoro GetMarketDataInstrumentsRatesParams  # one method, params type or model
go doc -all github.com/psyb0t/go-etoro                                 # the whole package
go doc github.com/psyb0t/go-etoro/ws Handler                           # every WebSocket message handler
go doc github.com/psyb0t/go-etoro/ws Client                            # the WebSocket Send methods and Run
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-etoro.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. Where a response type name clashes with a schema name, the response wrapper gets a `2` suffix, so `GetBalancesWithResponse` returns `*etoro.GetBalancesResponse2`.

## REST

Every endpoint is a method on `ClientWithResponses` named after its operation ID plus `WithResponse`. Most take a `*...Params` struct, and most params structs carry a required `XRequestId` (a UUID per request).

```go
import (
	"context"
	"fmt"
	"net/http"
	"os"

	"github.com/google/uuid"
	"github.com/psyb0t/go-etoro"
)

auth := etoro.WithRequestEditorFn(
	func(_ context.Context, req *http.Request) error {
		req.Header.Set("x-api-key", os.Getenv("ETORO_API_KEY"))
		req.Header.Set("x-user-key", os.Getenv("ETORO_USER_KEY"))

		return nil
	},
)

client, err := etoro.NewClientWithResponses(
	"https://public-api.etoro.com",
	auth,
)
if err != nil {
	return err
}

balances, err := client.GetBalancesWithResponse(
	ctx,
	&etoro.GetBalancesParams{XRequestId: uuid.New()},
)
if err != nil {
	return err // transport failure
}

if balances.JSON200 == nil {
	return fmt.Errorf("balances: %s", balances.Status())
}

total := balances.JSON200.TotalBalance // *float64

rates, err := client.GetMarketDataInstrumentsRatesWithResponse(
	ctx,
	&etoro.GetMarketDataInstrumentsRatesParams{
		InstrumentIds: []int32{1001},
		XRequestId:    uuid.New(),
	},
)
```

The error return covers only transport and decoding failures. An HTTP error status comes back as a response with `JSON200` nil: check `StatusCode()` and `Body`, and on 429 read `Headers429.RetryAfter`.

## WebSocket

```go
import (
	"crypto/rand"

	"github.com/psyb0t/gen-asyncapi/asyncapirt/gorillaws"
	"github.com/psyb0t/go-etoro/ws"
)

type handler struct {
	etorows.UnimplementedHandler
}

func (handler) HandleInstrumentRateMessage(
	ctx context.Context,
	envelope etorows.InstrumentRateEnvelope,
) error {
	for _, item := range envelope.Messages {
		rate, err := item.ContentValue()
		if err != nil {
			return err
		}

		_ = rate.Ask // *string, rates arrive as strings such as "1.25"
	}

	return nil
}

conn, err := gorillaws.Dial(ctx, etorows.ServerEtoroURL)
if err != nil {
	return err
}

client := etorows.NewClient(conn)
defer client.Close()

err = client.Authenticate(ctx, etorows.AuthenticateEnvelope{
	ID:        rand.Text(),
	Operation: "Authenticate",
	Data: etorows.AuthenticateData{
		APIKey:  os.Getenv("ETORO_API_KEY"),
		UserKey: os.Getenv("ETORO_USER_KEY"),
	},
})
if err != nil {
	return err
}

err = client.Subscribe(ctx, etorows.SubscribeEnvelope{
	ID:        rand.Text(),
	Operation: "Subscribe",
	Data: etorows.SubscribeData{
		Topics: []string{etorows.InstrumentRatesAddress("1001")},
	},
})
if err != nil {
	return err
}

return client.Run(ctx, handler{}) // blocks until ctx ends or the read fails
```

Embed `etorows.UnimplementedHandler` and override only the `Handle...` methods you need. A frame that matches no listed message goes to `HandleUnknownMessage` with an error that wraps `asyncapirt.ErrUnknownMessage`; the embedded default logs a warning and keeps reading, and returning an error there stops `Run`.
