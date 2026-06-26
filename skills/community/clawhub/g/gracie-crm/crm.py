#!/usr/bin/env python3
"""
Gracie CRM - Lightweight CLI for tracking Gracie AI Receptionist sales leads.
Usage: python3 crm.py <command> [options]
"""

import json
import os
import re
import sys
import argparse
from datetime import date, datetime

# ── Paths ──────────────────────────────────────────────────────────────────────
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
CRM_FILE = os.path.join(SKILL_DIR, "crm.json")
MASTER_LEADS = os.path.expanduser(
    "~/StudioBrain/30_INTERNAL/WLC-Services/LEADS/MASTER_LEAD_LIST.md"
)

# ── Colors ─────────────────────────────────────────────────────────────────────
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    RED    = "\033[91m"
    YELLOW = "\033[93m"
    GREEN  = "\033[92m"
    CYAN   = "\033[96m"
    BLUE   = "\033[94m"
    MAGENTA= "\033[95m"
    WHITE  = "\033[97m"

def no_color():
    for attr in vars(C):
        if not attr.startswith("_"):
            setattr(C, attr, "")

if not sys.stdout.isatty():
    no_color()

# ── Hot leads to pre-populate on first import ──────────────────────────────────
HOT_LEADS = [
    {"name": "Victory Auto Repair",                "phone": "718-698-9896", "category": "auto"},
    {"name": "P.A.C. Plumbing",                    "phone": "718-720-4980", "category": "hvac"},
    {"name": "Christine Relyea State Farm",         "phone": "718-698-5803", "category": "insurance"},
    {"name": "Community II HVAC",                   "phone": "347-212-1513", "category": "hvac"},
    {"name": "HI TECH HVAC SERVICES CORP",          "phone": "",             "category": "hvac"},
    {"name": "Sola Dental Spa",                     "phone": "718-948-3777", "category": "dental"},
    {"name": "Dr. Mariana Savel DDS",               "phone": "718-494-2200", "category": "dental"},
    {"name": "Family & Cosmetic Dentistry of SI",   "phone": "718-477-5588", "category": "dental"},
]

# ── Data I/O ───────────────────────────────────────────────────────────────────
def load():
    if not os.path.exists(CRM_FILE):
        return []
    with open(CRM_FILE) as f:
        return json.load(f)

def save(leads):
    with open(CRM_FILE, "w") as f:
        json.dump(leads, f, indent=2)

def next_id(leads):
    return max((l["id"] for l in leads), default=0) + 1

def get_lead(leads, lead_id):
    for l in leads:
        if l["id"] == lead_id:
            return l
    return None

def today_str():
    return date.today().isoformat()

def make_lead(lead_id, name, phone, category):
    return {
        "id": lead_id,
        "name": name,
        "phone": phone or "",
        "category": category or "other",
        "status": "new",
        "calls": [],
        "notes": [],
        "followup_date": None,
        "added": today_str(),
    }

# ── Status display ─────────────────────────────────────────────────────────────
STATUS_COLOR = {
    "new":         C.WHITE,
    "called":      C.BLUE,
    "no_answer":   C.DIM,
    "interested":  C.YELLOW,
    "demo_sent":   C.MAGENTA,
    "closed_won":  C.GREEN,
    "closed_lost": C.RED,
}

STATUS_LABEL = {
    "new":         "NEW",
    "called":      "CALLED",
    "no_answer":   "NO ANSWER",
    "interested":  "INTERESTED",
    "demo_sent":   "DEMO SENT",
    "closed_won":  "WON ✓",
    "closed_lost": "LOST ✗",
}

CATEGORY_EMOJI = {
    "auto":      "🔧",
    "hvac":      "❄️ ",
    "dental":    "🦷",
    "insurance": "🛡️ ",
    "medical":   "🏥",
    "legal":     "⚖️ ",
    "other":     "📋",
}

def fmt_status(status):
    color = STATUS_COLOR.get(status, C.WHITE)
    label = STATUS_LABEL.get(status, status.upper())
    return f"{color}{label}{C.RESET}"

def fmt_followup(followup_date):
    if not followup_date:
        return f"{C.DIM}—{C.RESET}"
    today = date.today()
    due = date.fromisoformat(followup_date)
    if due < today:
        return f"{C.RED}⚠ {followup_date} (OVERDUE){C.RESET}"
    elif due == today:
        return f"{C.YELLOW}● {followup_date} (TODAY){C.RESET}"
    return followup_date

