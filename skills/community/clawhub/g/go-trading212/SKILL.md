---
name: go-trading212
description: "Unofficial Go client for the Trading 212 Public API, generated with oapi-codegen from the OpenAPI document Trading 212 publishes. Package `trading212` (`github.com/psyb0t/go-trading212`) has a typed `...WithResponse` method for every endpoint: account summary, positions, open orders, limit, market, stop and stop-limit orders, order, dividend and transaction history, CSV report exports, exchange and instrument metadata, and pies. Prices and amounts are `float64`. Use when Go code needs to read a Trading 212 account or place Trading 212 orders, or already imports go-trading212."
homepage: https://github.com/psyb0t/go-trading212
license: MIT
user-invocable: true
metadata:
  openclaw:
    emoji: "💹"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the code you write talks HTTPS to demo.trading212.com or live.trading212.com only."
---

# go-trading212

Unofficial, typed Go client for the Trading 212 Public API, in package `trading212` at the module root.

For install, the full operation list, pagination and response fields, see [references/setup.md](references/setup.md).

## Security & safety

- Trading 212 uses HTTP Basic auth: the API key is the username and the API secret the password. Read both from environment variables (`TRADING212_API_KEY`, `TRADING212_API_SECRET`). Never hardcode, commit or log them, and never print a request with its `Authorization` header.
- Requests go only to `https://demo.trading212.com` (paper trading) or `https://live.trading212.com` (real money). A key works only on the environment it was made for. Default to demo.
- Placing or cancelling orders and creating, updating, duplicating or deleting pies act on the account. Call them only when the user asked for that exact action, and use the live host only when the user said so.

## When to use

- Go code needs a Trading 212 account summary, positions, open orders or history.
- Go code needs to place or cancel Trading 212 orders or manage pies, at the user's request.
- The project already imports `github.com/psyb0t/go-trading212`.

## When NOT to use

- The code is not Go. This module ships only a Go package.
- You need a client maintained by Trading 212. This one is unofficial and not affiliated with Trading 212.
- You want to change the generated client itself. See `AGENTS.md` in the repo.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-trading212`, from inside your module:

```bash
go doc github.com/psyb0t/go-trading212 ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-trading212 GetPositionsParams            # one method, params type or model
go doc -all github.com/psyb0t/go-trading212                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-trading212.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. Some operation IDs are generic or numbered; the note at the end of this file maps them.

## Usage

```go
import (
	"context"
	"fmt"
	"net/http"
	"os"

	"github.com/psyb0t/go-trading212"
)

auth := trading212.WithRequestEditorFn(
	func(_ context.Context, req *http.Request) error {
		req.SetBasicAuth(
			os.Getenv("TRADING212_API_KEY"),
			os.Getenv("TRADING212_API_SECRET"),
		)

		return nil
	},
)

client, err := trading212.NewClientWithResponses(
	"https://demo.trading212.com",
	auth,
)
if err != nil {
	return err
}

summary, err := client.GetAccountSummaryWithResponse(ctx)
if err != nil {
	return err // transport failure
}

if summary.JSON200 == nil {
	return fmt.Errorf("account summary: %s", summary.Status())
}

if total := summary.JSON200.TotalValue; total != nil { // *float64
	fmt.Println("account value:", *total)
}

positions, err := client.GetPositionsWithResponse(
	ctx,
	&trading212.GetPositionsParams{},
)
if err != nil {
	return err
}

if positions.JSON200 != nil {
	for _, position := range *positions.JSON200 {
		fmt.Println(*position.Instrument.Ticker, *position.Quantity)
	}
}
```

Most response fields are pointers; check for nil before dereferencing. The error return covers only transport and decoding failures. An API error (401, 403, 429 and so on) comes back with `JSON200` nil: check `StatusCode()` and `Body`.

Some method names come straight from the spec's operation IDs and are generic: `GetAll`, `Create`, `Update`, `Delete` and `GetDetailed` are the pie endpoints, `Orders1` is the order history, `PlaceStopOrder1` places a stop order and `PlaceStopOrder` a stop-limit order.
