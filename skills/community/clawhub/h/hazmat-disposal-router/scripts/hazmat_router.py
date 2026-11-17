#!/usr/bin/env python3
"""Hazmat Disposal Router — household hazardous waste verdicts,
cleanout audit, storage rules, channel finders. Stdlib only.

Verdicts are the consensus safe default across US/EU/UK guidance;
local rules vary — verify with your municipality.
"""
import argparse

# item -> (verdict_channel, why, warn)
# channels: HHW, RETAIL, TRASH, TAKEBACK, SHARPS, PHARMACY, SCRAP
ITEMS = {
    "latex paint": ("TRASH-if-dry", "Water-based; inert once fully dry. Air-dry or mix cat litter/paint hardener until solid.", "Liquid paint leaks from trucks — dry it first. Canned solid = trash."),
    "oil paint": ("HHW", "Oil-based paints carry VOCs + sometimes lead (pre-1980).", "Never drain. Keep lid on, original label."),
    "paint thinner": ("HHW", "Solvent; poison to septic and municipal biology.", "Never down any drain. Closed metal/glass container, cool place."),
    "varnish": ("HHW", "Solvent-based, flammable.", "Original can, tight lid."),
    "car battery": ("RETAIL", "Lead + sulfuric acid — the most recycled consumer good; retailers must take the core.", "Upright. No tools across terminals. Core credit ~$10."),
    "li-ion battery": ("HHW", "#1 cause of garbage-truck fires; damaged cells ignite in compactors.", "TAPE terminals, bag separately, cool transport."),
    "power tool battery": ("HHW", "Li-ion pack — same fire path.", "Tape terminals. Retailers (tool brands) also take them."),
    "e-bike battery": ("HHW", "Large li-ion — fires even unprovoked when damaged.", "Tape terminals; call facility first — many want notice."),
    "alkaline battery": ("TRASH (US) / battery-bin (EU)", "No mercury since mid-90s (US/EU); landfill-safe per makers.", "EU: city battery bins. Rechargeables NEVER trash."),
    "rechargeable battery": ("RETAIL", "NiMH/Li-ion contain recyclable metals + fire risk.", "Tape terminals; many electronics retailers have bins."),
    "button battery": ("HHW", "Small but lithium; swallowing hazard for kids/pets too.", "Tape both sides — they short against each other."),
    "motor oil": ("RETAIL", "1 L contaminates ~1,000,000 L water; auto stores collect & resell it.", "Clean sealed container, no bleach/jugs-residue bottles."),
    "oil filter": ("RETAIL/HHW", "Holds residual oil.", "Drain 24h upright first."),
    "coolant": ("HHW", "Ethylene glycol sweet-toxic to animals and kids.", "Never drain. Sealed jug, original label preferred."),
    "brake fluid": ("HHW", "Solvent + glycol mix.", "Never drain."),
    "gasoline": ("HHW", "Degrades but stays ignitable; vapor explosion risk.", "Approved gas can only. Never on ground, never in drains."),
    "propane tank": ("RETAIL-exchange/HHW", "Pressurized fuel — explodes in compactors.", "Valve closed. Exchange programs take grungy tanks."),
    "butane canister": ("HHW", "Pressurized; puncturing is the danger.", "Do NOT puncture even when 'empty'."),
    "cfl bulb": ("HHW/RETAIL-bin", "Contains mercury vapor.", "Intact transport. If broken: air room 10 min, seal fragments in jar/bag, HHW."),
    "fluorescent tube": ("HHW", "Mercury + phosphor.", "Wrap in newspaper; don't break."),
    "led bulb": ("TRASH", "No mercury.", "—"),
    "incandescent bulb": ("TRASH", "Inert.", "Wrap against breakage only."),
    "pesticide": ("HHW", "Designed to kill biota; treatment plants can't remove.", "Original container. NEVER reuse containers."),
    "weed killer": ("HHW", "Herbicides persist through treatment.", "Never dilute down drain."),
    "pool chlorine": ("HHW", "Oxidizer — reacts with acids, organics, ammonia.", "NEVER mix containers with anything; original pail."),
    "cleaning chemicals": ("HHW if solvent/acid/oxidizer", "Drain-safe in use-dilution, NOT as concentrated leftovers.", "Don't mix leftovers into one bottle."),
    "meds": ("PHARMACY", "Flushing puts APIs in water; take-back destroys properly.", "US: DEA take-back days + some pharmacy kiosks. Scratch labels."),
    "needles": ("SHARPS", "Worker injuries; program exists for exactly this.", "Approved sharps container or rigid labeled container per local rules. NEVER soda bottles."),
    "therometer-mercury": ("HHW", "Mercury.", "If broken: don't vacuum; sulfur powder or HHW guidance."),
    "thermostat": ("HHW", "Mercury switch.", "Keep level/intact."),
    "smoke alarm": ("TAKEBACK", "Ionization type has americium-241 (tiny, regulated).", "Mail-back programs by manufacturer; photoelectric-only = e-waste."),
    "fire extinguisher": ("HHW/FIRE-DEPT", "Pressurized steel.", "Completely discharge outdoors first if local rules allow, then HHW/scrap."),
    "electronics": ("RETAIL/HHW", "WEEE-regulated (EU); retailers must take on like-purchase.", "Wipe drives. Battery out if removable."),
    "tv": ("RETAIL/HHW", "CRTs hold leaded glass; flat panels hold mercury lamps (older).", "Two-person lift; don't set CRTs face-down."),
    "asbestos-suspect": ("PROFESSIONAL", "Inhale hazard; abatement is licensed work.", "Don't disturb, don't drill, wet-surface if it must wait. Test first."),
    "aerosol can": ("HHW if not empty / TRASH if empty", "Pressurized + propellant.", "Empty = trash (US most places). Never puncture or burn."),
}

