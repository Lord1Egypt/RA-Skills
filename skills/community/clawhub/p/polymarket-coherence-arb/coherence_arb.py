"""Polymarket Coherence Arb — main entrypoint.

Trade incoherent, CONFIRMED mutually-exclusive market sets back toward sum=1. No external data:
arbitrages Polymarket against itself. Sim/paper by default; --live and --dry-run are mutually
exclusive. One pass per run (cron-managed).
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simmer_sdk import SimmerClient  # noqa: E402

import state as st                   # noqa: E402
from discovery import discover_sets  # noqa: E402

SKILL_SLUG = "polymarket-coherence-arb"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"


def config():
    g = os.getenv
    return {
        "MAX_TRADE_USD": float(g("MAX_TRADE_USD", "20")),
        "DAILY_BUDGET_USD": float(g("DAILY_BUDGET_USD", "100")),
        "MIN_COHERENCE_GAP": float(g("MIN_COHERENCE_GAP", "0.05")),  # min |sum-1| to act
        "MAX_SLIPPAGE_PCT": float(g("MAX_SLIPPAGE_PCT", "0.03")),
    }


def ask_price(market):
    """Trade against the ASK when the venue exposes one; $SIM (LMSR) only has a mid."""
    ask = getattr(market, "best_ask", None)
    return ask if ask else getattr(market, "current_probability", None)


def _trade(client, signal=None, **kw):
    """trade() with signal_data when the SDK supports it; graceful without."""
    if signal:
        try:
            return client.trade(signal_data=signal, **kw)
        except TypeError:
            pass                                   # older SDK: no signal_data kwarg
    return client.trade(**kw)


def slippage_blocks(client, market_id, my_prob, cfg):
    try:
        ctx = client.get_market_context(market_id, my_probability=my_prob)
    except Exception as exc:
        return f"context unavailable ({exc})"           # fail closed
    if (ctx.get("slippage", {}) or {}).get("slippage_pct", 0) > cfg["MAX_SLIPPAGE_PCT"]:
        return "slippage above gate"
    if "SEVERE" in str((ctx.get("trading", {}) or {}).get("flip_flop_warning") or ""):
        return "flip-flop warning"
    return None


def coherence_decision(legs, cfg):
    """A confirmed exclusive set should sum to ~1.
    Overpriced (sum>1) -> buy NO on the richest leg. Underpriced (sum<1) -> buy YES on cheapest.
    Returns (market, side, my_prob, total, gap, reason) or None when coherent within the gap."""
    priced = [(m, ask_price(m)) for m in legs]
    if any(p is None for _, p in priced):
        return None
    total = sum(p for _, p in priced)
    gap = total - 1.0
    if abs(gap) < cfg["MIN_COHERENCE_GAP"]:
        return None
    if gap > 0:                                           # collectively overpriced -> NO richest
        m, p = max(priced, key=lambda x: x[1])
        return (m, "no", max(0.0, 1 - p), total, gap,
                f"Set sums {total:.2f} (>1 by {gap:.0%}); richest leg {p:.2f} overpriced -> NO")
    m, p = min(priced, key=lambda x: x[1])                # underpriced -> YES cheapest
    return (m, "yes", min(1.0, p + abs(gap)), total, gap,
            f"Set sums {total:.2f} (<1 by {abs(gap):.0%}); cheapest leg {p:.2f} underpriced -> YES")


def execute(client, market, side, amount, venue, reason, live, cfg, signal=None):
    """Guarded execution: one-per-market + exposure cap + slippage gate + fill-debited state."""
    with st.locked_state(live) as s:
        if st.has_position(s, market.id):
            return "already positioned"
        if not st.exposure_allows(s, amount, cfg["DAILY_BUDGET_USD"]):
            return "exposure cap reached"
        block = slippage_blocks(client, market.id, None, cfg)
        if block:
            return block
        r = _trade(client, signal=signal, market_id=market.id, side=side, amount=amount,
                   venue=venue, source=TRADE_SOURCE, skill_slug=SKILL_SLUG, reasoning=reason)
        if not getattr(r, "success", False):
            return f"trade failed: {getattr(r, 'error', None) or getattr(r, 'skip_reason', '?')}"
        st.add_position(s, market.id, kind=side, side=side,
                        cost=getattr(r, "cost", amount) or amount,
                        price=getattr(r, "new_price", 0.0) or 0.0, reason=reason)
        return None


def show_status(live):
    with st.locked_state(live) as s:
        open_pos = {k: v for k, v in s["positions"].items() if v["status"] == "open"}
        print(f"mode={'LIVE' if live else 'DRY'}  open_exposure=${s.get('open_exposure_usd', 0):.2f}"
              f"  open_positions={len(open_pos)}")
        for mid, p in open_pos.items():
            print(f"  {mid}  {p['side'].upper()}  cost=${p['cost']:.2f}  entry={p['entry_price']:.2f}")


def run(venue, live):
    cfg = config()
    mode = "LIVE" if live else "DRY-RUN (paper)"
    print(f"Coherence Arb — {mode} — venue={venue}  gap>={cfg['MIN_COHERENCE_GAP']:.0%}\n")
    # Dry-run still goes through the SDK paper engine (live=False), never a stub.
    client = SimmerClient.from_env(venue=venue) if live else \
        SimmerClient.from_env(venue=venue, live=False)

    sets = discover_sets(client)
    if not sets:
        print("No confirmed mutually-exclusive sets found "
              "(pre-listing, none configured, or discovery gap — see SKILL.md).")
        return

    for label, legs in sets:
        priced = [(m, ask_price(m)) for m in legs]
        total = sum(p for _, p in priced if p is not None)
        print(f"{label}: {len(legs)} legs, YES sum {total:.3f}")
        dec = coherence_decision(legs, cfg)
        if not dec:
            print("  coherent within gap — no action")
            continue
        m, side, my_prob, total, gap, reason = dec
        sig = {"signal_source": "coherence", "set": label, "sum": round(total, 4),
               "incoherence": round(gap, 4), "min_coherence_gap": cfg["MIN_COHERENCE_GAP"],
               "probability": round(my_prob, 4), "confidence": 0.6}
        err = execute(client, m, side, cfg["MAX_TRADE_USD"], venue, reason, live, cfg, signal=sig)
        print(f"  {'+ TRADE ' + side.upper() if not err else '- skipped: ' + err:40s} "
              f"{m.question[:55]!r}")


def main():
    ap = argparse.ArgumentParser(description="Polymarket Coherence Arb (Simmer skill)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--live", action="store_true", help="real trading (claimed+linked agent)")
    mode.add_argument("--dry-run", action="store_true", help="paper pass via SDK engine (default)")
    ap.add_argument("--status", action="store_true", help="print positions/exposure and exit")
    ap.add_argument("--venue", default=os.getenv("TRADING_VENUE", "sim"),
                    help="sim (default) or polymarket")
    args = ap.parse_args()
    if args.status:
        show_status(live=args.live)
        return
    run(venue=args.venue, live=args.live)


if __name__ == "__main__":
    main()