def cat_icon(category):
    return CATEGORY_EMOJI.get(category, "📋")

def print_lead(l, verbose=False):
    icon = cat_icon(l["category"])
    phone = l["phone"] if l["phone"] else "—"
    print(
        f"  {C.BOLD}#{l['id']}{C.RESET}  {icon} {C.BOLD}{l['name']}{C.RESET}"
        f"  {C.DIM}{phone}{C.RESET}"
    )
    print(
        f"       Status: {fmt_status(l['status'])}"
        f"  |  Follow-up: {fmt_followup(l['followup_date'])}"
        f"  |  Category: {l['category']}"
    )
    if verbose:
        if l["calls"]:
            print(f"       {C.CYAN}Calls:{C.RESET}")
            for c in l["calls"]:
                note = f" — {c['notes']}" if c.get("notes") else ""
                print(f"         {c['date']}  {c['outcome']}{note}")
        if l["notes"]:
            print(f"       {C.CYAN}Notes:{C.RESET}")
            for n in l["notes"]:
                print(f"         • {n}")

def sort_key(l):
    fd = l.get("followup_date") or "9999-99-99"
    return fd

# ── Commands ───────────────────────────────────────────────────────────────────

def cmd_list(args):
    leads = load()
    if not leads:
        print(f"{C.DIM}No leads yet. Run: python3 crm.py import{C.RESET}")
        return
    leads_sorted = sorted(leads, key=sort_key)
    print(f"\n{C.BOLD}{C.CYAN}━━━ Gracie CRM — All Leads ({len(leads)}) ━━━{C.RESET}\n")
    for l in leads_sorted:
        print_lead(l, verbose=getattr(args, "verbose", False))
        print()


def cmd_add(args):
    leads = load()
    # Check for duplicate name
    for l in leads:
        if l["name"].lower() == args.name.lower():
            print(f"{C.YELLOW}Lead '{args.name}' already exists (#{l['id']}).{C.RESET}")
            return
    lead = make_lead(next_id(leads), args.name, args.phone or "", args.category or "other")
    leads.append(lead)
    save(leads)
    print(f"{C.GREEN}✓ Added:{C.RESET} {lead['name']} (#{lead['id']}) — {lead['category']}")


def cmd_call(args):
    leads = load()
    lead = get_lead(leads, args.id)
    if not lead:
        print(f"{C.RED}Lead #{args.id} not found.{C.RESET}")
        return

    outcome = args.outcome.lower().replace(" ", "_")
    # Map outcome → status
    outcome_to_status = {
        "no_answer":  "no_answer",
        "no answer":  "no_answer",
        "interested": "interested",
        "demo_sent":  "demo_sent",
        "demo sent":  "demo_sent",
        "closed_won": "closed_won",
        "won":        "closed_won",
        "closed_lost":"closed_lost",
        "lost":       "closed_lost",
    }
    new_status = outcome_to_status.get(outcome, "called")

    call_record = {
        "date":    today_str(),
        "outcome": args.outcome,
        "notes":   args.notes or "",
    }
    lead["calls"].append(call_record)
    lead["status"] = new_status
    if args.followup:
        lead["followup_date"] = args.followup

    save(leads)
    print(
        f"{C.GREEN}✓ Call logged:{C.RESET} #{lead['id']} {lead['name']}\n"
        f"  Outcome: {args.outcome}  |  Status → {fmt_status(new_status)}"
        + (f"\n  Follow-up: {args.followup}" if args.followup else "")
    )


def cmd_note(args):
    leads = load()
    lead = get_lead(leads, args.id)
    if not lead:
        print(f"{C.RED}Lead #{args.id} not found.{C.RESET}")
        return
    lead["notes"].append(args.text)
    save(leads)
    print(f"{C.GREEN}✓ Note added to #{lead['id']} {lead['name']}{C.RESET}")
    print(f"  → {args.text}")


def cmd_today(args):
    leads = load()
    today = date.today()
    due = [
        l for l in leads
        if l.get("followup_date") and date.fromisoformat(l["followup_date"]) <= today
        and l["status"] not in ("closed_won", "closed_lost")
    ]
    if not due:
        print(f"{C.GREEN}✓ No follow-ups due today.{C.RESET}")
        return
    due_sorted = sorted(due, key=sort_key)
    print(f"\n{C.BOLD}{C.YELLOW}━━━ Due Today / Overdue ({len(due)}) ━━━{C.RESET}\n")
    for l in due_sorted:
        print_lead(l)
        print()


