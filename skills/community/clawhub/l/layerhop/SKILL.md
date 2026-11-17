---
name: layerhop
description: Quote and prepare cross-chain token swaps via LayerHop.
license: MIT-0
compatibility: Needs curl (or any HTTP client) and internet access to api.layerhop.com. Works with any agent; MCP clients can use https://mcp.layerhop.com/mcp instead.
metadata:
  version: "1.0.0"
  author: LayerHop
  homepage: https://docs.layerhop.com/guides/ai-agents
  openclaw:
    emoji: "🔁"
    homepage: https://docs.layerhop.com/guides/ai-agents
    requires:
      anyBins: [curl]
    envVars:
      - name: LAYERHOP_API_KEY
        required: false
        description: Optional LayerHop API key (lh_live_...). Raises rate limits; needed only for deposit addresses.
      - name: LAYERHOP_INTEGRATOR
        required: false
        description: Optional partner id, added to quotes and swap links so the integrator earns its partner fee.
  hermes:
    tags: [crypto, defi, bridge, swap, cross-chain]
---

# LayerHop: cross-chain swap quotes

LayerHop is a cross-chain swap API. One call compares routes from many bridges and aggregators across 70 chains
(Ethereum, Base, Arbitrum, Optimism, BNB Chain, Polygon, Solana, Tron, Hyperliquid and more) and returns the best
quote with every fee itemised.

**This skill never moves funds.** It only reads quotes and prepares data. LayerHop holds no keys and never signs.
The user's own wallet signs every swap, after the user has seen the quote and said yes.

## When to Use

- The user asks how much they'd get swapping or bridging a token from one chain to another.
- The user wants the cheapest or fastest route between two chains.
- The user wants a link to do the swap in their own wallet.
- The user wants to fund a Hyperliquid perps account or another chain from tokens they hold elsewhere.

Don't use it for price speculation, trading advice, or anything that needs the user's private key.

## Prerequisites

- `curl` (or any HTTP client). Base URL: `https://api.layerhop.com`.
- Optional: `LAYERHOP_API_KEY` sent as the `x-api-key` header. Without a key, requests are rate-limited per IP.
- MCP alternative: if the agent supports MCP, connect `https://mcp.layerhop.com/mcp` instead (same rules, ready-made tools).

## Quick Reference

| Step | Call |
|---|---|
| Chains | `GET /v1/chains` |
| Find a token | `GET /v1/tokens?chain=base&q=USDC` |
| Quote | `GET /v1/quote?srcChain=…&srcToken=…&amount=…&dstChain=…&dstToken=…&sender=…&recipient=…` |
| Unsigned transaction | `POST /v1/orders` with `{"quoteId":"q_…"}` |
| Order status | `GET /v1/orders/{provider}/{sourceTxHash}` |
| Swap link (user signs on layerhop.com) | `https://layerhop.com/swap?srcChain=base&srcToken=USDC&dstChain=arbitrum&dstToken=USDC&amount=25` |

Chains are slugs (`ethereum`, `base`, `arbitrum`, `solana`, `hyperliquid`, …). Tokens are a symbol such as `USDC`
or a contract address. In the API, `amount` is in **base units** of the source token (USDC has 6 decimals, so
`25000000` = 25 USDC). In a swap link, `amount` is human (`25`).

## Procedure

1. **Collect the inputs:** source chain and token, amount, destination chain and token, and the user's address
   (`sender`; also `recipient`, which must be on the destination chain's VM, for example a Solana address for
   Solana). If anything is missing, ask. Never guess an address.
2. **Quote:**
   ```bash
   curl -s "https://api.layerhop.com/v1/quote?srcChain=base&srcToken=USDC&amount=25000000&dstChain=arbitrum&dstToken=USDC&sender=0xUSER&recipient=0xUSER" \
     ${LAYERHOP_API_KEY:+-H "x-api-key: $LAYERHOP_API_KEY"}
   ```
   Read `best`: `provider`, `dstAmount` and `dstAmountMin` (destination base units), `estimatedSeconds`, `fees`,
   and `expiresAt` (quotes expire within about a minute). `quotes` lists the alternatives.
3. **Show the user the quote** in human units: what they send, what they receive at least (`dstAmountMin`), the
   fees, and the time. Ask whether to proceed. **Never continue without an explicit yes.**
4. **Hand over for signing**, in one of two ways:
   - **Default:** give a swap link (`https://layerhop.com/swap?...`, human amount). The user reviews and signs in
     their own wallet on layerhop.com.
   - **The user's own signer** (only if the user runs a wallet tool they control): `POST /v1/orders` with the
     `quoteId`. The response `tx` holds `chainId`, `to`, `data` and `value`, plus `approval` if a token approval
     must come first. Pass these to the user's signer; this skill does not sign or broadcast.
5. **Track:** after the user's wallet broadcasts, check `GET /v1/orders/{provider}/{sourceTxHash}` until the order
   `state` is `filled` (or `refunded` / `failed`), and report the outcome.

## Pitfalls

- **Never ask for or accept a private key or seed phrase.** If the user offers one, refuse and tell them to keep it secret.
- Quotes expire. If `expiresAt` has passed, quote again before building.
- Decimals: USDC and USDT are 6 on most EVM chains, 18 on BNB Chain; ETH is 18; Hyperliquid perps USDC is 8.
- `NO_ROUTE` errors often carry `error.details.suggestions` (another token or a hub chain), and `AMOUNT_TOO_SMALL`
  carries the route's minimum. Pass these on to the user.
- Hyperliquid is destination-only: quote `dstChain=hyperliquid&dstToken=USDC`, with the user's EVM address as recipient.
- Don't present a quote as guaranteed. The amount received can be lower, down to `dstAmountMin`.

## Verification

- `GET https://api.layerhop.com/v1/health` returns 200.
- A test quote for 10 USDC Base → Arbitrum returns `best.quoteId` and a `dstAmount` close to 10 USDC (`~9.9…e6`).

Docs: https://docs.layerhop.com · API reference: https://docs.layerhop.com/api-reference · MCP: https://docs.layerhop.com/guides/ai-agents
