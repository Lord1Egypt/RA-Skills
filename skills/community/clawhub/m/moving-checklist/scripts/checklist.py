#!/usr/bin/env python3
"""
Moving Checklist Generator — generate personalized moving timeline, task lists,
budget estimates, and role assignments.

Usage:
  python checklist.py --profile '{"current":"整租","new":"上海浦东","date":"2025-07-15","distance":"同城","members":"solo","furniture":"部分自有"}'
  python checklist.py --interactive
  python checklist.py --help

MIT-0 License
"""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta

REF_DIR = os.path.join(os.path.dirname(__file__), "..", "references")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_reference(name):
    return load_json(os.path.join(REF_DIR, name))


# ── Step 1: Gather Moving Context ──────────────────────────────────────────

DEFAULT_PROFILE = {
    "current": "整租",
    "new_address": "",
    "move_date": "",
    "distance": "同城",
    "household_size": "solo",
    "household_members": [],
    "furniture": "房東提供",
    "special_items": [],
    "timeline_days": 30,
    "city_tier": "Tier 1",
}


def build_profile(raw):
    """Build structured moving profile from raw input.

    AI Prompt Template:
      Extract moving profile from user input: {input}.
      Fields: current residence type, new address, move date,
      distance (同城/跨城/跨国), household size, furniture ownership,
      special items. Return structured JSON.
    """
    profile = dict(DEFAULT_PROFILE)
    if isinstance(raw, str):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # Fallback: parse as key-value pairs
            data = {}
            for part in raw.replace("，", ",").split(","):
                part = part.strip()
                if "：" in part:
                    k, v = part.split("：", 1)
                    data[k.strip()] = v.strip()
                elif ":" in part:
                    k, v = part.split(":", 1)
                    data[k.strip()] = v.strip()
    else:
        data = raw

    profile.update(data)

    # Parse move date and calculate timeline
    move_date_str = profile.get("move_date", "")
    if move_date_str:
        try:
            move_date = datetime.strptime(move_date_str, "%Y-%m-%d")
            today = datetime.now()
            delta = (move_date - today).days
            profile["timeline_days"] = max(delta, 1)
        except (ValueError, TypeError):
            profile["timeline_days"] = 30

    # Infer city tier from address
    addr = profile.get("new_address", "")
    tier1_cities = ["上海", "北京", "深圳", "广州", "杭州"]
    tier2_cities = ["成都", "重庆", "武汉", "西安", "南京", "苏州", "天津"]
    if any(c in addr for c in tier1_cities):
        profile["city_tier"] = "Tier 1"
    elif any(c in addr for c in tier2_cities):
        profile["city_tier"] = "Tier 2"
    else:
        profile["city_tier"] = "Tier 3"

    return profile


# ── Step 2: Generate Countdown Timeline ─────────────────────────────────────

