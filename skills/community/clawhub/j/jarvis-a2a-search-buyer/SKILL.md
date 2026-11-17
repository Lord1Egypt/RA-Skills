---
name: jarvis-a2a-search-buyer
description: No-key web search for autonomous agents. One Jarvis call, paid per use with Base USDC x402; You.com routes first with automatic Exa fallback. Fixed maximum buyer price $0.012. No search-provider account or API key required.
version: 1.0.2
homepage: https://clawhub.ai/yl124915300-dot/skills/jarvis-a2a-search-buyer
---

# x402 Web Search — No API Key

## Use when

Use this skill when an autonomous agent needs current public-web search but does not have — or should not provision — a You.com or Exa account and API key. The buyer only needs its own x402-capable wallet/client on Base.

## Why install

- No search-provider API key or account setup.
- One call to Jarvis instead of integrating multiple search suppliers.
- Pay per call with Base USDC via x402; no subscription.
- Automatic supplier routing: You.com first, then Exa fallback when needed.
- Fixed maximum buyer price: `12000` atomic USDC (`$0.012`) per search.
- Machine-readable terminal result: `SUCCESS` or `FAILED`.

## Install

`openclaw skills install @yl124915300-dot/jarvis-a2a-search-buyer`

## Minimal invocation

For a real search task, ask the installed skill:

> Search the current public web for "latest Base x402 documentation", return up to 3 results, and never authorize more than $0.012 USDC.

The skill creates a Jarvis quote, handles the endpoint's x402 challenge through the buyer's own wallet/client, and returns the terminal machine-readable result.

## Price

- Product: `MACHINE_WEB_SEARCH_V1`
- Network: Base (`eip155:8453`)
- Asset: native Base USDC
- Exact price and hard maximum: `12000` atomic USDC (`$0.012`)
- One-shot outcome: terminal `SUCCESS` or `FAILED`; no refund is promised or implemented.

## What happens under the hood

Jarvis accepts one search request, routes it to You.com first, and can fall back to Exa when needed. The buyer does not provision either supplier's credentials. Jarvis returns a machine-readable terminal outcome after the paid one-shot execution.

The Router endpoint and attribution are fixed:

- Quote: `https://jarvis-orderflow-router.yl124915300.workers.dev/v1/a2a/web-search/quotes`
- Funding: `https://jarvis-orderflow-router.yl124915300.workers.dev/v1/a2a/web-search/fund`
- Fulfilment: `https://jarvis-orderflow-router.yl124915300.workers.dev/v1/a2a/web-search/fulfil`
- Attribution header: `X-Jarvis-Client: jarvis-a2a-search-skill-v1`

## When NOT to use

- Do not call Jarvis if a free search tool already meets the task.
- Do not call if the buyer is unwilling to pay up to `$0.012` or cannot enforce that maximum.
- Do not call without a genuine current-web search need.
- Do not use for self-testing, endpoint probing, directory validation, synthetic traffic, or promotion.

## Exact call flow

1. POST a quote with `query` (1-1000 characters), optional `count` (1-5), optional `freshness`, and `max_buyer_price_atomic: "12000"`. Send a new `Idempotency-Key` and the fixed attribution header.
2. Validate the x402 v2 exact Base/USDC challenge. Using only the buyer's own x402 wallet/client, POST `{"deal_id":"<deal_id>"}` to the funding endpoint with a hard maximum of `12000` atomic USDC.
3. Only after funding succeeds, POST the same body to the fulfilment endpoint with the fixed attribution header. Return the terminal result.

Never substitute another endpoint, product, chain, token, amount, payee, or client tag. Never send a raw USDC transfer. This skill never receives, stores, or requests a wallet private key, seed phrase, API secret, or custody of funds.

Router manifest: https://jarvis-orderflow-router.yl124915300.workers.dev/.well-known/jarvis-a2a-router.json

Buyer examples: https://jarvis-orderflow-router.yl124915300.workers.dev/integrations/x402-buyers.md
