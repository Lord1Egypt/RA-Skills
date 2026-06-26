"""Strategy logic: repricing entry/exit + group-set coherence, Elo as tiebreak anchor only.

All thresholds come from env config (Autoresearch-mutable). Functions are small on purpose so the
experiment loop can mutate them safely.
"""

import os


def config():
    g = os.getenv
    return {
        "MAX_TRADE_USD": float(g("MAX_TRADE_USD", "5")),
        "DAILY_BUDGET_USD": float(g("DAILY_BUDGET_USD", "50")),
        "ENTRY_MAX_ASK": float(g("ENTRY_MAX_ASK", "0.55")),
        "ENTRY_MIN_FAV": float(g("ENTRY_MIN_FAV", "0.35")),   # leg must already lead its group
        "EXIT_REPRICE": float(g("EXIT_REPRICE", "0.78")),
        "MIN_COHERENCE_GAP": float(g("MIN_COHERENCE_GAP", "0.05")),
        "MAX_SLIPPAGE_PCT": float(g("MAX_SLIPPAGE_PCT", "0.03")),
    }


def ask_price(market):
    """Trade against the ASK when the venue exposes one; $SIM (LMSR) only has a mid."""
    ask = getattr(market, "best_ask", None)
    return ask if ask else getattr(market, "current_probability", None)


# --- Elo anchor (tiebreak ONLY — never a standalone winner-pick) -------------------------------
ELO = {
    "Spain": 2080, "France": 2100, "Argentina": 2140, "England": 2030, "Brazil": 2030,
    "Portugal": 2000, "Netherlands": 1990, "Germany": 1960, "Belgium": 1900, "Croatia": 1880,
    "Italy": 1880, "Uruguay": 1880, "Colombia": 1860, "Morocco": 1850, "USA": 1790,
    "Mexico": 1760, "Japan": 1840, "Korea": 1780, "Senegal": 1790, "Switzerland": 1830,
}


def elo_lean(question):
    """Rough anchor score for a 'win Group X' leg from the team named in the question."""
    q = question or ""
    for team, rating in ELO.items():
        if team.lower() in q.lower():
            return rating
    return 0  # unknown team -> no lean


def repricing_decisions(legs, held_ids, cfg):
    """Mechanism 1 — the headline repricing play.
    ENTRY: group favorite (highest-priced leg) if it leads clearly and ask <= ENTRY_MAX_ASK.
    EXIT:  any held leg whose price >= EXIT_REPRICE ('qualification obvious', casual money in).
    Returns (entries, exits) as (market, price, reason) tuples."""
    entries, exits = [], []
    priced = [(m, ask_price(m)) for m in legs]
    priced = [(m, p) for m, p in priced if p is not None]
    if not priced:
        return entries, exits

    for m, p in priced:                                   # exits first — they free exposure
        if m.id in held_ids and p >= cfg["EXIT_REPRICE"]:
            exits.append((m, p, f"Leg repriced to {p:.2f} >= exit {cfg['EXIT_REPRICE']:.2f} "
                                f"after qualification became market-obvious -> trim"))

    fav, fav_p = max(priced, key=lambda x: x[1])
    if (fav.id not in held_ids and cfg["ENTRY_MIN_FAV"] <= fav_p <= cfg["ENTRY_MAX_ASK"]):
        entries.append((fav, fav_p, f"Group favorite at pre-tournament ask {fav_p:.2f} "
                                    f"(<= {cfg['ENTRY_MAX_ASK']:.2f}); bet on the repricing, "
                                    f"not the champion"))
    return entries, exits


def coherence_decision(legs, cfg):
    """Mechanism 2 — confirmed-exclusive 4-leg set should sum to ~1.
    Underpriced set -> buy YES on the leg the Elo anchor leans to among the cheap legs.
    Overpriced set -> buy NO on the leg the anchor leans AGAINST among the rich legs.
    Returns (market, side, my_prob, reason) or None."""
    priced = [(m, ask_price(m)) for m in legs]
    if any(p is None for _, p in priced):
        return None
    total = sum(p for _, p in priced)
    gap = total - 1.0
    if abs(gap) < cfg["MIN_COHERENCE_GAP"]:
        return None
    if gap < 0:                                            # set underpriced -> buy best YES
        m, p = max(priced, key=lambda x: (elo_lean(x[0].question), -x[1]))
        return (m, "yes", p + abs(gap),
                f"Group set sums {total:.2f} (<1 by {abs(gap):.0%}); Elo-anchored leg at {p:.2f} "
                f"is the underpriced one -> YES")
    m, p = min(priced, key=lambda x: (elo_lean(x[0].question), -x[1]))
    return (m, "no", max(0.0, p - gap),
            f"Group set sums {total:.2f} (>1 by {gap:.0%}); anchor leans against this leg "
            f"at {p:.2f} -> NO")
