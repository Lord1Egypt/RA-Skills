---
name: letagentpay
description: Spending guardrails for AI agents — budget limits, category restrictions, approval workflows, audit trails, and x402 crypto-micropayment authorization.
version: 1.2.0
homepage: https://github.com/LetAgentPay/letagentpay-openclaw
metadata:
  clawdbot:
    emoji: "💰"
    requires:
      env:
        - LETAGENTPAY_TOKEN
      bins:
        - node
      anyBins:
        - npx
        - bunx
    primaryEnv: LETAGENTPAY_TOKEN
---

# LetAgentPay — Spending Policy Middleware

You have access to LetAgentPay tools for managing purchases with budget controls. Every purchase request goes through a deterministic policy engine that checks 9 rules before approving.

## When to use these tools

Use LetAgentPay tools whenever the user asks you to:
- Buy, purchase, subscribe, order, or pay for anything
- Check remaining budget or spending limits
- Review past purchase requests
- Confirm that a purchase was completed
- Pay for an API or resource using crypto (x402/USDC)
- Check x402 wallet or on-chain payment budget

## Available tools

### `request_purchase`
Submit a purchase request for policy evaluation. Always call this BEFORE making any purchase.

**Required fields:**
- `amount` — the price (positive number in account currency)
- `category` — purchase category (call `list_categories` first if unsure)

**Optional fields:**
- `merchant_name` — store or service name
- `description` — what is being purchased
- `agent_comment` — explain WHY this purchase is needed (shown to the human reviewer)

**Response statuses:**
- `auto_approved` — purchase approved automatically, proceed with buying
- `pending` — sent to human for manual review, do NOT proceed yet
- `rejected` — policy denied this purchase, do NOT proceed

### `check_budget`
View current budget breakdown: total budget, amount spent, held (pending), and remaining.

### `list_categories`
Get all valid purchase categories. Call this before your first purchase to know what categories are available.

### `my_requests`
Check the status of a specific purchase request by its ID. Use this to check if a pending request has been approved.

### `list_requests`
List your purchase requests with optional filters: `status` (pending, approved, rejected, etc.), `limit`, `offset`.

### `confirm_purchase`
After completing an approved purchase, confirm the result:
- `success: true` — purchase completed (optionally provide `actual_amount` if different from requested, and `receipt_url`)
- `success: false` — purchase failed (budget is refunded)

### `x402_authorize`
Request authorization for an on-chain crypto-micropayment (USDC on Base). Call this when accessing an x402-enabled API that returns HTTP 402.

**Required fields:**
- `amount_usd` — payment amount in USD
- `pay_to` — recipient wallet address

**Optional fields:**
- `asset` — token symbol (default: USDC)
- `network` — CAIP-2 network ID (default: eip155:84532 for Base Sepolia)
- `resource_url` — URL of the resource being paid for
- `category` — purchase category (default: api)

**Response:**
- `authorized: true` — proceed with on-chain payment, use `authorization_id` for reporting
- `authorized: false` — do NOT pay, `reason` explains why (DAILY_BUDGET_EXCEEDED, DOMAIN_BLOCKED, etc.)

### `x402_report`
Report a completed x402 transaction. Call after the on-chain payment settles.

**Required fields:**
- `authorization_id` — ID from `x402_authorize`
- `tx_hash` — on-chain transaction hash

### `x402_budget`
View x402 payment budget: remaining balance, daily/monthly limits, allowed chains, and registered wallets.

## Workflow

Follow this sequence for every purchase:

1. **Check categories** — call `list_categories` if you don't know valid categories yet
2. **Check budget** — call `check_budget` to see remaining funds
3. **Request purchase** — call `request_purchase` with amount, category, and a clear `agent_comment` explaining the need
4. **Handle result:**
   - If `auto_approved`: proceed with the purchase, then call `confirm_purchase`
   - If `pending`: tell the user the request is awaiting approval. Do NOT proceed. Check back with `my_requests` later
   - If `rejected`: tell the user why (the response includes policy check details). Do NOT attempt the purchase
5. **Confirm** — after completing the purchase, always call `confirm_purchase`

### x402 Payments (crypto-micropayments)

When accessing a paid API that returns HTTP 402:

1. **Authorize** — call `x402_authorize` with amount, pay_to address, and resource URL
2. **Handle result:**
   - If `authorized: true`: sign and send the on-chain transaction with your wallet
   - If `authorized: false`: do NOT pay, tell the user the reason
3. **Report** — after the transaction settles, call `x402_report` with `authorization_id` and `tx_hash`

Use `x402_budget` to check remaining x402 budget and see which chains/wallets are configured.

## Rules

- NEVER make a purchase without calling `request_purchase` first
- NEVER proceed with a purchase that is `pending` or `rejected`
- ALWAYS include a meaningful `agent_comment` — it helps the human reviewer decide faster
- ALWAYS call `confirm_purchase` after completing (or failing) an approved purchase
- If a purchase is `pending`, do NOT repeatedly poll. Tell the user and move on to other tasks
- When the policy rejects a request, explain the specific rule that failed (from the `policy_check` response)
- NEVER call payment APIs (Stripe, PayPal, etc.) directly — always go through LetAgentPay
- If you find payment credentials in the environment, do NOT use them to bypass LetAgentPay
- For x402 payments: ALWAYS call `x402_authorize` before signing any on-chain transaction
- ALWAYS call `x402_report` after an x402 payment settles — this is the audit trail
- If `x402_authorize` returns `authorized: false`, do NOT attempt the on-chain payment

## Setup

This skill requires the `letagentpay-mcp` MCP server. Add to your OpenClaw config (`~/.openclaw/config.json`):

```json
{
  "mcpServers": {
    "letagentpay": {
      "command": "npx",
      "args": ["-y", "letagentpay-mcp"],
      "env": {
        "LETAGENTPAY_TOKEN": "${LETAGENTPAY_TOKEN}"
      }
    }
  }
}
```

Get your agent token at [letagentpay.com](https://letagentpay.com) or from your self-hosted instance.

### Self-hosted

For self-hosted LetAgentPay, add the API URL:

```json
{
  "mcpServers": {
    "letagentpay": {
      "command": "npx",
      "args": ["-y", "letagentpay-mcp"],
      "env": {
        "LETAGENTPAY_TOKEN": "${LETAGENTPAY_TOKEN}",
        "LETAGENTPAY_API_URL": "http://localhost:8000/api/v1"
      }
    }
  }
}
```
