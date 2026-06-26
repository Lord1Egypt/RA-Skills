#!/usr/bin/env python3
"""memory-guardian: Case versioning & rollback module (v0.4.1).

Implements version tracking for case entries in meta.json:
  - Version chain: case_v1 (deprecated) ← case_v2 (active) ← case_v3 (active)
  - Rollback: mark current deprecated, activate previous version
  - Deprecation: auto-archive after 30 days
  - Failure signals: override_count, feature_drift, coldness_days
  - Deprecated sweep: auto-archive expired deprecated cases

Usage:
  python3 memory_case_rollback.py status [--workspace <path>]
  python3 memory_case_rollback.py history <case_id> [--workspace <path>]
  python3 memory_case_rollback.py rollback <case_id> [--reason "..."] [--workspace <path>]
  python3 memory_case_rollback.py promote <case_id> [--workspace <path>]
  python3 memory_case_rollback.py sweep [--workspace <path>] [--dry-run]
  python3 memory_case_rollback.py signals [--workspace <path>]
"""
import json, os, argparse, sys, copy
from datetime import datetime
from mg_utils import _now_iso, CST, load_meta, save_meta
from mg_events.telemetry import record_module_run

# ─── Versioning Parameters ──────────────────────────────────
DEPRECATED_RETENTION_DAYS = 30     # auto-archive after this many days
FAILURE_RATE_ROLLBACK = 0.2        # failure_rate threshold for auto-rollback suggestion
MIN_OVERRIDE_FOR_SIGNAL = 3        # consecutive overrides before flagging drift
COLDNESS_DRIFT_DAYS = 60           # days without match hit before flagging cold
DRIFT_DISTANCE_THRESHOLD = 0.5     # average match distance above which = feature drift



def _days_since(iso_str):
    if not iso_str:
        return float('inf')
    try:
        dt = datetime.fromisoformat(iso_str)
        return (datetime.now(CST) - dt).total_seconds() / 86400
    except (ValueError, TypeError):
        return float('inf')


def _find_case(meta, case_id):
    """Find a case by ID — exact match first, then prefix match with warning."""
    import logging
    # Exact match first
    for mem in meta.get("memories", []):
        if mem.get("id") == case_id:
            return mem
    # Fallback to prefix match (with warning)
    for mem in meta.get("memories", []):
        if mem.get("id", "").startswith(case_id):
            logging.warning(f"No exact match for {case_id}, falling back to prefix match → {mem.get('id')}")
            return mem
    return None


def _find_all_versions(meta, case_id):
    """Walk version chain to find all versions of a case (oldest first)."""
    chain = []
    current = _find_case(meta, case_id)
    if not current:
        return chain

    # Walk backwards through prev_version links
    visited = set()
    MAX_VERSION_DEPTH = 50  # safety limit against corrupted/tampered chains
    while current and current.get("id") not in visited:
        visited.add(current.get("id"))
        chain.append(current)
        if len(chain) >= MAX_VERSION_DEPTH:
            # Truncate to prevent unbounded traversal
            break
        prev = current.get("prev_version")
        if prev:
            current = _find_case(meta, prev)
        else:
            break

    chain.reverse()  # oldest first
    return chain


def create_version_entry(meta, original_case, updated_fields, workspace=None):
    """Create a new version of an existing case.

    The original is marked deprecated, the new entry becomes active.
    Both share the same 'version_group' for chain tracking.

    Returns: (new_case_dict, error_msg)
    """
    import uuid

    now = _now_iso()
    version = original_case.get("version", 1) + 1
    version_group = original_case.get("version_group", original_case.get("id"))

    # Mark original as deprecated
    original_case["deprecated"] = True
    original_case["deprecated_at"] = now
    original_case["deprecated_reason"] = f"superseded by v{version}"

    # Create new version entry
    new_id = f"case_{uuid.uuid4().hex[:8]}"
    new_case = copy.deepcopy(original_case)  # deep copy to isolate nested objects
    new_case["id"] = new_id
    new_case["version"] = version
    new_case["prev_version"] = original_case.get("id")
    new_case["version_group"] = version_group
    new_case["deprecated"] = False
    new_case["deprecated_at"] = None
    new_case["deprecated_reason"] = None
    new_case["created_at"] = now
    new_case["updated_at"] = now

    # Apply updated fields
    for key, value in updated_fields.items():
        if value is not None:
            new_case[key] = value

    # Reset version-specific counters
    new_case["failure_count"] = 0
    new_case["consecutive_overrides"] = 0
    new_case["feature_drift_score"] = 0.0

    # Unconditionally reset failure_signals to defaults
    new_case["failure_signals"] = {
        "consecutive_overrides": 0,
        "feature_drift_score": 0.0,
        "coldness_days": 0,
        "last_match_distance": None,
        "last_matched_at": None,
    }

    # v0.4.5 fix: update file_path and memory_id to match new id
    new_mid = new_case.get("memory_id", "")
    old_fp = new_case.get("file_path", "")
    if old_fp and workspace:
        tags = new_case.get("tags", [])
        try:
            from mg_utils import derive_file_path
            new_fp = derive_file_path(new_id, tags, new_case.get("content", ""))
            new_case["file_path"] = new_fp
            # Generate new memory_id based on new id
            from mg_utils import generate_memory_id
            existing_ids = {m.get("memory_id") or m.get("id") for m in meta.get("memories", []) if m.get("memory_id") or m.get("id")}
            new_case["memory_id"] = generate_memory_id(new_case.get("content", ""), existing_ids=existing_ids)
            # Write file to new path
            from memory_ingest import _write_memory_file
            _write_memory_file(new_case["memory_id"], new_case.get("content", ""), new_fp, workspace=workspace)
        except Exception:
            import logging
            logging.warning("create_version_entry: failed to update file for %s", new_id, exc_info=True)

    meta["memories"].append(new_case)
    return new_case, None