def generate_timeline(profile):
    """Generate countdown timeline from move date.

    AI Prompt Template:
      Generate a moving countdown timeline based on profile: {profile}.
      Periods: D-30~D-14 (Planning), D-14~D-7 (Preparation),
      D-7~D-3 (Packing), D-3~D-1 (Final Prep), D-Day (Move),
      D+1~D+7 (Settling). Adjust density based on timeline length.
      For urgent moves (<7 days), compress into fewer periods.
    """
    days = profile["timeline_days"]
    distance = profile["distance"]
    special_items = profile.get("special_items", [])
    is_urgent = days < 7
    is_intercity = distance in ("跨城", "跨国")

    periods = []

    if is_urgent:
        # Compressed mode
        periods = [
            {"period": f"D-{days}~D-4", "label": "Urgent Planning",
             "focus": "Prioritize critical tasks only",
             "tasks": [
                "Book movers immediately (call, don't message)",
                "Buy packing supplies (boxes, tape, bubble wrap)",
                "Notify landlord/property manager",
                "Arrange utilities transfer or cancellation",
                "Recruit friends or hire helpers",
             ]},
            {"period": "D-3~D-2", "label": "Intensive Packing",
             "focus": "Pack non-essentials room by room",
             "tasks": [
                "Pack off-season clothes and books first",
                "Label all boxes with room and contents",
                "Prepare essentials bag (3 days of clothes, toiletries)",
                "Confirm mover booking and timing",
             ]},
            {"period": "D-1", "label": "Final Prep",
             "focus": "Last-minute readiness",
             "tasks": [
                "Defrost refrigerator",
                "Pack toiletries and daily essentials separately",
                "Charge all devices, have cash ready",
                "Confirm elevator booking / parking permit",
             ]},
            {"period": "D-Day", "label": "Move Day",
             "focus": "Supervise loading, final walkthrough",
             "tasks": [
                "Supervise loading and inventory check",
                "Take photos of empty rooms for deposit claim",
                "Key handover and final walkthrough with landlord",
                "Clean move-out area if required",
             ]},
            {"period": "D+1~D+7", "label": "Settling",
             "focus": "Unpack essentials and register",
             "tasks": [
                "Unpack kitchen and bathroom essentials first",
                "Register at new community (居委会)",
                "Update address with bank, delivery apps, social security",
                "Test all appliances in new home",
             ]},
        ]
    else:
        # Standard timeline
        periods = [
            {"period": f"D-{min(days,30)}~D-14", "label": "Planning Phase",
             "focus": "Research, declutter, notify",
             "tasks": [
                "Research and compare 3+ moving companies (货拉拉, 快狗, traditional)",
                "Start decluttering: sell/donate/discard room by room",
                "Notify landlord of move-out date (check contract for notice period)",
                "Check deposit recovery requirements (repairs, deep clean)",
                "Request utilities: schedule water/electricity/gas transfer",
                "Order packing supplies: boxes, tape, bubble wrap, markers",
             ]},
            {"period": "D-14~D-7", "label": "Preparation Phase",
             "focus": "Book movers, pack non-essentials, change address",
             "tasks": [
                "Book movers and confirm date/time",
                "Book freight elevator if needed",
                "Start packing: off-season clothes, books, decorations",
                "Change address: bank, credit card, social security (社保)",
                "Update delivery app addresses (Meituan, Taobao, JD)",
                "Cancel/reschedule subscriptions (newspaper, milk delivery)",
                "If inter-city: arrange long-distance shipping, check customs",
             ]},
            {"period": "D-7~D-3", "label": "Packing Phase",
             "focus": "Pack room by room, label everything",
             "tasks": [
                "Pack room by room: bedroom -> living room -> kitchen -> bathroom",
                "Label every box: room name + contents summary + fragile flag",
                "Create box inventory spreadsheet",
                "Pack valuables separately: documents, jewelry, electronics (keep with you)",
                "Disassemble furniture: mark fittings per piece in labeled bags",
                "Defrost refrigerator (D-3)",
             ]},
            {"period": "D-3~D-1", "label": "Final Prep",
             "focus": "Essentials bag, confirm timing, clean",
             "tasks": [
                "Pack essentials bag: 3 days clothes, toiletries, meds, chargers",
                "Pack first-night box: sheets, towel, basic kitchen items",
                "Confirm mover arrival time, parking, elevators",
                "Take photos of current condition for deposit claim",
                "Prepare tips/cash for movers",
                "If pet: arrange temporary care or prepare transport",
                "If plants: water and protect for moving",
             ]},
            {"period": "D-Day", "label": "Move Day",
             "focus": "Supervise, inventory, handover",
             "tasks": [
                "Be present during entire loading process",
                "Check boxes against inventory before loading",
                "Final walkthrough: check all closets, cabinets, balcony",
                "Take photos of empty rooms",
                "Key handover to landlord / new tenant",
                "Check utility meter readings (take photos)",
                "Supervise unloading at new place: direct box placement",
             ]},
            {"period": "D+1~D+7", "label": "Settling Phase",
             "focus": "Unpack priorities, register, relax",
             "tasks": [
                "Day 1: Set up bed, kitchen, bathroom essentials",
                "Day 1: Clean new place (move-in deep clean)",
                "Day 2: Unpack clothes and daily essentials",
                "Day 3: Register at new community (居委会/物业)",
                "Day 3: Apply for parking / community access cards",
                "Day 4: Change address for social security, ID card (if inter-city)",
                "Day 5: Unpack remaining boxes room by room",
                "Day 6: Reassemble furniture, organize storage",
                "Day 7: Dispose of packing materials, recycle boxes",
                "If inter-city: update 居住证 (residence permit)",
             ]},
        ]

    # Add special-item tasks
    special_tasks = []
    for item in special_items:
        item_lower = item.lower()
        if "钢琴" in item or "piano" in item_lower:
            special_tasks.append("Hire piano specialist mover (extra fee)")
        if "猫" in item or "狗" in item or "pet" in item_lower or "宠物" in item:
            special_tasks.append("Arrange pet transport and temporary care")
        if "植物" in item or "plant" in item_lower:
            special_tasks.append("Protect plants: water, wrap, transport carefully")

    if special_tasks:
        periods.append({
            "period": "SPECIAL ITEMS",
            "label": "Special Handling",
            "focus": f"Items: {', '.join(special_items)}",
            "tasks": special_tasks,
        })

    return periods


