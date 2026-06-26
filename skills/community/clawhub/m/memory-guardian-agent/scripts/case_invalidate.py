#!/usr/bin/env python3
"""case_invalidate.py — Case 无效化机制 (v0.4.2 P1-2).

Design by lingxi_agent + azha0.

When a case's confidence drops below 0.2 for 3 consecutive evaluations:
  1. Mark as "frozen" (stop matching/triggers)
  2. Add to review queue for human inspection
  3. Human can: unfreeze (reset confidence), archive, or delete

Usage:
  python3 case_invalidate.py status --workspace /path
  python3 case_invalidate.py check --workspace /path [--dry-run]
  python3 case_invalidate.py review --workspace /path
  python3 case_invalidate.py unfreeze <id> --workspace /path [--new-confidence 0.5]
  python3 case_invalidate.py archive <id> --workspace /path
  python3 case_invalidate.py delete <id> --workspace /path
"""

import argparse
import json
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from mg_utils import load_meta, save_meta, _now_iso, CST


# ─── Constants ────────────────────────────────────────────────

INVALIDATION_CONFIDENCE_THRESHOLD = 0.2   # Below this = low confidence
INVALIDATION_CONSECUTIVE_N = 3             # Consecutive evaluations below threshold
INVALIDATION_COOLDOWN_DAYS = 7             # Min days between invalidation checks per case
MAX_FROZEN = 20                             # Max frozen cases before auto-archive oldest


# ─── Core Functions ───────────────────────────────────────────

def check_invalidations(meta_path, dry_run=False):
    """Check all active cases for invalidation criteria.

    A case is invalidated when:
    - confidence < 0.2 for 3 consecutive evaluations
    - OR failure_count >= 5 AND confidence < 0.4

    Args:
        meta_path: str
        dry_run: bool

    Returns:
        dict: {frozen: int, reviewed: int, details: [...]}
    """
    now = _now_iso()
    now_dt = datetime.now(CST)
    meta = load_meta(meta_path)
    memories = meta.get("memories", [])

    frozen = 0
    reviewed = 0
    details = []
    meta_changed = False

    for mem in memories:
        if mem.get("status") not in ("active", "observing"):
            continue

        conf = mem.get("confidence", 0.5)
        failure_count = mem.get("failure_count", 0)

        # Get consecutive low-confidence count
        consec = mem.get("consecutive_low_confidence", 0)
        last_check = mem.get("last_invalidation_check")

        # Cooldown: skip if checked recently
        if last_check:
            try:
                last_dt = datetime.fromisoformat(last_check)
                elapsed_days = (now_dt - last_dt).total_seconds() / 86400
                if elapsed_days < INVALIDATION_COOLDOWN_DAYS:
                    continue
            except (ValueError, TypeError):
                pass

        reviewed += 1

        # Check criteria
        should_freeze = False
        reason = None

        if conf < INVALIDATION_CONFIDENCE_THRESHOLD:
            consec += 1
            mem["consecutive_low_confidence"] = consec
            mem["last_invalidation_check"] = now

            if consec >= INVALIDATION_CONSECUTIVE_N:
                should_freeze = True
                reason = f"confidence {conf:.2f} < 0.2 for {consec} consecutive evaluations"
            elif not dry_run:
                meta_changed = True
        else:
            # Reset counter on good confidence
            mem["consecutive_low_confidence"] = 0
            mem["last_invalidation_check"] = now
            if not dry_run:
                meta_changed = True

        # Secondary: high failure count + low confidence
        if not should_freeze and failure_count >= 5 and conf < 0.4:
            should_freeze = True
            reason = f"failure_count {failure_count} >= 5 AND confidence {conf:.2f} < 0.4"

        if should_freeze:
            if not dry_run:
                meta_changed = True
                mem["status"] = "frozen"
                mem["frozen_at"] = now
                mem["frozen_reason"] = reason
                mem["frozen_consecutive_low"] = consec
                mem["consecutive_low_confidence"] = 0

                # Add to review queue
                meta.setdefault("case_review_queue", []).append({
                    "case_id": mem["id"],
                    "frozen_at": now,
                    "reason": reason,
                    "confidence_at_freeze": conf,
                    "status": "pending_review",
                })

                # Cap frozen cases
                _cap_frozen(meta)

            frozen += 1
            details.append({"id": mem["id"], "reason": reason, "confidence": conf})

    if not dry_run and meta_changed:
        save_meta(meta_path, meta)

    return {
        "frozen": frozen,
        "reviewed": reviewed,
        "dry_run": dry_run,
        "details": details,
    }


def get_review_queue(meta_path):
    """Get all cases pending human review.

    Returns:
        list: review queue entries
    """
    meta = load_meta(meta_path)
    return [r for r in meta.get("case_review_queue", []) if r["status"] == "pending_review"]


def unfreeze(meta_path, case_id, new_confidence=0.5):
    """Unfreeze a frozen case with reset confidence.

    Args:
        meta_path: str
        case_id: str
        new_confidence: float, reset confidence to this value

    Returns:
        dict: result
    """
    now = _now_iso()
    meta = load_meta(meta_path)
    mem = _find_memory(meta, case_id)
    if not mem:
        return {"status": "not_found", "id": case_id}

    if mem.get("status") != "frozen":
        return {"status": "not_frozen", "id": case_id, "current_status": mem.get("status")}

    mem["status"] = "active"
    mem["confidence"] = new_confidence
    mem["consecutive_low_confidence"] = 0
    mem["unfrozen_at"] = now
    mem["unfreeze_note"] = f"Unfrozen by owner, confidence reset to {new_confidence}"

    # Update review queue
    for r in meta.get("case_review_queue", []):
        if r["case_id"] == case_id and r["status"] == "pending_review":
            r["status"] = "unfrozen"
            r["resolved_at"] = now
            r["action"] = "unfreeze"
            r["new_confidence"] = new_confidence
            break

    save_meta(meta_path, meta)
    return {"status": "unfrozen", "id": case_id, "new_confidence": new_confidence}


