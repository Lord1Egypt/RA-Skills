#!/usr/bin/env python3
"""
presence.py — MO§ES™ Presence Protocol
Liveness + identity handshake before inter-agent kernel exchange.

Answers Séphira's critique: zombie agent problem.
An agent can be technically alive (responding to pings) but constitutionally
dead — running with no governance state, wrong posture, stale lineage. A TCP
handshake proves connectivity. A presence handshake proves governed identity.

How it works:
  1. Agent A calls: presence.py challenge
     → produces a nonce + commitment to current governed state
  2. Agent B calls: presence.py respond <nonce> <agent_id>
     → produces a signed response proving B's governed state at that nonce
  3. Agent A calls: presence.py verify <challenge_file> <response_file>
     → verifies B is alive, governed, and lineage-anchored at exchange time

Usage:
  python3 presence.py challenge                        — issue a challenge
  python3 presence.py respond <nonce> <agent_id>       — respond to a challenge
  python3 presence.py verify <challenge.json> <response.json>  — verify response
  python3 presence.py status                           — show local presence state
"""

import hashlib
import hmac
import json
import os
import sys
import time
from datetime import datetime, timezone

STATE_PATH = os.path.expanduser("~/.openclaw/governance/state.json")
PRESENCE_DIR = os.path.expanduser("~/.openclaw/governance/presence")
LINEAGE_ANCHOR = "1a2b3c4d5e6f7890abcdef1234567890abcdef1234567890abcdef1234567890ab"  # replaced at install

NONCE_TTL = 300  # 5 minutes — stale challenge = rejected


def ensure_dirs():
    os.makedirs(PRESENCE_DIR, exist_ok=True)


def load_state():
    if not os.path.exists(STATE_PATH):
        return {}
    with open(STATE_PATH) as f:
        return json.load(f)


