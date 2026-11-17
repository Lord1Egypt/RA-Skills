#!/usr/bin/env python3
"""
tank_forecast.py — propane grill-tank fuel forecasting from a bathroom scale.

Commands:
  weigh    Tank on the scale -> lb/g of propane left, hours of burn left
           to a 20% reserve floor, at your grill's total BTU.
  session  Per-cook consumption -> sessions per tank, weeks per tank,
           tanks/yr for a weekly routine.
  plan     Pre-party check: minimum scale weight needed before a cook
           of N hours for N guests, with re-fire margin + reserve.
  compare  Tank exchange vs refill: $/lb delivered, sessions per tank,
           annual cost at your actual usage.

Stdlib only. Offline. Weigh tanks outdoors; never store or check leaks
with an open flame — see references/tank-math.md for safety.
"""
import argparse
import json
import math
import sys

# ─── Physical constants (references/tank-math.md has the derivations) ───
BTU_PER_LB = 21_600        # energy in 1 lb of propane (LHV-ish common figure)
LB_PER_GAL = 4.24          # liquid propane density, lb per US gallon
G_PER_LB = 453.6           # 1 lb = 453.6 g (NOT 424 g — that's 4.24 lb/gal garbled)
EXCHANGE_FILL_LB = 15.0    # typical cage-swap fill (they rarely hand you 20 lb)
DEFAULT_TARE = 17.0        # stamped "TW" on most steel 20-lb cylinders
DEFAULT_FULL = 20.0        # nominal fuel capacity, lb
DEFAULT_RESERVE = 0.20     # keep 20% of nominal as the never-burn floor

ARGS = None  # set in main() so emit() can see --json


def fail(msg):
    """Domain error -> stderr + exit code 2 (argparse also exits 2 on bad flags)."""
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


def emit(data, lines):
    if ARGS and getattr(ARGS, "json", False):
        print(json.dumps(data, indent=2))
    else:
        print("\n".join(lines))


def burn_rate_lb_hr(btu):
    if btu <= 0:
        fail("--burner-btu must be positive (sum of the burners you actually light)")
    return btu / BTU_PER_LB


def session_fuel_lb(a):
    """Cook-session consumption model: preheat + duty-cycled cook time."""
    if a.hours <= 0:
        fail("--hours must be positive")
    if not 0.2 <= a.duty <= 1.0:
        fail("--duty must be 0.2-1.0 (manual grills ~1.0, thermostated ~0.6-0.7)")
    if a.preheat_min < 0:
        fail("--preheat-min cannot be negative")
    burn_time = a.preheat_min / 60.0 + a.hours * a.duty
    return burn_time * burn_rate_lb_hr(a.burner_btu), burn_time


# ─── weigh ───
def cmd_weigh(a):
    if a.tare_lb < 5 or a.tare_lb > 30:
        fail(f"--tare-lb {a.tare_lb} implausible (read the TW stamp; steel 20-lb ~17)")
    net_mode = a.current_lb <= a.tare_lb
    fuel = a.current_lb if net_mode else a.current_lb - a.tare_lb
    if fuel < 0:
        fail("fuel computed negative — check the scale reading and the TW stamp")
    rate = burn_rate_lb_hr(a.burner_btu)
    reserve = a.reserve_frac * a.full_lb
    usable = max(fuel - reserve, 0.0)
    hours_to_reserve = usable / rate
    hours_to_empty = fuel / rate
    pct = 100.0 * fuel / a.full_lb

    lines = [f"Tank weigh-in — tare {a.tare_lb:.1f} lb, reading {a.current_lb:.1f} lb"]
    if net_mode:
        lines.append(f"  (reading <= tare -> interpreted as NET fuel already tare-subtracted)")
    lines += [
        f"Fuel remaining:  {fuel:.2f} lb ({fuel * G_PER_LB:,.0f} g) = {pct:.0f}% of a "
        f"{a.full_lb:.0f} lb fill",
        f"Burn rate:       {rate:.2f} lb/hr at {a.burner_btu:,.0f} BTU "
        f"({rate * G_PER_LB:,.0f} g/hr)",
        f"Reserve floor:   {reserve:.1f} lb ({a.reserve_frac:.0%}) — scale reads "
        f"{a.tare_lb + reserve:.1f} lb there",
        "",
        f"Usable to reserve: {usable:.2f} lb -> {hours_to_reserve:.1f} hr of cooking",
        f"(to a dry tank, no reserve: {hours_to_empty:.1f} hr — never plan on this)",
    ]
    if fuel > a.full_lb:
        lines.append(f"NOTE: {fuel:.1f} lb exceeds the {a.full_lb:.0f} lb nominal fill — "
                     "verify tare; overfills are dangerous")
    if usable <= 0:
        lines.append("VERDICT: AT/BELOW RESERVE — swap or refill before the next cook")
    elif hours_to_reserve < 1:
        lines.append("VERDICT: LOW — under 1 hr left; carry a backup for any real cook")
    elif hours_to_reserve < 2.5:
        lines.append("VERDICT: one normal weeknight cook left, not a party")
    else:
        lines.append(f"VERDICT: healthy — covers a {hours_to_reserve / 2:.0f}-hr "
                     "smoke with room to spare" if hours_to_reserve > 6
                     else "VERDICT: enough for several typical cooks")
    emit({
        "fuel_lb": round(fuel, 2), "fuel_g": round(fuel * G_PER_LB), "pct_full": round(pct),
        "burn_rate_lb_hr": round(rate, 3), "reserve_lb": round(reserve, 2),
        "usable_lb": round(usable, 2), "hours_to_reserve": round(hours_to_reserve, 2),
        "hours_to_empty": round(hours_to_empty, 2), "net_input": net_mode,
    }, lines)


