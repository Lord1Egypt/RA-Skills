---
name: predge-settlement-risk
description: Pre-trade check of a Polymarket market's UMA settlement state on Polygon (disputes, UMA vote, proposal window, bulletin board). Observe-only.
metadata:
  author: "Predge (hello@predge.io)"
  version: "0.1.0"
  displayName: "Settlement-Risk Check (UMA on-chain)"
  difficulty: "beginner"
  attribution: "Vendor-authored by Predge. The data is UMA's own on-chain state; Predge reads, labels and signs it."
  simmer:
    credit: {name: "Predge", url: "https://predge.io", label: "by"}
    links: [https://api.predge.io/v1/settlement-risk/4424722, https://data.predge.io/samples/settlement-risk, https://api.predge.io/.well-known/predge-keys.json]
tags: [polymarket, uma, risk, pre-trade]
---
# Settlement-Risk Check (UMA on-chain)

> **This is a template.** Framework, not a production trading system. Read [DISCLAIMER.md](./DISCLAIMER.md).
> **Observe-only:** it places no orders, real-money or paper. Default gate: skip on `caution`, half size on `watch`, full size only on `ok`.
> **Vendor-authored** by [Predge](https://predge.io). The facts are UMA's own on-chain state; Predge reads, labels and signs them.

Before your strategy enters a Polymarket market, ask whether the market's resolution is contested on chain right now. One free call, no API key, no wallet:

```
GET https://api.predge.io/v1/settlement-risk/<market>
    <market> = Polymarket condition id (0x + 64 hex), numeric market id, or slug
```

## What you get

Read live from UMA's Optimistic Oracle and Polymarket's UMA CTF adapter on Polygon:

| field | meaning |
|---|---|
| `open_dispute` | a dispute is open on the current proposal, or the outcome is in a UMA vote |
| `dispute_count` | 0, 1 or 2. A first dispute resets the question for a new proposal |
| `sent_to_uma_vote` | disputed twice: the outcome goes to a UMA token-holder vote |
| `current_proposal` | proposed outcome, proposal time, end of the challenge window |
| `disputes[]` | time, tx and disputed proposal of each dispute |
| `bulletin_board.latest` | latest bulletin-board update (clarification, early-resolution notice, schedule notice, dispute notice, title fix), its time and poster |
| `onchain_resolution` | the final outcome, once UMA has resolved it on chain |
| `risk_level` | `ok`, `watch`, `caution` or `resolved` |
| `recommendation` | one line, e.g. `caution: disputed twice, the outcome goes to a UMA token-holder vote, second dispute 8.2 h ago; median 88.5 h from a second dispute to on-chain resolution` |
| `attestation` | ed25519 signature by Predge's published key `13fa3d18a369e6c7` |

## Why it matters (verified, 1 Jan to 2 Oct 2026, Polymarket on Polygon)

- 3,005 disputes on 2,666 markets; 323 markets were disputed twice or more, which sends the outcome to a UMA vote.
- Of 2,543 settled disputed markets, 853 (33.5%) settled differently from the disputed proposal.
- Median time to on-chain resolution: 3.3 h after a first dispute, 88.5 h after a second dispute.

A dispute blocks a proposal; it does not by itself change the outcome. What it does change is when your position settles and how sure the outcome is.

## Gate logic

| risk_level | when | default gate |
|---|---|---|
| `caution` | disputed once or twice, open dispute, or resolution paused | skip (`contested_resolution`) |
| `watch` | a proposal is in its challenge window, or a bulletin-board update in the last 72 h | allow at `watch_size_factor` (0.5) |
| `ok` | no proposal, dispute or recent bulletin-board update | allow at 1.0 |
| `resolved` | on-chain resolution is final | skip (`already_resolved`) |
| no record | API or network error | skip (`state_unavailable`), fails closed |

Tune in `config.json`: `block_on_caution` (true), `watch_size_factor` (0.5), `block_resolved` (true).

## Run it

```bash
python settlement_risk_check.py --demo                        # bundled real records, no network
python settlement_risk_check.py 4424722 601819                # live, no keys needed
python settlement_risk_check.py --simmer-market <market-uuid> # resolves via SimmerClient (SIMMER_API_KEY)
python settlement_risk_check.py 4424722 --json                # raw signed record
```

## Use it from your own skill

```python
from settlement_risk_check import check

record, decision = check(market.polymarket_condition_id)
if not decision.allowed:
    print("skip:", decision.reason, decision.recommendation)
    return  # do NOT fall through to sizing
amount = size_position(p_win, price, bankroll) * decision.size_factor
```

Pair it with `client.get_market_context(...)` and your own `p_win`. This gate decides trade or skip on settlement state only; it does not estimate edge.

## Limits

- Polymarket markets only (needs a Polymarket condition id; Kalshi markets are out of scope).
- Each record is a live chain read at `checked_at`, cached up to 60 s. Rate limit 60 checks per minute per IP.
- Bulletin-board kinds are a text heuristic. Only the question creator's and Polymarket operator accounts' posts are counted.
- `risk_level` and `recommendation` are Predge's reading of the facts, not advice.
