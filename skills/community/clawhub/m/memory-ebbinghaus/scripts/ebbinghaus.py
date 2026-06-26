#!/usr/bin/env python3
"""
Ebbinghaus Memory Manager
Manages AI agent memory items with forgetting curve lifecycle.

Usage:
  python3 ebbinghaus.py status          # View all memory items
  python3 ebbinghaus.py decay           # Update all strength values
  python3 ebbinghaus.py review <id>     # Reinforce a memory
  python3 ebbinghaus.py forget <id>     # Delete a memory item
  python3 ebbinghaus.py archive <id>    # Archive to long-term memory file
  python3 ebbinghaus.py add <content> [--category <cat>] [--source <file>]
  python3 ebbinghaus.py heartbeat       # Output fading items (for heartbeat use)

Environment Variables:
  EBBINGHAUS_DB       Path to JSON database (default: ./memory_db.json)
  EBBINGHAUS_ARCHIVE  Path to archive file  (default: ./MEMORY.md)
"""

import json
import math
import os
import sys
import argparse
from datetime import datetime, date

# Configurable paths via environment variables
DB_PATH = os.environ.get(
    "EBBINGHAUS_DB",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "memory_db.json")
)
ARCHIVE_PATH = os.environ.get(
    "EBBINGHAUS_ARCHIVE",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "MEMORY.md")
)

# Strength thresholds
THRESHOLD_ACTIVE = 0.7
THRESHOLD_DECAYING = 0.3


