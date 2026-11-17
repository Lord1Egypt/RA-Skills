#!/usr/bin/env python3
"""Insurance Claim Compass — evidence, letters, depreciation, appeal ladder.

Stdlib only. Not legal advice; timelines/deadlines vary by jurisdiction —
verify with your policy and state/country insurance department.
"""
import argparse
import sys
from datetime import date

# ---------------- knowledge tables ----------------

LOSS_TYPES = {
    "water": {
        "name": "Water damage (burst pipe, overflow, appliance leak)",
        "first24": [
            "Shut off the water at the nearest valve / main; STOP the source",
            "Photograph the source and the failed part BEFORE any repair",
            "Start mitigation NOW: extract water, run fans/dehumidifier (reimbursable — keep receipts)",
            "Do NOT discard the failed part or damaged items until adjuster releases them",
            "Move undamaged property out of the wet zone and photograph the move",
        ],
        "shotlist": [
            "Wide shot of each affected room (establish scale)",
            "Close-up of the failure point / pipe / hose",
            "Water line height on walls and furniture",
            "Warped flooring, stain edges, peeling veneer — mid + close",
            "The failed part itself, next to a ruler if possible",
            "Mitigation in progress (fans, plumber invoice)",
            "Water meter reading (proves leak volume)",
        ],
        "docs": ["plumber invoice", "mitigation/drying invoices", "receipts for damaged items", "policy declarations page"],
    },
    "theft": {
        "name": "Theft / burglary",
        "first24": [
            "File a police report FIRST — insurers require the report number",
            "Do not touch the entry point until photographed",
            "List serial numbers of electronics (box, account, receipt)",
            "Do NOT advertise absence from home on social media",
        ],
        "shotlist": [
            "Forced entry point: broken lock/window — wide + close",
            "Where items were taken from (empty stands, cut cables)",
            "Scene overall condition (proves no other damage)",
        ],
        "docs": ["police report number + copy", "proof of ownership: receipts, card statements, photos of items in use", "serial numbers", "appraisals for jewelry/art if any"],
    },
    "wind": {
        "name": "Wind / hail storm damage",
        "first24": [
            "Prevent further damage: tarp the roof, board openings (keep receipts — reimbursable)",
            "Photograph BEFORE any temporary repair hides the damage",
            "Note the storm date/time from weather service records",
        ],
        "shotlist": [
            "Roof: lifted/missing shingles, bruised shingle marks (hail), close-ups",
            "All building sides — siding dents, broken windows",
            "Date-stamped photos (turn on timestamp or check file EXIF)",
            "Damaged outdoor items, fencing, vehicles",
        ],
        "docs": ["contractor inspection report", "weather report for the date", "tarps/emergency repair receipts", "prior roof age documentation"],
    },
    "fire": {
        "name": "Fire / smoke damage",
        "first24": [
            "Do NOT re-enter until the fire department clears the structure",
            "Begin a room-by-room contents inventory from memory + old photos",
            "Ask about boarding/securing the property (insurer often arranges)",
            "Keep EVERY mitigation and lodging receipt (loss-of-use coverage)",
        ],
        "shotlist": [
            "After clearance: every room, every wall, wide shots",
            "Smoke/soot patterns and water damage from suppression",
            "Remaining recognizable items for the inventory",
        ],
        "docs": ["fire department report number", "inventory with ages and prices", "lodging/meal receipts", "mortgage/lease for occupancy proof"],
    },
    "auto": {
        "name": "Auto collision / comprehensive",
        "first24": [
            "Safety first, then: photos BEFORE cars move (if safe)",
            "Exchange: name, insurer, policy #, plate, VIN, license",
            "Police report or EU 'constat amiable' signed at scene",
            "Say NOTHING about fault — no admissions at the scene",
        ],
        "shotlist": [
            "Full vehicle from all 4 corners (shows orientation)",
            "Close-ups of every damaged panel",
            "License plate + VIN + odometer of all vehicles",
            "Road context: signals, signs, weather, skid marks",
            "Other driver's insurance card",
        ],
        "docs": ["police/constat report", "photos", "witness contacts", "repair estimates"],
    },
    "liability": {
        "name": "Guest injury on your property (liability)",
        "first24": [
            "Get medical help if needed — first, always",
            "Photograph the hazard EXACTLY as it was (lighting, obstacles)",
            "Collect witness names + numbers on the spot",
            "Make NO statements about fault or paying ('I'm sorry' is used against you)",
            "Notify your insurer the same day — late notice can void liability defense",
        ],
        "shotlist": [
            "The hazard wide + close from the visitor's walking path",
            "Lighting conditions at the time of day it happened",
            "Footwear/walkway surface, stairs, handrails",
        ],
        "docs": ["incident notes with times", "witness contacts", "photos", "any communication from the injured party (keep, do not reply substantively)"],
    },
}

