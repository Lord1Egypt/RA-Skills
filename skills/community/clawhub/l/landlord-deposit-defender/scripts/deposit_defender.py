#!/usr/bin/env python3
"""landlord-deposit-defender — security deposit dispute analysis toolkit.

Structures move-in/move-out condition inventories, diffs them, separates
fair wear-and-tear from chargeable damage using useful-life depreciation
conventions, prorates legitimate deductions, cites jurisdiction deposit
deadlines, and drafts an itemized dispute letter.

Stdlib only. Deterministic output. Python 3.9+.

Subcommands:
    inventory      Build a normalized room-by-room condition inventory.
    diff           Compare move-in vs move-out, classify every change.
    prorate        Compute the betterment-corrected maximum deduction.
    letter         Generate a full markdown demand/dispute letter.
    jurisdictions  Print the built-in deposit-deadline table.

This tool is decision support, not legal advice.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Sequence, Tuple

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

#: Condition grading rubric, 0 (like new) .. 5 (destroyed / non-functional).
GRADE_LABELS: Dict[int, str] = {
    0: "like new",
    1: "excellent — negligible signs of use",
    2: "good — light normal wear",
    3: "fair — noticeable wear, functional",
    4: "poor — significant damage, usable",
    5: "ruined — non-functional / needs replacement",
}

#: Typical useful life (years) for common rental fit-out items.
#: Sources: common industry depreciation schedules and IRS-style residential
#: rental property conventions. A lease, local statute or court precedent
#: can override these — treat as defaults, verify where it matters.
USEFUL_LIFE_YEARS: Dict[str, int] = {
    "interior paint": 3,
    "wallpaper": 7,
    "carpet": 8,
    "vinyl flooring": 10,
    "laminate flooring": 15,
    "tile": 25,
    "blinds": 5,
    "curtains": 7,
    "appliances": 12,
    "smoke detector": 10,
    "door": 30,
    "window seals": 20,
}

#: Keyword -> useful-life lookup used when a deduction names an item but the
#: caller did not supply an explicit useful life.
USEFUL_LIFE_KEYWORDS: List[Tuple[str, str]] = [
    ("carpet", "carpet"),
    ("rug", "carpet"),
    ("paint", "interior paint"),
    ("painted", "interior paint"),
    ("wallpaper", "wallpaper"),
    ("vinyl", "vinyl flooring"),
    ("linoleum", "vinyl flooring"),
    ("laminate", "laminate flooring"),
    ("tile", "tile"),
    ("blind", "blinds"),
    ("shade", "blinds"),
    ("curtain", "curtains"),
    ("drape", "curtains"),
    ("fridge", "appliances"),
    ("refrigerator", "appliances"),
    ("freezer", "appliances"),
    ("oven", "appliances"),
    ("stove", "appliances"),
    ("range", "appliances"),
    ("cooktop", "appliances"),
    ("dishwasher", "appliances"),
    ("washer", "appliances"),
    ("dryer", "appliances"),
    ("microwave", "appliances"),
    ("appliance", "appliances"),
    ("smoke detector", "smoke detector"),
    ("smoke alarm", "smoke detector"),
    ("door", "door"),
    ("window seal", "window seals"),
]

#: Defect descriptions that indicate tenant-caused damage, not wear.
DAMAGE_KEYWORDS: List[str] = [
    "burn", "burnt", "burned", "hole", "holes", "punch", "break", "broken",
    "broke", "crack", "cracked", "smash", "smashed", "shatter", "shattered",
    "missing", "gone", "removed", "stolen", "tear", "torn", "ripped",
    "gouge", "gouged", "destroy", "destroyed", "flood", "flooding",
    "water damage", "chew", "chewed", "urine", "nail polish", "ink stain",
    "bleach", "melt", "melted", "slash", "slashed", "cigarette",
]

#: Defect descriptions that indicate ordinary wear-and-tear.
WEAR_KEYWORDS: List[str] = [
    "scuff", "scuffed", "scuffing", "fade", "faded", "fading", "sun-fade",
    "sun fade", "worn", "wear", "ding", "dings", "marked", "marks",
    "small scratch", "light scratch", "minor scratch", "hairline",
    "patina", "tread wear", "traffic pattern", "matting", "flattening",
    "grime", "dust", "dulling", "discolor", "paint chip", "picture hook",
    "nail hole", "pin hole", "thumbtack",
]

#: Deposit-return deadlines by jurisdiction. "typical" values compiled from
#: commonly cited statutes; verify current local law before relying on them.
JURISDICTIONS: Dict[str, Dict[str, Any]] = {
    "US-CA": {
        "name": "California, US",
        "days": 21,
        "window": None,
        "requirement": "Itemized written statement + receipts required with refund.",
        "citation": "Cal. Civ. Code §1950.5",
    },
    "US-NY": {
        "name": "New York, US",
        "days": 14,
        "window": None,
        "requirement": "Itemized statement of repairs + receipts required.",
        "citation": "NY Gen. Oblig. Law §7-108 (14 days, statewide since 2019)",
    },
    "US-TX": {
        "name": "Texas, US",
        "days": 30,
        "window": None,
        "requirement": "Itemized list of deductions required unless tenant owes rent and no deduction is contested.",
        "citation": "Tex. Prop. Code §92.103",
    },
    "US-FL": {
        "name": "Florida, US",
        "days": None,
        "window": (15, 60),
        "requirement": "15 days for no-deduction returns; 30 days (up to 60 by notice) when deductions are intended.",
        "citation": "Fla. Stat. §83.31",
    },
    "US-WA": {
        "name": "Washington, US",
        "days": 21,
        "window": None,
        "requirement": "Full statement of basis for any deduction required.",
        "citation": "RCW 59.18.280",
    },
    "US-OR": {
        "name": "Oregon, US",
        "days": 31,
        "window": None,
        "requirement": "Itemized accounting of deposits held and deductions.",
        "citation": "ORS 90.300",
    },
    "US-CO": {
        "name": "Colorado, US",
        "days": 30,
        "window": None,
        "requirement": "Itemized statement; 60 days allowed if premises damaged.",
        "citation": "Colo. Rev. Stat. §38-12-103",
    },
    "US-IL": {
        "name": "Illinois, US",
        "days": 45,
        "window": None,
        "requirement": "Typical: 30 days to return, 45 days for itemized damage list; applies to 5+ unit buildings; municipal ordinances (e.g. Chicago RLTO) may be stricter.",
        "citation": "765 ILCS 710 (typical)",
    },
    "US-PA": {
        "name": "Pennsylvania, US",
        "days": 30,
        "window": None,
        "requirement": "No single fixed statewide day-count; 30 days is the widely used expectation after forwarding address is given.",
        "citation": "68 P.S. §250.512 (typical reading)",
    },
    "US-GA": {
        "name": "Georgia, US",
        "days": 30,
        "window": None,
        "requirement": "One month typical; itemization not universally required by statute.",
        "citation": "O.C.G.A. §44-7-33 (typical)",
    },
    "US-AZ": {
        "name": "Arizona, US",
        "days": 14,
        "window": None,
        "requirement": "14 business days, itemized list required.",
        "citation": "A.R.S. §33-1321(D)",
    },
    "US-MA": {
        "name": "Massachusetts, US",
        "days": 30,
        "window": None,
        "requirement": "Itemized statement of deductions with receipts.",
        "citation": "M.G.L. c.186 §15B",
    },
    "US-NC": {
        "name": "North Carolina, US",
        "days": 30,
        "window": None,
        "requirement": "30 days, extendable to 60 with an interim itemized accounting.",
        "citation": "N.C. Gen. Stat. §42-52",
    },
    "US-NV": {
        "name": "Nevada, US",
        "days": 30,
        "window": None,
        "requirement": "Itemized accounting of all deductions required.",
        "citation": "NRS 118A.242/.244 (typical)",
    },
    "GB": {
        "name": "England & Wales, UK",
        "days": 10,
        "window": None,
        "requirement": "Deposit must be held in a TDP scheme; refund or agreed disposition within 10 days of the end of tenancy.",
        "citation": "Housing Act 2004 tenancy deposit schemes (typical)",
    },
    "DE": {
        "name": "Germany",
        "days": None,
        "window": None,
        "requirement": "Landlord claims for deterioration must be made within 6 months of handback; normal wear (gewöhnliche Abnutzung) is never chargeable.",
        "citation": "BGB §§548, 306 (typical reading)",
    },
    "AU-NSW": {
        "name": "New South Wales, Australia",
        "days": 14,
        "window": None,
        "requirement": "Bond release agreed or claimed via NSW Fair Trading/NCAT typically within 14 days of tenancy end.",
        "citation": "Residential Tenancies Act 2010 (NSW) (typical)",
    },
    "CA-BC": {
        "name": "British Columbia, Canada",
        "days": 15,
        "window": None,
        "requirement": "15 days with condition-inspection agreement; missing deadline can forfeit the right to claim.",
        "citation": "Residential Tenancy Act (BC) s.38 (typical)",
    },
}

#: Alias table so "CA" -> US-CA, "UK" -> GB etc. (2-letter US states + UK).
JURISDICTION_ALIASES: Dict[str, str] = {
    code.split("-", 1)[1]: code for code in JURISDICTIONS if code.startswith("US-")
}
JURISDICTION_ALIASES["UK"] = "GB"
JURISDICTION_ALIASES["ENGLAND"] = "GB"
JURISDICTION_ALIASES["WALES"] = "GB"
JURISDICTION_ALIASES["NSW"] = "AU-NSW"
JURISDICTION_ALIASES["BC"] = "CA-BC"

DAYS_PER_YEAR = 365.25

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def fail(message: str, exit_code: int = 2) -> None:
    """Print an error to stderr and exit. Always returns nothing."""
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(exit_code)


def parse_iso_date(text: str, flag: str) -> date:
    """Parse a YYYY-MM-DD string into a datetime.date.

    Args:
        text: Date string in ISO format.
        flag: Name of the CLI flag, used in error messages.

    Returns:
        Parsed date.

    Exits with code 2 on malformed input.
    """
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        fail(f"{flag} expects a date in YYYY-MM-DD format, got {text!r}")


def years_between(start: date, end: date) -> float:
    """Return elapsed years between two dates (365.25-day year).

    Rounded to 2 decimals (~3.7-day precision) so whole-year tenancies
    compute to exact values (e.g. 731 days across a leap year -> 2.0).
    """
    if end < start:
        fail("--tenancy-end is before --tenancy-start")
    return round((end - start).days / DAYS_PER_YEAR, 2)


def round2(value: float) -> float:
    """Round a monetary value to 2 decimal places."""
    return round(value + 0.0, 2)


def money(value: float) -> str:
    """Format a monetary value as a dollar string."""
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):,.2f}"


def parse_grade(text: str) -> int:
    """Parse and validate a 0-5 condition grade.

    Exits with code 2 when the grade is out of range or not an integer.
    """
    try:
        grade = int(text.strip())
    except (TypeError, ValueError):
        fail(f"grade must be an integer 0-5, got {text!r}")
    if grade < 0 or grade > 5:
        fail(f"grade must be an integer 0-5, got {grade}")
    return grade


def parse_inventory_item(spec: str) -> Dict[str, Any]:
    """Parse 'room,item,grade0-5,note' into an inventory item dict.

    The note may itself contain commas (it takes the remainder of the
    string). Exits with code 2 on malformed input.
    """
    parts = spec.split(",", 3)
    if len(parts) < 3:
        fail(
            "inventory item must be 'room,item,grade0-5[,note]' "
            f"(note may contain commas), got {spec!r}"
        )
    room, item, grade_text = parts[0].strip(), parts[1].strip(), parts[2]
    note = parts[3].strip() if len(parts) == 4 else ""
    if not room or not item:
        fail(f"inventory item needs a non-empty room and item name, got {spec!r}")
    grade = parse_grade(grade_text)
    return {"room": room, "item": item, "grade": grade, "note": note}


def parse_prorate_item(spec: str, depreciated: bool) -> Dict[str, Any]:
    """Parse 'name,value,useful_life_years[,demanded|age]' for proration.

    Default form:  name,value,useful_life[,demanded] — age is assumed to
    equal the tenancy length (item new at move-in).
    --depreciated: name,value,useful_life,age — the item was already aged at
    move-in, so the caller supplies its true age directly and `demanded`
    defaults to the supplied value.

    Exits with code 2 on malformed input.
    """
    parts = [p.strip() for p in spec.split(",")]
    if not depreciated and len(parts) not in (3, 4):
        fail(f"prorate item must be 'name,value,useful_life_years[,demanded]', got {spec!r}")
    if depreciated and len(parts) != 4:
        fail(f"--depreciated items must be 'name,value,useful_life_years,age_years', got {spec!r}")
    name = parts[0]
    if not name:
        fail(f"prorate item needs a name, got {spec!r}")
    try:
        value = float(parts[1])
        life = float(parts[2])
        extra = float(parts[3]) if len(parts) == 4 else None
    except ValueError:
        fail(f"prorate item numbers must be numeric, got {spec!r}")
    if value < 0:
        fail(f"item value must be >= 0, got {spec!r}")
    if life <= 0:
        fail(f"useful_life_years must be > 0, got {spec!r}")
    if depreciated:
        return {
            "item": name,
            "value": value,
            "useful_life_years": life,
            "age_years": extra,
            "demanded": value,
        }
    return {
        "item": name,
        "value": value,
        "useful_life_years": life,
        "demanded": value if extra is None else extra,
    }


def lookup_useful_life(name: str) -> Optional[int]:
    """Look up a typical useful life (years) for an item by keyword, else None."""
    lowered = name.lower()
    for keyword, category in USEFUL_LIFE_KEYWORDS:
        if keyword in lowered:
            return USEFUL_LIFE_YEARS[category]
    return None


def normalize_jurisdiction(code: str) -> str:
    """Normalize a jurisdiction code (aliases like 'CA' -> 'US-CA').

    Exits with code 2 when the jurisdiction is unknown.
    """
    key = code.strip().upper()
    if key in JURISDICTIONS:
        return key
    if key in JURISDICTION_ALIASES:
        return JURISDICTION_ALIASES[key]
    known = ", ".join(sorted(JURISDICTIONS))
    fail(
        f"unknown jurisdiction {code!r}. Known codes: {known} "
        "(US states also accept their 2-letter code, e.g. CA, TX; UK accepts 'UK')"
    )


def classify_change(
    grade_in: int,
    grade_out: int,
    age_years: Optional[float],
    useful_life_years: Optional[int],
    note: str = "",
) -> Dict[str, Any]:
    """Classify a single item's change between move-in and move-out.

    Rules, applied in order (first match wins):
      1. delta < 0                     -> improvement (tenant left it better)
      2. delta == 0                    -> unchanged
      3. item age >= useful life       -> wear (fully depreciated; landlord
                                          must absorb — charging would be
                                          new-for-old betterment)
      4. damage keyword in note        -> damage (burns, holes, missing ...)
      5. wear keyword in note          -> wear (scuffs, fading, nail holes ...)
      6. delta >= 2 grade points       -> damage (large sudden deterioration)
      7. otherwise                     -> wear (small unexplained deterioration)

    Args:
        grade_in: Move-in condition grade 0-5 (lower is better).
        grade_out: Move-out condition grade 0-5.
        age_years: Item age at move-out, if known.
        useful_life_years: Item useful life, if known.
        note: Move-out (or diff) note describing the defect.

    Returns:
        Dict with delta, direction, classification, basis, and disputable
        flag (True when a landlord charge for this item is contestable).
    """
    delta = grade_out - grade_in
    note_lower = note.lower()

    if delta < 0:
        return {
            "delta": delta,
            "direction": "improved",
            "classification": "improvement",
            "basis": "condition improved versus move-in",
            "disputable": True,
        }
    if delta == 0:
        return {
            "delta": 0,
            "direction": "unchanged",
            "classification": "unchanged",
            "basis": "same grade as move-in",
            "disputable": False,
        }

    if (
        age_years is not None
        and useful_life_years is not None
        and age_years >= useful_life_years
    ):
        return {
            "delta": delta,
            "direction": "degraded",
            "classification": "wear",
            "basis": (
                f"item age {age_years:.1f}y >= useful life {useful_life_years}y: "
                "fully depreciated, replacement cost is landlord's own cost "
                "(no new-for-old betterment)"
            ),
            "disputable": True,
        }
    if any(k in note_lower for k in DAMAGE_KEYWORDS):
        return {
            "delta": delta,
            "direction": "degraded",
            "classification": "damage",
            "basis": "defect description matches tenant-caused damage patterns",
            "disputable": True,
        }
    if any(k in note_lower for k in WEAR_KEYWORDS):
        return {
            "delta": delta,
            "direction": "degraded",
            "classification": "wear",
            "basis": "defect description matches ordinary wear-and-tear patterns",
            "disputable": True,
        }
    if delta >= 2:
        return {
            "delta": delta,
            "direction": "degraded",
            "classification": "damage",
            "basis": "deterioration of 2+ grade points is beyond ordinary wear",
            "disputable": True,
        }
    return {
        "delta": delta,
        "direction": "degraded",
        "classification": "wear",
        "basis": "single-grade deterioration without damage indicators",
        "disputable": True,
    }


def prorate_value(value: float, years_used: float, useful_life_years: float) -> float:
    """Betterment-corrected maximum legitimate deduction.

    legitimate = value * max(0, 1 - years_used / useful_life)

    An item at/past its useful life contributes zero: the landlord received
    the item's full economic life and cannot bill the tenant for a brand-new
    replacement (new-for-old betterment).
    """
    if useful_life_years <= 0:
        fail("useful_life_years must be > 0")
    remaining = max(0.0, 1.0 - years_used / useful_life_years)
    return round2(value * remaining)


def load_inventory(path: str, flag: str) -> Dict[str, Any]:
    """Load and sanity-check an inventory JSON file produced by `inventory`.

    Exits with code 2 on missing/malformed files.
    """
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        fail(f"{flag}: file not found: {path}")
    except json.JSONDecodeError as exc:
        fail(f"{flag}: {path} is not valid JSON: {exc}")
    if not isinstance(data.get("items"), list):
        fail(f"{flag}: {path} has no 'items' list — was it made by `inventory`?")
    for entry in data["items"]:
        if "item" not in entry or "grade" not in entry:
            fail(f"{flag}: {path} contains an item without 'item'/'grade' fields")
    return data


def items_by_key(items: List[Dict[str, Any]]) -> Dict[Tuple[str, str], Dict[str, Any]]:
    """Index inventory items by lowercase (room, item) key."""
    return {
        (str(i.get("room", "")).lower(), str(i["item"]).lower()): i for i in items
    }


def print_json(payload: Any) -> None:
    """Print a JSON dump with stable key order."""
    print(json.dumps(payload, indent=2, sort_keys=False, default=str))


def deadline_description(entry: Dict[str, Any]) -> str:
    """Human sentence describing a jurisdiction's deadline."""
    if entry["days"] is not None:
        return f"{entry['days']} days"
    if entry["window"] is not None:
        lo, hi = entry["window"]
        return f"{lo}-{hi} days"
    return "no fixed day-count (see requirement)"


