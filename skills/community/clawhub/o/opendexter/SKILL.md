---
name: opendexter
description: "Use OpenDexter to search, price-check, and pay for any x402 API. Trigger whenever the user wants to find paid APIs, call an x402 endpoint, check pricing, see wallet info, or interact with the x402 marketplace."
---

# OpenDexter — x402 API Marketplace

OpenDexter gives you access to the x402 API marketplace across Solana and EVM chains (Base, Polygon, Arbitrum, Optimism, Avalanche). Search, preview pricing, and call any endpoint with automatic USDC payment. No API keys or subscriptions needed for the endpoints — you just pay per call.

## Tools

### `x402_search` — Find APIs

Search the OpenDexter marketplace. Results are ranked by a composite score (quality, usage, freshness, reputation, reliability).

Each result includes: name, price (USDC), network, qualityScore (0-100), verified status, seller, and call count.

Highlight verified endpoints (qualityScore 75+). Search is fuzzy — typos still find results.

### `x402_check` — Preview Pricing

Probe an endpoint for payment requirements without paying. Returns per-chain pricing options. Always use before `x402_fetch` so the user knows the cost upfront.

### `x402_fetch` — Call and Pay

Call any x402 endpoint with automatic payment from the configured wallet. The plugin checks USDC balances across all funded chains and picks the best option. Returns the API response data plus a payment receipt.

If the wallet has no funds on any accepted chain, tell the user to fund their wallet.

### `x402_pay` — Alias for `x402_fetch`

Same tool, alternate name.

### `x402_wallet` — Wallet Status

Shows which wallets are configured (Solana, EVM), the per-call spending limit, and the active network. Use when the user asks about their wallet or setup.

## Workflows

### "Find me an API for X"
1. `x402_search` with their query
2. Present top results with prices and quality scores
3. `x402_check` on their pick
4. Show per-chain pricing
5. `x402_fetch` to call it

### "Call this URL"
1. `x402_check` to show the price
2. `x402_fetch` to call and pay

### "What's my wallet setup?"
1. `x402_wallet`

## Quality Scores
- 90-100: Excellent. Verified, reliable, well-documented.
- 75-89: Good. Passed verification.
- 50-74: Mediocre. May have issues.
- Below 50: Untested or poor.

## Tips
- Most endpoints cost $0.01-$0.10 per call.
- Use `verified: true` to filter to tested endpoints.
- The plugin auto-selects the cheapest chain that the endpoint accepts and the wallet has funds on.
- If no wallet is configured, tools return a config help message.
