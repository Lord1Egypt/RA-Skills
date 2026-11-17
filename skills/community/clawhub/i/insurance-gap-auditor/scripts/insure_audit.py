#!/usr/bin/env python3
"""Insurance Gap Auditor — scenario engine, exclusion checklist, liability
sizing, and a policy-inventory gap audit for personal insurance.

Educational tool: encodes market-typical patterns (US personal lines,
UK/EU notes). Policies vary — output is questions for your agent.
Stdlib-only.
"""
import argparse
import json
import os
import sys
from datetime import date

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "policies.json")

SCENARIOS = [
    # (id, group, title, what happens, responds, typical gap, ask)
    ("kitchen-fire", "home", "Kitchen fire (own home)",
     "Fire starts in your kitchen; smoke damage beyond the room.",
     "Home: dwelling + contents (loss of use pays temp housing)",
     "ACV settlement on contents/roof if policy lacks replacement-cost",
     "Do I have replacement-cost on contents and dwelling?"),
    ("fire-spread", "liability", "Fire spreads to neighbor's property",
     "Your fire damages the adjacent house.",
     "Home liability section",
     "$100-300k limits vs rebuild cost of neighbor's home",
     "Is my liability limit at least my net worth?"),
    ("flood", "home", "Flood (external water enters)",
     "River/storm surge/heavy runoff enters the dwelling.",
     "NOT standard home insurance — separate NFIP/private flood policy",
     "Most-discovered denial: 'water damage' policies exclude flood",
     "Am I in a flood zone? What would a flood policy cost?"),
    ("sewer-backup", "home", "Sewer/drain backup",
     "Water pushes back through drains after heavy rain.",
     "Home ONLY IF water-backup endorsement exists",
     "Rider often absent or $5k limit vs finished-basement loss",
     "Do I have water backup & sump overflow? At what limit?"),
    ("sump-fail", "home", "Sump pump failure",
     "Pump dies during storm; basement floods from below.",
     "Water-backup endorsement (same rider as sewer backup)",
     "Same gap as sewer backup",
     "Is sump overflow included in my backup rider?"),
    ("jewelry-theft", "home", "Jewelry/furs/watches theft",
     "Burglary takes jewelry, watches, furs.",
     "Contents — but with $1,000-2,000 sub-limit category caps",
     "Sub-limit far below real value unless items are scheduled",
     "Should I schedule specific items with appraisals?"),
    ("home-office", "home", "Home business equipment",
     "Business laptops/inventory damaged or stolen from home.",
     "Contents with ~$2,500 business-property sub-limit",
     "Real business gear exceeds sub-limit; liability excluded",
     "Do I need a home-business endorsement or BOP policy?"),
    ("dog-bite", "liability", "Dog bite (guest / postal worker)",
     "Your dog bites a visitor.",
     "Home liability (auto if in car)",
     "Breed exclusions; claims follow the dog across insurers",
     "Is my dog's breed excluded? What's my liability limit?"),
    ("trampoline", "liability", "Trampoline / pool injury (neighbor kid)",
     "Attractive-nuisance injury to a trespassing child.",
     "Home liability — IF not excluded and safety requirements met",
     "Many insurers exclude trampolines or require fencing/locks",
     "Is my pool/trampoline compliant and covered?"),
    ("ebike", "home", "E-bike / Class-3 scooter theft or accident",
     "750W e-bike stolen, or you injure a pedestrian riding it.",
     "Typically NEITHER home (motorized vehicle exclusion) NOR auto",
     "Needs separate bike policy or endorsement; liability often bare",
     "How is my e-bike covered for theft AND liability?"),
    ("teen-driver", "auto", "Teen driver in family car",
     "16-year-old crashes the family SUV.",
     "Auto policy (permissive use of family vehicle)",
     "Rate/class must be updated; unlisted-driver exclusions",
     "Is my teen listed? What happens to rates after a claim?"),
    ("borrowed-car", "auto", "You crash a borrowed/rental car",
     "Driving a friend's car with permission; at-fault crash.",
     "Owner's policy responds first; yours secondary",
     "Non-owned-car liability gaps; rental CDW vs your coverage",
     "Does my policy extend to rentals and borrowed cars?"),
    ("wind-hail", "home", "Wind/hail roof damage",
     "Storm tears shingles; water follows.",
     "Home policy (named-peril or all-risk)",
     "Hurricane/wind percentage deductibles (1-5% of dwelling!)",
     "What is my wind/hail deductible in dollars?"),
    ("earthquake", "home", "Earthquake",
     "Quake cracks foundation.",
     "Rider/CEA policy only — excluded everywhere standard",
     "Denied unless separate earthquake endorsement",
     "Should I price an earthquake rider here?"),
    ("laptop-abroad", "travel", "Laptop lost on trip abroad",
     "Bag lost/damaged in transit or stolen from hotel.",
     "Travel insurance or home contents off-premises sub-limit (~10%)",
     "Off-premises caps; travel policy electronics limits",
     "What's my off-premises contents limit? Travel policy?"),
]

