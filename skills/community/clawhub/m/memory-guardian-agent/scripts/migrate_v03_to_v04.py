#!/usr/bin/env python3
"""memory-guardian: Migration script v0.3 → v0.4.

Upgrades meta.json schema:
  - Adds all v0.4 fields with sensible defaults
  - Preserves mem_* IDs (backward compatible)
  - Upgrades version string
  - Adds top-level conflicts[] and security_rules[]
  - Creates conflicts/ directory

Usage:
  python3 migrate_v03_to_v04.py [--workspace <path>] [--dry-run] [--backup]

Safe: always creates a backup before modifying meta.json.
"""
import json, os, sys, argparse, shutil
from datetime import datetime
from mg_utils import _now_iso, CST, safe_print

print = safe_print


# v0.4 default field values for each memory entry
V04_DEFAULTS = {
    "case_type": "case",
    "situation": None,
    "judgment": None,
    "consequence": None,
    "action_conclusion": None,
    "confidence": 0.5,
    "reversibility": 1,
    "beta": 1.0,
    "trigger_count": 0,
    "last_triggered": None,
    "cooling_threshold": 5,
    "boundary_words": [],
    "conflict_refs": [],
    "failure_conditions": [],
    "failure_count": 0,
    "last_failure_trigger": None,
    "last_failure_fix": None,
    "source_case_id": None,
    "alternatives_considered": [],
    "cost_factors": {
        "write_cost": 0,
        "verify_cost": 0,
        "human_cost": 0,
        "transfer_cost": 0,
    },
    "quality_gate": {
        "confidence": 0.5,
        "gate_mode": "normal",
        "bypass_reason": None,
    },
    "importance_explain": None,
    "security_version": 1,
    "cooldown_active": False,
    "cooldown_until": None,
    "observing_since": None,
    "suspended_pending_count": 0,
}

# Fields that should be removed (v0.3-only)
REMOVE_FIELDS = ["case_template", "consecutive_same_source"]


from mg_utils import load_meta, save_meta


def migrate_entry(mem):
    """Migrate a single memory entry to v0.4 schema."""
    migrated = dict(mem)  # shallow copy

    # Migrate v0.3 case_template → v0.4 structured fields
    case_template = mem.get("case_template")
    if case_template and isinstance(case_template, dict):
        if case_template.get("情境"):
            migrated["situation"] = case_template["情境"]
        if case_template.get("判断"):
            migrated["judgment"] = case_template["判断"]
        if case_template.get("后果"):
            migrated["consequence"] = case_template["后果"]
        if case_template.get("修正"):
            migrated["action_conclusion"] = case_template["修正"]

    # Add all v0.4 defaults (don't overwrite existing values)
    for key, default in V04_DEFAULTS.items():
        if key not in migrated:
            migrated[key] = default

    # Remove deprecated v0.3 fields
    for field in REMOVE_FIELDS:
        migrated.pop(field, None)

    # Ensure status is valid
    valid_statuses = {"active", "archived", "deleted", "draft", "observing", "suspended"}
    if migrated.get("status") not in valid_statuses:
        migrated["status"] = "active"

    return migrated


def run(workspace, dry_run, backup):
    meta_path = os.path.join(workspace, "memory", "meta.json")

    if not os.path.exists(meta_path):
        print(f"[ERROR] meta.json not found at {meta_path}")
        return False

    meta = load_meta(meta_path)
    old_version = meta.get("version", "unknown")

    if old_version.startswith("0.4"):
        print(f"[SKIP] Already at v0.4+ (version: {old_version})")
        return True

    print(f"{'=' * 60}")
    print(f"MEMORY GUARDIAN — Migration v0.3 → v0.4")
    print(f"  Current version: {old_version}")
    print(f"  Records: {len(meta.get('memories', []))}")
    print(f"{'=' * 60}")

    # Backup
    if backup and not dry_run:
        backup_path = meta_path + f".backup-{datetime.now(CST).strftime('%Y%m%d-%H%M%S')}"
        shutil.copy2(meta_path, backup_path)
        print(f"\n✅ Backup created: {backup_path}")

    # Migrate each memory entry
    memories = meta.get("memories", [])
    migrated_count = 0
    for i, mem in enumerate(memories):
        old_id = mem.get("id", "?")
        new_mem = migrate_entry(mem)
        memories[i] = new_mem
        migrated_count += 1

        # Show what changed
        new_fields = [k for k in V04_DEFAULTS if k not in mem and k in new_mem]
        removed_fields = [k for k in REMOVE_FIELDS if k in mem]
        if new_fields or removed_fields:
            print(f"  [{old_id}] +{len(new_fields)} fields, -{len(removed_fields)} fields")

    # Update top-level structure
    if "conflicts" not in meta:
        meta["conflicts"] = []
        print(f"\n  Added top-level conflicts[]")
    if "security_rules" not in meta:
        meta["security_rules"] = []
        print(f"  Added top-level security_rules[]")

    meta["version"] = "0.4.0"
    meta["migrated_at"] = _now_iso()
    meta["migration_from"] = old_version

    if dry_run:
        print(f"\n[DRY RUN] Would migrate {migrated_count} records")
        print(f"[DRY RUN] New version: 0.4.0")
        return True

    save_meta(meta_path, meta)

    # Create conflicts directory
    conflicts_dir = os.path.join(workspace, "memory", "conflicts")
    if not os.path.exists(conflicts_dir):
        os.makedirs(conflicts_dir, exist_ok=True)
        print(f"  Created: {conflicts_dir}/")

    print(f"\n✅ Migration complete!")
    print(f"  Migrated: {migrated_count} records")
    print(f"  New version: 0.4.0")
    print(f"  meta.json: {meta_path}")
    return True


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Migrate meta.json v0.3 → v0.4")
    p.add_argument("--workspace", default=None, help="Workspace root path")
    p.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    p.add_argument("--backup", action="store_true", default=True, help="Create backup (default: true)")
    p.add_argument("--no-backup", action="store_true", help="Skip backup creation")
    args = p.parse_args()

    workspace = args.workspace or os.environ.get(
        "OPENCLAW_WORKSPACE", os.path.expanduser("~/workspace/agent/workspace")
    )

    success = run(workspace, args.dry_run, not args.no_backup)
    sys.exit(0 if success else 1)
