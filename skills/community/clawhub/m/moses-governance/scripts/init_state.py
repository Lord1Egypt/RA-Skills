#!/usr/bin/env python3
"""
MO§ES™ State Manager — Initialize and manage governance state
Usage:
  python3 init_state.py init                          ← First-run setup
  python3 init_state.py set --mode high-integrity
  python3 init_state.py set --posture defense
  python3 init_state.py set --role primary
  python3 init_state.py get                           ← Print current state
  python3 init_state.py reset                         ← Reset to defaults
"""

import argparse
import json
import os
from datetime import datetime, timezone

STATE_PATH = os.path.expanduser("~/.openclaw/governance/state.json")
AUDIT_DIR = os.path.expanduser("~/.openclaw/audits/moses")
AMENDMENTS_DIR = os.path.join(AUDIT_DIR, "amendments")

VALID_MODES = [
    "high-security",
    "high-integrity",
    "creative",
    "research",
    "self-growth",
    "problem-solving",
    "idk",
    "unrestricted"
]

VALID_POSTURES = ["scout", "defense", "offense"]
VALID_ROLES = ["primary", "secondary", "observer", "broadcast"]

DEFAULT_STATE = {
    "mode": "high-integrity",
    "posture": "defense",
    "role": "primary",
    "vault": [],
    "session_hash": None,
    "initialized_at": None,
    "last_updated": None
}


def ensure_dirs():
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    os.makedirs(AUDIT_DIR, exist_ok=True)
    os.makedirs(AMENDMENTS_DIR, exist_ok=True)


def load_state():
    if not os.path.exists(STATE_PATH):
        return None
    with open(STATE_PATH) as f:
        return json.load(f)


def save_state(state):
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def cmd_init(args):
    ensure_dirs()
    if os.path.exists(STATE_PATH) and not getattr(args, "force", False):
        state = load_state()
        print(f"[INIT] State already exists. Mode: {state['mode']} | Posture: {state['posture']} | Role: {state['role']}")
        print("[INIT] Use --force to reinitialize.")
        return

    state = DEFAULT_STATE.copy()
    state["initialized_at"] = datetime.now(timezone.utc).isoformat()
    save_state(state)

    # Create empty ledger if not exists
    ledger = os.path.join(AUDIT_DIR, "audit_ledger.jsonl")
    if not os.path.exists(ledger):
        open(ledger, "w").close()

    print("[INIT] MO§ES™ governance initialized.")
    print(f"  State: {STATE_PATH}")
    print(f"  Audit: {ledger}")
    print(f"  Amendments: {AMENDMENTS_DIR}")
    print(f"  Mode: {state['mode']} | Posture: {state['posture']} | Role: {state['role']}")
    print("\n[INIT] To change: python3 init_state.py set --mode high-security --posture scout")


def cmd_set(args):
    ensure_dirs()
    state = load_state() or DEFAULT_STATE.copy()

    if args.mode:
        if args.mode not in VALID_MODES:
            print(f"[ERROR] Invalid mode '{args.mode}'. Valid: {', '.join(VALID_MODES)}")
            return
        state["mode"] = args.mode
        print(f"[SET] Mode → {args.mode}")

    if args.posture:
        if args.posture not in VALID_POSTURES:
            print(f"[ERROR] Invalid posture '{args.posture}'. Valid: {', '.join(VALID_POSTURES)}")
            return
        state["posture"] = args.posture
        print(f"[SET] Posture → {args.posture}")

    if args.role:
        if args.role not in VALID_ROLES:
            print(f"[ERROR] Invalid role '{args.role}'. Valid: {', '.join(VALID_ROLES)}")
            return
        state["role"] = args.role
        print(f"[SET] Role → {args.role}")

    save_state(state)
    print(f"[STATE] mode={state['mode']} | posture={state['posture']} | role={state['role']}")


def cmd_get(args):
    state = load_state()
    if not state:
        print("[ERROR] No state found. Run: python3 init_state.py init")
        return
    print(json.dumps(state, indent=2))


def cmd_reset(args):
    ensure_dirs()
    state = DEFAULT_STATE.copy()
    state["initialized_at"] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    print("[RESET] Governance state reset to defaults.")
    print(f"  Mode: {state['mode']} | Posture: {state['posture']} | Role: {state['role']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MO§ES™ Governance State Manager")
    subparsers = parser.add_subparsers(dest="command")

    init_p = subparsers.add_parser("init", help="Initialize governance state (first run)")
    init_p.add_argument("--force", action="store_true", help="Reinitialize even if state exists")

    set_p = subparsers.add_parser("set", help="Set governance state values")
    set_p.add_argument("--mode", help=f"Governance mode: {', '.join(VALID_MODES)}")
    set_p.add_argument("--posture", help=f"Posture: {', '.join(VALID_POSTURES)}")
    set_p.add_argument("--role", help=f"Role: {', '.join(VALID_ROLES)}")

    get_p = subparsers.add_parser("get", help="Print current governance state")
    reset_p = subparsers.add_parser("reset", help="Reset state to defaults")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args)
    elif args.command == "set":
        cmd_set(args)
    elif args.command == "get":
        cmd_get(args)
    elif args.command == "reset":
        cmd_reset(args)
    else:
        parser.print_help()