def cmd_pipeline(args):
    leads = load()
    total = len(leads)
    counts = {
        "new":         0,
        "called":      0,
        "no_answer":   0,
        "interested":  0,
        "demo_sent":   0,
        "closed_won":  0,
        "closed_lost": 0,
    }
    for l in leads:
        s = l.get("status", "new")
        counts[s] = counts.get(s, 0) + 1

    print(f"\n{C.BOLD}{C.CYAN}━━━ Gracie Pipeline Summary ━━━{C.RESET}\n")
    print(f"  {C.BOLD}Total Leads:{C.RESET}    {total}")
    print()
    rows = [
        ("new",         "🆕 New"),
        ("called",      "📞 Called"),
        ("no_answer",   "📵 No Answer"),
        ("interested",  "💛 Interested"),
        ("demo_sent",   "📤 Demo Sent"),
        ("closed_won",  "✅ Won"),
        ("closed_lost", "❌ Lost"),
    ]
    for status, label in rows:
        n = counts.get(status, 0)
        bar = "█" * n + "░" * max(0, 10 - n)
        color = STATUS_COLOR.get(status, C.WHITE)
        print(f"  {label:<22} {color}{n:>3}{C.RESET}  {C.DIM}{bar}{C.RESET}")
    print()

    active = total - counts["closed_won"] - counts["closed_lost"]
    print(f"  {C.BOLD}Active pipeline:{C.RESET}  {active}")
    print(f"  {C.GREEN}{C.BOLD}Closed Won:{C.RESET}       {counts['closed_won']}")
    print(f"  {C.RED}Closed Lost:{C.RESET}      {counts['closed_lost']}")
    print()


def _detect_category_from_section(section_header):
    """Guess category from section header text."""
    h = section_header.lower()
    if "auto" in h or "car" in h or "tire" in h:
        return "auto"
    if "hvac" in h or "plumb" in h or "heat" in h or "cool" in h:
        return "hvac"
    if "dental" in h or "dds" in h or "dentist" in h:
        return "dental"
    if "insur" in h:
        return "insurance"
    if "medical" in h or "health" in h or "doctor" in h:
        return "medical"
    if "legal" in h or "law" in h or "attorney" in h:
        return "legal"
    if "spa" in h or "salon" in h or "beauty" in h:
        return "beauty"
    if "real estate" in h or "realtor" in h:
        return "realestate"
    return "other"

def _clean_name(raw):
    """Strip markdown bold (**text**) and leading #/numbers."""
    raw = re.sub(r"\*\*(.+?)\*\*", r"\1", raw)
    raw = re.sub(r"^\s*\d+\s*", "", raw)
    return raw.strip()

def _clean_phone(raw):
    """Return digits-only phone string or empty."""
    if not raw:
        return ""
    raw = raw.strip()
    digits = re.sub(r"\D", "", raw)
    if len(digits) >= 7:
        # Return formatted (original cleaned)
        return re.sub(r"[^\d\-\(\)\s]", "", raw).strip()
    return ""

PHONE_RE = re.compile(r"\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}")
SKIP_NAMES = {
    "#", "business", "name", "lead", "company", "phone", "address",
    "notes", "category", "---", "", "email", "status", "total",
    "leads", "hot / pre-qualified", "auto repair", "hvac / plumbing",
    "dental", "other", "chiro", "wellness", "trucking", "e-commerce",
    "category", "est. mrr (25% close)", "real estate",
}
# Also skip rows where the first meaningful col looks like a category label
# (no bold, short, single word like "Auto Repair")
SKIP_IF_NO_BOLD_AND_SHORT = 20  # chars

