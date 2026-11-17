#!/usr/bin/env python3
"""
pet_poison_triage.py — first-response toxicity triage for cats & dogs.

Commands:
  triage    Species-aware hazard scoring of a suspected toxin + the
            first-30-minutes protocol (never induce vomiting unless told).
  chocolate Chocolate toxicity math: theobromine mg/kg vs toxic doses
            per product type (baking >> dark >> milk >> white).
  xylitol   Xylitol dose math: hypoglycemia vs AKI thresholds for dogs.
  grapes    Grape/raisin unknown-toxin protocol (ERT unknown, treat as
            any-ingestion for dogs; toxic for cats too).
  plants    Plant toxicity lookup (true lilies = CAT emergency, sago
            palm = dog emergency, etc).
  kit       Pet poison kit checklist + emergency contacts card.

Stdlib only. Offline. NOT a substitute for a vet/poison hotline —
this tool exists to make the call FASTER and better-informed.
"""
import argparse
import json

# ─── Toxin knowledge base ───
# sev: minimal | mild | moderate | severe | deadly
# Notes are action-oriented, species-specific.
TOXINS = {
    "chocolate": {
        "aliases": ["cocoa", "theobromine"],
        "species": {"dog": "severe", "cat": "moderate"},
        "action": "Run `chocolate` command for dose math. Theobromine "
                  "half-life in dogs ~17.5h — symptoms can persist/progress "
                  "for days. Bring wrapper/product.",
        "signs": "vomiting, diarrhea, restlessness, tremors, arrhythmia, seizures",
    },
    "xylitol": {
        "aliases": ["birch sugar", "sugar-free gum", "peanut butter"],
        "species": {"dog": "severe", "cat": "minimal"},
        "action": "Run `xylitol` command. Dogs: hypoglycemia in 10-60 min. "
                  "Do NOT wait for symptoms if >0.1 g/kg suspected. Bring "
                  "the product — xylitol is rarely on the front label "
                  "(look for 'birch sugar' — same compound, renamed).",
        "signs": "vomiting, weakness, stumbling, seizures (dogs)",
    },
    "grapes": {
        "aliases": ["raisin", "raisins", "grape", "sultana", "currant"],
        "species": {"dog": "severe", "cat": "moderate"},
        "action": "Run `grapes` command. Toxic dose is UNKNOWN and "
                  "individual — a single grape has caused AKI. No safe "
                  "amount. Any ingestion = vet, same day, ideally <6h.",
        "signs": "vomiting within 24h, then lethargy, not drinking, "
                 "kidney failure signs at 24-72h",
    },
    "lily": {
        "aliases": ["true lily", "easter lily", "tiger lily", "asiatic lily",
                    "stargazer", "rubrum", "daylily", "lily of the valley"],
        "species": {"cat": "deadly", "dog": "mild"},
        "action": "TRUE lilies (Lilium/Hemerocallis) + CAT = EMERGENCY NOW. "
                  "Even pollen groomed off fur or vase water causes acute "
                  "kidney injury. Run `plants`. GO to ER within 18h max — "
                  "every hour matters; beyond 18-24h prognosis drops hard. "
                  "Note: 'lily of the valley' = cardiac toxin (different "
                  "protocol, still vet-now); peace lily/peruvian lily are "
                  "irritants not kidney toxins.",
        "signs": "cats: drooling, vomiting, then 12-30h: hiding, not "
                 "eating, kidney values rise",
    },
    "sago_palm": {
        "aliases": ["cycad", "coontie", "cardboard palm"],
        "species": {"dog": "deadly", "cat": "deadly"},
        "action": "1-2 seeds can be fatal (liver failure). Vomit-induction "
                  "at vet within 30 min ideal. ANY ingestion = ER now, "
                  "even if asymptomatic — signs lag 2-3 days.",
        "signs": "vomiting (may improve!), then jaundice, bleeding, "
                 "liver failure at 2-3d",
    },
    "antifreeze": {
        "aliases": ["ethylene glycol", "coolant"],
        "species": {"dog": "deadly", "cat": "deadly"},
        "action": "DEADLY at small doses (dog: 4-5 mL/kg, cat: 1.4 mL/kg). "
                  "ER NOW — antidote (fomepizole) works best <8-12h; 'drunk' "
                  "phase passes, then kidney death. Wash paws/fur if walked "
                  "through it. Do not wait.",
        "signs": "drunken gait 30min-12h, then seeming recovery, then "
                 "kidney failure 24-72h",
    },
    "ibuprofen": {
        "aliases": ["advil", "motrin", "nsaid"],
        "species": {"dog": "severe", "cat": "deadly"},
        "action": "Cats: ANY dose is an emergency. Dogs: GI ulcers at "
                  "5-10 mg/kg, kidney risk >25 mg/kg, seizures >100 mg/kg. "
                  "Count pills possibly consumed; bring the bottle.",
        "signs": "vomiting (maybe bloody), black stool, lethargy, seizures",
    },
    "acetaminophen": {
        "aliases": ["tylenol", "paracetamol"],
        "species": {"dog": "severe", "cat": "deadly"},
        "action": "Cats: 10 mg/kg can kill (methemoglobinemia). ER + NAC "
                  "antidote. Dogs: liver damage threshold ~100-150 mg/kg "
                  "but cats are far more sensitive.",
        "signs": "brown/blue gums, face swelling (cats), weakness, "
                 "difficulty breathing",
    },
    "rat_poison": {
        "aliases": ["rodenticide", "d-con", "warfarin", "bromadiolone",
                    "brodifacoum", "cholecalciferol", "bromethalin"],
        "species": {"dog": "severe", "cat": "severe"},
        "action": "Bring the PACKAGE — antidote depends on type: "
                  "anticoagulants (vit K1, signs delayed 3-5 DAYS), "
                  "cholecalciferol (calcium spiral), bromethalin (brain "
                  "swelling, NO antidote). 'Wait and see' is the trap: "
                  "asymptomatic now ≠ safe.",
        "signs": "anticoagulant: pale gums, bleeding, bruises, blood in "
                 "urine — days later",
    },
    "onion_garlic": {
        "aliases": ["allium", "onions", "garlic", "chives", "leek", "powder"],
        "species": {"dog": "moderate", "cat": "severe"},
        "action": "Oxidative damage to red blood cells; signs DELAYED "
                  "1-5 days. Onion powder in baby food/soup is "
                  "concentrated. Dose matters: onion >0.5% of body weight. "
                  "Vet for CBC check if significant amount.",
        "signs": "lethargy, pale/yellowish gums, red-brown urine, "
                 "panting (delayed)",
    },
    "alcohol": {
        "aliases": ["ethanol", "beer", "wine", "yeast dough"],
        "species": {"dog": "moderate", "cat": "moderate"},
        "action": "Yeast dough is double trouble (ferments ethanol AND "
                  "expands). Raw dough = ER. Mild alcohol sip in a large "
                  "dog: call hotline; small dog or cat: vet.",
        "signs": "stumbling, low body temp, slow breathing, coma risk",
    },
    "caffeine": {
        "aliases": ["coffee", "energy drink", "espresso", "caffeine pills"],
        "species": {"dog": "moderate", "cat": "moderate"},
        "action": "Similar to theobromine but faster. Pills and espresso "
                  "are the dangerous forms. See chocolate math for scale.",
        "signs": "restlessness, racing heart, tremors",
    },
    "macadamia": {
        "aliases": ["macadamia nuts", "hawaii nuts"],
        "species": {"dog": "moderate", "cat": "unknown"},
        "action": "Dogs: hind-end weakness, tremors, fever — unpleasant "
                  "but rarely fatal; vet if large amount. Often combined "
                  "with chocolate (cookies) — run chocolate math too.",
        "signs": "wobbly hind legs, tremors, fever (dogs, 12h)",
    },
    "lily_of_valley": {
        "aliases": ["convallaria"],
        "species": {"dog": "severe", "cat": "severe"},
        "action": "Cardiac glycosides (like digoxin) — arrhythmia risk. "
                  "Any ingestion: vet now; bring plant if potted.",
        "signs": "vomiting, slow/irregular pulse, weakness",
    },
    "azalea_rhododendron": {
        "aliases": ["rhododendron", "azalea"],
        "species": {"dog": "moderate", "cat": "moderate"},
        "action": "Grayanotoxins; a few leaves usually GI upset, large "
                  "amounts cardiac/neuro. Vet if more than a mouthful.",
        "signs": "drooling, vomiting, weakness, slow heart",
    },
    "diffenbachia": {
        "aliases": ["dumb cane", "pothos", "philodendron", "peace lily"],
        "species": {"dog": "mild", "cat": "mild"},
        "action": "Calcium oxalate crystals: oral pain, drooling — rinse "
                  "mouth, offer milk/yogurt or water; usually not "
                  "systemic. Vet if swelling blocks breathing.",
        "signs": "intense oral pain, drooling, pawing at mouth",
    },
    "avocado": {
        "aliases": ["persin", "guacamole"],
        "species": {"dog": "mild", "cat": "mild"},
        "action": "Persin hits birds/horses/rabbits hard; dogs/cats: GI "
                  "upset at most; the PIT is the real danger (choking/"
                  "obstruction). Watch stool for pit passage.",
        "signs": "vomiting, diarrhea",
    },
}

