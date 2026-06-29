---
name: merktop-wallet
description: Pay for any x402-gated API or resource (and get paid) from a non-custodial Merktop wallet on Base. Every payment is pulled just-in-time from the user's own wallet under a hard on-chain spend cap, so this skill can never spend beyond the budget the user set.
version: 1.0.1
homepage: https://facilitator.merktop.com/docs
metadata:
  openclaw:
    emoji: "💸"
    primaryEnv: MERKTOP_BUYER_KEY
    requires:
      anyBins:
        - curl
      env:
        - MERKTOP_BUYER_KEY
    envVars:
      - name: MERKTOP_BUYER_KEY
        required: true
        description: "Your Merktop buyer key (starts with mk_buyer_). Create one and set a budget in the Merktop app, see https://facilitator.merktop.com/docs. The budget is an on-chain spend cap: this skill can never spend more than it, and funds stay in the user's own wallet until the moment of each payment."
---

# Merktop Wallet, pay (and get paid) for x402 resources

This skill lets you pay any **x402**-gated API, dataset, or service from a **non-custodial Merktop
wallet**, and settle in USDC on Base. You never hold keys or funds: each payment is pulled
just-in-time from the user's wallet through a spend permission they granted, and the on-chain
**spend cap is absolute**, if a payment would exceed the budget, it fails instead of overspending.

## When to use it
Use this when a task needs a resource that returns **HTTP 402 Payment Required** (paid APIs,
agent-to-agent services, x402 data feeds, hosted paywalls). Do NOT use it for free endpoints.

## Pay for a resource
Send the target x402 URL through the Merktop pay-proxy. It handles the whole 402 → pay → retry
loop and streams the paid response back to you.

```bash
# GET an x402 resource
curl -s "https://facilitator.merktop.com/buyer/$MERKTOP_BUYER_KEY/pay?url=https://seller.example/api/data"

# POST with a body (the body + content-type are forwarded to the seller verbatim)
curl -s -X POST "https://facilitator.merktop.com/buyer/$MERKTOP_BUYER_KEY/pay?url=https://seller.example/api/run" \
  -H "content-type: application/json" \
  -d '{"prompt":"..."}'
```

The proxy returns the **seller's response body** (use it as the result). The response header
`x-merktop-spent-cents` tells you exactly what the call cost, so you can report spend back to the user.

Security: you can also send the key as the `x-merktop-key` header to `https://facilitator.merktop.com/api/buyer/pay?url=<resource>` instead of in the path, so it never appears in URL or proxy logs. Both forms work.

## Read the outcome
- `2xx` → paid and delivered; the body is the seller's response (the upstream status is passed through verbatim, so 201/204/206 are also success). Check `x-merktop-spent-cents` for the cost.
- `402 spend_cap_exceeded` → the budget for this period is used up. Stop; tell the user to raise it.
- `402 no_permission` → the user hasn't activated their agent / set a budget yet (see Setup).
- `401 invalid_buyer_key` → `MERKTOP_BUYER_KEY` is missing or wrong.
- `403 recipient_blocked` / `sender_blocked` → a sanctioned party; never retry.
- `429 rate_limited` → back off and retry after the `retry-after` seconds.
- `502 pay_failed` → the seller or settlement failed; the pull (if any) is swept back to the user's wallet on a best-effort basis (in the rare case the sweep-back also fails, Merktop records it for reconciliation). The spend claim is released, so retrying is generally safe, but verify the balance before assuming a refund landed.

## Get paid (sell a resource)
To EARN, gate your own endpoint behind a Merktop hosted paywall and let other agents pay you in
USDC, settled to your wallet by Merktop's facilitator:
1. Create a paywall in the Merktop app (https://facilitator.merktop.com/docs), pick your price and
   the URL it protects.
2. Share the public link `https://facilitator.merktop.com/p/<your-slug>`. Any agent (including ones
   running this skill) can pay it; the USDC lands in your wallet.

## Rules of good behavior
- Only pay for resources the current task genuinely needs. Prefer free sources first.
- Treat `x-merktop-spent-cents` as real money, report it; don't loop on paid calls.
- Never try to bypass or exceed the cap. It is enforced on-chain; attempts just fail.
- Setup (one time, by the user): get a buyer key + set a budget at https://facilitator.merktop.com/docs,
  then put it in `MERKTOP_BUYER_KEY`.