def rollback_case(meta, case_id, reason=""):
    """Rollback a case to its previous version.

    Returns: (rolled_back:bool, message:str, chain:list)
    """
    current = _find_case(meta, case_id)
    if not current:
        return False, f"Case not found: {case_id}", []

    chain = _find_all_versions(meta, case_id)
    if len(chain) < 2:
        return False, "No previous version to rollback to", chain

    prev = chain[-2]  # second-to-last in the chain

    now = _now_iso()

    # Mark current as deprecated
    current["deprecated"] = True
    current["deprecated_at"] = now
    current["deprecated_reason"] = reason or f"rolled back to {prev.get('id')}"

    # Activate previous version
    prev["deprecated"] = False
    prev["deprecated_at"] = None
    prev["deprecated_reason"] = None
    prev["reactivated_at"] = now
    prev["reactivated_reason"] = reason or f"rollback from {current.get('id')}"

    # Record rollback in chain log
    if "version_log" not in prev:
        prev["version_log"] = []
    prev["version_log"].append({
        "action": "rollback",
        "from_version": current.get("version"),
        "to_version": prev.get("version"),
        "timestamp": now,
        "reason": reason,
    })

    return True, f"Rolled back {current.get('id')} (v{current.get('version')}) → {prev.get('id')} (v{prev.get('version')})", chain


def compute_failure_signals(meta, case_id):
    """Compute failure signals for a case.

    Returns: dict with signals or None if case not found.
    """
    case = _find_case(meta, case_id)
    if not case:
        return None

    signals = case.get("failure_signals", {
        "consecutive_overrides": 0,
        "feature_drift_score": 0.0,
        "coldness_days": 0,
        "last_match_distance": None,
        "last_matched_at": None,
    })

    # Coldness: days since last match
    if signals.get("last_matched_at"):
        signals["coldness_days"] = round(_days_since(signals["last_matched_at"]), 1)
    else:
        signals["coldness_days"] = _days_since(case.get("created_at", ""))

    # Failure rate from quality gate
    fc = case.get("failure_count", 0)
    tc = case.get("trigger_count", 0)
    signals["failure_rate"] = round(fc / max(tc, 1), 4)

    # Suggestion
    suggestions = []
    if signals.get("consecutive_overrides", 0) >= MIN_OVERRIDE_FOR_SIGNAL:
        suggestions.append(f"⚠️ High override count ({signals['consecutive_overrides']})")
    if signals.get("feature_drift_score", 0) > DRIFT_DISTANCE_THRESHOLD:
        suggestions.append(f"⚠️ Feature drift ({signals['feature_drift_score']:.2f} > {DRIFT_DISTANCE_THRESHOLD})")
    if signals.get("coldness_days", 0) > COLDNESS_DRIFT_DAYS:
        suggestions.append(f"⚠️ Cold case ({signals['coldness_days']:.0f} days without match)")
    if signals.get("failure_rate", 0) > FAILURE_RATE_ROLLBACK:
        suggestions.append(f"⚠️ High failure rate ({signals['failure_rate']:.1%}) — consider rollback")
    signals["suggestions"] = suggestions

    return signals