PRODUCTS = {  # chocolate: theobromine mg per gram
    "baking_chocolate": 16.0, "cocoa_powder": 20.0,
    "dark_70": 8.0, "dark": 5.5, "semisweet_chips": 5.0,
    "milk": 1.5, "white": 0.02,
}

PLANT_LOOKUP = {
    "true lily": "lily", "easter lily": "lily", "tiger lily": "lily",
    "asiatic lily": "lily", "stargazer": "lily", "oriental lily": "lily",
    "daylily": "lily", "rubrum": "lily", "lilium": "lily", "hemerocallis": "lily",
    "sago palm": "sago_palm", "cycad": "sago_palm",
    "lily of the valley": "lily_of_valley", "convallaria": "lily_of_valley",
    "azalea": "azalea_rhododendron", "rhododendron": "azalea_rhododendron",
    "dieffenbachia": "diffenbachia", "dumb cane": "diffenbachia",
    "pothos": "diffenbachia", "philodendron": "diffenbachia",
    "peace lily": "diffenbachia",
}

SEV_RANK = {"minimal": 0, "mild": 1, "moderate": 2, "severe": 3, "deadly": 4}
SEV_ICON = {"minimal": "·", "mild": "+", "moderate": "++",
            "severe": "+++ CALL VET NOW", "deadly": "++++ ER NOW — MINUTES MATTER"}