def add_days(a_date: date, days: int) -> date:
    """Return a_date + days using the 365.25-day year for month arithmetic."""
    from datetime import timedelta

    return a_date + timedelta(days=days)


# ---------------------------------------------------------------------------
# Subcommand: inventory
# ---------------------------------------------------------------------------


def cmd_inventory(args: argparse.Namespace) -> int:
    """Build a normalized, validated move-in/move-out inventory."""
    items = [parse_inventory_item(spec) for spec in args.item]
    if not items:
        fail("provide at least one --item 'room,item,grade0-5[,note]'")
    inv_date = parse_iso_date(args.date, "--date")
    label = args.label.strip() or "unlabeled"

    rooms: Dict[str, int] = {}
    grade_min, grade_max = 99, -1
    for entry in items:
        rooms[entry["room"]] = rooms.get(entry["room"], 0) + 1
        grade_min = min(grade_min, entry["grade"])
        grade_max = max(grade_max, entry["grade"])

    payload = {
        "label": label,
        "date": inv_date.isoformat(),
        "item_count": len(items),
        "room_count": len(rooms),
        "rooms": rooms,
        "grade_range": [
            grade_min if grade_min != 99 else None,
            grade_max if grade_max != -1 else None,
        ],
        "items": items,
    }

    if args.json:
        print_json(payload)
        return 0

    print(f"Condition inventory — {label} ({inv_date.isoformat()})")
    print(f"  items: {len(items)}  rooms: {len(rooms)}")
    for entry in items:
        note = f" — {entry['note']}" if entry["note"] else ""
        print(
            f"  [{entry['grade']}] {entry['room']} / {entry['item']}"
            f" ({GRADE_LABELS[entry['grade']]}){note}"
        )
    print("\nSave with: ... inventory ... --json > inventory.json")
    return 0