def sweep_deprecated(meta, dry_run=False, meta_path=None):
    """Find and archive deprecated cases past retention period.

    Returns: list of archived case IDs.
    """
    archived = []
    now = _now_iso()

    for mem in meta.get("memories", []):
        if not mem.get("deprecated"):
            continue

        days_deprecated = _days_since(mem.get("deprecated_at"))
        if days_deprecated > DEPRECATED_RETENTION_DAYS:
            if dry_run:
                archived.append({
                    "id": mem.get("id"),
                    "version": mem.get("version"),
                    "days_deprecated": round(days_deprecated),
                })
            else:
                mem["status"] = "archived"
                mem["archived_at"] = now
                mem["archived_reason"] = f"deprecated for {days_deprecated:.0f} days (>{DEPRECATED_RETENTION_DAYS})"
                archived.append({
                    "id": mem.get("id"),
                    "version": mem.get("version"),
                    "days_deprecated": round(days_deprecated),
                })

    if archived and not dry_run and meta_path:
        save_meta(meta_path, meta)

    return archived


# ─── CLI Commands ────────────────────────────────────────────

def cmd_status(meta_path, workspace):
    """Show versioning status overview."""
    meta = load_meta(meta_path)
    memories = meta.get("memories", [])

    total_cases = [m for m in memories if m.get("case_type") == "case"]
    versioned = [m for m in total_cases if m.get("version", 1) > 1]
    deprecated = [m for m in total_cases if m.get("deprecated")]
    active = [m for m in total_cases if not m.get("deprecated") and m.get("status") in ("active", "observing")]

    # Version groups
    groups = {}
    for m in total_cases:
        vg = m.get("version_group", m.get("id"))
        groups.setdefault(vg, []).append(m)

    multi_version_groups = {k: v for k, v in groups.items() if len(v) > 1}

    print(f"📋 Case Versioning Status")
    print(f"  Total cases: {len(total_cases)}")
    print(f"  Active: {len(active)}")
    print(f"  Versioned (v>1): {len(versioned)}")
    print(f"  Deprecated: {len(deprecated)}")
    print(f"  Version groups with history: {len(multi_version_groups)}")
    print()

    if multi_version_groups:
        print(f"  📊 Version Groups:")
        for vg_id, cases in sorted(multi_version_groups.items()):
            versions = sorted(cases, key=lambda c: c.get("version", 1))
            v_str = " → ".join(
                f"v{c.get('version','?')}{'❌' if c.get('deprecated') else '✅'}"
                for c in versions
            )
            print(f"    {vg_id[:16]}: {v_str}")

    if deprecated:
        print(f"\n  🗑️ Deprecated cases:")
        for d in deprecated:
            days = _days_since(d.get("deprecated_at"))
            remaining = max(0, DEPRECATED_RETENTION_DAYS - days)
            print(f"    {d.get('id')} v{d.get('version')} — deprecated {days:.0f}d ago — archive in {remaining:.0f}d")


def cmd_history(meta_path, workspace, case_id):
    """Show version history for a case."""
    meta = load_meta(meta_path)
    chain = _find_all_versions(meta, case_id)

    if not chain:
        print(f"Case not found: {case_id}")
        return

    print(f"📜 Version History: {chain[-1].get('id')} (group: {chain[-1].get('version_group', 'N/A')[:16]})")
    print()

    for c in chain:
        v = c.get("version", 1)
        status = "✅ active" if not c.get("deprecated") else "❌ deprecated"
        created = (c.get("created_at", "") or "")[:16]
        content_preview = (c.get("content", "") or "")[:80].replace("\n", " ")
        confidence = c.get("confidence", "?")
        print(f"  v{v} [{c.get('id')}] {status}")
        print(f"     Created: {created}  Confidence: {confidence}")
        print(f"     Content: {content_preview}")
        if c.get("deprecated_reason"):
            print(f"     Deprecated: {c['deprecated_reason']}")
        if c.get("reactivated_reason"):
            print(f"     Reactivated: {c['reactivated_reason']}")
        # Version log
        for log in c.get("version_log", []):
            ts = log.get("timestamp", "")[:16]
            print(f"     📋 [{ts}] {log.get('action')}: {log.get('reason', '')[:60]}")
        print()


def cmd_rollback(meta_path, workspace, case_id, reason):
    """Rollback a case to its previous version."""
    meta = load_meta(meta_path)
    success, message, chain = rollback_case(meta, case_id, reason=reason)

    if success:
        save_meta(meta_path, meta)
        print(f"🔄 {message}")
        if reason:
            print(f"  Reason: {reason}")
        print(f"\n  Version chain after rollback:")
        for c in chain:
            v = c.get("version", 1)
            status = "✅" if not c.get("deprecated") else "❌"
            print(f"    {status} v{v} {c.get('id')}")
    else:
        print(f"❌ {message}")


