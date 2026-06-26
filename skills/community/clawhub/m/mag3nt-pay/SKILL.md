---
name: mag3nt-pay
version: 1.0.5
description: "Pay for APIs and services, receive payments, and manage agent wallets using Mag3nt USDC virtual cards. Activate when the agent needs to pay for a resource, encounters an HTTP 402 response, a payment challenge header (x402, MPP, Pay Link), needs to issue or verify an AP2 payment mandate, check wallet balance, or set up payment credentials for autonomous transactions."
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(node *)", "Bash(npm *)", "Bash(npx *)", "Bash(curl *)"]
---

# Mag3nt Pay

Pay for APIs and services, receive payments, and manage agent wallets using USDC virtual cards. Settles on Base (`eip155:8453`), Solana (`solana:mainnet`), and Tempo (`eip155:4217`). Assets: USDC on Base/Solana, USDC or pathUSD on Tempo.

## Preflight

Confirm credentials are set:

```bash
[[ -z "$MAG3NT_API_KEY" ]] && echo "ERROR: Set MAG3NT_API_KEY (starts with mag3nt_live_)" && exit 1
[[ -z "$MAG3NT_CARD_ID" ]] && echo "ERROR: Set MAG3NT_CARD_ID" && exit 1
[[ -z "$MAG3NT_CARD_TOKEN" ]] && echo "ERROR: Set MAG3NT_CARD_TOKEN" && exit 1
```

If credentials are missing, tell the user to visit [mag3nt.com](https://mag3nt.com) to create an account, generate an API key, and fund an agent card.

## When to Activate

Activate this skill when ANY of these occur:

1. An HTTP response has status code **402**
2. A response contains a `PAYMENT-REQUIRED` header (x402)
3. A response contains a `WWW-Authenticate` header with `Payment request=` (MPP)
4. A response body contains a `paylink` object with a `code` field (Pay Link)
5. The user asks to issue or verify an AP2 payment mandate
6. The user asks to "pay for", "buy access to", or "unlock" an API
7. The user asks to check their Mag3nt balance or card status

## How Payment Works

Mag3nt supports two payment models:

**402-based (x402, MPP):** One universal endpoint `POST https://mag3nt.com/api/pay`. Pass the target URL and the engine auto-detects the protocol (x402 or MPP) and settles on-chain.

**Pay Links** (paylink object in 402 body): Use `POST https://mag3nt.com/api/pay/{code}/settle` with card credentials. No API key required.

**AP2 (Google Agentic Payment Protocol):** A separate mandate-based flow — NOT a 402 challenge. Uses dedicated endpoints at `/api/ap2/*`. Read `references/ap2-pay.md` for the full flow.

## Protocol Detection and Routing

When you receive an HTTP 402, inspect the response in this order:

1. **Body contains `paylink` object** → Pay Link → read `references/paylink-pay.md`
2. **`PAYMENT-REQUIRED` or `X-Payment` header** → x402 → read `references/x402-pay.md`
3. **`WWW-Authenticate: Payment` header** → MPP → read `references/mpp-pay.md` then `references/x402-pay.md`

**Multiple payment methods:** Some merchants offer multiple methods (e.g. `methods: ["tempo", "stripe"]` in body, or multiple `Payment` challenges in `WWW-Authenticate`). Parse the header to identify all offered methods. Select the method Mag3nt supports — `tempo` (chain 4217), `eip155:8453` (Base), or `solana:mainnet`. Ignore methods like `stripe` or `card` that require fiat. If payment fails on a multi-method endpoint, check the error response's `challenge` object to verify which method the engine attempted. Read `references/mpp-pay.md` for details.

AP2 does NOT use HTTP 402. It is a mandate-based flow triggered by a merchant checkout. Read `references/ap2-pay.md`.

Always check balance first. Read `references/balance.md` before any payment.

## Reference Routing

| Task | Read This First |
|------|----------------|
| Set up credentials | `references/setup.md` |
| Check card balance | `references/balance.md` |
| Pay a Pay Link (most common, no API key needed) | `references/paylink-pay.md` |
| Pay any x402 / MPP protected API (402-based) | `references/x402-pay.md` |
| MPP-specific detection notes | `references/mpp-pay.md` |
| AP2 mandate-based payments (not 402) | `references/ap2-pay.md` |

## Payment Flow

1. **Detect** — Agent receives HTTP 402
2. **Buyer-Agent Preflight** — Before any autonomous spend, extract and verify:
   - **Price / cap unit** — exact amount and currency from the 402 challenge
   - **Accepted methods** — which payment methods the merchant supports (read the body and headers)
   - **Policy / version hash** — if the merchant provides terms or a policy hash, log it
   - **Revocation / dispute path** — merchant contact or refund endpoint
   - **Allow / caution / block** — if the amount exceeds the user's stated limit, STOP and ask for confirmation
3. **Check** — Verify card balance >= required amount via `GET /api/cards`
4. **Pay** — Call `POST /api/pay` with `{ card_id, card_token, url }` (or `POST /api/pay/{code}/settle` for Pay Links). The response includes a `transaction_id`, `settlement.tx_hash`, and a `credential` object as settlement evidence.
5. **Receipt** — Log the `transaction_id`, `amount_debited`, `protocol`, and `tx_hash` for audit
6. **Fulfillment** — The pay engine returns settlement evidence (`credential`, `tx_hash`, `protocol`). It does NOT fulfill the purchase for you. Fulfillment means claiming what you paid for. Every merchant may implement fulfillment differently. Read the merchant's original challenge or checkout flow to understand how they expect payment proof presented. The `credential` object from the pay response contains the settlement evidence formatted for the detected protocol — use it as a starting point, but adapt based on what the merchant specified.

## Error Handling

- **Insufficient balance (403)**: Tell the user the current balance and required amount. Suggest topping up at mag3nt.com.
- **Card frozen or inactive**: Tell the user to check their card status in the dashboard.
- **Already settled (410)**: The payment was already made. Proceed directly to retrying the request.
- **No payable option (422)**: The target URL does not offer any payment protocol. Tell the user.
- **Network mismatch**: Ensure the card's network matches what the merchant expects. The network is set when the card is created.

## Important

- Payments settle in **USDC** (Base, Solana) or **USDC/pathUSD** (Tempo) depending on the merchant's challenge
- Card credentials never leave the local environment
- The agent should always confirm the payment amount with the user before paying amounts > $1.00
- Every payment returns a `transaction_id` and on-chain `tx_hash` — always log these as charge-evidence
- Pay Links are the most common protocol — most merchants use them
- API base URL is `https://mag3nt.com` (not api.mag3nt.com)