KEYS_HINT = {
    "paint": ["latex paint", "oil paint"], "battery": ["car battery", "li-ion battery", "alkaline battery"],
    "lithium": ["li-ion battery"], "oil": ["motor oil"], "gas": ["gasoline"],
    "bulb": ["cfl bulb", "led bulb"], "light": ["cfl bulb", "led bulb"],
    "med": ["meds"], "pill": ["meds"], "needle": ["needles"], "propane": ["propane tank"],
    "freon": ["PROFESSIONAL"], "fridge": ["RETAIL"], "tv": ["tv"],
}

def find_items(query):
    q = query.lower()
    if q in ITEMS:
        return [q]
    hits = []
    for k in ITEMS:
        if q in k or k.split()[0] in q:
            hits.append(k)
    if not hits:
        for hint_q, keys in KEYS_HINT.items():
            if hint_q in q:
                hits = [k for k in keys if k in ITEMS]
                break
    return hits

def print_verdict(key):
    chan, why, warn = ITEMS[key]
    print(f"{key.upper()}:")
    print(f"  VERDICT: {chan}")
    print(f"  WHY:     {why}")
    if warn != "—":
        print(f"  WARN:    {warn}")
    print()

def cmd_dispose(a):
    hits = find_items(a.item)
    if not hits:
        print(f"No entry for '{a.item}'. Closest families:")
        fams = sorted({v[0] for v in ITEMS.values()})
        for f in fams:
            print(f"  - {f}")
        print("\nRule of thumb: if it's liquid + chemical + not-water-based,")
        print("or pressurized, or battery-chemistry, or poison-by-design → HHW.")
        return
    for k in hits:
        print_verdict(k)

def cmd_audit(a):
    items = [i.strip() for i in a.items.split(",") if i.strip()]
    groups = {}
    unresolved = []
    for it in items:
        hits = find_items(it)
        if not hits:
            unresolved.append(it)
            continue
        chan = ITEMS[hits[0]][0]
        groups.setdefault(chan, []).append(hits[0])
    total = sum(len(v) for v in groups.values())
    print(f"CLEANOUT MANIFEST — {len(items)} listed, {total} routed"
          + (f", {len(unresolved)} unresolved" if unresolved else "") + ":")
    order = ["HHW", "HHW/RETAIL-bin", "HHW if not empty / TRASH if empty", "HHW if solvent/acid/oxidizer",
             "TRASH-if-dry", "TRASH", "RETAIL", "RETAIL-exchange/HHW", "RETAIL/HHW",
             "TAKEBACK", "PHARMACY", "SHARPS", "SCRAP", "HHW/FIRE-DEPT",
             "TRASH (US) / battery-bin (EU)", "PROFESSIONAL"]
    for chan in order:
        if chan in groups:
            print(f"\n  {chan}:")
            for it in groups[chan]:
                print(f"    - {it}")
    if unresolved:
        print("\n  UNRESOLVED (check individually):")
        for it in unresolved:
            print(f"    - {it}")
    hhw = [c for c in groups if c.startswith("HHW")]
    print("\nTRIP PLAN:")
    if hhw:
        print("  HHW run: " + ", ".join(i for c in hhw for i in groups[c]))
        print("  (check facility hours — many are one day/week or monthly)")
    if "RETAIL" in groups or "RETAIL-exchange/HHW" in groups:
        print("  Retailer stops: " + ", ".join(groups.get("RETAIL", []) + groups.get("RETAIL-exchange/HHW", [])))
    if "PHARMACY" in groups:
        print("  Pharmacy: " + ", ".join(groups["PHARMACY"]))
    if "PROFESSIONAL" in groups:
        print("  LICENSED ABATEMENT needed: " + ", ".join(groups["PROFESSIONAL"]) + " — do not DIY")
    print("\nTransport: upright, sealed, ventilated vehicle (windows cracked),")
    print("no smoking, lithium terminals taped, nothing stacked on batteries.")

