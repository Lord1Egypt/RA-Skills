#!/usr/bin/env python3
"""Household Illness Containment — stop one sick kid from becoming five.

When norovirus, flu, COVID, strep or RSV walks in the door, households
default to shared bathrooms, shared towels and shared fate. This tool
prints a dated, illness-specific containment protocol: isolation window,
who is on the exposure clock and until when, WHICH disinfectant actually
kills the pathogen (norovirus laughs at hand sanitizer and quats —
bleach at the right dilution), laundry/dish handling, bathroom rotation,
return-to-school/work clocks, protection for high-risk members, and the
red flags that end the home protocol.

Usage:
  containment_planner.py --illness norovirus --first-symptom 2026-11-22
  containment_planner.py --illness flu --first-symptom 2026-11-20 \
      --today 2026-11-24 --infant --elderly
  containment_planner.py --illness covid --first-symptom 2026-11-22 --food-handler

stdlib only. Educational protocol builder, not medical advice.
"""
import argparse
import sys
from datetime import date

# pathogen cards — windows are rule-of-thumb public-health guidance
ILLNESS = {
    "norovirus": {
        "label": "norovirus (vomiting/diarrhea)",
        "typical_days": (1, 3),
        "contagious": "symptomatic + 48 h after symptoms stop",
        "shed": "virus sheds in stool ~2 weeks — soap vigilance the whole time",
        "incubation": (0.5, 2),   # days after exposure
        "return": "48 h after last symptom; FOOD HANDLERS 48-72 h (state rules)",
        "disinfect": "bleach",
        "sanitizer": "INEFFECTIVE — alcohol hand sanitizer does not reliably "
                     "kill norovirus; soap + running water 20 s does",
        "kitchen": "no shared towels, dedicated utensils; bleach the sink "
                   "and faucet handles; sick person does NOT cook",
        "laundry": "gloves for soiled items; do NOT shake; hot water wash + "
                   "dryer; bleach-safe items get bleach",
        "laundry_c": "hot (60°C/140°F) + full dryer cycle",
        "flags": ["no urine output / dry mouth / no tears (dehydration)",
                  "vomiting everything for >24 h",
                  "blood in vomit/stool",
                  "severe abdominal pain or high fever with the GI illness",
                  "infant <3 mo with fever ≥100.4F/38C"],
    },
    "flu": {
        "label": "influenza",
        "typical_days": (3, 7),
        "contagious": "day 0 (before symptoms!) through ~5-7 days",
        "shed": "contagiousness peaks day 2-3; kids shed longer",
        "incubation": (1, 4),
        "return": "fever-free 24 h without fever reducers + energy to last "
                  "a school day",
        "disinfect": "any",
        "sanitizer": "effective — 60%+ alcohol or soap",
        "kitchen": "dedicated mug/utensils; dishwasher hot cycle; no shared "
                   "towels",
        "laundry": "normal wash fine; hot preferable; don't hug the hamper",
        "laundry_c": "warm-hot + dryer",
        "flags": ["breathing hard/fast, ribs pulling in",
                  "fever >104F / bluish lips",
                  "chest pain, confusion, not waking",
                  "improving then relapsing with fever+cough (secondary infection)",
                  "infant <3 mo with fever ≥100.4F/38C"],
    },
    "covid": {
        "label": "COVID-19",
        "typical_days": (2, 10),
        "contagious": "roughly days 0-5 (worse with worse symptoms)",
        "shed": "isolate through day 5 minimum, then mask to day 10",
        "incubation": (2, 5),
        "return": "≥24 h fever-free + improving + at least 5 days, then a "
                  "well-fitting mask through day 10",
        "disinfect": "any",
        "sanitizer": "effective — 60%+ alcohol or soap",
        "kitchen": "dedicated dishes; ventilate shared air (open windows, "
                   "fan exhausting outward)",
        "laundry": "normal; gloves if heavily soiled",
        "laundry_c": "warm + dryer",
        "flags": ["trouble breathing / persistent chest pain",
                  "SpO2 ≤ 94% on a home oximeter",
                  "confusion, blue lips, can't stay awake",
                  "improving then suddenly worse"],
    },
    "strep": {
        "label": "strep throat",
        "typical_days": (1, 3),
        "contagious": "until ~24 h of effective antibiotics",
        "shed": "test household contacts with new sore throats",
        "incubation": (2, 5),
        "return": "24 h on antibiotics + fever gone + feeling functional",
        "disinfect": "any",
        "sanitizer": "effective",
        "kitchen": "replace/shared toothbrush 24 h into antibiotics; "
                   "dedicated cups",
        "laundry": "hot wash bedding + the sick pillow",
        "laundry_c": "hot + dryer",
        "flags": ["drooling, can't swallow liquids",
                  "difficulty breathing",
                  "sandpaper rash + fever (scarlet fever)",
                  "urine the color of cola (post-strep kidneys)"],
    },
    "cold": {
        "label": "common cold",
        "typical_days": (5, 10),
        "contagious": "first ~3-4 days of symptoms",
        "shed": " contagiousness fades with symptoms",
        "incubation": (1, 3),
        "return": "fever-free + able to manage tissues/cough",
        "disinfect": "any",
        "sanitizer": "effective",
        "kitchen": "basic: no shared cups/towels",
        "laundry": "normal",
        "laundry_c": "normal",
        "flags": ["symptoms >10 days without improvement",
                  "fever after day 5 (think sinus/ear infection)",
                  "wheezing in an asthmatic"],
    },
    "rsv": {
        "label": "RSV",
        "typical_days": (4, 8),
        "contagious": "3-8 days (longer in infants/immunocompromised)",
        "shed": "",
        "incubation": (2, 8),
        "return": "fever-free + breathing comfortable",
        "disinfect": "any",
        "sanitizer": "effective",
        "kitchen": "keep infants away from the sick person entirely",
        "laundry": "normal, hot for infant-contact linens",
        "laundry_c": "hot for infant linens",
        "flags": ["INFANT: flaring nostrils, grunting, ribs pulling in, "
                  "pauses in breathing",
                  "infant <3 mo with ANY breathing trouble — same-day eval",
                  "not drinking — dehydration in infants is fast"],
    },
    "pinkeye": {
        "label": "conjunctivitis",
        "typical_days": (3, 7),
        "contagious": "viral: while eyes water/matter; bacterial: 24 h "
                      "after drops",
        "shed": "",
        "incubation": (1, 3),
        "return": "bacterial: 24 h on drops; viral: until discharge "
                  "resolves (schools vary)",
        "disinfect": "any",
        "sanitizer": "effective",
        "kitchen": "separate towels/washcloths — THE vector",
        "laundry": "hot wash towels + pillowcases daily",
        "laundry_c": "hot + dryer",
        "flags": ["eye pain with light, vision change",
                  "eyelid swelling shut with fever",
                  "contact-lens wearer: remove lenses, call same day"],
    },
}