def cmd_promote(meta_path, workspace, case_id):
    """Create a new version of a case (interactive — prints the new version info)."""
    meta = load_meta(meta_path)
    case = _find_case(meta, case_id)

    if not case:
        print(f"Case not found: {case_id}")
        return

    if case.get("deprecated"):
        print(f"⚠️ Case {case_id} is deprecated. Reactivate or create from its latest active version.")
        return

    print(f"📦 Promoting case {case_id} to new version...")
    print(f"  Current version: v{case.get('version', 1)}")
    print(f"  Use memory_case_grow.py merge or memory_ingest.py --update to create the new version")
    print(f"  Then call create_version_entry() from code to link versions.")
    print()
    print(f"  Alternatively, use rollback to go back to a previous version.")


def cmd_sweep(meta_path, workspace, dry_run):
    """Sweep deprecated cases past retention period."""
    meta = load_meta(meta_path)
    archived = sweep_deprecated(meta, dry_run=dry_run, meta_path=meta_path)

    if not archived:
        print(f"🧹 No deprecated cases to archive (retention: {DEPRECATED_RETENTION_DAYS}d)")
        return

    mode = "[DRY RUN] " if dry_run else ""
    print(f"🧹 {mode}Archived {len(archived)} deprecated cases:")
    for a in archived:
        print(f"  🗑️ {a['id']} v{a['version']} — deprecated for {a['days_deprecated']:.0f}d")


def cmd_signals(meta_path, workspace):
    """Compute and display failure signals for all active cases."""
    meta = load_meta(meta_path)
    cases = [m for m in meta.get("memories", [])
             if m.get("case_type") == "case" and not m.get("deprecated")
             and m.get("status") in ("active", "observing")]

    if not cases:
        print("No active cases found.")
        return

    print(f"📡 Failure Signals for {len(cases)} active cases")
    print()

    any_suggestions = False
    for c in cases:
        signals = compute_failure_signals(meta, c.get("id"))
        if not signals:
            continue

        suggestions = signals.get("suggestions", [])
        if not suggestions:
            continue

        any_suggestions = True
        print(f"  ⚠️ {c.get('id')} (v{c.get('version', 1)})")
        for s in suggestions:
            print(f"     {s}")
        print()

    if not any_suggestions:
        print(f"  ✅ All cases healthy — no failure signals detected")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="memory-guardian case versioning & rollback (v0.4.1)")
    p.add_argument("command", choices=["status", "history", "rollback", "promote", "sweep", "signals"],
                   help="Command")
    p.add_argument("case_id", nargs="?", default=None, help="Case ID (for history/rollback/promote)")
    p.add_argument("--workspace", default=None, help="Workspace root path")
    p.add_argument("--meta", default=None, help="Path to meta.json")
    p.add_argument("--reason", default="", help="Reason for rollback")
    p.add_argument("--dry-run", action="store_true", help="Show results without applying (for sweep)")
    args = p.parse_args()

    workspace = args.workspace or os.environ.get(
        "OPENCLAW_WORKSPACE", os.path.expanduser("~/workspace/agent/workspace")
    )
    meta_path = args.meta or os.path.join(workspace, "memory", "meta.json")
    telemetry_meta = load_meta(meta_path) if os.path.exists(meta_path) else {"memories": []}
    telemetry_input_count = sum(
        1
        for mem in telemetry_meta.get("memories", [])
        if mem.get("id", "").startswith("case_") or mem.get("case_type") == "case"
    )

    if args.command == "status":
        cmd_status(meta_path, workspace)
    elif args.command == "history":
        if not args.case_id:
            print("Error: case_id required for history command")
            sys.exit(1)
        cmd_history(meta_path, workspace, args.case_id)
    elif args.command == "rollback":
        if not args.case_id:
            print("Error: case_id required for rollback command")
            sys.exit(1)
        cmd_rollback(meta_path, workspace, args.case_id, args.reason)
    elif args.command == "promote":
        if not args.case_id:
            print("Error: case_id required for promote command")
            sys.exit(1)
        cmd_promote(meta_path, workspace, args.case_id)
    elif args.command == "sweep":
        cmd_sweep(meta_path, workspace, args.dry_run)
    elif args.command == "signals":
        cmd_signals(meta_path, workspace)

    record_module_run(
        workspace,
        "case_rollback",
        input_count=telemetry_input_count,
        output_count=telemetry_input_count,
    )
