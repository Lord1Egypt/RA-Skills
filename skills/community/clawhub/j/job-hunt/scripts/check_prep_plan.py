#!/usr/bin/env python3
"""Gate for a preparation plan.

Usage:
    python3 scripts/check_prep_plan.py --workspace <workspace>

Two plans, one format. In a prepare workspace (`<profile>/prep/<date>-<direction>/`)
the plan is the general one, `prep-plan.md`, built from the target direction and the
CV. In an interview workspace it is `mock/prep-plan.md`, the posting's additions to
that general plan. Where the workspace lives decides which file is read.

One `## <topic>` entry each, most important first. Every entry carries:

    - why: direction: "<words copied from direction.yaml>"
           | posting: "<words copied from posting.yaml>"
           | cv: "<words copied from cv.md>"
           | shape: <the market or role-family row in references/interview-shapes.md>
           | family: <the area in references/preparation.md §4>
    - be able to: <what the candidate must be able to do or explain, concretely>
    - practise: knowledge | coding | behavioural | case | role-play | presentation
                | design | self-study

The failure this exists for is the generic plan: "LeetCode top 150 and system
design" handed to a nurse, or a US behavioural list handed to a Dutch candidate. A
quoted reason must be words that are really in that file, so a topic cannot claim
the posting, the CV or the stated direction asks for it when it does not.

exit 0 — the plan holds up. exit 1 — findings on stdout. exit 2 — could not run
(including a missing or empty plan).
Every exit except a missing workspace appends one receipt to journal.jsonl.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import check_mock
import journal
import mock_blocks as MB
import paths

GATE = "check_prep_plan"
PRACTISE = ("knowledge", "coding", "behavioural", "case", "role-play", "presentation",
            "design", "self-study")
WHY_KINDS = ("direction", "posting", "cv", "shape", "family")
# The files a quoted reason is checked against. A kind whose file is absent in this
# workspace (no posting.yaml in a prepare session) fails PREP_WHY_NO_SOURCE.
QUOTED_SOURCES = {"direction": "direction.yaml", "posting": "posting.yaml", "cv": "cv.md"}


def is_prep_workspace(workspace: pathlib.Path) -> bool:
    """Decided by where the workspace is (paths.prep_workspace), not by the journal:
    a session that never recorded its mode entry must still be read as the plan it
    is, so the missing entry is reported as NO_MODE_ENTRY rather than as a missing
    plan in the wrong directory."""
    return pathlib.Path(workspace).parent.name == "prep"


def plan_path(workspace: pathlib.Path) -> pathlib.Path:
    """The general plan in a prepare workspace, the posting delta elsewhere."""
    if is_prep_workspace(workspace):
        return workspace / paths.PREP_PLAN_NAME
    return workspace / "mock" / paths.PREP_PLAN_NAME

# `[ \t]`, never `\s`, for the reason check_mock gives: `\s` crosses the newline and
# an empty field borrows the next bullet.
_HEADING = re.compile(r"^##[ \t]+(.+?)[ \t]*$", re.M)
_FIELD = {name: re.compile(r"^[ \t]*-[ \t]*" + name + r":[ \t]*(\S.*?)[ \t]*$", re.M)
          for name in ("why", "be able to", "practise")}
_QUOTED = re.compile(r"^[\"“'‘](.+)[\"”'’]$")


def _norm(text: str) -> str:
    return MB.collapse_ws(text).casefold()


class InputMissing(RuntimeError):
    """The plan itself is absent — there is nothing to check."""


def check_plan(workspace: pathlib.Path, path: pathlib.Path | None = None) -> list:
    """Findings for the plan at `path` (default: where plan_path() puts it), with
    quoted reasons checked against the files beside it in `workspace`."""
    path = path or plan_path(workspace)
    if not path.is_file() or not path.read_text(encoding="utf-8").strip():
        raise InputMissing(f"NO_PREP_PLAN: {path} is missing or empty — nothing to check")
    text = path.read_text(encoding="utf-8")
    marks = list(_HEADING.finditer(text))
    if not marks:
        return [f"NO_PREP_TOPICS: {path.name} has no '## ' topic entries"]
    sources = {kind: workspace / name for kind, name in QUOTED_SOURCES.items()}
    findings = []
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(text)
        body, topic = text[mark.end():end], mark.group(1)
        found = {name: rx.search(body) for name, rx in _FIELD.items()}
        if not found["be able to"]:
            findings.append(
                f"PREP_NO_ABILITY: topic {topic!r} has no '- be able to:' line — a "
                "topic name alone is a reading list, not preparation")
        practise = found["practise"].group(1) if found["practise"] else ""
        if practise not in PRACTISE:
            findings.append(
                f"PREP_BAD_PRACTISE: topic {topic!r} needs '- practise:' with one of "
                + " | ".join(PRACTISE))
        if not found["why"]:
            findings.append(
                f"PREP_NO_WHY: topic {topic!r} has no '- why:' line, so nothing ties "
                "it to this posting, this CV or this loop")
            continue
        kind, _, reason = found["why"].group(1).partition(":")
        kind, reason = kind.strip().lower(), reason.strip()
        if kind not in WHY_KINDS or not reason:
            findings.append(
                f"PREP_BAD_WHY: topic {topic!r}: '- why:' must start with one of "
                + ", ".join(k + ":" for k in WHY_KINDS) + " and give the reason")
            continue
        if kind not in sources:
            continue
        quoted = _QUOTED.match(reason)
        source = sources[kind]
        if not quoted:
            findings.append(
                f"PREP_WHY_UNQUOTED: topic {topic!r}: a {kind}: reason must quote the "
                f"words from {source.name} in quotation marks")
        elif not source.is_file():
            findings.append(
                f"PREP_WHY_NO_SOURCE: topic {topic!r} quotes {source.name}, which is "
                "not in the workspace")
        elif _norm(quoted.group(1)) not in _norm(source.read_text(encoding="utf-8")):
            findings.append(
                f"PREP_WHY_NOT_IN_SOURCE: topic {topic!r} quotes {quoted.group(1)!r}, "
                f"which is not in {source.name} — the plan may not claim the "
                f"{source.name} says what it does not")
    return findings


def run(workspace, skill_root=None, vocab_scanner=None) -> list:
    workspace = pathlib.Path(workspace)
    skill_root = pathlib.Path(skill_root) if skill_root else paths.SKILL_ROOT
    scanner = (check_mock._default_scanner(workspace) if vocab_scanner is None
               else vocab_scanner)
    findings = check_mock.check_mode_entry(
        workspace, skill_root, "prepare" if is_prep_workspace(workspace) else check_mock.MODE)
    findings += check_plan(workspace)
    plan = plan_path(workspace)
    findings += check_mock.check_vocabulary([plan], scanner, code_ok=(plan,))
    return findings


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Gate for mock/prep-plan.md.")
    parser.add_argument("--workspace", required=True, type=pathlib.Path)
    parser.add_argument("--skill-root", type=pathlib.Path, default=None)
    args = parser.parse_args(argv)
    if not args.workspace.is_dir():
        print(f"cannot run {GATE}: workspace {args.workspace} does not exist",
              file=sys.stderr)
        return 2
    plan = plan_path(args.workspace)
    inputs = {plan.relative_to(args.workspace).as_posix(): plan,
              **{name: args.workspace / name for name in QUOTED_SOURCES.values()}}
    hashes = {k: journal.sha256_file(p) for k, p in inputs.items() if p.exists()}
    try:
        findings = run(args.workspace, skill_root=args.skill_root)
    except (InputMissing, check_mock.MissingDependency, OSError, UnicodeError) as exc:
        print(str(exc), file=sys.stderr)
        try:
            journal.receipt(args.workspace, GATE, hashes, "could_not_run", [str(exc)])
        except OSError as fail:
            print(f"RECEIPT_WRITE_FAILED: {fail}", file=sys.stderr)
        return 2
    try:
        journal.receipt(args.workspace, GATE, hashes, "fail" if findings else "pass",
                        findings)
    except OSError as fail:
        print(f"RECEIPT_WRITE_FAILED: could not append the {GATE} receipt: {fail}",
              file=sys.stderr)
        return 2
    for finding in findings:
        print(finding)
    return 1 if findings else 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    raise SystemExit(main())
