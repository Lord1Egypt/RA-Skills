#!/usr/bin/env python3
"""Post-power-outage fridge/freezer food triage (FDA/USDA consumer guidance)."""
import argparse

# Category rules: (keywords, verdict, reason)
ITEMS = [
    (["leftover", "takeout", "casserole", "cooked rice", "cooked pasta", "stew", "soup", "chili"],
     "TOSS if >4h in danger zone", "cooked perishables: no further cook-step protection"),
    (["deli meat", "lunch meat", "cold cut", "deli turkey", "deli ham",
      "sliced turkey", "sliced ham", "salami"],
     "TOSS after 4h", "listeria risk class; deli meats are top post-outage hazard"),
    (["raw meat", "chicken", "ground beef", "pork", "steak", "fish", "shrimp", "seafood"],
     "TOSS if >2h above 40F", "fast bacterial growth; refreeze ONLY if still <=40F w/ crystals"),
    (["milk", "yogurt", "cream", "sour cream", "buttermilk", "kefir", "soft cheese",
      "brie", "ricotta", "cottage cheese", "shredded cheese"],
     "TOSS after 4h", "high-moisture dairy; spoilage + pathogen risk"),
    (["hard cheese", "parmesan", "cheddar block", "swiss block"],
     "KEEP if smell/texture normal", "low moisture = hostile environment"),
    (["butter", "margarine"],
     "KEEP", "fat-dominant, low water activity"),
    (["eggs", "egg"],
     "KEEP if uncracked and <=4h... then cook fully", "shell + membranes give some margin; cook hard"),
    (["mayonnaise", "ketchup", "mustard", "soy sauce", "hot sauce", "vinegar", "pickle",
      "jam", "jelly", "peanut butter", "salsa (commercial, acidic)"],
     "KEEP (commercial, acidic/high-sugar/fat)", "water activity/pH blocks pathogen growth"),
    (["open salad dressing", "creamy dressing (open, dairy)"],
     "TOSS creamy open jars after 4h; vinegar-based keep", "dairy-based emulsions spoil"),
    (["fruits", "vegetables", "fresh produce", "cut fruit", "cut melon"],
     "CUT fruit/melon: TOSS after 4h. Whole produce: KEEP", "cut melon is a listed listeria vector"),
    (["juice (open)", "pasta sauce (open)", "tomato sauce (open)"],
     "KEEP if still cool; toss if warm or off", "acidity helps but not immunity"),
    (["breast milk", "infant formula (prepared)", "baby food (open)"],
     "TOSS if >4h in danger zone — strict rule", "infant immune systems get zero margin"),
    (["bread", "tortilla", "bagel", "cake", "cookies", "crackers", "dry goods", "flour"],
     "KEEP", "not perishable; check only for mold from condensation"),
    (["frozen vegetables", "frozen fruit"],
     "REFREEZE if crystals intact; else cook-now or toss", "ice = never entered danger zone"),
    (["frozen meat", "frozen pizza", "frozen meal", "ice cream"],
     "REFREEZE only if hard-frozen/crystals; ice cream: TOSS if soft", "texture loss ok, thaw-and-warm is not"),
]


def cmd_verdict(a):
    h = a.hours
    t = a.fridge_temp  # number F or 'unknown'
    print(f"OUTAGE: {h} hours without power")
    if t == "unknown":
        temp_note = "thermometer reading UNKNOWN -> assume worst case for zones"
        temp = None
    else:
        temp = float(t)
        temp_note = f"thermometer reads {temp:.0f}F"
    print(f"Fridge status: {temp_note}")
    print()

    # FRIDGE
    print("FRIDGE (door kept closed):")
    if h <= 4:
        print(f"  h={h} <= 4h: PASS — perishables safe; door-shelf items cook-first")
    elif h <= 8:
        v = "PARTIAL CULL"
        if temp is not None and temp <= 40:
            print(f"  h={h} but measured {temp:.0f}F <= 40F: PASS — food never entered danger zone")
        else:
            print(f"  h={h}: {v} — toss deli meat, leftovers, fish, dairy;")
            print("    hard cheese/butter/condiments survive. Door-zone = 1h worse.")
    else:
        if temp is not None and temp <= 40:
            print(f"  h={h} but measured {temp:.0f}F <= 40F: PASS with margin")
        else:
            print(f"  h={h} > 8h: FULL PERISHABLE CULL — all meat, dairy, leftovers,")
            print("    cut produce, prepared infant food OUT. Keep: condiments,")
            print("    butter, hard cheese, whole produce, bread/pantry goods.")

    # FREEZER
    print()
    print("FREEZER (door kept closed):")
    if h <= 24:
        full_note = "24h (half-full) / 48h (full) window"
        print(f"  h={h} <= 24h: {full_note} — items safe IF still hard/crystals;")
        print("    verify with crystal check, not by look")
    elif h <= 48:
        print(f"  h={h}: HALF-FULL freezers are past the 24h line — full ones hold;")
        print("    check blocks: hard-frozen core = refreeze; thawed edges = cook or toss")
    else:
        print(f"  h={h} > 48h: assume danger-zone entry unless deeply frozen;")
        print("    anything soft/warm: toss (meat) or cook-immediately (veg)")
    print()
    print("Run `item --name` for borderline calls. Never taste-test anything.")


