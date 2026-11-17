#!/usr/bin/env python3
"""Laundry Decoder — care symbols, safe load planning, stain first aid.

Subcommands:
  decode SYM [SYM...]  — translate described symbols into meanings + risks
  plan --item ...       — partition garments into the fewest safe loads
  stain NAME [--fabric] — least-destructive-first stain removal protocol
  list                  — print the full symbol reference

Stdlib only. All data embedded.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

# ---------------------------------------------------------------------------
# Care symbol database (ISO 37500 / GINETEX families, described in words)

# dots: 1=30°C(care: 110°C iron), 2=40°C(150°C), 3=50°C(200°C), 4=60°C, 5=95°C
# bars under tub: 1 bar = mild, 2 bars = very mild

TUB_TEMPS = {
    "hand": ("Hand wash only", "max 40°C, gentle squeezing, no wringing"),
    "30": ("Wash 30°C", "cold/mild cycle"),
    "40": ("Wash 40°C", "warm, normal cycle"),
    "50": ("Wash 50°C", "warm"),
    "60": ("Wash 60°C", "hot"),
    "70": ("Wash 70°C", "hot"),
    "95": ("Wash 95°C", "boil wash (whites/towels)"),
}

SYMBOLS = {
    # washtub family
    "tub hand": ("Hand wash only", "Max 40°C water. Do not wring or twist; press water out in a towel."),
    "tub 30": ("Machine wash cold (30°C)", "Cold water, reduced spinning. Synthetics and darks keep color longer cold."),
    "tub 40": ("Machine wash warm (40°C)", "Standard cotton/permanent-press cycle."),
    "tub 50": ("Machine wash 50°C", "Hot-ish; colors may fade over time."),
    "tub 60": ("Machine wash hot (60°C)", "Towels, bedding, whites. Kills dust mites."),
    "tub 95": ("Machine wash very hot (95°C)", "Boil wash — white cotton only. Sanitizing."),
    "tub crossed": ("Do not wash", "Water will destroy it (leather, structured hats, some wools) — spot clean or professional."),
    "tub 40 with bar": ("Wash 40°C, mild (reduced agitation)", "Use gentle/permanent-press cycle; spin low."),
    "tub 40 with two bars": ("Wash 40°C, very mild", "Delicates cycle + mesh bag, minimal spin."),
    # triangle family
    "triangle": ("Bleach allowed (any)", "Chlorine bleach OK on sturdy whites. Never on wool/silk/spandex."),
    "triangle crossed": ("Do not bleach", "Chlorine yellows synthetics, holes wool/silk, rots spandex. Oxygen bleach usually fine."),
    "triangle two lines": ("Non-chlorine bleach only", "Oxygen/color-safe bleach only."),
    # dry: square with circle
    "square circle": ("Tumble dry, normal", "Any heat."),
    "square circle 1 dot": ("Tumble dry low heat", "Delicate synthetics."),
    "square circle 2 dots": ("Tumble dry normal heat", "Standard cottons."),
    "square circle crossed": ("Do not tumble dry", "Line/flat dry. Wool knits stretch in the drum; down clumps."),
    "square circle 1 dot with bar": ("Tumble dry low, gentle", "Delicate cycle."),
    "square line": ("Line dry", "Hang wet; reshape knits first."),
    "square horizontal line in box": ("Dry flat", "Wool/sweaters — hangers deform them wet."),
    "square diagonal line": ("Dry in shade", "Sun fades and yellows; bright dyes and whites-with-optical-whiteners both."),
    # iron family
    "iron 1 dot": ("Iron low (110°C)", "Synthetics: acetate, nylon, acrylic. Steam off, press cloth."),
    "iron 2 dots": ("Iron medium (150°C)", "Wool, polyester blends. Steam OK."),
    "iron 3 dots": ("Iron high (200°C)", "Cotton, linen. Damp or steam."),
    "iron crossed": ("Do not iron", "Prints, sequins, permanent press finishes melt/shine."),
    # professional care: circle
    "circle p": ("Dry clean, any solvent", "Professional care. P = tetrachloroethylene permitted."),
    "circle f": ("Dry clean, hydrocarbon solvent only", "Milder professional cleaning."),
    "circle w": ("Professional wet clean", "Gentler than dry clean for many wools."),
    "circle crossed": ("Do not dry clean", "Coatings/trims react with solvent."),
    "circle a": ("Dry clean, any solvent", "A = all solvents (older labeling)."),
}

# aliases so fuzzy descriptions still hit
ALIASES = {
    "washing machine": "tub 40", "machine wash": "tub 40",
    "hand wash": "tub hand", "do not wash": "tub crossed",
    "no bleach": "triangle crossed", "bleach ok": "triangle",
    "no tumble": "square circle crossed", "do not tumble dry": "square circle crossed",
    "tumble low": "square circle 1 dot", "tumble dry low": "square circle 1 dot",
    "no iron": "iron crossed", "do not iron": "iron crossed",
    "dry clean": "circle p", "do not dry clean": "circle crossed",
    "dry flat": "square horizontal line in box", "line dry": "square line",
    "wash 30": "tub 30", "wash 40": "tub 40", "wash 60": "tub 60",
}


def lookup_symbol(desc: str):
    d = " ".join(desc.lower().split())
    for pat, key in ALIASES.items():
        if d == pat:
            return key, SYMBOLS[key]
    if d in SYMBOLS:
        return d, SYMBOLS[d]
    # try "tub N" / "iron N dots" / "square circle N dots" shapes
    m = re.match(r"^(tub|iron|square circle|circle)\s+(\d+)(\s*dots?)?$", d)
    if m:
        fam, n = m.group(1), int(m.group(2))
        key = f"{fam} {n} dot" if fam == "iron" else f"{fam} {n}"
        if key in SYMBOLS:
            return key, SYMBOLS[key]
    # "circle p" family letters (F, P, W, A solvents)
    m = re.match(r"^circle\s+([fpwa])$", d)
    if m and d in SYMBOLS:
        return d, SYMBOLS[d]
    m = re.match(r"^(tub)\s+(\d+)\s*°?c?\s*(with (one|two) bars?)?$", d)
    if m and m.group(3):
        key = f"tub {m.group(2)} with {'bar' if 'one' in m.group(3) else 'two bars'}"
        if key in SYMBOLS:
            return key, SYMBOLS[key]
    return None, None


# ---------------------------------------------------------------------------
# Stain protocols: least destructive first. Each: steps ordered, NEVER hard rule.

STAINS = {
    "red wine": {
        "steps": ["Blot (never rub) with paper towel from outside in",
                   "Cover thick with salt or talc; let pull dye 15 min; brush off",
                   "Cold water rinse from the back of the fabric",
                   "Soak 30 min in cool water + oxygen bleach (colors: 1 tbsp/2L)",
                   "Wash at the hottest temp the label allows with detergent",
                   "If residue: repeat oxygen soak — do not machine-dry until gone"],
        "never": "Heat or chlorine bleach before the dye is out — heat sets anthocyanins; chlorine can yellow wool/silk.",
    },
    "blood": {
        "steps": ["Rinse in COLD water immediately, from the back",
                   "Soak 30+ min in cold salt water (1 tbsp/250 ml)",
                   "Work in 3% hydrogen peroxide (test seam first; fizzing = working)",
                   "Cold wash with detergent + a scoop of oxygen bleach",
                   "Dried/old: paste of meat tenderizer (papain) + water 15 min, then cold wash"],
        "never": "Hot water — it cooks the protein into the fiber permanently. Never chlorine bleach on wool/silk.",
    },
    "coffee": {
        "steps": ["Blot liquid; scrape milk solids with a dull edge",
                   "Rinse cold from the back",
                   "Liquid detergent or dish soap worked in, 5 min",
                   "Rinse; wash warm per label"],
        "never": "Soap-first on a milk coffee — casein sets like glue. Rinse, THEN detergent.",
    },
    "grass": {
        "steps": ["Rubbing alcohol dabbed (inside-out cloth underneath)",
                   "Liquid detergent worked in 15 min",
                   "Wash hottest allowed; air-dry and check",
                   "Persistent: 3% hydrogen peroxide on whites / oxygen bleach soak colors"],
        "never": "Chlorine bleach on colored fabrics; heat before the chlorophyll is out.",
    },
    "ink ballpoint": {
        "steps": ["Place cloth under stain; drip rubbing alcohol through it",
                   "Blot; repeat until no transfer",
                   "Rinse; liquid detergent; wash warm",
                   "Stubborn on cotton: aerosol hairspray (alcohol carrier) same method"],
        "never": "Water first on oil-based ballpoint ink — it spreads the blob.",
    },
    "oil grease": {
        "steps": ["Sprinkle cornstarch/talc; sit 20 min; brush off (absorbs fresh oil)",
                   "Dish detergent (degreaser) worked in dry fabric",
                   "Hot water rinse from the back as hot as label allows",
                   "Wash hottest allowed"],
        "never": "Water alone or machine-drying with residue — dryer heat bakes the oil in.",
    },
    "tomato sauce": {
        "steps": ["Scrape off solids with a dull edge; do not rub in",
                   "Cold rinse from the back",
                   "Liquid detergent 15 min; rinse",
                   "Oxygen bleach soak for colorfast items; wash warm"],
        "never": "Hot water first (sets the pigment) or chlorine on colors.",
    },
    "chocolate": {
        "steps": ["Chill with ice; scrape off the bulk",
                   "Cold rinse from the back",
                   "Liquid detergent or dish soap, 10 min",
                   "Wash warm; check before drying"],
        "never": "Hot water at the start — cocoa butter + protein set together.",
    },
    "sweat armpits": {
        "steps": ["White vinegar 1:1 water, soak 30 min",
                   "Baking soda paste 1h on the pit area",
                   "Wash warm with enzyme detergent",
                   "Yellowing on whites: oxygen bleach overnight soak"],
        "never": "Chlorine bleach — it reacts with sweat proteins and makes the yellow WORSE.",
    },
    "mud": {
        "steps": ["Let dry completely; brush off all loose dirt",
                   "Soak in cool water + detergent 15 min",
                   "Work liquid detergent into the remainder",
                   "Wash warm; repeat if brown shadow remains"],
        "never": "Attacking wet mud — you grind it deeper into the weave.",
    },
    "makeup foundation": {
        "steps": ["Blot; treat with makeup remover or rubbing alcohol dab",
                   "Liquid detergent worked in 15 min",
                   "Rinse; wash per label"],
        "never": "Chlorine bleach; hot dryer before fully out.",
    },
    "lipstick": {
        "steps": ["Blot with alcohol-damp cloth",
                   "Dish detergent on the oils, 10 min",
                   "Rinse; repeat; wash warm"],
        "never": "Rubbing (spreads waxy pigment); heat.",
    },
    "pet urine": {
        "steps": ["Blot up all you can with towels + weight",
                   "Enzyme cleaner (nature's-miracle type) SATURATE; sit 15 min covered",
                   "Blot; repeat enzyme application; air dry 24-48h",
                   "Machine washable: enzyme detergent wash, air dry"],
        "never": "Ammonia products (smells like urine to pets = repeat marking) or steam/heat before enzymes finish — heat kills them.",
    },
    "wax": {
        "steps": ["Harden with ice; scrape off the bulk",
                   "Brown paper bag over/under; warm iron melts wax into the paper",
                   "Repeat with fresh paper until no transfer",
                   "Treat residual oily spot as a grease stain"],
        "never": "Direct hot iron on fabric — scorch marks are forever.",
    },
    "rust": {
        "steps": ["Lemon juice + salt, sit 10 min in sun (mild acid)",
                   "Rinse thoroughly; wash normally",
                   "Stubborn: commercial rust remover (oxalic acid) per label"],
        "never": "Chlorine bleach — it sets rust permanently. Never heat-dry with rust present.",
    },
    "dye transfer": {
        "steps": ["STOP — do not dry; rewash immediately with detergent + oxygen bleach",
                   "Still pink: soak all-night in oxygen bleach solution",
                   " Whites: Rit color-remover as last resort"],
        "never": "Drying the item before the rogue dye is fully out — the dryer sets it.",
    },
    "paint latex": {
        "steps": ["Wet paint: rinse warm water immediately; detergent; wash warm",
                   "Dried: saturate with rubbing alcohol; scrape; work in detergent; wash"],
        "never": "Hot dryer — latex paint cures into plastic permanently.",
    },
    "paint oil": {
        "steps": ["Wet: blot; mineral spirits on a cloth from the outside in",
                   "Dish detergent on residue; wash hottest allowed"],
        "never": "Water on oil paint; machine drying with residue.",
    },
    "gum": {
        "steps": ["Freeze hard with ice cube / freezer bag; crack and peel off",
                   "Residue: rub with alcohol or peanut butter oils, then wash"],
        "never": "Heat-softening — you embed it into the fibers.",
    },
    "deodorant": {
        "steps": ["White marks: nylon stockings or dry towel rubs them off dry fabric",
                   "Buildup: liquid detergent 15 min, wash warm"],
        "never": "Chlorine bleach on buildup (same ammonia reaction as sweat).",
    },
    "coffee cream liqueur": {
        "steps": ["Cold rinse from the back",
                   "Enzyme detergent 15 min (cream = protein)",
                   "Wash warm; oxygen bleach if shadow remains"],
        "never": "Hot water before enzyme treatment.",
    },
}

# ---------------------------------------------------------------------------
# Load planner

FABRIC_CLASS = {
    "cotton": "heavy", "terry": "heavy", "towel": "heavy", "denim": "heavy",
    "canvas": "heavy", "linen": "mid", "polyester": "mid", "synthetic": "mid",
    "blend": "mid", "wool": "delicate_fiber", "silk": "delicate_fiber",
    "cashmere": "delicate_fiber", "lace": "delicate", "lingerie": "delicate",
    "activewear": "mid", "down": "special", "tech_shell": "special",
}

VALID_COLORS = {"white", "light", "dark", "red", "new"}


class Garment:
    def __init__(self, spec: str):
        parts = [p.strip() for p in spec.split(";")]
        if not 3 <= len(parts) <= 5:
            raise ValueError(f"item spec: name;color;tempC;fabric[;flags] — got {spec!r}")
        self.name = parts[0]
        self.color = parts[1].lower()
        if self.color not in VALID_COLORS:
            raise ValueError(f"{self.name}: color must be one of {sorted(VALID_COLORS)}")
        self.temp = int(parts[2])
        if not 20 <= self.temp <= 95:
            raise ValueError(f"{self.name}: temp 20-95 °C")
        self.fabric = parts[3].lower()
        flags = [f.lower() for f in parts[4].split(",")] if len(parts) > 4 and parts[4] else []
        if len(parts) == 5 and not flags:
            flags = [parts[4].lower()]
        self.delicate = any(f in ("delicate", "delicates") for f in flags)
        self.hot_only = any("hot" in f for f in flags)
        self.fclass = FABRIC_CLASS.get(self.fabric, "mid")

    @property
    def bleeder(self) -> bool:
        return self.color in ("red", "new")

    def __repr__(self):
        return self.name


def compatible(a: Garment, b: Garment) -> tuple[bool, str]:
    """Pairwise compatibility; returns (ok, rule_if_not)."""
    if a.bleeder != b.bleeder:
        return False, "bleeder separation (new/red dye runs)"
    if {a.color, b.color} == {"white", "dark"} or {a.color, b.color} == {"white", "red"}:
        return False, "whites separate from darks (even non-new darks tint the wash)"
    if a.delicate != b.delicate:
        return False, "delicates cycle separation"
    if {a.fclass, b.fclass} == {"delicate_fiber", "heavy"}:
        return False, "wool/silk never with terry/heavy cotton (felting/snagging)"
    if a.hot_only != b.hot_only:
        return False, "temperature conflict (hot-only vs capped item)"
    if a.temp != b.temp and (a.hot_only or b.hot_only):
        return False, "temperature conflict"
    return True, ""


def plan_loads(items: list[Garment]) -> list[dict]:
    """Greedy partition into fewest pairwise-compatible loads."""
    loads: list[list[Garment]] = []
    reasons: dict[int, list[str]] = {}
    for item in items:
        placed = False
        for li, load in enumerate(loads):
            if all(compatible(item, m)[0] for m in load):
                load.append(item)
                placed = True
                break
            else:
                reasons.setdefault(li, [])
        if not placed:
            loads.append([item])
    out = []
    for load in loads:
        temp = min(g.temp for g in load)
        cycle = "delicates" if any(g.delicate for g in load) else \
                ("heavy/cotton" if all(g.fclass == "heavy" for g in load) else "normal")
        names = ", ".join(g.name for g in load)
        rules = []
        if any(g.bleeder for g in load):
            rules.append("bleeder: wash alone first 2 times, cold, color-set soak")
        if any(g.fclass == "delicate_fiber" for g in load):
            rules.append("wool/silk cycle: minimal agitation, no tumble (dry flat)")
        if any(g.hot_only for g in load):
            rules.append("hot-only members need ≥60°C to sanitize/de-oil")
        out.append({"items": names, "temp_c": temp, "cycle": cycle, "notes": rules})
    return out


# ---------------------------------------------------------------------------
# CLI

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Care symbols, load planning, stain first aid")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("decode", help="decode described symbols")
    d.add_argument("symbols", nargs="+")

    pl = sub.add_parser("plan", help="partition garments into safe loads")
    pl.add_argument("--item", action="append", required=True,
                    help="name;color;tempC;fabric[;flags] (flags: delicate,hot-only)")
    pl.add_argument("--json", action="store_true")

    st = sub.add_parser("stain", help="stain removal protocol")
    st.add_argument("name")
    st.add_argument("--fabric", default="cotton")

    sub.add_parser("list", help="list all symbols")

    args = p.parse_args(argv)

    if args.cmd == "decode":
        print("=" * 66)
        print("CARE LABEL DECODE")
        print("=" * 66)
        for desc in args.symbols:
            key, entry = lookup_symbol(desc)
            if entry:
                print(f"\n{desc!r} → {key}")
                print(f"  meaning : {entry[0]}")
                print(f"  how     : {entry[1]}")
            else:
                print(f"\n{desc!r} → ? unknown. Try shapes: tub/triangle/iron/circle/square")
                print("  e.g. 'tub 40', 'tub 40 with bar', 'square circle 2 dots', 'circle p'")
        return 0

    if args.cmd == "plan":
        try:
            items = [Garment(s) for s in args.item]
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 2
        loads = plan_loads(items)
        if args.json:
            print(json.dumps(loads, indent=2))
            return 0
        print("=" * 66)
        print(f"LOAD PLAN — {len(items)} garments → {len(loads)} loads")
        print("=" * 66)
        for i, load in enumerate(loads, 1):
            print(f"\nLoad {i}: {load['items']}")
            print(f"  temp {load['temp_c']}°C · {load['cycle']} cycle")
            for r in load["notes"]:
                print(f"  ⚠ {r}")
        print()
        return 0

    if args.cmd == "stain":
        name = args.name.lower().strip()
        entry = STAINS.get(name) or next(
            (v for k, v in STAINS.items() if name in k or k in name), None)
        if not entry:
            print(f"No protocol for {args.name!r}. Known: {', '.join(sorted(STAINS))}")
            return 2
        print("=" * 66)
        print(f"STAIN: {args.name.upper()}  (fabric: {args.fabric})")
        print("=" * 66)
        print("\nSteps, least destructive first:")
        for i, s in enumerate(entry["steps"], 1):
            print(f"  {i}. {s}")
        print(f"\n🚫 NEVER: {entry['never']}")
        if args.fabric in ("wool", "silk", "cashmere"):
            print("\n⚠ protein fibers: skip oxygen/chlorine bleach and hydrogen peroxide;")
            print("  use gentle detergent + cool water; consider professional care.")
        return 0

    if args.cmd == "list":
        print(f"{len(SYMBOLS)} symbols:\n")
        for k, (m, h) in SYMBOLS.items():
            print(f"  {k:<32} {m}")
            print(f"  {'':32} → {h}")
        print(f"\n{len(STAINS)} stain protocols — 'stain <name>'")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
