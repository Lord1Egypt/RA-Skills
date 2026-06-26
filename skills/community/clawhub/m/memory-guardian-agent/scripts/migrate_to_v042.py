#!/usr/bin/env python3
"""migrate_to_v042.py — v0.4.1 → v0.4.2 migration script.

P0 fixes:
  P0-0. Bootstrap case migration (mem_* → case_* with five-tuple)
  P0-1. Unarchive high-importance memories (imp>=0.8) + pinned marking
  P0-2. MEMORY.md compression + daily note rotation
  P0-3. decay_config persistence + schema_version + quality_gate cleanup

Usage:
  python3 migrate_to_v042.py --workspace /path/to/workspace [--dry-run]
  python3 migrate_to_v042.py --workspace /path/to/workspace --apply

Options:
  --workspace   Workspace root (contains memory/meta.json, MEMORY.md)
  --dry-run     Show what would change without applying
  --apply       Actually apply changes
  --step        Run only a specific step (p0-0, p0-1, p0-2, p0-3)
"""

import argparse
import json
import os
import re
import shutil
import uuid
from datetime import datetime, timedelta, timezone
from mg_utils import read_text_file, save_meta, safe_print

print = safe_print

CST = timezone(timedelta(hours=8))


def now_iso():
    return datetime.now(CST).isoformat()


def load_meta(workspace):
    path = os.path.join(workspace, "memory", "meta.json")
    if not os.path.exists(path):
        print(f"[ERROR] meta.json not found at {path}")
        return None, None
    return json.loads(read_text_file(path)), path


def _save_meta_dry_run(path, meta, dry_run=False):
    """Wrapper around mg_utils.save_meta with dry-run support."""
    if dry_run:
        print(f"  [DRY-RUN] Would save meta.json ({len(json.dumps(meta))} bytes)")
        return
    save_meta(path, meta)
    print(f"  ✅ Saved meta.json")


# ─── P0-0: Bootstrap Case Migration ──────────────────────────

def step_p0_0(meta, dry_run=False):
    """Convert active mem_* memories to case_* five-tuple format.

    Five-tuple: trigger_pattern, action, context, confidence, source
    Plus: case.context preserves "毛刺" (situation context, failure cases, dispute records)
    """
    print("\n" + "=" * 60)
    print("P0-0: Bootstrap Case Migration (mem_* → case_*)")
    print("=" * 60)

    memories = meta.get("memories", [])
    active_mems = [m for m in memories if m.get("status") == "active" and m.get("id", "").startswith("mem_")]
    existing_cases = [m for m in memories if m.get("id", "").startswith("case_")]

    print(f"  Active mem_*: {len(active_mems)}")
    print(f"  Existing case_*: {len(existing_cases)}")

    if not active_mems:
        print("  ℹ️  No active mem_* to migrate.")
        return meta, 0

    migrated = 0
    for mem in active_mems:
        old_id = mem["id"]
        new_id = f"case_{uuid.uuid4().hex[:8]}"

        # Extract trigger_pattern from content heading
        content = mem.get("content", "")
        heading_match = re.match(r"\[(.+?)\]\s*(.*)", content)
        heading = heading_match.group(1) if heading_match else ""
        body = heading_match.group(2) if heading_match else content

        # Generate trigger_pattern from heading + tags
        tags = mem.get("tags", [])
        trigger_pattern = heading
        if "bootstrapped" in tags:
            trigger_pattern = f"bootstrap: {heading}"

        # Build context with "毛刺" preservation
        context_parts = []
        context_parts.append(f"Original source: MEMORY.md section [{heading}]")
        if "daily-note" in tags:
            context_parts.append(f"Extracted from daily note: {body[:200]}")
        # Preserve failure/conflict info if present
        if mem.get("failure_conditions"):
            context_parts.append(f"Known failures: {json.dumps(mem['failure_conditions'])}")
        if mem.get("conflict_refs"):
            context_parts.append(f"Conflicts: {json.dumps(mem['conflict_refs'])}")
        if mem.get("alternatives_considered"):
            context_parts.append(f"Alternatives: {json.dumps(mem['alternatives_considered'])}")

        # Build new case record
        case = {
            "id": new_id,
            "content": content[:2000],  # Keep content for backward compat
            "importance": mem.get("importance", 0.5),
            "entities": mem.get("entities", []),
            "tags": list(tags) + ["migrated", "v0.4.2"],
            "created_at": mem.get("created_at", now_iso()),
            "last_accessed": mem.get("last_accessed", now_iso()),
            "access_count": mem.get("access_count", 0),
            "decay_score": mem.get("decay_score", mem.get("importance", 0.5)),
            "status": "active",
            # Five-tuple
            "trigger_pattern": trigger_pattern,
            "action": body[:300] if body else "",
            "context": "\n".join(context_parts),
            "confidence": mem.get("confidence", 0.5),
            "source": "bootstrap_migration",
            # Case fields
            "case_type": mem.get("case_type", "case"),
            "reversibility": mem.get("reversibility", 1),
            "beta": mem.get("beta", 1.0),
            "trigger_count": mem.get("trigger_count", 0),
            "last_triggered": mem.get("last_triggered"),
            "cooling_threshold": mem.get("cooling_threshold", 5),
            "boundary_words": mem.get("boundary_words", []),
            "conflict_refs": mem.get("conflict_refs", []),
            "failure_conditions": mem.get("failure_conditions", []),
            "failure_count": mem.get("failure_count", 0),
            "last_failure_trigger": mem.get("last_failure_trigger"),
            "last_failure_fix": mem.get("last_failure_fix"),
            "source_case_id": mem.get("source_case_id"),
            "alternatives_considered": mem.get("alternatives_considered", []),
            "cost_factors": mem.get("cost_factors", {"write_cost": 0, "verify_cost": 0, "human_cost": 0, "transfer_cost": 0}),
            "quality_gate": mem.get("quality_gate", {"confidence": 0.5, "gate_mode": "normal", "bypass_reason": None}),
            "importance_explain": mem.get("importance_explain"),
            "security_version": mem.get("security_version", 1),
            "cooldown_active": mem.get("cooldown_active", False),
            "cooldown_until": mem.get("cooldown_until"),
            "observing_since": mem.get("observing_since"),
            "suspended_pending_count": mem.get("suspended_pending_count", 0),
            # v0.4.2 new fields
            "pinned": mem.get("importance", 0) >= 0.9,
            "memory_type": _classify_memory(mem),
            "migration_source": old_id,
            "schema_version": "v0.4.2",
        }

        # Replace old mem with new case
        idx = next((i for i, m in enumerate(memories) if m["id"] == old_id), None)
        if idx is None:
            print(f"  ⚠️  {old_id} not found in memories list, skipping")
            continue
        memories[idx] = case
        migrated += 1
        print(f"  📦 {old_id} → {new_id} (imp={case['importance']:.1f}, type={case['memory_type']})")

    print(f"\n  ✅ Migrated {migrated} memories to case format")
    return meta, migrated


