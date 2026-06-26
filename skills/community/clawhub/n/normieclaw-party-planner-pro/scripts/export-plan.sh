#!/usr/bin/env bash
# export-plan.sh — Export a party plan to a shareable markdown summary
# Usage: ./export-plan.sh <event-slug>
# Example: ./export-plan.sh sarah-30th-birthday
# Output: reports/party-plan-EVENT_SLUG.md

set -euo pipefail
umask 077

# --- Workspace root detection ---
find_skill_root() {
    # Stay within the skill directory — do not traverse outside
    cd "$(dirname "$0")/.." && pwd
}

SKILL_DIR="$(find_skill_root)"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="$SKILL_DIR/data"
REPORTS_DIR="$SKILL_DIR/reports"

# --- Args ---
if [ $# -lt 1 ]; then
    echo "Usage: $0 <event-slug>"
    echo "Example: $0 sarah-30th-birthday"
    echo ""
    echo "Available events:"
    if [ -d "$DATA_DIR/events" ]; then
        for f in "$DATA_DIR/events"/*.json; do
            [ -f "$f" ] || continue
            basename "$f" .json
        done
    else
        echo "  (none — no events directory found)"
    fi
    exit 1
fi

EVENT_SLUG="$1"

# --- Input validation (prevent path traversal) ---
if [[ ! "$EVENT_SLUG" =~ ^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}$ ]]; then
    echo "Error: Invalid event slug '$EVENT_SLUG'."
    echo "Slugs must be alphanumeric with hyphens/underscores/dots, 1-128 chars."
    exit 1
fi

EVENT_FILE="$DATA_DIR/events/$EVENT_SLUG.json"
EVENT_DIR="$DATA_DIR/events/$EVENT_SLUG"

if [ ! -f "$EVENT_FILE" ]; then
    echo "Error: Event '$EVENT_SLUG' not found."
    echo "Expected: $EVENT_FILE"
    exit 1
fi

mkdir -p "$REPORTS_DIR"
chmod 700 "$REPORTS_DIR"
OUTPUT_FILE="$REPORTS_DIR/party-plan-$EVENT_SLUG.md"

# --- Parse event data using python for reliable JSON handling ---
EVENT_FILE_ENV="$EVENT_FILE" \
EVENT_DIR_ENV="$EVENT_DIR" \
OUTPUT_FILE_ENV="$OUTPUT_FILE" \
python3 << 'PYEOF'
import json, os, sys
from datetime import datetime

event_file = os.environ["EVENT_FILE_ENV"]
event_dir = os.environ["EVENT_DIR_ENV"]
output_file = os.environ["OUTPUT_FILE_ENV"]

with open(event_file) as f:
    event = json.load(f)

lines = []
lines.append(f"# 🎉 {event.get('name', 'Party Plan')}")
lines.append(f"")
lines.append(f"**Type:** {event.get('type', 'N/A').replace('_', ' ').title()}")
lines.append(f"**Date:** {event.get('date', 'TBD')} at {event.get('time_start', 'TBD')} — {event.get('time_end', 'TBD')}")
lines.append(f"**Venue:** {event.get('venue_name', 'TBD')} ({event.get('venue_type', 'TBD').replace('_', ' ').title()})")
if event.get('venue_address'):
    lines.append(f"**Address:** {event['venue_address']}")
lines.append(f"**Theme:** {event.get('theme', 'TBD')}")
lines.append(f"**Formality:** {event.get('formality', 'casual').title()}")
lines.append(f"**Estimated Guests:** {event.get('guest_count_estimate', 'TBD')}")
lines.append(f"")

# Guest list
guests_file = os.path.join(event_dir, "guests.json")
if os.path.isfile(guests_file):
    with open(guests_file) as f:
        guests = json.load(f)
    confirmed = [g for g in guests if g.get("rsvp_status") == "confirmed"]
    declined = [g for g in guests if g.get("rsvp_status") == "declined"]
    pending = [g for g in guests if g.get("rsvp_status") in ("invited", "maybe", "no_response")]
    lines.append(f"---")
    lines.append(f"## 👥 Guest List ({len(guests)} total)")
    lines.append(f"- ✅ Confirmed: {len(confirmed)}")
    lines.append(f"- ❌ Declined: {len(declined)}")
    lines.append(f"- ⏳ Pending: {len(pending)}")
    lines.append(f"")
    dietary = {}
    for g in guests:
        for d in g.get("dietary", []):
            dietary[d] = dietary.get(d, 0) + 1
    if dietary:
        lines.append(f"**Dietary Restrictions:**")
        for d, count in sorted(dietary.items()):
            lines.append(f"- {d}: {count} guest(s)")
        lines.append(f"")

# Budget
budget_file = os.path.join(event_dir, "budget.json")
if os.path.isfile(budget_file):
    with open(budget_file) as f:
        budget = json.load(f)
    lines.append(f"---")
    lines.append(f"## 💰 Budget")
    lines.append(f"- **Total Budget:** \${budget.get('total_budget', 0):,.2f}")
    lines.append(f"- **Total Spent:** \${budget.get('total_spent', 0):,.2f}")
    lines.append(f"- **Remaining:** \${budget.get('total_remaining', 0):,.2f}")
    if budget.get('cost_per_head'):
        lines.append(f"- **Cost Per Head:** \${budget['cost_per_head']:,.2f}")
    lines.append(f"")
    for cat in budget.get("categories", []):
        spent = cat.get("spent", 0)
        allocated = cat.get("allocated", 0)
        pct = (spent / allocated * 100) if allocated > 0 else 0
        lines.append(f"- **{cat['name']}:** \${spent:,.2f} / \${allocated:,.2f} ({pct:.0f}%)")
    lines.append(f"")

# Menu
menu_file = os.path.join(event_dir, "menu.json")
if os.path.isfile(menu_file):
    with open(menu_file) as f:
        menu = json.load(f)
    lines.append(f"---")
    lines.append(f"## 🍽️ Menu ({menu.get('style', 'TBD').title()})")
    for course in menu.get("courses", []):
        lines.append(f"**{course['name']}:**")
        for item in course.get("items", []):
            tags = ", ".join(item.get("dietary_tags", []))
            tag_str = f" [{tags}]" if tags else ""
            lines.append(f"- {item['name']}{tag_str}")
        lines.append(f"")
    drinks = menu.get("drinks", {})
    if drinks:
        lines.append(f"**Drinks:**")
        if drinks.get("beer_units"): lines.append(f"- Beer: {drinks['beer_units']} units")
        if drinks.get("wine_bottles"): lines.append(f"- Wine: {drinks['wine_bottles']} bottles")
        if drinks.get("liquor_bottles"): lines.append(f"- Liquor: {drinks['liquor_bottles']} bottles")
        for na in drinks.get("non_alcoholic", []):
            lines.append(f"- {na}")
        lines.append(f"")

# Tasks / Timeline
tasks_file = os.path.join(event_dir, "tasks.json")
if os.path.isfile(tasks_file):
    with open(tasks_file) as f:
        tasks = json.load(f)
    done = [t for t in tasks if t.get("status") == "done"]
    remaining = [t for t in tasks if t.get("status") != "done"]
    lines.append(f"---")
    lines.append(f"## ✅ Planning Checklist ({len(done)}/{len(tasks)} complete)")
    for t in sorted(remaining, key=lambda x: x.get("due_date", "9999")):
        assignee = f" → {t['assigned_to']}" if t.get("assigned_to") else ""
        lines.append(f"- [ ] {t['description']} (due {t.get('due_date', 'TBD')}){assignee}")
    for t in sorted(done, key=lambda x: x.get("completed_at", "")):
        lines.append(f"- [x] {t['description']}")
    lines.append(f"")

# Vendors
vendors_file = os.path.join(event_dir, "vendors.json")
if os.path.isfile(vendors_file):
    with open(vendors_file) as f:
        vendors = json.load(f)
    if vendors:
        lines.append(f"---")
        lines.append(f"## 📋 Vendors")
        for v in vendors:
            status = v.get("booking_status", "researching").replace("_", " ").title()
            lines.append(f"- **{v['business_name']}** ({v.get('service_type', 'N/A').replace('_', ' ').title()}) — {status} — \${v.get('quote_amount', 0):,.2f}")
        lines.append(f"")

lines.append(f"---")
lines.append(f"*Exported by Party Planner Pro on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*")

with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ Party plan exported to: {output_file}")
PYEOF