def load_db():
    db_path = os.path.abspath(DB_PATH)
    if not os.path.exists(db_path):
        return {"items": [], "next_id": 1}
    with open(db_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(db):
    db_path = os.path.abspath(DB_PATH)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def calc_strength(last_reviewed: str, stability: float) -> float:
    """Ebbinghaus strength formula: e^(-days_elapsed / stability)"""
    try:
        last = date.fromisoformat(last_reviewed)
    except ValueError:
        return 1.0
    elapsed = (date.today() - last).days
    return math.exp(-elapsed / max(stability, 0.1))


def status_emoji(strength: float) -> str:
    if strength >= THRESHOLD_ACTIVE:
        return "🟢"
    elif strength >= THRESHOLD_DECAYING:
        return "🟡"
    else:
        return "🔴"


def cmd_status(db):
    items = db["items"]
    if not items:
        print("📭 No memory items found.")
        return
    print(f"{'ID':<6} {'Str':>5} {'St'} {'Stab':>6} {'Last Review':>12}  Content")
    print("-" * 80)
    for item in sorted(items, key=lambda x: calc_strength(x["last_reviewed"], x["stability"])):
        s = calc_strength(item["last_reviewed"], item["stability"])
        item["strength"] = round(s, 3)
        emoji = status_emoji(s)
        print(f"{item['id']:<6} {s:>5.2f} {emoji}   {item['stability']:>5.1f}  {item['last_reviewed']:>12}  {item['content'][:50]}")
    save_db(db)


def cmd_decay(db):
    updated = 0
    for item in db["items"]:
        old = item.get("strength", 1.0)
        new = calc_strength(item["last_reviewed"], item["stability"])
        item["strength"] = round(new, 3)
        if abs(old - new) > 0.001:
            updated += 1
    save_db(db)
    print(f"✅ Updated {updated} memory strength values.")


def cmd_review(db, item_id):
    for item in db["items"]:
        if str(item["id"]) == str(item_id):
            item["last_reviewed"] = date.today().isoformat()
            item["stability"] = round(item["stability"] * 1.5, 2)
            item["strength"] = 1.0
            item["review_count"] = item.get("review_count", 0) + 1
            save_db(db)
            print(f"✅ Reviewed: [{item_id}] {item['content'][:50]}")
            print(f"   Stability: {item['stability']:.1f} | Next ~{int(item['stability'])} days to 37%")
            return
    print(f"❌ Item not found: ID={item_id}")


def cmd_forget(db, item_id):
    for i, item in enumerate(db["items"]):
        if str(item["id"]) == str(item_id):
            content = item["content"]
            db["items"].pop(i)
            save_db(db)
            print(f"🗑️  Deleted: [{item_id}] {content[:50]}")
            return
    print(f"❌ Item not found: ID={item_id}")


def cmd_archive(db, item_id):
    for i, item in enumerate(db["items"]):
        if str(item["id"]) == str(item_id):
            content = item["content"]
            source = item.get("source", "")
            category = item.get("category", "general")
            archive_path = os.path.abspath(ARCHIVE_PATH)
            os.makedirs(os.path.dirname(archive_path), exist_ok=True)
            with open(archive_path, "a", encoding="utf-8") as f:
                f.write(f"\n### [Archived] {content}\n")
                if source:
                    f.write(f"- Source: {source}\n")
                f.write(f"- Category: {category} | Archived: {date.today().isoformat()}\n")
            db["items"].pop(i)
            save_db(db)
            print(f"📦 Archived to {archive_path}: [{item_id}] {content[:50]}")
            return
    print(f"❌ Item not found: ID={item_id}")


def cmd_add(db, content, category="general", source=""):
    new_id = db.get("next_id", len(db["items"]) + 1)
    item = {
        "id": new_id,
        "content": content,
        "category": category,
        "source": source,
        "created": date.today().isoformat(),
        "last_reviewed": date.today().isoformat(),
        "stability": 1.0,
        "strength": 1.0,
        "review_count": 0
    }
    db["items"].append(item)
    db["next_id"] = new_id + 1
    save_db(db)
    print(f"✅ Added: [{new_id}] {content[:50]}")


def cmd_heartbeat(db):
    """Output fading items for heartbeat use."""
    red = []
    yellow = []
    for item in db["items"]:
        s = calc_strength(item["last_reviewed"], item["stability"])
        item["strength"] = round(s, 3)
        if s < THRESHOLD_DECAYING:
            red.append(item)
        elif s < THRESHOLD_ACTIVE:
            yellow.append(item)
    save_db(db)

    if not red and not yellow:
        print("HEARTBEAT_OK")
        return

    output = []
    if red:
        output.append(f"🔴 **{len(red)} memories fading** (strength < 0.3):")
        for item in red[:5]:
            output.append(f"  - [{item['id']}] {item['content'][:60]} (strength: {item['strength']:.2f})")
        if len(red) > 5:
            output.append(f"  ... and {len(red)-5} more")

    if yellow:
        output.append(f"🟡 **{len(yellow)} memories decaying** (strength 0.3–0.7):")
        for item in yellow[:3]:
            output.append(f"  - [{item['id']}] {item['content'][:60]} (strength: {item['strength']:.2f})")

    output.append("\n💡 Use `python3 ebbinghaus.py review <id>` to reinforce, or `forget <id>` to delete.")
    print("\n".join(output))


def main():
    parser = argparse.ArgumentParser(description="Ebbinghaus Memory Manager")
    parser.add_argument("command", choices=["status", "decay", "review", "forget", "archive", "add", "heartbeat"])
    parser.add_argument("target", nargs="?", help="ID or content")
    parser.add_argument("--category", default="general")
    parser.add_argument("--source", default="")
    args = parser.parse_args()

    db = load_db()

    if args.command == "status":
        cmd_status(db)
    elif args.command == "decay":
        cmd_decay(db)
    elif args.command == "review":
        if not args.target:
            print("❌ Please provide ID, e.g.: review 3")
            sys.exit(1)
        cmd_review(db, args.target)
    elif args.command == "forget":
        if not args.target:
            print("❌ Please provide ID, e.g.: forget 3")
            sys.exit(1)
        cmd_forget(db, args.target)
    elif args.command == "archive":
        if not args.target:
            print("❌ Please provide ID, e.g.: archive 3")
            sys.exit(1)
        cmd_archive(db, args.target)
    elif args.command == "add":
        if not args.target:
            print("❌ Please provide content, e.g.: add 'project completed'")
            sys.exit(1)
        cmd_add(db, args.target, args.category, args.source)
    elif args.command == "heartbeat":
        cmd_heartbeat(db)


if __name__ == "__main__":
    main()
