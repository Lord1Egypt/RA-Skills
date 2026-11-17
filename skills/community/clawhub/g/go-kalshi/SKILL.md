---
name: go-kalshi
description: Unofficial Go client for Kalshi, generated from the API specs Kalshi publishes. The root package `kalshi` (`github.com/psyb0t/go-kalshi`) is an oapi-codegen REST client for the Trade API at `https://external-api.kalshi.com/trade-api/v2` with a typed `...WithResponse` method per endpoint (markets, events, series, orderbooks, trades, balance, positions, fills, orders, RFQs and quotes). `kalshiws` (`/ws`) streams market data (orderbook, ticker, trade, fill, lifecycle, RFQ and index pushes) through a typed `Handler`, `kalshiperpsws` (`/perpsws`) does the same for the perps channels, and `kalshiauth` (`/auth`) signs REST requests and WebSocket handshakes with an RSA-PSS or Ed25519 API key. Use when Go code needs to read Kalshi markets, manage a Kalshi account or stream Kalshi data, or already imports go-kalshi.
license: MIT
homepage: https://github.com/psyb0t/go-kalshi
user-invocable: true
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files; your code supplies the private key bytes."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the code you write talks HTTPS and WSS to Kalshi's hosts only: external-api.kalshi.com, external-api-ws.kalshi.com and external-api-margin-ws.kalshi.com, or their demo.kalshi.co counterparts."
---

# go-kalshi

Unofficial, typed Go clients for Kalshi: REST in the root package `kalshi`, WebSockets in `kalshiws` and `kalshiperpsws`, request signing in `kalshiauth`.

For install, environments, response fields, the handler list and errors, see [references/setup.md](references/setup.md).

## Security & safety

- Kalshi signs each request with your private key. Read the key ID and the PEM key from environment variables (`KALSHI_API_KEY_ID`, `KALSHI_PRIVATE_KEY`) or a file path the user gives. Never hardcode, commit or log them, and never print signed request headers.
- Requests go only to Kalshi's API hosts. Do not attach the signer to a client for another host.
- Placing, cancelling or batch-cancelling orders, accepting quotes, transfers between subaccounts and API key changes act on a real account. Call them only when the user asked for that exact action, and prefer the demo environment while developing. Public market data needs no signer.

## When to use

- Go code needs Kalshi markets, events, series, orderbooks or trades.
- Go code needs the user's Kalshi balance, positions, fills or orders.
- Go code needs a live stream of Kalshi tickers, orderbook deltas, trades or the user's fills and orders.
- The project already imports `github.com/psyb0t/go-kalshi` or one of its subpackages.

## When NOT to use

- The code is not Go. This module ships only Go packages.
- You need a client maintained by Kalshi. This one is unofficial and not affiliated with Kalshi.
- You want to change the generated clients themselves. See `AGENTS.md` in the repo.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the specs has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-kalshi`, from inside your module:

```bash
go doc github.com/psyb0t/go-kalshi ClientWithResponsesInterface  # every REST endpoint method
go doc github.com/psyb0t/go-kalshi GetMarketsParams              # one method, params type or model
go doc -all github.com/psyb0t/go-kalshi                          # the whole REST package
go doc github.com/psyb0t/go-kalshi/ws Handler                    # every market data push handler
go doc github.com/psyb0t/go-kalshi/ws Client                     # the Send... commands
go doc github.com/psyb0t/go-kalshi/perpsws Handler               # every perps push handler
go doc github.com/psyb0t/go-kalshi/perpsws Client                # the perps Send... commands
go doc github.com/psyb0t/go-kalshi/auth Signer                   # request and handshake signing
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-kalshi.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. Response wrappers whose names clash with a schema get a `2` suffix (`GetBalanceWithResponse` returns `*GetBalanceResponse2`).

## REST

```go
import (
	"context"
	"fmt"
	"os"

	"github.com/psyb0t/go-kalshi"
	"github.com/psyb0t/go-kalshi/auth"
)

key, err := kalshiauth.ParsePrivateKeyPEM(
	[]byte(os.Getenv("KALSHI_PRIVATE_KEY")),
)
if err != nil {
	return err
}

signer, err := kalshiauth.NewSigner(os.Getenv("KALSHI_API_KEY_ID"), key)
if err != nil {
	return err
}

client, err := kalshi.NewClientWithResponses(
	"https://external-api.kalshi.com/trade-api/v2",
	kalshi.WithRequestEditorFn(signer.RequestEditor),
)
if err != nil {
	return err
}

balance, err := client.GetBalanceWithResponse(ctx, &kalshi.GetBalanceParams{})
if err != nil {
	return err // transport failure
}

if balance.JSON200 == nil {
	return fmt.Errorf("balance: %s", balance.Status())
}

cents := balance.JSON200.Balance // int64, in cents

status := kalshi.GetMarketsParamsStatusOpen
limit := kalshi.MarketLimitQuery(100)

markets, err := client.GetMarketsWithResponse(ctx, &kalshi.GetMarketsParams{
	Status: &status,
	Limit:  &limit,
})
if err != nil {
	return err
}

if markets.JSON200 != nil {
	for _, market := range markets.JSON200.Markets {
		fmt.Println(market.Ticker, market.YesBidDollars, market.YesAskDollars)
	}

	next := markets.JSON200.Cursor // pass as Cursor for the next page
	_ = next
}
```

The error return covers only transport and decoding failures. An API error comes back as a response with `JSON200` nil and, for declared statuses, `JSON401` or `JSON500` set to an `ErrorResponse` (`Code`, `Message`, `Details`).

## WebSocket

```go
import (
	"net/http"

	"github.com/psyb0t/gen-asyncapi/asyncapirt/gorillaws"
	"github.com/psyb0t/go-kalshi/ws"
)

type handler struct {
	kalshiws.UnimplementedHandler
}

func (handler) HandleTicker(
	ctx context.Context,
	ticker kalshiws.TickerPayload,
) error {
	fmt.Println(ticker.Msg.MarketTicker, ticker.Msg.PriceDollars)

	return nil
}

header, err := signer.Headers(http.MethodGet, kalshiauth.WebSocketPath)
if err != nil {
	return err
}

options := make([]gorillaws.Option, 0, len(header))
for name := range header {
	options = append(options, gorillaws.WithHeader(name, header.Get(name)))
}

conn, err := gorillaws.Dial(ctx, kalshiws.ServerProductionURL, options...)
if err != nil {
	return err
}

client := kalshiws.NewClient(conn)
defer client.Close()

err = client.SendSubscribe(ctx, kalshiws.SubscribeCommandPayload{
	ID: 1,
	Params: kalshiws.SubscribeCommandPayloadParams{
		Channels: []kalshiws.SubscribeCommandPayloadParamsChannelsItem{
			kalshiws.SubscribeCommandPayloadParamsChannelsItemTicker,
		},
		MarketTickers: []kalshiws.MarketTicker{"EXAMPLE-TICKER"},
	},
})
if err != nil {
	return err
}

return client.Run(ctx, handler{}) // blocks until ctx ends or a read fails
```

Embed `kalshiws.UnimplementedHandler` and override only the `Handle...` methods you need. `kalshiperpsws` works the same way with its own `ServerProductionURL`; sign its handshake with the path of that URL, `/trade-api/ws/v2/margin`.
