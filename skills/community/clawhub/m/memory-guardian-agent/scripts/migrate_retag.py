#!/usr/bin/env python3
"""migrate_retag.py — v0.4.4 → v0.4.5 schema migration.

Adds v0.4.5 fields to all existing memories, creates directory structure,
and generates memory_id for each entry.

New fields added per memory:
  - memory_id: mem_<md5_8>_<ts_4> (unique primary key)
  - file_path: derived from tags + memory_id
  - tags_locked: False (existing entries unlocked for reclassification)
  - classification_confidence: None
  - classification_context: "migrated from v0.4.4"
  - inbox_reason: None
  - signal_level: None
  - reactivation_count: 0
  - last_reactivated: None
  - trigger_words: []
  - needs_review: False
  - needs_review_since: None
  - needs_review_timeout: "7d"
  - review_result: None
  - reviewed_at: None
  - version: 0
  - access_signals: []

Global fields added:
  - routing_log: []
  - conflict_log: []
  - migration_log: [migration_record]

Usage:
  python3 migrate_retag.py --workspace /path/to/workspace [--dry-run]
  python3 migrate_retag.py --workspace /path/to/workspace --apply
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(__file__))

from mg_utils import (
    read_text_file, safe_print, _now_iso, generate_memory_id,
    derive_file_path, resolve_primary_tag, save_meta, load_meta,
)
from mg_schema import MEMORY_DEFAULTS

print = safe_print

CST = timezone(timedelta(hours=8))

# Directories to create
MEMORY_DIRS = [
    "memory/project",
    "memory/social",
    "memory/tech",
    "memory/personal",
    "memory/_inbox/uncertain",
    "memory/_inbox/deferred",
    "memory/_inbox/pending_review",
    "memory/_sandbox",
    "memory/misc",
]

V045_GLOBAL_DEFAULTS = {
    "routing_log": [],
    "conflict_log": [],
}


def parse_args():
    parser = argparse.ArgumentParser(description="migrate_retag: v0.4.4 → v0.4.5")
    parser.add_argument("--workspace", required=True, help="Workspace root path")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes")
    parser.add_argument("--apply", action="store_true", help="Apply migration")
    parser.add_argument("--step", choices=["fields", "dirs", "files", "verify"], help="Run specific step only")
    return parser.parse_args()


def backup_meta(meta_path, dry_run=False):
    """Create backup of meta.json before migration."""
    bak_path = meta_path + ".v044.bak"
    if dry_run:
        print(f"  [DRY-RUN] Would backup meta.json → {bak_path}")
        return True
    if os.path.exists(bak_path):
        print(f"  ⚠️  Backup already exists: {bak_path}")
        print(f"  ℹ️  Skipping backup (remove manually to re-backup)")
        return True
    shutil.copy2(meta_path, bak_path)
    print(f"  ✅ Backup created: {bak_path}")
    return True


def step_fields(meta, dry_run=False):
    """Step 1: Add v0.4.5 fields to all memories."""
    print("\n" + "=" * 60)
    print("Step 1: Add v0.4.5 schema fields")
    print("=" * 60)

    memories = meta.get("memories", [])
    print(f"  Total memories: {len(memories)}")

    # Collect existing memory_ids for uniqueness
    existing_ids = set()
    for mem in memories:
        if mem.get("memory_id"):
            existing_ids.add(mem["memory_id"])

    updated = 0
    skipped = 0
    for mem in memories:
        mem_id = mem.get("id", "")
        content = mem.get("content", "")
        tags = mem.get("tags", [])

        # Generate memory_id if not present
        if not mem.get("memory_id"):
            new_mid = generate_memory_id(content, existing_ids=existing_ids)
            mem["memory_id"] = new_mid
            existing_ids.add(new_mid)
            if dry_run:
                print(f"  [DRY-RUN] {mem_id} → memory_id={new_mid}")
            else:
                print(f"  + {mem_id} → memory_id={new_mid}")
            updated += 1
        else:
            skipped += 1

        # Derive file_path if not present
        if not mem.get("file_path"):
            mem["file_path"] = derive_file_path(
                mem["memory_id"], tags, content
            )

        # Fill new field defaults (only if not already present)
        for key, default in MEMORY_DEFAULTS.items():
            if key not in mem:
                mem[key] = default

        # Migration-specific: tag classification context
        if mem.get("classification_context") is None:
            mem["classification_context"] = "migrated from v0.4.4"

    # Add global fields
    for key, default in V045_GLOBAL_DEFAULTS.items():
        if key not in meta:
            meta[key] = default

    # Add migration log
    migration_logs = meta.get("migration_log", [])
    migration_logs.append({
        "from_version": meta.get("version", "0.4.4"),
        "to_version": "0.4.5",
        "timestamp": _now_iso(),
        "memories_processed": len(memories),
        "memory_ids_generated": updated,
        "description": "v0.4.4 → v0.4.5: added memory_id, file_path, classification fields, signal fields, needs_review, version",
    })
    meta["migration_log"] = migration_logs

    # Update version
    meta["version"] = "0.4.5"
    meta["schema_version"] = "v0.4.5"

    print(f"  ✅ Updated: {updated} memory_ids generated, {skipped} already had memory_id")
    print(f"  ✅ Added {len(MEMORY_DEFAULTS)} default fields per memory")
    return True


def step_dirs(workspace, dry_run=False):
    """Step 2: Create category directory structure."""
    print("\n" + "=" * 60)
    print("Step 2: Create directory structure")
    print("=" * 60)

    for dir_path in MEMORY_DIRS:
        full_path = os.path.join(workspace, dir_path)
        if dry_run:
            print(f"  [DRY-RUN] mkdir -p {full_path}")
        else:
            os.makedirs(full_path, exist_ok=True)
            print(f"  ✅ {dir_path}/")

    print(f"  ✅ {len(MEMORY_DIRS)} directories ready")
    return True


def step_write_files(meta, workspace, dry_run=False):
    """Step 3: Write memory content files to category directories."""
    print("\n" + "=" * 60)
    print("Step 3: Write memory files to category directories")
    print("=" * 60)

    from memory_ingest import _write_memory_file

    memories = meta.get("memories", [])
    files_written = 0
    files_skipped = 0

    for mem in memories:
        fp = mem.get("file_path", "")
        if not fp:
            files_skipped += 1
            continue

        # Skip if file already exists (idempotent)
        abs_path = os.path.join(workspace, fp)
        if os.path.exists(abs_path):
            continue

        if dry_run:
            print(f"  [DRY-RUN] {fp}")
            files_written += 1
            continue

        try:
            result = _write_memory_file(
                mem["memory_id"], mem.get("content", ""), fp, workspace=workspace
            )
            if result:
                files_written += 1
        except Exception as e:
            logging.warning("migrate_retag: failed to write %s: %s", fp, e)
            files_skipped += 1

    existing = sum(1 for m in memories
                   if m.get("file_path") and os.path.exists(os.path.join(workspace, m["file_path"])))
    total = len([m for m in memories if m.get("file_path")])
    print(f"  ✅ {files_written} files written (skipped {files_skipped})")
    print(f"  ✅ {existing}/{total} memory files now on disk")
    return True


def step_verify(meta, workspace, dry_run=False):
    """Step 4: Verify migration integrity."""
    print("\n" + "=" * 60)
    print("Step 3: Verify migration integrity")
    print("=" * 60)

    memories = meta.get("memories", [])
    errors = []
    warnings = []

    # Check 1: All memories have memory_id
    missing_mid = [m for m in memories if not m.get("memory_id")]
    if missing_mid:
        errors.append(f"{len(missing_mid)} memories missing memory_id")
    else:
        print(f"  ✅ All {len(memories)} memories have memory_id")

    # Check 2: All memory_ids are unique
    mids = [m.get("memory_id") for m in memories if m.get("memory_id")]
    if len(mids) != len(set(mids)):
        dupes = len(mids) - len(set(mids))
        errors.append(f"{dupes} duplicate memory_ids")
    else:
        print(f"  ✅ All {len(mids)} memory_ids are unique")

    # Check 3: All memories have v0.4.5 fields
    field_errors = []
    for key in MEMORY_DEFAULTS:
        missing = [m.get("id", m.get("memory_id", "?")) for m in memories if key not in m]
        if missing:
            field_errors.append(f"{len(missing)} memories missing field '{key}'")
    errors.extend(field_errors)
    if not field_errors:
        print(f"  ✅ All {len(MEMORY_DEFAULTS)} v0.4.5 fields present")

    # Check 4: All file_paths are valid
    missing_files = []
    for mem in memories:
        fp = mem.get("file_path", "")
        if not fp:
            warnings.append(f"{mem.get('memory_id', '?')} has empty file_path")
        elif not os.path.exists(os.path.join(workspace, fp)):
            missing_files.append(mem.get("memory_id", "?"))
    if missing_files:
        warnings.append(f"{len(missing_files)} memory files missing on disk (file_path set but file not found)")
    if warnings:
        print(f"  ⚠️  {len(warnings)} warnings:")
        for w in warnings[:10]:
            print(f"      - {w}")
    else:
        print(f"  ✅ All file_paths populated and files exist on disk")

    # Check 5: Directories exist
    if not dry_run:
        for dir_path in MEMORY_DIRS:
            full_path = os.path.join(workspace, dir_path)
            if not os.path.isdir(full_path):
                errors.append(f"Missing directory: {dir_path}")
        if not any("Missing directory" in e for e in errors):
            print(f"  ✅ All {len(MEMORY_DIRS)} directories exist")

    # Check 6: Version updated
    if meta.get("version") == "0.4.5":
        print(f"  ✅ Version updated to 0.4.5")
    else:
        errors.append(f"Version is {meta.get('version')}, expected 0.4.5")

    # Check 7: Original id fields preserved
    missing_orig = [m for m in memories if not m.get("id")]
    if missing_orig:
        errors.append(f"{len(missing_orig)} memories lost original 'id' field")
    else:
        print(f"  ✅ Original 'id' fields preserved")

    if errors:
        print(f"\n  ❌ {len(errors)} ERRORS:")
        for e in errors:
            print(f"      - {e}")
        return False
    else:
        print(f"\n  ✅ Migration verified — all checks passed")
        return True


def rollback(workspace):
    """Rollback migration using backup."""
    meta_path = os.path.join(workspace, "memory", "meta.json")
    bak_path = meta_path + ".v044.bak"

    if not os.path.exists(bak_path):
        print(f"  ❌ No backup found: {bak_path}")
        return False

    print(f"  Rolling back: {bak_path} → {meta_path}")
    shutil.copy2(bak_path, meta_path)
    print(f"  ✅ Rolled back to pre-migration state")
    return True


def main():
    args = parse_args()
    workspace = os.path.abspath(args.workspace)
    meta_path = os.path.join(workspace, "memory", "meta.json")

    if not os.path.exists(meta_path):
        print(f"[ERROR] meta.json not found at {meta_path}")
        sys.exit(1)

    meta = load_meta(meta_path)
    current_version = meta.get("version", "unknown")
    print(f"Current version: {current_version}")
    print(f"Memories: {len(meta.get('memories', []))}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'APPLY' if args.apply else 'INFO'}")

    if args.apply and not args.dry_run:
        backup_meta(meta_path, dry_run=False)

    if args.step == "fields" or args.step is None:
        step_fields(meta, dry_run=args.dry_run)

    if args.step == "dirs" or args.step is None:
        step_dirs(workspace, dry_run=args.dry_run)

    if args.step == "files" or args.step is None:
        step_write_files(meta, workspace, dry_run=args.dry_run)

    if args.step == "verify" or args.step is None:
        step_verify(meta, workspace, dry_run=args.dry_run)

    if args.apply and not args.dry_run:
        save_meta(meta_path, meta, use_lock=True)
        print(f"\n✅ Migration complete — meta.json saved")

    elif args.dry_run:
        print(f"\n[DRY-RUN] No changes made. Use --apply to execute.")


if __name__ == "__main__":
    main()
