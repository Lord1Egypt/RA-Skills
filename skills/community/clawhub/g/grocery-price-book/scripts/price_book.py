#!/usr/bin/env python3
"""Grocery Price Book — personal grocery price intelligence.

Logs item prices from receipts, normalizes unit prices, ranks stores by
YOUR basket, detects price increases and shrinkflation, and answers
bulk-buy and membership questions with real math. Pure stdlib; data
stays in a local JSON file.

Usage:
    price_book.py add --store S --item I [--size "2L"] --price P [--date D] [--qty N]
    price_book.py import --store S <receipt.txt>
    price_book.py unit --opts "500g@2.99" "1kg@4.79" ...
    price_book.py report [--json]
    price_book.py bulk --size 15kg --price 19.90 --use 2kg/month --shelf 12months
    price_book.py membership --store costco --fee 60
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import date, datetime
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "pricebook.json"

# --------------------------------------------------------------------------
# Size parsing → (base_quantity, base_unit) normalized to g / ml / ct
# --------------------------------------------------------------------------

ML_IN = {"ml": 1, "l": 1000, "liter": 1000, "litre": 1000, "lt": 1000}
G_IN = {"g": 1, "kg": 1000, "gr": 1, "gram": 1, "kg.": 1000}
# US customary → metric-ish base for unit-price comparison
LB_G = 453.59237
OZ_G = 28.349523
FLOZ_ML = 29.573529
GAL_ML = 3785.412
QT_ML = 946.353
PT_ML = 473.176
CUP_ML = 236.588


def _tokenize_size(s: str):
    """Split '6x330ml' into (6, '330ml') and parse the size token."""
    s = s.strip().lower().replace(" ", "")
    m = re.match(r"^(\d+(?:\.\d+)?)\s*[x×*]\s*(.+)$", s)
    mult, rest = 1, s
    if m:
        mult, rest = float(m.group(1)), m.group(2)
    return mult, rest


def parse_size(s: str):
    """Parse a size string to (quantity, unit) where unit in {g, ml, ct}.

    Returns (None, None) if unparseable. Handles multi-part like
    '24x330ml', '6x1L', '500g', '1lb', '12ct', '1.5L', '16oz'.
    """
    if not s:
        return None, None
    mult, rest = _tokenize_size(s)

    m = re.match(r"^(\d+(?:\.\d+)?)\s*(ct|count|pack|pcs?|pieces?)$", rest)
    if m:
        return mult * float(m.group(1)), "ct"

    m = re.match(r"^(\d+(?:\.\d+)?)\s*(ml|l|liter|litre|lt|floz|fl\.?oz|gal|gallon|qt|quart|pt|pint|cup)s?$", rest)
    if m:
        v, u = float(m.group(1)), m.group(2)
        u = u.replace(".", "")
        if u in ("fl", "floz"):
            return mult * v * FLOZ_ML, "ml"
        factor = {"ml": 1, "l": 1000, "liter": 1000, "litre": 1000, "lt": 1000,
                  "gal": GAL_ML, "gallon": GAL_ML, "qt": QT_ML, "quart": QT_ML,
                  "pt": PT_ML, "pint": PT_ML, "cup": CUP_ML}[u]
        return mult * v * factor, "ml"

    m = re.match(r"^(\d+(?:\.\d+)?)\s*(g|gr|gram|grams|kg|kgs|lb|lbs|pound|pounds|oz|ounce|ounces)$", rest)
    if m:
        v, u = float(m.group(1)), m.group(2)
        factor = {"g": 1, "gr": 1, "gram": 1, "grams": 1, "kg": 1000, "kgs": 1000,
                  "lb": LB_G, "lbs": LB_G, "pound": LB_G, "pounds": LB_G,
                  "oz": OZ_G, "ounce": OZ_G, "ounces": OZ_G}[u]
        return mult * v * factor, "g"

    # bare number → count
    m = re.match(r"^(\d+(?:\.\d+)?)$", rest)
    if m:
        return float(m.group(1)), "ct"
    return None, None


def unit_price(price: float, qty: float, size_qty: float | None, size_unit: str | None):
    """Return (unit_price, display) normalized per 100g / 100ml / 1ct."""
    if not size_qty or not size_unit:
        return None, None
    total = size_qty * qty
    if size_unit in ("g", "ml"):
        per = price / (total / 100.0)
        label = "100g" if size_unit == "g" else "100ml"
    else:
        per = price / total
        label = "ct"
    return per, label


def fuzzy_key(name: str) -> str:
    """Normalize item names for fuzzy matching ('Milk 2% ' == 'milk 2%').

    Strips size-like suffixes ('butter 250g' → 'butter') so receipt imports
    and manual entries land on the same item.
    """
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9% ]", " ", s)
    s = re.sub(r"\b\d+(?:\.\d+)?\s*(?:x\s*)?(?:ml|l|g|kg|lb|oz|ct|count|pack|pcs?)\b", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


# --------------------------------------------------------------------------
# Storage
# --------------------------------------------------------------------------

def load():
    if DB.exists():
        return json.loads(DB.read_text())
    return {"entries": []}


def save(db):
    DB.write_text(json.dumps(db, indent=2))


def add_entry(db, store, item, price, size=None, qty=1, day=None):
    sq, su = parse_size(size) if size else (None, None)
    e = {
        "store": store.lower().strip(),
        "item": item.strip(),
        "price": round(float(price), 2),
        "qty": qty,
        "size_raw": size,
        "size_qty": sq,
        "size_unit": su,
        "date": day or date.today().isoformat(),
    }
    db["entries"].append(e)
    return e


# --------------------------------------------------------------------------
# Receipt import
# --------------------------------------------------------------------------

def parse_receipt(text: str):
    """Extract (item, price) lines from loose receipt text.

    Handles lines like:
        OAT MILK 1L            1.29
        2 x BANANAS            1.98
        FLOUR AP 2.5KG   3.29
    """
    out = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = re.match(r"^(.*?)[\s.]{2,}(\d+[.,]\d{2})$", line)
        if not m:
            m = re.match(r"^(.+?)\s+(\d+[.,]\d{2})$", line)
        if not m:
            continue
        name, price = m.group(1).strip(" .-"), m.group(2).replace(",", ".")
        # skip obvious non-items
        if re.search(r"total|subtotal|tax|vat|cash|card|change|balance|debit|credit|saving|coupon|loyalty|points|thank|phone|www\.|\.com", name, re.I):
            continue
        if len(name) < 2 or float(price) <= 0 or float(price) > 500:
            continue
        qty = 1
        qm = re.match(r"^(\d+)\s*[x×]\s*(.+)$", name)
        if qm:
            qty = int(qm.group(1))
            name = qm.group(2)
        # pull a size out of the name if present (e.g. 'FLOUR AP 2.5KG')
        size = None
        sm = re.search(r"\b(\d+(?:\.\d+)?\s*(?:x\s*)?(?:ml|l|g|kg|lb|oz|ct|count|pack))\b", name, re.I)
        if sm:
            size = re.sub(r"\s+", "", sm.group(1))
            name = (name[:sm.start()] + " " + name[sm.end():]).strip(" .-")
        out.append((name, float(price), qty, size))
    return out


# --------------------------------------------------------------------------
# Analysis
# --------------------------------------------------------------------------

def item_history(db):
    """{fuzzy_key: [(date, store, price, qty, size_qty, size_unit, item)]}"""
    hist = {}
    for e in db["entries"]:
        k = fuzzy_key(e["item"])
        hist.setdefault(k, []).append({
            "date": e["date"], "store": e["store"], "price": e["price"],
            "qty": e["qty"], "size_qty": e["size_qty"],
            "size_unit": e["size_unit"], "item": e["item"],
        })
    for k in hist:
        hist[k].sort(key=lambda x: x["date"])
    return hist


def store_ranking(db):
    """Rank stores by total cost of items available at ≥2 stores (latest obs)."""
    hist = item_history(db)
    stores = sorted({e["store"] for e in db["entries"]})
    # latest price per (item, store)
    per_store = {s: {} for s in stores}
    for k, obs in hist.items():
        for o in obs:
            per_store[o["store"]][k] = o  # obs sorted by date → last wins
    # items present at 2+ stores
    common = [k for k in hist if sum(1 for s in stores if k in per_store[s]) >= 2]
    ranking = []
    for s in stores:
        total = sum(per_store[s][k]["price"] for k in common if k in per_store[s])
        n = sum(1 for k in common if k in per_store[s])
        ranking.append((s, total, n))
    ranking.sort(key=lambda x: x[1])
    return ranking, common, per_store


def price_increases(db, threshold_pct=10.0):
    """Items whose unit price rose > threshold between first and last obs.

    Tracked per (item, store) so switching stores isn't misread as a hike.
    """
    hist = item_history(db)
    out = []
    for k, obs in hist.items():
        by_store = {}
        for o in obs:
            if o["size_qty"] and o["size_unit"]:
                by_store.setdefault(o["store"], []).append(o)
        for store, oo in by_store.items():
            if len(oo) < 2:
                continue
            first, last = oo[0], oo[-1]
            u1 = first["price"] / (first["size_qty"] * first["qty"])
            u2 = last["price"] / (last["size_qty"] * last["qty"])
            if u1 <= 0:
                continue
            pct = (u2 - u1) / u1 * 100
            if pct > threshold_pct:
                out.append({
                    "item": last["item"], "store": store,
                    "from": round(u1 * (100 if first["size_unit"] in ("g", "ml") else 1), 3),
                    "to": round(u2 * (100 if first["size_unit"] in ("g", "ml") else 1), 3),
                    "pct": round(pct, 1), "unit": first["size_unit"],
                    "first_date": first["date"], "last_date": last["date"],
                })
    out.sort(key=lambda x: -x["pct"])
    return out


def shrinkflation(db):
    """Same item, package size decreased while price held or rose."""
    hist = item_history(db)
    out = []
    for k, obs in hist.items():
        sized = [o for o in obs if o["size_qty"] and o["size_unit"]]
        if len(sized) < 2:
            continue
        first, last = sized[0], sized[-1]
        if (first["size_unit"] == last["size_unit"]
                and last["size_qty"] < first["size_qty"] * 0.97
                and last["price"] >= first["price"] * 0.98):
            u1 = first["price"] / first["size_qty"]
            u2 = last["price"] / last["size_qty"]
            out.append({
                "item": last["item"], "store": last["store"],
                "size_from": first["size_qty"], "size_to": last["size_qty"],
                "unit": last["size_unit"], "price_from": first["price"],
                "price_to": last["price"],
                "unit_pct": round((u2 / u1 - 1) * 100, 1) if u1 else None,
            })
    out.sort(key=lambda x: -(x["unit_pct"] or 0))
    return out


def buy_floors(db):
    """Historical lowest price per item (for stock-up timing)."""
    hist = item_history(db)
    floors = []
    for k, obs in hist.items():
        by_store = {}
        for o in obs:
            by_store.setdefault(o["store"], []).append(o)
        for s, oo in by_store.items():
            best = min(oo, key=lambda o: o["price"])
            latest = oo[-1]
            if best["price"] < latest["price"] * 0.95:
                floors.append({
                    "item": latest["item"], "store": s,
                    "floor": best["price"], "floor_date": best["date"],
                    "current": latest["price"],
                })
    floors.sort(key=lambda x: -(x["current"] - x["floor"]))
    return floors


def bulk_advice(size, price, use, shelf_months, db=None):
    """Bulk-buy math: consumption vs shelf life vs savings."""
    sq, su = parse_size(size)
    if not sq:
        return {"error": f"cannot parse size '{size}'"}
    um = re.match(r"^([\d.]+)\s*([a-z]+)\s*/\s*month$", (use or "").lower().replace(" ", ""))
    if not um:
        return {"error": "usage must look like '2kg/month' or '750g/month'"}
    use_q, use_u = float(um.group(1)), um.group(2)
    uq, uu = parse_size(f"{use_q}{use_u}")
    if uq is None:
        return {"error": f"cannot parse usage unit '{use_u}'"}
    months_to_use = sq / uq
    shelf = float(shelf_months.replace("months", "").replace("month", "").strip())
    waste = max(0.0, months_to_use - shelf)
    wasted_frac = min(1.0, waste / months_to_use if months_to_use else 1.0)
    # effective price per usage-unit, accounting for waste
    eff_unit = price / (sq * (1 - wasted_frac)) if sq else None
    return {
        "size": size, "price": price,
        "months_to_consume": round(months_to_use, 1),
        "shelf_life_months": shelf,
        "verdict": "OK — consumed within shelf life" if waste == 0 else
                   f"WASTE — {waste:.1f} months of usage expires unused "
                   f"({wasted_frac*100:.0f}% of purchase)",
        "effective_price_per_use_unit": round(eff_unit, 4) if eff_unit else None,
        "note": "Compare effective price per unit with your regular package; "
                "bulk only wins if it beats the regular unit price AFTER waste.",
    }


def membership_math(db, store, fee):
    ranking, common, per_store = store_ranking(db)
    store = store.lower()
    others = [s for s in per_store if s != store and s in [r[0] for r in ranking]]
    if store not in per_store:
        return {"error": f"no entries for store '{store}'"}
    overlap = [k for k in common if k in per_store[store]]
    if not overlap:
        return {"error": "no overlapping items with other stores yet — log more receipts"}
    savings = 0.0
    details = []
    for k in overlap:
        mine = per_store[store][k]
        other_best = min((per_store[s][k]["price"], s) for s in others if k in per_store[s])
        diff = other_best[0] - mine["price"]
        if abs(diff) > 1e-9:
            savings += diff
            details.append((mine["item"], diff, other_best[1]))
    per_trip = savings
    trips = math.ceil(fee / per_trip) if per_trip > 0 else None
    return {
        "store": store, "fee": fee,
        "overlapping_items": len(overlap),
        "savings_per_trip": round(per_trip, 2),
        "trips_to_breakeven": trips,
        "verdict": (f"Worth it: fee repaid after {trips} trips "
                    f"(~{trips} weeks if weekly)" if per_trip > 0 else
                    "NOT worth it: this store is not cheaper on your items"),
    }


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def fmt_money(x):
    return f"${x:,.2f}"


def render_report(db):
    lines = []
    n_items = len({fuzzy_key(e['item']) for e in db['entries']})
    stores = sorted({e['store'] for e in db['entries']})
    lines.append(f"=== PRICE BOOK: {n_items} items, {len(stores)} stores, "
                 f"{len(db['entries'])} entries ===")
    lines.append("")

    ranking, common, per_store = store_ranking(db)
    if len(ranking) > 1 and common:
        lines.append("STORE RANKING by overlapping-basket cost (lower = better):")
        for i, (s, total, n) in enumerate(ranking, 1):
            lines.append(f"  {i}. {s:10s} {fmt_money(total):>9s}   ({n} common items)")
        if len(ranking) >= 2:
            diff = ranking[-1][1] - ranking[0][1]
            lines.append(f"  → Cheapest vs priciest on your basket: {fmt_money(diff)}/trip"
                         f"  (~{fmt_money(diff*52)}/yr at weekly trips)")
        lines.append("")

    hist = item_history(db)
    lines.append("UNIT-PRICE TABLE (best deal per item flagged):")
    shown = 0
    for k, obs in sorted(hist.items()):
        per_store_obs = {}
        for o in obs:
            if o["size_qty"]:
                per_store_obs[o["store"]] = o
        if len(per_store_obs) < 1:
            continue
        rows = []
        best = None
        for s, o in per_store_obs.items():
            up, label = unit_price(o["price"], o["qty"], o["size_qty"], o["size_unit"])
            if up is None:
                continue
            if best is None or up < best[0]:
                best = (up, s)
            rows.append(f"    {o['item'][:20]:20s} {s:10s} {fmt_money(o['price']):>8s}   "
                        f"${up:.3f}/{label}")
        if rows:
            print_name = obs[-1]["item"]
            lines.append(f"  {print_name}")
            for r in rows:
                star = " ★" if best and f"${best[0]:.3f}" in r else ""
                lines.append(r + star)
            shown += 1
            if shown >= 12:
                lines.append("  … (more items in JSON)")
                break
    lines.append("")

    incs = price_increases(db)
    if incs:
        lines.append("PRICE INCREASES (>10% unit-price jump, tracked items):")
        for i in incs[:6]:
            per = "100g" if i["unit"] == "g" else ("100ml" if i["unit"] == "ml" else "ct")
            lines.append(f"  {i['item']} @ {i['store']}: ${i['from']:.2f} → ${i['to']:.2f} "
                         f"/{per}  +{i['pct']}%  ({i['first_date']} → {i['last_date']})")
        lines.append("")

    shr = shrinkflation(db)
    if shr:
        lines.append("SHRINKFLATION SUSPECTS (size down, price same/up):")
        for s in shr[:6]:
            lines.append(f"  {s['item']} @ {s['store']}: "
                         f"{s['size_from']:.0f}{s['unit']} → {s['size_to']:.0f}{s['unit']} "
                         f"at {fmt_money(s['price_to'])}  → unit price +{s['unit_pct']}% silently")
        lines.append("")

    floors = buy_floors(db)
    if floors:
        lines.append("BULK/STOCK-UP FLOORS (historical lows — buy when at/below):")
        for f in floors[:6]:
            lines.append(f"  {f['item']}: floor {fmt_money(f['floor'])} ({f['store']}, "
                         f"{f['floor_date']}) — current {fmt_money(f['current'])} → "
                         f"{'buy' if f['current'] <= f['floor']*1.03 else 'wait'}")
        lines.append("")
    return "\n".join(lines)


def cmd_unit(opts):
    rows = []
    for o in opts:
        m = re.match(r"^(.*)@([\d.]+)$", o)
        if not m:
            print(f"skip (bad format): {o}", file=sys.stderr)
            continue
        size, price = m.group(1), float(m.group(2))
        sq, su = parse_size(size)
        if not sq:
            print(f"skip (unparseable size): {o}", file=sys.stderr)
            continue
        up, label = unit_price(price, 1, sq, su)
        rows.append((up, size, price, label))
    rows.sort(key=lambda r: r[0])
    print("SHELF COMPARISON (cheapest per unit first):")
    for i, (up, size, price, label) in enumerate(rows):
        star = "  ★BEST" if i == 0 else ""
        print(f"  {size:12s} {fmt_money(price):>8s}  →  ${up:.3f}/{label}{star}")
    if len(rows) >= 2:
        save_pct = (rows[-1][0] - rows[0][0]) / rows[-1][0] * 100
        print(f"  Cheapest option saves {save_pct:.0f}% per unit vs priciest")
    return rows


def main():
    ap = argparse.ArgumentParser(description="Grocery price book")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add")
    a.add_argument("--store", required=True)
    a.add_argument("--item", required=True)
    a.add_argument("--price", required=True, type=float)
    a.add_argument("--size")
    a.add_argument("--qty", type=int, default=1)
    a.add_argument("--date")

    imp = sub.add_parser("import")
    imp.add_argument("--store", required=True)
    imp.add_argument("file")

    u = sub.add_parser("unit")
    u.add_argument("--opts", nargs="+", required=True)

    r = sub.add_parser("report")
    r.add_argument("--json", action="store_true")

    b = sub.add_parser("bulk")
    b.add_argument("--size", required=True)
    b.add_argument("--price", required=True, type=float)
    b.add_argument("--use", required=True, help="e.g. 2kg/month")
    b.add_argument("--shelf", required=True, help="e.g. 12months")

    m = sub.add_parser("membership")
    m.add_argument("--store", required=True)
    m.add_argument("--fee", required=True, type=float)

    args = ap.parse_args()
    db = load()

    if args.cmd == "add":
        e = add_entry(db, args.store, args.item, args.price, args.size, args.qty, args.date)
        save(db)
        sq = f" ({e['size_qty']:.0f}{e['size_unit']})" if e["size_qty"] else ""
        print(f"added: {e['item']}{sq} @ {e['store']} {fmt_money(e['price'])} [{e['date']}]")

    elif args.cmd == "import":
        text = open(args.file, encoding="utf-8", errors="replace").read()
        items = parse_receipt(text)
        if not items:
            print("no item lines found — check the file format", file=sys.stderr)
            return 1
        for name, price, qty, size in items:
            add_entry(db, args.store, name, price, size, qty)
        save(db)
        print(f"imported {len(items)} items from {args.file} @ {args.store}:")
        for name, price, qty, size in items:
            print(f"  {qty}x {name} {size or ''} {fmt_money(price)}")
        return 0

    elif args.cmd == "unit":
        cmd_unit(args.opts)

    elif args.cmd == "report":
        if not db["entries"]:
            print("price book empty — add entries first", file=sys.stderr)
            return 1
        if args.json:
            hist = item_history(db)
            ranking, common, per_store = store_ranking(db)
            print(json.dumps({
                "items": {k: v for k, v in list(hist.items())},
                "store_ranking": ranking,
                "price_increases": price_increases(db),
                "shrinkflation": shrinkflation(db),
                "buy_floors": buy_floors(db),
            }, indent=2, default=str))
        else:
            print(render_report(db))

    elif args.cmd == "bulk":
        res = bulk_advice(args.size, args.price, args.use, args.shelf)
        if "error" in res:
            print(res["error"], file=sys.stderr)
            return 1
        print(json.dumps(res, indent=2))

    elif args.cmd == "membership":
        res = membership_math(db, args.store, args.fee)
        if "error" in res:
            print(res["error"], file=sys.stderr)
            return 1
        print(json.dumps(res, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
