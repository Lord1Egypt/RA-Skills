# Examples

Show real, working examples of what agents can do with lobster.cash. Each example has been verified end-to-end.

## When to use

- After setup completes and the user has no specific request.
- When the user asks "what can you do?" or "what can I buy?".
- Only show once per session — do not repeat if the user already saw it.

## Command

```
lobstercash examples
```

## Reading the output

Each example includes:

- `name` — example name
- `oneLiner` — short description
- `description` — how it works in a few lines
- `skillUrl` — link to the skill repo with full instructions

## Current examples

### xStocks

Buy tokenized stocks (Apple, Tesla, NVIDIA, S&P 500…) on Solana with USDC. The skill includes a local catalog of 104 tokens — no API calls needed to search or look up mint addresses. Purchases go through Jupiter swaps: the skill builds an unsigned transaction, lobster.cash signs it, and the agent owns fractional stock exposure on-chain.

Skill: https://github.com/manu-xmint/xstocks-skill

## How to present

Do not dump the raw output. Summarize conversationally:

"Here's something you can do right now:

- **Buy tokenized stocks** — trade Apple, Tesla, NVIDIA, and 100+ other stocks on Solana using USDC (xStocks)

Want to try it?"

## After the user picks

Once the user picks an example, check their balance (`lobstercash crypto balance`)
and proceed with the relevant skill. If they need funds, guide them to
the crypto request flow.
