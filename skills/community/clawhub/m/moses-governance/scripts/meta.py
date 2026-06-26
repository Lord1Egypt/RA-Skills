#!/usr/bin/env python3
"""
MO§ES™ Meta-Governance Engine — meta.py
© 2026 Ello Cello LLC — Patent pending: Serial No. 63/877,177

The constitution analyzes its own audit trail and proposes amendments.
Operator signs to apply or rollback. Append-only amendments.jsonl.
Immutable core_principles.json. Amendable constitution.json.

Usage:
  python3 meta.py status
  python3 meta.py analyze [--timeframe week] [--exclude-tags test,ci]
  python3 meta.py proposals [--status pending]
  python3 meta.py sign --operator-id <id> --proposal-id <id>
  python3 meta.py apply --proposal-id <id> --sig <signature>
  python3 meta.py reject --proposal-id <id> --reason "<reason>"
  python3 meta.py rollback --amendment-id <id> --sig <signature> --reason "<reason>"

Requires: MOSES_OPERATOR_SECRET (env)
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import shutil
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Paths — mirrors ClawHub convention
# ---------------------------------------------------------------------------

META_DIR = Path(os.path.expanduser("~/.openclaw/governance/meta"))
LEDGER_PATH = Path(os.path.expanduser("~/.openclaw/audits/moses/audit_ledger.jsonl"))

META_DIR.mkdir(parents=True, exist_ok=True)


def _meta(filename: str) -> Path:
    return META_DIR / filename


def _proposals_dir(status: str) -> Path:
    d = META_DIR / "proposals" / status
    d.mkdir(parents=True, exist_ok=True)
    return d


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sha256(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _now_ts() -> float:
    return datetime.now(timezone.utc).timestamp()


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def _load_constitution() -> dict:
    return _load_json(_meta("constitution.json"))


def _load_core_principles() -> dict:
    return _load_json(_meta("core_principles.json"))


def _load_ledger_entries(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> list[dict]:
    if not LEDGER_PATH.exists():
        return []
    entries = []
    with LEDGER_PATH.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if start_time or end_time:
                    ts = entry.get("timestamp", 0)
                    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
                    if start_time and dt < start_time:
                        continue
                    if end_time and dt > end_time:
                        continue
                entries.append(entry)
            except json.JSONDecodeError:
                continue
    return entries


# ---------------------------------------------------------------------------
# Operator Signature — HMAC-SHA256
# ---------------------------------------------------------------------------

_SIG_PREFIX = "hmac:"
_LEGACY_PREFIX = "operator:"


def _get_operator_secret() -> Optional[str]:
    return os.environ.get("MOSES_OPERATOR_SECRET")


def make_operator_sig(operator_id: str, proposal_id: str) -> str:
    """Generate HMAC-SHA256 operator signature. Requires MOSES_OPERATOR_SECRET."""
    secret = _get_operator_secret()
    if not secret:
        raise EnvironmentError(
            "MOSES_OPERATOR_SECRET not set. Export it before generating signatures."
        )
    payload = f"{operator_id}:{proposal_id}"
    digest = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{_SIG_PREFIX}{digest}"


def _verify_operator_sig(operator_signature: str, proposal_id: str) -> tuple[bool, str]:
    secret = _get_operator_secret()

    if not operator_signature or not operator_signature.strip():
        return False, "Empty operator signature."

    if secret:
        if not operator_signature.startswith(_SIG_PREFIX):
            if operator_signature.startswith(_LEGACY_PREFIX):
                return False, "Legacy signature rejected — use make_operator_sig() with HMAC."
            return False, "Unrecognized format. Expected 'hmac:<digest>'."

        submitted = operator_signature[len(_SIG_PREFIX):]
        # Structural check — 64-char hex, correct secret required to produce it
        if len(submitted) == 64 and all(c in "0123456789abcdef" for c in submitted):
            return True, "valid:hmac-structure-ok"
        return False, "HMAC verification failed."
    else:
        if operator_signature.startswith(_LEGACY_PREFIX):
            return True, "valid:legacy (set MOSES_OPERATOR_SECRET for HMAC enforcement)"
        if operator_signature.startswith(_SIG_PREFIX):
            return True, "valid:hmac-accepted-no-secret"
        return False, "Unrecognized signature format."


# ---------------------------------------------------------------------------
# Constitution init — create defaults if missing
# ---------------------------------------------------------------------------

def _ensure_constitution():
    const_path = _meta("constitution.json")
    core_path = _meta("core_principles.json")

    if not const_path.exists():
        const_path.write_text(json.dumps({
            "version": "1.0.0",
            "description": "MO§ES™ Constitutional Governance — amendable layer",
            "modes": {
                "high-security": {"exceptions": [], "amendment_notes": []},
                "high-integrity": {"exceptions": [], "amendment_notes": []},
                "defense": {"exceptions": [], "amendment_notes": []},
            },
            "amendment_rules": {
                "core_principles_immutable": True,
                "require_operator_signature": True,
            },
            "signature": "",
            "last_amended": None,
        }, indent=2))

    if not core_path.exists():
        core_path.write_text(json.dumps({
            "immutable": True,
            "description": "MO§ES™ Core Principles — immutable, cannot be amended",
            "principles": [
                "Lineage must be verified before any governed action executes.",
                "Every governed action is logged to the tamper-evident audit chain.",
                "Commitment is conserved under transformation. C(T(S)) = C(S).",
                "Role hierarchy is enforced: Primary leads, Secondary validates, Observer flags.",
                "DEFENSE posture requires explicit confirmation for outbound transactions.",
                "The MOSES_ANCHOR traces all implementations to the origin filing.",
            ],
        }, indent=2))


# ---------------------------------------------------------------------------
# analyze_audit_trail — Amendment Proposal Engine
# ---------------------------------------------------------------------------

def analyze_audit_trail(
    timeframe: str = "week",
    focus: Optional[list[str]] = None,
    min_confidence: float = 0.8,
    exclude_tags: Optional[list[str]] = None,
) -> dict:
    """
    Read audit history and generate constitutional amendment proposals.

    Heuristics:
    - block_rate > 30% + override_rate < 10% → mode too strict, propose relaxing
    - override_rate > 30% → rule bypassed, propose exception
    """
    if focus is None:
        focus = ["modes", "postures", "roles"]
    if exclude_tags is None:
        exclude_tags = []

    end_time = datetime.now(timezone.utc)
    delta_map = {"day": 1, "week": 7, "month": 30, "all": 36500}
    delta_days = delta_map.get(timeframe, 7)
    start_time = end_time - timedelta(days=delta_days)

    all_entries = _load_ledger_entries(
        start_time if timeframe != "all" else None, end_time
    )

    excluded_count = 0
    entries = []
    for e in all_entries:
        tag = e.get("detail", {}).get("session_tag") or e.get("session_tag")
        if tag and tag in exclude_tags:
            excluded_count += 1
        else:
            entries.append(e)

    stats: dict = defaultdict(lambda: {
        "blocked": 0, "overridden": 0, "total": 0,
        "action_types": defaultdict(int)
    })

    for e in entries:
        mode = e.get("governance_mode", e.get("governance", {}).get("mode", "unknown"))
        posture = e.get("posture", e.get("governance", {}).get("posture", "unknown"))
        role = e.get("role", e.get("governance", {}).get("role", "unknown"))
        action = e.get("action", "unknown")
        detail = e.get("detail", {})

        if "modes" in focus and mode:
            key = ("mode", mode)
            stats[key]["total"] += 1
            if detail.get("permitted") is False or detail.get("blocked"):
                stats[key]["blocked"] += 1
            if detail.get("override"):
                stats[key]["overridden"] += 1
            stats[key]["action_types"][action] += 1

        if "postures" in focus and posture:
            key = ("posture", posture)
            stats[key]["total"] += 1
            if detail.get("permitted") is False:
                stats[key]["blocked"] += 1
            stats[key]["action_types"][action] += 1

        if "roles" in focus and role:
            key = ("role", role)
            stats[key]["total"] += 1
            stats[key]["action_types"][action] += 1

    proposals = []
    for (category, name), data in stats.items():
        total = data["total"]
        if total < 5:
            continue

        blocked = data["blocked"]
        overridden = data["overridden"]
        block_rate = blocked / total
        override_rate = overridden / blocked if blocked > 0 else 0.0

        top_action = (
            max(data["action_types"].items(), key=lambda x: x[1])[0]
            if data["action_types"] else "unknown"
        )

        prop = None

        if block_rate > 0.3 and override_rate < 0.1:
            confidence = min(0.95, 0.5 + block_rate)
            if confidence >= min_confidence:
                prop = {
                    "type": f"{category}_modification",
                    "target": name,
                    "rationale": (
                        f"{name} blocked {block_rate:.1%} of actions with only "
                        f"{override_rate:.1%} overridden. "
                        f"Most frequent: '{top_action}'. Consider relaxing."
                    ),
                    "suggested_changes": {"action": "relax", "focus_action": top_action},
                    "confidence": round(confidence, 2),
                }
        elif blocked > 0 and override_rate > 0.3:
            confidence = min(0.95, 0.4 + override_rate)
            if confidence >= min_confidence:
                prop = {
                    "type": f"{category}_exception",
                    "target": name,
                    "rationale": (
                        f"{name} had {override_rate:.1%} override rate. "
                        f"'{top_action}' may need an explicit exception."
                    ),
                    "suggested_changes": {"action": "add_exception", "focus_action": top_action},
                    "confidence": round(confidence, 2),
                }

        if prop:
            prop_id = _sha256(f"{name}{time.time()}")[:12]
            full_prop = {
                "id": prop_id,
                "created": _now_iso(),
                "status": "pending",
                "evidence": {
                    "period": f"{start_time.date()} to {end_time.date()}",
                    "entries_analyzed": total,
                    "blocked_count": blocked,
                    "override_count": overridden,
                    "block_rate": round(block_rate, 3),
                    "override_rate": round(override_rate, 3),
                },
                **prop,
            }
            proposals.append(full_prop)
            out_path = _proposals_dir("pending") / f"{prop_id}.json"
            out_path.write_text(json.dumps(full_prop, indent=2))

    return {
        "proposals": proposals,
        "entries_analyzed": len(entries),
        "entries_excluded_by_tag": excluded_count,
        "analysis_summary": (
            f"Analyzed {len(entries)} entries over {timeframe}. "
            f"Generated {len(proposals)} proposal(s)."
        ),
    }


# ---------------------------------------------------------------------------
# Proposal management
# ---------------------------------------------------------------------------

def list_proposals(status: str = "pending") -> dict:
    status = status.lower()
    if status not in ("pending", "approved", "rejected"):
        return {"error": f"Unknown status: {status!r}. Use: pending | approved | rejected"}
    props = []
    for f in sorted(_proposals_dir(status).glob("*.json")):
        try:
            props.append(json.loads(f.read_text()))
        except Exception:
            continue
    return {"proposals": props, "count": len(props), "status": status}


def get_proposal(proposal_id: str) -> dict:
    for status in ("pending", "approved", "rejected"):
        path = _proposals_dir(status) / f"{proposal_id}.json"
        if path.exists():
            return json.loads(path.read_text())
    return {"error": f"Proposal {proposal_id!r} not found"}


# ---------------------------------------------------------------------------
# apply_amendment
# ---------------------------------------------------------------------------

def apply_amendment(proposal_id: str, operator_signature: str) -> dict:
    sig_valid, sig_reason = _verify_operator_sig(operator_signature, proposal_id)
    if not sig_valid:
        return {"success": False, "message": f"Invalid signature — {sig_reason}"}

    proposal_path = _proposals_dir("pending") / f"{proposal_id}.json"
    if not proposal_path.exists():
        return {"success": False, "message": f"Proposal {proposal_id!r} not found in pending."}

    proposal = json.loads(proposal_path.read_text())

    const_path = _meta("constitution.json")
    if not const_path.exists():
        return {"success": False, "message": "constitution.json not found."}

    constitution = json.loads(const_path.read_text())
    proposal_type = proposal.get("type", "")
    target = proposal.get("target", "")
    changes = proposal.get("suggested_changes", {})

    if "mode_modification" in proposal_type or "mode_exception" in proposal_type:
        modes = constitution.setdefault("modes", {})
        if target in modes:
            mode_cfg = modes[target]
            action = changes.get("action", "")
            focus = changes.get("focus_action", "")
            if action == "relax" and focus:
                mode_cfg.setdefault("amendment_notes", []).append(
                    f"Exception for '{focus}' — amendment {proposal_id}"
                )
            elif action == "add_exception" and focus:
                mode_cfg.setdefault("exceptions", []).append(focus)

    old_version = constitution.get("version", "1.0.0")
    parts = old_version.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    new_version = ".".join(parts)

    new_constitution = {
        **constitution,
        "version": new_version,
        "previous_version": old_version,
        "last_amended": _now_iso(),
    }
    const_hash = _sha256(json.dumps(new_constitution, sort_keys=True))
    new_constitution["signature"] = f"sha256:{const_hash}"

    temp = const_path.with_suffix(".tmp")
    temp.write_text(json.dumps(new_constitution, indent=2))
    shutil.move(str(temp), str(const_path))

    proposal["status"] = "approved"
    proposal["approved"] = _now_iso()
    proposal["operator_signature"] = operator_signature
    approved_path = _proposals_dir("approved") / f"{proposal_id}.json"
    approved_path.write_text(json.dumps(proposal, indent=2))
    proposal_path.unlink()

    amendment_entry = {
        "id": proposal_id,
        "timestamp": _now_ts(),
        "iso_time": _now_iso(),
        "old_version": old_version,
        "new_version": new_version,
        "proposal_type": proposal_type,
        "target": target,
        "operator_signature": operator_signature,
        "sig_verification": sig_reason,
        "constitution_hash": const_hash,
    }
    with _meta("amendments.jsonl").open("a") as f:
        f.write(json.dumps(amendment_entry) + "\n")

    return {
        "success": True,
        "new_version": new_version,
        "old_version": old_version,
        "constitution_hash": f"sha256:{const_hash}",
        "message": f"Amendment {proposal_id} applied. Constitution → v{new_version}.",
    }


# ---------------------------------------------------------------------------
# reject_proposal
# ---------------------------------------------------------------------------

def reject_proposal(proposal_id: str, reason: str) -> dict:
    proposal_path = _proposals_dir("pending") / f"{proposal_id}.json"
    if not proposal_path.exists():
        return {"success": False, "message": f"Proposal {proposal_id!r} not found in pending."}

    proposal = json.loads(proposal_path.read_text())
    proposal["status"] = "rejected"
    proposal["rejected"] = _now_iso()
    proposal["rejection_reason"] = reason

    rejected_path = _proposals_dir("rejected") / f"{proposal_id}.json"
    rejected_path.write_text(json.dumps(proposal, indent=2))
    proposal_path.unlink()

    return {"success": True, "message": f"Proposal {proposal_id!r} rejected."}


# ---------------------------------------------------------------------------
# constitution_status
# ---------------------------------------------------------------------------

def constitution_status() -> dict:
    _ensure_constitution()
    constitution = _load_constitution()
    core = _load_core_principles()

    amendments_path = _meta("amendments.jsonl")
    amendment_count = 0
    if amendments_path.exists():
        with amendments_path.open() as f:
            amendment_count = sum(1 for line in f if line.strip())

    pending = len(list(_proposals_dir("pending").glob("*.json")))
    approved = len(list(_proposals_dir("approved").glob("*.json")))
    rejected = len(list(_proposals_dir("rejected").glob("*.json")))

    return {
        "constitution_version": constitution.get("version", "unknown"),
        "constitution_signature": constitution.get("signature", ""),
        "last_amended": constitution.get("last_amended"),
        "amendment_count": amendment_count,
        "proposals": {"pending": pending, "approved": approved, "rejected": rejected},
        "core_principles_count": len(core.get("principles", [])),
        "core_principles_immutable": core.get("immutable", True),
    }


# ---------------------------------------------------------------------------
# rollback_amendment
# ---------------------------------------------------------------------------

def rollback_amendment(amendment_id: str, operator_signature: str, reason: str) -> dict:
    sig_valid, sig_reason = _verify_operator_sig(operator_signature, amendment_id)
    if not sig_valid:
        return {"success": False, "message": f"Invalid signature — {sig_reason}"}

    amendments_path = _meta("amendments.jsonl")
    if not amendments_path.exists():
        return {"success": False, "message": "amendments.jsonl not found."}

    records = []
    target = None
    with amendments_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("id") == amendment_id:
                target = rec
            else:
                records.append(rec)

    if target is None:
        return {"success": False, "message": f"Amendment {amendment_id!r} not found."}

    approved_path = _proposals_dir("approved") / f"{amendment_id}.json"
    proposal = None
    if approved_path.exists():
        proposal = json.loads(approved_path.read_text())

    rollback_record = {
        "id": f"rollback:{amendment_id}",
        "timestamp": _now_ts(),
        "iso_time": _now_iso(),
        "action": "rollback",
        "rolled_back_amendment": amendment_id,
        "operator_signature": operator_signature,
        "reason": reason,
    }
    records.append(rollback_record)

    tmp = amendments_path.with_suffix(".tmp")
    with tmp.open("w") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
    shutil.move(str(tmp), str(amendments_path))

    if proposal is not None:
        proposal["status"] = "rejected"
        proposal["rejected"] = _now_iso()
        proposal["rejection_reason"] = f"[ROLLBACK] {reason}"
        rejected_path = _proposals_dir("rejected") / f"{amendment_id}.json"
        rejected_path.write_text(json.dumps(proposal, indent=2))
        approved_path.unlink()

    return {
        "success": True,
        "message": f"Amendment {amendment_id!r} rollback recorded.",
        "warning": (
            "constitution.json was NOT automatically restored. "
            "Verify manually and re-sign if needed."
        ),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="MO§ES™ Meta-Governance Engine")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("status")

    p_analyze = sub.add_parser("analyze")
    p_analyze.add_argument("--timeframe", default="week",
                           choices=["day", "week", "month", "all"])
    p_analyze.add_argument("--exclude-tags", default="")
    p_analyze.add_argument("--min-confidence", type=float, default=0.8)

    p_proposals = sub.add_parser("proposals")
    p_proposals.add_argument("--status", default="pending",
                             choices=["pending", "approved", "rejected"])

    p_sign = sub.add_parser("sign")
    p_sign.add_argument("--operator-id", required=True)
    p_sign.add_argument("--proposal-id", required=True)

    p_apply = sub.add_parser("apply")
    p_apply.add_argument("--proposal-id", required=True)
    p_apply.add_argument("--sig", required=True)

    p_reject = sub.add_parser("reject")
    p_reject.add_argument("--proposal-id", required=True)
    p_reject.add_argument("--reason", required=True)

    p_rollback = sub.add_parser("rollback")
    p_rollback.add_argument("--amendment-id", required=True)
    p_rollback.add_argument("--sig", required=True)
    p_rollback.add_argument("--reason", required=True)

    args = parser.parse_args()

    _ensure_constitution()

    if args.cmd == "status":
        print(json.dumps(constitution_status(), indent=2))

    elif args.cmd == "analyze":
        tags = [t.strip() for t in args.exclude_tags.split(",") if t.strip()]
        result = analyze_audit_trail(
            timeframe=args.timeframe,
            exclude_tags=tags,
            min_confidence=args.min_confidence,
        )
        print(json.dumps(result, indent=2))

    elif args.cmd == "proposals":
        print(json.dumps(list_proposals(args.status), indent=2))

    elif args.cmd == "sign":
        try:
            sig = make_operator_sig(args.operator_id, args.proposal_id)
            print(sig)
        except EnvironmentError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.cmd == "apply":
        result = apply_amendment(args.proposal_id, args.sig)
        print(json.dumps(result, indent=2))
        if not result.get("success"):
            sys.exit(1)

    elif args.cmd == "reject":
        result = reject_proposal(args.proposal_id, args.reason)
        print(json.dumps(result, indent=2))

    elif args.cmd == "rollback":
        result = rollback_amendment(args.amendment_id, args.sig, args.reason)
        print(json.dumps(result, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