RIDERS = {
    "home": [
        ("Water backup & sump overflow", "$50-250/yr", "closes sewer-backup, sump-fail"),
        ("Scheduled personal property (floater)", "$1-3/$100/yr", "closes jewelry-theft"),
        ("Replacement-cost contents endorsement", "included-modest", "closes depreciation gap"),
        ("Extended replacement cost (dwelling +25-50%)", "modest", "rebuild inflation guard"),
        ("Ordinance or law (code upgrade)", "modest", "rebuild to current code"),
        ("Home business endorsement", "$100-300/yr", "closes home-office"),
        ("Identity theft", "$25-100/yr", "restoration costs"),
        ("Earthquake endorsement/CEA", "regional", "closes earthquake"),
        ("Flood (NFIP/private)", "separate policy", "closes flood"),
    ],
    "auto": [
        ("Uninsured/underinsured motorist (UM/UIM)", "required in some states", "the OTHER driver has no insurance"),
        ("Medical payments / PIP", "varies", "your passengers regardless of fault"),
        ("Rental reimbursement", "$30-80/yr", "loaner car during repair"),
        ("Loan/lease gap coverage", "$20-40/yr", "totaled new car vs loan balance"),
        ("Full glass (zero-deductible)", "$50-150/yr", "windshield"),
        ("Custom parts & equipment", "varies", "aftermarket wheels/audio"),
    ],
    "umbrella": [
        ("Underlying-limit requirement", "auto 250/500 + home 300k typical", "dropping underlying voids umbrella"),
        ("Exclusions to know", "intentional acts, business, e-bikes above class", "umbrella is personal liability only"),
    ],
}


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def load():
    if os.path.exists(DATA):
        with open(DATA) as f:
            return json.load(f)
    return {"policies": []}


def save(d):
    with open(DATA, "w") as f:
        json.dump(d, f, indent=2)


def cmd_scenarios(args):
    rows = SCENARIOS
    if args.filter:
        q = args.filter.lower()
        rows = [s for s in rows if q in " ".join(s).lower()]
    if args.group:
        rows = [s for s in rows if s[1] == args.group]
    if not rows:
        print("No scenarios match. Try: --group home|auto|liability|travel")
        return
    for sid, grp, title, what, resp, gap, ask in rows:
        print(f"[{title.upper()}] {what}")
        print(f"  Responds: {resp}")
        print(f"  Typical gap: {gap}")
        print(f"  Ask agent: \"{ask}\"")
        print()


def cmd_exclusions(args):
    if args.policy not in RIDERS:
        die(f"policy must be one of {list(RIDERS)}")
    print(f"Standard gaps & closing riders — {args.policy} (US typical; UK/EU vary)")
    print()
    print(f"{'Rider/coverage':<48}{'Cost band':<28}Closes")
    print("-" * 100)
    for name, cost, closes in RIDERS[args.policy]:
        print(f"{name:<48}{cost:<28}{closes}")
    print()
    print("Ask your agent to quote each line; get them as written")
    print("endorsements, not verbal assurances.")


def cmd_liability(args):
    nw, inc = args.net_worth, args.income
    target = nw + 2 * inc
    umbrella = max(1_000_000, int(round(target / 500_000)) * 500_000)
    print(f"Net worth: ${nw:,.0f} | Income: ${inc:,.0f}/yr")
    print()
    print(f"Reasonable total liability ceiling: ${target:,.0f}")
    print(f"  = assets at risk (${nw:,.0f}) + ~2 years future income (${2*inc:,.0f})")
    print(f"Umbrella layer to consider: ${umbrella:,}")
    print()
    print("Structure: auto BI/PD at 250/500 + home liability $300k,")
    print(f"then umbrella ${umbrella:,} on top. Umbrella cost typically")
    print("$150-400/yr for the first $1M — the cheapest protection per")
    print("dollar in personal lines.")
    print()
    print("Cautions: umbrella requires underlying limits (verify yours);")
    print("excludes business liability and often higher-class e-bikes.")


