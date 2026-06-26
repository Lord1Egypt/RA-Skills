# MPP Pay — Streaming Micropayments

MPP (Machine Payment Protocol) is used for streaming or metered APIs. Detection is described below, but **payment uses the same universal endpoint** as all protocols.

## Detection

An HTTP 402 response with a `WWW-Authenticate` header containing `Payment request=` indicates MPP:

```
WWW-Authenticate: Payment id="...", realm="...", method="tempo", intent="charge|session", request="<base64>"
```

The `method` field tells you the payment method (e.g. `tempo`). The `intent` tells you whether payment unlocks a single charge (`charge`) or a session (`session`).

## Multiple Methods

Some merchants offer multiple methods in the same header or body. For example:

```
body: { "methods": ["tempo", "stripe"] }
www-authenticate: Payment method="tempo" ..., Payment method="stripe" ...
```

The agent should identify which methods Mag3nt supports — `tempo` (chain 4217), `eip155:8453` (Base), or `solana:mainnet` — and ignore unsupported methods like `stripe` or `card`.

If payment fails on a multi-method endpoint, verify that the engine parsed the correct challenge by checking the error response. The `challenge` object in the error will show which method was attempted.

## Pay

MPP payments use the same `POST /api/pay` endpoint as x402. See `references/x402-pay.md` for the full API contract.

## Fulfillment

Read the merchant's challenge to understand how they expect payment proof. The credential from the pay response is your starting point — adapt based on what the merchant specified. For `intent="session"`, the credential may be reusable for multiple requests within the payment window. If the session expires, the merchant issues a new 402 challenge.

## Notes

- MPP is common for **streaming** or **metered** APIs (compute, search, inference)
- Single-method endpoints work reliably (e.g. Edgar Search via Locus)
- See `references/x402-pay.md` for the complete request/response schema
