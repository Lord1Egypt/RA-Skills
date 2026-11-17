#!/usr/bin/env python3
"""Hand-Me-Down Flow — registry of stored kids' items + per-kid fit-window
matching, chain verdicts (donate/pass), transfer manifests, storage risk
flags. Pure stdlib, JSON storage.

Examples:
    python3 handmedown.py --data fam.json add-kid --name Mia --birthday 2021-04-10
    python3 handmedown.py --data fam.json add --name "winter coat" --category clothes \
        --size 4T --season winter --condition B --location "closet bin 2"
    python3 handmedown.py --data fam.json match
    python3 handmedown.py --data fam.json manifest --to Emma
"""
import argparse
import json
import sys
from datetime import date

# size label -> (fit_lo_months, fit_hi_months) median windows
SIZE_WINDOWS = {
    "NB": (0, 1), "3M": (0, 3), "6M": (3, 6), "9M": (6, 9), "12M": (9, 12),
    "18M": (12, 18), "24M": (18, 24), "2T": (20, 28), "3T": (30, 38),
    "4T": (38, 46), "4": (44, 52), "5": (50, 58), "6": (58, 68),
    "7": (66, 78), "8": (76, 88), "10": (86, 100), "12": (96, 116),
    "14": (112, 134), "S": (96, 116), "M": (112, 134), "L": (128, 150),
}

# US kids shoe sizes -> months (feet: ~half size per 3-4 months to age 5)
SHOE_WINDOWS = {
    "4": (12, 16), "5": (15, 20), "6": (17, 22), "7": (20, 26),
    "8": (26, 32), "9": (32, 38), "10": (38, 45), "11": (44, 50),
    "12": (49, 55), "13": (54, 60), "13.5": (56, 62),
    "y1": (60, 68), "y2": (66, 74), "y3": (72, 80), "y4": (78, 86),
    "y5": (84, 92), "y6": (90, 100), "y7": (96, 108),
}

STORAGE_RISK = {
    "attic": "HEAT: 50-65C summer peaks destroy elastic/foam/laminates in 1-3 seasons. Move A/B items.",
    "basement": "DAMP: mildew on cotton above ~65% RH. Use sealed bins + desiccant, check quarterly.",
    "garage": "TEMP SWINGS + PESTS: rodents, exhaust. Hard goods OK; no textiles long-term.",
    "closet": "Ideal: interior closet, sealed clear bins, items washed.",
    "crawl": "DAMP like basement; worst textile location.",
}


def load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"kids": [], "items": []}


def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def months_between(d0, d1):
    return (d1.year - d0.year) * 12 + (d1.month - d0.month) + (d1.day - d0.day) / 30.0


def age_months(birthday, today):
    return months_between(date.fromisoformat(birthday), today)


def window_for(size_label, shift=0, category="clothes"):
    table = SHOE_WINDOWS if category == "shoes" else SIZE_WINDOWS
    if size_label in table:
        lo, hi = table[size_label]
        return lo + shift, hi + shift
    # EU height sizes like 92/104 -> approximate months
    try:
        cm = int(size_label)
        if 50 <= cm <= 176:
            # rough: months ~= (cm - 44) / 6.5
            m = (cm - 44) / 6.5
            return m - 6, m + 6
    except ValueError:
        pass
    return None


def season_compatible(item_season, month):
    if item_season in ("all", None, ""):
        return True
    winter = {11, 0, 1, 2}
    summer = {5, 6, 7, 8}
    spring_fall = {3, 4, 9, 10}
    m = month % 12
    if item_season == "winter":
        return m in winter
    if item_season == "summer":
        return m in summer
    if item_season in ("spring", "fall"):
        return m in spring_fall
    return True


def month_in_months(month, horizon_months, today):
    """iterate next horizon months of calendar months"""
    return [(today.month - 1 + i) % 12 + 1 for i in range(horizon_months)]


