"""WC Group Repricer — main entrypoint.

Market-dynamics Groups skill: repricing timing + group-set coherence (Elo as tiebreak anchor).
Sim/paper by default; --live and --dry-run are mutually exclusive. One pass per run (cron-managed).
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simmer_sdk import SimmerClient  # noqa: E402

import state as st                    # noqa: E402
from discovery import discover, format_report, is_confirmed_exclusive  # noqa: E402
from strategy import config, repricing_decisions, coherence_decision, ask_price  # noqa: E402

SKILL_SLUG = "polymarket-worldcup-group-repricer"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"


def _trade(client, signal=None, **kw):
    """trade() with signal_data when the SDK supports it (0.9.17+); graceful without."""
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


def execute(client, market, side, amount, venue, reason, live, cfg, signal=None):
    """Guarded execution: exposure cap + slippage gate + fill-debited state. Raw prices to SDK."""
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


def exit_position(client, market, price, venue, reason, live, signal=None):
    with st.locked_state(live) as s:
        pos = s["positions"].get(market.id)
        if not pos or pos["status"] != "open":
            return "no open position"
        r = _trade(client, signal=signal, market_id=market.id, side="no", amount=pos["cost"],
                   venue=venue, source=TRADE_SOURCE, skill_slug=SKILL_SLUG, reasoning=reason)
        if not getattr(r, "success", False):
            return f"exit failed: {getattr(r, 'error', None) or '?'}"
        st.close_position(s, market.id, proceeds=getattr(r, "cost", 0.0) or 0.0)
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
    print(f"WC Group Repricer — {mode} — venue={venue}\n")
    # Dry-run still goes through the SDK paper engine (live=False), never a stub.
    client = SimmerClient.from_env(venue=venue) if live else \
        SimmerClient.from_env(venue=venue, live=False)

    disc = discover(client)
    print(format_report(disc))
    print()

    # Trade ACTIVE legs only. Importable candidates are surfaced in the report above but are NEVER
    # sent to the execution path — they aren't tradeable until Simmer imports + prices them.
    groups = {letter: [e["raw"] for e in g["active"]]
              for letter, g in disc["groups"].items() if g["active"]}
    if not groups:
        print("No active group-winner legs to trade "
              "(see importable candidates above — pending Simmer import).")
        return
    with st.locked_state(live) as s:
        held = {k for k, v in s["positions"].items() if v["status"] == "open"}

    for letter, legs in sorted(groups.items()):
        print(f"Group {letter}: {len(legs)} legs")
        entries, exits = repricing_decisions(legs, held, cfg)
        for m, p, reason in exits:
            sig = {"signal_source": "repricing_exit", "group": letter, "probability": round(p, 4),
                   "exit_reprice": cfg["EXIT_REPRICE"], "confidence": 0.7}
            err = exit_position(client, m, p, venue, reason, live, signal=sig)
            print(f"  {'~ EXIT ' if not err else '! EXIT skipped: ' + err:40s} {m.question[:60]!r}")
        for m, p, reason in entries:
            sig = {"signal_source": "repricing_entry", "group": letter, "probability": round(p, 4),
                   "entry_max_ask": cfg["ENTRY_MAX_ASK"], "confidence": 0.6}
            err = execute(client, m, "yes", cfg["MAX_TRADE_USD"],
                          venue, reason, live, cfg, signal=sig)
            print(f"  {'+ ENTRY' if not err else '- entry skipped: ' + err:40s} {m.question[:60]!r}")

        if is_confirmed_exclusive(legs):
            dec = coherence_decision(legs, cfg)
            if dec:
                m, side, my_prob, reason = dec
                price = ask_price(m) or 0.0
                sig = {"signal_source": "coherence", "group": letter,
                       "edge": round(abs(my_prob - price), 4), "probability": round(price, 4),
                       "min_coherence_gap": cfg["MIN_COHERENCE_GAP"], "confidence": 0.65}
                err = execute(client, m, side, cfg["MAX_TRADE_USD"], venue, reason, live, cfg,
                              signal=sig)
                print(f"  {'+ COHER' if not err else '- coherence skipped: ' + err:40s} {side.upper()} "
                      f"{m.question[:50]!r}")
        else:
            print(f"  ALERT [unconfirmed-set] Group {letter} has {len(legs)} visible legs — "
                  f"NOTE: mutual exclusivity unconfirmed from text; alert only, no arb.")


def main():
    ap = argparse.ArgumentParser(description="WC Group Repricer (Simmer skill)")
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
