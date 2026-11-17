#!/usr/bin/env python3
"""
Long-horizon research session state machine (mid-proof persistence).

A hard proof takes many sessions. Context is lost between them; the same dead
ends get re-explored. This script persists the state of a long attempt:
the goal, every attempt made, what killed it, and the next concrete action.

Rules enforced:
  - an attempt must record an outcome (success / failure / inconclusive);
  - a failed attempt must record WHY (otherwise the dead end is lost);
  - `--resume` always prints the last checkpoint and the next action first.

Usage:
    python long_horizon_session.py --start "prove C(d,n) = A_leq d(n)" -d ./session
    python long_horizon_session.py -d ./session --attempt "LP duality on the envelope" \
        --outcome failure --why "dual is unbounded; envelope not polyhedral"
    python long_horizon_session.py -d ./session --checkpoint "reduced to d=2 case"
    python long_horizon_session.py -d ./session --resume
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

FILE = "session.json"
OUTCOMES = ("success", "failure", "inconclusive")


def load(d: Path) -> dict:
    p = d / FILE
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def save(d: Path, data: dict) -> None:
    d.mkdir(parents=True, exist_ok=True)
    data["updated"] = datetime.now().isoformat(timespec="seconds")
    (d / FILE).write_text(json.dumps(data, indent=2), encoding="utf-8")


def require(d: Path) -> dict:
    data = load(d)
    if data is None:
        print("error: no session here. Start one with --start \"<goal>\"", file=sys.stderr)
        sys.exit(2)
    return data


def main() -> int:
    ap = argparse.ArgumentParser(description="Long-horizon research session tracker")
    ap.add_argument("-d", "-p", "--dir", default="./session")
    ap.add_argument("--start", metavar="GOAL")
    ap.add_argument("--attempt", metavar="DESC")
    ap.add_argument("--outcome", choices=OUTCOMES)
    ap.add_argument("--why", default="")
    ap.add_argument("--checkpoint", metavar="STATE")
    ap.add_argument("--next", metavar="ACTION")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    d = Path(args.dir).expanduser().resolve()

    if args.start:
        save(d, {"goal": args.start,
                 "created": datetime.now().isoformat(timespec="seconds"),
                 "updated": None,
                 "attempts": [], "checkpoints": [], "next_action": None})
        print(f"session started: {args.start}")
        return 0

    data = require(d)

    if args.attempt:
        if not args.outcome:
            print("error: --outcome required with --attempt", file=sys.stderr)
            return 2
        if args.outcome == "failure" and not args.why.strip():
            print("error: a failed attempt must record --why "
                  "(otherwise the dead end is lost and will be re-walked)", file=sys.stderr)
            return 2
        data["attempts"].append({
            "n": len(data["attempts"]) + 1,
            "description": args.attempt,
            "outcome": args.outcome,
            "why": args.why or None,
            "at": datetime.now().isoformat(timespec="seconds"),
        })
        save(d, data)
        print(f"attempt {len(data['attempts'])} recorded ({args.outcome})")
        return 0

    if args.checkpoint:
        data["checkpoints"].append({"state": args.checkpoint,
                                    "at": datetime.now().isoformat(timespec="seconds")})
        save(d, data)
        print(f"checkpoint saved ({len(data['checkpoints'])} total)")
        return 0

    if args.next:
        data["next_action"] = args.next
        save(d, data)
        print(f"next action set: {args.next}")
        return 0

    if args.resume or args.status:
        ok = sum(1 for a in data["attempts"] if a["outcome"] == "success")
        fail = [a for a in data["attempts"] if a["outcome"] == "failure"]
        print(f"GOAL      : {data['goal']}")
        print(f"Updated   : {data.get('updated')}")
        print(f"Attempts  : {len(data['attempts'])} (success {ok}, failure {len(fail)})")
        if data["checkpoints"]:
            print(f"LAST STATE: {data['checkpoints'][-1]['state']}")
        print(f"NEXT      : {data.get('next_action') or '(none set - set one with --next)'}")
        if fail:
            print("\nDead ends already explored (do not repeat):")
            for a in fail:
                print(f"  - #{a['n']} {a['description']}")
                print(f"      why: {a.get('why')}")
        return 0

    print("nothing to do; try --resume")
    return 0


if __name__ == "__main__":
    sys.exit(main())
