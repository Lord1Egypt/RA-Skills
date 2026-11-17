#!/usr/bin/env python3
"""Resolve every evidence reference, drop the ones that do not resolve, and keep
block ids out of the prose a reader actually sees.

Dropping rather than failing is the whole design. An empty evidence list is not an
error: rejecting it discards an honest analysis, while an INVENTED ref lands in that
same empty array and sails through. Punishing the honest shape and passing the
dishonest one is exactly backwards, so both land on [].

Stripping ids from prose is belt-and-braces. The mode file asks the model not to write
them there and it mostly complies, which is exactly the problem: a rule that holds most
of the time still ships the defect, and only this layer can stop it. Grounding is
unaffected -- refs travel in the evidence lists, and in the requirement table, which is
the one place a reader is meant to see them because it is what makes the denominator
auditable.

Exit 2 still writes a receipt, verdict "could_not_run". The single exception is a
workspace directory that does not exist: there is nothing to append to, and creating it
would leave a journal for a run that never happened.

A clean run's verdict is "recorded" whether or not --check-only was passed. The same
state must never produce two different verdicts: the composer that reads this receipt
-- check_assessment.py, not check_apply.py -- has PASSING_VERDICTS ("pass", "recorded"),
so a second spelling of "this was fine" reads downstream as a failure. Note the other
direction too: "recorded" here means "ran, nothing to report". A gate whose clean path
stores a baseline instead of checking one writes "baseline_recorded" -- see
journal.VERDICTS for why the two must not share a token.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import journal  # noqa: E402
import yaml  # noqa: E402

GATE = "check_evidence_refs"

# NOT `\b`: there is no word boundary between a CJK character and `C`, because
# both are word characters to `re`. So `见CV-001显示` matched NOTHING while
# `see CV-001 here` matched — internal block ids stayed in Chinese reader-facing
# prose with no STRIPPED_ID, in a skill whose default output language is Chinese.
REF_RE = re.compile(r"(?<![0-9A-Za-z])(?:CV|JD)-\d{3}(?![0-9A-Za-z])")
_BRACKETED = re.compile(
    r"[\(（\[【]\s*(?:CV|JD)-\d{3}(?:\s*[,、;；]\s*(?:CV|JD)-\d{3})*\s*[\)）\]】]")


def cannot_run(workspace: pathlib.Path, reason: str, code: str = "NO_INPUT") -> int:
    """Exactly one receipt on the could-not-run path, then exit 2.

    `code` is NO_INPUT for a file that is absent and journal.UNREADABLE_INPUT for one
    that is present and unusable. Those are different instructions to the reader.
    """
    print(f"cannot run: {reason}", file=sys.stderr)
    if workspace.is_dir():
        journal.receipt(workspace, GATE, {}, "could_not_run", [f"{code}: {reason}"])
    return 2


def load_block_ids(path: pathlib.Path) -> set[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        raise journal.YamlUnreadable(path, f"cannot read evidence JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise journal.YamlUnreadable(path, "evidence JSON must be an object")
    journal.require_lists(data, path, blocks=dict)
    blocks = data.get("blocks") or []
    if any(not isinstance(b.get("id"), str) or not b["id"].strip() for b in blocks):
        raise journal.YamlUnreadable(path, "each evidence block requires a non-empty string id")
    return {block["id"] for block in blocks}


def drop_unresolvable_refs(assessment: dict, ids: set[str]) -> tuple[dict, list[str]]:
    findings: list[str] = []
    journal.require_lists(assessment, "fit-assessment.yaml", requirements=dict, stated_conditions=dict)
    for collection in ("requirements", "stated_conditions"):
        for index, entry in enumerate(assessment.get(collection) or []):
            journal.require_lists(entry, f"fit-assessment.yaml {collection}[{index}]", evidence=dict)
    for row in assessment.get("requirements") or []:
        kept = []
        for item in row.get("evidence") or []:
            ref = str(item.get("ref", "")).strip()
            if ref in ids:
                kept.append(item)
            else:
                findings.append(
                    f"DROPPED_REF: {ref or '<empty>'} in requirement "
                    f"{row.get('id', '?')} does not name an existing block")
        if "evidence" in row or kept:
            row["evidence"] = kept
    for condition in assessment.get("stated_conditions") or []:
        kept = []
        for item in condition.get("evidence") or []:
            ref = str(item.get("ref", "")).strip()
            if ref in ids:
                kept.append(item)
            else:
                findings.append(
                    f"DROPPED_REF: {ref or '<empty>'} in stated_conditions "
                    f"({condition.get('type', '?')}) does not name an existing block")
        condition["evidence"] = kept
    return assessment, findings


def strip_block_ids(markdown: str) -> tuple[str, list[str]]:
    findings: list[str] = []
    out_lines: list[str] = []
    for number, line in enumerate(markdown.splitlines(keepends=True), start=1):
        if line.lstrip().startswith("|"):
            out_lines.append(line)          # the auditable requirement table
            continue
        found = REF_RE.findall(line)
        if not found:
            out_lines.append(line)
            continue
        for ref in found:
            findings.append(
                f"STRIPPED_ID: {ref} appeared in reader-facing prose at line {number}; "
                f"name the thing itself instead")
        cleaned = _BRACKETED.sub("", line)
        cleaned = REF_RE.sub("", cleaned)
        cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
        cleaned = re.sub(r" +([,.;:!?，。；：！？）】])", r"\1", cleaned)
        cleaned = re.sub(r"([（【(\[]) +", r"\1", cleaned)
        cleaned = re.sub(r"[ \t]+(\n)", r"\1", cleaned)
        out_lines.append(cleaned)
    return "".join(out_lines), findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resolve or drop evidence references.")
    parser.add_argument("--workspace", required=True, type=pathlib.Path)
    parser.add_argument("--check-only", action="store_true",
                        help="make no writes; exit 1 if any drop or strip would happen")
    args = parser.parse_args(argv)

    workspace = args.workspace
    blocks_path = workspace / "evidence-blocks.json"
    yaml_path = workspace / "fit-assessment.yaml"
    md_path = workspace / "fit-assessment.md"
    if not workspace.is_dir():
        return cannot_run(workspace, f"workspace {workspace} does not exist")
    for path in (blocks_path, yaml_path):
        if not path.exists():
            return cannot_run(workspace, f"{path.name} not found at {path}")

    try:
        ids = load_block_ids(blocks_path)
    except journal.YamlUnreadable as exc:
        return cannot_run(workspace, str(exc), journal.UNREADABLE_INPUT)
    findings: list[str] = []
    if not ids:
        findings.append("NO_BLOCKS: evidence-blocks.json holds no blocks; "
                        "re-run evidence_blocks.py before assessing")

    try:
        assessment = journal.load_yaml(yaml_path)
        assessment, ref_findings = drop_unresolvable_refs(assessment, ids)
    except journal.YamlUnreadable as exc:
        return cannot_run(workspace, str(exc), journal.UNREADABLE_INPUT)
    findings += ref_findings

    try:
        markdown = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
    except (OSError, UnicodeError) as exc:
        return cannot_run(workspace, str(exc), journal.UNREADABLE_INPUT)
    cleaned_md, md_findings = strip_block_ids(markdown)
    findings += md_findings

    if not args.check_only:
        if ref_findings:
            yaml_path.write_text(
                yaml.safe_dump(assessment, allow_unicode=True, sort_keys=False),
                encoding="utf-8")
        if md_findings:
            md_path.write_text(cleaned_md, encoding="utf-8")

    hard_failure = any(f.startswith("NO_BLOCKS:") for f in findings)
    failed = hard_failure or (args.check_only and bool(findings))
    for finding in findings:
        print(finding)
    journal.receipt(
        workspace, GATE,
        {"evidence-blocks.json": journal.sha256_file(blocks_path),
         "fit-assessment.yaml": journal.sha256_file(yaml_path)},
        "fail" if failed else "recorded",
        findings)
    return 1 if failed else 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    raise SystemExit(main())
