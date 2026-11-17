# go-polar: setup and reference

This module is unofficial and not affiliated with Polar.

## Requirements

- Go 1.26.11 or newer, per the module's `go.mod`.
- A Polar organization access token, personal access token or OAuth access token with the operation's required scopes, exported as `POLAR_ACCESS_TOKEN`.

## Install

```bash
go get github.com/psyb0t/go-polar
```

## Environments

| Environment | Base URL |
|---|---|
| Production | `https://api.polar.sh` |
| Sandbox | `https://sandbox-api.polar.sh` |

Use the token for the selected environment. Paths include `/v1`, so do not append that prefix to the base URL.

## Auth

Set `req.Header.Set("Authorization", "Bearer "+token)` in a request editor registered with `polar.WithRequestEditorFn`. The generated client does not acquire or refresh tokens. Customer portal and member endpoints use corresponding session bearer tokens instead of an organization token.

## Client

- `polar.NewClientWithResponses(server, opts...)`. Options include `polar.WithRequestEditorFn`, `polar.WithHTTPClient` for a custom HTTP client and timeouts, and `polar.WithBaseURL`.
- Each operation has a raw client method, a parsed `...WithResponse` method and a `New...Request` constructor. Operations with a body also expose methods that take an `io.Reader`.

## Operations

| Method | Endpoint |
|---|---|
| `ProductsListWithResponse` | `GET /v1/products/` |
| `ProductsGetWithResponse` | `GET /v1/products/{id}` |
| `CustomersListWithResponse` | `GET /v1/customers/` |
| `CustomersGetWithResponse` | `GET /v1/customers/{id}` |
| `CustomersCreateWithResponse` | `POST /v1/customers/` |

The full generated client also covers subscriptions, checkouts, orders, payments, refunds, benefits, meters, usage events, files, discounts, customer sessions and webhook management. Consult `client_*.gen.go` for the operation's parameters, request types, scopes and response statuses.

`CustomerCreate` is a union. Construct an individual or team branch using `FromCustomerIndividualCreate` or `FromCustomerTeamCreate`. `Customer` responses have the discriminator `type`, with `individual` and `team` branches. Decode them using `AsCustomerIndividual` or `AsCustomerTeam`.

## Responses

| Field or method | Holds |
|---|---|
| `JSON200`, `JSON201` | The decoded body for that success status, nil otherwise |
| Other `JSON...` fields | Typed error bodies declared in the spec |
| `Body`, `StatusCode()`, `Status()`, `HTTPResponse` | The raw response |

Go errors report transport and decoding failures. HTTP failures can return a nil Go error; check the status. Nullable fields may be pointers. Number fields use `float64`, and integer amounts remain integers.

Responses with an empty schema, such as invoice generation, expose `*json.RawMessage` success fields. Decode those bytes into an application-specific type when the shape is known.

Customer `tax_id` response values are two-element arrays containing the tax ID and format. They generate as `*[]interface{}`; the client does not validate positional types or the format enum. Customer-create `tax_id` input values are strings.

## Pagination

List endpoints use `Page` and `Limit` parameters. Pages start at 1. The response has `Items` and `Pagination`, with `TotalCount` and `MaxPage`. Request successive pages until `MaxPage` is reached. The documented maximum page size for product and customer lists is 100.

## Rate limits

Handle HTTP 429 with bounded retries and backoff. The generated client does not retry or paginate automatically.