def cmd_item(a):
    q = a.name.lower()
    for kws, verdict, why in ITEMS:
        if any(k in q for k in kws):
            print(f"'{a.name}':")
            print(f"  → {verdict}")
            print(f"  because: {why}")
            return
    print(f"'{a.name}': no specific rule — default logic:")
    print("  - animal + moist + cooked/handled  => treat as perishable (4h rule)")
    print("  - dry / acidic / fatty / commercial-sealed => keep")
    print("  - 'in doubt' => out (cost of groceries < cost of illness)")


def cmd_refreeze(a):
    s = a.state.lower()
    print(f"State: {a.state}")
    print()
    has_crystals = "crystal" in s and "no crystal" not in s
    if has_crystals:
        print("  VERDICT: REFREEZE-SAFE")
        print("  - was thawing but stayed <=40F with ice crystals")
        print("  - quality (texture) drops; safety holds")
        print("  - label with date; use first")
    elif "cold" in s or "cool" in s or "soft" in s:
        print("  VERDICT: COOK-NOW OR TOSS")
        print("  - cold but no crystals = unknown time in danger zone")
        print("  - if it's veg/fruit: cook immediately; meat/fish: toss")
    elif "hard" in s or "frozen" in s:
        print("  VERDICT: REFREEZE-SAFE")
        print("  - still hard-frozen: never left the safe zone")
        print("  - verify a frozen core; edges may have partially thawed")
    else:
        print("  VERDICT: TOSS")
        print("  - thawed and warm/unknown temp = assume toxin window elapsed")
        print("  - toxins survive refreezing AND cooking")
    print()
    print("Iron rules: refreeze only if <=40F throughout; never refreeze")
    print("thawed ice cream, stuffed poultry/fish, or anything warm.")
    print("Partial thaw is normal — a frozen core counts as crystals.")


DOORSIGN = """# POWER OUTAGE — FRIDGE DOOR SIGN

## Before an outage (do today)
- [ ] Appliance thermometer IN the fridge (target <= 40F / 4C)
- [ ] Freeze water jugs to fill freezer air gaps (full = 48h runway)
- [ ] This sign taped inside the door

## When the power goes out
1. KEEP THE DOORS CLOSED. Fridge: 4h. Freezer: 24h half / 48h full.
2. Note the outage START time on this line: ____:____
3. Do not open "to check" — every open costs ~30 min of runway.

## When power returns — 2-minute triage
- Fridge <= 4h closed:            everything passes
- Fridge 4-8h:                    toss deli meat, leftovers, fish, soft dairy
- Fridge > 8h:                    full perishable cull (keep condiments,
                                  butter, hard cheese, whole produce)
- Freezer: hard/crystals = refreeze-safe; soft = cook now; warm = toss

## TOSS FIRST (highest risk)
deli/lunch meat - leftovers - raw fish - cooked rice/pasta -
soft cheese - shredded cheese - milk/yogurt/cream - cut melon -
prepared infant formula - creamy open dressings

## KEEP (survivors)
butter - hard cheese blocks - commercial mayo/ketchup/mustard -
vinegar pickles - jams/peanut butter - whole produce - bread

NEVER taste-test. When in doubt, throw it out.
"""


def cmd_doorsign(a):
    with open(a.out, "w") as f:
        f.write(DOORSIGN)
    print(f"Wrote {a.out} — print and tape inside the fridge door.")


def main():
    p = argparse.ArgumentParser(description="Post-outage food safety triage (FDA/USDA guidance).")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("verdict")
    s.add_argument("--hours", type=float, required=True)
    s.add_argument("--fridge-temp", default="unknown", help="F reading or 'unknown'")
    s.set_defaults(f=cmd_verdict)
    s = sub.add_parser("item"); s.add_argument("--name", required=True); s.set_defaults(f=cmd_item)
    s = sub.add_parser("refreeze"); s.add_argument("--state", required=True); s.set_defaults(f=cmd_refreeze)
    s = sub.add_parser("doorsign"); s.add_argument("--out", default="door-sign.md"); s.set_defaults(f=cmd_doorsign)
    a = p.parse_args(); a.f(a)


if __name__ == "__main__":
    main()