def archive_case(meta_path, case_id):
    """Archive a frozen case after review.

    Args:
        meta_path: str
        case_id: str

    Returns:
        dict: result
    """
    now = _now_iso()
    meta = load_meta(meta_path)
    mem = _find_memory(meta, case_id)
    if not mem:
        return {"status": "not_found", "id": case_id}

    mem["status"] = "archived"
    mem["archived_at"] = now
    mem["archive_reason"] = "frozen_case_reviewed:archived"

    for r in meta.get("case_review_queue", []):
        if r["case_id"] == case_id and r["status"] == "pending_review":
            r["status"] = "archived"
            r["resolved_at"] = now
            r["action"] = "archive"
            break

    save_meta(meta_path, meta)
    return {"status": "archived", "id": case_id}


def delete_case(meta_path, case_id):
    """Permanently delete a frozen case.

    Args:
        meta_path: str
        case_id: str

    Returns:
        dict: result
    """
    now = _now_iso()
    meta = load_meta(meta_path)
    mem = _find_memory(meta, case_id)
    if not mem:
        return {"status": "not_found", "id": case_id}

    # Mark as deleted (soft delete)
    mem["status"] = "deleted"
    mem["deleted_at"] = now
    mem["delete_reason"] = "frozen_case_reviewed:deleted"

    for r in meta.get("case_review_queue", []):
        if r["case_id"] == case_id and r["status"] == "pending_review":
            r["status"] = "deleted"
            r["resolved_at"] = now
            r["action"] = "delete"
            break

    save_meta(meta_path, meta)
    return {"status": "deleted", "id": case_id}


def get_status(meta_path):
    """Get case invalidation system status.

    Returns:
        dict: status summary
    """
    meta = load_meta(meta_path)
    memories = meta.get("memories", [])

    by_status = {}
    low_conf_count = 0
    frozen_count = 0

    for mem in memories:
        s = mem.get("status", "unknown")
        by_status[s] = by_status.get(s, 0) + 1
        if mem.get("confidence", 0.5) < 0.3:
            low_conf_count += 1
        if s == "frozen":
            frozen_count += 1

    review_queue = [r for r in meta.get("case_review_queue", []) if r["status"] == "pending_review"]

    return {
        "total": len(memories),
        "by_status": by_status,
        "low_confidence_count": low_conf_count,
        "frozen_count": frozen_count,
        "review_queue_size": len(review_queue),
        "review_queue": review_queue[:10],  # Show top 10
        "config": {
            "confidence_threshold": INVALIDATION_CONFIDENCE_THRESHOLD,
            "consecutive_n": INVALIDATION_CONSECUTIVE_N,
            "cooldown_days": INVALIDATION_COOLDOWN_DAYS,
            "max_frozen": MAX_FROZEN,
        },
    }


# ─── Internal ─────────────────────────────────────────────────

def _find_memory(meta, mem_id):
    for mem in meta.get("memories", []):
        if mem.get("id") == mem_id:
            return mem
    return None


def _cap_frozen(meta):
    """Auto-archive oldest frozen cases if over max_frozen limit."""
    frozen = [m for m in meta["memories"] if m.get("status") == "frozen"]
    while len(frozen) > MAX_FROZEN:
        oldest = min(frozen, key=lambda m: m.get("frozen_at", ""))
        oldest["status"] = "archived"
        oldest["archived_at"] = _now_iso()
        oldest["archive_reason"] = "max_frozen_exceeded"
        # Sync review queue to reflect archived status
        for r in meta.get("case_review_queue", []):
            if r.get("case_id") == oldest["id"] and r.get("status") == "pending_review":
                r["status"] = "archived"
                r["resolved_at"] = _now_iso()
                r["action"] = "auto_archive"
                break
        frozen.remove(oldest)


# ─── CLI ─────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="Case 无效化机制 v0.4.2")
    p.add_argument("--workspace", default=os.path.expanduser("~/workspace/agent/workspace"))
    p.add_argument("command",
                   choices=["status", "check", "review", "unfreeze", "archive", "delete"],
                   help="Command")
    p.add_argument("case_id", nargs="?", default=None, help="Case ID (for unfreeze/archive/delete)")
    p.add_argument("--new-confidence", type=float, default=0.5, help="Reset confidence (for unfreeze)")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    meta_path = os.path.join(args.workspace, "memory", "meta.json")

    if args.command == "status":
        result = get_status(meta_path)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif args.command == "check":
        result = check_invalidations(meta_path, args.dry_run)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif args.command == "review":
        queue = get_review_queue(meta_path)
        if not queue:
            print("No cases pending review.")
        else:
            for r in queue:
                print(f"  {r['case_id']} | frozen: {r['frozen_at'][:16]} | conf: {r['confidence_at_freeze']:.2f}")
                print(f"    Reason: {r['reason'][:80]}")

    elif args.command == "unfreeze":
        if not args.case_id:
            print("Error: case_id required")
            sys.exit(1)
        result = unfreeze(meta_path, args.case_id, args.new_confidence)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif args.command == "archive":
        if not args.case_id:
            print("Error: case_id required")
            sys.exit(1)
        result = archive_case(meta_path, args.case_id)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif args.command == "delete":
        if not args.case_id:
            print("Error: case_id required")
            sys.exit(1)
        result = delete_case(meta_path, args.case_id)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