ITEM_LIFE_YR = {
    "electronics": 5, "major appliance": 12, "small appliance": 7,
    "furniture": 10, "carpet/flooring": 10, "clothing": 3,
    "bicycle": 7, "power tools": 10, "mattress": 8, "phone": 4,
}

KEYWORD_CLASS = [
    ("tv|laptop|computer|monitor|console|camera|stereo|receiver|speaker", "electronics"),
    ("washer|dryer|refrigerator|fridge|dishwasher|range|oven|furnace|water heater|boiler", "major appliance"),
    ("microwave|blender|toaster|coffee|vacuum|air fryer|mixer", "small appliance"),
    ("carpet|floor|hardwood|laminate|tile|lvp", "carpet/flooring"),
    ("shirt|jacket|coat|dress|shoes|boots|jeans|clothing|pants", "clothing"),
    ("bike|bicycle", "bicycle"),
    ("drill|saw|sander|grinder|tool", "power tools"),
    ("mattress|box spring", "mattress"),
    ("phone|tablet|ipad|watch", "phone"),
    ("sofa|couch|table|chair|desk|bed|dresser|shelf|bookcase|cabinet", "furniture"),
]

# ---------------- helpers ----------------

def classify(item: str) -> str:
    import re
    low = item.lower()
    for pat, cls in KEYWORD_CLASS:
        if re.search(pat, low):
            return cls
    return "furniture"  # conservative default

def acv(price: float, age_yr: float, life_yr: float):
    pct = max(0.10, 1.0 - age_yr / life_yr)
    return price * pct, pct

# ---------------- commands ----------------

def cmd_document(a):
    t = LOSS_TYPES[a.type]
    print(f"=== {t['name'].upper()} — EVIDENCE FILE ===\n")
    print("FIRST 24 HOURS:")
    for i, s in enumerate(t["first24"], 1):
        print(f"  {i}. {s}")
    print("\nPHOTO SHOT-LIST (do before cleanup):")
    for s in t["shotlist"]:
        print(f"  [ ] {s}")
    print("\nDOCUMENTS TO COLLECT:")
    for d in t["docs"]:
        print(f"  [ ] {d}")
    print("\nRULE: mitigate further damage but KEEP damaged items and the failed")
    print("part until the adjuster releases them. Photograph everything first.")
    print("Verify state/country deadlines with your insurer and insurance dept.")

def cmd_letter(a):
    today = date.today().isoformat()
    print(f"""Date: {a.date or today}

To: Claims Department, {a.insurer or "[INSURER NAME]"}
Re: NOTICE OF LOSS — Policy No. {a.policy}

To whom it may concern:

I am reporting a covered loss under the above policy.

  Date of loss:      {a.date or today}
  Type of loss:      {a.loss}
  Location:          {a.location or "[property address]"}
  Description:       {a.loss}. {a.detail or ""}
  Estimated damage:  ${a.amount:.2f} (preliminary, subject to adjustment)

Emergency mitigation has been performed to prevent further damage;
related invoices are available and will be forwarded. I have documented
the loss with photographs and retained the damaged items for inspection.

Please confirm receipt of this notice in writing and advise:
 1. your claim number for this loss;
 2. when an adjuster will inspect;
 3. whether any additional documentation is required at this stage.

I reserve all rights under the policy and applicable law.

Sincerely,
[YOUR NAME]  ·  [ADDRESS]  ·  [PHONE]  ·  [EMAIL]
""")
    print("--- Send by a channel that proves delivery (portal, email with")
    print("read receipt, or certified mail). Keep a copy: this letter starts")
    print("the acknowledgment clock.")

def cmd_value(a):
    cls = classify(a.item)
    life = ITEM_LIFE_YR[cls]
    age = max(0.0, date.today().year - a.purchase)
    acv_v, pct = acv(a.price, age, life)
    print(f"{a.item} → class '{cls}', life {life} yr, purchased {a.purchase} (age {age:.0f} yr)")
    print(f"  Depreciation retained: {(1-pct)*100:.0f}%")
    print(f"  ACV settlement:   ${acv_v:,.2f}")
    if a.rcv:
        print(f"  RCV replacement:  ${a.price:,.2f}")
        print(f"  Recoverable holdback: ${a.price - acv_v:,.2f}")
        print("  → Replace the item, send receipts, reclaim the holdback (RCV policies).")
    else:
        print("  (add --rcv to see the replacement-cost recovery gap)")
    print("Adjusters may deviate; request their itemized depreciation sheet to compare.")