# ─── session ───
def cmd_session(a):
    if a.sessions_week <= 0:
        fail("--sessions-week must be positive")
    rate = burn_rate_lb_hr(a.burner_btu)
    sess_lb, burn_time = session_fuel_lb(a)
    reserve = a.reserve_frac * a.full_lb
    usable = a.full_lb - reserve
    sessions_per_tank = usable / sess_lb
    weeks_per_tank = sessions_per_tank / a.sessions_week
    annual_sessions = a.sessions_week * 52.0
    annual_lb = annual_sessions * sess_lb
    ex_sessions = (EXCHANGE_FILL_LB - reserve) / sess_lb

    lines = [
        f"Session model — {a.burner_btu:,.0f} BTU, {a.hours:g} hr cook, "
        f"{a.preheat_min:g} min preheat, duty {a.duty:.0%}",
        f"Burn time incl. preheat: {burn_time:.2f} hr at {rate:.2f} lb/hr",
        f"Fuel per session: {sess_lb:.2f} lb ({sess_lb * G_PER_LB:,.0f} g)",
        "",
        f"Full {a.full_lb:.0f} lb tank: {sessions_per_tank:.1f} sessions "
        f"(plan on {math.floor(sessions_per_tank)}) to the {a.reserve_frac:.0%} reserve",
        f"At {a.sessions_week:g} cooks/week: one tank lasts {weeks_per_tank:.1f} weeks",
        f"Annual: {annual_sessions:.0f} sessions = {annual_lb:,.0f} lb propane = "
        f"{annual_lb / a.full_lb:.1f} tank-equivalents, "
        f"{annual_lb / usable:.1f} refill trips (top-up at reserve)",
        f"Cage-exchange fills are ~{EXCHANGE_FILL_LB:.0f} lb: only "
        f"{ex_sessions:.1f} sessions per swap",
    ]
    emit({
        "fuel_per_session_lb": round(sess_lb, 2), "sessions_per_tank": round(sessions_per_tank, 2),
        "weeks_per_tank": round(weeks_per_tank, 2), "annual_lb": round(annual_lb, 1),
        "annual_tank_equivalents": round(annual_lb / a.full_lb, 1),
        "annual_refill_trips": round(annual_lb / usable, 1),
        "sessions_per_exchange_tank": round(ex_sessions, 2),
    }, lines)


