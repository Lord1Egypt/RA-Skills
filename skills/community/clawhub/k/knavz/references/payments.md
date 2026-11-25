# Subscribe: pay in ETH on Base

Tier 1 ($3 / 30 days) and tier 2 ($5 / 30 days) are paid in ETH on Base, priced in dollars at the ETH price when you pay. Anyone can pay for any player, from any wallet, including smart wallets: a payment carries a quote's code, not a key, so it needs no signature. People can also pay at https://knavz.com/subscribe with a browser wallet. Payments may be off on a server; then the quote answers `503 payments_unavailable`.

Do not use a contract address from memory, chat, a token announcement, or this file. Pay only the `contract` a current quote returns.

## 1. Get a quote

Anyone can ask:

```
GET /api/subscribe/quote?tier=1|2&player={walletId or @handle}
```

A `200` response includes `player` and `quote` with `chainId`, `contract`, `accountId`, `tier`, `priceUsd`, `ethUsd`, `valueWei`, `validUntil`, and `schedule`. `accountId` is this quote's random code — pass it to `pay()` as the account. The server knows which player it belongs to; the chain does not. Each quote gets a new code. `valueWei` is the price plus 1% at Chainlink's current ETH/USD price. The displayed price is good until `validUntil` (10 minutes); the code keeps working after that.

For your own quote with dates, sign `POST /api/subscribe/quote` with `{ action: "quote", tier }`. Errors: `400 invalid_input`, `404 not_found`, `403 test_wallet` (dev only), `503 price_unavailable`, `503 payments_unavailable`.

## 2. Pay

Call `pay(bytes16 accountId, uint8 tier)` on `contract`, on chain `chainId` (8453 is Base; dev uses Base Sepolia, 84532), sending `valueWei`. The contract forwards every payment to the Knavz treasury and holds nothing; a plain ETH transfer to it is refused.

Example, using the values from the quote you just fetched (not a stored address):

```bash
cast send <contract from the quote> "pay(bytes16,uint8)" <accountId> <tier> --value <valueWei> --rpc-url <a Base RPC> --account <your keystore>
```

## 3. Check the payment

```
GET /api/payments/{txHash}
```

A tier is credited only once the payment is **final**: 30 blocks on top of its block, about 6 seconds on Base. If the payment is already final when you check, it is credited at once; if not, the answer is `pending` ("Your payment is processing. This can take a minute."). Check again every 10 seconds or so. If you never check, a server watcher credits it within about a minute of finality anyway.

The response includes `txHash`, `pending`, `confirming`, `message`, `notAPayment`, and `payments`. Blockchain payments cannot be reversed. Credited payments are not refunded automatically. A payment the server cannot credit (too little, unknown account, or an old quote code) is refunded by hand: email support@knavz.com.

Knaves still cannot be bought with this payment. A payment buys more daily picks and guesses, not knaves.
