#!/usr/bin/env python3
"""
Migrate existing account configs from old skill-embedded location
to the new persistent data directory.

Run this once if you had existing accounts configured before v1.5.4.

Usage:
    python3 migrate_data.py
"""

import json
import os
import shutil
import sys

# Old locations (within skill directory)
OLD_SKILL_DIRS = [
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".."),
    os.path.expanduser("~/.openclaw/workspace/skills/mail-assistant"),
]

# New location
from data_dir import DATA_DIR, ACCOUNTS_DIR, SYNC_STATE_PATH, RULES_PATH, ensure_data_dirs


def migrate():
    ensure_data_dirs()
    migrated_any = False

    for old_dir in set(OLD_SKILL_DIRS):
        if not os.path.isdir(old_dir):
            continue

        # Migrate accounts
        old_accts = os.path.join(old_dir, "accounts")
        if os.path.isdir(old_accts):
            for fname in os.listdir(old_accts):
                old_path = os.path.join(old_accts, fname)
                new_path = os.path.join(ACCOUNTS_DIR, fname)
                if fname.endswith((".json", ".token.json")) and not os.path.exists(new_path):
                    shutil.copy2(old_path, new_path)
                    print(f"[MIGRATED] {fname} -> {new_path}")
                    migrated_any = True

        # Migrate sync_state.json
        old_sync = os.path.join(old_dir, "sync_state.json")
        if os.path.exists(old_sync) and not os.path.exists(SYNC_STATE_PATH):
            with open(old_sync, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data:
                with open(SYNC_STATE_PATH, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                print(f"[MIGRATED] sync_state.json")
                migrated_any = True

        # Migrate auto_reply_rules.json
        old_rules = os.path.join(old_dir, "auto_reply_rules.json")
        if os.path.exists(old_rules) and not os.path.exists(RULES_PATH):
            with open(old_rules, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data:
                with open(RULES_PATH, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                print(f"[MIGRATED] auto_reply_rules.json")
                migrated_any = True

    if not migrated_any:
        print("[INFO] No data to migrate. Data directory is already at:")
        print(f"  {DATA_DIR}")
    else:
        print(f"\n[DONE] All data migrated to: {DATA_DIR}")
        print("You can now safely remove the old skill directory if desired.")


if __name__ == "__main__":
    migrate()
