#!/usr/bin/env python3
"""Idempotent dual-store eval bridge for OCAS dispatch closure.

Appends each relpath to BOTH the praxis-eval store (key `journal_id`) and the
dispatch-eval store (key `filename`), skipping any already present (substring
guard). Corrected 2026-07-15: the `--action` value is consumed by argparse and
NEVER treated as a relpath (the historical --action-leak bug).

Phantom guard: if a relpath does NOT exist on disk under the journals tree, it is
SKIPPED with a warning instead of bridged -- bridging a non-existent file creates
a phantom eval entry (see ocas-forge references/session-20260715-mixed-wave-
closure.md, "Dispatch-wave journal MUST be written BEFORE it is bridged").

Usage:
  python3 scripts/bridge_eval_inline.py REL1 REL2 REL3 --action my_label
  python3 scripts/bridge_eval_inline.py REL1 --require-exists   # skip missing files
"""
import os, sys, json, argparse

PROFILE = os.environ.get("HERMES_HOME", os.environ.get("HERMES_HOME", os.path.join(os.path.expanduser("~"), ".hermes", "profiles", "indigo")))
JDIR = os.path.join(PROFILE, "commons", "journals")
PRAXIS_EV = os.path.join(PROFILE, "commons", "data", "ocas-praxis", "journals_evaluated.jsonl")
DISPATCH_EV = os.path.join(PROFILE, "commons", "data", "ocas-dispatch", "journals_evaluated.jsonl")


def append_unique(fpath, key_field, key_val, action_taken, source):
    if not os.path.exists(fpath):
        print(f"WARN: eval file missing: {fpath}")
        return False
    with open(fpath) as f:
        for line in f:
            if key_val in line:
                return False
    with open(fpath, "a") as f:
        f.write(json.dumps({key_field: key_val, "action_taken": action_taken,
                            "source": source}) + "\n")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Idempotently bridge relative journal paths into BOTH the praxis-eval "
                    "and dispatch-eval stores, skipping entries already present.",
        epilog="Examples:\n"
               "  python3 bridge_eval_inline.py REL1 REL2 --action my_label\n"
               "  python3 bridge_eval_inline.py REL1 --require-exists\n"
               "Put --action LAST in the argument list (its value is consumed, never treated as a relpath).")
    parser.add_argument("rels", nargs="*", help="relative journal paths to bridge "
                                               "(e.g. ocas-forge/2026-07-16/forge-scan-TS.json)")
    parser.add_argument("--action", default="manual_bridge",
                        help="action_taken label written to both eval stores (place LAST)")
    parser.add_argument("--require-exists", action="store_true",
                        help="skip (with a warning) any relpath whose file is missing on disk "
                             "(prevents phantom eval entries)")
    args = parser.parse_args()
    added = 0
    for rel in args.rels:
        disk = os.path.join(JDIR, rel)
        if args.require_exists and not os.path.exists(disk):
            print(f"SKIP (missing on disk): {rel}")
            continue
        a1 = append_unique(PRAXIS_EV, "journal_id", rel, args.action, "bridge_eval_inline")
        a2 = append_unique(DISPATCH_EV, "filename", rel, args.action, "bridge_eval_inline")
        if a1 or a2:
            added += 1
            print(f"bridged {rel} (praxis={a1} dispatch={a2})")
    print(f"total bridged: {added}")


if __name__ == "__main__":
    main()