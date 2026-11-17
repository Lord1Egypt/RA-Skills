#!/usr/bin/env python3
"""trigger_log.py — 30-second habit trigger journal (JSONL).

Two entry types:
  event    — an occurrence of the behavior (or urge) you're tracking
  baseline — a random moment with NO urge (comparison denominator)

Keep entries honest and quick; the analyzer tolerates free text.
"""
import json
import os
import sys
import time
from pathlib import Path

DEFAULT_JOURNAL = os.path.join(os.path.expanduser("~"), "trigger_journal.jsonl")

PROMPTS_EVENT = [
    ("behavior", "behavior (e.g. vape/scroll/snack/skip-workout): ", str),
    ("location", "location (home/work/commute/other): ", str),
    ("company", "company (alone/partner/friends/colleagues): ", str),
    ("device", "device in hand (none/phone/laptop/tv): ", str),
    ("emotional_state", "emotional state 1(bad)-5(great): ", int),
    ("urge", "urge strength 1-5: ", int),
    ("prev_action", "what were you doing last 30 min: ", str),
]

PROMPTS_BASELINE = PROMPTS_EVENT[1:]  # everything except behavior label


def ask(prompts):
    row: dict = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
    for key, q, cast in prompts:
        while True:
            try:
                raw = input(q).strip()
                if cast is int:
                    v = int(raw)
                    if 1 <= v <= 5:
                        row[key] = v
                        break
                    print("  enter 1-5")
                else:
                    row[key] = raw.lower() or "other"
                    break
            except ValueError:
                print("  enter a number 1-5")
            except EOFError:
                return None
    return row


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("event", "baseline"):
        print(__doc__)
        print("usage: trigger_log.py event|baseline [journal.jsonl]")
        return 2
    mode = sys.argv[1]
    journal = Path(sys.argv[2] if len(sys.argv) > 2 else DEFAULT_JOURNAL)
    row = ask(PROMPTS_EVENT if mode == "event" else PROMPTS_BASELINE)
    if row is None:
        print("[aborted]")
        return 1
    row["type"] = mode
    with journal.open("a") as f:
        f.write(json.dumps(row) + "\n")
    print(f"logged {mode} -> {journal}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