def cmd_policy(args):
    d = load()
    if args.policy_cmd == "add":
        if not args.name or not args.type:
            die("policy add needs --name and --type")
        p = {"name": args.name, "type": args.type,
             "dwelling": args.dwelling, "contents": args.contents,
             "liability": args.liability, "deductible": args.deductible,
             "added": date.today().isoformat()}
        d["policies"].append(p)
        save(d)
        print(f"Added policy {args.name!r} ({args.type})")
    elif args.policy_cmd == "list":
        if not d["policies"]:
            print("No policies recorded.")
            return
        print(f"{'Name':<14}{'Type':<8}{'Dwelling':<10}{'Contents':<10}"
              f"{'Liability':<10}Deductible")
        print("-" * 62)
        for p in d["policies"]:
            f = lambda v: (f"{int(v):,}" if v == int(v) else f"{v:,.0f}") if v else "-"
            print(f"{p['name']:<14}{p['type']:<8}{f(p['dwelling']):<10}"
                  f"{f(p['contents']):<10}{f(p['liability']):<10}"
                  f"{f(p['deductible'])}")


def cmd_audit(args):
    d = load()
    if not d["policies"]:
        die("no policies recorded — run 'policy add' first")
    print("=== GAP AUDIT ===")
    print()
    home = [p for p in d["policies"] if p["type"] in ("home", "renters")]
    auto = [p for p in d["policies"] if p["type"] == "auto"]
    gaps = []

    if home:
        p = home[0]
        if not p.get("dwelling") and p["type"] == "home":
            gaps.append(("dwelling coverage unknown",
                         "verify dwelling = REBUILD cost, not market value"))
        if (p.get("liability") or 0) < 300000:
            gaps.append((f"{p['name']} liability ${(p.get('liability') or 0):,.0f}",
                         "raise to $300k+ (umbrella prerequisite)"))
        gaps.append((f"{p['name']} water-backup rider",
                     "confirm present; limit ≥ finished-basement value"))
        gaps.append((f"{p['name']} valuables scheduling",
                     "jewelry/watches/furs above ~$1.5k each — schedule"))
        if p["type"] == "renters" and not p.get("contents"):
            gaps.append((f"{p['name']} contents unknown",
                         "inventory and set contents limit (renters')"))
    else:
        gaps.append(("no home/renters policy recorded",
                     "renters policy ~$15-30/mo covers liability + belongings"))

    if auto:
        p = auto[0]
        if (p.get("liability") or 0) < 250000:
            gaps.append((f"{p['name']} liability ${(p.get('liability') or 0):,.0f}",
                         "raise to 250/500 before adding umbrella"))
    else:
        gaps.append(("no auto policy recorded", "n/a if you don't drive"))

    if args.net_worth:
        has_umbrella = any(p["type"] == "umbrella" for p in d["policies"])
        if not has_umbrella and args.net_worth > 300000:
            target = max(1_000_000, args.net_worth)
            gaps.append(("no umbrella policy",
                         f"consider ${target:,} umbrella (~$150-400/yr)"))

    gaps.append(("flood", "standard policies exclude it — know your zone"))
    gaps.append(("e-bike/scooter", "usually excluded by home AND auto"))
    gaps.append(("home business gear", "sub-limited ~$2.5k; endorse if more"))

    print("Take this list to your agent / annual review:")
    print()
    for i, (item, action) in enumerate(gaps, 1):
        print(f"{i:>2}. {item}")
        print(f"     → {action}")
    print()
    print("Recorded policies:")
    for p in d["policies"]:
        print(f"  - {p['name']} ({p['type']})")
    print()
    print("This is a market-typical checklist, not coverage advice; your")
    print("contract and jurisdiction control.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("scenarios", help="loss scenarios → who responds, gaps")
    p.add_argument("--group", choices=["home", "auto", "liability", "travel"])
    p.add_argument("--filter", default=None, help="substring match")
    p.set_defaults(fn=cmd_scenarios)

    p = sub.add_parser("exclusions", help="standard gaps + closing riders")
    p.add_argument("--policy", required=True, choices=list(RIDERS))
    p.set_defaults(fn=cmd_exclusions)

    p = sub.add_parser("liability", help="umbrella sizing from finances")
    p.add_argument("--net-worth", type=float, required=True)
    p.add_argument("--income", type=float, required=True)
    p.set_defaults(fn=cmd_liability)

    p = sub.add_parser("policy", help="policy inventory")
    p.add_argument("policy_cmd", choices=["add", "list"])
    p.add_argument("--name", required=False)
    p.add_argument("--type", required=False,
                   choices=["home", "renters", "auto", "umbrella", "health",
                            "travel", "life"])
    p.add_argument("--dwelling", type=float, default=None)
    p.add_argument("--contents", type=float, default=None)
    p.add_argument("--liability", type=float, default=None)
    p.add_argument("--deductible", type=float, default=None)
    p.set_defaults(fn=cmd_policy)

    p = sub.add_parser("audit", help="run the gap audit on recorded policies")
    p.add_argument("--net-worth", type=float, default=None)
    p.set_defaults(fn=cmd_audit)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
