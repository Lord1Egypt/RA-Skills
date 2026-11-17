---
name: go-revolut-business
description: Unofficial Go client for the Revolut Business REST API, generated with oapi-codegen. Package revolut (github.com/psyb0t/go-revolut-business) has revolut.NewClientWithResponses, which returns a client with one typed method per endpoint (accounts, transactions, counterparties, payments, transfers and more). Auth is a bearer access token set through revolut.WithRequestEditorFn, and responses decode into JSON200, JSON201 and JSONDefault fields. Use when Go code needs to call the Revolut Business API or already imports go-revolut-business.
license: MIT
homepage: https://github.com/psyb0t/go-revolut-business
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
  network: "HTTPS to the Revolut Business API at b2b.revolut.com or sandbox-b2b.revolut.com, and `go get` to your Go module proxy."
---

# go-revolut-business

Typed Go client for the Revolut Business API. Every endpoint in Revolut's OpenAPI document is a method on `ClientWithResponses`.

For install, auth details, environments and more operations, see [references/setup.md](references/setup.md).

## Security & safety

- Read the access token from an environment variable such as `REVOLUT_ACCESS_TOKEN`. Never hardcode it, commit it or log it, and never print request headers.
- Requests go only to the base URL you pass: `https://b2b.revolut.com/api/1.0` or `https://sandbox-b2b.revolut.com/api/1.0`. Prefer the sandbox while writing code.
- Payment, transfer, exchange and delete endpoints move money or remove data. Call them only when the user asked for that action.

## When to use

- Go code needs to read Revolut Business accounts, balances, transactions or counterparties, or create payments and transfers.
- The project already imports `github.com/psyb0t/go-revolut-business`.

## When NOT to use

- You need the OAuth2 token flow (JWT client assertion, `/auth/token`). This module does not implement it; get a token some other way and pass it in.
- You need Revolut Merchant or Open Banking APIs. This client covers only the Business API.
- The code is not Go.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-revolut-business`, from inside your module:

```bash
go doc github.com/psyb0t/go-revolut-business ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-revolut-business GetTransactionsParams         # one method, params type or model
go doc -all github.com/psyb0t/go-revolut-business                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-revolut-business.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. The package name is `revolut` while the module path ends in `go-revolut-business`, so import it as `revolut "github.com/psyb0t/go-revolut-business"`. Most operations declare only a `default` error response, so errors decode into `JSONDefault`.

## Usage

```go
import (
	"context"
	"fmt"
	"net/http"
	"os"

	revolut "github.com/psyb0t/go-revolut-business"
)

auth := revolut.WithRequestEditorFn(
	func(_ context.Context, req *http.Request) error {
		req.Header.Set(
			"Authorization",
			"Bearer "+os.Getenv("REVOLUT_ACCESS_TOKEN"),
		)

		return nil
	},
)

client, err := revolut.NewClientWithResponses(
	"https://sandbox-b2b.revolut.com/api/1.0",
	auth,
)
if err != nil {
	return err
}

res, err := client.GetAccountsWithResponse(ctx)
if err != nil {
	return err // transport failure
}

if res.JSON200 == nil {
	// non-2xx: res.StatusCode(), and res.JSONDefault has Code and Message
	return fmt.Errorf("revolut: %d", res.StatusCode())
}

for _, account := range *res.JSON200 {
	fmt.Println(account.Id, account.Currency, account.Balance)
}
```

Listing transactions for one account:

```go
count := 50

txs, err := client.GetTransactionsWithResponse(
	ctx,
	&revolut.GetTransactionsParams{Account: &accountID, Count: &count},
)
if err != nil {
	return err
}

if txs.JSON200 != nil {
	for _, tx := range *txs.JSON200 {
		fmt.Println(tx.Id, tx.Type, tx.State, tx.CreatedAt)
	}
}
```

`accountID` is an `openapi_types.UUID` (a `github.com/google/uuid` UUID), as in `account.Id`.

A method returns an error only when the request could not be sent or the body could not be decoded. An API error is a normal response: check `StatusCode()` and read `JSONDefault`.
