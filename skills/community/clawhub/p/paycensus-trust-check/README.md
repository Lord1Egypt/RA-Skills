# paycensus-trust-check

**Look up an x402 merchant's on-chain Trust Rank before your agent pays.**

Scores are computed by the PayCensus census from **real on-chain settlement
behaviour** across four chains (Base, Arbitrum, Polygon, Solana) — volume,
buyer diversity, ticket sanity, identity verification — never self-reported,
never paid placement. The ranked list is public, keyless, and Bitcoin-anchored
daily via OpenTimestamps.

## Why

x402's supply side exploded in 2026: thousands of machine-payable endpoints,
zero identity layer, and an agent about to pay a `payTo` address it has never
seen. This skill gives your agent a one-line risk check before the first
payment:

```
$ python3 scripts/trust_check.py --domain api.bitrefill.com
{
 "found": true,
 "best": {"domain": "api.bitrefill.com", "score": 82.8, "buyers": 2467,
          "volume_usd": 257968.84, "price_usdc": 0.002},
 "verdict": "trusted",
 "advice": "score 82.8: trusted"
}
```

`unknown` is honest: it means *no observed settlements*, not *scam*. The skill
says so explicitly and advises a small first payment.

## Install

**ClawHub (OpenClaw):** listed as `paycensus-trust-check`, or
`npx clawhub install paycensus-trust-check`

**Hermes Agent:** `npx skills add https://github.com/PayCensusLabs/openclaw-skill-paycensus-trust-check --skill paycensus-trust-check`

**Manual:** copy this folder into `~/.openclaw/skills/` (OpenClaw) or your
Hermes skills directory.

## Pairs with

[`agent-spend-gate`](https://github.com/PayCensusLabs/openclaw-skill-agent-spend-gate)
— enforcement layer (budgets, allowlists, approval thresholds, hash-chained
local audit). Trust check informs; gate decides.

## Data & evidence

- Data: https://agent.paycensus.com/data/rank.json (hourly, keyless)
- Scoring method: https://agent.paycensus.com/standard.html
- Tamper evidence: https://paycensus.com/audit.html (per-audience OpenTimestamps chains)
- Free tier for programmatic use; no key needed for this skill.

## License

MIT
