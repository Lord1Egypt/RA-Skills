#!/usr/bin/env python3
"""Gate: the judges must have read the files that are on disk now.

Re-judging a stale cv.md produces a verdict block that is completely valid and
*self-confirming* — the judges hand back the same feedback that was supposedly
just addressed, so the loop looks like it is working while nothing changes. No
timestamp, hash or artifact tied a verdict to the file version it judged, which
is why the per-round order (edit → re-render → re-judge) had no backstop at all.

Two modes, in this order:
  --record FILE...  at dispatch, before the judges are spawned
  (no --record)     after the verdicts arrive; a mismatch voids the round

Exit 0 = fresh / recorded. Exit 1 = stale. Exit 2 = nothing to check.
"""
from __future__ import annotations

import argparse
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import journal
import rounds

GATE = "check_render_freshness"


def _rel(ws: pathlib.Path, p: pathlib.Path) -> str:
    try:
        return p.resolve().relative_to(ws.resolve()).as_posix()
    except ValueError:
        return str(p.resolve())


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--round", type=int, required=True)
    ap.add_argument("--record", nargs="+", default=None, metavar="FILE",
                    help="hash these files now, before dispatching the judges")
    args = ap.parse_args(argv)
    ws = pathlib.Path(args.workspace)
    if not ws.is_dir():
        # journal.receipt() would mkdir it, and a gate that creates the
        # workspace it is auditing has manufactured its own evidence.
        print(f"cannot run {GATE}: workspace {ws} does not exist", file=sys.stderr)
        return 2

    if args.record is not None:
        hashes = {}
        for raw in args.record:
            p = pathlib.Path(raw)
            if not p.exists():
                journal.receipt(ws, GATE, {}, "could_not_run", [f"MISSING_INPUT: {p}"])
                print(f"cannot run {GATE}: {p} does not exist", file=sys.stderr)
                return 2
            hashes[_rel(ws, p)] = journal.sha256_file(p)
        rounds.merge_round(ws, args.round, {"dispatch": {
            "ts": datetime.datetime.now(datetime.timezone.utc)
                          .strftime("%Y-%m-%dT%H:%M:%SZ"),
            "input_hashes": hashes,
        }})
        # "baseline_recorded", not "recorded". This gate's two receipts are
        # otherwise identical — same gate, same input hashes, same shape — so the
        # verdict is the ONLY thing that can tell "hashed the files before
        # dispatch" from "confirmed the judges read what is on disk now". Sharing
        # one token let a round that was recorded and never verified satisfy
        # check_apply.py, which is the substitution this gate exists to prevent.
        journal.receipt(ws, GATE, hashes, "baseline_recorded", [])
        return 0

    dispatch = (rounds.load_round(ws, args.round) or {}).get("dispatch") or {}
    recorded = dispatch.get("input_hashes") or {}
    if not recorded:
        journal.receipt(ws, GATE, {}, "could_not_run",
                        [f"NO_DISPATCH_RECORD: round {args.round}"])
        print(f"cannot run {GATE}: NO_DISPATCH_RECORD — judge-round-{args.round}.json "
              f"has no dispatch hashes, so nothing vouches for what the judges read. "
              f"Re-render, re-record with --record, and re-dispatch.", file=sys.stderr)
        return 2

    findings, now = [], {}
    for rel, was in sorted(recorded.items()):
        p = pathlib.Path(rel)
        if not p.is_absolute():
            p = ws / rel
        if not p.exists():
            findings.append(f"MISSING_FILE: {rel} was hashed at dispatch but is gone "
                            f"from disk — this round is void")
            continue
        now[rel] = journal.sha256_file(p)
        if now[rel] != was:
            findings.append(f"STALE: {rel} hashed {was[:12]}… at dispatch != "
                            f"{now[rel][:12]}… on disk — this round is void; "
                            f"re-render, re-record and re-dispatch all three judges")
    for f in findings:
        print(f)
    journal.receipt(ws, GATE, now, "fail" if findings else "pass", findings)
    return 1 if findings else 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    sys.exit(main())
