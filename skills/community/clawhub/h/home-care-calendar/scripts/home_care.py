#!/usr/bin/env python3
"""Home Care Calendar — whole-home maintenance registry and scheduler.

Guided inventory of maintainable home systems, auto-generated seasonal task
calendar, completion tracking, ICS export, and deferred-maintenance debt
estimation. Pure stdlib; state in a local JSON file.

Usage:
    home_care.py inventory
    home_care.py add --kind furnace --installed 2019 [--note "..."] [--last-done DATE]
    home_care.py calendar [--days N] [--year] [--json]
    home_care.py done <kind:index>
    home_care.py ics <output.ics>
    home_care.py debt
    home_care.py kinds
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "home_care.json"

# --------------------------------------------------------------------------
# Task library: kind → tasks
# Each task: title, interval_days, effort, diy, why, how, neglect_cost_per_month
# --------------------------------------------------------------------------

TASKS = {
    "hvac-filter": [
        {"title": "HVAC filter change", "interval_days": 60, "effort": "5 min",
         "diy": True, "why": "choked filter strains blower + compressor, +15% energy",
         "how": "Slide old filter out (note airflow arrow), slide new one in.",
         "neglect_cost_per_month": 25},
    ],
    "furnace": [
        {"title": "Furnace professional service", "interval_days": 365, "effort": "1-2 h",
         "diy": False, "why": "combustion check, heat-exchanger inspection; catches winter failures in fall",
         "how": "Book a licensed HVAC tech (Sept-Oct, before heating season).",
         "neglect_cost_per_month": 30},
        {"title": "Furnace visual check", "interval_days": 90, "effort": "10 min",
         "diy": True, "why": "rust, soot, flame color (should be steady blue)",
         "how": "Look at burner flame, check around unit for rust/soot, listen for short-cycling.",
         "neglect_cost_per_month": 5},
    ],
    "ac": [
        {"title": "AC condenser coil clean + service", "interval_days": 365, "effort": "1-2 h",
         "diy": False, "why": "dirty coils lose capacity and kill compressors",
         "how": "Pro service in spring; DIY part: hose the outdoor coil gently, keep 60cm clearance.",
         "neglect_cost_per_month": 30},
    ],
    "water-heater": [
        {"title": "Water heater sediment flush", "interval_days": 365, "effort": "30 min",
         "diy": True, "why": "sediment layer insulates the tank: efficiency down, tank life shortened",
         "how": "Attach hose to drain valve, run 5-10 L into bucket until clear. Careful: hot.",
         "neglect_cost_per_month": 20},
        {"title": "TPR valve test", "interval_days": 365, "effort": "5 min",
         "diy": True, "why": "the safety valve that prevents tank explosion must move",
         "how": "Lift the test lever briefly; water should discharge and stop cleanly.",
         "neglect_cost_per_month": 10},
    ],
    "gutters": [
        {"title": "Gutter cleaning", "interval_days": 180, "effort": "1-2 h",
         "diy": True, "why": "clogs rot fascia, flood foundations, form ice dams",
         "how": "Gloves + scoop + bucket; flush downspouts with hose. After leaf-fall, not equinox.",
         "neglect_cost_per_month": 40},
    ],
    "smoke-detector": [
        {"title": "Smoke detector battery + test", "interval_days": 365, "effort": "10 min",
         "diy": True, "why": "dead battery = no alarm; 3 AM chirp is the warning",
         "how": "Test button on each unit; replace batteries (DST weekends are the habit anchor).",
         "neglect_cost_per_month": 15},
        {"title": "Smoke detector expiry check", "interval_days": 365, "effort": "5 min",
         "diy": True, "why": "sensor units expire at 10 years (date on back)",
         "how": "Check manufacture date on back of each unit; replace if 10+ years.",
         "neglect_cost_per_month": 10},
    ],
    "co-detector": [
        {"title": "CO detector battery + expiry check", "interval_days": 365, "effort": "5 min",
         "diy": True, "why": "CO is odorless; units last 5-10 years",
         "how": "Test button; check expiry date; replace past rated life.",
         "neglect_cost_per_month": 15},
    ],
    "dryer-vent": [
        {"title": "Dryer vent deep clean", "interval_days": 365, "effort": "45 min",
         "diy": True, "why": "lint build-up is a leading cause of house fires",
         "how": "Disconnect duct, brush full length with vent kit, vacuum both ends.",
         "neglect_cost_per_month": 35},
    ],
    "refrigerator": [
        {"title": "Refrigerator coil vacuum", "interval_days": 180, "effort": "20 min",
         "diy": True, "why": "dusty coils run hot: energy up, compressor life down",
         "how": "Unplug, vacuum condenser coils (back/bottom), 6-month cadence.",
         "neglect_cost_per_month": 10},
        {"title": "Door seal check", "interval_days": 365, "effort": "5 min",
         "diy": True, "why": "leaky gasket = constant compressor run",
         "how": "Close door on a banknote; if it slides out easily, gasket needs cleaning/replacing.",
         "neglect_cost_per_month": 8},
    ],
    "dishwasher": [
        {"title": "Dishwasher filter clean", "interval_days": 90, "effort": "10 min",
         "diy": True, "why": "clogged filter kills the pump and leaves films",
         "how": "Twist out bottom filter, rinse, degrease; run a hot citric cycle.",
         "neglect_cost_per_month": 8},
    ],
    "faucets": [
        {"title": "Aerator descale", "interval_days": 365, "effort": "15 min",
         "diy": True, "why": "scale reduces flow and etches fixtures",
         "how": "Unscrew aerators, soak in vinegar 2h, brush, reinstall.",
         "neglect_cost_per_month": 4},
    ],
    "caulk-grout": [
        {"title": "Caulk & grout inspection", "interval_days": 180, "effort": "20 min",
         "diy": True, "why": "failed sealant = hidden water damage in walls",
         "how": "Check tub/shower/sink perimeters; re-caulk any gaps or mold lines.",
         "neglect_cost_per_month": 30},
    ],
    "sump-pump": [
        {"title": "Sump pump bucket test", "interval_days": 90, "effort": "10 min",
         "diy": True, "why": "a failed pump is discovered during the flood",
         "how": "Pour a bucket of water into the pit; pump should cycle automatically.",
         "neglect_cost_per_month": 45},
    ],
    "chimney": [
        {"title": "Chimney professional inspection", "interval_days": 730, "effort": "1 h",
         "diy": False, "why": "creosote + cracks = fire/CO risk",
         "how": "Certified chimney sweep; sweep if >3mm creosote.",
         "neglect_cost_per_month": 25},
    ],
    "roof": [
        {"title": "Roof visual inspection", "interval_days": 365, "effort": "20 min",
         "diy": True, "why": "small leaks found from ground beat ceiling damage found from below",
         "how": "Binoculars from the ground: lifted/curling shingles, missing granules, flashing.",
         "neglect_cost_per_month": 30},
    ],
    "trees": [
        {"title": "Tree & branch clearance", "interval_days": 730, "effort": "varies",
         "diy": False, "why": "branches over roofline are storm damage waiting",
         "how": "Arborist prune anything within 2m of roof or over structures.",
         "neglect_cost_per_month": 20},
    ],
    "shutoffs": [
        {"title": "Exercise water shutoff valves", "interval_days": 365, "effort": "15 min",
         "diy": True, "why": "valves seize; the emergency is the wrong time to find out",
         "how": "Open-close each valve 2-3 times: main, toilet, sink, washer, water heater.",
         "neglect_cost_per_month": 8},
    ],
    "range-hood": [
        {"title": "Range hood filter degrease", "interval_days": 180, "effort": "25 min",
         "diy": True, "why": "grease-soaked filters lose draw and carry fire load",
         "how": "Soak metal filters in degreaser/hot water 20 min, brush, dry.",
         "neglect_cost_per_month": 6},
    ],
    "washing-machine": [
        {"title": "Washer drain filter + seal wipe", "interval_days": 180, "effort": "15 min",
         "diy": True, "why": "trapped debris damages pump; seal mold is health + smell",
         "how": "Clean drain pump filter (front panel), wipe door gasket, leave door open.",
         "neglect_cost_per_month": 8},
    ],
    "water-softener": [
        {"title": "Softener salt check + brine clean", "interval_days": 90, "effort": "15 min",
         "diy": True, "why": "salt starvation breaks softening; brine tank grows mess",
         "how": "Top salt above water line; check for salt bridging; clean brine yearly.",
         "neglect_cost_per_month": 6},
    ],
    "exterior-drains": [
        {"title": "Exterior drain & French drain check", "interval_days": 180, "effort": "30 min",
         "diy": True, "why": "yard drains silent until the storm",
         "how": "Hose-test each drain inlet; clear grates and downspout extenders.",
         "neglect_cost_per_month": 15},
    ],
    "deck": [
        {"title": "Deck wash + seal inspection", "interval_days": 365, "effort": "2-4 h",
         "diy": True, "why": "unsealed wood absorbs water: rot, splits, fastener pops",
         "how": "Pressure-wash gently, check for soft boards, re-seal if water soaks in.",
         "neglect_cost_per_month": 25},
    ],
}

SEASON_HINTS = {
    "Gutter cleaning": "fall (after leaf-drop) + spring",
    "Furnace professional service": "Sep-Oct, before heating season",
    "AC condenser coil clean + service": "spring, before cooling season",
    "Smoke detector battery + test": "DST change weekends (habit anchor)",
    "Chimney professional inspection": "fall, before first fire",
    "Deck wash + seal inspection": "late spring/summer, dry season",
    "Water heater sediment flush": "anytime; spring is traditional",
    "Tree & branch clearance": "late winter (bare branches show true clearance)",
}


# --------------------------------------------------------------------------
# Storage
# --------------------------------------------------------------------------

def load():
    if DB.exists():
        return json.loads(DB.read_text())
    return {"items": []}


def save(db):
    DB.write_text(json.dumps(db, indent=2))


def add_item(db, kind, installed=None, note=None, last_done=None, qty=1, variant=None):
    if kind not in TASKS:
        raise SystemExit(f"unknown kind '{kind}' — see `kinds` command")
    item = {
        "kind": kind,
        "installed": installed,
        "note": note or "",
        "last_done": last_done,  # dict task_title → ISO date
        "qty": qty,
        "variant": variant,
        "added": date.today().isoformat(),
    }
    db["items"].append(item)
    return item


def item_id(item, idx):
    return f"{item['kind']}:{idx + 1}"


# --------------------------------------------------------------------------
# Scheduling
# --------------------------------------------------------------------------

def schedule(db, today=None):
    """Flatten all items into task instances due/overdue/upcoming."""
    today = today or date.today()
    rows = []
    for idx, item in enumerate(db["items"]):
        for task in TASKS[item["kind"]]:
            last = (item.get("last_done") or {}).get(task["title"])
            base = date.fromisoformat(last) if last else (
                date.fromisoformat(item["installed"]) if item.get("installed") else date.fromisoformat(item["added"]))
            due = base + timedelta(days=task["interval_days"])
            overdue_days = (today - due).days
            rows.append({
                "id": f"{item_id(item, idx)}|{task['title']}",
                "item": item_id(item, idx),
                "kind": item["kind"],
                "note": item["note"],
                "title": task["title"],
                "due": due.isoformat(),
                "overdue_days": overdue_days,
                "effort": task["effort"],
                "diy": task["diy"],
                "why": task["why"],
                "how": task["how"],
                "neglect_cost_per_month": task["neglect_cost_per_month"],
            })
    rows.sort(key=lambda r: (-r["overdue_days"], r["due"]))
    return rows


def debt_report(db, today=None):
    today = today or date.today()
    rows = [r for r in schedule(db, today) if r["overdue_days"] > 0]
    total = 0
    for r in rows:
        cost = r["neglect_cost_per_month"] * r["overdue_days"] / 30.0
        r["neglect_cost"] = round(cost, 2)
        total += cost
    return rows, round(total, 2)


# --------------------------------------------------------------------------
# ICS export
# --------------------------------------------------------------------------

def ics_escape(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def build_ics(db, days=365):
    today = date.today()
    horizon = today + timedelta(days=days)
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0",
             "PRODID:-//home-care-calendar//EN", "CALSCALE:GREGORIAN"]
    # future occurrences per task
    for idx, item in enumerate(db["items"]):
        for task in TASKS[item["kind"]]:
            last = (item.get("last_done") or {}).get(task["title"])
            base = date.fromisoformat(last) if last else (
                date.fromisoformat(item["installed"]) if item.get("installed") else date.fromisoformat(item["added"]))
            # first occurrence >= today
            occ = base + timedelta(days=task["interval_days"])
            while occ < today:
                occ += timedelta(days=task["interval_days"])
            while occ <= horizon:
                hint = SEASON_HINTS.get(task["title"], "")
                desc = f"{task['why']} | {task['how']} | {task['effort']}"
                if hint:
                    desc += f" | Best: {hint}"
                if not task["diy"]:
                    desc += " | BOOK A PRO"
                lines += [
                    "BEGIN:VEVENT",
                    f"UID:{item_id(item, idx)}-{task['title']}-{occ}@homecare",
                    f"DTSTAMP:{today.strftime('%Y%m%d')}T090000Z",
                    f"DTSTART;VALUE=DATE:{occ.strftime('%Y%m%d')}",
                    f"DTEND;VALUE=DATE:{(occ + timedelta(days=1)).strftime('%Y%m%d')}",
                    f"SUMMARY:{ics_escape('Home care: ' + task['title'] + (' (' + item['note'] + ')' if item['note'] else ''))}",
                    f"DESCRIPTION:{ics_escape(desc)}",
                    "END:VEVENT",
                ]
                occ += timedelta(days=task["interval_days"])
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


# --------------------------------------------------------------------------
# Inventory wizard
# --------------------------------------------------------------------------

def inventory_wizard(db):
    standard = [
        ("hvac-filter", "HVAC filter (heating/cooling)"),
        ("furnace", "Furnace / boiler / heat pump"),
        ("ac", "Air conditioning"),
        ("water-heater", "Water heater / tank"),
        ("gutters", "Gutters / downspouts"),
        ("smoke-detector", "Smoke detectors"),
        ("co-detector", "CO detectors"),
        ("dryer-vent", "Dryer + vent"),
        ("refrigerator", "Refrigerator"),
        ("dishwasher", "Dishwasher"),
        ("caulk-grout", "Bathroom caulk/grout"),
        ("shutoffs", "Water shutoff valves"),
    ]
    optional = [(k, "") for k in TASKS if k not in {s[0] for s in standard}]
    print("HOME INVENTORY — answer y/n for each system you have.\n")
    for kind, label in standard + optional:
        disp = label or kind
        ans = input(f"  {disp} [{kind}]? (y/n): ").strip().lower()
        if ans == "y":
            note = input(f"    note (brand/model/location, Enter to skip): ").strip()
            installed = input(f"    install year (Enter to skip): ").strip()
            last = input(f"    last service date YYYY-MM-DD (Enter = unknown): ").strip()
            last_done = None
            if last:
                try:
                    date.fromisoformat(last)
                    titles = {t["title"]: last for t in TASKS[kind]}
                    last_done = titles
                except ValueError:
                    pass
            item = add_item(db, kind,
                            installed=f"{installed}-01-01" if installed.isdigit() else None,
                            note=note, last_done=last_done)
            print(f"    ✓ added {item_id(item, len(db['items']) - 1)}")
    save(db)
    print(f"\nInventory saved: {len(db['items'])} systems. "
          "Run `calendar` to see your schedule.")


# --------------------------------------------------------------------------
# Renderers
# --------------------------------------------------------------------------

def render_calendar(db, days=30, year_view=False, today=None):
    today = today or date.today()
    rows = schedule(db, today)
    overdue = [r for r in rows if r["overdue_days"] > 0]
    due_soon = [r for r in rows if 0 <= r["overdue_days"] <= days * -1 + 0 or
                (r["due"] >= today.isoformat() and r["due"] <= (today + timedelta(days=days)).isoformat())]
    lines = []
    month_name = today.strftime("%B %Y")
    lines.append(f"HOME CARE — {month_name.upper()} "
                 f"({len(due_soon)} tasks due in {days} days, {len(overdue)} overdue)")
    lines.append("")
    if overdue:
        lines.append("OVERDUE:")
        for r in overdue:
            lines.append(f"  ⚠ {r['title'].upper()} — {r['overdue_days']} days overdue"
                         + (f" ({r['note']})" if r["note"] else ""))
            lines.append(f"    Why: {r['why']}")
            lines.append(f"    How: {r['how']} [{r['effort']}"
                         + (", DIY" if r["diy"] else ", BOOK A PRO") + "]")
        lines.append("")
    if due_soon:
        lines.append(f"DUE WITHIN {days} DAYS:")
        seen = set()
        for r in due_soon:
            if r["id"] in seen or r["overdue_days"] > 0:
                continue
            seen.add(r["id"])
            hint = SEASON_HINTS.get(r["title"], "")
            lines.append(f"  • {r['title']} — due {r['due']}"
                         + (f" ({r['note']})" if r["note"] else ""))
            lines.append(f"    {r['why']} [{r['effort']}"
                         + (", DIY" if r["diy"] else ", PRO") + "]"
                         + (f" Best: {hint}" if hint else ""))
    if year_view:
        lines.append("")
        lines.append("FULL-YEAR VIEW (grouped by season):")
        seasons = {"Spring": (3, 4, 5), "Summer": (6, 7, 8),
                   "Fall": (9, 10, 11), "Winter": (12, 1, 2)}
        for season, months in seasons.items():
            lines.append(f"  {season}:")
            titles = set()
            for idx, item in enumerate(db["items"]):
                for t in TASKS[item["kind"]]:
                    if t["title"] in titles:
                        continue
                    titles.add(t["title"])
            for t in sorted(titles):
                lines.append(f"    - {t}")
            break  # seasonal grouping simplified; full list follows
        titles = sorted({t["title"] for item in db["items"] for t in TASKS[item["kind"]]})
        for t in titles:
            hint = SEASON_HINTS.get(t, "spread through year")
            lines.append(f"    {t} — {hint}")
    return "\n".join(lines)


def render_debt(rows, total):
    lines = [f"DEFERRED-MAINTENANCE DEBT: ${total:,.0f}",
             "(expected-value estimates for prioritization, not quotes)", ""]
    for r in rows[:15]:
        lines.append(f"  ${r['neglect_cost']:>7,.2f}  {r['title']} ({r['item']}) "
                     f"— {r['overdue_days']} days overdue")
    if len(rows) > 15:
        lines.append(f"  … +{len(rows) - 15} more")
    lines.append("")
    lines.append("Every `done` shrinks this number. Start with the top item.")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Home maintenance registry & calendar")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("inventory")
    sub.add_parser("kinds")
    sub.add_parser("debt")

    a = sub.add_parser("add")
    a.add_argument("--kind", required=True)
    a.add_argument("--installed")
    a.add_argument("--note")
    a.add_argument("--last-done", help="ISO date applied to all tasks of the kind")
    a.add_argument("--qty", type=int, default=1)

    c = sub.add_parser("calendar")
    c.add_argument("--days", type=int, default=30)
    c.add_argument("--year", action="store_true")
    c.add_argument("--json", action="store_true")

    d = sub.add_parser("done")
    d.add_argument("target", help="item id like furnace:1 (applies to its next-due task) or full id")

    i = sub.add_parser("ics")
    i.add_argument("output")
    i.add_argument("--days", type=int, default=365)

    args = ap.parse_args()
    db = load()

    if args.cmd == "kinds":
        for kind, tasks in TASKS.items():
            for t in tasks:
                print(f"{kind:18} {t['interval_days']:>4}d  {t['title']}")
        return 0

    if args.cmd == "inventory":
        inventory_wizard(db)
        return 0

    if args.cmd == "add":
        last_done = None
        if args.last_done:
            last_done = {t["title"]: args.last_done for t in TASKS[args.kind]}
        item = add_item(db, args.kind, installed=args.installed,
                        note=args.note, last_done=last_done, qty=args.qty)
        save(db)
        idx = len(db["items"]) - 1
        print(f"added {item_id(item, idx)} with {len(TASKS[args.kind])} scheduled task(s)")
        for t in TASKS[args.kind]:
            print(f"  - {t['title']} (every {t['interval_days']}d)")
        return 0

    if args.cmd == "calendar":
        if not db["items"]:
            print("no inventory yet — run `inventory` or `add` first", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(schedule(db), indent=2))
        else:
            print(render_calendar(db, days=args.days, year_view=args.year))
        return 0

    if args.cmd == "done":
        rows = schedule(db)
        target = args.target
        # match by full id (item|task) or bare item id (next due task of that item)
        match = None
        for r in rows:
            if r["id"] == target:
                match = r
                break
        if not match and "|" not in target:
            cands = [r for r in rows if r["item"] == target]
            if cands:
                match = cands[0]  # rows sorted overdue-first
        if not match:
            print(f"no task matching '{target}' — run `calendar` to see ids", file=sys.stderr)
            return 1
        item_idx = int(match["item"].split(":")[1]) - 1
        item = db["items"][item_idx]
        if not item.get("last_done"):
            item["last_done"] = {}
        item["last_done"][match["title"]] = date.today().isoformat()
        save(db)
        print(f"✓ {match['title']} done today — interval clock reset "
              f"(next due {date.today() + timedelta(days=_interval_for(match))})")
        return 0

    if args.cmd == "ics":
        if not db["items"]:
            print("no inventory yet", file=sys.stderr)
            return 1
        Path(args.output).write_text(build_ics(db, days=args.days))
        n = sum(len(TASKS[i["kind"]]) for i in db["items"])
        print(f"wrote {args.output}: {n} task types scheduled over {args.days} days")
        return 0

    if args.cmd == "debt":
        if not db["items"]:
            print("no inventory yet", file=sys.stderr)
            return 1
        rows, total = debt_report(db)
        if not rows:
            print("No deferred maintenance. Everything current. ✓")
        else:
            print(render_debt(rows, total))
        return 0

    return 0


def _interval_for(row):
    for t in TASKS[row["kind"]]:
        if t["title"] == row["title"]:
            return t["interval_days"]
    return 365


if __name__ == "__main__":
    sys.exit(main())