# ---------------------------------------------------------------------------
# Subcommand: diff
# ---------------------------------------------------------------------------


def cmd_diff(args: argparse.Namespace) -> int:
    """Diff two inventories and classify every change as wear/damage/etc."""
    # Load move-in side.
    if args.move_in:
        move_in = load_inventory(args.move_in, "--move-in")
        in_items = move_in["items"]
        in_date = move_in.get("date")
    elif args.in_item:
        in_items = [parse_inventory_item(spec) for spec in args.in_item]
        in_date = None
        move_in = None
    else:
        fail("diff needs --move-in FILE or repeated --in-item specs")

    # Load move-out side.
    if args.move_out:
        move_out = load_inventory(args.move_out, "--move-out")
        out_items = move_out["items"]
        out_date = move_out.get("date")
    elif args.out_item:
        out_items = [parse_inventory_item(spec) for spec in args.out_item]
        out_date = None
        move_out = None
    else:
        fail("diff needs --move-out FILE or repeated --out-item specs")

    # Tenancy length (for the fully-depreciated rule).
    tenancy_years: Optional[float] = None
    if args.tenancy_start and args.tenancy_end:
        tenancy_years = years_between(
            parse_iso_date(args.tenancy_start, "--tenancy-start"),
            parse_iso_date(args.tenancy_end, "--tenancy-end"),
        )
    elif in_date and out_date:
        tenancy_years = years_between(
            parse_iso_date(in_date, "move-in date"),
            parse_iso_date(out_date, "move-out date"),
        )

    in_index = items_by_key(in_items)
    out_index = items_by_key(out_items)
    all_keys = list(dict.fromkeys(list(in_index.keys()) + list(out_index.keys())))

    results: List[Dict[str, Any]] = []
    for key in all_keys:
        entry_in = in_index.get(key)
        entry_out = out_index.get(key)
        room, item = (entry_out or entry_in)["room"], (entry_out or entry_in)["item"]

        if entry_in is None:
            results.append(
                {
                    "room": room,
                    "item": item,
                    "grade_in": None,
                    "grade_out": entry_out["grade"],
                    "delta": None,
                    "direction": "no-move-in-baseline",
                    "classification": "unverifiable",
                    "basis": "item not recorded at move-in — demand is unprovable without a baseline",
                    "disputable": True,
                    "age_years": None,
                    "useful_life_years": None,
                }
            )
            continue
        if entry_out is None:
            results.append(
                {
                    "room": room,
                    "item": item,
                    "grade_in": entry_in["grade"],
                    "grade_out": None,
                    "delta": None,
                    "direction": "missing-at-move-out",
                    "classification": "damage",
                    "basis": "recorded at move-in but absent at move-out (missing/removed)",
                    "disputable": False,
                    "age_years": tenancy_years,
                    "useful_life_years": lookup_useful_life(item),
                }
            )
            continue

        note = entry_out.get("note", "") or entry_in.get("note", "")
        life = lookup_useful_life(item)
        verdict = classify_change(
            grade_in=entry_in["grade"],
            grade_out=entry_out["grade"],
            age_years=tenancy_years,
            useful_life_years=life,
            note=note,
        )
        verdict.update(
            {
                "room": room,
                "item": item,
                "grade_in": entry_in["grade"],
                "grade_out": entry_out["grade"],
                "age_years": tenancy_years,
                "useful_life_years": life,
            }
        )
        results.append(verdict)

    counts = {"wear": 0, "damage": 0, "improvement": 0, "unchanged": 0, "unverifiable": 0}
    for row in results:
        counts[row["classification"]] = counts.get(row["classification"], 0) + 1
    summary = {
        "tenancy_years": tenancy_years,
        "items_compared": len(results),
        **counts,
        "degraded": counts["wear"] + counts["damage"],
        "disputable_count": sum(1 for r in results if r["disputable"]),
    }

    if args.json:
        print_json({"summary": summary, "items": results})
        return 0

    print(f"Inventory diff — {summary['items_compared']} items compared")
    if tenancy_years is not None:
        print(f"  tenancy: {tenancy_years:.1f} years")
    print(
        f"  wear: {counts['wear']}  damage: {counts['damage']}  "
        f"improvements: {counts['improvement']}  unchanged: {counts['unchanged']}  "
        f"unverifiable: {counts['unverifiable']}"
    )
    print(f"  disputable items: {summary['disputable_count']}\n")
    for row in results:
        flag = " ⚑ disputable" if row["disputable"] else ""
        gi = "-" if row["grade_in"] is None else row["grade_in"]
        go = "-" if row["grade_out"] is None else row["grade_out"]
        print(
            f"  {row['room']} / {row['item']}: grade {gi}→{go}  "
            f"{row['classification'].upper()}{flag}"
        )
        print(f"      {row['basis']}")
    return 0


