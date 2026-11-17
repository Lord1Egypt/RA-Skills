---
name: go-deribit
description: Writes Go code with go-deribit, an unofficial client for Deribit crypto options and futures generated from Deribit's public specs. Root package `deribit` (`github.com/psyb0t/go-deribit`) covers all 186 REST paths for instruments, market data, accounts, positions, orders, transfers and account administration. Package `deribitws` (`/ws`) covers all 43 JSON-RPC subscription channels for order books, tickers, trades and account updates. Use when Go code needs Deribit REST calls or WebSocket subscriptions, or already imports go-deribit.
license: MIT
homepage: https://github.com/psyb0t/go-deribit
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
  network: "`go get` fetches the module from the configured Go module proxy. At runtime the code sends HTTPS requests or WSS frames to test.deribit.com, www.deribit.com or deribit.com. Private calls send account credentials or tokens and account instructions."
---

# go-deribit

Unofficial, typed Go clients for Deribit: REST in the root package `deribit`, WebSocket subscriptions in `deribitws`.

For installation, environments, generated methods, response fields and WebSocket limits, see [references/setup.md](references/setup.md).

## Security & safety

- Private REST requests use an OAuth bearer token. Read it from `DERIBIT_ACCESS_TOKEN`; public market data needs no token. Never hardcode, commit or log tokens, client secrets or authentication request URLs.
- Use testnet while developing. Select the production host only when the user requests it; credentials must match the environment.
- Order placement and cancellation, transfers, withdrawals and account or API key changes affect the account. Perform them only when the user requested that exact action.
- Private WebSocket subscriptions and raw market-data channels require authentication on the same connection. The generated subscription package does not implement token renewal or authentication requests.

## When to use

- Go code needs Deribit instruments, order books, tickers, trades or other market data.
- Go code needs account summaries, positions, orders, transfers or account administration.
- Go code needs Deribit subscription notifications over WebSocket.
- The project already imports `github.com/psyb0t/go-deribit` or `/ws`.

## When NOT to use

- The code is not Go. This module ships Go packages.
- A provider-maintained client is required. This client is unofficial and unaffiliated with Deribit.
- The task changes generated code. Read the repository's `AGENTS.md` instead.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the specs has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-deribit`, from inside your module:

```bash
go doc github.com/psyb0t/go-deribit ClientWithResponsesInterface  # every REST endpoint method
go doc github.com/psyb0t/go-deribit PublicGetInstrumentsParams    # one method, params type or model
go doc -all github.com/psyb0t/go-deribit                          # the whole REST package
go doc github.com/psyb0t/go-deribit/ws Handler                    # every subscription notification handler
go doc github.com/psyb0t/go-deribit/ws Client                     # the SendSubscribe... methods and Run
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-deribit.

REST operation IDs are assigned from the complete path, so `/public/get_time` becomes `PublicGetTime`; every operation is a GET with query parameters. `<OperationId>WithResponse` takes the context, then `*<OperationId>Params` when the operation has query parameters. Parsed response types can carry a numeric suffix from name collision resolution (`PublicGetTimeResponse3`). The `JSON200` field (or `JSON401` where the spec declares it) holds the decoded body for that status; it is nil for any other status.

## Usage

Use `deribit.NewClientWithResponses("https://test.deribit.com/api/v2", options...)`. Each REST operation has a raw method and a parsed `...WithResponse` method. `PublicGetTimeWithResponse(ctx)` reads server time without credentials. Attach `deribit.WithRequestEditorFn` to set `Authorization` to `"Bearer "+token` for private calls.

Check the returned error, HTTP status and decoded response before using fields. A nil Go error does not establish API success. Read the JSON-RPC result or error envelope as well as the HTTP response. The generated client does not retry, refresh tokens or enforce permissions.

For WebSockets, construct `deribitws.NewClient` with a transport. Embed `deribitws.UnimplementedHandler` and override the handlers you need. Handle authentication and command replies on that connection before starting the subscription receive loop, or in the unknown-message handler.
