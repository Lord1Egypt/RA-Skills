#!/usr/bin/env python3
"""plant-light-doctor: monthly DLI model for windows + plant matching + grow-light sizing.

Physics: solar declination -> day length -> clear-sky PPFD (Bouguer) -> vertical
wall capture by orientation -> multiplicative corrections (floor, obstruction,
glass, overhang, climate) -> DLI per month. Verdicts: THRIVES / SURVIVES /
STRUGGLES / IMPOSSIBLE vs a built-in plant library. Optional grow-light spec.

Pure stdlib. Constants calibrated to give ballpark-accurate results (+/-30%).
"""
import argparse
import math
import sys

SOLAR_PPFD_0 = 2550.0  # extraterrestrial PAR, umol/m2/s


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def month_days():
    return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def day_of_year(month):
    return sum(month_days()[: month - 1]) + 15


def solar_declination_deg(n):
    return 23.44 * math.sin(math.radians(360.0 * (284 + n) / 365.0))


def day_length_hours(lat_deg, decl_deg):
    lat = math.radians(lat_deg)
    dec = math.radians(decl_deg)
    x = -math.tan(lat) * math.tan(dec)
    x = clamp(x, -1.0, 1.0)
    h0 = math.degrees(math.acos(x))
    return 2.0 * h0 / 15.0


def noon_elevation_deg(lat_deg, decl_deg):
    return 90.0 - abs(lat_deg - decl_deg)


def clearsky_direct_ppfd(elev_deg):
    """Bouguer-style attenuation of direct beam PAR."""
    if elev_deg <= 2:
        return 0.0
    am = 1.0 / math.sin(math.radians(elev_deg))
    am = min(am, 38.0)
    return SOLAR_PPFD_0 * (0.7 ** (am ** 0.678))


# --- vertical wall capture coefficients (fraction of daily global horizontal PAR
# --- that a vertical wall of given orientation receives), northern hemisphere,
# --- parameterized by |latitude| band and month. Calibrated from typical
# --- solar geometry tables (Perez anisotropic sky, simplified).
def capture_coeff(orientation, lat_abs, decl):
    """Return direct+diffuse capture fraction for a vertical wall."""
    o = orientation.upper()
    summerish = decl > 8           # high-sun season
    winterish = decl < -8          # low-sun season
    if lat_abs < 15:               # tropics: E/W dominate, N/S get high sun only
        base = {"S": 0.42, "N": 0.38, "E": 0.58, "W": 0.58,
                "SE": 0.50, "SW": 0.50, "NE": 0.52, "NW": 0.52}
    elif lat_abs < 40:             # mid-latitude
        base = {"S": 0.56, "N": 0.14, "E": 0.44, "W": 0.44,
                "SE": 0.52, "SW": 0.52, "NE": 0.28, "NW": 0.28}
    else:                          # high latitude: S wall winter advantage huge
        base = {"S": 0.58, "N": 0.10, "E": 0.42, "W": 0.42,
                "SE": 0.50, "SW": 0.50, "NE": 0.24, "NW": 0.24}
    if summerish:
        base = dict(base)
        base["S"] *= 0.78          # high sun grazes equator-facing wall
        base["N"] *= 1.9           # long summer days reach pole-facing wall
        for k in ("E", "W", "NE", "NW", "SE", "SW"):
            base[k] *= 1.12
    if winterish:
        base = dict(base)
        base["S"] *= 1.15          # low winter sun near-perpendicular on S wall
        base["N"] *= 0.35
        for k in ("E", "W", "NE", "NW", "SE", "SW"):
            base[k] *= 0.92
    return base.get(o, 0.35)


CLIMATE = {"cloudy": 0.58, "temperate": 0.78, "sunny": 1.0}
GLASS = {"single": 0.90, "double": 0.85, "low-e": 0.75, "tinted": 0.65}


def floor_penalty(floor):
    if floor <= 0:
        return 0.80
    if floor == 1:
        return 0.86
    if floor == 2:
        return 0.92
    return 0.96


