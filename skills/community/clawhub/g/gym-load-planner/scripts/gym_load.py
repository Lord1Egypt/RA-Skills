#!/usr/bin/env python3
"""Gym Load Planner — 1RM estimation, %-1RM tables, progression blocks,
plate math, and a progress log with next-session load suggestions.

Stdlib-only.
"""
import argparse
import json
import math
import os
import sys
from datetime import date

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gym_log.json")

LBS = "lb"
KG = "kg"


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def epley(w, r):
    return w * (1 + r / 30.0)


def brzycki(w, r):
    return w * 36.0 / (37.0 - r) if r < 37 else float("inf")


def round25(x, unit=KG):
    step = 2.5 if unit == KG else 5.0
    return round(x / step) * step


# ---------------------------------------------------------------- one-rm
def cmd_one_rm(args):
    if args.reps < 1 or args.reps > 20:
        die("reps must be 1..20")
    if args.reps == 1:
        print(f"That IS your 1RM: {args.weight:g} {args.unit}")
        return
    e, b = epley(args.weight, args.reps), brzycki(args.weight, args.reps)
    mean = (e + b) / 2
    spread = abs(e - b) / mean * 100
    print(f"Set: {args.weight:g} {args.unit} x {args.reps}")
    print(f"Epley:    {e:.1f} {args.unit}")
    print(f"Brzycki:  {b:.1f} {args.unit}")
    print(f"Mean e1RM: {mean:.1f} {args.unit}")
    if args.reps > 12:
        print("CAUTION: reps > 12 — estimate error grows fast; treat as rough.")
    elif spread > 5:
        print(f"Formulas disagree by {spread:.1f}% — estimate uncertain.")
    else:
        print(f"Formulas agree within {spread:.1f}% — good estimate.")
    print()
    print("Rep-max predictions from the mean e1RM:")
    for r in (3, 5, 8, 10, 12):
        w = mean / (1 + r / 30.0)
        print(f"  {r:>2}RM  {round25(w, args.unit):g} {args.unit}")


# ---------------------------------------------------------------- table
ZONES = {
    "strength": (0.80, 0.90, "3-6", "3-5 min", "3-5"),
    "hypertrophy": (0.65, 0.80, "8-12", "1.5-3 min", "3-4"),
    "endurance": (0.50, 0.65, "15-20", "60-90 s", "2-3"),
}


def cmd_table(args):
    if args.goal not in ZONES:
        die(f"goal must be one of {list(ZONES)}")
    lo, hi, reps, rest, sets = ZONES[args.goal]
    orm = args.one_rm
    print(f"Loading table — goal {args.goal} (from e1RM {orm:g} {args.unit})")
    print()
    print(f"{'%1RM':<7}{'Weight':<10}{'Reps':<8}{'Sets':<6}Rest")
    print("-" * 42)
    for pct in [hi, hi - 0.05, (hi + lo) / 2, lo + 0.05, lo]:
        w = round25(orm * pct, args.unit)
        label = "peak" if pct == hi else ("light" if pct == lo else "")
        print(f"{pct*100:.0f}%{'':<3}{w:<10g}{reps:<8}{sets:<6}{rest}  {label}")
    print()
    print("Start mid-zone, progress toward the peak column over 3 weeks,")
    print("then deload (plan command schedules this).")


# ---------------------------------------------------------------- plan
def cmd_plan(args):
    if args.goal not in ZONES:
        die(f"goal must be one of {list(ZONES)}")
    lo, hi, reps, rest, sets = ZONES[args.goal]
    n_sets = int(sets.split("-")[0])
    reps_top = args.top_reps or int(reps.split("-")[1].split("-")[0]
                                    if "-" in reps.split("-")[1] else reps.split("-")[1])
    print(f"{args.weeks}-week {args.goal} block — e1RM {args.one_rm:g} {args.unit}, "
          f"+{args.increment:g} {args.unit}/session progression")
    print()
    print(f"{'Week':<6}{'Load':<10}{'Reps x sets':<14}Note")
    print("-" * 48)
    # wave structure: 3 load weeks + 1 deload
    load = round25(args.one_rm * (lo + hi) / 2, args.unit)
    sessions_per_week = 2
    for wk in range(1, args.weeks + 1):
        if wk % 4 == 0:
            dl = round25(load * 0.90, args.unit)
            print(f"W{wk:<5}{dl:<10g}{max(3, reps_top-2)} x {n_sets:<8}DELOAD -10%")
            continue
        # two sessions per week, each +increment if planned linear
        l1 = load
        l2 = round25(load + args.increment, args.unit)
        print(f"W{wk:<5}{l1:<10g}{reps_top} x {n_sets:<8}"
              f"+{args.increment:g} to {l2:g} on second session")
        load = round25(l2 + args.increment, args.unit)
    print()
    print("Rule: only add weight when ALL sets hit the target reps;")
    print("miss twice in a row -> hold load, add a set, or switch to")
    print("double progression (log next --rule double).")


# ---------------------------------------------------------------- plates
PLATES_KG = [25, 20, 15, 10, 5, 2.5, 1.25]
PLATES_LB = [45, 35, 25, 10, 5, 2.5]


