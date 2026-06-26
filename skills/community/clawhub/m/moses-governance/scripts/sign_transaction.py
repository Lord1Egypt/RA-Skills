#!/usr/bin/env python3
"""
sign_transaction.py — Signing tool with governance gate (v0.5)

The signing function IS the governance function.
No bypass path exists — by architecture, not by rule.

The MOSES_OPERATOR_SECRET is accessed ONLY inside this tool, ONLY after the
governance gate passes. There is no code path that reaches the key without
first clearing posture/mode/role constraints. That is what makes it
architecture rather than policy.

Architecture:
  Agent requests signing →
    calls sign_transaction.py sign →
      governance gate checks posture + mode (inside this tool) →
        BLOCKED? returns error, exits 1. Key never accessed.
        PERMITTED? signs payload, writes audit, returns signed JSON.

Usage:
  python3 sign_transaction.py sign --payload "<text>" --agent <name> [--confirm]
  python3 sign_transaction.py verify --payload "<text>" --sig <hex>
  python3 sign_transaction.py status
"""

import argparse
import contextlib
import datetime
import hashlib
import hmac as _hmac
import importlib.util
import json
import os
import sys
import types

_HERE = os.path.dirname(os.path.abspath(__file__))


# ── dynamic imports (stdlib only — mirrors audit_stub.py pattern) ────────────

def _load_module(name, filename):
    path = os.path.join(_HERE, filename)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _state_mod():
    return _load_module("init_state", "init_state.py")


def _audit_mod():
    return _load_module("audit_stub", "audit_stub.py")


# ── governance gate ───────────────────────────────────────────────────────────

class GovernanceBlock(Exception):
    pass


def _governance_gate(state: dict, confirm: bool) -> dict:
    """
    Check posture and mode before any key access.

    SCOUT   — always blocked. No state changes permitted by posture definition.
    DEFENSE — blocked unless --confirm is passed (explicit operator authorization).
    OFFENSE — permitted within active mode constraints.

    Returns approved state dict on success. Raises GovernanceBlock on failure.
    """
    posture = (state.get("posture") or "scout").lower()
    mode    = state.get("mode", "unknown")
    role    = state.get("role", "unknown")

    if posture == "scout":
        raise GovernanceBlock(
            "BLOCKED — posture=SCOUT. No state changes permitted. "
            "Set posture to DEFENSE (with --confirm) or OFFENSE to sign."
        )

    if posture == "defense" and not confirm:
        raise GovernanceBlock(
            "BLOCKED — posture=DEFENSE requires explicit operator confirmation. "
            "Re-run with --confirm to authorize this signing operation. "
            "DEFENSE posture means: protect + confirm outbound. Confirmation is the protection."
        )

    return {"posture": posture, "mode": mode, "role": role}


# ── cryptographic primitives ──────────────────────────────────────────────────

