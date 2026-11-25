#!/usr/bin/env python3
"""Gate for one prepare-mode drill: a knowledge or coding round with no posting.

Usage:
    python3 scripts/check_drill.py --workspace <prep workspace> --round <n>

A drill has no posting, no tailored CV to defend and no claims.yaml, so the parts of
check_mock that exist for those (coverage per must-have, the provenance pass, the
answer bank, the walk-back list) do not apply. What does apply is reused from
check_mock unchanged: quotes must come from the cited answer, every question gets
its RECALL / SOLVE row, the hint level is the one the transcript logs, a SOLVE
row's tests= is what run_mock_tests.py recorded for the code on disk, and the study
notes cover every question and predict no outcome.

exit 0 — the drill holds up. exit 1 — findings on stdout. exit 2 — could not run.
Every exit except a missing workspace appends one receipt to journal.jsonl.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import check_mock
import journal
import mock_blocks as MB
import mock_vocab as V
import paths

GATE = "check_drill"
MODE = "prepare"


def check_drill(workspace: pathlib.Path, round_no: int, transcript_text: str,
                assessment_text: str) -> list:
    findings: list = []
    if MB.ASSESSMENT not in assessment_text:
        return ["MISSING_BLOCK: MOCK-ASSESSMENT-V1 — the transcript pass did not run, or "
                "its block was not copied into the file verbatim"]
    try:
        block = MB.parse_block(assessment_text, MB.ASSESSMENT)
    except MB.BlockParseError as exc:
        return [f"PARSE_FAIL: {exc} — re-dispatch the pass rather than hand-editing it"]
    refs = check_mock.transcript_refs(transcript_text)
    if not refs:
        findings.append(
            "NO_QUESTION_HEADINGS: the transcript has no '## Q<n>' headings, so no "
            "row can be checked against the answer it cites")
    check_mock._check_headers(block, round_no, findings)
    round_type = block.header.get("ROUND-TYPE", "")
    if round_type not in V.LEARNED_ROUND_TYPES:
        findings.append(
            f"DRILL_ROUND_TYPE: ROUND-TYPE: {round_type!r} — a prepare drill is "
            + " or ".join(V.LEARNED_ROUND_TYPES)
            + "; a story, role-play or case round needs a posting (interview mode)")
    for record in block.records:
        if record.kind == "FINDING":
            check_mock._check_tag(record, block, findings)
            check_mock._check_quote(record, block.kind, transcript_text, refs, findings)
        elif record.kind in ("RECALL", "SOLVE"):
            check_mock._check_quote(record, block.kind, transcript_text, refs, findings)
        elif record.kind == "BAND":
            findings.append(
                f"BAND_IN_DRILL: line {record.line_no}: a drill is assessed per question "
                "with RECALL / SOLVE, not banded on the experience dimensions")
    findings += check_mock.check_learned_records(block, transcript_text, workspace, round_no)
    findings += check_mock.check_study_notes(workspace / "mock", round_no, transcript_text,
                                             round_type)
    return findings


def run(workspace, round_no: int, skill_root=None, vocab_scanner=None) -> list:
    workspace = pathlib.Path(workspace)
    skill_root = pathlib.Path(skill_root) if skill_root else paths.SKILL_ROOT
    transcript = workspace / "mock" / f"transcript-{round_no}.md"
    assessment = workspace / "mock" / f"assessment-{round_no}.md"
    for path in (transcript, assessment):
        if not path.is_file():
            raise check_mock.InputMissing(f"{path} is missing — nothing to check")
    transcript_text = transcript.read_text(encoding="utf-8")
    scanner = (check_mock._default_scanner(workspace) if vocab_scanner is None
               else vocab_scanner)
    notes = check_mock.study_notes_path(workspace / "mock", round_no)
    findings = check_mock.check_mode_entry(workspace, skill_root, MODE)
    findings += check_drill(workspace, round_no, transcript_text,
                            assessment.read_text(encoding="utf-8"))
    findings += check_mock.check_vocabulary([assessment, notes], scanner, code_ok=(notes,))
    return findings


def _inputs(workspace: pathlib.Path, round_no: int) -> dict:
    mock = workspace / "mock"
    found = {f"mock/transcript-{round_no}.md": mock / f"transcript-{round_no}.md",
             f"mock/assessment-{round_no}.md": mock / f"assessment-{round_no}.md",
             f"mock/study-notes-{round_no}.md": check_mock.study_notes_path(mock, round_no)}
    for path in sorted((mock / "code" / f"round-{round_no}").glob("*/result.json")):
        found[path.relative_to(workspace).as_posix()] = path
    return found


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Gate for one prepare-mode drill.")
    parser.add_argument("--workspace", required=True, type=pathlib.Path)
    parser.add_argument("--round", required=True, type=int)
    parser.add_argument("--skill-root", type=pathlib.Path, default=None)
    args = parser.parse_args(argv)
    if not args.workspace.is_dir():
        print(f"cannot run {GATE}: workspace {args.workspace} does not exist",
              file=sys.stderr)
        return 2
    hashes = {k: journal.sha256_file(p)
              for k, p in _inputs(args.workspace, args.round).items() if p.exists()}
    try:
        findings = run(args.workspace, args.round, skill_root=args.skill_root)
    except (check_mock.InputMissing, check_mock.MissingDependency, OSError,
            UnicodeError) as exc:
        print(str(exc), file=sys.stderr)
        try:
            journal.receipt(args.workspace, GATE, hashes, "could_not_run", [str(exc)],
                            extra={"round": args.round})
        except OSError as fail:
            print(f"RECEIPT_WRITE_FAILED: {fail}", file=sys.stderr)
        return 2
    try:
        journal.receipt(args.workspace, GATE, hashes, "fail" if findings else "pass",
                        findings, extra={"round": args.round})
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