def main():
    ap = argparse.ArgumentParser(description="Hand-me-down chain registry & matcher")
    ap.add_argument("--data", default="handmedown.json")
    ap.add_argument("--fit-shift-months", type=float, default=0.0,
                    help="negative = kid fits sizes earlier (big kid)")
    ap.add_argument("--today", default=None, help="override today YYYY-MM-DD")
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("add-kid")
    p.add_argument("--name", required=True)
    p.add_argument("--birthday", required=True, help="YYYY-MM-DD")

    p = sub.add_parser("add")
    p.add_argument("--name", required=True)
    p.add_argument("--category", default="clothes",
                   choices=["clothes", "outerwear", "shoes", "gear", "toys", "books"])
    p.add_argument("--size", default="")
    p.add_argument("--season", default="all",
                   choices=["all", "winter", "spring", "summer", "fall"])
    p.add_argument("--condition", required=True, choices=list("ABCD"))
    p.add_argument("--location", default="closet")
    p.add_argument("--note", default="")

    p = sub.add_parser("match")
    p.add_argument("--horizon-months", type=int, default=6)
    p.add_argument("--chain-only", action="store_true")

    p = sub.add_parser("manifest")
    p.add_argument("--to", required=True, help="receiving family/kid name")
    p.add_argument("--items", nargs="*", default=None,
                   help="item ids (default: all C/D or unassigned)")

    p = sub.add_parser("list", help="dump registry")
    p.add_argument("remove", help="item id", nargs="?")  # unused, keeps help clean

    a = ap.parse_args()
    data = load(a.data)
    today = date.fromisoformat(a.today) if a.today else date.today()

    if a.cmd == "add-kid":
        data["kids"].append({"name": a.name, "birthday": a.birthday})
        save(a.data, data)
        print(f"Kid added: {a.name} (birthday {a.birthday}) — {len(data['kids'])} kids total")
        return

    if a.cmd == "add":
        item = {
            "id": len(data["items"]) + 1,
            "name": a.name, "category": a.category, "size": a.size,
            "season": a.season, "condition": a.condition,
            "location": a.location, "note": a.note,
        }
        data["items"].append(item)
        save(a.data, data)
        risk = STORAGE_RISK.get(a.location.lower().split()[0] if a.location else "", "")
        print(f"Item #{item['id']} added: {a.name} [{a.condition}] {a.size or '-'} {a.season}")
        if a.condition == "D":
            print("  NOTE: D-grade — do not store; donate/dispose now.")
        if risk and "Ideal" not in risk:
            print(f"  STORAGE RISK ({a.location}): {risk}")
        return

    if a.cmd == "list":
        print(json.dumps(data, indent=2))
        return

    if a.cmd == "match":
        kids = data["kids"]
        items = data["items"]
        if not kids:
            print("No kids in registry. add-kid first."); sys.exit(1)
        shift = a.fit_shift_months
        if not a.chain_only:
            for kid in kids:
                age = age_months(kid["birthday"], today)
                print("=" * 66)
                print(f"{kid['name']} — {age:.0f} months old")
                print("=" * 66)
                pull, later, closing = [], [], []
                for it in items:
                    win = window_for(it["size"], shift, it["category"]) if it["size"] else None
                    if win is None:
                        continue
                    lo, hi = win
                    if age < lo - 0.5:
                        if lo - age <= a.horizon_months:
                            later.append((it, lo - age))
                    elif age <= hi:
                        # fits now; season check
                        if it["season"] in ("all", "") or season_compatible(
                                it["season"], today.month) or any(
                                season_compatible(it["season"], m)
                                for m in month_in_months(today.month, 3, today)):
                            pull.append(it)
                            if hi - age < 3:
                                closing.append(it)
                        else:
                            later.append((it, 0))
                    else:
                        continue
                if pull:
                    print(f"  PULL NOW ({len(pull)}):")
                    for it in pull:
                        flag = "  << window closing <3mo" if it in closing else ""
                        print(f"    #{it['id']:>3} [{it['condition']}] {it['name']:<30s} "
                              f"{it['size'] or '-':<4} {it['season']:<7} @ {it['location']}{flag}")
                else:
                    print("  PULL NOW: nothing in storage fits this season.")
                if later:
                    print(f"  IN NEXT {a.horizon_months} MONTHS ({len(later)}):")
                    for it, mo in sorted(later, key=lambda t: t[1]):
                        when = "now (season)" if mo == 0 else f"in {mo:.0f} mo"
                        print(f"    #{it['id']:>3} [{it['condition']}] {it['name']:<30s} "
                              f"{it['size'] or '-':<4} — {when}")
                print()
        # chain verdicts: does ANY kid ever fit each item again?
        print("=" * 66)
        print("CHAIN VERDICTS (everyone only gets older)")
        print("=" * 66)
        for it in items:
            win = window_for(it["size"], shift, it["category"]) if it["size"] else None
            futures = []
            for kid in kids:
                age = age_months(kid["birthday"], today)
                if win is None:
                    futures.append((kid["name"], "no-size"))
                    continue
                lo, hi = win
                if age < lo:
                    futures.append((kid["name"], f"fits in {lo-age:.0f} mo"))
                elif age <= hi:
                    futures.append((kid["name"], "fits now"))
            if futures and all(f == "no-size" for _, f in futures):
                print(f"  #{it['id']:>3} {it['name']:<30} no size data — manual call")
            elif not futures:
                print(f"  #{it['id']:>3} {it['name']:<30} NO FUTURE RECIPIENT — "
                      f"PASS ALONG / DONATE now")
            else:
                who = ", ".join(f"{n} ({w})" for n, w in futures)
                print(f"  #{it['id']:>3} {it['name']:<30} -> {who}")
        return

    if a.cmd == "manifest":
        ids = [int(x) for x in (a.items or [])] if a.items else None
        batch = [it for it in data["items"]
                 if (ids is None and it["condition"] in "CD") or (ids and it["id"] in ids)]
        if not batch:
            print("No items selected (default takes C/D-grade items).")
            return
        print("=" * 66)
        print(f"TRANSFER MANIFEST — to: {a.to} — {today.isoformat()}")
        print("=" * 66)
        for it in batch:
            print(f"  #{it['id']:>3} [{it['condition']}] {it['name']:<30s} "
                  f"size {it['size'] or '-':<4} {it['season']:<7}")
            if it["note"]:
                print(f"        note: {it['note']}")
        counts = {g: sum(1 for it in batch if it["condition"] == g) for g in "ABCD"}
        print("-" * 66)
        print(f"Totals: {len(batch)} items — " +
              ", ".join(f"{g}:{counts[g]}" for g in "ABCD" if counts[g]))
        print("Grades: A=new/tags B=gentle C=visible wear D=play-only")
        # remove transferred items from registry
        data["items"] = [it for it in data["items"] if it not in batch]
        save(a.data, data)
        print(f"(Removed {len(batch)} items from registry — they left the chain.)")
        return

    ap.print_help()


if __name__ == "__main__":
    main()
