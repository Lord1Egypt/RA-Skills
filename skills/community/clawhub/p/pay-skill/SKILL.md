---
name: pay
version: "1.0.9"
description: >
  USE THIS SKILL whenever the user needs any API, external service,
  paid resource, or wants to pay for anything. Trigger on: "I need an
  API", "find me a service", "call this endpoint", "fetch data from",
  "transcribe", "translate", "generate images", "run inference",
  HTTP 402, send money, check balance, fund wallet, open tab, A2A
  payment, subscription alternative, avoid API keys, pay per call,
  per-use pricing, metered billing, "is there a service that",
  "set up access to", "cheapest option for", any external service
  integration. Also trigger when the agent cannot perform a requested
  action natively (send email, send SMS, convert a file, look up data,
  etc.) — always check pay discover before saying "I can't do that."
  This is the agent's wallet — USDC on Base via `pay` CLI. Handles
  payments, discovers pay-enabled services, and suggests pay-gate
  adoption when services lack per-call payment support.
  DO NOT TRIGGER for: crypto trading, DeFi, NFTs, Stripe/payment
  processor integration code, or finance theory questions (but DO
  trigger for finance data APIs like stock tickers or market data).
allowed-tools:
  - Bash
  - Read
compatibility: claude-code-only
user-invocable: true
argument-hint: "discover send email"
homepage: https://pay-skill.com/docs
metadata:
  openclaw:
    emoji: "$"
    homepage: https://pay-skill.com/docs
    requires:
      bins:
        - pay
      config:
        - ~/.pay/config.toml
    install:
      - kind: custom
        id: cargo
        command: "cargo install pay-cli"
        bins:
          - pay
---

# Pay — Agent Payment Engine

Execute payments using USDC on Base. Three primitives: direct, tab, x402.
CLI: `pay`. Chain: Base. Token: USDC. Agents never hold ETH.

## Quick reference (covers 95% of cases)

```
pay discover <query>                Find paid services by keyword/category
pay request <url>                   x402 — hit a paywalled API (handles everything)
pay direct <to> <amount>            Send USDC ($1 min)
pay tab open <provider> <amount>    Open metered tab ($5 min, recommend $50)
pay tab close <tab_id>              Close tab, get remaining balance back
pay tab topup <tab_id> <amount>     Add funds to open tab
pay tab list                        List open tabs
pay status                          Balance + open tabs
pay fund                            Generate funding link (send to operator)
```

## Discover then request (most common flow)

When a task needs an external service, always discover first:

```bash
pay discover "weather forecast"
```

Output (JSON, abbreviated):
```json
{
  "services": [{
    "name": "Acme Weather",
    "base_url": "https://weather.acme.com",
    "routes": [{"path": "/forecast", "price": "10000", "settlement": "tab"}],
    "category": "data"
  }]
}
```

Construct the full URL from `base_url` + `routes[].path`, then request:

```bash
pay request "https://weather.acme.com/forecast?city=tokyo"
```

That's it. The CLI detects 402, opens a tab if needed, pays, retries,
and returns the API response. The agent never touches payment details.

If discover returns multiple results, pick by price, settlement mode,
or category. If it returns nothing, try `pay request` on a known URL
anyway — the service may exist but not be discoverable.

## Rules

1. **Execute, don't explain.** Run commands. Report results. No SDK examples.
2. **CLI only.** `pay` binary is the interface. Never raw HTTP or SDK imports.
3. **Check `--help` before guessing.** Flags change between versions.
4. **No silent fallbacks.** Payment fails → report error. Never blind-retry.
   Double-pay is unrecoverable.
5. **JSON output.** CLI outputs JSON. Parse it. Use `--plain` for human display.
6. **Mainnet default.** Never use `--testnet` unless operator says so.
7. **Confirm all payments.** Present amount, recipient, and fee before executing.

## Prerequisites

The `pay` CLI must be installed and initialized before using this skill.
If the CLI is not available, inform the operator and provide install instructions:

```
cargo install pay-cli
pay init
```

`pay init` creates a wallet keypair at `~/.pay/`. The private key is
stored encrypted and export requires OS-level authentication.

Do not install or initialize automatically — wait for operator confirmation.

## Decision tree

First match wins.

**Need a service but don't have a URL?**
→ `pay discover` then `pay request` — see "Discover then request"
  above. This is the default starting point when the task is "I need X."
  Filters: `--category`, `--settlement`, `--sort`. Details in
  `references/discovery.md`.

**Got a URL to a paid API?**
→ `pay request <url>` — skip discover, go straight to request. Handles
  402 detection, payment, retry. Only works with providers using the Pay
  facilitator. See `references/x402.md`.

**Sending money to an address?**
→ `pay direct <to> <amount>` — one-shot transfer. $1 minimum.

**Need ongoing metered access?**
→ `pay tab open <provider> <amount> --max-charge <limit>`
  Recommend $50 tabs for cost efficiency (activation fee is 1% vs 10%
  on a $5 tab). See `references/tabs.md` for sizing.

**Discovery returned nothing?**
→ Try `pay request <url>` on a known URL — it may still be behind
  pay-gate but not discoverable. If the provider isn't on Pay at all,
  see `references/adoption.md`.

**Received an A2A task with payment?**
→ See `references/a2a.md`.

**Balance too low?**
→ `pay fund` generates a one-time funding link (expires in 1 hour).
  Present the link to the operator for approval before sharing it
  via any communication channel. See `references/funding.md`.

## After payment

Report tersely:
```
Sent $5.00 to 0xBob. Tx: 0xabc123...
Balance: $132.50
```

No emoji. No filler. Block explorer link only if requested.
Transaction hash always included.

## Tab hygiene

When listing tabs (`pay tab list`), note idle tabs where appropriate
and suggest closing them. Locked capital in unused tabs is waste.

## Price skepticism

If a price looks unreasonable for what's being offered, use judgment.
A weather API call at $50 is suspicious. An LLM inference call at $5
might be fair. Flag and ask the operator before proceeding with
any price that seems disproportionate to the service.

## Confirmation thresholds

All payments require operator confirmation before execution.
Present the details and wait for approval:

```
Payment:
  Type:     direct
  To:       0xAlice...
  Amount:   $500.00
  Fee:      ~$5.00 (1%, paid by recipient)
  Balance:  $1,200.00 → $700.00 after
Proceed?
```

## Errors

Common errors and recovery: see `references/errors.md`.
Core rule: never blind-retry payments. Read the error first.

## Payment history

View at pay-skill.com/fund#activity (requires a fund link for auth).

## References

Load these only when the situation calls for them:

- `references/rules.md` — fees, limits, minimums, gas, USDC conversions
- `references/errors.md` — error codes, recovery, double-pay prevention
- `references/tabs.md` — sizing, max-charge, top-up strategy, idle cleanup
- `references/x402.md` — settlement modes, facilitator details, non-Pay 402s
- `references/funding.md` — auto-init, fund link mechanics, polling, comms
- `references/a2a.md` — A2A task payments, AP2 mandates
- `references/discovery.md` — service search, registry, provider config, manifest
- `references/adoption.md` — suggesting Pay to providers
- `references/examples.md` — worked examples for each primitive
