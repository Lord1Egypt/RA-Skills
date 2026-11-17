---
name: go-ibkr
description: Unofficial Go client for the Interactive Brokers Web API (Client Portal API v1), generated with oapi-codegen from the OpenAPI document Interactive Brokers publishes. Package `ibkr` (`github.com/psyb0t/go-ibkr`) has a typed `...WithResponse` method for each of the spec's endpoints, covering session status and keepalive, accounts, portfolio positions and summary, contract search and details, market data snapshots, order submission, status, modification and cancellation, and model portfolios. It works through a local Client Portal Gateway or against `https://api.ibkr.com` with an OAuth token. Use when Go code needs to read an Interactive Brokers account, look up contracts or market data, or place orders, or already imports go-ibkr.
license: MIT
homepage: https://github.com/psyb0t/go-ibkr
user-invocable: true
metadata:
  openclaw:
    emoji: "🏦"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the code you write talks HTTPS to the user's own Client Portal Gateway (by default https://localhost:5000) or to api.ibkr.com only."
---

# go-ibkr

Unofficial, typed Go client for the Interactive Brokers Web API, in package `ibkr` at the module root.

For install, both auth setups, operation lookup and response handling, see [references/setup.md](references/setup.md).

## Security & safety

- The client implements no login. With the Client Portal Gateway the user logs in in a browser and the gateway holds the session, so the code needs no credentials. With OAuth, read the access token from an environment variable or the user's own token code; never hardcode, commit or log it.
- Requests go only to the user's gateway or to `https://api.ibkr.com`. Skip TLS verification only for a gateway on the user's own machine, which serves a self-signed certificate. Never skip it for any other host.
- `SubmitNewOrder`, `ModifyOpenOrder`, `CancelOpenOrder`, `ConfirmOrderReply`, the model order endpoints and `Logout` act on a real brokerage account. Call them only when the user asked for that exact action, and prefer a paper trading login while developing.

## When to use

- Go code needs Interactive Brokers accounts, positions, portfolio summary, contract details or market data snapshots.
- Go code needs to place, modify or cancel Interactive Brokers orders, at the user's request.
- The project already imports `github.com/psyb0t/go-ibkr`.

## When NOT to use

- The code is not Go. This module ships only a Go package.
- You need the TWS socket API. This client covers the Web API only.
- You need a client maintained by Interactive Brokers. This one is unofficial and not affiliated with Interactive Brokers.
- You want to change the generated client itself. See `AGENTS.md` in the repo.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-ibkr`, from inside your module:

```bash
go doc github.com/psyb0t/go-ibkr ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-ibkr GetPaginatedPositionsParams   # one method, params type or model
go doc -all github.com/psyb0t/go-ibkr                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-ibkr.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. Each method's doc comment names its path (`Corresponds with GET /v1/api/iserver/accounts`), so filter the interface listing by path to find one, and operation IDs the spec repeats get a numeric suffix (`GetTradingSchedule2`).

## Usage

The spec paths carry their full prefix (`/v1/api/...`), so the base URL is only the scheme and host.

```go
import (
	"context"
	"crypto/tls"
	"errors"
	"fmt"
	"net/http"

	"github.com/psyb0t/go-ibkr"
)

// A Client Portal Gateway on this machine serves a self-signed certificate.
httpClient := &http.Client{
	Transport: &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	},
}

client, err := ibkr.NewClientWithResponses(
	"https://localhost:5000",
	ibkr.WithHTTPClient(httpClient),
)
if err != nil {
	return err
}

status, err := client.GetBrokerageStatusWithResponse(ctx)
if err != nil {
	return err // transport failure
}

if status.JSON200 == nil || status.JSON200.Authenticated == nil ||
	!*status.JSON200.Authenticated {
	return errors.New("log in to the gateway at https://localhost:5000")
}

accounts, err := client.GetBrokerageAccountsWithResponse(ctx)
if err != nil {
	return err
}

if accounts.JSON200 == nil || accounts.JSON200.Accounts == nil {
	return fmt.Errorf("accounts: %s", accounts.Status())
}

accountID := (*accounts.JSON200.Accounts)[0]

positions, err := client.GetPaginatedPositionsWithResponse(
	ctx,
	accountID,
	0, // page
	&ibkr.GetPaginatedPositionsParams{},
)
if err != nil {
	return err
}

if positions.JSON200 != nil {
	for _, position := range *positions.JSON200 {
		fmt.Println(*position.Conid, *position.ContractDesc)
	}
}
```

Keep a gateway session alive by calling `GetSessionTokenWithResponse` (`POST /v1/api/tickle`) about once a minute.

With OAuth, use `https://api.ibkr.com` as the base URL and add the token in a request editor:

```go
auth := ibkr.WithRequestEditorFn(
	func(_ context.Context, req *http.Request) error {
		req.Header.Set("Authorization", "Bearer "+accessToken)

		return nil
	},
)

client, err := ibkr.NewClientWithResponses("https://api.ibkr.com", auth)
```

Most response fields are pointers; check for nil before dereferencing. The error return covers only transport and decoding failures. An API error comes back with `JSON200` nil: check `StatusCode()` and `Body`.
