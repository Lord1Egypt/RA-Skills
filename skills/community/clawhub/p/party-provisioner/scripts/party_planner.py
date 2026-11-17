#!/usr/bin/env python3
"""Party Provisioner — drinks, ice, food, and supplies for events.

Model: consumption scales with GUEST-HOURS, adjusted for heat, activity,
and crowd type. Outputs purchasable units (6-pack, bottle, 750ml, lb, bag)
with round-up, plus glassware/plates/napkins and a budget estimate.

Industry-standard baselines (catering/bartending norms):
  drinks/drinker: 2 in hour 1, 1 each following hour
  wine: 5 glasses per 750ml bottle (150ml catering pour)
  spirits: 17 shots per 750ml (44ml)
  champagne toast pour: 100ml -> 8 glasses/bottle
  ice: ~1 lb per drinking guest for evening + 0.5 lb/drinker-hr in heat
  food: meal 1.2 lb/person (2-3h), appetizers 12 bites/hr, bbq 1/2 lb protein
Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import math
import sys

# ---------------------------------------------------------------------------
# Consumption constants

FIRST_HOUR_DRINKS = 2.0
PER_HOUR_AFTER = 1.0
WINE_GLASSES_PER_BOTTLE = 5
SHOTS_PER_750 = 17
TOAST_GLASSES_PER_BOTTLE = 8
NONALC_PER_HOUR = 2.0        # servings per non-drinking guest-hour
NONALC_DRINKER_HYDRATION = 0.5  # water/soda alongside alcohol, per drinker-hour
ICE_LB_PER_DRINKER = 1.0     # evening baseline
ICE_LB_PER_DRINKER_HOUR_HEAT = 0.5
BEER_PACK = 6


def ceil_to(x: float, unit: int = 1) -> int:
    return int(math.ceil(x / unit) * unit)


# ---------------------------------------------------------------------------
# Core math

def drinks_needed(drinkers: int, hours: float, heat=False, active=False,
                  light=False, wine_only=False) -> float:
    if drinkers <= 0 or hours <= 0:
        return 0.0
    if wine_only:
        per = 1.5 * hours
    else:
        per = FIRST_HOUR_DRINKS + PER_HOUR_AFTER * max(0, hours - 1)
    adj = 1.0
    if heat:
        adj *= 1.2
    if active:
        adj *= 1.1
    if light:
        adj *= 0.8
    return per * adj * drinkers


def split_drinks(total: float, mix: tuple[float, float, float]):
    b, w, s = mix
    total_w = b + w + s
    if total_w == 0:
        return 0.0, 0.0, 0.0
    return total * b / total_w, total * w / total_w, total * s / total_w


def plan(args) -> dict:
    guests = args.guests
    drinkers = args.drinkers if args.drinkers is not None else int(guests * 0.7)
    drinkers = min(drinkers, guests)
    kids = args.kids or 0
    adults = guests - kids
    hours = args.hours
    heat = args.heat
    style = args.style

    # --- drinks
    total = drinks_needed(drinkers, hours, heat=heat, active=args.active,
                          light=args.light, wine_only=args.wine_only)
    beer, wine_glasses, cocktails = split_drinks(total, args.mix)

    beer_units = ceil_to(beer, BEER_PACK) if beer > 0 else 0
    wine_bottles = math.ceil(wine_glasses / WINE_GLASSES_PER_BOTTLE) if wine_glasses > 0 else 0
    spirit_bottles = math.ceil(cocktails / SHOTS_PER_750) if cocktails > 0 else 0
    mixer_servings = ceil_to(cocktails * 0.9, 1) if cocktails > 0 else 0  # 90% take mixer

    toast_bottles = 0
    if args.toast:
        toast_bottles = math.ceil(guests / TOAST_GLASSES_PER_BOTTLE)

    # --- non-alc
    non_drinkers = max(0, guests - drinkers)
    nonalc = non_drinkers * NONALC_PER_HOUR * hours
    hydration = drinkers * NONALC_DRINKER_HYDRATION * hours
    if heat:
        nonalc *= 1.2
        hydration *= 1.2
    soda = ceil_to(nonalc * 0.6, 2)      # 2L bottles ≈ 8 servings
    soda_servings = nonalc + hydration   # total servings needed
    water_500ml = ceil_to(soda_servings * 0.5, 6)  # 6-packs of .5L

    # --- ice
    ice_lb = drinkers * ICE_LB_PER_DRINKER
    if heat:
        ice_lb += drinkers * hours * ICE_LB_PER_DRINKER_HOUR_HEAT
    ice_bags_20lb = max(1, math.ceil(ice_lb / 20)) if drinkers else 0

    # --- food (per style; kids eat half)
    def food_units(adult_equiv):
        if style == "meal" or style == "dinner":
            return {"total_lb": round(adult_equiv * 1.2, 1)}
        if style == "appetizer" or style == "cocktail":
            return {"bites": int(math.ceil(adult_equiv * hours * 12))}
        if style == "bbq":
            return {"protein_lb": round(adult_equiv * 0.5, 1),
                    "sides_lb": round(adult_equiv * 1.0, 1)}
        if style == "reception":
            return {"heavy_appetizer_lb": round(adult_equiv * 1.0, 1),
                    "dessert_servings": guests}
        if style == "birthday":
            return {"cake_servings": guests,
                    "kid_food_servings": int(math.ceil(kids * hours * 1.5)),
                    "adult_snack_lb": round(max(0, adults - kids) * 0.5, 1)}
        return {"total_lb": round(adult_equiv * 1.0, 1)}

    adult_equiv = adults + kids * 0.5
    if args.big_eaters:
        adult_equiv *= 1.25
    food = food_units(adult_equiv)

    # --- extras
    extras = {
        "cups_or_glassware": guests * 2 if style not in ("dinner", "meal") else guests,
        "plates": ceil_to(guests * 1.5, 10),
        "napkins": ceil_to(guests * 3, 25),
        "trash_bags_13gal": max(2, math.ceil(guests / 10)),
        "toilet_paper_rolls_extra": max(1, math.ceil(guests / 15)),
    }

    # --- budget
    budget = None
    if args.price_beer or args.price_wine or args.price_spirit:
        budget = {
            "beer": beer_units * (args.price_beer or 0),
            "wine": wine_bottles * (args.price_wine or 0) + toast_bottles * (args.price_wine or 0),
            "spirits": spirit_bottles * (args.price_spirit or 0),
        }
        budget["total"] = round(sum(v for v in budget.values() if isinstance(v, (int, float))), 2)

    return {
        "guests": guests, "drinkers": drinkers, "kids": kids, "hours": hours,
        "style": style, "heat": heat,
        "drinks_total": round(total, 1),
        "beer_bottles": beer_units,
        "wine_bottles": wine_bottles,
        "spirit_750ml": spirit_bottles,
        "mixer_servings": mixer_servings,
        "toast_bottles": toast_bottles if args.toast else 0,
        "nonalc_servings": int(math.ceil(soda_servings)),
        "soda_2l": soda,
        "water_500ml_6pack": water_500ml,
        "ice_20lb_bags": ice_bags_20lb,
        "food": food,
        "extras": extras,
        "budget": budget,
    }


# ---------------------------------------------------------------------------
# Reporting

def print_plan(p: dict) -> None:
    print("=" * 64)
    print("PARTY PROVISIONER")
    print("=" * 64)
    print(f"{p['guests']} guests ({p['drinkers']} drinkers, {p['kids']} kids) · "
          f"{p['hours']}h · {p['style']} party" + (" · HOT 🥵" if p["heat"] else ""))
    print("-" * 64)

    print("\n🥂 DRINKS")
    if p["drinks_total"]:
        print(f"  total alcohol servings: {p['drinks_total']:.0f} drinks")
        if p["beer_bottles"]:
            print(f"  beer      : {p['beer_bottles']} bottles ({p['beer_bottles']//6 or 1} six-packs)")
        if p["wine_bottles"]:
            print(f"  wine      : {p['wine_bottles']} bottles (5 glasses each)")
        if p["spirit_750ml"]:
            print(f"  spirits   : {p['spirit_750ml']} × 750ml (17 shots each)")
            print(f"  mixers    : {p['mixer_servings']} servings (tonic, juice, cola)")
        if p["toast_bottles"]:
            print(f"  champagne : {p['toast_bottles']} bottles (toast pour 100ml)")
    else:
        print("  no alcohol planned")
    print(f"  non-alc   : {p['nonalc_servings']} servings "
          f"({p['soda_2l']} × 2L soda + {p['water_500ml_6pack']} × 500ml water)")

    print("\n🧊 ICE")
    print(f"  {p['ice_20lb_bags']} × 20 lb bags" if p["ice_20lb_bags"] else "  —")

    print("\n🍽️ FOOD")
    for k, v in p["food"].items():
        unit = "lb" if "lb" in k else ("servings" if "servings" in k or k == "bites" else k)
        print(f"  {k:<24} {v} {unit if 'lb' in k or 'servings' in k or k == 'bites' else ''}")

    print("\n📦 SUPPLIES")
    for k, v in p["extras"].items():
        print(f"  {k:<24} {v}")

    if p["budget"]:
        print("\n💵 BUDGET (alcohol only)")
        for k, v in p["budget"].items():
            print(f"  {k:<24} ${v:.2f}" if isinstance(v, (int, float)) else f"  {k:<24} {v}")

    print("\n⏱️ HOST NOTES")
    print("  · chill whites/rosé & beer 4h ahead; reds 1h if hot")
    print("  · 1 cooler per 15 guests; ice last-minute if >27°C")
    print("  · water station visible = 30% less alcohol consumed")
    print("  · tripwire: <25% of any drink left at 60% of party → prep backup")
    print("=" * 64)


# ---------------------------------------------------------------------------
# CLI

def parse_mix(s: str) -> tuple[float, float, float]:
    parts = [float(x) for x in s.split("/")]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("mix must be beer/wine/spirits like 40/40/20")
    return tuple(parts)  # type: ignore


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Party provisioning calculator")
    p.add_argument("-g", "--guests", type=int, required=True)
    p.add_argument("-t", "--hours", type=float, required=True)
    p.add_argument("--drinkers", type=int, help="drinking guests (default 70%)")
    p.add_argument("--kids", type=int, default=0)
    p.add_argument("--style", default="party",
                   choices=["party", "dinner", "meal", "cocktail", "appetizer",
                            "bbq", "reception", "birthday"],
                   help="food service style")
    p.add_argument("--mix", type=parse_mix, default=(40, 40, 20),
                   help="beer/wine/spirits split %% (default 40/40/20)")
    p.add_argument("--heat", action="store_true", help="hot day (>27°C)")
    p.add_argument("--active", action="store_true", help="dancing/games")
    p.add_argument("--light", action="store_true", help="light-drinker crowd")
    p.add_argument("--wine-only", action="store_true")
    p.add_argument("--toast", action="store_true", help="champagne toast")
    p.add_argument("--big-eaters", action="store_true")
    p.add_argument("--price-beer", type=float)
    p.add_argument("--price-wine", type=float)
    p.add_argument("--price-spirit", type=float)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    if args.guests < 1 or args.hours <= 0:
        print("ERROR: guests ≥ 1 and hours > 0", file=sys.stderr)
        return 2

    p_dict = plan(args)
    if args.json:
        print(json.dumps(p_dict, indent=2, default=str))
    else:
        print_plan(p_dict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
