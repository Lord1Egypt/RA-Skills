---
name: miraix-meme-court
description: Use this skill when the user wants to run Miraix Meme Court, shortlist Solana meme candidates, apply Rug Court safety and liquidity checks, approve one disciplined meme trade, prepare an unsigned payload when live Bitget execution is available, or check the status of a previously prepared order.
---

# Miraix Meme Court

Use this skill to run the public Miraix Meme Court flow for the Bitget Wallet track. The skill narrows Solana meme candidates into one approved trade by splitting the work into Scout, Risk Agent / Rug Court, and Trader.

Public endpoints:

- Desk API: `https://app.miraix.fun/api/meme-rotation-desk`
- Prepare API: `https://app.miraix.fun/api/meme-rotation-desk/prepare`
- Order status API: `https://app.miraix.fun/api/meme-rotation-desk/order-status`

Defaults:

- `walletAddress`: `AYY3Bi6NSwH3F9Q5cy5xN9ZqRgnNYhm6TMkTwVBRVGeq`
- `budgetUsd`: `100`
- `riskMode`: `balanced`
- `strategy`: `momentum`

Allowed values:

- `riskMode`: `safe`, `balanced`, `degen`
- `strategy`: `momentum`, `reversal`, `shadow`

## When to use it

- The user wants one disciplined Solana meme trade instead of a list of ideas.
- The user wants to run Scout, Rug Court, and Trader against a wallet and budget.
- The user wants a shortlist plus vetoes plus one approved trade.
- The user wants to know whether unsigned payload preparation is available.
- The user already has an `orderId` and wants to check order status.

## Workflow

1. Extract these inputs from the request:
   - `walletAddress`
   - `budgetUsd`
   - `riskMode`
   - `strategy`

   If any field is missing, fill it with the defaults above instead of blocking.

2. Run the desk:

```bash
curl -sS https://app.miraix.fun/api/meme-rotation-desk \
  -H 'Content-Type: application/json' \
  -d '{
    "walletAddress":"<wallet-address>",
    "budgetUsd":<budget-usd>,
    "riskMode":"<safe|balanced|degen>",
    "strategy":"<momentum|reversal|shadow>"
  }'
```

3. Base the answer on these fields:
   - `dataMode`
   - `warnings`
   - `marketContext`
   - `agents`
   - `candidates`
   - `approvedTrade`
   - `execution`
   - `proofBundle`

4. Lead with the one approved trade:
   - symbol
   - size in USD
   - allocation percentage
   - rationale
   - invalidation
   - take-profit ladder

5. Then summarize Rug Court:
   - approved names
   - watch names
   - banned names
   - the most important `courtNote`

6. Then summarize execution readiness:
   - `state`
   - `mode`
   - `source`
   - `market`
   - `estimatedOutput`
   - whether `canPrepare` is true

7. If and only if all of these are true:
   - the user explicitly wants payload preparation
   - `execution.canPrepare` is true
   - `execution.market` exists
   - `approvedTrade.outputContract` exists

   then call:

```bash
curl -sS https://app.miraix.fun/api/meme-rotation-desk/prepare \
  -H 'Content-Type: application/json' \
  -d '{
    "walletAddress":"<wallet-address>",
    "outputContract":"<approved-trade-output-contract>",
    "market":"<execution-market>",
    "amountUsd":<approved-trade-amount-usd>,
    "mode":"<order|swap>",
    "outputSymbol":"<approved-trade-symbol>"
  }'
```

8. If the user gives an `orderId` and wants status, run:

```bash
curl -sS https://app.miraix.fun/api/meme-rotation-desk/order-status \
  -H 'Content-Type: application/json' \
  -d '{
    "orderId":"<order-id>"
  }'
```

9. Treat preview mode honestly:
   - If `dataMode` is `fallback`, say the result is in preview mode.
   - If prepare returns `prepared: false`, say unsigned payload generation is not available in the current live environment.
   - Do not claim live signing or live order creation unless the API returns a live prepared payload.

## Output guidance

- Keep the answer structured and concise.
- Lead with `Approved trade`.
- Then show `Rug Court summary`.
- Then show `Execution readiness`.
- Then show `Warnings` if present.
- Use the exact field values from the API instead of paraphrasing away important numbers.
- If the API is in preview mode, say so explicitly.
- Do not claim that Miraix or Bitget signed, submitted, or filled any trade unless the API response proves that.