def find_toxin(q):
    q = " " + q.lower().strip() + " "
    for key, t in TOXINS.items():
        if key.replace("_", " ") in q:
            return key
        for al in t["aliases"]:
            if len(al) <= 3:
                if f" {al} " in q:
                    return key
            elif al in q:
                return key
    for alias, key in PLANT_LOOKUP.items():
        if alias in q:
            return key
    return None


def cmd_triage(a):
    key = find_toxin(a.toxin)
    if not key:
        print(f"'{a.toxin}' not in knowledge base. Default protocol:")
        print("1. Call ASPCA Poison Control 888-426-4435 or Pet Poison Helpline 855-764-7661 (fee ~$65-85).")
        print("2. Do NOT induce vomiting unless a professional tells you to.")
        print("3. Estimate amount + time; secure the product/wrapper.")
        print("4. If gum color pale/blue/yellow, breathing hard, collapsing: ER now.")
        return
    t = TOXINS[key]
    sev = t["species"].get(a.species, "unknown")
    print(f"HAZARD: {key.upper()} — {a.species}")
    print(f"Severity for {a.species}: {SEV_ICON.get(sev, sev)}")
    if sev in ("severe", "deadly"):
        print("\nHOTLINE/VET FIRST — while on the phone:")
        print("  ASPCA Animal Poison Control: (888) 426-4435  (US, ~$75 consult)")
        print("  Pet Poison Helpline: (855) 764-7661  (~$85, incl. follow-ups)")
    print(f"\nACTION: {t['action']}")
    print(f"\nWATCH FOR: {t['signs']}")
    print("\nFirst 30 minutes, in order:")
    print("  1. Remove pet from the toxin; secure the product/wrapper.")
    print("  2. Do NOT induce vomiting, do NOT give salt/milk/oil (old advice, harmful).")
    print("  3. If toxin on FUR/PAWS: wash with dish soap + warm water, dry —")
    print("     cats will groom it off (that's how they get poisoned).")
    print("  4. Estimate: what, how much, when. Weigh the pet if unsure.")
    print("  5. Call hotline or ER with those numbers. Bring the wrapper.")
    print("  6. If instructed to ER: bring product, packaging, and a fresh urine sample if easy.")


