#!/usr/bin/env bash
# migrate-contacts.sh — Import contacts from CSV into Relationship Buddy
#
# Usage: bash migrate-contacts.sh <input.csv>
#
# CSV format (first row = headers):
#   name,relationship,category,birthday,email,phone,notes
#
# Example:
#   name,relationship,category,birthday,email,phone,notes
#   Sarah Chen,best_friend,inner_circle,1988-07-15,sarah@email.com,555-1234,Loves matcha
#
# Output: Appends to data/contacts.json in the workspace data directory.
# Requires: python3

set -euo pipefail
umask 077

# --- Workspace root detection ---
find_skill_root() {
    # Stay within the skill directory — do not traverse outside
    cd "$(dirname "$0")/.." && pwd
}

SKILL_DIR="$(find_skill_root)"
if [[ -z "$SKILL_DIR" ]]; then
    echo "ERROR: Could not find workspace root. Run this script from within your agent workspace."
    exit 1
fi

DATA_DIR="$SKILL_DIR/data/relationship-buddy/data"
CONTACTS_FILE="$DATA_DIR/contacts.json"

# --- Validate input ---
if [[ $# -lt 1 ]]; then
    echo "Usage: bash migrate-contacts.sh <input.csv>"
    echo ""
    echo "CSV format: name,relationship,category,birthday,email,phone,notes"
    exit 1
fi

INPUT_FILE="$1"

if [[ ! -f "$INPUT_FILE" ]]; then
    echo "ERROR: File not found: $INPUT_FILE"
    exit 1
fi

if [[ -L "$INPUT_FILE" ]]; then
    echo "ERROR: Refusing symlink input file: $INPUT_FILE"
    exit 1
fi

# --- Ensure data directory exists ---
mkdir -p "$DATA_DIR"
chmod 700 "$DATA_DIR"

if [[ ! -f "$CONTACTS_FILE" ]]; then
    echo '[]' > "$CONTACTS_FILE"
    chmod 600 "$CONTACTS_FILE"
fi

if [[ -L "$CONTACTS_FILE" ]]; then
    echo "ERROR: Refusing to write to symlinked contacts file: $CONTACTS_FILE"
    exit 1
fi

# --- Import using Python for proper JSON handling ---
python3 - "$INPUT_FILE" "$CONTACTS_FILE" << 'PYEOF'
import csv, json, sys, os, re
from datetime import datetime

input_file = sys.argv[1]
contacts_file = sys.argv[2]

with open(contacts_file, "r") as f:
    contacts = json.load(f)

max_id = 0
for c in contacts:
    match = re.match(r"c_(\d+)", c.get("id", "c_000"))
    if match:
        max_id = max(max_id, int(match.group(1)))

imported = 0
skipped = 0

with open(input_file, "r", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get("name", "").strip()
        if not name:
            skipped += 1
            continue
        if any(c["name"].lower() == name.lower() for c in contacts):
            print(f"SKIP (duplicate): {name}")
            skipped += 1
            continue

        max_id += 1
        contact = {
            "id": f"c_{max_id:03d}",
            "name": name,
            "nickname": None,
            "relationship": row.get("relationship", "friend").strip(),
            "category": row.get("category", "friends").strip(),
            "key_dates": [],
            "preferences": {
                "favorite_foods": [],
                "favorite_drinks": [],
                "clothing_size": None,
                "hobbies": [],
                "dislikes": [],
                "gift_notes": []
            },
            "family": [],
            "life_events": [],
            "communication": {
                "preferred_channel": None,
                "best_time": None,
                "frequency_target_days": None
            },
            "notes": row.get("notes", "").strip(),
            "tags": ["imported"],
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "updated_at": datetime.now().strftime("%Y-%m-%d")
        }
        birthday = row.get("birthday", "").strip()
        if birthday:
            contact["key_dates"].append({
                "label": "Birthday",
                "date": birthday,
                "remind_days_before": 7
            })
        contacts.append(contact)
        imported += 1
        print(f"IMPORTED: {name}")

with open(contacts_file, "w") as f:
    json.dump(contacts, f, indent=2)
os.chmod(contacts_file, 0o600)

print(f"\nDone! Imported: {imported}, Skipped: {skipped}, Total contacts: {len(contacts)}")
PYEOF

echo ""
echo "Contacts file: $CONTACTS_FILE"
echo "Permissions set to 600 (owner read/write only)."
