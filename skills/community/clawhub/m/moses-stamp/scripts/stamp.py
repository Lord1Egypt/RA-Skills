#!/usr/bin/env python3
"""
MO§ES™ Governed Output Stamp
Generates and appends a governance stamp to document content.
Usage:
  python3 stamp.py generate --mode <mode> --posture <posture> --role <role> --content <text>
  python3 stamp.py append --file <path> --mode <mode> --posture <posture> --role <role>
"""

import hashlib
import sys
import json
import os
import argparse
from datetime import datetime, timezone

STAMP_BLOCK = """\
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MO§ES™ GOVERNANCE STAMP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Produced under:  MO§ES™ Governance Framework
Mode:            {mode}
Posture:         {posture}
Role:            {role}
Session ID:      {session_id}
Action #:        {action_num}
Integrity hash:  {integrity_hash}
Runtime:         ClawHub (cryptographic)
© 2026 Ello Cello LLC — MO§ES™ is trademark pending
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

STATE_PATH = os.path.expanduser("~/.openclaw/governance/state.json")
STAMP_LOG = os.path.expanduser("~/.openclaw/governance/stamps.jsonl")


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH) as f:
            return json.load(f)
    return {}


def get_action_num():
    if not os.path.exists(STAMP_LOG):
        return 1
    with open(STAMP_LOG) as f:
        return sum(1 for _ in f) + 1


def compute_session_id(state):
    seed = state.get("session_start", datetime.now(timezone.utc).isoformat())
    return hashlib.sha256(seed.encode()).hexdigest()[:8]


def compute_integrity_hash(content, mode, posture, action_num):
    slug = (content[:64] + mode + posture + str(action_num)).encode()
    return hashlib.sha256(slug).hexdigest()


def generate_stamp(mode, posture, role, content=""):
    state = load_state()
    action_num = get_action_num()
    session_id = compute_session_id(state)
    integrity_hash = compute_integrity_hash(content, mode, posture, action_num)

    stamp = STAMP_BLOCK.format(
        mode=mode or state.get("mode", "Unrestricted"),
        posture=posture or state.get("posture", "None"),
        role=role or state.get("role", "Primary"),
        session_id=session_id,
        action_num=action_num,
        integrity_hash=integrity_hash,
    )

    # Log the stamp event
    os.makedirs(os.path.dirname(STAMP_LOG), exist_ok=True)
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "action_num": action_num,
        "integrity_hash": integrity_hash,
        "session_id": session_id,
    }
    with open(STAMP_LOG, "a") as f:
        f.write(json.dumps(record) + "\n")

    return stamp


def cmd_generate(args):
    stamp = generate_stamp(args.mode, args.posture, args.role, args.content or "")
    print(stamp)


def cmd_append(args):
    if not os.path.exists(args.file):
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    with open(args.file) as f:
        content = f.read()
    stamp = generate_stamp(args.mode, args.posture, args.role, content)
    with open(args.file, "a") as f:
        f.write("\n\n" + stamp + "\n")
    print(f"Stamp appended to {args.file}")


def main():
    parser = argparse.ArgumentParser(description="MO§ES™ governance stamp generator")
    sub = parser.add_subparsers(dest="cmd")

    gen = sub.add_parser("generate", help="Print a governance stamp")
    gen.add_argument("--mode", default="")
    gen.add_argument("--posture", default="")
    gen.add_argument("--role", default="Primary")
    gen.add_argument("--content", default="")

    app = sub.add_parser("append", help="Append stamp to a file")
    app.add_argument("--file", required=True)
    app.add_argument("--mode", default="")
    app.add_argument("--posture", default="")
    app.add_argument("--role", default="Primary")

    args = parser.parse_args()
    if args.cmd == "generate":
        cmd_generate(args)
    elif args.cmd == "append":
        cmd_append(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