def cmd_chocolate(a):
    # theobromine thresholds (dogs): 20 mg/kg mild, 40-50 moderate, 60 severe
    tb = PRODUCTS.get(a.product)
    if tb is None:
        print(f"Unknown product '{a.product}'. Options: {', '.join(PRODUCTS)}")
        return
    tbmg = a.grams * tb
    perkg = tbmg / a.weight_kg
    if perkg < 20:
        verdict = "below symptom threshold — monitor, expect nothing or mild GI upset"
        plan = "Watch 12-24h. Call hotline only if vomiting/diarrhea starts."
    elif perkg < 40:
        verdict = "MILD range: vomiting, diarrhea, restlessness"
        plan = "Call hotline now (decontamination timing decision); vet if symptoms."
    elif perkg < 60:
        verdict = "MODERATE: tremors, arrhythmia risk — vet visit now"
        plan = "ER/hotline NOW; induced vomiting likely within 1-2h window."
    else:
        verdict = "SEVERE: seizures, arrhythmia — ER NOW"
        plan = "ER immediately. Bring wrapper. Do not wait for symptoms."
    print(f"Chocolate triage — {a.species}, {a.weight_kg} kg")
    print(f"Product: {a.product} ({tb} mg theobromine/g) x {a.grams} g "
          f"= {tbmg:,.0f} mg theobromine = {perkg:,.0f} mg/kg")
    print(f"Verdict: {verdict}")
    print(f"Plan: {plan}")
    if a.species != "dog":
        print(f"Note: thresholds are canine; cats are MORE sensitive per kg —")
        print("treat one band higher and call the hotline.")


def cmd_xylitol(a):
    # dogs: hypoglycemia >=0.1 g/kg; AKI >=0.5 g/kg
    gkg = a.grams / a.weight_kg
    if gkg < 0.1:
        verdict = "below hypoglycemia threshold — monitor, syrup-of-choice check"
        plan = "Feed a small meal; watch for stumbling/weakness 12h. Hotline call reasonable."
    elif gkg < 0.5:
        verdict = "HYPOGLYCEMIA range (>=0.1 g/kg) — blood sugar crash 10-60 min"
        plan = ("Vet NOW (do not wait for symptoms). Bring gum/product. "
                "If already stumbling: rub corn syrup on GUMS (not swallowed) "
                "en route.")
    else:
        verdict = "ACUTE KIDNEY INJURY range (>=0.5 g/kg) — deadly tier"
        plan = "ER NOW. 48h monitoring likely (glucose + kidney values)."
    print(f"Xylitol triage — dog, {a.weight_kg} kg, {a.grams} g xylitol = {gkg:.3f} g/kg")
    print(f"Verdict: {verdict}")
    print(f"Plan: {plan}")
    if not a.pure:
        print("\nIf grams are PRODUCT weight (gum etc.), xylitol is ~0.3-1 g/piece "
              "in sugar-free gum — count PIECES and re-run with the estimated "
              "xylitol grams (piece count x ~0.4 g).")