# ── Step 3: Categorize Tasks ────────────────────────────────────────────────

def categorize_tasks(profile, timeline):
    """Categorize tasks into 4 pillars.

    AI Prompt Template:
      Categorize moving tasks into Admin, Packing, Logistics, and Cleaning
      pillars based on the profile: {profile}.
    """
    categories = {
        "Admin": {
            "label": "A. Admin Tasks",
            "description": "Address changes, contracts, utilities, documents",
            "tasks": [
                ("Notify landlord of move-out", "D-30~D-14"),
                ("Review lease termination terms and deposit conditions", "D-30~D-14"),
                ("Schedule utility disconnection: water, electricity, gas", "D-14~D-7"),
                ("Arrange internet/phone transfer or cancellation", "D-14~D-7"),
                ("Change address: bank, credit card, insurance", "D-14~D-7"),
                ("Update address on delivery apps and subscriptions", "D-14~D-7"),
                ("Update social security / welfare address (社保)", "D-14~D-7"),
                ("Apply for parking permit / community access at new place", "D-7~D-3"),
                ("Submit change of address for ID card / 居住证 (if applicable)", "D+1~D+7"),
                ("Register at new community 居委会/派出所", "D+1~D+7"),
            ],
        },
        "Packing": {
            "label": "B. Packing Tasks",
            "description": "Declutter, packing order, labeling, valuables",
            "tasks": [
                ("Declutter room by room: sell on Xianyu, donate, discard", "D-30~D-14"),
                ("Order packing supplies: boxes (various sizes), tape, markers", "D-30~D-14"),
                ("Pack off-season clothes and rarely used items", "D-14~D-7"),
                ("Pack books, decorations, collectibles", "D-14~D-7"),
                ("Create box inventory spreadsheet", "D-7~D-3"),
                ("Pack room by room: label every box clearly", "D-7~D-3"),
                ("Pack valuables separately: documents, jewelry, electronics", "D-7~D-3"),
                ("Disassemble furniture; keep fittings in labeled bags", "D-7~D-3"),
                ("Pack essentials bag (3 days) and first-night box", "D-3~D-1"),
            ],
        },
        "Logistics": {
            "label": "C. Logistics Tasks",
            "description": "Mover booking, transport, insurance",
            "tasks": [
                ("Research 3+ moving options: 货拉拉, 快狗, traditional movers", "D-30~D-14"),
                ("Get quotes and compare prices", "D-30~D-14"),
                ("Book movers and confirm date/time", "D-14~D-7"),
                ("Book freight elevator / parking permit for moving truck", "D-14~D-7"),
                ("Check mover insurance coverage; consider supplemental", "D-14~D-7"),
                ("Confirm final box count with movers", "D-7~D-3"),
                ("Prepare cash/cards for payment and tips", "D-3~D-1"),
                ("Check weather forecast for move day", "D-3~D-1"),
            ],
        },
        "Cleaning": {
            "label": "D. Cleaning Tasks",
            "description": "Move-out deep clean, move-in sanitize",
            "tasks": [
                ("Plan move-out cleaning: walls, kitchen grease, bathroom mold", "D-7~D-3"),
                ("Buy move-out cleaning supplies if DIY", "D-7~D-3"),
                ("Schedule professional cleaning if needed", "D-7~D-3"),
                ("Deep clean move-out after all boxes are loaded", "D-Day"),
                ("Sanitize new place: kitchen, bathroom, floors", "D+1~D+2"),
                ("Check for pests in new place (cockroaches, mice)", "D+1~D+2"),
                ("Wipe down all cabinets and shelves before unpacking", "D+1~D+2"),
                ("Test all appliances in new place", "D+1~D+2"),
            ],
        },
    }

    # Adjust for distance
    if profile["distance"] == "跨城":
        categories["Admin"]["tasks"].extend([
            ("Arrange long-distance shipping / luggage delivery", "D-14~D-7"),
            ("Update 居住证 (residence permit) for new city", "D+1~D+7"),
            ("Research new city utility setup process", "D-14~D-7"),
        ])
    elif profile["distance"] == "跨国":
        categories["Admin"]["tasks"].extend([
            ("Handle customs documentation for shipped items", "D-30~D-14"),
            ("Arrange international moving company", "D-30~D-14"),
            ("Update visa / residence status for new country", "D-14~D-7"),
            ("Arrange pet quarantine paperwork if applicable", "D-30~D-14"),
        ])

    return categories


