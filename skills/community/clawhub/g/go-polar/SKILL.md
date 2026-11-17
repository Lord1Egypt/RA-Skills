---
name: go-polar
description: Unofficial Go client for the Polar API, generated with oapi-codegen from Polar's published OpenAPI document. Package polar (github.com/psyb0t/go-polar) provides typed REST methods for products, customers, subscriptions, checkouts, orders, payments, benefits, usage events, meters, refunds and webhook management. Use when Go code needs the Polar API or already imports go-polar.
license: MIT
homepage: https://github.com/psyb0t/go-polar
user-invocable: true
metadata:
  openclaw:
    emoji: "❄️"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. Runtime requests use HTTPS to api.polar.sh or sandbox-api.polar.sh."
---

# go-polar

Unofficial, typed Go client for the Polar API, in package `polar` at the module root.

For install, operation examples, pagination and response fields, see [references/setup.md](references/setup.md).

## Security & safety

- Read a bearer access token from `POLAR_ACCESS_TOKEN`. Never hardcode, commit or log it, and never print a request with its `Authorization` header.
- Use `https://api.polar.sh` for production or `https://sandbox-api.polar.sh` for sandbox. Select the environment the user requested.
- Create, update, delete, refund and revoke operations change account data. Call them only when the user requested that action.
- Use the token type and scopes the operation requires. Customer portal and member operations use their corresponding session tokens.

## When to use

- Go code needs Polar products, customers, subscriptions, orders, checkouts, benefits or usage billing.
- Go code needs to change Polar account data at the user's request.
- The project already imports `github.com/psyb0t/go-polar`.

## When NOT to use

- The code is not Go. This module ships only a Go package.
- You need a client maintained by Polar. This one is unofficial and not affiliated with Polar.
- You want to change the generated client itself. See `AGENTS.md` in the repo.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-polar`, from inside your module:

```bash
go doc github.com/psyb0t/go-polar ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-polar ProductsListParams            # one method, params type or model
go doc -all github.com/psyb0t/go-polar                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-polar.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status.

## Usage

Create a client with `polar.NewClientWithResponses` and a `polar.WithRequestEditorFn` option that sets `Authorization` to `Bearer ` followed by the access token. Use the host URL without a `/v1` suffix.

`ProductsListWithResponse(ctx, &polar.ProductsListParams{})` lists products. `CustomersListWithResponse(ctx, &polar.CustomersListParams{})` lists customers. `CustomersCreateWithResponse` accepts a generated customer-create union; construct a branch using the generated `FromCustomerIndividualCreate` or `FromCustomerTeamCreate` helper. Decode a customer union with `AsCustomerIndividual` or `AsCustomerTeam`.

The Go error return covers transport and decoding failures. Inspect `StatusCode()` and the matching success field, such as `JSON200` or `JSON201`, before using a response. Unsupported status bodies remain available in `Body`.

Nullable fields can be pointers; check for nil before dereferencing. Number fields use `float64`; integer minor-unit amounts remain integers. Scalar-or-array query filters take slices; use one element for a single value. List methods do not paginate automatically. Continue with `Page` until the response's `Pagination.MaxPage` is reached.