def cmd_storage(a):
    print("INTERIM STORAGE RULES (until drop-off):")
    rules = [
        "Original containers, original labels — relabeled jam jars are how accidents start.",
        "NEVER mix leftovers into one container (chlorine+acid, ammonia+bleach = gas).",
        "Lithium batteries: tape terminals, separate bags, cool spot away from fuel.",
        "Lead-acid batteries: upright, on plastic tray (acid weep), no metal across posts.",
        "Liquids: tight lids, upright, off concrete floors where possible (corrosion).",
        "Flammables (gas, thinners): away from water heaters/engines, out of sun.",
        "Ventilated area — never a sealed bedroom closet; garage shelf > under-sink pile.",
        "Out of kid/pet reach, preferably locked cabinet.",
        "Plan the run within a month; corroding containers don't improve.",
    ]
    for i, r in enumerate(rules, 1):
        print(f"  {i}. {r}")

def cmd_channels(a):
    if a.region == "US":
        print("US CHANNELS:")
        for line in [
            "HHW facility: search '<county> household hazardous waste' — most counties run them (often Sat-only).",
            "Earth911.org / Call2Recycle.org — nearest drop-offs by item + ZIP.",
            "Auto parts stores (AutoZone/O'Reilly/NAPA): motor oil, oil filters, car & often li-ion batteries — free.",
            "Home Depot/Lowe's: CFL & rechargeable battery bins at entrance.",
            "Best Buy: electronics/TVs (limits per day), some appliances.",
            "DEA takeback day (April/October) + pharmacy kiosks for meds.",
            "Paint: PaintCare states take it at paint retailers (paintcare.org).",
            "Propane: Blue Rhino/exchange cages accept grungy tanks.",
        ]:
            print(f"  - {line}")
    elif a.region == "EU":
        print("EU CHANNELS:")
        for line in [
            "Municipal recycling yard (Recyclinghof / déchetterie / ecocentro): all HHW classes, usually free for residents.",
            "WEEE: any electronics retailer MUST take your old device when you buy a like one (law).",
            "Battery bins: every supermarket + school entrance (battery directive).",
            "Pharmacies take expired meds (most countries; never trash/flush).",
            "Paint/partial cans: municipal yard chemical container; some paint shops take them.",
            "Check municipality website for chemical waste mobile collections (toxic taxi).",
        ]:
            print(f"  - {line}")
    else:
        print("UK CHANNELS:")
        for line in [
            "Council HWRC (household waste recycling centre): paint, chemicals, batteries, gas bottles — check your council's site for what's accepted.",
            "Small electricals: many retailers take them in-store; some councils collect with bins.",
            "Batteries: supermarket entrances + any shop selling them >32kg/yr must take back.",
            "Medicines: any pharmacy, always.",
            "Engine oil: HWRC oil banks.",
        ]:
            print(f"  - {line}")
    print("\nSearch pattern that always works: '<your city/county>' + item +")
    print("'disposal' or 'recycling'. Municipal .gov/.gov.uk sites list accepted items.")

def cmd_never(a):
    print("THE NEVER LIST (each of these is common — that's the problem):")
    nevers = [
        ("Solvents/thinners/oil paint down ANY drain", "Septic death + treatment plants can't strip them + illegal."),
        ("Li-ion batteries in any bin", "Compactor fires; sanitation fires doubled where enforcement lags."),
        ("Needles loose or in plastic bottles", "Worker injuries; rigid sharps containers exist for this."),
        ("Mixing chemical leftovers into one jug", "Chlorine+acid, ammonia+bleach: toxic gas in your kitchen."),
        ("Liquid paint into trash", "Leaks through trucks, paints streets; DRY first or HHW."),
        ("Gasoline on weeds/ground/drains", "Groundwater + fire; 1 L ruins a municipal aquifer well."),
        ("Puncturing aerosols or propane", "The propellant IS the explosion."),
        ("Flushing meds", "Pharmaceuticals pass treatment into waterways."),
        ("Burning treated wood/painted wood", "Arsenic, lead, dioxin smoke."),
        ("Shop-vacuuming mercury or asbestos dust", "Concentrates the hazard into your breathing air."),
    ]
    for i, (act, why) in enumerate(nevers, 1):
        print(f"  {i:2d}. NEVER {act}\n      because: {why}")

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("dispose")
    d.add_argument("--item", required=True)
    d.set_defaults(fn=cmd_dispose)

    au = sub.add_parser("audit")
    au.add_argument("--items", required=True, help="comma-separated list")
    au.set_defaults(fn=cmd_audit)

    s = sub.add_parser("storage")
    s.set_defaults(fn=cmd_storage)

    c = sub.add_parser("channels")
    c.add_argument("--region", choices=["US", "EU", "UK"], default="US")
    c.set_defaults(fn=cmd_channels)

    n = sub.add_parser("never")
    n.set_defaults(fn=cmd_never)

    a = p.parse_args()
    a.fn(a)

if __name__ == "__main__":
    main()
