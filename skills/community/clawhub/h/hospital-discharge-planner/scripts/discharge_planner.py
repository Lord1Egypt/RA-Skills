#!/usr/bin/env python3
"""Hospital discharge planner — audit, paperwork decode, post-acute math,
72-hour landing plan, caregiver handoff card.

Subcommands:
  audit      7-question discharge-order audit (ask BEFORE signing)
  paperwork  Decode AVS / NOF / MOON / instructions stack
  postacute  Setting decision: home-with-help vs SNF vs IRF + Medicare clocks
  landing    72-hour landing zone: meds, floor, coverage, red-flag sheet
  handoff    Printable caregiver handoff card

Stdlib only. Offline. Patient-advocacy information, not medical advice.
"""
import argparse
import json
from datetime import date, timedelta

AUDIT = [
    ("Meds reconciled?",
     "Line-by-line against the HOME pharmacy list — every change named (start/stop/dose) and WHY. Blood thinners, diabetes meds, diuretics are the danger trio."),
    ("Follow-up BOOKED?",
     "Dates + provider names in writing. 'Someone will call' = not booked. Book PCP within 7-14 days + specialist per condition; call from the hospital room if not."),
    ("Equipment/services ordered AND trained?",
     "Walker/bed/oxygen named supplier + delivery date + a human trained you on it. Verbal 'we'll order home health' = nothing — get the agency + order in the AVS."),
    ("Red flags for THIS condition?",
     "Specific symptoms (fever threshold, wound signs, new confusion, bleeding on anticoagulants) each with who-to-call numbers — clinic / after-hours / 911."),
    ("Activity/wound/diet orders in writing?",
     "Weight limits, driving, stair rules, wound care steps, diet — on paper, not verbal folklore."),
    ("Who owns me until follow-up?",
     "Named responsible clinician between discharge and first visit + their number. 'The ER' is not the answer you want."),
    ("Is the destination actually ready?",
     "Person + meds picked up + bed on the right floor + ride at the REAL discharge time (ask the morning of — '10 am' often means 4 pm)."),
]

DOCS = [
    ("AVS (After-Visit Summary)", "diagnoses, final med list, follow-ups, all orders",
     "PHOTO EVERY PAGE — it travels to every next visit; this is the source of truth"),
    ("Discharge instructions", "activity/wound/diet per condition",
     "fridge copy + one per caregiver"),
    ("NOF (CMS-10123)", "'Medicare may stop paying' for SNF/home-health",
     "signing is NOT agreeing; it opens your appeal window — file fast if you disagree"),
    ("MOON", "observation-status notice (outpatient despite looking admitted)",
     "if receiving hospital-level care as 'observation', this is your appeal hook + ask for status change review"),
    ("Prescriptions", "new meds",
     "route to pharmacy BEFORE leaving the building"),
    ("DME order", "equipment (walker, bed, oxygen)",
     "supplier + delivery date + training confirmed"),
]


def cmd_audit(a):
    print("DISCHARGE-ORDER AUDIT — ask BEFORE signing")
    for i, (q, why) in enumerate(AUDIT, 1):
        print(f"  {i}. {q}")
        print(f"     {why}")
    print()
    print("Any NO = a gap with an owner and a time. Say it: 'What will it take")
    print("to close that before we leave?' If the patient is unsafe to move,")
    print("say THAT: 'I don't believe this discharge is safe — I want to appeal'")
    print("-> case manager + NOF + BFCC/QIO fast review (see references).")
    return {"questions": len(AUDIT)}


def cmd_paperwork(a):
    print("PAPERWORK STACK DECODE")
    for name, what, move in DOCS:
        print(f"  {name}")
        print(f"     is: {what}")
        print(f"     -> {move}")
    print()
    print("STATUS CHECK (do today): 'Is the patient INPATIENT or OBSERVATION today?'")
    print("  Observation breaks SNF coverage (3 inpatient nights required).")
    return {"documents": len(DOCS)}