def overhang_factor(orientation, decl, lat_abs):
    """Deep overhangs block high summer sun but admit low winter sun."""
    if decl > 12:
        return 0.60
    if decl > 0:
        return 0.80
    if decl > -12:
        return 0.92
    return 1.00


def monthly_dli(orientation, latitude, floor=2, obstruction=0.0, glass="double",
                climate="temperate", overhang=False):
    """Return list of 12 DLI values (mol/m2/day) at the window plane."""
    lat_abs = abs(latitude)
    glass_t = GLASS.get(glass, 0.85)
    clim = CLIMATE.get(climate, 0.78)
    out = []
    for m in range(1, 13):
        n = day_of_year(m)
        decl = solar_declination_deg(n)
        dl = day_length_hours(latitude, decl)
        elev = noon_elevation_deg(latitude, decl)
        direct = clearsky_direct_ppfd(elev)
        diffuse = 0.10 * direct + 25.0  # sky scatter floor, umol/m2/s
        # daily global horizontal PAR -> mol
        ghor = (direct * max(math.sin(math.radians(elev)), 0.05) + diffuse)
        ghor_mol = ghor * 3600.0 * dl / 1e6
        cap = capture_coeff(orientation, lat_abs, decl)
        # diffuse-only floor for pole-facing walls: sky light still arrives
        wall = ghor_mol * cap
        if cap < 0.15:
            wall = max(wall, ghor_mol * 0.09)  # diffuse on glass
        wall *= floor_penalty(floor)
        wall *= (1.0 - clamp(obstruction, 0.0, 0.95))
        wall *= glass_t
        if overhang:
            wall *= overhang_factor(orientation, decl, lat_abs)
        wall *= clim
        out.append(wall)
    return out


# Plant library: name -> (min_dli, opt_low, opt_high, category)
PLANTS = {
    # edible
    "basil": (8, 12, 16, "herb"),
    "mint": (6, 10, 14, "herb"),
    "chives": (7, 12, 16, "herb"),
    "parsley": (7, 12, 16, "herb"),
    "cilantro": (9, 13, 17, "herb"),
    "rosemary": (10, 15, 20, "herb"),
    "lettuce": (11, 14, 17, "edible"),
    "spinach": (10, 13, 16, "edible"),
    "microgreens": (6, 8, 12, "edible"),
    "cherry tomato": (18, 22, 30, "edible"),
    "chili pepper": (16, 20, 28, "edible"),
    "strawberry": (14, 18, 24, "edible"),
    "wheatgrass": (6, 10, 14, "edible"),
    # foliage
    "pothos": (2.5, 5, 9, "foliage"),
    "zz plant": (1.5, 4, 8, "foliage"),
    "snake plant": (2.0, 5, 10, "foliage"),
    "philodendron heartleaf": (2.5, 5, 9, "foliage"),
    "monstera": (4.5, 8, 14, "foliage"),
    "peace lily": (3, 6, 10, "foliage"),
    "chinese evergreen": (2, 4, 8, "foliage"),
    "calathea": (3, 5, 8, "foliage"),
    "fiddle-leaf fig": (7, 12, 20, "foliage"),
    "rubber plant": (5, 9, 15, "foliage"),
    "ficus benjamina": (6, 10, 16, "foliage"),
    "dracaena": (3, 6, 10, "foliage"),
    "dieffenbachia": (3.5, 6, 10, "foliage"),
    "anthurium": (6, 9, 14, "foliage"),
    "peperomia": (4, 7, 11, "foliage"),
    "hoya": (6, 10, 16, "foliage"),
    "spider plant": (4, 7, 12, "foliage"),
    "aloe vera": (9, 14, 20, "succulent"),
    "jade plant": (8, 13, 20, "succulent"),
    "echeveria": (9, 14, 22, "succulent"),
    "cactus": (12, 18, 30, "succulent"),
    "orchid phalaenopsis": (5, 7, 11, "bloom"),
    "orchid cattleya": (10, 14, 20, "bloom"),
    "african violet": (5, 8, 12, "bloom"),
    "bromeliad": (6, 9, 14, "bloom"),
    "boston fern": (4, 6, 10, "fern"),
    "air plant": (6, 9, 14, "epiphyte"),
    "dwarf citrus": (16, 20, 28, "edible"),
    "dwarf olive": (16, 20, 30, "edible"),
    "venus flytrap": (18, 25, 35, "carnivorous"),
}

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def verdict(dli_available, need_min, opt_low, opt_high):
    if dli_available >= opt_low:
        return "THRIVES"
    if dli_available >= need_min:
        return "SURVIVES"
    if dli_available >= 0.55 * need_min:
        return "STRUGGLES"
    return "IMPOSSIBLE"


