#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""breaker.py — runnable loop circuit-breaker for keelwright (T15, v1.8.0).

WHY: SKILL.md documents 4 caps (MAX_ITERS=50, no-progress=5, wall-clock=2h,
similarity=3x). Those are run-contract parameters an agent reads, but nothing
*enforces* them machine-side. This script is the enforceable counterpart: a
file-backed counter that a loop driver calls once per iteration; it STOPs the
loop when any cap is hit and writes `.loop_stopped` so a crashed run leaves proof.

USAGE:
  python breaker.py --iter            # call once per iteration; exits non-zero if should stop
  python breaker.py --reset           # clear state (new goal)
  python breaker.py --status          # print current counters

State lives in .keelwright_loop_state.json next to CWD (or $KEELWRIGHT_LOOP_STATE).
"""
import argparse
import json
import os
import sys
import time

DEFAULT_STATE = os.path.join(os.getcwd(), ".keelwright_loop_state.json")

# Caps (mirror SKILL.md circuit-breaker table)
MAX_ITERS = int(os.environ.get("KEELWRIGHT_MAX_ITERS", "50"))
ABSOLUTE_MAX_ITERS = int(os.environ.get("KEELWRIGHT_ABSOLUTE_MAX_ITERS", "100"))
NO_PROGRESS_CAP = int(os.environ.get("KEELWRIGHT_NO_PROGRESS_CAP", "5"))
WALL_CLOCK_SEC = int(os.environ.get("KEELWRIGHT_WALL_CLOCK_SEC", "7200"))
SIMILARITY_CAP = int(os.environ.get("KEELWRIGHT_SIMILARITY_CAP", "3"))


def _state_path() -> str:
    return os.environ.get("KEELWRIGHT_LOOP_STATE", DEFAULT_STATE)


def load() -> dict:
    p = _state_path()
    if os.path.exists(p):
        try:
            with open(p, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"iters": 0, "no_progress": 0, "start": time.time(), "similar": 0, "stopped": False}


def save(s: dict) -> None:
    with open(_state_path(), "w", encoding="utf-8") as f:
        json.dump(s, f)


def reset() -> None:
    s = {"iters": 0, "no_progress": 0, "start": time.time(), "similar": 0, "stopped": False}
    save(s)
    print("loop state reset")


def status() -> None:
    s = load()
    print(json.dumps(s, ensure_ascii=False))


def iter(progress: bool) -> int:
    """Call once per iteration. Returns exit code: 0 = continue, 1 = STOP."""
    s = load()
    if s.get("stopped"):
        print("CIRCUIT-BREAKER: already stopped. Refusing to continue.")
        return 1
    s["iters"] += 1
    if progress:
        s["no_progress"] = 0
    else:
        s["no_progress"] += 1
    elapsed = time.time() - s.get("start", time.time())

    reasons = []
    hard_cap = min(MAX_ITERS, ABSOLUTE_MAX_ITERS)
    if s["iters"] >= hard_cap:
        reasons.append(f"hard cap {s['iters']}>={hard_cap}")
    if s["no_progress"] >= NO_PROGRESS_CAP:
        reasons.append(f"no-progress cap ({s['no_progress']}>={NO_PROGRESS_CAP})")
    if elapsed >= WALL_CLOCK_SEC:
        reasons.append(f"wall-clock ({elapsed:.0f}s>={WALL_CLOCK_SEC}s)")
    if s.get("similar", 0) >= SIMILARITY_CAP:
        reasons.append(f"similarity ({s['similar']}>={SIMILARITY_CAP})")

    if reasons:
        s["stopped"] = True
        save(s)
        # Proof a crashed run left behind
        try:
            proof = {
                "iter": s["iters"],
                "reason": "; ".join(reasons),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            with open(os.path.join(os.path.dirname(_state_path()), ".loop_stopped"), "w", encoding="utf-8") as f:
                json.dump(proof, f, ensure_ascii=False)
        except Exception:
            pass
        print("CIRCUIT-BREAKER FIRED: " + "; ".join(reasons) + ". STOP.")
        return 1
    save(s)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--iter", action="store_true", help="register one iteration (pass --progress for keep/green)")
    ap.add_argument("--progress", action="store_true", help="this iteration made progress (resets no-progress)")
    ap.add_argument("--similar", action="store_true", help="mark a similarity repeat (3x -> stop)")
    ap.add_argument("--reset", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    if args.reset:
        reset()
        return 0
    if args.status:
        status()
        return 0
    if args.iter:
        s = load()
        if args.similar:
            s["similar"] = s.get("similar", 0) + 1
            save(s)
        return iter(args.progress)
    if args.similar:
        # Allow similarity check without registering a full iteration.
        s = load()
        s["similar"] = s.get("similar", 0) + 1
        save(s)
        return iter(progress=False)
    # default: status
    status()
    return 0


if __name__ == "__main__":
    sys.exit(main())