def cmd_postacute(a):
    print(f"POST-ACUTE SETTING DECISION — nights inpatient: {a.nights}")
    if a.setting == "snf":
        if a.nights < 3:
            print(f"  !! {a.nights} inpatient night(s) < 3-night rule -> SNF days NOT")
            print("     covered by Medicare Part A. Confirm status daily; ask the case")
            print("     manager for a status review or BFCC/QIO appeal if care is")
            print("     hospital-level but flagged observation.")
        else:
            print("  3+ inpatient nights: SNF eligible IF skilled need documented.")
            print("  Day 1-20: $0. Day 21-100: ~$209.50/day coinsurance (2026).")
            print("  Day 101+: full cost. Advantage plans differ — call the plan.")
        print("  Weekly: ask therapy for the progress note; at 'plateaued' pivot to")
        print("  home-health transition BEFORE the last covered day.")
    elif a.setting == "irf":
        print("  IRF needs 3-hours/day therapy tolerance — stroke/SCI/major trauma")
        print("  class. Joint replacement usually goes SNF or home-with-PT now.")
    else:
        print("  HOME-WITH-HELP: usually right when a caregiver exists + patient")
        print("  transfers safely. Home health (SN + PT at home, $0, no day cap")
        print("  while skilled need continues) needs: doctor order + homebound")
        print("  + skilled need. GET THE ORDER IN THE AVS BEFORE DISCHARGE.")
    print()
    print("COVERAGE SANITY: home health $0 vs SNF $209.50/day after day 20 —")
    print("if the family can cover caregiving, home-with-home-health is usually")
    print("the better deal AND the better recovery.")
    return {"setting": a.setting, "nights": a.nights}


def cmd_landing(a):
    print(f"72-HOUR LANDING PLAN — help hours/day: {a.help_hours}, floors: {a.floors}")
    print()
    print("MEDS (night one)")
    for line in (
        "  - Fill new scripts same-day (regular pharmacy on the way home)",
        "  - Times-grid from the reconciled list; organizer loaded weekly",
        "  - OTC interaction check: ibuprofen+anticoagulant, sedating",
        "    antihistamine+opioid are the classic home incidents",
    ):
        print(line)
    print("THE FLOOR")
    if a.floors > 1:
        print(f"  - {a.floors} floors: bedroom on entry level 2 weeks, or stair")
        print("    protocol (up-leads, one flight, nobody carrying anything)")
    else:
        print("  - Single floor: bathroom path at night = motion lights, no rugs,")
        print("    shower chair in place BEFORE arrival")
    print("  - Chair height: firm + armrests; toilet riser if hip/knee protocol")
    print("  - Equipment delivered AND assembled — confirm the morning of")
    print("COVERAGE GRID (honest math)")
    if a.help_hours < 8:
        print(f"  - {a.help_hours} h/day of help is thin: cover nights + mornings")
        print("    first; hire or rotate the gap; fall/wander risk needs a night plan")
    else:
        print(f"  - {a.help_hours} h/day: write the shift grid; give the primary")
        print("    caregiver one protected sleep block")
    print("RED-FLAG SHEET (fridge + every caregiver): condition symptoms with")
    print("  clinic / after-hours / 911 numbers printed; allergies; code status.")
    print("FIRST FOLLOW-UP: transport booked for the real appointment time")
    print("  (appointment + ride both actually exist, right?) + AVS photographed.")
    return {"help_hours": a.help_hours}


def cmd_handoff(a):
    card = f"""# CAREGIVER HANDOFF CARD — {date.today().isoformat()}
Patient: {a.patient}
Primary contact: {a.contact}

CONDITIONS / REASON FOR HOSPITAL STAY:
  [fill: e.g. hip replacement day 3, afib on Eliquis]

ALLERGIES:  [fill — every caregiver must know these]

MEDS + TIMES (from the reconciled discharge list):
  08:00  [med, dose]
  12:00  [med, dose]
  18:00  [med, dose]

RED FLAGS — CALL NUMBERS:
  clinic: [number]   after-hours: [number]   emergency: 911/112
  - fever > [threshold per discharge sheet]
  - wound: spreading redness / drainage / opening
  - new confusion, one-sided weakness, chest pain, unusual bruising
  - falls with head strike on blood thinners = ED NOW

CODE STATUS / DIRECTIVES: [fill]
PCP: [name/number]   SPECIALIST: [name/number]
PHARMACY: [name/number]   INSURANCE ID: [fill]

Keep this with the patient's meds. Update with every change.
"""
    print(card)
    return {"card_lines": card.count(chr(10))}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    for name in ("audit", "paperwork"):
        sp = sub.add_parser(name)
        sp.set_defaults(fn=cmd_audit if name == "audit" else cmd_paperwork)

    sp = sub.add_parser("postacute")
    sp.add_argument("--nights", type=int, default=3,
                    help="inpatient nights (observation doesn't count)")
    sp.add_argument("--setting", default="home-with-help",
                    choices=["home-with-help", "snf", "irf"])
    sp.set_defaults(fn=cmd_postacute)

    sp = sub.add_parser("landing")
    sp.add_argument("--help-hours", type=int, default=6)
    sp.add_argument("--floors", type=int, default=1)
    sp.set_defaults(fn=cmd_landing)

    sp = sub.add_parser("handoff")
    sp.add_argument("--patient", default="[name, age, condition]")
    sp.add_argument("--contact", default="[name, relation, phone]")
    sp.set_defaults(fn=cmd_handoff)

    a = p.parse_args()
    out = a.fn(a)
    if a.json:
        print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