# ─── plan ───
def cmd_plan(a):
    if a.cook_hours <= 0:
        fail("--cook-hours must be positive")
    if a.guests < 1:
        fail("--guests must be >= 1")
    if a.capacity < 1:
        fail("--capacity must be >= 1")
    rate = burn_rate_lb_hr(a.burner_btu)
    batches = math.ceil(a.guests / a.capacity)
    burn_time = a.preheat_min / 60.0 + a.cook_hours * batches
    fuel = burn_time * rate
    need = fuel * (1 + a.margin_pct / 100.0)
    reserve = a.reserve_frac * a.full_lb
    start_fuel = need + reserve
    start_scale = a.tare_lb + start_fuel
    pct = 100.0 * start_fuel / a.full_lb

    lines = [
        f"Cook plan — {a.cook_hours:g} hr for {a.guests} guests "
        f"(grate capacity {a.capacity} -> {batches} batch{'es' if batches > 1 else ''})",
        f"Burn time incl. {a.preheat_min:g} min preheat: {burn_time:.2f} hr at "
        f"{a.burner_btu:,.0f} BTU = {rate:.2f} lb/hr",
        f"Raw fuel: {fuel:.2f} lb  + {a.margin_pct:g}% re-fire/wind/holding margin "
        f"= {need:.2f} lb",
        f"Plus {a.reserve_frac:.0%} reserve ({reserve:.1f} lb, never plan past it): "
        f"{start_fuel:.2f} lb propane needed at ignition",
        "",
        f"GO if the scale shows >= {start_scale:.1f} lb "
        f"(= tare {a.tare_lb:.1f} + {start_fuel:.2f} lb fuel, {pct:.0f}% of a tank)",
        f"Equivalent net-fuel reading: >= {start_fuel:.1f} lb after tare subtraction",
    ]
    if pct > 100:
        lines.append(f"NOTE: {pct:.0f}% of one tank — stage a backup or a second tank")
    cur_fuel = None
    if a.current_lb is not None:
        cur_fuel = a.current_lb if a.current_lb <= a.tare_lb else a.current_lb - a.tare_lb
        ok = cur_fuel >= start_fuel
        lines += [
            "",
            f"Your tank: reading {a.current_lb:.1f} lb -> {cur_fuel:.2f} lb fuel. "
            + ("GO — enough fuel with margin." if ok else
               f"NO-GO — short by {start_fuel - cur_fuel:.1f} lb; swap/refill first."),
        ]
    emit({
        "batches": batches, "burn_time_hr": round(burn_time, 2),
        "fuel_lb": round(fuel, 2), "fuel_with_margin_lb": round(need, 2),
        "start_fuel_lb": round(start_fuel, 2), "start_scale_lb": round(start_scale, 1),
        "pct_of_tank": round(pct), "go": (None if a.current_lb is None else cur_fuel >= start_fuel),
    }, lines)


# ─── compare ───
def cmd_compare(a):
    for name, val in (("--exchange-cost", a.exchange_cost), ("--refill-cost", a.refill_cost)):
        if val <= 0:
            fail(f"{name} must be positive")
    rate = burn_rate_lb_hr(a.burner_btu)
    sess_lb, _ = session_fuel_lb(a)
    reserve = a.reserve_frac * a.full_lb
    ex_fill, rf_fill = a.exchange_fill_lb, a.refill_fill_lb
    ex_usable, rf_usable = ex_fill - reserve, rf_fill - reserve
    annual_lb = a.sessions_week * 52.0 * sess_lb
    ex_per_lb, rf_per_lb = a.exchange_cost / ex_fill, a.refill_cost / rf_fill

    # Scenario A (recommended): swap at the 20% reserve floor each time.
    ex_trips = annual_lb / ex_usable
    rf_trips = annual_lb / rf_usable
    cost_a_ex, cost_a_rf = ex_trips * a.exchange_cost, rf_trips * a.refill_cost
    # Scenario B (not recommended): run tanks to fumes before swapping.
    cost_b_ex = annual_lb / ex_fill * a.exchange_cost
    cost_b_rf = annual_lb / rf_fill * a.refill_cost
    save = cost_a_ex - cost_a_rf
    cheaper = "refill" if rf_per_lb < ex_per_lb else "exchange"

    lines = [
        f"Exchange vs refill — cage swap ${a.exchange_cost:g} for {ex_fill:.0f} lb vs "
        f"refill ${a.refill_cost:g} for {rf_fill:.0f} lb",
        f"Cost per delivered lb: exchange ${ex_per_lb:.2f} vs refill ${rf_per_lb:.2f} "
        f"-> {cheaper} is {(1 - min(ex_per_lb, rf_per_lb) / max(ex_per_lb, rf_per_lb)):.0%} cheaper",
        f"Sessions per tank: exchange {ex_usable / sess_lb:.1f} "
        f"(surrendering {reserve:.0f} lb of your leftover) vs refill {rf_usable / sess_lb:.1f}",
        "",
        f"Your usage: {a.sessions_week:g} x {a.hours:g} hr cooks/week at "
        f"{a.burner_btu:,.0f} BTU = {annual_lb:,.0f} lb propane/yr",
        f"Swap at the {a.reserve_frac:.0%} reserve (recommended):",
        f"  exchange: {ex_trips:.0f} swaps/yr = ${cost_a_ex:,.0f}/yr",
        f"  refill:   {rf_trips:.0f} fills/yr = ${cost_a_rf:,.0f}/yr   "
        f"-> refill saves ${save:,.0f}/yr",
        f"Run to fumes before swapping (not recommended): "
        f"${cost_b_ex:,.0f} vs ${cost_b_rf:,.0f}/yr",
        "",
        "Refill also gives: fresh 20 lb by weight, tank stays yours, no waiting in line.",
        "Exchange wins only on: dead/recert-expired tank (12-yr stamp), or 24/7 convenience.",
    ]
    emit({
        "exchange_per_lb": round(ex_per_lb, 2), "refill_per_lb": round(rf_per_lb, 2),
        "cheaper": cheaper,
        "sessions_per_exchange_tank": round(ex_usable / sess_lb, 2),
        "sessions_per_refill_tank": round(rf_usable / sess_lb, 2),
        "annual_lb": round(annual_lb, 1),
        "annual_cost_exchange": round(cost_a_ex), "annual_cost_refill": round(cost_a_rf),
        "annual_savings_refill": round(save),
        "annual_cost_exchange_to_fumes": round(cost_b_ex),
        "annual_cost_refill_to_fumes": round(cost_b_rf),
    }, lines)


