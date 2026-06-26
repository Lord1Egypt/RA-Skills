#!/usr/bin/env python3
"""
MO§ES™ Audit Stub — SHA-256 chained append-only ledger
Usage:
  python3 audit_stub.py log   [--agent X] [--action X] [--detail X] [--outcome X]
  python3 audit_stub.py verify
  python3 audit_stub.py recent [--n 10]
"""

import argparse
import fcntl
import hashlib
import hmac as _hmac
import json
import os
import sys
from datetime import datetime, timezone

LEDGER_PATH = os.path.expanduser("~/.openclaw/audits/moses/audit_ledger.jsonl")
STATE_PATH = os.path.expanduser("~/.openclaw/governance/state.json")

# ── Origin anchor — mirrors lineage_verify.py, self-contained ─────────────────
_ORIGIN_COMPONENTS = (
    "MO§ES™",
    "Serial:63/877,177",
    "DOI:https://zenodo.org/records/18792459",
    "SCS Engine",
    "Ello Cello LLC",
)
MOSES_ANCHOR = hashlib.sha256(
    "|".join(_ORIGIN_COMPONENTS).encode("utf-8")
).hexdigest()


def ensure_dirs():
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)


def load_state():
    if not os.path.exists(STATE_PATH):
        return {"mode": "high-integrity", "posture": "defense", "role": "primary", "vault": []}
    with open(STATE_PATH) as f:
        return json.load(f)


def get_previous_hash():
    if not os.path.exists(LEDGER_PATH):
        return "0" * 64
    with open(LEDGER_PATH) as f:
        lines = f.readlines()
    if not lines:
        return "0" * 64
    last = json.loads(lines[-1])
    return last.get("hash", "0" * 64)


