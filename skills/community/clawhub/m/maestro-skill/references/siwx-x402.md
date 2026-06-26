# SIWX + x402 Reference

Use this file only after Maestro has already returned a live `402` challenge, or when you need the exact signing and header formats.

## Challenge Shape

Initial request:

- Send the real endpoint request with no auth or payment headers.

Typical `402` body:

```json
{
  "extensions": {
    "sign-in-with-x": {
      "domain": "api.gomaestro.org",
      "nonce": "uuid-v4",
      "statement": "Sign in to Maestro API Gateway",
      "issued_at": "2026-03-09T21:34:00Z",
      "expiration_time": "2026-03-09T21:39:00Z",
      "supported_chains": ["eip155:1", "eip155:8453"]
    }
  },
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:1",
      "asset": "0x...",
      "pay_to": "0x...",
      "price": "100000",
      "extra": {
        "name": "USDC",
        "version": "2",
        "min_price": "100000",
        "max_price": "50000000",
        "credits_per_token": "0.04"
      }
    }
  ]
}
```

The challenge defines how to authenticate and pay. It does not define the REST base URL. Keep taking the request URL from the docs operation page.

## SIWX Authentication

Build an EIP-4361 message and sign it with EIP-191 `personal_sign`.

Critical rules:

- `Chain ID` uses the full CAIP-2 value from `supported_chains`, for example `eip155:1`.
- `domain`, `statement`, `issued_at`, and `expiration_time` come from the live `402` challenge.
- `URI: https://api.gomaestro.org` is authentication metadata only. It is not the REST base URL.

Message template:

```text
api.gomaestro.org wants you to sign in with your Ethereum account:
0xYourWalletAddress

Sign in to Maestro API Gateway

URI: https://api.gomaestro.org
Version: 1
Chain ID: eip155:1
Nonce: <nonce from challenge>
Issued At: <issued_at from challenge>
Expiration Time: <expiration_time from challenge>
```

Header format:

```text
sign-in-with-x: base64({ "message": "<full message>", "signature": "0x..." })
```

Use standard base64 with `=` padding. Keep the header name lowercase.

Response handling:

- `200` means the request succeeded with existing credits.
- `402` plus `Authorization: Bearer <jwt>` means SIWX succeeded but credits are insufficient.
- `401` usually means the SIWX nonce expired or was replayed.

The JWT is typically valid for about one hour. Reuse it until Maestro asks for more credits or returns an auth failure.

## Credit Purchase

Choose the payment terms from the most recent `402` response.

- Pick one live `accepts[]` entry.
- Choose an amount inside `extra.min_price` and `extra.max_price`.
- Use the selected entry's `network`, `asset`, and `pay_to`.

Keep the signing flows separate:

| Flow | Signature method | Chain ID format |
|---|---|---|
| SIWX auth | EIP-191 `personal_sign` | CAIP-2, for example `eip155:1` |
| Credit purchase | EIP-712 typed data | numeric, for example `1` |

### EIP-712 Domain

Use:

- `verifyingContract = accepts[].asset`
- `chainId = numeric chain ID for the selected network`
- `name` and `version` from the token contract when possible

Do not assume a token symbol is the correct EIP-712 domain name.

Verified USDC values:

| Network | Asset | `name()` | `version()` |
|---|---|---|---|
| `eip155:1` | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` | `USD Coin` | `2` |
| `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | `USD Coin` | `2` |

### EIP-712 Types

```json
{
  "TransferWithAuthorization": [
    { "name": "from", "type": "address" },
    { "name": "to", "type": "address" },
    { "name": "value", "type": "uint256" },
    { "name": "validAfter", "type": "uint256" },
    { "name": "validBefore", "type": "uint256" },
    { "name": "nonce", "type": "bytes32" }
  ]
}
```

### EIP-712 Message Example

```json
{
  "from": "0xYourWalletAddress",
  "to": "<pay_to from accepts>",
  "value": 100000,
  "validAfter": 1773093821,
  "validBefore": 1773097421,
  "nonce": "0x<random 32 bytes hex>"
}
```

For signing, `value`, `validAfter`, and `validBefore` are integers. In the transport payload below, those same values must be strings.

### `X-PAYMENT` Header Format

```json
{
  "x402Version": 2,
  "scheme": "exact",
  "network": "eip155:1",
  "asset": "<asset from accepts>",
  "pay_to": "<pay_to from accepts>",
  "price": "<chosen amount as string>",
  "nonce": "0x<same nonce as authorization>",
  "payload": {
    "signature": "0x<EIP-712 signature>",
    "authorization": {
      "from": "0xYourWalletAddress",
      "to": "<pay_to from accepts>",
      "value": "100000",
      "validAfter": "1773093821",
      "validBefore": "1773097421",
      "nonce": "0x<same nonce>"
    }
  }
}
```

Critical rules:

- `payload.authorization` values must be strings.
- top-level `price` must be a string.
- the sent `payload.authorization` values must exactly match the values that were signed.
- if a payment attempt is retriable, retry the same encoded `X-PAYMENT` first instead of immediately generating a new nonce.

Request headers for the paid retry:

```text
Authorization: Bearer <jwt>
X-PAYMENT: base64(<payment json>)
```

## Response Headers

| Header | Meaning |
|---|---|
| `Authorization` | New JWT after successful SIWX auth |
| `X-Credits-Remaining` | Credits left after a successful charged request |
| `X-Credit-Cost` | Credits deducted for the request |
| `X-Credits-Purchased` | Credits added by the payment |
| `Payment-Response` | Base64 JSON settlement metadata, usually includes `txHash` |

## Common Outcomes

| Scenario | Status | What to do |
|---|---|---|
| No auth yet | `402` | Parse `accepts` and `extensions.sign-in-with-x` |
| SIWX succeeded, no credits | `402` with `Authorization` header | Reuse the JWT and buy credits |
| Query with existing credits | `200` | Return data and remaining credits |
| Purchase plus query success | `200` | Return data, credit headers, and payment metadata |
| SIWX nonce expired or replayed | `401` | Start over from a fresh challenge |
| Credits exhausted later | `402` | Buy more credits using the latest `accepts[]` |

## Credit Economics

- Base credit cost is `$0.000025` per credit.
- Prices are in USDC atomic units, where `1000000 = 1 USDC`.
- Credits are `floor(amount * credits_per_token)`.

## Common Pitfalls

1. Resolve the endpoint from docs, not from SIWX metadata.
2. Keep SIWX signing and ERC-3009 payment signing separate.
3. Use the latest live `accepts[]` values. Do not hardcode `asset`, `pay_to`, or price.
4. Use the token contract's EIP-712 domain, not a guessed symbol or label.
5. Set `verifyingContract` to the exact `asset` address from `accepts[]`.
6. Keep method, path, query, and body unchanged across retries.
7. Use standard base64 with `=` padding.
8. Retry the same payment payload before generating a fresh authorization.

## Explorer Links

When `Payment-Response` includes a transaction hash:

| Network | Explorer |
|---|---|
| `eip155:1` | `https://etherscan.io/tx/<tx_hash>` |
| `eip155:8453` | `https://basescan.org/tx/<tx_hash>` |