def _classify_memory(mem):
    """Classify memory as static/derive/absorb based on tags, importance, and content.

    - static: 人设/规范/身份/核心规则 (imp>=0.8 or contains rule-identity keywords)
    - derive: 经验/判断/决策/教训 (imp 0.5-0.8, contains experience keywords)
    - absorb: 运行时吸收的信息
    """
    tags = mem.get("tags", [])
    imp = mem.get("importance", 0.5)
    content = (mem.get("content", "") + " " + " ".join(tags)).lower()

    # Static: high importance OR rule/identity keywords
    static_keywords = ["人设", "规范", "规则", "身份", "偏好", "禁止", "安全",
                       "安全约束", "最高优先级", "发帖规范", "格式规则"]
    if imp >= 0.8 or any(kw in content for kw in static_keywords):
        return "static"

    # Derive: medium importance with experience/lesson keywords
    derive_keywords = ["经验", "教训", "修正", "决策", "踩坑", "设计", "架构",
                       "方案", "策略", "发现", "结论"]
    if imp >= 0.5 and any(kw in content for kw in derive_keywords):
        return "derive"

    # Everything else
    return "absorb"


# ─── P0-1: Unarchive High-Importance + Pinned ────────────────

def step_p0_1(meta, dry_run=False):
    """Unarchive high-importance memories (imp>=0.8) and mark pinned.

    Also handles quality_gate_state → quality_gate key migration.
    """
    print("\n" + "=" * 60)
    print("P0-1: Unarchive High-Importance + Pinned Marking")
    print("=" * 60)

    memories = meta.get("memories", [])
    unarchived = 0
    pinned = 0

    for mem in memories:
        # Migrate quality_gate_state → quality_gate
        old_qg = mem.pop("quality_gate_state", None)
        if old_qg and not mem.get("quality_gate"):
            mem["quality_gate"] = old_qg

        # Unarchive high-importance
        if mem.get("status") == "archived" and mem.get("importance", 0) >= 0.8:
            old_status = mem["status"]
            mem["status"] = "active"
            unarchived += 1
            print(f"  📤 Unarchived {mem['id']} (imp={mem['importance']:.1f})")

        # Pin static/high-importance memories
        if mem.get("importance", 0) >= 0.9 and not mem.get("pinned"):
            mem["pinned"] = True
            pinned += 1
            if unarchived == 0:  # Only print if not already printed above
                print(f"  📌 Pinned {mem['id']} (imp={mem['importance']:.1f})")

    # Also migrate top-level quality_gate_state → quality_gate
    old_qg_state = meta.pop("quality_gate_state", None)
    if old_qg_state:
        if "quality_gate" not in meta:
            meta["quality_gate"] = old_qg_state
        print(f"  🔄 Migrated quality_gate_state → quality_gate (top-level)")

    print(f"\n  ✅ Unarchived: {unarchived}, Pinned: {pinned}")
    return meta


