#!/usr/bin/env python3
"""Holiday lights circuit-load planner.

Sums decorative light strings, inflatables and projectors against a circuit's
80% continuous budget, checks daisy-chain limits, extension-cord gauge vs run
length, outdoor GFCI rules and timer ratings, and prices the season with
LED-payback math. Pure stdlib; no network; dry arithmetic on user input.

Examples:
  python3 lights_load.py --breaker 15 --existing-watts 100 \
      --strings incandescent-mini:100:12 led-mini:70:3 --inflatables 1 \
      --cord-gauge 14 --cord-length-ft 80 --outdoor --timer-amps 15
  python3 lights_load.py --breaker 15 --strings incandescent-mini:100:24 --compare-led
"""
import argparse
import sys

# watts per bulb by light type; chain = max end-to-end strings (typical fused-plug limit)
LIGHT_TYPES = {
    # name: (watts_per_bulb, max_daisy_chain, label)
    "incandescent-mini": (0.45, 5, "Incandescent mini (0.4-0.5 W/bulb)"),
    "incandescent-c7":   (5.0, 2, "Incandescent C7 (5-7 W/bulb)"),
    "incandescent-c9":   (7.0, 2, "Incandescent C9 (7-10 W/bulb)"),
    "led-mini":          (0.07, 43, "LED mini/string"),
    "led-c9":            (0.10, 43, "LED C9"),
    "rope-incandescent": (5.5, 10, "Rope light, incandescent (per meter!)"),
    "rope-led":          (2.0, 10, "Rope light, LED (per meter!)"),
    "net-lights":        (0.45, 3, "Net lights, incandescent"),
}
# rope types are per-meter, not per-bulb — handled via key prefix below
PER_METER_TYPES = {"rope-incandescent", "rope-led"}

VOLTS = 120.0
RATE_DEFAULT = 0.17  # $/kWh national-ish average, override with --kwh-cost

# extension cord: gauge -> (max ft at ~13A light duty, max ft at ~10A)
CORD_LIMITS = {
    16: (50, 25),
    14: (100, 50),
    12: (150, 100),
    10: (250, 150),
}


def parse_strings(specs):
    """'type:bulbs:count' -> list of dicts; bulbs means meters for rope types."""
    out = []
    for spec in specs or []:
        parts = spec.split(":")
        if len(parts) != 3:
            sys.exit(f"ERROR: bad --strings entry '{spec}' (want type:bulbs:count)")
        typ, bulbs, count = parts[0].strip().lower(), float(parts[1]), int(parts[2])
        if typ not in LIGHT_TYPES:
            sys.exit(f"ERROR: unknown light type '{typ}'. Known: {', '.join(LIGHT_TYPES)}")
        out.append({"type": typ, "bulbs": bulbs, "count": count})
    return out