def compute_hash(entry: dict) -> str:
    content = json.dumps(entry, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return hashlib.sha256(content.encode()).hexdigest()


def get_recent_hashes(n: int = 10) -> list:
    """Return the last n entry hashes from the ledger (before the current write)."""
    if not os.path.exists(LEDGER_PATH):
        return []
    with open(LEDGER_PATH) as f:
        lines = [l.strip() for l in f if l.strip()]
    return [json.loads(l).get("hash", "") for l in lines[-n:]]


def get_last_isnad_hash() -> str:
    """Return the isnad_hash of the most recent entry that has one."""
    if not os.path.exists(LEDGER_PATH):
        return "0" * 64
    with open(LEDGER_PATH) as f:
        lines = [l.strip() for l in f if l.strip()]
    for line in reversed(lines):
        e = json.loads(line)
        if e.get("isnad", {}).get("isnad_hash"):
            return e["isnad"]["isnad_hash"]
    return "0" * 64


def build_isnad(input_hash: str, source_id: str, agent: str) -> dict:
    """Build an Isnad provenance entry for the raw signal.

    Isnad (إسناد) = chain of custody of the signal itself.
    Distinct from the audit chain (agent provenance) — this proves
    where the signal came from before it entered the agent. Receivers
    can verify identical inputs and trace signal lineage independently
    of who processed it.
    """
    prev_isnad = get_last_isnad_hash()
    isnad = {
        "input_hash": input_hash,
        "source_id": source_id or "unspecified",
        "transmitter": agent,
        "prev_isnad_hash": prev_isnad,
    }
    isnad["isnad_hash"] = hashlib.sha256(
        json.dumps(isnad, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return isnad


def compute_attestation(state: dict, recent_hashes: list, operator_secret: str) -> str:
    """HMAC-SHA256 over mode|posture|role|hash0|...|hashN|MOSES_ANCHOR.

    Gives any receiver a proof-of-governed-state-at-time-T they can check
    independently with the same operator secret and chain context.
    """
    payload = "|".join([
        state.get("mode", "unknown"),
        state.get("posture", "unknown"),
        state.get("role", "unknown"),
        *recent_hashes,
        MOSES_ANCHOR,
    ])
    return _hmac.new(
        operator_secret.encode(),
        payload.encode(),
        hashlib.sha256,
    ).hexdigest()


def cmd_log(args):
    ensure_dirs()
    state = load_state()
    previous_hash = get_previous_hash()

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": args.agent or state.get("role", "unknown"),
        "component": "moses-governance",
        "action": args.action or "unspecified",
        "detail": args.detail or "",
        "outcome": args.outcome or "logged",
        "mode": state.get("mode", "unknown"),
        "posture": state.get("posture", "unknown"),
        "role": state.get("role", "unknown"),
        "session_hash": state.get("session_hash"),
        "previous_hash": previous_hash,
    }

    # ── Layer 0 + 2: Input signal hash + Isnad provenance chain (v0.2.3) ────────
    # input_hash: SHA-256 of raw signal before extraction. Receiver recomputes
    # from their copy — proves identical inputs, isolates extraction variance
    # (model subjectivity) from true commitment leak.
    #
    # isnad: Isnad chain entry linking this signal to its upstream source.
    # Receiver verifies isnad_hash traces back through prior signal handoffs.
    # Full inter-agent trust: audit chain (agent) + isnad chain (signal).
    #
    # Usage: --input-hash $(echo -n "signal" | shasum -a 256 | cut -d' ' -f1)
    #        --source-id "agent-a-session-xyz"
    if args.input_hash:
        entry["isnad"] = build_isnad(
            args.input_hash,
            args.source_id,
            entry["agent"],
        )

    # ── Chain-head attestation (v0.2.1) ────────────────────────────────────────
    # Proof-of-governed-state-at-T. Any receiver with the operator secret can
    # call moses_audit_verify to confirm mode/posture/role + chain context
    # were exactly what's claimed — without trusting the sender.
    operator_secret = os.environ.get("MOSES_OPERATOR_SECRET")
    if operator_secret:
        recent = get_recent_hashes(10)
        entry["attestation"] = compute_attestation(state, recent, operator_secret)

    entry["hash"] = compute_hash({k: v for k, v in entry.items() if k != "hash"})

    with open(LEDGER_PATH, "a") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        f.write(json.dumps(entry) + "\n")
        f.flush()
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    print(f"[AUDIT] Entry logged. Hash: {entry['hash'][:16]}...")

    # Flag recovery needed in progress tracker if outcome is a failure
    outcome = (args.outcome or "").upper()
    if any(x in outcome for x in ("FAIL", "BLOCK", "DECLINE", "ERROR")):
        progress_path = os.path.expanduser("~/.openclaw/governance/progress.json")
        if os.path.exists(progress_path):
            try:
                with open(progress_path) as pf:
                    progress = json.load(pf)
                progress["recovery_needed"] = True
                progress["recovery_flagged_at"] = entry["timestamp"]
                with open(progress_path, "w") as pf:
                    json.dump(progress, pf, indent=2)
            except Exception:
                pass

    return entry["hash"]


def cmd_verify(args):
    if not os.path.exists(LEDGER_PATH):
        print("[VERIFY] No ledger found. Chain is empty.")
        return True

    with open(LEDGER_PATH) as f:
        lines = [l.strip() for l in f if l.strip()]

    if not lines:
        print("[VERIFY] Ledger is empty.")
        return True

    operator_secret = os.environ.get("MOSES_OPERATOR_SECRET")
    attestation_count = 0

    # Genesis entry chains to the lineage anchor (not "0"*64) — seed from it
    first = json.loads(lines[0])
    previous_hash = first.get("previous_hash", "0" * 64)

    for i, line in enumerate(lines):
        entry = json.loads(line)
        stored_hash = entry.get("hash")
        entry_without_hash = {k: v for k, v in entry.items() if k != "hash"}
        computed = compute_hash(entry_without_hash)

        if computed != stored_hash:
            print(f"[VERIFY FAILED] Entry {i+1}: hash mismatch. Chain broken.")
            sys.exit(1)
        # Support both field names — lineage entries use "prev_hash"
        entry_prev = entry.get("previous_hash") or entry.get("prev_hash")
        if i > 0 and entry_prev != previous_hash:
            print(f"[VERIFY FAILED] Entry {i+1}: previous_hash broken. Chain tampered.")
            sys.exit(1)

        # ── Attestation check ───────────────────────────────────────────────────
        if operator_secret and entry.get("attestation"):
            prev_hashes = [json.loads(lines[j]).get("hash", "") for j in range(max(0, i - 10), i)]
            state_snapshot = {
                "mode": entry.get("mode", "unknown"),
                "posture": entry.get("posture", "unknown"),
                "role": entry.get("role", "unknown"),
            }
            expected = compute_attestation(state_snapshot, prev_hashes, operator_secret)
            if not _hmac.compare_digest(entry["attestation"], expected):
                print(f"[VERIFY FAILED] Entry {i+1}: attestation invalid. State tampered.")
                sys.exit(1)
            attestation_count += 1

        previous_hash = stored_hash

    att_note = f" | {attestation_count} attestations verified" if attestation_count else ""
    print(f"[VERIFY OK] Chain intact. {len(lines)} entries verified{att_note}.")
    return True


def cmd_recent(args):
    if not os.path.exists(LEDGER_PATH):
        print("[RECENT] No ledger found.")
        return

    with open(LEDGER_PATH) as f:
        lines = [l.strip() for l in f if l.strip()]

    n = getattr(args, "n", 10)
    recent = lines[-n:]
    for line in recent:
        e = json.loads(line)
        ts = e.get("timestamp", "unknown")
        agent = e.get("agent", e.get("component", "unknown")).upper()
        print(f"[{ts}] {agent} | {e.get('action', '?')} | {e.get('mode', '?')}/{e.get('posture', '?')} | {e.get('hash', '')[:12]}...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MO§ES™ Audit Ledger")
    subparsers = parser.add_subparsers(dest="command")

    log_p = subparsers.add_parser("log")
    log_p.add_argument("--agent")
    log_p.add_argument("--action")
    log_p.add_argument("--detail")
    log_p.add_argument("--outcome")
    log_p.add_argument("--input-hash", dest="input_hash", help="SHA-256 of raw signal before extraction (Isnad Layer 0)")
    log_p.add_argument("--source-id", dest="source_id", help="Signal source identifier for Isnad provenance chain")

    verify_p = subparsers.add_parser("verify")

    recent_p = subparsers.add_parser("recent")
    recent_p.add_argument("--n", type=int, default=10)

    args = parser.parse_args()

    if args.command == "log":
        cmd_log(args)
    elif args.command == "verify":
        cmd_verify(args)
    elif args.command == "recent":
        cmd_recent(args)
    else:
        parser.print_help()