# ---------------------------------------------------------------------------
# Subcommand: prorate
# ---------------------------------------------------------------------------


def cmd_prorate(args: argparse.Namespace) -> int:
    """Prorate demanded deductions against remaining useful life."""
    items = [parse_prorate_item(spec, args.depreciated) for spec in args.item]
    if not items:
        fail("provide at least one --item 'name,value,useful_life_years[,...]'")

    tenancy_years: Optional[float] = None
    if not args.depreciated:
        if args.tenancy_years is None:
            fail("prorate needs --tenancy-years N (or --depreciated with explicit ages)")
        if args.tenancy_years < 0:
            fail("--tenancy-years must be >= 0")
        tenancy_years = float(args.tenancy_years)

    rows: List[Dict[str, Any]] = []
    total_demanded = total_legit = 0.0
    for entry in items:
        age = entry["age_years"] if args.depreciated else tenancy_years
        legit = prorate_value(entry["value"], age, entry["useful_life_years"])
        fraction_remaining = max(0.0, 1.0 - age / entry["useful_life_years"])
        savings = round2(entry["demanded"] - legit)
        row = {
            "item": entry["item"],
            "value": round2(entry["value"]),
            "useful_life_years": entry["useful_life_years"],
            "years_used": round(age, 4),
            "fraction_remaining": round(fraction_remaining, 4),
            "demanded": round2(entry["demanded"]),
            "max_legitimate_deduction": legit,
            "tenant_savings_if_demanded_full": savings,
            "fully_depreciated": fraction_remaining <= 0.0,
            "over_demand": savings > 0.005,
        }
        rows.append(row)
        total_demanded += entry["demanded"]
        total_legit += legit

    totals = {
        "demanded_total": round2(total_demanded),
        "max_legitimate_total": round2(total_legit),
        "tenant_savings_total": round2(total_demanded - total_legit),
    }

    if args.json:
        print_json(
            {
                "mode": "depreciated" if args.depreciated else "tenancy",
                "tenancy_years": tenancy_years,
                "items": rows,
                "totals": totals,
            }
        )
        return 0

    print(
        f"Proration — {'pre-aged items' if args.depreciated else f'{tenancy_years:g}-year tenancy'}"
    )
    print(f"  legit deduction = value × max(0, 1 − years_used / useful_life)\n")
    for row in rows:
        marker = "  [FULLY DEPRECIATED → 0]" if row["fully_depreciated"] else ""
        over = "  ← OVER-DEMAND" if row["over_demand"] else ""
        print(
            f"  {row['item']}: value {money(row['value'])}, life {row['useful_life_years']:g}y, "
            f"used {row['years_used']:g}y ({row['fraction_remaining']*100:.0f}% life left)"
        )
        print(
            f"      demanded {money(row['demanded'])} → legit {money(row['max_legitimate_deduction'])}"
            f"{marker}{over}"
        )
    print(
        f"\n  TOTALS: demanded {money(totals['demanded_total'])} | "
        f"max legitimate {money(totals['max_legitimate_total'])} | "
        f"tenant saves {money(totals['tenant_savings_total'])}"
    )
    return 0


