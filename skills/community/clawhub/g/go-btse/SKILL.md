---
name: go-btse
description: Writes Go code with go-btse (github.com/psyb0t/go-btse), an unofficial BTSE client generated from its public OpenAPI and AsyncAPI specifications. REST packages btse (spot), futures, markets, wallet, earn and otc cover spot and futures orders, account fees, positions, public markets, wallets, transfers, withdrawals, earn products and OTC quotes; auth signs private requests with HMAC-SHA384; ws/spot, ws/futures and ws/otc cover WebSocket messages. Use when Go code needs BTSE API access or already imports github.com/psyb0t/go-btse.
license: MIT
homepage: https://github.com/psyb0t/go-btse
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to Go source in the current project. The client reads and writes no files."
  shell: "Uses the Go toolchain to add and compile the dependency."
  network: "Module installation fetches dependencies from the Go module proxy. Runtime requests send API parameters and authentication headers to the selected BTSE HTTPS or WSS host. Tests use local servers and fixtures."
---

# go-btse

Unofficial typed Go client for BTSE. The root `btse` package covers spot REST operations. Other products have separate packages to keep their schemas and operation names distinct.

See [references/setup.md](references/setup.md) for installation, product base URLs, responses and generation details.

## Security & safety

- Read private API credentials from `BTSE_API_KEY` and `BTSE_API_SECRET`. Never hardcode, commit or log them, or print signed request headers. Public market data does not require credentials.
- Default to `https://testapi.btse.io`. Production requests use `https://api.btse.com`. Select the service prefix from the table in the setup reference, and use credentials for that environment.
- Orders, cancellations, position changes, transfers, withdrawals, earn deposits and redemptions, and accepted OTC quotes change the account. Call them only for the exact action the user requested. Use production only when requested.

## When to use

- Go code needs BTSE account data, public market data or WebSocket messages.
- Go code needs to place orders or use BTSE wallet, earn or OTC operations at the user's request.
- The project already imports `github.com/psyb0t/go-btse` or one of its product packages.

## When NOT to use

- The code is not Go.
- The user needs an SDK maintained by BTSE. This client is unofficial.
- The task changes the generated client. Read the repository's `AGENTS.md` for that workflow.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the specs has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-btse`, from inside your module:

```bash
go doc github.com/psyb0t/go-btse ClientWithResponsesInterface          # every spot endpoint method
go doc github.com/psyb0t/go-btse GetAccountFeesParams                  # one method, params type or model
go doc -all github.com/psyb0t/go-btse                                  # the whole spot package
go doc github.com/psyb0t/go-btse/futures ClientWithResponsesInterface  # same for markets, wallet, earn, otc
go doc github.com/psyb0t/go-btse/auth Signer                           # request signing
go doc github.com/psyb0t/go-btse/ws HeartbeatTransport                 # spot and futures heartbeat adapter
go doc github.com/psyb0t/go-btse/ws/spot Handler                       # every received message handler
go doc github.com/psyb0t/go-btse/ws/spot Client                        # Authenticate, Subscribe, SendPing, Run
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-btse. The `ws/futures` and `ws/otc` packages have the same `Handler` and `Client` entry points; the OTC client's send methods are `Authenticate` and the `SubscribeQuote...` methods.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status.

## Usage

Construct a signer with `btseauth.NewSigner(key, secret)`. Handle its error, then pass `btse.WithRequestEditorFn(signer.RequestEditor)` to `btse.NewClientWithResponses("https://testapi.btse.io/spot", opts...)`. For another product, use that package's constructor and `WithRequestEditorFn` option with its base URL.

For example, `client.GetAccountFeesWithResponse(ctx, &btse.GetAccountFeesParams{})` fetches spot maker and taker fees. The complete compiling example is `example_test.go`, also shown in the README.

The signer sets `request-api`, an increasing millisecond `request-nonce`, and the lowercase hexadecimal HMAC-SHA384 `request-sign`. Register it after editors that change the URL or body. Share one signer per API key. It signs the API path without the query, strips `/spot` or `/futures` only before `/api/`, and preserves the exact body bytes.

The Go error covers transport and decoding failures. Check `StatusCode()` and the expected response field before dereferencing it. A non-2xx API result can return a nil Go error. Most generated fields are pointers. JSON number fields use `float64`; fields declared as strings stay strings.

Method names come from each product's operation IDs. `CreateOrderWithResponse` exists in both the root spot package and the `futures` package, with different request types. Keep those types in their owning package.
