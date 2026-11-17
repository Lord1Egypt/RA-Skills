#!/usr/bin/env python3
"""grocery_flow.py — map stores, route lists into walking order, track staples.

Subcommands:
  map-store  interactively define a store's zones in YOUR walking order
  route      sort a list file into zone-by-zone walking order
  staples    add/list/mark-bought household staples with cadence radar
  merge      multi-store trip: route per store + suggest store sequence

State: ~/.grocery_flow/<store>.json. Pure stdlib.
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

STATE_DIR = Path(os.path.expanduser("~/.grocery_flow"))

# canonical item -> conventional zone (matcher data; see references/item-zones.md)
ITEM_ZONES = {
    "produce": """apple apples banana bananas orange oranges lemon lemons lime
       avocado avocados tomato tomatoes cucumber onions garlic potato potatoes
       carrot carrots lettuce spinach kale salad greens pepper peppers broccoli
       cauliflower mushrooms zucchini berries strawberry strawberries grapes
       melon pineapple mango herbs basil parsley cilantro ginger corn cabbage
       green-onions scallions radish beets sweet-potato squash""",
    "bakery": """bread loaf baguette tortillas pita bagels buns rolls english-muffins
       croissant cake cookies pie naan croutons crumpets""",
    "deli": """ham turkey salami sliced-cheese prosciutto hummus olives
       prepared-food rotisserie lunch-meat pastrami mortadella""",
    "dairy": """milk buttermilk cream half-and-half yogurt kefir butter
       cheese cheddar mozzarella parmesan feta cream-cheese sour-cream eggs
       egg-substitute cottage-cheese ricotta ghee""",
    "meat": """chicken chicken-thighs chicken-breast whole-chicken beef
       ground-beef steak pork pork-chops sausage bacon lamb ribs ground-turkey
       meatballs brisket""",
    "seafood": """salmon shrimp tilapia cod tuna crab lobster scallops
       fish canned-tuna smoked-salmon whitefish mussels clams""",
    "frozen": """frozen-pizza ice-cream frozen-vegetables frozen-peas frozen-broccoli
       frozen-berries frozen-fries frozen-waffles frozen-dinners popsicles
       edamame frozen-shrimp puff-pastry frozen-mango""",
    "pantry": """rice pasta spaghetti macaroni noodles flour sugar salt
       pepper olive-oil vegetable-oil vinegar soy-sauce canned-tomatoes
       tomato-sauce beans chickpeas lentils canned-soup broth stock
       peanut-butter jam honey syrup oats quinoa couscous breadcrumbs
       taco-shells canned-corn canned-beans tomato-paste coconut-milk
       mustard ketchup mayo hot-sauce salsa spices raisins nuts almonds
       walnuts cashews chia chocolate-chips baking-soda baking-powder
       vanilla cornstarch oil""",
    "breakfast": """cereal granola muesli coffee coffee-beans ground-coffee
       tea teabags orange-juice juice maple-syrup pancake-mix english-breakfast
       hot-chocolate creamer""",
    "beverages": """water sparkling-water soda soft-drinks cola beer wine
       sparkling juice-boxes energy-drinks tonic kombucha seltzer""",
    "snacks": """chips pretzels popcorn crackers tortilla-chips candy
       chocolate granola-bars trail-mix fruit-snacks cookies snack-bars
       nuts dried-fruit""",
    "household": """trash-bags garbage-bags paper-towels toilet-paper tissues
       dishwasher-tabs dish-soap laundry-detergent fabric-softener bleach
       sponges aluminum-foil plastic-wrap zip-bags batteries lightbulbs
       candles air-freshener cleaning-spray disinfectant mop-bags ziplock""",
    "health": """toothpaste toothbrush floss shampoo conditioner soap
       deodorant razors band-aids pain-reliever vitamins sunscreen
       hand-sanitizer lotion cold-medicine first-aid""",
    "baby": """diapers baby-wipes formula baby-food baby-lotion
       diaper-rash-cream baby-snacks sippy-cups""",
    "pet": """dog-food cat-food cat-litter pet-treats dog-treats birdseed
       pet-shampoo flea-treatment""",
    "floral": """flowers bouquet potted-plant greeting-card balloon""",
}

ZONE_ALIASES = {
    "veg": "produce", "vegetables": "produce", "fruits": "produce",
    "dairy-case": "dairy", "cheese": "dairy", "eggs": "dairy",
    "meats": "meat", "butcher": "meat", "fish": "seafood",
    "freezer": "frozen", "ices": "frozen", "dry-goods": "pantry",
    "grocery": "pantry", "canned": "pantry", "drinks": "beverages",
    "paper-goods": "household", "cleaning": "household",
    "pharmacy": "health", "hba": "health", "toiletries": "health",
    "pets": "pet", "cards": "floral",
}


def norm_item(s):
    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^a-z\- ]", "", s)
    if s.endswith("ies"):
        s = s[:-3] + "y"
    elif s.endswith("es") and not s.endswith("ses"):
        s = s[:-2]
    elif s.endswith("s") and not s.endswith("ss"):
        s = s[:-1]
    return s.strip()


def build_lookup():
    lut = {}
    for zone, blob in ITEM_ZONES.items():
        for w in blob.split():
            w = norm_item(w)
            if w:
                lut[w] = zone
    return lut


LUT = build_lookup()


def match_zone(item, store_zones, learned):
    """Return zone for item or None."""
    it = norm_item(item)
    if it in learned:
        return learned[it]
    variants = {it, it.replace(" ", "-"), it.replace("-", " ")}
    # prefix conventions: frozen/canned/jarred/bottled/dried override
    prefix_zone = None
    for v in list(variants):
        m = re.match(r"^(frozen|canned|jarred|bottled|dried|fresh)\s+(.+)$", v)
        if m:
            pref, rest = m.group(1), m.group(2)
            prefix_zone = {"frozen": "frozen", "canned": "pantry",
                           "jarred": "pantry", "bottled": "pantry",
                           "dried": "pantry", "fresh": "produce"}[pref]
            variants.add(rest)
            variants.add(rest.replace(" ", "-"))
    if prefix_zone:
        for cand in (prefix_zone, prefix_zone.split("-")[0]):
            for sz in store_zones:
                if cand_match(sz, cand):
                    return sz
    for v in variants:
        if v in LUT:
            z = ZONE_ALIASES.get(LUT[v], LUT[v])
            for cand in (z, z.split("-")[0]):
                for sz in store_zones:
                    if cand_match(sz, cand):
                        return sz
    # head-noun scan (last word) — "canned tomatoes" -> tomatoes, then
    # "bag of apples" -> apples; weaker than exact, stronger than substring
    words = it.split()
    if words:
        head = norm_item(words[-1])
        if head in LUT:
            z = LUT[head]
            z = ZONE_ALIASES.get(z, z) if z else None
            if z:
                for sz in store_zones:
                    if cand_match(sz, z):
                        return sz
    # full substring scan, last resort
    for w, z in LUT.items():
        if w and len(w) > 3 and (w in it or it in w):
            z = ZONE_ALIASES.get(z, z)
            for sz in store_zones:
                if cand_match(sz, z):
                    return sz
    return None


def cand_match(store_zone, canon):
    return (store_zone.lower() == canon
            or canon in store_zone.lower()
            or store_zone.lower() in canon)


def load_store(name):
    p = STATE_DIR / f"{name}.json"
    if not p.exists():
        return None
    return json.loads(p.read_text())


def save_store(data, name):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (STATE_DIR / f"{name}.json").write_text(json.dumps(data, indent=2))


def new_store(name):
    return {"name": name, "zones": [], "learned": {}, "staples": {}}


def cmd_map_store(args):
    data = load_store(args.name) or new_store(args.name)
    print(f"Mapping store '{args.name}'.")
    if data["zones"]:
        print("Current zones (walking order):")
        for i, z in enumerate(data["zones"], 1):
            print(f"  {i:>2}. {z}")
        if input("Redo from scratch? [y/N] ").strip().lower() != "y":
            return 0
        data["zones"] = []
    print("Name each zone in the order you WALK it, entrance -> checkout.")
    print("8-12 zones is ideal. Blank line to finish. Examples: produce,")
    print("bakery, deli, dairy, meat, pantry, household, frozen, checkout")
    while True:
        try:
            z = input(f"zone {len(data['zones'])+1}: ").strip()
        except EOFError:
            break
        if not z:
            break
        z = z.lower()
        if z not in data["zones"]:
            data["zones"].append(z)
    if len(data["zones"]) < 3:
        print("[!] fewer than 3 zones — a map this small saves nothing")
        return 1
    save_store(data, args.name)
    print(f"saved {len(data['zones'])} zones for '{args.name}'")
    return 0


def parse_list(text):
    items = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        prio = line.startswith("!")
        if prio:
            line = line[1:].strip()
        hint = None
        m = re.match(r"(.+?)\s*\[([^\]]+)\]$", line)
        if m:
            line, hint = m.group(1).strip(), m.group(2).strip().lower()
        items.append({"name": line, "prio": prio, "hint": hint})
    return items


def cmd_route(args):
    data = load_store(args.store)
    if not data or not data["zones"]:
        print(f"[!] store '{args.store}' not mapped. Run map-store first.")
        return 1
    text = Path(args.list).read_text()
    items = parse_list(text)
    zones = data["zones"]
    learned = data.get("learned", {})
    placed = {z: [] for z in zones}
    unplaced = []
    for it in items:
        if it["hint"]:
            z = next((sz for sz in zones if cand_match(sz, it["hint"])), None)
        else:
            z = match_zone(it["name"], zones, learned)
        if z:
            placed[z].append(it)
        else:
            unplaced.append(it)
    # interactive learning for unplaced (EOF/pipe-end breaks safely)
    if unplaced:
        print("\nUnplaced items — tell me the zone (learned for next time):")
        for it in unplaced[:]:
            print("  zones: " + ", ".join(zones))
            try:
                ans = input(f"  '{it['name']}' -> ").strip().lower()
            except EOFError:
                break
            if not ans:
                continue
            z = next((sz for sz in zones if cand_match(sz, ans)), None)
            if z:
                placed[z].append(it)
                learned[norm_item(it["name"])] = z
                unplaced.remove(it)
    data["learned"] = learned
    save_store(data, args.store)

    total = sum(len(v) for v in placed.values()) + len(unplaced)
    print(f"\n{args.store.upper()} — route (entrance -> checkout), "
          f"{total} items, {sum(1 for v in placed.values() if v)} zones")
    print("=" * 62)
    for i, z in enumerate(zones, 1):
        if placed[z]:
            flags = " ".join(it["name"] + ("(!)" if it["prio"] else "")
                             for it in placed[z])
            print(f"[{i:>2} {z}] {flags}")
    if unplaced:
        print(f"[?? unplaced] " + ", ".join(it["name"] for it in unplaced)
              + "  (run interactively to teach zones)")

    if args.staples:
        radar = staples_radar(data)
        if radar:
            print("\nSTAPLES RADAR (probably out or due):")
            for name, days, cad in radar:
                print(f"  - {name}: {days}d since bought (cadence {cad}d)"
                      if days is not None else
                      f"  - {name}: never marked bought (cadence {cad}d)")
    return 0


def staples_radar(data):
    out = []
    now = time.time()
    for name, rec in data.get("staples", {}).items():
        cad = rec.get("days", 7)
        last = rec.get("last_bought")
        days = int((now - last) / 86400) if last else None
        if days is None or days >= cad - 1:
            out.append((name, days, cad))
    return sorted(out, key=lambda t: -(t[1] if t[1] is not None else 999))


def cmd_staples(args):
    data = load_store(args.store)
    if not data:
        data = new_store(args.store)
    staples = data.setdefault("staples", {})
    if args.add:
        for name in args.add:
            staples[name.lower()] = {"days": args.days or 7,
                                     "last_bought": None}
        print(f"staples added: {', '.join(args.add)} "
              f"(cadence {args.days or 7}d)")
    if args.bought:
        now = time.time()
        for name in args.bought:
            if name.lower() in staples:
                staples[name.lower()]["last_bought"] = now
            else:
                staples[name.lower()] = {"days": 7, "last_bought": now}
        print(f"marked bought: {', '.join(args.bought)}")
    if args.remove:
        for name in args.remove:
            staples.pop(name.lower(), None)
        print(f"removed: {', '.join(args.remove)}")
    save_store(data, args.store)
    print(f"\nstaples for {args.store}:")
    radar = staples_radar(data)
    due = {n for n, *_ in radar}
    for name, rec in sorted(staples.items()):
        last = rec.get("last_bought")
        days = int((time.time() - last) / 86400) if last else None
        mark = " <-- DUE" if name in due else ""
        print(f"  {name:<20} cadence {rec.get('days',7)}d, "
              f"bought {'never' if days is None else f'{days}d ago'}{mark}")
    return 0


def cmd_merge(args):
    stores = [s.strip() for s in args.stores.split(",")]
    text = Path(args.list).read_text()
    items = parse_list(text)
    print(f"MULTI-STORE TRIP — {len(stores)} stores, {len(items)} items")
    print("=" * 62)
    leftovers = items
    for s in stores:
        data = load_store(s)
        if not data or not data["zones"]:
            print(f"\n[{s}] NOT MAPPED — skipping (map-store first)")
            continue
        placed = {z: [] for z in data["zones"]}
        rest = []
        learned = data.get("learned", {})
        for it in leftovers:
            z = match_zone(it["name"], data["zones"], learned)
            if z:
                placed[z].append(it)
            else:
                rest.append(it)
        leftovers = rest
        print(f"\n[{s}]")
        for i, z in enumerate(data["zones"], 1):
            if placed[z]:
                print(f"  [{i:>2} {z}] "
                      + ", ".join(it["name"] for it in placed[z]))
    if leftovers:
        print("\n[unmatched anywhere] "
              + ", ".join(it["name"] for it in leftovers)
              + "\n  -> teach zones per store (interactive route) or add "
              "a store that carries them")
    print("\nSuggested store order: the one with the most frozen/refrigerated")
    print("hits LAST (cold-chain time), closest-parking store FIRST if")
    print("buying heavy items (cases of water, bags of food).")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("map-store", help="define store zones interactively")
    p.add_argument("--name", required=True)
    p.set_defaults(fn=cmd_map_store)
    p = sub.add_parser("route", help="sort list into walking order")
    p.add_argument("--store", required=True)
    p.add_argument("list")
    p.add_argument("--staples", action="store_true")
    p.set_defaults(fn=cmd_route)
    p = sub.add_parser("staples", help="manage staples radar")
    p.add_argument("--store", required=True)
    p.add_argument("--add", nargs="+")
    p.add_argument("--days", type=int, default=None)
    p.add_argument("--bought", nargs="+")
    p.add_argument("--remove", nargs="+")
    p.set_defaults(fn=cmd_staples)
    p = sub.add_parser("merge", help="multi-store routing")
    p.add_argument("--stores", required=True, help="comma-separated")
    p.add_argument("list")
    p.set_defaults(fn=cmd_merge)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
