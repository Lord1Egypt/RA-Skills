# heyAura portfolio API reference

## Contents

- [Endpoint](#endpoint)
- [x402 payment](#x402-payment)
- [Response shape](#response-shape)

## Endpoint

Use only:

```text
GET https://aura.adex.network/api/x402/portfolio/balances?address=<wallet-or-ens>
```

Live machine-readable specification:

- x402 OpenAPI JSON: `https://aura.adex.network/.well-known/openapi.json`

## x402 payment

The endpoint currently returns an x402 v2 challenge in the Base64-encoded `PAYMENT-REQUIRED` response header. Always inspect it live because price and settlement details can change.

The current challenge advertises the optional `payment-identifier` extension. Generate one identifier per logical paid request and append it only when advertised. For a user-authorized retry of that same logical request, reuse the identifier while allowing the x402 client to create a fresh signed payment payload. Never replay an old signed payment header.

heyAura's cache behavior was verified on 2026-08-20: a second request with the same identifier and request fingerprint returned the same response without a second settlement header or transaction. The identifier lifetime is server-configured and is not declared by the challenge. Do not treat `maxTimeoutSeconds` or an HTTP cache header as a guaranteed idempotency TTL.

The OpenAPI JSON lists the `402` response but does not currently model the `PAYMENT-REQUIRED` header schema. Decode the live response header according to x402 v2 rather than relying on generated OpenAPI response types for the challenge.

The scheme is `exact`. Select payment terms from the fresh challenge printed by `inspect` and check them against the user's authorization; do not assume a fixed price or network.

## Response shape

Top-level object:

| Field | Type | Notes |
|---|---|---|
| `address` | string | Queried wallet |
| `portfolio` | array | One entry per network |
| `cached` | boolean, optional | Whether heyAura served cached data |
| `version` | string | API response version |

Each network entry contains:

- `network`: `name`, `chainId`, `platformId`, `explorerUrl`, `iconUrls[]`.
- `tokens[]`: `address`, `symbol`, `decimals`, `balance`, `balanceRaw`, `balanceUSD`.
- `positionTokens[]` (optional): token fields plus `type`, `providerName`, and optional provider metadata, `chainId`, `action`, `apy`, and `healthRate`.

`positionTokens[].type` is one of `liquidity`, `collateral`, `borrow`, or `reward`.
