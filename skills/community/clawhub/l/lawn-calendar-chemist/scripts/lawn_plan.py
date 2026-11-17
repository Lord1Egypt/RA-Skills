#!/usr/bin/env python3
"""Lawn care calendar + fertilizer/chemistry calculator.

Subcommands:
  soil-temp — estimate 2-inch soil temp from recent air temps, verdict on the
              crabgrass pre-emergent window (GO / WATCH / TOO LATE)
  fert      — exact product dose, coverage, and cost-per-lb-N from bag guarantee
  calendar  — region- and grass-adjusted annual care calendar with dated entries

stdlib only.
"""
import argparse
import datetime as dt

F = lambda c: c * 9 / 5 + 32
C = lambda f: (f - 32) * 5 / 9

# region -> (spring soil-55F gate week, fall seeding window, notes)
REGIONS = {
    "deep-south":   ("Feb wk1", "—", "warm-season dominant; fall overseed only for ryegrass color"),
    "south":        ("Feb wk3", "—", "bermuda/st aug; fall PRE for Poa when nights <70"),
    "transition":   ("Mar mid", "Sep 1-30", "tall fescue belt; both grass types stressed"),
    "midwest":      ("Apr wk1", "Aug 20-Sep 20", "cool-season; KBG/fescue"),
    "northeast":    ("Apr wk2", "Aug 25-Sep 25", "cool-season; crabapple bloom co-incident"),
    "northwest":    ("Apr wk1", "Sep 1-30", "cool; moss = pH/shade/drainage issue"),
    "mountain":     ("May wk1", "Sep 1-25", "short season; elevation swings rule"),
}


def cmd_soil(args):
    air = args.air_mean  # deg F, 7-day mean
    # lag model: soil ≈ 0.7×(last 10d mean) + 0.3×(older) − 1.5 ; assume older = air_mean − seasonal
    month = args.date.month
    seasonal = 2.0 if month in (2, 3, 4) else (-2.0 if month in (8, 9, 10) else 0.0)
    older = air - seasonal  # spring: older air was colder -> soil lags below air
    soil = 0.7 * air + 0.3 * older - 1.5
    print(f"7-day mean air: {air:.0f}°F → estimated 2\" soil temp: {soil:.0f}°F "
          f"(lag model; a $10 thermometer beats this)")
    gate = 55.0
    if soil < 50:
        print(f"VERDICT: HOLD — soil {soil:.0f}°F below the 50°F pre-window. "
              f"Germination gate is {gate:.0f}°F x4 days.")
        print("  Watch the forecast: apply when soil crosses 50-53°F and rising.")
    elif soil < gate:
        print(f"VERDICT: WATCH/APPLY — soil {soil:.0f}°F in the 50-55°F pre-window. "
              "Standard practice: apply NOW so the barrier activates before germination.")
        print("  Water in 0.5\" within 48 h to activate.")
    elif soil < 60:
        print(f"VERDICT: APPLY TODAY — soil {soil:.0f}°F at/past the 55°F gate. "
              "Germination starts at 55°F sustained; every day past is crabgrass edge.")
        print("  Dithiopyr still works early-post (1-leaf). Water in 0.5\".")
    else:
        print(f"VERDICT: TOO LATE for pre-emergent alone — soil {soil:.0f}°F; crabgrass is "
              "germinating. Use dithiopyr (early post) or quinclorac on 1-3-leaf plants.")
        print("  Plan round 2 anyway: pre-emergent in late summer when soil 70°F FALLING "
              "for Poa annua (nights in the 60s).")
    if args.region:
        print(f"  Region {args.region}: typical gate {REGIONS[args.region][0]}")


def cmd_fert(args):
    n, p, k = (float(x) for x in args.npk.split("-"))
    bag_n = args.bag_lbs * n / 100
    bag_p = args.bag_lbs * p / 100
    bag_k = args.bag_lbs * k / 100
    need_n = args.area / 1000 * args.n_rate
    product = need_n / (n / 100) if n else 0
    print(f"BAG: {args.bag_lbs} lb of {args.npk} = {bag_n:.1f} lb N, {bag_p:.1f} lb P₂O₅, "
          f"{bag_k:.1f} lb K₂O")
    print(f"NEED: {args.area} ft² @ {args.n_rate} lb N/1000 → {need_n:.2f} lb N "
          f"→ {product:.1f} lb product ({product/args.bag_lbs:.2f} bag)")
    if args.price:
        print(f"COST: ${args.price/bag_n:.2f} per lb N → this application "
              f"${args.price*product/args.bag_lbs:.2f}")
    print(f"COVERAGE: one bag covers {bag_n/args.n_rate*1000:,.0f} ft² at this rate.")
    if p > 0 and args.region in ("deep-south", "south") and args.grass == "centipede":
        print("  ⚠ Phosphorus on centipede = decline risk; use 0-P product.")
    if args.slow_release is not None and args.slow_release < 30 and args.n_rate > 1.0:
        print(f"  ⚠ {args.slow_release:.0f}% slow-release < 30% and rate {args.n_rate} > 1.0 "
              "lb N/1000 → burn risk. Cut to ≤1.0 or split applications.")
    if args.month in (6, 7, 8) and args.grass == "cool":
        print("  ⚠ Summer N on cool-season grass: skip or ≤0.5 lb/1000 + iron for color "
              "instead; water in 0.5\" immediately.")
    print("  Spreaders drift: calibrate (5 lb over 500 ft², weigh leftover, adjust).")


