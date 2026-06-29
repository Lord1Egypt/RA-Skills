---
name: polymarket-coherence-arb
description: Detects logically-linked Polymarket markets that price incoherently (a mutually-exclusive, exhaustive set whose YES prices don't sum to ~1) and trades the cheap/rich legs back toward coherence. No external data — arbitrages Polymarket against itself. Exclusivity is confirmed from market text; unconfirmed sets are alerted, never arbed. Sim by default.
metadata:
  author: "Nick (@BridgeAISocial)"
  version: "0.1.0"
  displayName: "Polymarket Coherence Arb"
  difficulty: "intermediate"
---

# Polymarket Coherence Arb

Finds sets of related Polymarket markets that *should* satisfy a probability constraint but don't,
and trades the cheap/rich legs back toward coherence — **arbitraging Polymarket against itself**.

## The edge
No sharp book to outrun, **no external data**, low latency pressure. If the YES prices of a
complete, mutually-exclusive set sum materially above 1, the set is collectively overpriced (buy
**NO** on the richest leg); if materially below 1, it's underpriced (buy **YES** on the cheapest leg).

## What it actually trades (v0.1)
1. **Confirmed sets only.** The only relationship v0.1 confirms *from market text* is a complete
   FIFA "win Group X" set — exactly 4 legs, same group letter (2026 format). Mutual exclusivity is
   read from the text itself; if a set can't be confirmed (partial, mixed letters, advance/qualify
   wording) it is **alerted, never arbed**.
2. **Bring-your-own sets.** Set `COHERENCE_GROUPS` to trade explicit market-id groups you assert are
   mutually exclusive (e.g. a tournament/final ladder). Format:
   `"id1,id2,id3,id4; idA,idB,idC"` — `;` separates groups, `,` separates legs.
3. **Remix point.** `discover_sets()` in `discovery.py` is where you add other relationships
   (win-tournament ≤ reach-final, parlay consistency, etc.). The skill handles pricing, the
   coherence test, the context/exposure gates, and execution — you supply which markets are linked.

This is **not** the WC Group Repricer: there's no repricing-timing mechanism and no Elo tiebreak —
it's pure price-coherence, leg picked by price alone, generalizable beyond the World Cup.

## Safety rails
- **Sim-first.** Default venue is `$SIM`; real trading requires `--live` **and** `--venue polymarket`
  **and** a claimed, wallet-linked Simmer agent. `--live` and `--dry-run` are mutually exclusive.
- **Budget = open exposure**, not daily spend: new trades are rejected if
  `open_exposure + cost > DAILY_BUDGET_USD`. State updates are lock-protected (`fcntl.flock`), and
  live vs dry-run state live in separate files (`state_live.json` / `state_dry.json`).
- Dry-run never touches live state and routes through the SDK paper engine (`live=False`) rather
  than stubbing success.
- Prices are passed raw to the SDK (no pre-rounding); edges are computed vs the **ask** when the
  venue exposes one (falls back to mid on `$SIM` — see Known limitations).
- One position per market; every trade carries `skill_slug`, a public `reasoning` string, and
  `signal_data` (Autoresearch backtest-ready).

## Configuration (env — all knobs Autoresearch-mutable)
| Var | Default | Meaning |
|---|---|---|
| `TRADING_VENUE` | `sim` | `sim` or `polymarket` (with `--live`) |
| `MAX_TRADE_USD` | `20` | per-leg cap |
| `DAILY_BUDGET_USD` | `100` | open-exposure cap |
| `MIN_COHERENCE_GAP` | `0.05` | min `|sum−1|` on a confirmed set before acting |
| `MAX_SLIPPAGE_PCT` | `0.03` | skip legs whose context slippage exceeds this |
| `COHERENCE_GROUPS` | _(unset)_ | optional explicit market-id groups (see above) |

## Usage
```bash
python coherence_arb.py --dry-run            # default; sim paper pass
python coherence_arb.py --status             # show positions/exposure
python coherence_arb.py --live --venue polymarket   # real money (after sim record)
```
Requires `SIMMER_API_KEY`.

## Known limitations (v0.1)
1. `$SIM` (LMSR) has no order book — ask/spread/depth gates only bind on the real venue; sim
   validates *logic*, not microstructure. **Capturing this edge cleanly often needs near-simultaneous
   fills**, which `$SIM` cannot model — validate in `live=False` paper mode against real spreads.
2. Auto-discovery confirms only the WC "win Group X" set from text; the canonical WC tag/series slug
   is unverified upstream, so discovery may need the paginated sports-markets workaround at launch.
   Other relationships require `COHERENCE_GROUPS` or a `discover_sets()` remix.
3. Legs are entered one at a time, not atomically; partial-fill unwind is basic.
4. Inconsistencies are often small and short-lived — `MIN_COHERENCE_GAP` ships at a reasonable
   default and is meant to be tuned in sim / by Autoresearch, not trusted blindly.
5. Real-venue depth (L2) checks are a TODO hook; v0.1 uses the context slippage gate.

No performance claims are made or implied. This skill describes what it does, not what it returns.