def _parse_master_leads(filepath):
    """
    Parse MASTER_LEAD_LIST.md.
    Returns list of dicts: {name, phone, category}
    Strategy: track current section header for category,
    then parse table rows. A valid lead row has:
    - a bold **Business Name** OR a name that isn't a header/skip word
    - optionally a phone number column
    """
    results = []
    seen = set()
    current_category = "other"

    with open(filepath) as f:
        lines = f.readlines()

    for line in lines:
        stripped = line.strip()

        # Detect section headers (## or ###)
        if stripped.startswith("#"):
            current_category = _detect_category_from_section(stripped)
            continue

        # Skip separator rows
        if re.match(r"^\|[\s\-\|]+\|$", stripped):
            continue

        # Only process table rows
        if not stripped.startswith("|"):
            continue

        cols = [c.strip() for c in stripped.split("|")]
        cols = [c for c in cols if c]  # remove empties from leading/trailing |

        if len(cols) < 2:
            continue

        # Find name: first col with bold **text** or a plausible business name
        name = ""
        phone = ""
        for i, col in enumerate(cols):
            if "**" in col:
                name = _clean_name(col)
                break

        if not name:
            # No bold — skip this row entirely (summary/header row)
            continue

        if not name or name.lower() in SKIP_NAMES or re.match(r"^\d[\d,]+$", name):
            continue

        # Find phone: any col matching phone pattern
        for col in cols:
            m = PHONE_RE.search(col)
            if m:
                phone = m.group(0).strip()
                break

        key = name.lower()
        if key not in seen:
            seen.add(key)
            results.append({"name": name, "phone": phone, "category": current_category})

    return results

def cmd_import(args):
    leads = load()
    existing_names = {l["name"].lower() for l in leads}
    added = 0

    # Always seed the HOT_LEADS list
    print(f"{C.CYAN}Seeding hot leads...{C.RESET}")
    for hl in HOT_LEADS:
        if hl["name"].lower() not in existing_names:
            lead = make_lead(next_id(leads), hl["name"], hl["phone"], hl["category"])
            leads.append(lead)
            existing_names.add(hl["name"].lower())
            added += 1
            print(f"  {C.GREEN}+{C.RESET} {hl['name']}")
        else:
            print(f"  {C.DIM}~ {hl['name']} (exists){C.RESET}")

    # Parse MASTER_LEAD_LIST.md if present
    if os.path.exists(MASTER_LEADS):
        print(f"\n{C.CYAN}Parsing {os.path.basename(MASTER_LEADS)}...{C.RESET}")
        parsed = _parse_master_leads(MASTER_LEADS)
        for p in parsed:
            if p["name"].lower() not in existing_names:
                lead = make_lead(next_id(leads), p["name"], p["phone"], p["category"])
                leads.append(lead)
                existing_names.add(p["name"].lower())
                added += 1
                print(f"  {C.GREEN}+{C.RESET} {p['name']}  {C.DIM}{p['phone']}{C.RESET}")
        print(f"  {C.DIM}({len(parsed)} leads found in file){C.RESET}")
    else:
        print(f"\n{C.DIM}(MASTER_LEAD_LIST.md not found — skipped){C.RESET}")

    save(leads)
    print(f"\n{C.BOLD}{C.GREEN}✓ Import complete. {added} new leads added. Total: {len(leads)}{C.RESET}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="crm.py",
        description="Gracie CRM — Lightweight sales lead tracker",
    )
    sub = parser.add_subparsers(dest="command", metavar="command")

    # list
    p_list = sub.add_parser("list", help="Show all leads")
    p_list.add_argument("-v", "--verbose", action="store_true", help="Show calls and notes")

    # add
    p_add = sub.add_parser("add", help="Add a new lead")
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--phone", default="")
    p_add.add_argument("--category", default="other")

    # call
    p_call = sub.add_parser("call", help="Log a call")
    p_call.add_argument("id", type=int)
    p_call.add_argument("--outcome", required=True, help="e.g. 'no answer', 'interested'")
    p_call.add_argument("--followup", help="Follow-up date YYYY-MM-DD")
    p_call.add_argument("--notes", default="", help="Optional call notes")

    # note
    p_note = sub.add_parser("note", help="Add a note to a lead")
    p_note.add_argument("id", type=int)
    p_note.add_argument("text")

    # today
    sub.add_parser("today", help="Show leads due today or overdue")

    # pipeline
    sub.add_parser("pipeline", help="Show pipeline summary")

    # import
    sub.add_parser("import", help="Import leads from MASTER_LEAD_LIST.md + hot leads")

    args = parser.parse_args()

    dispatch = {
        "list":     cmd_list,
        "add":      cmd_add,
        "call":     cmd_call,
        "note":     cmd_note,
        "today":    cmd_today,
        "pipeline": cmd_pipeline,
        "import":   cmd_import,
    }

    if args.command in dispatch:
        dispatch[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