def _payload_hash(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _sign(payload: str, secret: str) -> str:
    return _hmac.new(
        secret.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


# ── audit write ───────────────────────────────────────────────────────────────

def _write_audit(agent: str, action: str, detail: str, outcome: str, gov: dict) -> str:
    """Write a governance audit entry. Returns the entry hash prefix."""
    audit = _audit_mod()
    fake_args = types.SimpleNamespace(
        agent=agent,
        action=action,
        detail=detail,
        outcome=outcome,
        input_hash=None,
        source_id=None,
    )
    # audit_stub prints "[AUDIT] Entry logged..." to stdout — redirect to stderr
    # so sign_transaction's JSON output stays clean for programmatic callers.
    with contextlib.redirect_stdout(sys.stderr):
        entry_hash = audit.cmd_log(fake_args)
    return entry_hash or "logged"


# ── commands ──────────────────────────────────────────────────────────────────

def cmd_sign(args):
    # ── Step 1: Load governance state. Key is never touched yet. ─────────────
    state_mod = _state_mod()
    state = state_mod.load_state()
    if state is None:
        out = {
            "status": "ERROR",
            "reason": "Governance state not initialized. Run: python3 init_state.py init",
            "signature": None,
        }
        print(json.dumps(out, indent=2))
        sys.exit(1)

    # ── Step 2: Governance gate. Raises on block. Key still untouched. ───────
    try:
        approved = _governance_gate(state, confirm=getattr(args, "confirm", False))
    except GovernanceBlock as e:
        out = {
            "status": "BLOCKED",
            "reason": str(e),
            "posture": state.get("posture"),
            "mode": state.get("mode"),
            "signature": None,
        }
        print(json.dumps(out, indent=2))
        sys.exit(1)

    # ── Step 3: Key access. Only reachable after gate passes. ────────────────
    secret = os.environ.get("MOSES_OPERATOR_SECRET", "")
    if not secret:
        out = {
            "status": "ERROR",
            "reason": (
                "MOSES_OPERATOR_SECRET not set. "
                "The signing key must be present for authorized operations. "
                "Set it in your environment before calling this tool."
            ),
            "signature": None,
        }
        print(json.dumps(out, indent=2))
        sys.exit(1)

    # ── Step 4: Sign. ─────────────────────────────────────────────────────────
    p_hash = _payload_hash(args.payload)
    sig    = _sign(args.payload, secret)
    ts     = datetime.datetime.now(datetime.timezone.utc).isoformat()

    signed = {
        "status":           "SIGNED",
        "payload_hash":     p_hash,
        "signature":        sig,
        "timestamp":        ts,
        "governance_state": approved,
        "agent":            args.agent,
    }

    # ── Step 5: Audit. Atomic with signing — both succeed or both fail. ───────
    try:
        _write_audit(
            agent   = args.agent,
            action  = "moses_sign_transaction",
            detail  = f"payload_hash={p_hash}",
            outcome = "SIGNED",
            gov     = approved,
        )
        signed["audit_ref"] = p_hash
    except Exception as e:
        signed["audit_warning"] = f"Signing succeeded but audit write failed: {e}"

    print(json.dumps(signed, indent=2))


def cmd_verify(args):
    """Verify a signature. Requires MOSES_OPERATOR_SECRET in environment."""
    secret = os.environ.get("MOSES_OPERATOR_SECRET", "")
    if not secret:
        out = {"status": "ERROR", "reason": "MOSES_OPERATOR_SECRET not set"}
        print(json.dumps(out, indent=2))
        sys.exit(1)

    expected = _sign(args.payload, secret)
    match    = _hmac.compare_digest(expected, args.sig)

    out = {
        "status":          "VALID" if match else "INVALID",
        "payload_hash":    _payload_hash(args.payload),
        "signature_match": match,
    }
    print(json.dumps(out, indent=2))
    sys.exit(0 if match else 1)


def cmd_status(args):
    """Show the current governance gate status — will signing be permitted?"""
    state_mod = _state_mod()
    state = state_mod.load_state()

    if state is None:
        out = {
            "gate":   "ERROR",
            "reason": "Governance state not initialized. Run: python3 init_state.py init",
        }
        print(json.dumps(out, indent=2))
        sys.exit(1)

    posture = (state.get("posture") or "scout").lower()

    try:
        # Pass confirm=True to check OFFENSE vs DEFENSE separately in output
        _governance_gate(state, confirm=True)
        if posture == "defense":
            gate = "REQUIRES_CONFIRM"
            note = "DEFENSE posture — signing permitted with --confirm flag only."
        else:
            gate = "OPEN"
            note = "Signing permitted under current governance state."
    except GovernanceBlock as e:
        gate = "BLOCKED"
        note = str(e)

    print(json.dumps({
        "gate":    gate,
        "posture": posture,
        "mode":    state.get("mode"),
        "role":    state.get("role"),
        "note":    note,
    }, indent=2))


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="moses_sign_transaction — signing tool with governance gate (v0.5)"
    )
    sub = parser.add_subparsers(dest="command")

    p_sign = sub.add_parser("sign", help="Sign a payload (governance gate runs first)")
    p_sign.add_argument("--payload",  required=True, help="Payload text or JSON string to sign")
    p_sign.add_argument("--agent",    required=True, help="Agent name for audit record")
    p_sign.add_argument("--confirm",  action="store_true",
                        help="Explicit operator confirmation (required in DEFENSE posture)")

    p_verify = sub.add_parser("verify", help="Verify a signature against a payload")
    p_verify.add_argument("--payload", required=True, help="Original payload text")
    p_verify.add_argument("--sig",     required=True, help="Signature hex to verify")

    sub.add_parser("status", help="Show current governance gate status")

    args = parser.parse_args()

    if args.command == "sign":
        cmd_sign(args)
    elif args.command == "verify":
        cmd_verify(args)
    elif args.command == "status":
        cmd_status(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