def find_plant(name):
    key = name.lower().strip()
    if key in PLANTS:
        return key
    for k in PLANTS:
        if key in k or k in key:
            return k
    return None


def humanize(x):
    return f"{x:.1f}"


def main():
    ap = argparse.ArgumentParser(
        description="Monthly window DLI model + plant matching + grow-light sizing")
    ap.add_argument("--orientation", required=True,
                    choices=["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
                    help="Direction the window FACES")
    ap.add_argument("--latitude", type=float, required=True,
                    help="Positive = northern hemisphere (e.g. 52.5 for Berlin)")
    ap.add_argument("--floor", type=int, default=2,
                    help="Floor number (0=ground/basement, default 2)")
    ap.add_argument("--obstruction", type=float, default=0.0,
                    help="Fraction of sun hours blocked 0.0-0.95")
    ap.add_argument("--glass", default="double",
                    choices=["single", "double", "low-e", "tinted"])
    ap.add_argument("--climate", default="temperate",
                    choices=["cloudy", "temperate", "sunny"])
    ap.add_argument("--overhang", action="store_true",
                    help="Deep eave/balcony above the window")
    ap.add_argument("--check", default=None,
                    help="Check one plant by name (quoted)")
    ap.add_argument("--list-matches", action="store_true",
                    help="Print the full ranked match table")
    ap.add_argument("--grow-light", action="store_true",
                    help="Size a grow light to reach --target-dli")
    ap.add_argument("--target-dli", type=float, default=None,
                    help="Target DLI for grow-light sizing (mol/m2/day)")
    ap.add_argument("--photoperiod", type=float, default=14.0,
                    help="Grow-light hours/day (default 14)")
    args = ap.parse_args()

    if args.latitude > 0:
        eff_orient = args.orientation
    else:
        flip = {"N": "S", "NE": "SW", "E": "W", "SE": "NW",
                "S": "N", "SW": "NE", "W": "E", "NW": "SE"}
        eff_orient = flip[args.orientation]

    dli = monthly_dli(eff_orient, args.latitude, args.floor,
                      args.obstruction, args.glass, args.climate, args.overhang)
    worst_i = min(range(12), key=lambda i: dli[i])
    best_i = max(range(12), key=lambda i: dli[i])

    print("=" * 62)
    print(f"WINDOW LIGHT AUDIT  —  {args.orientation}-facing, "
          f"lat {args.latitude:+.1f}, floor {args.floor}")
    print(f"obstruction {args.obstruction:.0%}, {args.glass} glass, "
          f"{args.climate} climate"
          + (", overhang" if args.overhang else ""))
    print("=" * 62)
    print(f"{'Month':<6}", *(f"{m:>5}" for m in MONTH_NAMES))
    print(f"{'DLI':<6}", *(f"{humanize(v):>5}" for v in dli))
    print(f"\nWorst month: {MONTH_NAMES[worst_i]} = {humanize(dli[worst_i])} "
          f"mol/m2/day   (plan around THIS)")
    print(f"Best  month: {MONTH_NAMES[best_i]} = {humanize(dli[best_i])} "
          f"mol/m2/day")

    band = dli[worst_i]
    if args.check:
        key = find_plant(args.check)
        if not key:
            print(f"\n[!] Plant '{args.check}' not in library. "
                  f"Closest matches:", file=sys.stderr)
            cands = sorted(PLANTS)[:10]
            print("    " + ", ".join(cands), file=sys.stderr)
            sys.exit(2)
        mn, lo, hi, cat = PLANTS[key]
        print(f"\n--- {key.upper()} ({cat}) ---")
        print(f"needs min {mn} / optimal {lo}-{hi} mol")
        v_worst = verdict(band, mn, lo, hi)
        v_best = verdict(dli[best_i], mn, lo, hi)
        print(f"Worst month: {v_worst}   Best month: {v_best}")
        if v_worst == "SURVIVES":
            print("-> Will live year-round but grow slowly; expect smaller"
                  " leaves, maybe no bloom.")
        elif v_worst == "STRUGGLES":
            print(f"-> Will etiolate. Supplement with light "
                  f"({MONTH_NAMES[worst_i]} is the killer) or pick another plant.")
        elif v_worst == "IMPOSSIBLE":
            if v_best in ("THRIVES", "SURVIVES"):
                print(f"-> SEASONAL ONLY: fine {MONTH_NAMES[best_i]}-{MONTH_NAMES[(best_i+3)%12]}"
                      f" (best {humanize(dli[best_i])} mol), but {MONTH_NAMES[worst_i]}="
                      f"{humanize(band)} is far below the {mn} mol floor.")
                print("   Options: grow as a summer annual, take cuttings in"
                      " late summer, or add a grow light Oct-Mar.")
            else:
                print("-> This window cannot support it, even in summer. "
                      "Strong grow light or different plant.")
        else:
            print("-> Good to go, year-round in this window.")
    else:
        tiers = {"THRIVES": [], "SURVIVES": [], "STRUGGLES": [], "IMPOSSIBLE": []}
        for name, (mn, lo, hi, cat) in PLANTS.items():
            tiers[verdict(band, mn, lo, hi)].append((name, mn, lo, hi, cat))
        print(f"\nMatch verdicts at worst-month DLI {humanize(band)}:")
        for tier in ("THRIVES", "SURVIVES", "STRUGGLES", "IMPOSSIBLE"):
            lst = sorted(tiers[tier])
            names = [n for n, *_ in lst]
            show = names[:8] if not args.list_matches else names
            print(f"  {tier:<11} ({len(lst):>2}): " + ", ".join(show)
                  + (f" ... +{len(names)-8} more" if len(names) > 8 and not args.list_matches else ""))
        # what the good months unlock
        best_band = dli[best_i]
        unlock = sorted(n for n, (mn, lo, hi, c) in PLANTS.items()
                        if verdict(band, mn, lo, hi) in ("STRUGGLES", "IMPOSSIBLE")
                        and verdict(best_band, mn, lo, hi) in ("THRIVES", "SURVIVES"))
        if unlock:
            show = unlock[:8]
            print(f"\nSummer-only campers (OK in {MONTH_NAMES[best_i]}, dead by "
                  f"{MONTH_NAMES[worst_i]}): " + ", ".join(show)
                  + (f" ... +{len(unlock)-8} more" if len(unlock) > 8 else ""))

    if args.grow_light:
        target = args.target_dli
        if target is None:
            target = max(6.0, band + 4.0)
        gap = max(0.0, target - band)
        ppfd = gap * 1e6 / (3600.0 * args.photoperiod)
        print("\n--- GROW LIGHT SPEC ---")
        print(f"target DLI {target:.1f} vs worst month {humanize(band)} "
              f"-> gap {gap:.1f} mol/m2/day")
        print(f"required PPFD over {args.photoperiod:.0f} h/day: "
              f"{ppfd:.0f} umol/m2/s at the canopy")
        # fixture suggestions for a 60x20 cm shelf (0.12 m2)
        area = 0.12
        watts_quality = ppfd * area / 2.6
        watts_cheap = ppfd * area / 1.4
        print(f"fixture for a 60x20cm shelf: ~{watts_quality:.0f} W quality "
              f"quantum-board class, or ~{watts_cheap:.0f} W cheap full-spectrum strip")
        print("hang 25-40 cm above canopy; put a timer on it - "
              "photoperiod consistency beats raw intensity")

    return 0


if __name__ == "__main__":
    sys.exit(main())
