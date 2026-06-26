# Balance — Check Available Funds

Always check balance before attempting a payment to avoid failed transactions.

## Card Balance

```
GET https://mag3nt.com/api/cards
Authorization: Bearer <MAG3NT_API_KEY>
```

Find the card matching your `MAG3NT_CARD_ID`. Key fields:

- `remaining` — available balance on this card (use for pre-flight checks)
- `balance` — total spent from this card
- `limit_amount` — max spend cap set at creation
- `status` — must be `ACTIVE` to transact
- `funding_network` — the EVM chain the card was funded on
- `accepted_protocols` — which protocols this card can pay with (e.g. `x402,ap2,mpp`)

## Treasury Balance

```
GET https://mag3nt.com/api/balance
Authorization: Bearer <MAG3NT_API_KEY>
```

Returns the treasury-level view across all cards:

- `available` — unallocated treasury funds
- `total_funded` — all deposits ever
- `total_allocated` — funds assigned to cards
- `total_spent` — total spent across all cards
- `total_withdrawn` — funds withdrawn off-platform

## Pre-Flight Check

Before paying, verify:
- `card.status` is `ACTIVE` (not `CLOSED`, `FROZEN`, or `EXPIRED`)
- `card.remaining` >= the amount from the challenge (`remaining` is the available balance; `balance` is total spent)

If balance is insufficient, tell the user the current `remaining` balance and required amount. The user can top up a card from treasury via `POST /api/cards/{id}/fund`, or deposit USDC at mag3nt.com.

Supported deposit networks: Base, Arbitrum, Optimism, Ethereum, Polygon, Avalanche.

## Important

- All balances are in **USDC**
- If the card status is not `ACTIVE`, payments will fail
- If the card is `FROZEN`, contact the card owner to unfreeze via `POST /api/cards/{id}/unfreeze`