BLEACH = {
    "note": "make fresh; bleach solution loses potency within 24 h",
    "heavy": "3/4 cup household bleach (5-6%) per gallon ≈ 5000 ppm — "
             "vomit/stool contamination",
    "light": "1/3 cup per gallon ≈ 1000 ppm — routine surfaces",
    "contact": "wet the surface visibly, keep it wet ≥1 min (5 for "
               "norovirus), air dry",
}

HIGH_RISK = {
    "infant": "infant in house",
    "pregnant": "pregnant household member",
    "elderly": "adult 65+",
    "immunocompromised": "immunocompromised member",
}


def d(s):
    try:
        return date.fromisoformat(s)
    except ValueError:
        raise SystemExit(f"bad date '{s}' (YYYY-MM-DD)")


def hr(t):
    print("\n" + "=" * 62)
    print(t)
    print("=" * 62)


def main():
    p = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    p.add_argument("--illness", required=True, choices=sorted(ILLNESS))
    p.add_argument("--first-symptom", required=True, help="YYYY-MM-DD")
    p.add_argument("--today", default=None, help="YYYY-MM-DD")
    p.add_argument("--symptom-free-since", default=None,
                   help="YYYY-MM-DD last symptom ended")
    p.add_argument("--household", type=int, default=4)
    p.add_argument("--shared-bathroom", action="store_true",
                   help="no dedicated sick bathroom available")
    p.add_argument("--food-handler", action="store_true",
                   help="sick (or exposed) person works with food")
    for k, v in HIGH_RISK.items():
        p.add_argument(f"--{k}", action="store_true", help=v)
    a = p.parse_args()

    ill = ILLNESS[a.illness]
    d0 = d(a.first_symptom)
    ref = d(a.today) if a.today else date.today()
    day = (ref - d0).days

    hr(f"CONTAINMENT PROTOCOL — {ill['label'].upper()}")
    print(f"First symptom ............. {d0.isoformat()}")
    print(f"Today (day {day}) ........... {ref.isoformat()}")
    lo, hi = ill["typical_days"]
    print(f"Typical course ............ {lo}-{hi} days")
    print(f"Contagious window ......... {ill['contagious']}")
    if ill["shed"]:
        print(f"Shedding note ............. {ill['shed']}")
    inc_lo, inc_hi = ill["incubation"]
    watch_start = d0.fromordinal(d0.toordinal() + int(inc_lo))
    watch_end = d0.fromordinal(d0.toordinal() + int(inc_hi))
    print(f"Household exposure watch .. {watch_start.isoformat()} → "
          f"{watch_end.isoformat()} (incubation {inc_lo}-{inc_hi} d)")
    print(f"Household size ............ {a.household}")

    # phase
    if day < 0:
        phase = "PRE-ONSET (exposure ahead?)"
    elif day <= hi:
        phase = f"ACUTE — expect symptoms through ~day {hi}"
    else:
        phase = "EXPECTED RECOVERY — confirm symptoms actually stopped"
    sf = d(a.symptom_free_since) if a.symptom_free_since else None
    if sf:
        lift = sf.fromordinal(sf.toordinal() + 2)
        phase = (f"SYMPTOM-FREE since {sf.isoformat()} — "
                 f"48 h gate lifts {lift.isoformat()}")

    hr("PHASE")
    print(phase)

    # disinfection
    hr("DISINFECTION — what actually kills it")
    if ill["disinfect"] == "bleach":
        print("This pathogen is non-enveloped and SURVIVES common wipes:")
        print(f"  • HEAVY mix: {BLEACH['heavy']}")
        print(f"  • ROUTINE:   {BLEACH['light']}")
        print(f"  • Contact:   {BLEACH['contact']}")
        print(f"  • {BLEACH['note']}")
        print("  • Quat wipes / 'kills 99.9%' sprays are NOT enough here.")
        print("  • Hard non-porous targets: toilet flush+seat, sink+faucet,")
        print("    door+light knobs, phone, remote, game controllers.")
        print("  • Soft surfaces: vacuum, steam where possible; porous items")
        print("    may need to be retired (norovirus is a survivor).")
    else:
        print("Enveloped/fragile virus — standard disinfection works:")
        print("  • EPA-registered disinfectant, 60%+ alcohol, or soap+water")
        print("  • hit the high-touch set: toilet, sink, knobs, phone,")
        print("    remote, game controllers, fridge handle.")
    print(f"\nHAND HYGIENE: {ill['sanitizer']}.")

    # rooms
    hr("HOUSE RULES")
    print(f"• Sick room: door closed, own bedding, own water glass,")
    print(f"  tray for dishes; sick person masked if they must emerge.")
    if a.shared_bathroom:
        print("• BATHROOM IS SHARED — the highest-risk compromise. Rotate:")
        print("  - sick user LAST before a dedicated clean pass, or")
        print("    dedicated times; wipe seat/flush/seat knobs after")
        print("    sick use (bleach if GI illness);")
        print("  - separate towel PER PERSON (paper towels ideal);")
        print("  - toothbrushes capped, distanced, never touching.")
    else:
        print("• Dedicate one bathroom to the sick if at all possible.")
    print(f"• Kitchen: {ill['kitchen']}.")
    print(f"• Laundry: {ill['laundry']} ({ill['laundry_c']}).")
    print("• Dishes: dedicated set for the sick; dishwasher hot cycle,")
    print("  or wash with gloves + hot soapy water.")

    # return-to-life clock
    hr("RETURN CLOCK")
    print(f"{ill['return']}.")
    if a.food_handler:
        print("\nFOOD-HANDLER override: you may not handle food while")
        print("symptomatic; most jurisdictions add 48-72 h after norovirus")
        print("resolution specifically. Tell your manager — sending yourself")
        print("in starts an outbreak you'll be famous for.")
    if day >= 0:
        est = d0.fromordinal(d0.toordinal() + hi)
        print(f"\nEarliest realistic return on this course: ~{est.isoformat()}"
              " (subject to the rules above, not the calendar).")

    # high risk
    risks = [k for k in HIGH_RISK if getattr(a, k)]
    if risks:
        hr("HIGH-RISK MEMBERS — protection routing")
        if "infant" in risks:
            print("• INFANT: keep out of the sick room entirely; feeding")
            print("  caregiver washes hands + changes outer layer before")
            print("  every feed. Any fever ≥100.4F in <3 months = same-day")
            print("  medical eval, not a home protocol. RSV + infant =")
            print("  count breaths; >50-60/min or ribs pulling in → urgent.")
        if "pregnant" in risks:
            print("• PREGNANT: same household OK with masking + distance;")
            print("  fever ≥100.4F is NOT 'just ride it out' in pregnancy —")
            print("  call the OB same day (they may want antivirals early).")
        if "elderly" in risks:
            print("• 65+: flu/COVID in this group earns an early call —")
            print("  antivirals work best within 48 h of symptoms; consider")
            print("  separate meals and TV for the duration.")
        if "immunocompromised" in risks:
            print("• IMMUNOCOMPROMISED: treat household exposure as serious;")
            print("  mask BOTH directions, separate rooms, separate bathroom;")
            print("  call their care team at exposure, not at symptoms.")

    # red flags
    hr("RED FLAGS — stop home care, get help")
    for fl in ill["flags"]:
        if fl:
            print(f"• {fl}")
    print("• Any doubt: urgent line/nurse line exists for exactly this.")

    hr("CONTAINMENT KIT (one store run, gloves on)")
    kit = ["household bleach (new bottle if yours is >3 months old)",
           "disposable gloves + paper towels",
           "ORS/electrolyte drinks (Pedialyte/sports dilution)",
           "thermometer + batteries; masks (sick + caregivers)",
           "soap refills + laundry detergent",
           "bland foods: rice, toast, bananas, broth, crackers"]
    if ill["disinfect"] == "bleach":
        kit += ["bucket + measuring cup for bleach dilutions"]
    for k in kit:
        print(f"• {k}")

    print("\n" + "-" * 62)
    print("Educational protocol builder from public-health guidance —")
    print("not medical advice. Windows are rules of thumb; your doctor,")
    print("school policy and local health department outrank this file.")
    print("-" * 62)
    return 0


if __name__ == "__main__":
    sys.exit(main())
