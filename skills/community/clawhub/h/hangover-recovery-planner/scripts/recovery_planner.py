#!/usr/bin/env python3
"""recovery_planner.py — evidence-based hangover mitigation planner.

The hangover is not one thing: it's dehydration (ethanol inhibits
vasopressin → diuresis), acetaldehyde load (ALDH2 bottleneck; the
Asian-flush genotype processes it slower), methanol metabolism
(congener-heavy dark spirits leave more to metabolize slowly into
formaldehyde/formate), sleep disruption (ethanol wrecks REM),
gastritis, and an inflammatory response. Different mechanisms want
different countermeasures, and several folk remedies actively backfire
(hair-of-the-dog delays recovery; acetaminophen + alcohol loads the
liver; "sweating it out" adds dehydration to dehydration).

This tool takes what the user actually did (drinks by type, duration,
body weight, sex, sleep) and produces:

  1. BAC estimate (Widmark) at end of drinking and NOW, with
     zero-alcohol-since countdown
  2. Fluid deficit estimate (10 mL ethanol diuretic cost per g
     ethanol, minus what was consumed)
  3. A staged recovery plan: rehydration schedule, electrolyte
     targets, food timing (fructose-rich first, fat later), light
     exposure, nap policy
  4. Symptom-router: which mechanism each symptom points at and what
     actually helps it
  5. Red flags that mean "emergency room, not electrolytes"
  6. Next-time prevention card personalized to this episode

Subcommands:
  plan   — full after-the-fact recovery plan
  drink  — live session tracker: is the next drink a good idea?
  rehydrate — just the fluid/electrolyte math

No judgments, no lectures — just physiology and math. If the user
can't go a day without the plan saying STOP, that's a medical
conversation (references/prevention.md has the screening question).
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta

# grams of ethanol per "standard" drink by type (US standard = 14 g)
DRINK_GRAMS = {
    "beer": 14, "light-beer": 11, "craft-beer": 20, "wine": 14,
    "fortified-wine": 20, "champagne": 12, "seltzer": 14,
    "shot": 14, "cocktail": 21, "martini": 28, "long-island": 33,
    "margarita": 24, "whiskey": 14, "vodka": 14, "gin": 14, "rum": 14,
    "tequila": 14, "brandy": 14, "absinthe": 21,
}
# congener load index 0-5 (0 = clean, 5 = congener bomb)
CONGENERS = {
    "vodka": 0, "gin": 1, "seltzer": 0, "light-beer": 0, "beer": 1,
    "champagne": 0, "wine": 2, "craft-beer": 2, "shot": 1,
    "whiskey": 3, "rum": 3, "tequila": 2, "brandy": 4,
    "fortified-wine": 4, "cocktail": 2, "margarita": 2, "martini": 1,
    "long-island": 3, "absinthe": 2,
}

WATER_PER_G_ETHANOL = 10  # mL net fluid loss per gram ethanol
NA_PER_L_SWEAT = 0.9      # g sodium per L — WHO ORS adjacent targets
BAC_ELIM = 0.015          # %BAC per hour, average


def total_grams(drinks: list[tuple[str, int]]) -> tuple[float, float]:
    g = sum(DRINK_GRAMS.get(kind, 14) * n for kind, n in drinks)
    cong = sum(CONGENERS.get(kind, 1) * n for kind, n in drinks)
    return g, cong


def widmark(grams: float, weight_kg: float, sex: str, hours: float) -> float:
    """%BAC: A/(W*r) gives per-mille (g/kg); /10 converts to percent."""
    r = 0.68 if sex == "male" else 0.55
    promille = grams / (weight_kg * r)
    bac = promille / 10
    return max(0.0, bac - BAC_ELIM * hours)


def bac_now(grams, weight, sex, start: datetime, now: datetime) -> tuple[float, float]:
    hours = (now - start).total_seconds() / 3600
    return widmark(grams, weight, sex, hours), hours


def plan(args) -> None:
    drinks = parse_drinks(args.drinks)
    grams, cong = total_grams(drinks)
    start = datetime.fromisoformat(args.start)
    now = datetime.now()
    bac, hours = bac_now(grams, args.weight, args.sex, start, now)
    fluid_deficit_mL = grams * WATER_PER_G_ETHANOL - args.water_during * 250

    print(f"=== SESSION ===")
    print(f"  ethanol: {grams:.0f} g ({grams/14:.1f} US standard drinks)")
    print(f"  congener index: {cong:.0f} ({cong/max(1,sum(n for _,n in drinks)):.1f}/drink — "
          f"{'dark/heavy: worse hangover per gram' if cong/max(1,sum(n for _,n in drinks))>=2.5 else 'light: kinder morning'})")
    print(f"  drinking duration: {hours:.1f} h")

    print(f"\n=== BAC ===")
    print(f"  estimated BAC now: {bac:.3f}% "
          f"{'— DO NOT DRIVE' if bac > 0.02 else '(below 0.02% — likely metabolized)'}")
    if bac > 0.08:
        print(f"  ⚠ still above 0.08% legal limit; ~{bac/BAC_ELIM:.0f} h to zero")

    print(f"\n=== FLUIDS ===")
    deficit = max(0, fluid_deficit_mL)
    print(f"  net fluid deficit ≈ {deficit/1000:.1f} L")
    rehyd = deficit * 1.5
    print(f"  rehydration target: {rehyd/1000:.1f} L over 4-6 h "
          f"(1.5× deficit; sip, don't chug — chugging wastes it as urine)")
    na = rehyd / 1000 * (1.0 if args.sweaty else 0.7)
    print(f"  sodium target: ~{na:.1f} g over the day "
          f"(~{na/0.4:.0f}× typical sports-drink 500 mL; or broth/ORS/norimaki)")

    print(f"\n=== STAGED PLAN ===")
    print("  NOW      500 mL water + electrolytes; no coffee yet")
    print("           (caffeine is fine AFTER rehydration, not instead of it)")
    if bac > 0.02:
        print("           wait for BAC < 0.02% before eating heavy food or napping long")
    print("  +30-60m  easy carbs + fructose: honey toast, fruit, juice —")
    print("           fructose accelerates ethanol metabolism modestly; fat can wait")
    print("  +1-2 h   biggest meal you can face: eggs (cysteine for acetaldehyde),")
    print("           bananas/potato (potassium), salted broth (sodium)")
    print("  +2-4 h   20-min walk outside if upright is possible: light + mild")
    print("           activity speeds clearance; intense exercise ADDS dehydration")
    print("  sleep    REM rebound tonight: expect vivid dreams; 20-min nap max")
    print("           before 3 PM so night sleep isn't shattered")
    print("  avoid    more alcohol (delays methanol clearance — the actual")
    print("           'hair of the dog' mechanism), acetaminophen (liver), NSAIDs")
    print("           on an inflamed stomach — prefer food first")

    print(f"\n=== SYMPTOM ROUTER ===")
    print("  headache        → dehydration + vasodilation: fluids + sodium first;")
    print("                    only THEN ibuprofen WITH food (stomach already angry)")
    print("  nausea          → gastritis: small sips, ginger, antacid; dry carbs")
    print("  shakey/anxious  → low blood sugar: juice now; the anxiety is")
    print("                    glutamate rebound — it passes in hours")
    print("  exhausted-but-wired → REM disruption: tonight's sleep fixes more")
    print("                    than this morning's coffee")
    print("  flushing/rapid pulse → if this happens EVERY time: possible ALDH2")
    print("                    variant — acetaldehyde accumulates; drinking is")
    print("                    measurably more harmful for you (see references)")

    print(f"\n=== RED FLAGS — ER, not electrolytes ===")
    print("  • vomiting > 6 h or can't keep water down 12 h")
    print("  • confusion, slow responses, seizures")
    print("  • cold/clammy/rapid heartbeat that doesn't settle")
    print("  • vomit with blood or like coffee grounds")
    print("  • severe crushing chest/abdominal pain")
    print("  • stopped breathing spells (witnessed) — recovery position, call help")

    print(f"\n=== NEXT TIME (personalized) ===")
    print(f"  • pacing: this session peaked around {widmark(grams,args.weight,args.sex,0):.3f}% BAC;")
    drinks_to_008 = 0.08 * 10 * args.weight * (0.68 if args.sex == 'male' else 0.55) / 14
    print(f"    keep peak < 0.08% ≈ {drinks_to_008:.0f} standard drinks spread over {max(2,hours):.0f}+ h")
    if cong / max(1, sum(n for _, n in drinks)) >= 2.5:
        print("  • congeners: you drank dark/heavy — same buzz on vodka/seltzer")
    else:
        print("  • congeners: already light — keep it that way")
    print("  • 500 mL water per 2 drinks DURING; salty snack slows absorption")
    print("  • eat before, not just after — food in the stomach cuts peak BAC ~2x")


def drink(args) -> None:
    drinks = parse_drinks(args.drinks)
    grams, cong = total_grams(drinks)
    start = datetime.fromisoformat(args.start)
    bac, hours = bac_now(grams, args.weight, args.sex, start, datetime.now())
    print(f"session so far: {grams:.0f} g ethanol, est. BAC {bac:.3f}%")
    if bac >= 0.06:
        print("VERDICT: STOP — at/above 0.06% judgment and coordination are")
        print("measurably impaired and the hangover cost of more is steep.")
    elif bac >= 0.04:
        print("VERDICT: LAST ONE — alternate 500 mL water; kitchen is closing.")
    else:
        print("VERDICT: pace OK — match each drink with water, snack now.")
    print(f"(elimination ≈ {BAC_ELIM}%/h; zero in ~{bac/BAC_ELIM:.1f} h)")


def rehydrate(args) -> None:
    grams, _ = total_grams(parse_drinks(args.drinks))
    deficit = max(0.0, grams * WATER_PER_G_ETHANOL - args.water_during * 250)
    print(f"ethanol {grams:.0f} g → net deficit ≈ {deficit/1000:.1f} L")
    print(f"target: {deficit*1.5/1000:.1f} L over 4-6 h with ~{deficit*1.5/1000*0.7:.1f} g sodium")


def parse_drinks(spec: str) -> list[tuple[str, int]]:
    """'beer:4,shot:2' → [('beer',4),('shot',2)]"""
    out = []
    for part in spec.split(","):
        kind, _, n = part.partition(":")
        out.append((kind.strip().lower(), int(n or 1)))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("plan", help="after-the-fact recovery plan")
    p.add_argument("--drinks", required=True, help="e.g. 'beer:4,shot:2,wine:1'")
    p.add_argument("--weight", type=float, required=True, help="kg")
    p.add_argument("--sex", choices=("male", "female"), required=True)
    p.add_argument("--start", required=True, help="ISO datetime drinking started")
    p.add_argument("--water-during", type=int, default=0, help="glasses of water during")
    p.add_argument("--sweaty", action="store_true", help="dancing/heat")
    p.set_defaults(fn=plan)

    p = sub.add_parser("drink", help="mid-session: next drink verdict")
    p.add_argument("--drinks", required=True)
    p.add_argument("--weight", type=float, required=True)
    p.add_argument("--sex", choices=("male", "female"), required=True)
    p.add_argument("--start", required=True)
    p.set_defaults(fn=drink)

    p = sub.add_parser("rehydrate", help="fluid/electrolyte math only")
    p.add_argument("--drinks", required=True)
    p.add_argument("--water-during", type=int, default=0)
    p.set_defaults(fn=rehydrate)

    args = ap.parse_args()
    if not args.cmd:
        ap.print_help()
        return
    args.fn(args)


if __name__ == "__main__":
    main()