# ─── P0-2: Daily Note Rotation ───────────────────────────────

def step_p0_2(meta, dry_run=False):
    """Rotate oversized daily notes (>30KB → archive/summary).

    Only rotates, does not modify MEMORY.md (that's compact.py's job).
    """
    print("\n" + "=" * 60)
    print("P0-2: Daily Note Rotation (>30KB)")
    print("=" * 60)

    # Use workspace path for memory_dir (meta["_path"] is set by main() but its dirname
    # would give workspace/memory, and joining with "memory" would double-nest)
    workspace = meta.get("_workspace", ".")
    memory_dir = os.path.join(workspace, "memory")

    if not os.path.exists(memory_dir):
        print(f"  ℹ️  Memory dir not found: {memory_dir}")
        return meta

    archive_dir = os.path.join(memory_dir, "archive")
    rotated = 0

    for fname in sorted(os.listdir(memory_dir)):
        if not re.match(r"\d{4}-\d{2}-\d{2}\.md$", fname):
            continue
        fpath = os.path.join(memory_dir, fname)
        size = os.path.getsize(fpath)
        if size < 30 * 1024:  # 30KB
            continue

        print(f"  📄 {fname}: {size // 1024}KB — needs rotation")

        if dry_run:
            print(f"    [DRY-RUN] Would archive to {archive_dir}/{fname}")
            rotated += 1
            continue

        os.makedirs(archive_dir, exist_ok=True)

        # Generate summary (first 50 lines + header)
        lines = read_text_file(fpath).splitlines(keepends=True)

        summary_lines = lines[:50]
        summary_lines.append(f"\n---\n[Archived {now_iso()}, original {len(lines)} lines, {size // 1024}KB]\n")

        # Move original to archive
        archive_path = os.path.join(archive_dir, fname)
        counter = 1
        while os.path.exists(archive_path):
            archive_path = os.path.join(archive_dir, f"{fname}.{counter}")
            counter += 1
        shutil.move(fpath, archive_path)

        # Write summary
        with open(fpath, "w", encoding="utf-8") as f:
            f.writelines(summary_lines)

        print(f"    📦 Archived → {os.path.basename(archive_path)}")
        print(f"    📝 Summary: {len(summary_lines)} lines")
        rotated += 1

    if rotated == 0:
        print("  ✅ No oversized daily notes found.")
    else:
        print(f"\n  ✅ Rotated {rotated} daily notes")
    return meta


# ─── P0-3: decay_config Persistence + Schema ─────────────────

