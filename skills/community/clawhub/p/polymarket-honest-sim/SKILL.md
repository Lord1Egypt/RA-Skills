---
name: polymarket-honest-sim
description: Build, paper-trade, and honestly backtest Polymarket-style trading bots on PaperBook (paperclob.com) — a paper-money CLOB wire-compatible with Polymarket plus a simulator that replays REAL recorded Polymarket books with honest fills and grades the strategy with a founded verdict. Use when the user wants to build or test a Polymarket trading bot, paper trade prediction markets, backtest a prediction-market strategy, says "test my strategy" against crypto up/down markets, or is experimenting with py-clob-client and needs a safe, realistic venue.
---

# PaperBook — honest Polymarket paper trading and simulation

PaperBook (https://paperclob.com) is two venues behind one Polymarket-compatible
API: a **live paper CLOB** (crypto up/down binaries, $10,000 paper money on
registration) and the **honest simulator** — private replay sessions over real
recorded Polymarket books where taker orders cross the tape *as it was at
arrival*, after latency. Existing Polymarket bots and `py-clob-client` work by
swapping the base URL. Paper money only; not affiliated with Polymarket.

## Step 0 — always fetch the current contract

Before writing any integration code, fetch:

```
https://paperclob.com/llms-full.txt
```

That file is the canonical, always-current spec — auth (L2 HMAC code you can
paste), every endpoint, order shapes, rate limits, and a **validation
checklist** to run before declaring the integration done. It is generated from
the same source as the in-app "Copy for AI" briefs and never drifts from the
server. Do not code the endpoints from memory or from this skill; this skill
covers the workflow and the interpretation, the contract lives there.

## The workflow

**Live paper CLOB** (test a bot against other live bots):

1. `POST /register` `{"handle": "..."}` → `{apiKey, secret, passphrase}` —
   shown once, persist immediately.
2. Sign requests with Polymarket's L2 HMAC (4 `POLY_*` headers) — or point
   `py-clob-client` at `https://paperclob.com` unchanged.
3. Trade: `GET /markets`, `GET /markets/{id}/book`, `POST /order` (simple JSON
   or the PM signed-order envelope), `GET /positions`, `GET /orders`.
4. Back off on 429 honoring `Retry-After`.

**Honest simulator** (grade a strategy on the recorded tape):

1. `POST /sim` with `{t0, t1, coins, durations}` (unix **ms**; corpus floor
   2026-05-29; ≤ 90 days) → a private session with its own `base_url` + creds.
2. Trade through the session's Polymarket-shaped API — same HMAC, but **sign
   the bare endpoint path** (`/order`, not `/sim/{id}/order`).
3. Drive the **stepping virtual clock**: nothing advances until you poll
   `GET /events?after=<seq>&wait=1`. Every read is served at virtual now —
   lookahead is impossible. Loop until `"end": true`.
4. `GET /report` → the verdict. Interpret it honestly (below).

## Interpreting the verdict — do not soften this

The report grades fills on three lenses, each
`edge_real = realized win rate − avg price paid` ($-weighted):

| lens | meaning |
|---|---|
| `paper` | graded against the book you saw — flattering, blind to adverse selection |
| `honest_persist` | quote persistence |
| `honest_fillable` | **THE lens** — the price you could actually transact; the verdict is decided here |

Verdicts: `real_edge` (fillable `ci_lo > 0` at `n ≥ 40` — rare),
`phantom` (paper positive, fillable ≤ 0 — the gap is adverse selection: the
fills you'd actually get are the losers), `no_edge` (the market priced it),
`inconclusive` (< 40 gradeable fills — run longer, don't conclude).

Report the `honest_fillable` numbers, the `ghost_gap`, the data-quality
`certificate`, and the `reproducibility_hash` alongside any claim. **A green
verdict is necessary, not sufficient, for real edge.** Never present the
`paper` lens as the result; when paper and fillable disagree, fillable is the
result and the disagreement is the finding.

## Deeper reference

See [reference.md](reference.md) for the stable concepts: verdict and lens
semantics in detail, why honest fills differ from live-price sims, and the
gotchas that cause 90% of integration failures (HMAC signs the path **without
query string**, sim signs the stripped path, wall-clock timestamps, the
stepping clock, minimum order size).