def cmd_plates(args):
    unit = args.unit
    plates = PLATES_KG if unit == KG else PLATES_LB
    bar = args.bar if args.bar is not None else (20.0 if unit == KG else 45.0)
    per_side = (args.target - bar) / 2.0
    if per_side < 0:
        die(f"target {args.target} is below bar weight {bar:g}")
    stack, rem = [], per_side
    for p in plates:
        while rem + 1e-9 >= p:
            stack.append(p)
            rem -= p
    if rem > 0.01:
        near = bar + 2 * (per_side - rem)
        print(f"Cannot load exactly {args.target:g} {unit} with these plates.")
        print(f"Nearest loadable: {near:g} {unit}")
        print(f"Per-side stack for {near:g}: "
              + " + ".join(f"{p:g}" for p in stack) + f" {unit}")
        return
    print(f"Target {args.target:g} {args.unit}, bar {bar:g} — per side:")
    print("  " + " + ".join(f"{p:g}" for p in stack) + f" {unit}"
          + (f"  (total {bar + 2*per_side:g} {unit})" if stack else "  (empty bar)"))


# ---------------------------------------------------------------- log
def load_log():
    if os.path.exists(LOG):
        with open(LOG) as f:
            return json.load(f)
    return {"sessions": []}


def save_log(data):
    with open(LOG, "w") as f:
        json.dump(data, f, indent=2)


def cmd_log(args):
    data = load_log()
    if args.log_cmd == "add":
        entry = {"date": date.today().isoformat(), "lift": args.lift,
                 "weight": args.weight, "reps": args.reps,
                 "sets": args.sets, "unit": args.unit}
        data["sessions"].append(entry)
        save_log(data)
        e = epley(args.weight, args.reps)
        print(f"Logged: {args.lift} {args.weight:g}{args.unit} x {args.reps}"
              f"{f' x{args.sets}' if args.sets > 1 else ''}  (e1RM {e:.1f})")
    elif args.log_cmd == "show":
        if not data["sessions"]:
            print("Log is empty.")
            return
        print(f"{'Date':<12}{'Lift':<16}{'Weight':<9}Reps  e1RM")
        print("-" * 50)
        for s in data["sessions"]:
            if args.lift and s["lift"] != args.lift:
                continue
            print(f"{s['date']:<12}{s['lift']:<16}{s['weight']:<9g}"
                  f"{s['reps']:<6}{epley(s['weight'], s['reps']):.1f}")
    elif args.log_cmd == "next":
        hist = [s for s in data["sessions"] if s["lift"] == args.lift]
        if not hist:
            die(f"no history for {args.lift!r}; log a session first")
        last = hist[-1]
        unit = last["unit"]
        best = max(epley(s["weight"], s["reps"]) for s in hist)
        inc = 2.5 if unit == KG else 5.0
        if args.rule == "linear":
            nxt = round25(last["weight"] + inc, unit)
            print(f"Linear: last {last['weight']:g} x {last['reps']}")
            print(f"Next session: {nxt:g} {unit} for same reps"
                  f" — ONLY if last session hit all target reps.")
        else:  # double
            lo_r, hi_r = 8, 12
            if last["reps"] >= hi_r:
                nxt = round25(last["weight"] + inc, unit)
                print(f"Double: hit {last['reps']} (>= {hi_r}) at "
                      f"{last['weight']:g} -> raise to {nxt:g} {unit}, "
                      f"back to {lo_r} reps.")
            else:
                print(f"Double: {last['weight']:g} x {last['reps']} (< {hi_r}) "
                      f"-> stay at {last['weight']:g} {unit}, "
                      f"add reps ({last['reps']+1} next).")
        print(f"Best e1RM on record: {best:.1f} {unit}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("one-rm", help="estimate 1RM from weight x reps")
    p.add_argument("--weight", type=float, required=True)
    p.add_argument("--reps", type=int, required=True)
    p.add_argument("--unit", choices=[KG, LBS], default=KG)
    p.set_defaults(fn=cmd_one_rm)

    p = sub.add_parser("table", help="%-1RM loading table for a goal")
    p.add_argument("--one-rm", type=float, required=True)
    p.add_argument("--goal", choices=list(ZONES), required=True)
    p.add_argument("--unit", choices=[KG, LBS], default=KG)
    p.set_defaults(fn=cmd_table)

    p = sub.add_parser("plan", help="progressive overload block with deloads")
    p.add_argument("--one-rm", type=float, required=True)
    p.add_argument("--goal", choices=list(ZONES), required=True)
    p.add_argument("--weeks", type=int, default=8)
    p.add_argument("--increment", type=float, default=2.5,
                   help="load increment per session")
    p.add_argument("--top-reps", type=int, default=None)
    p.add_argument("--unit", choices=[KG, LBS], default=KG)
    p.set_defaults(fn=cmd_plan)

    p = sub.add_parser("plates", help="per-side plate stack for a target weight")
    p.add_argument("--target", type=float, required=True)
    p.add_argument("--bar", type=float, default=None)
    p.add_argument("--unit", choices=[KG, LBS], default=KG)
    p.set_defaults(fn=cmd_plates)

    p = sub.add_parser("log", help="progress log")
    p.add_argument("log_cmd", choices=["add", "show", "next"])
    p.add_argument("--lift", required=True)
    p.add_argument("--weight", type=float)
    p.add_argument("--reps", type=int)
    p.add_argument("--sets", type=int, default=1)
    p.add_argument("--rule", choices=["linear", "double"], default="double")
    p.add_argument("--unit", choices=[KG, LBS], default=KG)
    p.set_defaults(fn=cmd_log)

    args = ap.parse_args()
    if args.cmd == "log" and args.log_cmd == "add":
        if args.weight is None or args.reps is None:
            die("log add needs --weight and --reps")
    args.fn(args)


if __name__ == "__main__":
    main()
