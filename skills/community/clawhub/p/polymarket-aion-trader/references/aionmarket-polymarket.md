# Aionmarket Polymarket Reference

This reference summarizes the Aionmarket documentation needed to place Polymarket trades.

## Base API

- Base URL: `https://pm-t1.bxingupdate.com/bvapi`
- Auth header: `Authorization: Bearer YOUR_API_KEY`
- `POST /agents/register` is the only documented unauthenticated endpoint.

## Core Flow

1. Register agent: `POST /agents/register`
2. Verify agent and connectivity: `GET /agents/me`
3. Register wallet credentials for Polymarket live trading: `POST /wallet/credentials`
4. Verify wallet readiness: `GET /wallet/credentials/check?walletAddress=...`
5. Search market or review briefing: `GET /markets`, `GET /markets/briefing`
6. Inspect market context before trading: `GET /markets/context/:marketId?user=YOUR_WALLET`
7. Submit signed trade: `POST /markets/trade`
8. Monitor positions or open orders after execution.

Where the Python SDK is available, the docs show SDK equivalents for briefing and wallet credential management. See [aionmarket-sdk.md](./aionmarket-sdk.md).

## Wallet Credential Registration

Polymarket live trading requires wallet credential registration. The documented payload is:

```json
{
  "walletAddress": "0x1111111111111111111111111111111111111111",
  "apiKey": "your-polymarket-api-key",
  "apiSecret": "your-polymarket-api-secret",
  "apiPassphrase": "your-polymarket-api-passphrase"
}
```

Verification returns `hasCredentials: true` and a detected `signatureType` when the wallet is ready.

## Trade Payload Requirements

Documented top-level fields for `POST /markets/trade` include:

- `venue`: defaults to `polymarket`
- `marketConditionId`: required
- `marketQuestion`: required
- `outcome`: required, `YES` or `NO`
- `orderSize`: required number of contracts
- `price`: required price per contract
- `isLimitOrder`: optional boolean
- `orderType`: optional, `GTC`, `FOK`, `GTD`, or `FAK`
- `walletAddress`: optional but should be supplied for clarity
- `orderVersion`: optional, `1` or `2`
- `order`: required signed EIP712 payload
- `reasoning`: optional but recommended
- `source`: optional source tag
- `skillSlug`: optional skill identifier

Additional optional fields documented for V2 and advanced control include `tickSize`, `negRisk`, `funderAddress`, `postOnly`, `deferExec`, `owner`, `feeAmount`, and `expirationTime`.

## Signed Order Object

Aionmarket documentation states that `order` must already be a signed EIP712 Polymarket order payload. Required fields vary slightly by order version, but commonly include:

- `maker`
- `signer`
- `taker`
- `tokenId`
- `makerAmount`
- `takerAmount`
- `side`
- `expiration`
- `signature`
- `salt`
- `signatureType`

Version-specific fields may also include `nonce`, `feeRateBps`, `timestamp`, `metadata`, and `builder`.

## Precision Rules

For immediate BUY orders using `FAK` or `FOK`, the docs call out extra precision checks:

- `makerAmount` supports max 2 decimals
- `takerAmount` supports max 4 decimals
- amounts are sent as 6-decimal micro-units
- validate `makerAmount % 10000 == 0`
- validate `takerAmount % 100 == 0`

## Status And Error Handling

- `200` or `201`: accepted or success, depending on endpoint
- `400`: invalid payload, market, outcome, or order object
- `401`: invalid or missing API key
- `403`: forbidden, often claim status, permission, or guardrail issue
- `429`: rate limited, retry with backoff and jitter
- `500`: server-side failure

## Best-Practice Checklist

- Verify the agent is claimed before live trading.
- Confirm wallet credentials belong to the same Polymarket owner as the wallet address.
- Check market context before execution.
- Prefer the documented SDK methods for briefing and wallet credential setup, then fall back to REST for trade submission if no documented SDK submit helper is available.
- Start with small order size.
- Include `reasoning` for auditability.
- Monitor open orders and positions after submission.
- Do not store private keys or secrets in repository files.
