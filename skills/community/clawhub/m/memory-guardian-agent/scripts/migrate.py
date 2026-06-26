#!/usr/bin/env python3
"""migrate.py — Unified schema migration tool.

Auto-detects the current meta.json version and runs all needed upgrade steps
in order. This is the single migration entry point — users should never need
to run individual migrate_*.py scripts directly.

Usage:
  python3 migrate.py --workspace <path> [--apply] [--dry-run] [--step <step>]

Steps (auto-detected, but can be forced):
  v0.3-to-v0.4    — Add v0.4 fields (importance, entities, decay, etc.)
  v0.4-to-v0.4.2  — Bootstrap case migration (mem_* → case_*)
  v0.4.2-to-v0.4.5 — Add memory_id, file_path, classification, signal fields
  files           — Write missing memory files to category directories
  verify          — Validate migration integrity
"""
import argparse
import json
import os
import shutil
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from mg_utils import load_meta, save_meta, _now_iso, read_text_file


def detect_version(meta):
    """Detect current schema version from meta.json."""
    ver = meta.get("version", "")
    schema = meta.get("schema_version", "")

    if not ver and not schema:
        # v0.3 has no version field
        return "0.3"
    if ver in ("0.4", "0.4.0", "0.4.1"):
        return "0.4.1"
    if ver in ("0.4.2", "0.4.3", "0.4.4"):
        return ver
    if ver == "0.4.5":
        return "0.4.5"
    return ver


def needs_step(current_ver, step_ver):
    """Check if a migration step is needed."""
    try:
        parts_a = [int(x) for x in current_ver.split(".")]
        parts_b = [int(x) for x in step_ver.split(".")]
        return parts_a < parts_b
    except (ValueError, AttributeError):
        return True


def step_v03_to_v04(meta, workspace, dry_run=False):
    """v0.3 → v0.4: Add core v0.4 fields to all memories."""
    print("\n" + "=" * 60)
    print("Step: v0.3 → v0.4")
    print("=" * 60)

    v04_memory_fields = {
        "importance": 0.5,
        "importance_f": 0.5,
        "entities": [],
        "tags": [],
        "status": "active",
        "decay_score": 0.5,
        "access_count": 0,
        "trigger_count": 0,
        "confidence": 0.5,
        "reversibility": 1,
        "beta": 1.0,
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
        "cost_factors": {"write_cost": 0, "verify_cost": 0, "human_cost": 0, "transfer_cost": 0},
        "quality_gate": {"confidence": 0.5, "gate_mode": "normal", "bypass_reason": None},
    }

    updated = 0
    for mem in meta.get("memories", []):
        changed = False
        for key, default in v04_memory_fields.items():
            if key not in mem:
                mem[key] = default
                changed = True
        if changed:
            updated += 1

    meta["version"] = "0.4.1"
    print(f"  ✅ Updated {updated} memories with v0.4 fields")
    return True


def step_v04_to_v042(meta, workspace, dry_run=False):
    """v0.4.1 → v0.4.2: Migrate bootstrap mem_* → case_* with five-tuple."""
    print("\n" + "=" * 60)
    print("Step: v0.4.1 → v0.4.2")
    print("=" * 60)

    import copy
    import uuid

    v042_fields = {
        "trigger_pattern": None,
        "action": None,
        "context": None,
        "source": "migration",
        "case_type": "case",
        "memory_type": "derive",
        "importance_explain": None,
        "security_version": 1,
        "cooldown_active": False,
        "cooldown_until": None,
        "observing_since": None,
        "suspended_pending_count": 0,
        "provenance_level": "L1",
        "provenance_source": "human_direct",
        "citations": [],
        "pinned": False,
        "schema_version": "v0.4.2",
    }

    migrated = 0
    for mem in meta.get("memories", []):
        changed = False
        if mem.get("id", "").startswith("mem_") and "bootstrapped" in mem.get("tags", []):
            # Convert mem_* to case_*
            old_id = mem["id"]
            mem["id"] = f"case_{uuid.uuid4().hex[:8]}"
            mem["migration_source"] = old_id
            mem["case_type"] = "case"
            # Extract heading and body for five-tuple
            content = mem.get("content", "")
            parts = content.split("\n", 1)
            mem["trigger_pattern"] = parts[0][:200] if parts else ""
            mem["context"] = parts[1][:300] if len(parts) > 1 else ""
            mem["action"] = ""
            changed = True

        for key, default in v042_fields.items():
            if key not in mem:
                mem[key] = default
                changed = True
        if changed:
            migrated += 1

    meta["version"] = "0.4.2"
    meta["schema_version"] = "v0.4.2"
    print(f"  ✅ Migrated {migrated} memories to v0.4.2 schema")
    return True


