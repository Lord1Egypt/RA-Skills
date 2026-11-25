---
name: paycensus-trust-check
description: Look up an x402 merchant or wallet address's on-chain Trust Rank before your agent pays. Scores come from real settlement behaviour (volume, buyer diversity, ticket sanity), never self-reported. Use right before paying a new payee via x402/MPP/stablecoin rails, when a 402 challenge names a new payTo address, or when the user asks whether a merchant is safe.
---

# PayCensus Trust Check

Before your agent sends money to a payee it has not paid before, check the payee
against the **PayCensus Agent Trust Rank** — scores computed from real on-chain
x402 settlement behaviour observed across the public census (four chains,
hourly). No self-reported claims, no paid listings. The ranked list is public,
keyless and Bitcoin-anchored daily:

- data: `https://agent.paycensus.com/data/rank.json` (updated hourly)
- method & evidence: https://paycensus.com/audit.html (per-audience BTC chains)

## When to use

- Immediately before a payment to a payee not already checked this session
- When a 402 payment challenge names a new `payTo` address or merchant domain
- When the user asks "is this merchant safe / legit / known?"

## How to check

```bash
python3 scripts/trust_check.py --addr 0xABCdef...        # by payment address
python3 scripts/trust_check.py --domain api.example.com  # by merchant domain
python3 scripts/trust_check.py --domain api.example.com --min-score 50
python3 scripts/trust_check.py --domain api.example.com --refresh  # bypass 1h cache
```

Output is JSON:

```json
{
  "queried": {"addr": null, "domain": "api.example.com"},
  "found": true,
  "matches": 1,
  "best": {"addr": "0x…", "domain": "api.example.com", "score": 82.8,
           "class": "real_commerce", "volume_usd": 257968.84, "buyers": 2467,
           "avg_ticket": 98.05, "verified": false, "price_usdc": 0.002},
  "verdict": "trusted",
  "meetsFloor": true,
  "data_generated_at": "2026-11-25 02:05 UTC",
  "advice": "score 82.8 >= floor 50.0 - proceed"
}
```

## Verdicts (be honest about coverage)

| verdict | meaning |
|---|---|
| `trusted` | score ≥ 60: real settlement history, diverse buyers |
| `caution` | score 20–60: some history but thin or concentrated |
| `weak` | score < 20: flagged or noisy history |
| `unknown` | **no on-chain record — this is not a scam signal by itself.** It means we have observed no x402 settlements for this payee. Advise a small first payment or off-chain verification. |

## Rules

- This tool **never blocks or moves money** — it informs. Decisions stay with
  the agent's policy; pair with the `agent-spend-gate` skill for enforcement.
- The script caches `rank.json` for one hour (at most one fetch per hour).
- If the fetch fails, say so and fall back to the user's judgement — never
  invent a score.