CAL_COOL = [
    ("{y}-02-{d1}", "soil 50-55°F rising: PRE-EMERGENT #1 (prodiamine 0.37-0.65 oz ai/1000); water 0.5\""),
    ("{y}-04-{d2}", "PRE-EMERGENT #2 (8-10 wk after #1) if heavy pressure; broadleaf spray at full leaf"),
    ("{y}-05-15",   "optional light N 0.5 lb/1000 (only if fall feeding was skipped)"),
    ("{y}-06-01",   "raise mow height to 3.5-4\"; NO summer N on fescue/KBG"),
    ("{y}-08-25",   "seedbed prep if overseeding; STOP broadleaf sprays 4 wk before seed"),
    ("{y}-09-01",   "AERATE + OVERSEED cool-season (soil 60-75°F falling); starter fertilizer 1.0 N"),
    ("{y}-10-01",   "fall N 1.0 lb/1000 (root season)"),
    ("{y}-11-01",   "final N 0.75 winterizer while still green; leaf cleanup"),
]
CAL_WARM = [
    ("{y}-02-{d1}", "soil 50-55°F: PRE-EMERGENT spring (crabgrass/goosegrass) on dormant turf"),
    ("{y}-04-15",   "wait for GREEN-UP (soil 65°F+): first N 0.5-0.75 lb/1000 after full green"),
    ("{y}-05-15",   "N monthly begins (bermuda 1.0; zoysia/centipede 0.25)"),
    ("{y}-07-15",   "peak-season N; check chinch bugs (St Aug) / armyworm"),
    ("{y}-08-{d3}", "soil 70°F FALLING + nights <70: fall PRE-EMERGENT for Poa annua"),
    ("{y}-10-01",   "last N 30-45 d before frost; raise mow height slightly"),
    ("{y}-11-15",   "dormant: stop feeding; keep 1\"/wk water if no rain until soil 40s"),
]


def cmd_calendar(args):
    region = args.region
    gate, seedwin, note = REGIONS[region]
    dmap = {"deep-south": ("01", "15", "20"), "south": ("15", "01", "20"),
            "transition": ("20", "10", "20"), "midwest": ("01", "20", "10"),
            "northeast": ("10", "25", "15"), "northwest": ("05", "20", "10"),
            "mountain": ("01", "20", "05")}
    d1, d2, d3 = dmap[region]
    cal = CAL_COOL if args.grass == "cool" else CAL_WARM
    y = args.year or dt.date.today().year
    print(f"ANNUAL LAWN CALENDAR — {args.grass}-season grass, {region} "
          f"(typical gate: {gate}; seed window: {seedwin})")
    print(note + "\n")
    for tmpl, action in cal:
        date = tmpl.format(y=y, d1=d1, d2=d2, d3=d3)
        try:
            d = dt.date.fromisoformat(date)
        except ValueError:
            d = dt.date.fromisoformat(date[:-2] + "28")
        flag = ""
        if "OVERSEED" in action and args.preemergent_spring:
            flag = "  ⚠ CONFLICT: spring pre-emergent residue kills fall seed if applied <12 wk ago" \
                   " (prodiamine ≈ 3-4 mo) — verify application date or use seeding-rate +25%"
        if action.startswith("optional light N") and args.grass == "cool":
            flag = "  (skip if you fertilized last fall — spring N feeds topgrowth, starves roots)"
        print(f"  {d}: {action}{flag}")
    print("\n  Dates are anchors — the GATES are soil temps: PRE at 50-55°F rising; "
          "fall seed at 60-75°F falling; warm-season N after 65°F green-up.")
    print("  Mow rules: never remove >1/3 of blade; taller = deeper roots + shade for weed seed.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("soil-temp")
    s.add_argument("--air-mean", type=float, required=True, help="7-day mean air temp °F")
    s.add_argument("--date", type=dt.date.fromisoformat, default=dt.date.today())
    s.add_argument("--region", choices=sorted(REGIONS))
    s.set_defaults(fn=cmd_soil)

    f = sub.add_parser("fert")
    f.add_argument("--npk", required=True, help="e.g. 20-0-8")
    f.add_argument("--bag-lbs", type=float, required=True)
    f.add_argument("--price", type=float)
    f.add_argument("--area", type=float, required=True, help="sq ft")
    f.add_argument("--n-rate", type=float, default=1.0, help="lb N per 1000 sq ft")
    f.add_argument("--slow-release", type=float, help="% slow-release N")
    f.add_argument("--grass", default="cool", choices=["cool", "warm"])
    f.add_argument("--region", choices=sorted(REGIONS))
    f.add_argument("--month", type=int, default=dt.date.today().month)
    f.set_defaults(fn=cmd_fert)

    c = sub.add_parser("calendar")
    c.add_argument("--grass", required=True, choices=["cool", "warm"])
    c.add_argument("--region", required=True, choices=sorted(REGIONS))
    c.add_argument("--year", type=int)
    c.add_argument("--preemergent-spring", action="store_true",
                   help="flag: spring pre-emergent was applied (checks fall-seed conflict)")
    c.set_defaults(fn=cmd_calendar)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