def step_p0_3(meta, dry_run=False):
    """Persist decay_config defaults + set schema_version.

    Default decay_config:
    - alpha: 2.0
    - beta_cap: 3.0
    - queue_cap: 20
    - queue_timeout_min: 30
    - quiet_period_days: 30
    - median_discount: 0.7 (neuro, configurable)
    - iqr_multiplier: 1.5 (neuro, per-rule adaptive)
    - min_sample: 5 (neuro)
    - cold_start_exempt_trigger_count: 5 (neuro)
    - static_beta_max: 1.0 (ovea)
    - derive_beta_default: 2.0 (ovea)
    - absorb_beta_default: 3.0 (ovea)
    """
    print("\n" + "=" * 60)
    print("P0-3: decay_config Persistence + Schema Version")
    print("=" * 60)

    changes = []

    # Set schema_version
    if not meta.get("schema_version"):
        meta["schema_version"] = "v0.4.2"
        changes.append("schema_version: v0.4.2")
    elif meta.get("schema_version") != "v0.4.2":
        old = meta["schema_version"]
        meta["schema_version"] = "v0.4.2"
        changes.append(f"schema_version: {old} → v0.4.2")

    # Update version
    if meta.get("version") != "0.4.2":
        old = meta.get("version", "unknown")
        meta["version"] = "0.4.2"
        changes.append(f"version: {old} → 0.4.2")

    # Persist decay_config
    default_decay_config = {
        "alpha": 2.0,
        "beta_cap": 3.0,
        "queue_cap": 20,
        "queue_timeout_min": 30,
        "quiet_period_days": 30,
        # v0.4.2 new params (from community discussion)
        "median_discount": 0.7,  # neuro: 待实测校准
        "iqr_multiplier": 1.5,  # neuro: per-rule adaptive IQR threshold
        "min_sample": 5,  # neuro: min samples for stability calculation
        "cold_start_exempt_trigger_count": 5,  # neuro: exempt if trigger_count < N
        "static_beta_max": 1.0,  # ovea: static memories barely decay
        "derive_beta_default": 2.0,  # ovea: normal decay
        "absorb_beta_default": 3.0,  # ovea: fast decay
        # Provenance (SimonClaw)
        "provenance_auth_base": 0.6,
        "provenance_auth_mult": 1.0,
        "provenance_nonauth_base": 0.4,
        "provenance_nonauth_mult": 0.7,
        "provenance_verify_step": 0.1,
        "provenance_verify_cap": 0.3,
        # Confidence thresholds (maste)
        "confidence_warn_static": 0.5,
        "confidence_warn_derive": 0.3,
        "confidence_warn_absorb": 0.5,
        # Anomaly detection (maste)
        "anomaly_mode_enabled": True,  # 3-state: normal→anomaly→recovery
        "event_annotation_threshold": 0.15,  # maste: ±0.15
        "case_verify_min_hits": 3,  # maste: 3 hits + 1 feedback
    }

    if not meta.get("decay_config"):
        meta["decay_config"] = default_decay_config
        changes.append(f"decay_config: initialized with {len(default_decay_config)} params")
    else:
        # Merge: add missing keys, don't overwrite existing user values
        existing = meta["decay_config"]
        added = []
        for k, v in default_decay_config.items():
            if k not in existing:
                existing[k] = v
                added.append(k)
        if added:
            changes.append(f"decay_config: added {len(added)} new params: {', '.join(added[:5])}{'...' if len(added) > 5 else ''}")

    # Migrate quality_gate_state → quality_gate (top-level)
    old_qg_state = meta.get("quality_gate_state")
    if old_qg_state and not meta.get("quality_gate"):
        meta["quality_gate"] = old_qg_state
        del meta["quality_gate_state"]
        changes.append("quality_gate_state → quality_gate (migrated)")

    # Also ensure quality_gate exists
    if "quality_gate" not in meta:
        meta["quality_gate"] = {
            "state": "NORMAL",
            "anomaly_count": 0,
            "consecutive_clean": 0,
            "total_writes": 0,
            "total_failures": 0,
            "failure_rate": 0.0,
        }
        changes.append("quality_gate: initialized (NORMAL)")

    for c in changes:
        print(f"  🔄 {c}")

    if not changes:
        print("  ✅ Already up to date.")
    else:
        print(f"\n  ✅ {len(changes)} changes applied")
    return meta


# ─── Main ────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="migrate v0.4.1 → v0.4.2")
    parser.add_argument("--workspace", default=os.path.expanduser("~/workspace/agent/workspace"),
                        help="Workspace root directory")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without applying")
    parser.add_argument("--apply", action="store_true", help="Apply changes")
    parser.add_argument("--step", default=None,
                        choices=["p0-0", "p0-1", "p0-2", "p0-3"],
                        help="Run only a specific step")
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print("⚠️  Neither --dry-run nor --apply specified. Defaulting to --dry-run.")
        args.dry_run = True

    mode = "DRY-RUN" if args.dry_run else "APPLY"
    print(f"{'=' * 60}")
    print(f"v0.4.1 → v0.4.2 Migration [{mode}]")
    print(f"  Workspace: {args.workspace}")
    print(f"  Time: {now_iso()}")
    print(f"{'=' * 60}")

    # Load meta
    meta, meta_path = load_meta(args.workspace)
    if meta is None:
        print("Cannot proceed without meta.json")
        return

    # Store paths for P0-2
    meta["_path"] = meta_path
    meta["_workspace"] = args.workspace

    # Run steps
    steps = {
        "p0-0": lambda: step_p0_0(meta, args.dry_run),
        "p0-1": lambda: step_p0_1(meta, args.dry_run),
        "p0-2": lambda: step_p0_2(meta, args.dry_run),
        "p0-3": lambda: step_p0_3(meta, args.dry_run),
    }

    try:
        if args.step:
            steps[args.step]()
        else:
            # P0-3 first (safest, just adds fields)
            step_p0_3(meta, args.dry_run)
            # P0-1 next (unarchive + pin)
            step_p0_1(meta, args.dry_run)
            # P0-0 (case migration)
            step_p0_0(meta, args.dry_run)
            # P0-2 last (daily note rotation)
            step_p0_2(meta, args.dry_run)
    finally:
        # Always cleanup temp fields (even on exception)
        meta.pop("_path", None)
        meta.pop("_workspace", None)

    # Save
    if not args.step or args.step in ("p0-0", "p0-1", "p0-3"):
        _save_meta_dry_run(meta_path, meta, args.dry_run)

    print(f"\n{'=' * 60}")
    print(f"Migration complete [{mode}]")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
