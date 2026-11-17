---
name: iomarkets-topup
description: Buy real-world things for your principal with USDC on Algorand via x402 — travel eSIMs for 200+ destinations, and mobile airtime and data top-ups in 150+ countries delivered to any phone number. Use when the user is travelling and needs data abroad, asks to recharge or top up a phone, buys mobile data, or checks a USDC→local FX rate. No account, no card; signed proof of delivery; automatic on-chain refunds. Prepaid bills and international payouts are built but supplier-gated — GET /v1/catalog is the live answer.
version: 0.2.7
metadata:
  homepage: https://iomarkets.app
  agent_docs: https://iomarkets.app/agent.md
  tags: [x402, algorand, usdc, esim, travel, topup, airtime, agentic-commerce, real-world]
---

# IoMarkets Topup

Real-world checkout for agents. Four HTTP calls, or the `iomarkets-topup` MCP server (`pnpm mcp` in the repo).

## What is live

**Two products, both selling today:**

- **`type: "esim"` — travel eSIMs, 200+ destinations.** $0.50–$50 a package. There is no recipient: an
  eSIM is delivered to the buyer as an **LPA activation string** they install on their own phone.
  `GET /v1/countries?type=esim` lists every destination; `GET /v1/catalog?type=esim&country=JP` lists
  the packages for one.
- **`type: "topup"` — mobile airtime and data, 150+ countries**, delivered to a phone number.

`type: "bill"` and `type: "payout"` (international payments) are implemented end to end — same quote,
same settlement, same signed receipt — but each needs a supplier that is not currently wired. **Do not
offer those two on the strength of this file.** `GET /v1/catalog?type=<type>` is the live answer and
returns an empty list for anything unavailable; `/agent.md` names the live set in its first paragraph.
A quote for an unavailable type is refused up front rather than accepted and then failed.

⚠️ **eSIMs are sold for travel, on ordinary phones.** The supplier's terms exclude routers, dongles,
IoT devices, hotspots and automated background traffic. Do not buy one to put in a server.

## When to use
- "I land in Tokyo on Tuesday — get me data for a week" → eSIM
- "Cheapest 5GB eSIM for Europe" · "Does this work in Georgia?" → `GET /v1/countries?type=esim`
- "Top up / recharge +91…, +234…, +995… with N (local currency)" → topup
- "Buy mobile data for this number" → topup
- "What's the USDC→INR rate?"

## Procedure
1. **Discover** — `GET https://iomarkets.app/v1/lookup?phone=<E.164>` (operator + offers) or `GET https://iomarkets.app/v1/catalog?type=esim&country=IN`.
2. **Quote** — `POST https://iomarkets.app/v1/quote` with `{type, offerId, recipient:{phone}, amount}` (amount in the recipient's currency for range offers; omit for fixed bundles). **For an eSIM there is no recipient**: `{"type":"esim","offerId":"ea-…","recipient":{}}`. You get `quoteId`, `price_usdc`, `delivers`, `expires_at`.
   A quote can be refused with **503** when the supplier float cannot cover it; the message says how much is fillable, so re-quote smaller rather than retrying the same amount. `GET /v1/limits` publishes `fillable_now_usdc` if you want to size a basket first.
3. **Confirm with the human** — state exactly: *what* is delivered, *to whom* (number), and the *USDC price*. Never skip this for a purchase.
4. **Pay** — `POST https://iomarkets.app/v1/orders` with `{ "quoteId" }` using your x402 client (Algorand USDC, `exact` scheme). First response is 402 with the exact amount; retry with the payment signature. 202 → order.
5. **Poll** — `GET https://iomarkets.app/v1/orders/<orderId>` every 3 s until `terminal: true`. Report `status`, the `confirmation` (operator reference / eSIM LPA + install steps) and the `settlement_url`.
6. **If refunded** — tell the human the money is back at their address (`refund_url`) and offer to retry with another offer.

**No wallet, or the human should pay themselves?** Skip steps 4–5: `POST https://iomarkets.app/v1/links` with `{type, offerId, recipient, amount, note}` (topup or esim) and give the human the returned `url`. They see the exact price and approve it in their own Pera wallet. You never hold a key, and the eSIM QR code appears on their page. A top-up link can be paid by anyone, so it works as a "top up my phone" request to family. Add `"ref": "<your Algorand address>"` to any quote or link to earn a share of margin on delivered orders (`GET /v1/referrals`).

## Rules
- One quote = one payment. Quotes expire in 10 minutes; re-quote instead of retrying an expired one.
- Respect the wallet budget you were given. Server-side caps are $50/order and $200/payer/day — **read `GET /v1/limits` rather than trusting these numbers**, which change without this file changing.
- **Confirm the operator with the human before buying.** `/v1/lookup` detects it from the number range and is reliably wrong on MVNOs (Tesco Mobile, Giff Gaff, Lebara, Voxi, Sky resolve to the host network). A voucher bought for the wrong network delivers successfully, verifies, and cannot be redeemed or refunded. Use `other_brands` to correct it.
- Top-ups are irreversible once delivered: read the number back to the human verbatim before `buy`.
- **An eSIM is delivered as `confirmation.lpa`** — an `LPA:1$…` string the human installs in
  Settings → Mobile Data → Add eSIM, plus `qrcode_url` if they would rather scan it. Give them both,
  and the validity (`validity_days`) and data (`data_bytes`).
- Keep the receipt (`order.receipt`) — it is the proof of delivery. Check it with the `verify_receipt` tool, or `POST /v1/verify` with the receipt as the body: it checks the signature **and** both transactions on Algorand, and works on receipts from any server using the format (`/receipts.md`).
- Do not retry a `buy` on a timeout without first checking `order_status`; the settlement may have succeeded.

## Install as MCP (Claude Code / Codex / Cursor / Hermes / OpenClaw)

**Hosted — nothing to install, no key given to anyone:**
```json
{ "mcpServers": { "iomarkets-topup": { "url": "https://iomarkets.app/mcp" } } }
```
This server holds no wallet, so `buy` returns the x402 payment challenge (exact amount, asset, `payTo`,
facilitator) for **you** to pay from your own Algorand wallet, then you re-POST the quote with your payment
signature. Everything else — lookup, catalog, quote, order status, receipt verification, FX, ledger — works as-is.

**Local — the server pays for you, under a budget:**
```json
{ "mcpServers": { "iomarkets-topup": { "command": "pnpm", "args": ["--dir", "/path/to/iomarkets-app", "mcp"],
  "env": { "API_URL": "https://iomarkets.app", "AGENT_MNEMONIC_FILE": "/home/you/.secrets/agent.mnemonic", "AGENT_BUDGET_USD": "20" } } } }
```
Here `buy` signs and settles itself from the agent wallet, capped by `AGENT_BUDGET_USD` per session and
`AGENT_MAX_ORDER_USD` per order. Keep the mnemonic in a file (mode 0400) — never inline in the config.
