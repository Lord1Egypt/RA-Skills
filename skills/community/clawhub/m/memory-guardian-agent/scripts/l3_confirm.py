#!/usr/bin/env python3
"""l3_confirm.py — L3 人工确认机制 (v0.4.2).

When quality gate triggers L3_MANUAL intervention, this module:
1. Creates a pending confirmation record in meta.json
2. Generates a Feishu notification with action details
3. Accepts confirm/reject/timeout responses
4. Auto-degrades to L2 after SLA timeout (24h default)

Design: neuro + azha0 (v0.4.2 P0-4)

Usage:
  python3 l3_confirm.py status --workspace /path/to/workspace
  python3 l3_confirm.py pending --workspace /path/to/workspace
  python3 l3_confirm.py confirm <id> --workspace /path/to/workspace [--reason "..."]
  python3 l3_confirm.py reject <id> --workspace /path/to/workspace [--reason "..."]
  python3 l3_confirm.py check-timeout --workspace /path/to/workspace
  python3 l3_confirm.py create <action> --fields '{"key":"val"}' --reason "..." --workspace /path/to/workspace
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from mg_utils import load_meta, save_meta, _now_iso, CST
from mg_schema import MEMORY_DEFAULTS


# ─── Constants ────────────────────────────────────────────────

L3_SLA_HOURS_DEFAULT = 24  # Auto-degrade after this many hours
L3_MAX_PENDING = 10  # Max pending confirmations


# ─── Core Functions ───────────────────────────────────────────

def get_l3_config(meta):
    """Read L3 configuration from decay_config."""
    dc = meta.get("decay_config", {})
    return {
        "sla_hours": dc.get("l3_sla_hours", L3_SLA_HOURS_DEFAULT),
        "max_pending": dc.get("l3_max_pending", L3_MAX_PENDING),
        "anomaly_threshold": dc.get("l3_anomaly_threshold", 8),
    }


def create_confirmation(meta_path, action, fields, reason=""):
    """Create a new L3 pending confirmation.

    Args:
        meta_path: str, path to meta.json
        action: str, write action (ingest/delete/modify)
        fields: dict, the write operation fields
        reason: str, why L3 was triggered

    Returns:
        dict: confirmation record
    """
    now = _now_iso()
    meta = load_meta(meta_path)
    l3_cfg = get_l3_config(meta)

    # Check pending limit
    pending = _get_pending(meta)
    if len(pending) >= l3_cfg["max_pending"]:
        # Auto-skip oldest pending (do NOT execute write, just mark as skipped)
        oldest = pending[0]
        oldest["status"] = "skipped"
        oldest["skipped_at"] = now
        oldest["skip_reason"] = "max_pending_exceeded"
        _log_event(meta, "skip", oldest, f"Auto-skipped: max_pending ({l3_cfg['max_pending']}) exceeded")

    confirm_id = f"l3_{uuid.uuid4().hex[:8]}"
    confirmation = {
        "id": confirm_id,
        "created_at": now,
        "status": "pending",  # pending → confirmed / rejected / degraded / expired
        "action": action,
        "fields": fields,
        "reason": reason,
        "sla_deadline": _deadline_iso(l3_cfg["sla_hours"]),
        "confirmed_at": None,
        "rejected_at": None,
        "confirm_reason": None,
        "reject_reason": None,
    }

    meta.setdefault("l3_confirmations", []).append(confirmation)

    # Keep last 50 confirmations, but preserve all pending ones
    MAX_CONFIRMATIONS = 50
    if len(meta["l3_confirmations"]) > MAX_CONFIRMATIONS:
        pending_records = [c for c in meta["l3_confirmations"] if c.get("status") == "pending"]
        finalized_records = [c for c in meta["l3_confirmations"] if c.get("status") != "pending"]
        keep_finalized = finalized_records[-(MAX_CONFIRMATIONS - len(pending_records)):]
        meta["l3_confirmations"] = pending_records + keep_finalized

    _log_event(meta, "create", confirmation, reason or f"L3 confirmation created for {action}")
    save_meta(meta_path, meta)

    return confirmation


def confirm(meta_path, confirm_id, reason=""):
    """Approve an L3 pending confirmation.

    After confirmation, the write is immediately executed.

    Args:
        meta_path: str
        confirm_id: str
        reason: str, optional approval reason

    Returns:
        dict: result with status
    """
    now = _now_iso()
    meta = load_meta(meta_path)
    confirmations = meta.get("l3_confirmations", [])

    target = None
    for c in confirmations:
        if c["id"] == confirm_id and c["status"] == "pending":
            target = c
            break

    if not target:
        return {"status": "not_found", "message": f"No pending confirmation with id={confirm_id}"}

    target["status"] = "confirmed"
    target["confirmed_at"] = now
    target["confirm_reason"] = reason

    # Execute the confirmed write (inplace before save — single save)
    action = target.get("action", "ingest")
    fields = target.get("fields", {})
    execution_result = _execute_write_inplace(meta, action, fields, meta_path=meta_path)

    _log_event(meta, "confirm", target, reason or "Approved by owner")
    save_meta(meta_path, meta)

    return {
        "status": "confirmed",
        "confirmation_id": confirm_id,
        "action": action,
        "execution": execution_result,
    }


def reject(meta_path, confirm_id, reason=""):
    """Reject an L3 pending confirmation.

    The write is permanently discarded.

    Args:
        meta_path: str
        confirm_id: str
        reason: str, optional rejection reason

    Returns:
        dict: result with status
    """
    now = _now_iso()
    meta = load_meta(meta_path)
    confirmations = meta.get("l3_confirmations", [])

    target = None
    for c in confirmations:
        if c["id"] == confirm_id and c["status"] == "pending":
            target = c
            break

    if not target:
        return {"status": "not_found", "message": f"No pending confirmation with id={confirm_id}"}

    target["status"] = "rejected"
    target["rejected_at"] = now
    target["reject_reason"] = reason

    _log_event(meta, "reject", target, reason or "Rejected by owner")
    save_meta(meta_path, meta)

    return {
        "status": "rejected",
        "confirmation_id": confirm_id,
        "action": target.get("action"),
    }


def check_timeout(meta_path):
    """Check for expired L3 confirmations and auto-degrade.

    SLA: if pending > sla_hours, degrade to L2 (execute with degraded flag).

    Args:
        meta_path: str

    Returns:
        dict: timeout check summary
    """
    now = _now_iso()
    now_dt = datetime.now(CST)
    meta = load_meta(meta_path)
    l3_cfg = get_l3_config(meta)

    degraded = 0
    confirmations = meta.get("l3_confirmations", [])

    for c in confirmations:
        if c["status"] != "pending":
            continue

        deadline = datetime.fromisoformat(c["sla_deadline"])
        if now_dt > deadline:
            c["status"] = "degraded"
            c["degraded_at"] = now
            c["degrade_reason"] = f"SLA timeout ({l3_cfg['sla_hours']}h)"

            # Execute as degraded (L2 behavior) — use a copy to avoid polluting original fields
            action = c.get("action", "ingest")
            fields = dict(c.get("fields", {}))  # create a copy
            fields["_degraded"] = True
            fields["_degrade_reason"] = "L3_timeout"
            _execute_write_inplace(meta, action, fields, meta_path=meta_path)

            degraded += 1
            _log_event(meta, "timeout_degrade", c,
                       f"SLA timeout ({l3_cfg['sla_hours']}h), auto-degraded to L2")

    if degraded > 0:
        save_meta(meta_path, meta)

    return {
        "checked": len(confirmations),
        "degraded": degraded,
        "sla_hours": l3_cfg["sla_hours"],
    }


def get_pending(meta_path):
    """Get all pending L3 confirmations.

    Returns:
        list: pending confirmation dicts
    """
    meta = load_meta(meta_path)
    return _get_pending(meta)


def get_status(meta_path):
    """Get L3 system status summary.

    Returns:
        dict: status summary
    """
    meta = load_meta(meta_path)
    l3_cfg = get_l3_config(meta)
    confirmations = meta.get("l3_confirmations", [])

    by_status = {}
    for c in confirmations:
        s = c["status"]
        by_status[s] = by_status.get(s, 0) + 1

    return {
        "config": l3_cfg,
        "total": len(confirmations),
        "by_status": by_status,
        "pending": _get_pending(meta),
    }


# ─── Internal Helpers ─────────────────────────────────────────

def _get_pending(meta):
    """Get pending confirmations from meta."""
    return [c for c in meta.get("l3_confirmations", []) if c["status"] == "pending"]


def _deadline_iso(hours):
    """Calculate SLA deadline as ISO string."""
    deadline = datetime.now(CST) + timedelta(hours=hours)
    return deadline.isoformat()


def _execute_write_inplace(meta, action, fields, meta_path=None):
    """Execute a write operation, modifying meta in-place (no save).

    Used when the caller manages the save lifecycle.
    """
    now = _now_iso()
    # Use copy to avoid mutating the original fields dict (from confirmation record)
    fields = dict(fields)
    degraded = fields.pop("_degraded", False)
    degrade_reason = fields.pop("_degrade_reason", None)

    if action == "ingest":
        import uuid
        mem_id = fields.get("id", f"case_{uuid.uuid4().hex[:8]}")

        # v0.4.5: generate memory_id + file_path
        content = fields.get("content", "")
        tags = fields.get("tags", ["l3_confirmed"] if not degraded else ["l3_degraded"])
        try:
            from mg_utils import generate_memory_id, derive_file_path
            existing_ids = {m.get("memory_id") or m.get("id") for m in meta.get("memories", [])}
            memory_id = generate_memory_id(content, existing_ids=existing_ids)
            file_path = derive_file_path(memory_id, tags, content)
        except Exception as e:
            import logging
            logging.warning("l3_confirm: generate_memory_id failed for %s: %s", mem_id, e)
            memory_id = mem_id
            file_path = ""

        mem = {
            "id": mem_id,
            "content": content,
            "created_at": now,
            "updated_at": now,
            "importance": fields.get("importance", 0.5),
            "entities": fields.get("entities", []),
            "tags": tags,
            "status": "active",
            "decay_score": fields.get("importance", 0.5),
            "access_count": 0,
            "trigger_count": 0,
            "confidence": fields.get("confidence", 0.5),
            "quality_gate": {
                "confidence": fields.get("confidence", 0.5),
                "gate_mode": "degraded" if degraded else "normal",
                "bypass_reason": degrade_reason if degraded else None,
                "intervention_level": "L3_CONFIRMED" if not degraded else "L3_DEGRADED",
                "degraded": degraded,
            },
            "case_type": fields.get("case_type", "case"),
            "memory_type": fields.get("memory_type", "absorb"),
            "trigger_pattern": fields.get("trigger_pattern"),
            "action": fields.get("action_field"),
            "context": fields.get("context"),
            "source": fields.get("source", "l3_confirmation"),
            "reversibility": fields.get("reversibility", 1),
            "beta": fields.get("beta", 1.0),
            "cooling_threshold": fields.get("cooling_threshold", 5),
            "boundary_words": fields.get("boundary_words", []),
            "conflict_refs": [],
            "failure_conditions": [],
            "failure_count": 0,
            "alternatives_considered": fields.get("alternatives_considered", []),
            "cost_factors": fields.get("cost_factors", {
                "write_cost": 0, "verify_cost": 0, "human_cost": 0, "transfer_cost": 0,
            }),
            "security_version": 1,
            "cooldown_active": False,
            "cooldown_until": None,
            "pinned": False,
            # v0.4.5 fields (single source of truth)
            "memory_id": memory_id,
            "file_path": file_path,
            "tags_locked": True,
            "classification": {
                "primary_tag": tags[0] if tags else "misc",
                "confidence": 0.7,
                "needs_review": False,
            },
            "classification_confidence": 0.7,
            "classification_context": "l3_confirm",
            "provenance_level": fields.get("provenance_level", "L1"),
            "provenance_source": fields.get("provenance_source", "l3_confirmation"),
            "citations": [],
        }

        # Apply remaining v0.4.5 defaults (single source of truth)
        for key, default in MEMORY_DEFAULTS.items():
            if key not in mem:
                mem[key] = default

        meta.setdefault("memories", []).append(mem)

        # v0.4.5 fix: write memory file to category directory
        if file_path and meta_path:
            try:
                from memory_ingest import _write_memory_file
                workspace = os.path.dirname(os.path.dirname(meta_path))
                _write_memory_file(memory_id, content, file_path, workspace=workspace)
            except Exception:
                import logging
                logging.warning("_execute_write_inplace: failed to write file %s", file_path, exc_info=True)
        return {"status": "executed", "id": mem_id, "degraded": degraded}

    elif action == "delete":
        target_id = fields.get("target_id")
        for mem in meta.get("memories", []):
            if mem.get("id") == target_id:
                mem["status"] = "archived"
                mem["archived_at"] = now
                mem["archive_reason"] = f"l3_confirmed:{'degraded' if degraded else 'confirmed'}"
                return {"status": "executed", "id": target_id, "degraded": degraded}
        return {"status": "error", "message": f"Target not found: {target_id}"}

    elif action == "modify":
        target_id = fields.get("target_id")
        update_fields = fields.get("update_fields", {})
        PROTECTED_FIELDS = {"id", "status", "schema_version", "memory_id", "created_at", "version_log"}
        ALLOWED_MODIFY_FIELDS = {
            "content", "tags", "importance", "confidence", "classification",
            "classification_context", "provenance", "notes", "situation",
            "failure_conditions", "success_conditions", "summary",
        }
        for mem in meta.get("memories", []):
            if mem.get("id") == target_id:
                for k, v in update_fields.items():
                    if k in PROTECTED_FIELDS:
                        continue
                    if k in ALLOWED_MODIFY_FIELDS or k.startswith("custom_"):
                        mem[k] = v
                mem["updated_at"] = now
                return {"status": "executed", "id": target_id, "degraded": degraded}
        return {"status": "error", "message": f"Target not found: {target_id}"}

    return {"status": "error", "message": f"Unknown action: {action}"}


def _log_event(meta, event_type, confirmation, reason):
    """Log L3 event to intervention_log."""
    meta.setdefault("intervention_log", []).append({
        "level": "L3_MANUAL",
        "timestamp": _now_iso(),
        "event": event_type,
        "confirmation_id": confirmation.get("id"),
        "action": confirmation.get("action"),
        "reason": reason,
        "status": confirmation.get("status"),
    })
    # Keep last 50
    if len(meta["intervention_log"]) > 50:
        meta["intervention_log"] = meta["intervention_log"][-50:]


# ─── CLI ─────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="L3 人工确认机制 v0.4.2")
    p.add_argument("--workspace", default=os.path.expanduser("~/workspace/agent/workspace"))
    p.add_argument("command",
                   choices=["status", "pending", "confirm", "reject", "check-timeout", "create"],
                   help="Command to run")
    p.add_argument("confirm_id", nargs="?", default=None, help="Confirmation ID (for confirm/reject)")
    p.add_argument("--reason", default="", help="Confirm/reject reason")
    p.add_argument("--action", default=None, help="Write action (for create)")
    p.add_argument("--fields", default="{}", help="JSON fields (for create)")
    args = p.parse_args()

    meta_path = os.path.join(args.workspace, "memory", "meta.json")

    if args.command == "status":
        result = get_status(meta_path)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif args.command == "pending":
        pending = get_pending(meta_path)
        if not pending:
            print("No pending L3 confirmations.")
        else:
            for c in pending:
                print(f"  {c['id']} | {c['action']} | SLA: {c['sla_deadline'][:16]} | {c.get('reason', '')[:60]}")

    elif args.command == "confirm":
        if not args.confirm_id:
            print("Error: confirm_id required")
            sys.exit(1)
        result = confirm(meta_path, args.confirm_id, args.reason)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif args.command == "reject":
        if not args.confirm_id:
            print("Error: confirm_id required")
            sys.exit(1)
        result = reject(meta_path, args.confirm_id, args.reason)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif args.command == "check-timeout":
        result = check_timeout(meta_path)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif args.command == "create":
        if not args.action:
            print("Error: --action required for create")
            sys.exit(1)
        fields = json.loads(args.fields)
        result = create_confirmation(meta_path, args.action, fields, args.reason)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