def step_v042_to_v045(meta, workspace, dry_run=False):
    """v0.4.2 → v0.4.5: Add memory_id, file_path, classification, signal fields."""
    print("\n" + "=" * 60)
    print("Step: v0.4.2/0.4.3/0.4.4 → v0.4.5")
    print("=" * 60)

    from mg_utils import generate_memory_id, derive_file_path, resolve_primary_tag
    from mg_schema import MEMORY_DEFAULTS

    memories = meta.get("memories", [])
    updated = 0

    for mem in memories:
        content = mem.get("content", "")
        tags = mem.get("tags", [])

        # Generate memory_id if missing
        if not mem.get("memory_id"):
            existing_ids = {m.get("memory_id") or m.get("id") for m in memories}
            mem["memory_id"] = generate_memory_id(content, existing_ids=existing_ids)
            updated += 1

        # Classify primary tag
        primary_tag = resolve_primary_tag(tags, content)
        if primary_tag not in tags:
            tags.append(primary_tag)
            mem["tags"] = tags

        # Derive file_path if missing
        if not mem.get("file_path"):
            mem["file_path"] = derive_file_path(mem["memory_id"], tags, content)
            updated += 1

        # Classification dict
        if not isinstance(mem.get("classification"), dict):
            mem["classification"] = {
                "primary_tag": primary_tag,
                "confidence": mem.get("classification_confidence", 0.5) or 0.5,
                "needs_review": False,
            }
            if mem.get("classification_confidence") is None:
                mem["classification_confidence"] = 0.5
            if mem.get("classification_context") is None:
                mem["classification_context"] = "migrated"
            updated += 1

        # Fill v0.4.5 defaults (single source of truth)
        for key, default in MEMORY_DEFAULTS.items():
            if key not in mem:
                mem[key] = default
                updated += 1

    # Global fields
    for key, default in {"routing_log": [], "conflict_log": []}.items():
        if key not in meta:
            meta[key] = default

    meta["version"] = "0.4.5"
    meta["schema_version"] = "v0.4.5"

    # Migration log
    logs = meta.get("migration_log", [])
    logs.append({
        "from_version": detect_version.__wrapped__(meta) if hasattr(detect_version, "__wrapped__") else "pre-v0.4.5",
        "to_version": "0.4.5",
        "timestamp": _now_iso(),
        "memories_processed": len(memories),
        "fields_updated": updated,
        "description": "Unified migration to v0.4.5 (via migrate.py)",
    })
    meta["migration_log"] = logs

    print(f"  ✅ Updated {updated} fields across {len(memories)} memories")
    return True


def step_write_files(meta, workspace, dry_run=False):
    """Write missing memory files to category directories."""
    print("\n" + "=" * 60)
    print("Step: Write missing memory files")
    print("=" * 60)

    from memory_ingest import _write_memory_file

    MEMORY_DIRS = [
        "memory/project", "memory/social", "memory/tech", "memory/personal",
        "memory/_inbox/uncertain", "memory/_inbox/deferred",
        "memory/_inbox/pending_review", "memory/_sandbox", "memory/misc",
    ]

    # Create directories
    for dir_path in MEMORY_DIRS:
        full_path = os.path.join(workspace, dir_path)
        if not dry_run:
            os.makedirs(full_path, exist_ok=True)

    # Write missing files
    memories = meta.get("memories", [])
    files_written = 0
    for mem in memories:
        fp = mem.get("file_path", "")
        if not fp or not mem.get("content"):
            continue
        abs_path = os.path.join(workspace, fp)
        if os.path.exists(abs_path):
            continue
        if dry_run:
            files_written += 1
            continue
        try:
            _write_memory_file(mem["memory_id"], mem["content"], fp, workspace=workspace)
            files_written += 1
        except Exception as e:
            print(f"  ⚠️  Failed to write {fp}: {e}")

    existing = sum(
        1 for m in memories
        if m.get("file_path") and os.path.exists(os.path.join(workspace, m["file_path"]))
    )
    total = len([m for m in memories if m.get("file_path")])
    print(f"  ✅ {files_written} files written")
    print(f"  ✅ {existing}/{total} memory files on disk")
    return True