def watts_for(entry):
    w_per, _, label = LIGHT_TYPES[entry["type"]]
    if entry["type"] in PER_METER_TYPES:
        w = entry["bulbs"] * w_per * entry["count"]  # bulbs field = meters
    else:
        w = entry["bulbs"] * w_per * entry["count"]
    return w, label


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--breaker", type=float, default=15, help="circuit breaker amps (default 15)")
    ap.add_argument("--existing-watts", type=float, default=0.0, help="always-on load already on circuit")
    ap.add_argument("--strings", nargs="*", default=[], help="type:bulbs-or-meters:count entries")
    ap.add_argument("--inflatables", type=int, default=0, help="count of inflatables (blowers)")
    ap.add_argument("--projector", action="store_true", help="include one light projector (~60 W)")
    ap.add_argument("--cord-gauge", type=int, choices=sorted(CORD_LIMITS), help="extension cord AWG")
    ap.add_argument("--cord-length-ft", type=float, help="extension cord run length")
    ap.add_argument("--outdoor", action="store_true", help="outdoor display: GFCI + wet-location rules")
    ap.add_argument("--timer-amps", type=float, help="timer/photocell contact rating")
    ap.add_argument("--hours-per-night", type=float, default=6.0)
    ap.add_argument("--nights", type=int, default=45, help="season nights (default 45)")
    ap.add_argument("--kwh-cost", type=float, default=RATE_DEFAULT)
    ap.add_argument("--compare-led", action="store_true",
                    help="also print LED equivalent of incandescent strings")
    args = ap.parse_args()

    print("=" * 62)
    print("HOLIDAY LIGHTS LOAD SHEET")
    print("=" * 62)

    # 1. circuit budget
    nameplate = args.breaker * VOLTS
    budget = nameplate * 0.8
    print(f"\n[1] CIRCUIT BUDGET  ({args.breaker:g} A breaker)")
    print(f"    nameplate {nameplate:,.0f} W | 80% continuous budget {budget:,.0f} W")
    print(f"    existing load claimed: {args.existing_watts:,.0f} W")
    available = budget - args.existing_watts
    if available <= 0:
        sys.exit("ERROR: existing load already exceeds the 80% budget — move to another circuit.")
    print(f"    available for lights: {available:,.0f} W")

    # 2. string load
    print(f"\n[2] STRING LOADS")
    total_w = 0.0
    for entry in parse_strings(args.strings):
        w, label = watts_for(entry)
        total_w += w
        per_str, chain, _ = LIGHT_TYPES[entry["type"]]
        per_str_w = entry["bulbs"] * per_str
        unit = "m" if entry["type"] in PER_METER_TYPES else "bulbs"
        print(f"    {entry['count']:3d} x {label}")
        print(f"        {entry['bulbs']:g} {unit}/string x {entry['count']} = {w:,.0f} W"
              f"  ({w / VOLTS:,.2f} A)")

    if args.inflatables:
        w = args.inflatables * 100  # 50-150 W blowers, midpoint
        total_w += w
        print(f"    {args.inflatables} x inflatables (blowers @100 W avg)  = {w:,.0f} W"
              f"  ({w / VOLTS:,.2f} A)")
    if args.projector:
        total_w += 60
        print(f"    1 x light projector                        =   60 W  (0.50 A)")

    total_a = total_w / VOLTS
    grand = total_w + args.existing_watts
    print(f"\n    LIGHTS TOTAL: {total_w:,.0f} W ({total_a:,.2f} A)")
    print(f"    WITH EXISTING: {grand:,.0f} W ({grand / VOLTS:,.2f} A)")

    # 3. verdict
    margin = budget - grand
    pct = grand / budget * 100
    print(f"\n[3] CIRCUIT VERDICT")
    print(f"    load {grand:,.0f} W vs budget {budget:,.0f} W  ({pct:.0f}% used, margin {margin:+,.0f} W)")
    if grand > budget:
        verdict = "OVERLOAD — re-plan: split across circuits or convert to LED"
    elif pct > 90:
        verdict = "TIGHT — works, but zero headroom for anything else on this circuit"
    else:
        verdict = "SAFE — comfortable headroom"
    print(f"    >> {verdict}")

    # 4. daisy-chain check
    print(f"\n[4] DAISY-CHAIN CHECK")
    any_flag = False
    for entry in parse_strings(args.strings):
        typ = entry["type"]
        if typ in PER_METER_TYPES:
            continue
        chain = LIGHT_TYPES[typ][1]
        if entry["count"] > chain:
            any_flag = True
            print(f"    !! {typ}: {entry['count']} strings but fused plug allows ~{chain} end-to-end.")
            print(f"       Split into {(entry['count'] + chain - 1) // chain} runs fed from the wall.")
    if not any_flag:
        print("    OK — no single run exceeds its type's typical end-to-end limit.")

    # 5. cord check
    print(f"\n[5] EXTENSION CORD")
    if args.cord_gauge and args.cord_length_ft:
        hi, lo = CORD_LIMITS[args.cord_gauge]
        # light duty (<=13A) limit is `hi`; heavier 10A continuous uses `lo`
        ok_13, ok_10 = args.cord_length_ft <= hi, args.cord_length_ft <= lo
        if ok_13:
            print(f"    #{args.cord_gauge} at {args.cord_length_ft:g} ft: OK (rated to {hi} ft at light duty)")
        elif ok_10:
            print(f"    #{args.cord_gauge} at {args.cord_length_ft:g} ft: MARGINAL — fine ≤{lo} ft at 10 A;")
            print(f"       for {args.cord_length_ft:g} ft at this load step up one gauge")
        else:
            print(f"    !! #{args.cord_gauge} at {args.cord_length_ft:g} ft TOO LONG — voltage drop and")
            print(f"       heating; use #{args.cord_gauge - 2} or shorter runs")
    else:
        print("    (no cord specified — reference: #16 ≤50 ft, #14 ≤100 ft, #12 ≤150 ft)")
        print("     outdoor runs want #14 minimum, outdoor-rated jacket, nothing coiled")

    # 6. outdoor
    print(f"\n[6] OUTDOOR RULES")
    if args.outdoor:
        print("    REQUIRED: GFCI-protected outlet (or GFCI cord adapter);")
        print("    wet-location-rated (UL/ETL) lights and cords; plugs elevated in")
        print("    bubble covers, never on the ground; staked down, not across walks.")
    else:
        print("    indoor plan — keep plugs away from fabric/drapes; no cords under rugs.")

    # 7. timer
    print(f"\n[7] TIMER / PHOTOCELL")
    if args.timer_amps:
        if args.timer_amps >= total_a:
            print(f"    OK — timer rated {args.timer_amps:g} A ≥ load {total_a:.2f} A")
        else:
            print(f"    !! Timer rated {args.timer_amps:g} A < load {total_a:.2f} A — fire risk.")
            print(f"       Use a relay/contactor-rated timer or split loads across two timers.")
    else:
        print("    rate the timer like a cord: contact rating ≥ total amps through it")

    # 8. season cost + LED payback
    print(f"\n[8] SEASON COST & LED PAYBACK")
    kwh = total_w / 1000 * args.hours_per_night * args.nights
    cost = kwh * args.kwh_cost
    print(f"    {args.hours_per_night:g} h/night x {args.nights} nights @ {args.kwh_cost:g} $/kWh")
    print(f"    = {kwh:,.1f} kWh = ${cost:,.2f} for the season")
    if args.compare_led:
        led_w = 0.0
        for entry in parse_strings(args.strings):
            if entry["type"].startswith("incandescent") or entry["type"] == "net-lights":
                led_equiv = "led-" + entry["type"].replace("incandescent-", "")
                if led_equiv in LIGHT_TYPES:
                    led_w += entry["bulbs"] * LIGHT_TYPES[led_equiv][0] * entry["count"]
                else:
                    led_w += entry["bulbs"] * 0.07 * entry["count"]
        new_total = led_w + (total_w - sum(watts_for(e)[0] for e in parse_strings(args.strings)
                                           if e["type"].startswith("incandescent") or e["type"] == "net-lights"))
        saved = total_w - new_total
        if saved > 1:
            skwh = saved / 1000 * args.hours_per_night * args.nights
            print(f"    LED swap saves {saved:,.0f} W ({skwh:,.0f} kWh ≈ ${skwh * args.kwh_cost:,.2f}/season)")
            print(f"    headroom freed: {saved:,.0f} W ≈ {saved / 0.45 / 100:,.0f} more mini-equivalents")
        else:
            print("    nothing incandescent to convert — already LED-clean.")

    print("\n" + "=" * 62)
    print("Verify after hanging: plugs/cords cool to touch after 15 minutes.")
    print("=" * 62)


if __name__ == "__main__":
    main()