# ── Step 4: Role Assignment ─────────────────────────────────────────────────

def assign_roles(profile, categories):
    """Assign tasks to household members.

    AI Prompt Template:
      Assign tasks from the categorized list to household members: {members}.
      Default assignments by category or room. Allow overrides.
    """
    members = profile.get("household_members", [])
    if not members and profile["household_size"] == "solo":
        return {"owner": "You", "note": "Solo move — all tasks assigned to you."}

    if not members:
        return {"owner": "All", "note": "General assignment (no members specified)."}

    default_map = [
        ("Admin", 0),
        ("Packing", 1 if len(members) > 1 else 0),
        ("Logistics", 0 if len(members) > 1 else 0),
        ("Cleaning", 1 if len(members) > 0 else 0),
    ]

    assignment = {}
    for i, (cat, member_idx) in enumerate(default_map):
        m = members[member_idx % len(members)]
        assignment[cat] = m

    return {
        "owner": "Team",
        "members": members,
        "assignment": assignment,
        "note": "Default assignment by category. Use --override to customize.",
    }


# ── Step 5: Budget Estimation ────────────────────────────────────────────────

def estimate_budget(profile):
    """Estimate moving costs.

    AI Prompt Template:
      Estimate moving costs based on profile: {profile}.
      Apply city-tier multipliers. Output categorized breakdown.
    """
    distance = profile["distance"]
    hh_size = profile["household_size"]
    furniture = profile.get("furniture", "")
    city_tier = profile.get("city_tier", "Tier 1")
    has_special = bool(profile.get("special_items", []))

    multiplier = {"Tier 1": 1.3, "Tier 2": 1.0, "Tier 3": 0.85}.get(city_tier, 1.0)

    # Base estimates
    if hh_size == "solo":
        box_est = "15-20"
        box_cost = 80
        mover_est = "¥300-600"
        mover_min, mover_max = 300, 600
    elif hh_size == "couple":
        box_est = "20-30"
        box_cost = 120
        mover_est = "¥500-900"
        mover_min, mover_max = 500, 900
    else:  # family
        box_est = "40-55"
        box_cost = 200
        mover_est = "¥800-1500"
        mover_min, mover_max = 800, 1500

    if distance == "跨城":
        mover_min = int(mover_min * 3.5)
        mover_max = int(mover_max * 4)
        mover_est = f"¥{mover_min}-{mover_max}"
    elif distance == "跨国":
        mover_min = int(mover_min * 15)
        mover_max = int(mover_max * 20)
        mover_est = f"¥{mover_min}-{mover_max}"

    mover_min = int(mover_min * multiplier)
    mover_max = int(mover_max * multiplier)

    cleaning_cost = 200 if hh_size == "solo" else (350 if hh_size == "couple" else 500)
    cleaning_cost = int(cleaning_cost * multiplier)

    deposit_expectation = 500 if hh_size == "solo" else (1000 if hh_size == "couple" else 2000)

    special_cost = 0
    if has_special:
        special_cost = 500

    total_min = mover_min + box_cost + cleaning_cost + special_cost
    total_max = mover_max + box_cost + cleaning_cost + deposit_expectation + special_cost

    budget = {
        "city_tier": city_tier,
        "multiplier": multiplier,
        "box_count_estimate": box_est,
        "categories": [
            {"item": "Movers / 搬运", "est": f"¥{mover_min}-{mover_max}"},
            {"item": "Packing supplies / 包装材料 (boxes, tape, wrap)", "est": f"¥{box_cost}"},
            {"item": "Cleaning / 保洁", "est": f"¥{cleaning_cost}"},
            {"item": "Deposit deduction expected / 押金扣款", "est": f"¥0-{deposit_expectation}"},
        ],
        "total_range": f"¥{total_min}-{total_max}",
        "notes": [],
    }

    if has_special:
        budget["categories"].append({"item": "Special items / 特殊物品搬运", "est": f"¥{special_cost}+"})

    if distance == "跨城":
        budget["notes"].append("Inter-city moves may require additional shipping costs for large furniture")
    elif distance == "跨国":
        budget["notes"].append("International moving: add customs fees, shipping container costs, visa expenses")

    budget["notes"].append(f"City tier multiplier applied: {city_tier} (×{multiplier})")

    return budget