def cmd_timeline(a):
    kind = a.type
    rows = [
        ("Day 0 — report loss (written)", "immediately; late notice can void coverage"),
        ("Acknowledgment + claim number", "typically 10–15 business days (many US states: 15)"),
        ("Adjuster first contact/inspection", "1–3 weeks after notice"),
        ("Coverage decision", "often 30–60 days; some states impose 40–60 day bounds"),
        ("Payment after agreement", "5–15 business days typical"),
        ("Supplemental claims", "usually allowed 1 yr+ if hidden damage appears"),
    ]
    print(f"TYPICAL {kind.upper()} CLAIM TIMELINE (verify for your state/country):")
    for step, when in rows:
        print(f"  {step:42s} {when}")
    print("\nEU note: acknowledgment ~14 days, decision up to 3 months for many")
    print("policies. US: your state Department of Insurance publishes exact bounds.")

def cmd_appeal(a):
    gap = a.estimate - a.offer
    pct = 100.0 * a.offer / a.estimate if a.estimate else 0
    print(f"OFFER ${a.offer:,.2f} vs ESTIMATE ${a.estimate:,.2f} → GAP ${gap:,.2f} (offer = {pct:.0f}% of estimate)\n")
    ladder = [
        "Demand a written ITEMIZED explanation of every deduction and the adjuster's depreciation sheet (set a 7–10 day deadline).",
        "Obtain an independent contractor/appraiser estimate; resubmit with photos and receipts.",
        "Invoke the APPRAISAL CLAUSE (each side hires an appraiser; they pick an umpire; the result binds on amount)." if gap >= 1000 else "Small gap: negotiate from the independent estimate.",
        "File a complaint with the state Department of Insurance (free, tracked; insurers answer quickly).",
        "Public adjuster (fee ~10% of recovery) or attorney consultation for large losses.",
    ]
    print("APPEAL LADDER (climb in order; never argue only by phone):")
    for i, s in enumerate(ladder, 1):
        print(f"  {i}. {s}")
    print(f"""
--- DRAFT LETTER ---
To: Claims Department
Re: Claim No. {a.claim} — objection to settlement offer of ${a.offer:,.2f}

I received your settlement offer of ${a.offer:,.2f} for the loss dated
{a.date or "[date]"}. My documented estimate, supported by attached
photos, receipts and an independent estimate, is ${a.estimate:,.2f}.

Please provide, within 10 business days, a written itemized explanation
of every deduction taken, including the depreciation schedule applied to
each item and the basis for any coverage-portion denial.

I do not accept the offer as final and reserve all rights under the
policy, including invoking the appraisal provision if we cannot resolve
the difference.

Sincerely,
[YOUR NAME]  ·  Policy No. {a.policy or "[policy]"}
""")
    print("Do not sign a release/proof-of-loss you disagree with. Ask what any")
    print("release covers BEFORE signing — signing usually ends the claim.")

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("document", help="evidence checklist + photo shot-list")
    d.add_argument("--type", required=True, choices=sorted(LOSS_TYPES))
    d.set_defaults(fn=cmd_document)

    l = sub.add_parser("letter", help="first notice of loss letter")
    l.add_argument("--type", default="home", help="home|auto|liability")
    l.add_argument("--loss", required=True)
    l.add_argument("--detail", default="")
    l.add_argument("--date", default=None)
    l.add_argument("--policy", default="[POLICY #]")
    l.add_argument("--insurer", default=None)
    l.add_argument("--location", default=None)
    l.add_argument("--amount", type=float, default=0.0)
    l.set_defaults(fn=cmd_letter)

    v = sub.add_parser("value", help="ACV depreciation + RCV gap")
    v.add_argument("--item", required=True)
    v.add_argument("--purchase", type=int, required=True)
    v.add_argument("--price", type=float, required=True)
    v.add_argument("--rcv", action="store_true")
    v.set_defaults(fn=cmd_value)

    t = sub.add_parser("timeline", help="typical milestones")
    t.add_argument("--type", default="home")
    t.set_defaults(fn=cmd_timeline)

    ap = sub.add_parser("appeal", help="lowball/denial ladder + letter")
    ap.add_argument("--reason", default="lowball", choices=["lowball", "denial", "delay"])
    ap.add_argument("--offer", type=float, required=True)
    ap.add_argument("--estimate", type=float, required=True)
    ap.add_argument("--claim", default="[CLAIM #]")
    ap.add_argument("--policy", default=None)
    ap.add_argument("--date", default=None)
    ap.set_defaults(fn=cmd_appeal)

    a = p.parse_args()
    a.fn(a)

if __name__ == "__main__":
    main()