def main():
    global ARGS
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="JSON instead of text")
    sub = ap.add_subparsers(dest="cmd", required=True)

    w = sub.add_parser("weigh", help="scale reading -> hours left to 20% reserve")
    w.add_argument("--tare-lb", type=float, default=DEFAULT_TARE, dest="tare_lb",
                   help="empty-tank weight, TW stamp (default 17)")
    w.add_argument("--current-lb", type=float, required=True, dest="current_lb",
                   help="scale reading with tank on it (or net fuel if <= tare)")
    w.add_argument("--burner-btu", type=float, default=36_000, dest="burner_btu",
                   help="SUM of burners you light (default 36000 = 3x12k)")
    w.add_argument("--full-lb", type=float, default=DEFAULT_FULL, dest="full_lb",
                   help="nominal fill (20; use 15 for a cage-exchange tank)")
    w.add_argument("--reserve-frac", type=float, default=DEFAULT_RESERVE, dest="reserve_frac",
                   help="never-burn floor fraction (default 0.20)")

    s = sub.add_parser("session", help="per-cook burn -> tanks and weeks")
    s.add_argument("--burner-btu", type=float, default=36_000, dest="burner_btu")
    s.add_argument("--hours", type=float, default=2.5, help="cook hours per session")
    s.add_argument("--sessions-week", type=float, default=2, dest="sessions_week")
    s.add_argument("--preheat-min", type=float, default=15, dest="preheat_min")
    s.add_argument("--duty", type=float, default=1.0,
                   help="burner duty cycle; thermostated grills 0.6-0.7")
    s.add_argument("--full-lb", type=float, default=DEFAULT_FULL, dest="full_lb")
    s.add_argument("--reserve-frac", type=float, default=DEFAULT_RESERVE, dest="reserve_frac")

    p = sub.add_parser("plan", help="pre-cook: minimum scale weight needed")
    p.add_argument("--cook-hours", type=float, required=True, dest="cook_hours")
    p.add_argument("--guests", type=int, default=8)
    p.add_argument("--capacity", type=int, default=8,
                   help="servings per batch your grate holds (default 8)")
    p.add_argument("--burner-btu", type=float, default=36_000, dest="burner_btu")
    p.add_argument("--preheat-min", type=float, default=15, dest="preheat_min")
    p.add_argument("--margin-pct", type=float, default=25, dest="margin_pct",
                   help="re-fire/wind/holding margin on top of raw fuel")
    p.add_argument("--tare-lb", type=float, default=DEFAULT_TARE, dest="tare_lb")
    p.add_argument("--current-lb", type=float, default=None, dest="current_lb",
                   help="optional: your scale reading now for GO/NO-GO")
    p.add_argument("--full-lb", type=float, default=DEFAULT_FULL, dest="full_lb")
    p.add_argument("--reserve-frac", type=float, default=DEFAULT_RESERVE, dest="reserve_frac")

    c = sub.add_parser("compare", help="exchange vs refill economics")
    c.add_argument("--exchange-cost", type=float, default=26.0, dest="exchange_cost")
    c.add_argument("--refill-cost", type=float, default=19.0, dest="refill_cost")
    c.add_argument("--exchange-fill-lb", type=float, default=EXCHANGE_FILL_LB,
                   dest="exchange_fill_lb", help="cage tanks are usually 15 lb")
    c.add_argument("--refill-fill-lb", type=float, default=20.0, dest="refill_fill_lb")
    c.add_argument("--burner-btu", type=float, default=36_000, dest="burner_btu")
    c.add_argument("--hours", type=float, default=2.5)
    c.add_argument("--sessions-week", type=float, default=2, dest="sessions_week")
    c.add_argument("--preheat-min", type=float, default=15, dest="preheat_min")
    c.add_argument("--duty", type=float, default=1.0)
    c.add_argument("--full-lb", type=float, default=DEFAULT_FULL, dest="full_lb")
    c.add_argument("--reserve-frac", type=float, default=DEFAULT_RESERVE, dest="reserve_frac")

    ARGS = ap.parse_args()
    {"weigh": cmd_weigh, "session": cmd_session, "plan": cmd_plan,
     "compare": cmd_compare}[ARGS.cmd](ARGS)


if __name__ == "__main__":
    main()