# ---------------------------------------------------------------------------
# Subcommand: jurisdictions
# ---------------------------------------------------------------------------


def cmd_jurisdictions(args: argparse.Namespace) -> int:
    """Print the built-in jurisdiction deadline table."""
    if args.json:
        print_json(
            {
                "note": "Typical values — verify current local law before relying on them.",
                "jurisdictions": JURISDICTIONS,
            }
        )
        return 0
    print("Deposit-return deadlines by jurisdiction (TYPICAL — verify current local law)\n")
    print(f"{'CODE':<7} {'JURISDICTION':<28} {'DEADLINE':<18} REQUIREMENT")
    print("-" * 100)
    for code in sorted(JURISDICTIONS):
        entry = JURISDICTIONS[code]
        print(
            f"{code:<7} {entry['name']:<28} {deadline_description(entry) + ':':<18} "
            f"{entry['requirement']} [{entry['citation']}]"
        )
    print("\nUS states also accept their 2-letter code (e.g. CA, TX); 'UK' is an alias for GB.")
    return 0


# ---------------------------------------------------------------------------
# Subcommand: letter
# ---------------------------------------------------------------------------


def cmd_letter(args: argparse.Namespace) -> int:
    """Generate a full markdown demand letter for disputed deductions."""
    move_in = load_inventory(args.move_in, "--move-in")
    move_out = load_inventory(args.move_out, "--move-out")
    code = normalize_jurisdiction(args.jurisdiction)
    jur = JURISDICTIONS[code]

    try:
        with open(args.deductions, "r", encoding="utf-8") as handle:
            deductions = json.load(handle)
    except FileNotFoundError:
        fail(f"--deductions: file not found: {args.deductions}")
    except json.JSONDecodeError as exc:
        fail(f"--deductions: {args.deductions} is not valid JSON: {exc}")
    if not isinstance(deductions, list) or not deductions:
        fail("--deductions must be a JSON list of {item, amount, reason} objects")
    for d in deductions:
        if "item" not in d or "amount" not in d:
            fail("--deductions entries need at least 'item' and 'amount'")
        d.setdefault("reason", "")
        d["amount"] = float(d["amount"])

    # Timeline.
    in_date = parse_iso_date(move_in.get("date", date.today().isoformat()), "--move-in")
    out_date = parse_iso_date(move_out.get("date", date.today().isoformat()), "--move-out")
    if args.tenancy_start:
        in_date = parse_iso_date(args.tenancy_start, "--tenancy-start")
    if args.tenancy_end:
        out_date = parse_iso_date(args.tenancy_end, "--tenancy-end")
    tenancy_years = years_between(in_date, out_date)

    # Grade cross-reference from the inventories.
    in_index = items_by_key(move_in["items"])
    out_index = items_by_key(move_out["items"])

    today = date.today()
    if jur["days"] is not None:
        response_deadline = add_days(out_date, jur["days"])
        deadline_line = (
            f"{jur['days']} days after the end of tenancy "
            f"({jur['citation']}) — i.e. by {response_deadline.isoformat()}"
        )
    elif jur["window"] is not None:
        lo, hi = jur["window"]
        response_deadline = add_days(out_date, lo)
        deadline_line = (
            f"{lo}-{hi} days after the end of tenancy ({jur['citation']}) — "
            f"no later than {add_days(out_date, hi).isoformat()}"
        )
    else:
        response_deadline = add_days(out_date, 30)
        deadline_line = jur["requirement"] + f" [{jur['citation']}]"

    # Rebuttal analysis per deduction.
    analysis_rows: List[Dict[str, Any]] = []
    for d in deductions:
        name = str(d["item"])
        amount = round2(d["amount"])
        reason = str(d.get("reason", ""))
        key = None
        for candidate in out_index:
            if candidate[1] == name.lower() or name.lower() in candidate[1]:
                key = candidate
                break
        grade_in = grade_out = None
        note = reason
        if key and key in in_index:
            grade_in = in_index[key]["grade"]
        if key:
            grade_out = out_index[key]["grade"]
            note = out_index[key].get("note", "") or reason

        verdict = classify_change(
            grade_in=grade_in if grade_in is not None else 2,
            grade_out=grade_out if grade_out is not None else 3,
            age_years=tenancy_years,
            useful_life_years=lookup_useful_life(name),
            note=f"{name} {reason} {note}",
        )
        life = lookup_useful_life(name)

        if verdict["classification"] == "wear":
            legit = 0.0
            position = (
                "Ordinary wear-and-tear — not lawfully chargeable against the deposit."
            )
        elif verdict["classification"] == "improvement":
            legit = 0.0
            position = "Condition matches or exceeds move-in state — nothing owed."
        else:  # damage / unverifiable / unchanged-with-charge
            if life is not None:
                legit = prorate_value(amount, tenancy_years, life)
                position = (
                    f"Even if chargeable, the {name} had a typical useful life of "
                    f"{life} years and was {tenancy_years:.1f} years old at move-out; "
                    f"betterment-corrected maximum is {money(legit)} "
                    f"({money(amount)} × {max(0.0, 1 - tenancy_years / life):.2f})."
                )
            else:
                legit = amount
                position = (
                    "No known useful-life convention for this item; demand accepted "
                    "at face value pending receipts — reasonable cost must still be proven."
                )

        analysis_rows.append(
            {
                "item": name,
                "demanded": amount,
                "reason": reason,
                "classification": verdict["classification"],
                "basis": verdict["basis"],
                "useful_life_years": life,
                "max_legitimate": legit,
                "position": position,
                "over_demand": round2(amount - legit) > 0.005,
            }
        )

    demanded_total = round2(sum(r["demanded"] for r in analysis_rows))
    fair_total = round2(sum(r["max_legitimate"] for r in analysis_rows))
    refund_due = round2(args.deposit - fair_total)
    savings = round2(demanded_total - fair_total)

    analysis = {
        "jurisdiction": code,
        "jurisdiction_name": jur["name"],
        "deadline_line": deadline_line,
        "tenancy_years": tenancy_years,
        "deposit": round2(args.deposit),
        "demanded_total": demanded_total,
        "max_legitimate_total": fair_total,
        "refund_due": refund_due,
        "over_demand_savings": savings,
        "items": analysis_rows,
    }

    # ----- Markdown letter -------------------------------------------------
    lines: List[str] = []
    lines.append(f"# Demand for Return of Security Deposit\n")
    lines.append(f"**Date:** {today.isoformat()}\n")
    lines.append(f"**From:** {args.tenant} (tenant)  ")
    lines.append(f"**To:** {args.landlord} (landlord/agent)\n")
    lines.append(f"**Re:** Security deposit of {money(args.deposit)} — itemized dispute "
                 f"and demand for refund of {money(max(refund_due, 0.0))}\n")
    lines.append("---\n")

    lines.append("## 1. Timeline\n")
    lines.append(f"- **{in_date.isoformat()}** — move-in condition inventory recorded "
                 f"({move_in.get('label', 'move-in')}, {move_in.get('item_count', '?')} items).")
    lines.append(f"- **{out_date.isoformat()}** — move-out condition inventory recorded "
                 f"({move_out.get('label', 'move-out')}, {move_out.get('item_count', '?')} items); "
                 "keys returned.")
    lines.append(f"- Tenancy length: **{tenancy_years:.1f} years**.")
    lines.append(f"- Statutory deadline in {jur['name']}: **{deadline_line}**.\n")

    lines.append("## 2. Deductions demanded vs. amounts lawfully owed\n")
    lines.append("| # | Item | Landlord demanded | Classification | Max legitimate (prorated) |")
    lines.append("|---|------|------------------:|----------------|--------------------------:|")
    for i, row in enumerate(analysis_rows, 1):
        lines.append(
            f"| {i} | {row['item']} | {money(row['demanded'])} | "
            f"{row['classification']} | {money(row['max_legitimate'])} |"
        )
    lines.append(
        f"| | **TOTAL** | **{money(demanded_total)}** | | **{money(fair_total)}** |\n"
    )
    lines.append(f"Deductions exceed the lawful maximum by **{money(savings)}**.\n")

    lines.append("## 3. Itemized rebuttal\n")
    for i, row in enumerate(analysis_rows, 1):
        lines.append(f"**{i}. {row['item']} — demanded {money(row['demanded'])}**\n")
        lines.append(f"*Stated reason:* {row['reason'] or '(none provided)'}\n")
        lines.append(f"{row['position']}\n")
        if row["over_demand"]:
            lines.append(
                f"The difference of {money(round2(row['demanded'] - row['max_legitimate']))} "
                "is contested in full.\n"
            )

    lines.append("## 4. Documents requested\n")
    lines.append("Within the statutory period, please provide:")
    lines.append("1. An **itemized statement** of every deduction, as required by "
                 f"{jur['citation']};")
    lines.append("2. **Invoices/receipts** proving actual, reasonable costs "
                 "(not estimates) for each item charged;")
    lines.append("3. **Proof of age/installation date** (invoice or work order) for every "
                 "replaced item, so remaining useful life can be verified;\n")

    lines.append("## 5. Resolution demanded\n")
    lines.append(f"Refund of **{money(max(refund_due, 0.0))}** "
                 f"(deposit {money(args.deposit)} minus the prorated, documented maximum of "
                 f"{money(fair_total)}) within the statutory period.\n")
    if jur["days"] is not None:
        lines.append(f"Please pay by **{response_deadline.isoformat()}** "
                     f"({jur['days']} days after move-out, {jur['citation']}).\n")
    else:
        lines.append(f"Please pay promptly; statutory reference: {jur['citation']}.\n")

    lines.append("## 6. Escalation notice\n")
    lines.append(
        "If the deposit (or a lawfully itemized balance) is not returned within the "
        "deadline above, I will file in **small-claims court** without further notice, "
        "where penalties for bad-faith withholding (which in several jurisdictions "
        "include multiples of the deposit) may be sought, and report the withholding to "
        "the local tenancy authority.\n"
    )
    lines.append("This letter is a factual dispute summary; it is a good-faith attempt "
                 "to resolve this matter before court.\n")
    lines.append("---\n")
    lines.append(f"Signed,\n\n{args.tenant}\n")
    letter_md = "\n".join(lines)

    if args.json:
        print_json({"analysis": analysis, "letter_markdown": letter_md})
        return 0
    print(letter_md)
    return 0


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="deposit_defender",
        description=(
            "Security deposit protection: condition inventories, wear-vs-damage "
            "classification, useful-life proration, jurisdiction deadlines, "
            "and dispute letters. Decision support, not legal advice."
        ),
    )
    parser.add_argument(
        "--version", action="version", version="landlord-deposit-defender 1.0.0"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # inventory
    p = sub.add_parser("inventory", help="build a normalized condition inventory")
    p.add_argument(
        "--item", action="append", default=[], metavar="'room,item,grade0-5[,note]'",
        help="repeatable; note may contain commas",
    )
    p.add_argument("--label", default="unlabeled", help="'move-in' or 'move-out'")
    p.add_argument("--date", default=date.today().isoformat(), help="YYYY-MM-DD")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.set_defaults(func=cmd_inventory)

    # diff
    p = sub.add_parser("diff", help="compare move-in vs move-out inventories")
    p.add_argument("--move-in", help="move-in inventory JSON file")
    p.add_argument("--move-out", help="move-out inventory JSON file")
    p.add_argument("--in-item", action="append", default=[],
                   metavar="'room,item,grade,note'", help="inline move-in item")
    p.add_argument("--out-item", action="append", default=[],
                   metavar="'room,item,grade,note'", help="inline move-out item")
    p.add_argument("--tenancy-start", help="YYYY-MM-DD (age rule)")
    p.add_argument("--tenancy-end", help="YYYY-MM-DD (age rule)")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.set_defaults(func=cmd_diff)

    # prorate
    p = sub.add_parser("prorate", help="prorate a deduction by remaining useful life")
    p.add_argument(
        "--item", action="append", default=[],
        metavar="'name,value,useful_life_years[,demanded|age]'",
        help="repeatable",
    )
    p.add_argument("--tenancy-years", type=float,
                   help="years item was used (default: item new at move-in)")
    p.add_argument(
        "--depreciated", action="store_true",
        help="inputs are already aged: 'name,value,life,age_years'",
    )
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.set_defaults(func=cmd_prorate)

    # letter
    p = sub.add_parser("letter", help="generate a markdown dispute/demand letter")
    p.add_argument("--move-in", required=True, help="move-in inventory JSON")
    p.add_argument("--move-out", required=True, help="move-out inventory JSON")
    p.add_argument("--deposit", type=float, required=True, help="deposit amount")
    p.add_argument("--deductions", required=True,
                   help="JSON list of {item, amount, reason}")
    p.add_argument("--jurisdiction", required=True,
                   help="e.g. CA, US-TX, UK, DE, AU-NSW (see `jurisdictions`)")
    p.add_argument("--tenant", default="Tenant", help="tenant name")
    p.add_argument("--landlord", default="Landlord", help="landlord name")
    p.add_argument("--tenancy-start", help="override move-in date")
    p.add_argument("--tenancy-end", help="override move-out date")
    p.add_argument("--json", action="store_true",
                   help="structured letter data + markdown")
    p.set_defaults(func=cmd_letter)

    # jurisdictions
    p = sub.add_parser("jurisdictions", help="list deposit-return deadlines")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.set_defaults(func=cmd_jurisdictions)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
