---
name: go-twelvedata
description: "Unofficial Go client for the Twelve Data market data API, generated with oapi-codegen. Package twelvedata (github.com/psyb0t/go-twelvedata) provides typed REST methods for prices, quotes, time series, technical indicators, fundamentals, instrument metadata and batch queries. Use when Go code needs Twelve Data market data or already imports go-twelvedata."
homepage: https://github.com/psyb0t/go-twelvedata
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
  network: "`go get` fetches the module from your Go module proxy. At runtime the code you write talks HTTPS to api.twelvedata.com."
---

# go-twelvedata

Unofficial, typed Go client for the Twelve Data API, in package `twelvedata` at the module root.

Read [references/setup.md](references/setup.md) before writing calls. It covers installation, authentication, representative operations, responses and request limits.

## Security & safety

- Read the API key from `TWELVEDATA_API_KEY`. Set `Authorization: apikey <key>` through `WithRequestEditorFn`. Never hardcode, commit or log the key or an authenticated request.
- Use `https://api.twelvedata.com`. The spec also permits an `apikey` query parameter, which can expose the key in URL logs.
- Calls consume API credits. Respect the user's plan, data permissions and request budget.

## When to use

- Go code needs prices, quotes, historical candles, technical indicators, fundamentals or instrument lists from Twelve Data.
- Go code needs to combine market data requests with the batch endpoint.
- The project already imports `github.com/psyb0t/go-twelvedata`.

## When NOT to use

- The code is not Go. This module ships only a Go package.
- You need a client maintained by Twelve Data. This one is unofficial and not affiliated with Twelve Data.
- You want to change the generated client itself. Read `AGENTS.md` in the repository.

## Finding endpoints and types

The example below covers one call. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-twelvedata`, from inside your module:

```bash
go doc github.com/psyb0t/go-twelvedata ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-twelvedata GetTimeSeriesParams           # one method, params type or model
go doc -all github.com/psyb0t/go-twelvedata                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-twelvedata.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. Parameter fields carry the provider's `x-go-name` names, so `outputsize` is `PageSize` and `dp` is `DecimalPlaces`, and the batch endpoint `POST /batch` is `AdvancedWithResponse`.

## Usage

The README example also lives in `example_test.go`:

```go
package main

import (
	"context"
	"net/http"
	"os"

	"github.com/psyb0t/go-twelvedata"
)

func main() {
	auth := twelvedata.WithRequestEditorFn(
		func(_ context.Context, req *http.Request) error {
			req.Header.Set(
				"Authorization",
				"apikey "+os.Getenv("TWELVEDATA_API_KEY"),
			)

			return nil
		},
	)

	client, err := twelvedata.NewClientWithResponses(
		"https://api.twelvedata.com",
		auth,
	)
	if err != nil {
		panic(err)
	}

	const symbol = "SYMBOL_X"

	res, err := client.GetPriceWithResponse(
		context.Background(),
		&twelvedata.GetPriceParams{Symbol: new(symbol)},
	)
	if err != nil {
		panic(err)
	}

	_ = res.JSON200
}
```

Replace `SYMBOL_X` with the requested instrument. Check `StatusCode()` and the appropriate decoded status field before using a response. A nil Go error covers transport and decoding, not HTTP success. `JSON200` can be nil.

The `Price` response field is a string. Number schemas map to `float64`; many market price fields remain strings as defined by the provider.

Before finishing a change, compile the calling code and test its request and response handling against a local HTTP server. Tests must not spend provider credits.