# ── Step 6: Generate Handbook ───────────────────────────────────────────────

def generate_handbook(profile, timeline, categories, role_assignment, budget):
    """Generate complete moving handbook.

    AI Prompt Template:
      Combine timeline, categorized tasks, role assignments, and budget
      into a complete printable moving handbook in structured Markdown.
      Sections: Cover -> Countdown Calendar -> Admin Checklist ->
      Packing Guide -> Logistics Plan -> Cleaning Checklist ->
      Budget Sheet -> Emergency Contacts.
    """
    lines = []
    lines.append("# Moving Handbook / 搬家手册")
    lines.append("")
    lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Move Date**: {profile.get('move_date', 'TBD')}")
    lines.append(f"**From → To**: {profile.get('current', '?')} → {profile.get('new_address', '?')}")
    lines.append(f"**Distance**: {profile.get('distance', '?')}")
    lines.append(f"**Household**: {profile.get('household_size', '?')}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Countdown Calendar
    lines.append("## Countdown Calendar / 倒计时日历")
    lines.append("")
    for period in timeline:
        lines.append(f"### {period['period']}: {period['label']}")
        lines.append(f"*Focus: {period['focus']}*")
        lines.append("")
        for task in period['tasks']:
            lines.append(f"- [ ] {task}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Task Categories
    lines.append("## Categorized Task Checklists")
    lines.append("")
    for cat_key in ["Admin", "Packing", "Logistics", "Cleaning"]:
        cat = categories.get(cat_key)
        if not cat:
            continue
        lines.append(f"### {cat['label']}")
        lines.append(f"*{cat['description']}*")
        lines.append("")
        for task, deadline in cat["tasks"]:
            lines.append(f"- [ ] {deadline} — {task}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Role Assignment
    lines.append("## Role Assignment / 角色分工")
    lines.append("")
    if role_assignment.get("members"):
        lines.append(f"**Members**: {', '.join(role_assignment['members'])}")
        lines.append("")
        lines.append("| Category | Owner |")
        lines.append("|----------|-------|")
        for cat, owner in role_assignment.get("assignment", {}).items():
            cat_label = {"Admin": "Admin", "Packing": "Packing", "Logistics": "Logistics", "Cleaning": "Cleaning"}.get(cat, cat)
            lines.append(f"| {cat_label} | {owner} |")
    else:
        lines.append(f"**{role_assignment.get('owner', 'You')}**")
        lines.append("")
        lines.append(f"*{role_assignment.get('note', '')}*")
    lines.append("")

    lines.append("---")
    lines.append("")

    # Budget
    lines.append("## Budget Estimation / 预算估算")
    lines.append("")
    for cat in budget.get("categories", []):
        lines.append(f"- **{cat['item']}**: {cat['est']}")
    lines.append("")
    lines.append(f"**Total estimated range: {budget['total_range']}**")
    lines.append("")
    for note in budget.get("notes", []):
        lines.append(f"> {note}")
    lines.append("")

    lines.append("---")
    lines.append("")

    # Emergency Contacts
    lines.append("## Emergency Contacts / 紧急联系方式")
    lines.append("")
    lines.append("| Contact | Phone | Notes |")
    lines.append("|---------|-------|-------|")
    lines.append("| Mover (车队长) | | Confirm day before |")
    lines.append("| Landlord (房东) | | Key handover |")
    lines.append("| Property manager (物业) | | Elevator booking |")
    lines.append("| Emergency contact | | |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Handbook generated by Moving Checklist Skill. MIT-0 License.*")

    return "\n".join(lines)


# ── CLI ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Moving Checklist — generate personalized moving timeline & checklist.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --profile '{"current":"整租","new_address":"上海浦东","move_date":"2025-07-15","distance":"同城","household_size":"solo"}'
  %(prog)s --profile '{"distance":"跨城","household_size":"family","special_items":["钢琴","猫"]}'
  %(prog)s --interactive
  %(prog)s --validate-schemas
        """,
    )
    parser.add_argument("--profile", "-p", type=str, default="",
                        help="JSON moving profile or comma-separated key:value pairs")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Interactive mode (step-by-step questionaire)")
    parser.add_argument("--output", "-o", choices=["handbook", "json"], default="handbook",
                        help="Output format")
    parser.add_argument("--validate-schemas", action="store_true",
                        help="Validate schemas (dev mode)")

    args = parser.parse_args()

    if args.validate_schemas:
        try:
            load_reference("task_templates.json")
            load_reference("budget_tiers.json")
            print("  Schemas validated successfully")
            return 0
        except Exception as e:
            print(f"  Schema validation failed: {e}")
            return 1

    # Build profile
    if args.interactive:
        print("\n== Moving Checklist — Interactive Setup ==\n")
        current = input("Current residence type (整租/合租/自有): ") or "整租"
        new_addr = input("New address (city + district): ")
        move_date = input("Move date (YYYY-MM-DD): ")
        distance = input("Distance (同城/跨城/跨国): ") or "同城"
        hh_size = input("Household size (solo/couple/family): ") or "solo"
        members = input("Household members (comma-separated names, or leave blank): ")
        furniture = input("Furniture (房东提供/部分自有/全部自有): ") or "部分自有"
        special = input("Special items (comma-separated, or leave blank): ")

        profile = build_profile({
            "current": current,
            "new_address": new_addr,
            "move_date": move_date,
            "distance": distance,
            "household_size": hh_size,
            "household_members": [m.strip() for m in members.split(",") if m.strip()],
            "furniture": furniture,
            "special_items": [s.strip() for s in special.split(",") if s.strip()],
        })
    else:
        if not args.profile:
            print("Error: provide --profile or use --interactive")
            return 1
        profile = build_profile(args.profile)

    print(f"\n  Moving Profile: {profile.get('current', '?')} → {profile.get('new_address', '?')}")
    print(f"  Date: {profile.get('move_date', 'TBD')} | Distance: {profile.get('distance', '?')}")
    print(f"  Household: {profile.get('household_size', '?')} | City tier: {profile.get('city_tier', '?')}")

    # Step 2: Timeline
    print("\n  [Step 2/7] Generating countdown timeline...")
    timeline = generate_timeline(profile)
    print(f"  -> {len(timeline)} timeline periods generated")

    if args.output == "json":
        print(json.dumps(timeline, ensure_ascii=False, indent=2))

    # Step 3: Categorize tasks
    print("\n  [Step 3/7] Categorizing tasks into 4 pillars...")
    categories = categorize_tasks(profile, timeline)
    total_tasks = sum(len(c["tasks"]) for c in categories.values())
    print(f"  -> {total_tasks} tasks across {len(categories)} categories")

    # Step 4: Role assignment
    print("\n  [Step 4/7] Assigning roles...")
    role_assignment = assign_roles(profile, categories)
    print(f"  -> {role_assignment.get('owner', 'Assigned')}")

    # Step 5: Budget
    print("\n  [Step 5/7] Estimating budget...")
    budget = estimate_budget(profile)
    print(f"  -> Estimated: {budget['total_range']}")

    # Step 6: Generate handbook
    print("\n  [Step 6/7] Generating printable handbook...")
    handbook = generate_handbook(profile, timeline, categories, role_assignment, budget)
    print(f"  -> Handbook generated ({len(handbook)} chars)")

    if args.output == "handbook":
        print("\n" + "=" * 60)
        print(handbook)
        print("\n" + "=" * 60)
        print("  Step 7/7: Post-move follow-up available after move confirmation")

    if args.output == "json":
        output = {
            "version": "1.0.0",
            "profile": profile,
            "timeline": timeline,
            "categories": categories,
            "role_assignment": role_assignment,
            "budget": budget,
            "handbook": handbook,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))

    print("\n  Handbook complete! Save the output for your move.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
