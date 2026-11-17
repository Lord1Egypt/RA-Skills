#!/usr/bin/env python3
"""Record entering a mode, and the exact bytes of the mode file that was loaded.

modes/*.md is layer 1.5: loaded unconditionally on entering the mode, not "if
relevant". That distinction is only real if something reports its absence — a
reference file skipped is a silent deletion, which is the failure this whole
layering exists to avoid. So the mode's own gate requires this record, and
requires the hash to still match the file on disk.

Exit 0 = entered. Exit 2 = the mode file does not exist; a `mode_entry_failed`
record is written first, because a failed entry that left no trace looks exactly
like an entry nobody attempted — the same silence the record exists to break.

Exit 2 also, and with NOTHING written, when the WORKSPACE does not exist. This
script does not create it. paths.py and four separate gates carry the same
sentence about why — "a helper that created directories would materialise an
empty workspace on a typo, and the resume lookup would then find a shell" — and
this was the one script that defeated it, because journal.append() mkdirs. One
mistyped --workspace left a directory holding a single mode_entry line, which
`paths.workspace()`'s <company>-<role>-<date> lookup then finds by shape and
offers to resume from. Make the directory first; the mode files say so.

Usage: mkdir -p W && python3 scripts/enter_mode.py --workspace W --mode apply
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import doctor
import journal
import paths

MODES = ("discover", "assess", "apply", "interview")


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def latest_mode_entry(workspace, mode: str):
    path = pathlib.Path(workspace) / "journal.jsonl"
    if not path.exists():
        return None
    found = None
    for line in journal._decode(path).splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(rec, dict) and rec.get("action") == "mode_entry" \
                and rec.get("mode") == mode:
            found = rec
    return found


def _assessment_present(ws) -> bool:
    """Did an assessment happen in this workspace?

    Either artifact counts: the file assess mode writes, or a receipt from the
    gate that composes it. A run that assessed and a run that did not are
    otherwise indistinguishable at the end.
    """
    ws = pathlib.Path(ws)
    if (ws / "fit-assessment.yaml").is_file() or (ws / "fit-assessment.md").is_file():
        return True
    path = ws / "journal.jsonl"
    if not path.exists():
        return False
    for line in journal._decode(path).splitlines():
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(rec, dict) or rec.get("gate") != "check_assessment":
            continue
        # A DECIDED receipt only. `could_not_run` and `fail` mean the assessment
        # gate did not produce one, and counting them made `check_apply` suppress
        # its NO_ASSESSMENT notice — so a run whose assessment never ran read as
        # fit-assessed, and the completion message never said "no fit assessment
        # was made", which modes/apply.md requires it to say.
        if rec.get("verdict") in ("pass", "recorded"):
            return True
    return False


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--mode", required=True, choices=MODES)
    ap.add_argument("--skill-root", default=None)
    # Optional, and recorded either way. SKILL.md tells the model to decide the
    # mode from what the user asked and to SAY which one it picked -- but the
    # record only ever held the choice, never the inference behind it, so a wrong
    # mode produced a perfectly valid entry and nothing could see it. Not made
    # required: four mode docs and ten test files call this script, and breaking
    # them to force a field would cost more than the field is worth. Absence is
    # recorded as null so the gate can report it.
    ap.add_argument("--because", default=None,
                    help="one line: why this mode, from what the user asked")
    args = ap.parse_args(argv)
    missing = doctor.fast_capabilities()
    root = pathlib.Path(args.skill_root) if args.skill_root else paths.SKILL_ROOT
    path = paths.mode_file(args.mode, root)
    ws = pathlib.Path(args.workspace)
    # Checked BEFORE the mode file, because the mode-file branch journals — and
    # journaling into a workspace that is not there is what creates it.
    if not ws.is_dir():
        print(f"cannot enter mode {args.mode}: workspace {ws} does not exist. "
              f"Create it first (mkdir -p) — this script will not, because a typo "
              f"would leave an empty workspace that the resume lookup finds by name "
              f"and offers to continue from.", file=sys.stderr)
        return 2
    if not path.exists():
        journal.append(ws, {
            "ts": _now(),
            "action": "mode_entry_failed",
            "mode": args.mode,
            "mode_file": f"modes/{args.mode}.md",
            "reason": f"{path} does not exist",
        })
        print(f"cannot enter mode {args.mode}: {path} does not exist", file=sys.stderr)
        return 2
    journal.append(ws, {
        "ts": _now(),
        "action": "mode_entry",
        "mode": args.mode,
        "mode_file": f"modes/{args.mode}.md",
        "mode_file_sha256": journal.sha256_file(path),
        "because": (args.because.strip() or None) if args.because else None,
        # modes/apply.md, Entry conditions: an assessment SHOULD exist, and its
        # verdict decides how apply opens -- but running without one is allowed
        # provided the run "say[s] plainly that no fit assessment was made".
        # Recorded here rather than left to the model's memory, so check_apply
        # can state it at the end.
        "assessment_present": _assessment_present(ws),
        # Recorded on every entry because a capability the machine lacks
        # explains an output the user never got. `doctor.py` existed for a
        # week before this line and was named in SKILL.md and in no mode
        # file, so no run ever invoked it: a new user learned their machine
        # could not render a PDF when a PDF failed to appear. This is the
        # cheap half -- sound about what is missing, silent about what works.
        "capabilities_missing": missing,
    })
    if missing:
        print(f"NOTICE_MISSING_CAPABILITIES: {', '.join(missing)}. "
              f"Run `python3 scripts/doctor.py` for what each one costs and "
              f"how to install it. This mode still runs; some outputs will "
              f"not be produced.", file=sys.stderr)
    print(f"entered mode {args.mode}; read {path} in full before doing anything else")
    return 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    sys.exit(main())