def step_verify(meta, workspace, dry_run=False):
    """Verify migration integrity."""
    print("\n" + "=" * 60)
    print("Step: Verify integrity")
    print("=" * 60)

    from mg_schema import MEMORY_DEFAULTS

    memories = meta.get("memories", [])
    errors = []

    # Check memory_id uniqueness
    mids = [m.get("memory_id") for m in memories if m.get("memory_id")]
    if len(mids) != len(set(mids)):
        dupes = len(mids) - len(set(mids))
        errors.append(f"{dupes} duplicate memory_ids")

    # Check v0.4.5 fields
    missing_fields = 0
    for m in memories:
        for key in MEMORY_DEFAULTS:
            if key not in m:
                missing_fields += 1
    if missing_fields:
        errors.append(f"{missing_fields} missing v0.4.5 fields")

    # Check file_path
    missing_fp = [m for m in memories if not m.get("file_path")]
    if missing_fp:
        errors.append(f"{len(missing_fp)} memories missing file_path")

    # Check files on disk
    missing_files = [
        m.get("memory_id", "?") for m in memories
        if m.get("file_path") and not os.path.exists(os.path.join(workspace, m["file_path"]))
    ]
    if missing_files:
        errors.append(f"{len(missing_files)} memory files missing on disk")

    # Check version
    if meta.get("version") != "0.4.5":
        errors.append(f"Version is {meta.get('version')}, expected 0.4.5")

    if errors:
        print(f"  ❌ {len(errors)} errors:")
        for e in errors:
            print(f"      - {e}")
        return False

    print(f"  ✅ All {len(memories)} memories valid")
    print(f"  ✅ All v0.4.5 fields present")
    print(f"  ✅ All file_paths populated and files exist")
    print(f"  ✅ Version: 0.4.5")
    return True


# Step registry: each step has a minimum version below which it runs
STEPS = [
    ("v0.3-to-v0.4", "0.4.1", step_v03_to_v04),
    ("v0.4-to-v0.4.2", "0.4.2", step_v04_to_v042),
    ("v0.4.2-to-v0.4.5", "0.4.5", step_v042_to_v045),
    ("files", "0.4.5", step_write_files),
    ("verify", "0.4.5", step_verify),
]


def main():
    parser = argparse.ArgumentParser(description="Unified schema migration tool")
    parser.add_argument("--workspace", required=True, help="Workspace root path")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    parser.add_argument("--apply", action="store_true", help="Apply changes and save meta.json")
    parser.add_argument("--step", choices=[s[0] for s in STEPS], help="Run specific step only")
    parser.add_argument("--force", action="store_true", help="Force all steps regardless of version")
    args = parser.parse_args()

    workspace = os.path.abspath(args.workspace)
    meta_path = os.path.join(workspace, "memory", "meta.json")

    if not os.path.exists(meta_path):
        print(f"[ERROR] meta.json not found at {meta_path}")
        print("  Run bootstrap first: python3 memory_guardian.py bootstrap --workspace <path>")
        sys.exit(1)

    meta = load_meta(meta_path)
    current_ver = detect_version(meta)
    print(f"Current version: {current_ver}")
    print(f"Memories: {len(meta.get('memories', []))}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'APPLY' if args.apply else 'INFO'}")

    if args.apply and not args.dry_run:
        # Backup before applying
        bak_path = meta_path + f".v{current_ver}.bak"
        if not os.path.exists(bak_path):
            shutil.copy2(meta_path, bak_path)
            print(f"  ✅ Backup: {bak_path}")

    steps_run = 0
    for step_name, step_ver, step_fn in STEPS:
        if args.step and args.step != step_name:
            continue
        if not args.force and not needs_step(current_ver, step_ver):
            print(f"  ⊘ Skip {step_name} (already at {current_ver})")
            continue

        if args.apply and not args.dry_run:
            step_fn(meta, workspace, dry_run=False)
        else:
            step_fn(meta, workspace, dry_run=True)
        steps_run += 1
        current_ver = step_ver  # Track version progression

    if args.apply and not args.dry_run:
        save_meta(meta_path, meta, use_lock=True)
        print(f"\n✅ Migration complete — meta.json saved")
    elif args.dry_run:
        print(f"\n[DRY-RUN] No changes made. Use --apply to execute.")
    elif steps_run == 0:
        print(f"\n✅ Already at latest version ({current_ver})")


if __name__ == "__main__":
    main()