def cmd_grapes(a):
    print(f"Grape/raisin triage — {a.species}")
    if a.species == "dog":
        print("Toxin is UNKNOWN; individual sensitivity varies wildly — there is")
        print("NO established safe dose. Treat ANY confirmed ingestion as toxic:")
        print("  <6h since ingestion: vet for induced vomiting + 48-72h kidney")
        print("  monitoring (SDMA/creatinine). Do not 'wait and see'.")
        print("  If already vomiting: ER now — that's the early sign, window closing.")
    else:
        print("Cats: documented cases exist (AKI), rarer than dogs. Confirmed")
        print("ingestion = vet same day, baseline kidney values + 48-72h monitoring.")
    print("Bring the box/bag (organic vs conventional doesn't change protocol).")


def cmd_plants(a):
    q = a.plant.lower()
    hits = [(k, v) for k, v in PLANT_LOOKUP.items() if k in q or q in k]
    if not hits:
        print("Plant not in table. Rule of thumb: 'lily' + cat = treat as TRUE")
        print("lily until a vet/pro identifies it. Keep the plant for ID.")
        return
    for alias, key in hits:
        t = TOXINS[key]
        for sp in ("cat", "dog"):
            sev = t["species"].get(sp, "unknown")
            print(f"{alias} ({key}) — {sp}: {SEV_ICON.get(sev, sev)}")
        print(f"  ACTION: {t['action']}\n")


def cmd_kit(a):
    print("PET POISON KIT — keep in one box, check every 6 months")
    for line in [
        "3% hydrogen peroxide (UNOPENED, expires!) — vomit induction, DOGS only, only when told",
        "dish soap (fur decontamination), disposable gloves",
        "bulb syringe / large oral syringe (dosing)",
        "corn syrup (hypoglycemia rescue — gums, not swallowed)",
        "digital kitchen scale (dose math needs weight)",
        "muzzle or towel wrap (pain/fear bites — even from your pet)",
        "carrier; leash; old towel",
        "saline eye rinse (splash exposures)",
        "list: vet, nearest 24/7 ER, ASPCA (888) 426-4435, Pet Poison Helpline (855) 764-7661",
    ]:
        print("  - " + line)
    print("\nEMERGENCY CARD (photo on every phone in the house):")
    print("  Pet: ____  Weight: ____ kg  Conditions: ____  Meds: ____")
    print("  Vet: ____  24/7 ER: ____  Hotlines above. Rabies tag # ____")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("triage", help="hazard + first-30-min protocol")
    t.add_argument("toxin")
    t.add_argument("--species", choices=["dog", "cat"], default="dog")
    c = sub.add_parser("chocolate", help="theobromine mg/kg math")
    c.add_argument("--product", default="milk", choices=sorted(PRODUCTS))
    c.add_argument("--grams", type=float, required=True)
    c.add_argument("--weight-kg", type=float, required=True, dest="weight_kg")
    c.add_argument("--species", choices=["dog", "cat"], default="dog")
    x = sub.add_parser("xylitol", help="hypoglycemia/AKI thresholds (dogs)")
    x.add_argument("--grams", type=float, required=True,
                   help="xylitol grams (or product grams + note)")
    x.add_argument("--weight-kg", type=float, required=True, dest="weight_kg")
    x.add_argument("--pure", action="store_true",
                   help="grams are pure xylitol, not product weight")
    g = sub.add_parser("grapes", help="unknown-toxin protocol")
    g.add_argument("--species", choices=["dog", "cat"], default="dog")
    p = sub.add_parser("plants", help="plant lookup")
    p.add_argument("plant")
    sub.add_parser("kit", help="poison kit + emergency card")
    a = ap.parse_args()
    {"triage": cmd_triage, "chocolate": cmd_chocolate, "xylitol": cmd_xylitol,
     "grapes": cmd_grapes, "plants": cmd_plants, "kit": cmd_kit}[a.cmd](a)


if __name__ == "__main__":
    main()