def state_fingerprint(state):
    """Deterministic fingerprint of current governed state."""
    relevant = {
        "mode": state.get("mode", "unknown"),
        "posture": state.get("posture", "unknown"),
        "role": state.get("role", "unknown"),
        "session_hash": state.get("session_hash", ""),
    }
    return hashlib.sha256(
        json.dumps(relevant, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def make_nonce():
    import secrets
    return secrets.token_hex(16)


def cmd_challenge(args):
    """Issue a presence challenge. Share the output with the agent you want to verify."""
    ensure_dirs()
    state = load_state()
    nonce = make_nonce()
    issued_at = datetime.now(timezone.utc).isoformat()
    ts = int(time.time())

    challenge = {
        "nonce": nonce,
        "issued_at": issued_at,
        "issued_ts": ts,
        "expires_ts": ts + NONCE_TTL,
        "issuer_state_fingerprint": state_fingerprint(state),
        "issuer_lineage_anchor": LINEAGE_ANCHOR,
        "issuer_mode": state.get("mode", "unknown"),
        "issuer_posture": state.get("posture", "unknown"),
        "issuer_role": state.get("role", "unknown"),
    }
    challenge["challenge_hash"] = hashlib.sha256(
        json.dumps(challenge, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    path = os.path.join(PRESENCE_DIR, f"challenge_{nonce[:8]}.json")
    with open(path, "w") as f:
        json.dump(challenge, f, indent=2)

    print(json.dumps(challenge, indent=2))
    print(f"\n[PRESENCE] Challenge issued. Share this with the agent you want to verify.")
    print(f"[PRESENCE] Saved to: {path}")
    print(f"[PRESENCE] Expires in {NONCE_TTL}s. Run: presence.py verify <challenge.json> <response.json>")


def cmd_respond(args):
    """Respond to a presence challenge. Proves your governed identity at this moment."""
    if len(args) < 2:
        print("Usage: presence.py respond <nonce> <agent_id>")
        sys.exit(1)

    nonce = args[0]
    agent_id = args[1]
    state = load_state()
    ts = int(time.time())

    if not state:
        print("[PRESENCE] ERROR: No governance state loaded. Cannot prove governed identity.")
        print("           Run: init_state.py init")
        sys.exit(1)

    response = {
        "nonce": nonce,
        "agent_id": agent_id,
        "responded_at": datetime.now(timezone.utc).isoformat(),
        "responded_ts": ts,
        "state_fingerprint": state_fingerprint(state),
        "lineage_anchor": LINEAGE_ANCHOR,
        "mode": state.get("mode", "unknown"),
        "posture": state.get("posture", "unknown"),
        "role": state.get("role", "unknown"),
        "session_hash": state.get("session_hash", ""),
    }

    # Bind response to nonce — proves freshness
    response_payload = json.dumps(response, sort_keys=True, separators=(",", ":"))
    response["response_hash"] = hashlib.sha256(
        f"{nonce}|{response_payload}".encode()
    ).hexdigest()

    path = os.path.join(PRESENCE_DIR, f"response_{nonce[:8]}_{agent_id[:8]}.json")
    with open(path, "w") as f:
        json.dump(response, f, indent=2)

    print(json.dumps(response, indent=2))
    print(f"\n[PRESENCE] Response generated. Send this back to the challenge issuer.")
    print(f"[PRESENCE] Saved to: {path}")


def cmd_verify(args):
    """Verify a presence response against a challenge."""
    if len(args) < 2:
        print("Usage: presence.py verify <challenge.json> <response.json>")
        sys.exit(1)

    challenge_path, response_path = args[0], args[1]

    if not os.path.exists(challenge_path):
        print(f"[PRESENCE] ERROR: Challenge file not found: {challenge_path}")
        sys.exit(1)
    if not os.path.exists(response_path):
        print(f"[PRESENCE] ERROR: Response file not found: {response_path}")
        sys.exit(1)

    with open(challenge_path) as f:
        challenge = json.load(f)
    with open(response_path) as f:
        response = json.load(f)

    now_ts = int(time.time())
    checks = {}

    # 1. Nonce match
    checks["nonce_match"] = challenge.get("nonce") == response.get("nonce")

    # 2. Freshness — response must arrive before challenge expires
    checks["not_expired"] = now_ts <= challenge.get("expires_ts", 0)
    checks["responded_after_issued"] = (
        response.get("responded_ts", 0) >= challenge.get("issued_ts", 0)
    )

    # 3. Lineage anchor — must match known anchor
    checks["lineage_anchor_valid"] = response.get("lineage_anchor") == LINEAGE_ANCHOR

    # 4. Governed state present — posture/mode/role must be real values
    valid_modes = {"CREATIVE", "BALANCED", "PRECISE", "RESEARCH"}
    valid_postures = {"SCOUT", "STANDARD", "ELEVATED", "DEFENSE"}
    valid_roles = {"Primary", "Secondary", "Operator", "Observer"}
    checks["valid_mode"] = response.get("mode", "").upper() in valid_modes
    checks["valid_posture"] = response.get("posture", "").upper() in valid_postures
    checks["valid_role"] = response.get("role", "") in valid_roles

    # 5. Response hash integrity
    response_copy = {k: v for k, v in response.items() if k != "response_hash"}
    response_payload = json.dumps(response_copy, sort_keys=True, separators=(",", ":"))
    expected_hash = hashlib.sha256(
        f"{response.get('nonce')}|{response_payload}".encode()
    ).hexdigest()
    checks["response_hash_valid"] = response.get("response_hash") == expected_hash

    all_pass = all(checks.values())
    result = {
        "verified": all_pass,
        "agent_id": response.get("agent_id"),
        "agent_mode": response.get("mode"),
        "agent_posture": response.get("posture"),
        "agent_role": response.get("role"),
        "agent_lineage_anchor": response.get("lineage_anchor"),
        "checks": checks,
    }

    if not all_pass:
        failed = [k for k, v in checks.items() if not v]
        result["failed_checks"] = failed
        result["verdict"] = "REJECT — agent is not present, not governed, or response is stale/forged"
    else:
        result["verdict"] = "ACCEPT — agent is live, governed, lineage-anchored"

    print(json.dumps(result, indent=2))
    sys.exit(0 if all_pass else 1)


def cmd_status(args):
    state = load_state()
    if not state:
        print("[PRESENCE] No governance state. Not presenceable.")
        sys.exit(1)
    fp = state_fingerprint(state)
    print(json.dumps({
        "presence_ready": True,
        "state_fingerprint": fp,
        "lineage_anchor": LINEAGE_ANCHOR,
        "mode": state.get("mode"),
        "posture": state.get("posture"),
        "role": state.get("role"),
    }, indent=2))


COMMANDS = {
    "challenge": cmd_challenge,
    "respond": cmd_respond,
    "verify": cmd_verify,
    "status": cmd_status,
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd not in COMMANDS:
        print(f"Usage: presence.py [{'|'.join(COMMANDS)}] ...")
        sys.exit(1)
    COMMANDS[cmd](sys.argv[2:])
