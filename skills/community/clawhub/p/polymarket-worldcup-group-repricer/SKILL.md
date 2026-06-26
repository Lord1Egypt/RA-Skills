---
name: polymarket-worldcup-group-repricer
description: World Cup Groups skill — a market-dynamics play on group-winner sets. Buys group favorites at pre-tournament prices and trims after qualification "becomes obvious" and casual money reprices (bet on the repricing, not the champion), plus trades incoherent group market sets back toward consistency. Sim by default.
metadata:
  author: "Nick (@BridgeAISocial)"
  version: "0.2.0"
  displayName: "WC Group Repricer"
  difficulty: "intermediate"
---

# WC Group Repricer

A **Groups**-category skill for the 2026 World Cup built on *market dynamics*, not winner-picking:

1. **Repricing timing** — enter group favorites at pre-tournament asks; exit after qualification
   becomes "obvious" and retail money reprices the leg up. "Obvious" is read **from the market
   itself** (the leg crossing a configured price threshold) — no sports model required.
   *(Strategy family credit: group-stage repricing ideas circulating on X.)*
2. **Group-set coherence** — within a group's winner set (mutually exclusive, exhaustive), trade
   prices that sum incoherently back toward 1. Mutual exclusivity is **confirmed from market text**
   (a complete 4-leg group-winner set — "win Group X" *or* "finish first in Group X") — if it can't
   be confirmed, the set is alerted, never arbed.
3. **Elo anchor (tiebreak only)** — a static Elo table decides *which* leg of an incoherent set is
   the mispriced one. It never picks winners standalone.

## Safety rails
- **Sim-first.** Default venue is `$SIM`; real trading requires `--live` *and* `--venue polymarket`
  *and* a claimed, wallet-linked Simmer agent. `--live` and `--dry-run` are mutually exclusive.
- **Budget = open exposure**, not daily spend: new trades are rejected if
  `open_exposure + cost > DAILY_BUDGET_USD`. State updates are lock-protected (`fcntl.flock`).
- Dry-run never touches live state (separate `state_dry.json`) and routes through the SDK paper
  engine rather than stubbing success.
- Prices are passed raw to the SDK (no pre-rounding); edges are computed vs the **ask** when the
  venue exposes one (falls back to mid on `$SIM` — see Known limitations).
- One position per market; every trade carries `skill_slug` + a public `reasoning` string.

## Configuration (env — all knobs Autoresearch-mutable)
| Var | Default | Meaning |
|---|---|---|
| `TRADING_VENUE` | `sim` | `sim` or `polymarket` (with `--live`) |
| `MAX_TRADE_USD` | `5` | per-leg cap |
| `DAILY_BUDGET_USD` | `50` | open-exposure cap |
| `ENTRY_MAX_ASK` | `0.55` | buy a group favorite only at/below this |
| `EXIT_REPRICE` | `0.78` | trim a held leg at/above this |
| `MIN_COHERENCE_GAP` | `0.05` | min `|sum−1|` on a confirmed 4-leg set |
| `MAX_SLIPPAGE_PCT` | `0.03` | skip legs whose context slippage exceeds this |

## Usage
```bash
python scripts/group_repricer.py --dry-run            # default; sim paper pass
python scripts/group_repricer.py --status             # show positions/exposure
python scripts/group_repricer.py --live --venue polymarket   # real money (after sim record)
```
Requires `SIMMER_API_KEY`.

## Known limitations (v0.1)
1. `$SIM` (LMSR) has no order book — ask/spread/depth gates only bind on the real venue; sim
   validates *logic*, not microstructure.
2. Discovery is **two-source**: the active Simmer venue (tradeable today) *and* the importable
   upstream pool (`list_importable_markets`). Group-winner markets live upstream until Simmer
   imports them, so importable candidates are **surfaced in the report but never traded** — they
   only become tradeable once imported + priced. (Simmer's WC auto-importer hasn't imported the
   group-winner event yet — likely an upstream `fifa-world-cup` tag mismatch, tracked Simmer-side;
   until then the skill shows candidates without trading them.)
3. Coherence legs are entered sequentially, not atomically; partial-fill unwind is basic.
4. The exit threshold (`EXIT_REPRICE`) is the strategy's most sensitive knob — it ships at a
   reasonable default and is meant to be tuned in sim / by Autoresearch, not trusted blindly.
5. Real-venue depth (L2) checks are a TODO hook; v0.1 uses the context slippage gate.
6. Platform per-leg stop-losses can fire on temporarily-down legs of a coherent set — review
   auto-risk settings before running live.

No performance claims are made or implied. This skill describes what it does, not what it returns.
