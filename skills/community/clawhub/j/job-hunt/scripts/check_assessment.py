#!/usr/bin/env python3
"""Whether an assessment may be shown to the person who asked for it.

Composes the five checks that stand on their own -- evidence refs, the prediction lint,
the contradiction detectors, the counting path, the market-table lint -- and adds the
rules that only make sense once all five outputs sit in the same document.

Composition means requiring the receipts, not recomputing the answers. A gate that was
never run produces no output, and no output looks exactly like a clean run, so this
gate reads journal.jsonl and refuses to pass when an upstream receipt is missing or
records a failure. It re-derives their logic on top of that as a belt-and-braces check
on the SHIPPED bytes, which is a different question from "did the gate run".

Each added rule closes a way an assessment can be internally consistent and still
wrong: counts without the disclaimer read as a prediction; a hard barrier printed after
the conclusion is a barrier nobody registered; a contradiction found in code and absent
from the page is one the reader averages away; a convention restated by the model is how
a "usually" becomes a "must" with nothing to check it against; a 大概率被筛掉 with no
「那该怎么办」 half is a door closed with nothing behind it.

Two comparisons are deliberately loose, because the tight version fires on correct
output and a gate that cries wolf is a gate people stop reading:

* Conventions are compared with ALL whitespace removed. The tables use YAML block
  scalars with hard wraps; demanding the model reproduce the wrap points would fail a
  card rendered character-for-character.
* Disqualifiers are keyed on the `## 硬性阻断项` section and the ROW IDS it lists, never
  on the posting's own wording. A Chinese section naming an English requirement is a
  paraphrase by construction, and that is the correct output, not the defect.

One finding is deliberately downgraded. check_conventions.py fails hard on an expired
review_by because it is the CI lint and that is where a stale date should stop a build.
Here it becomes WARN_EXPIRED_REVIEW_BY and the card must instead carry a 「已过复核期」 /
"past its review date" banner (spec §10). A date passing while the code did not change
must not stop the skill working -- but rendering a stale card without saying so is worse
than either.

A mode may not claim success without a receipt. Exit 2 writes one too, verdict
"could_not_run", unless the workspace directory itself is absent.
"""
from __future__ import annotations

import argparse
import copy
import datetime
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import check_conventions as conventions  # noqa: E402
import check_evidence_refs as refs  # noqa: E402
import consistency  # noqa: E402
import count_coverage as coverage  # noqa: E402
import enter_mode  # noqa: E402
import journal  # noqa: E402
import lint_no_prediction as prediction  # noqa: E402
import paths  # noqa: E402
import vocab  # noqa: E402
import report_locales as locales  # noqa: E402

GATE = "check_assessment"
MODE = "assess"

# Reader-facing anchors follow the report language; schema keys remain stable.
DISCLAIMER_ANCHORS = locales.anchors("disclaimer")
VERDICT_MARKERS = locales.anchors("verdict")
DISQUALIFIER_HEADINGS = locales.anchors("blockers")
# The last anchor here that knew only one language, and the one that could not be
# caught by running the gate today: it cannot fire before the first `review_by`
# passes (2026-11-09, twelve entries). Matched case-insensitively, because unlike
# the anchors above it is a BANNER — sentence-initial by nature, so
# "past its review date" has to match "Past its review date — …".
STALE_BANNER = locales.anchors("stale")

# The closed set modes/assess.md §10 defines. Exactly one of these, inside the section
# below, on exactly the two verdicts below; the two column headers are where the
# section's whole value sits. One supported translation of each is enough.
STRATEGIES = ("apply_anyway", "reposition", "skill_sprint", "side_door", "change_track")
STRATEGY_HEADINGS = locales.anchors("strategy")
OTHER_HALF_VERDICTS = ("likely_screen_out", "blocked")
ACCEPTANCE_COLUMNS = (locales.anchors("acceptance"), locales.anchors("deliverable"))

# Composition: each of these must have run on THIS workspace and not failed.
UPSTREAM_GATES = ("evidence_blocks", "count_coverage", "consistency",
                  "check_evidence_refs", "lint_no_prediction")
PASSING_VERDICTS = ("pass", "recorded")

# NOT `\b`, for the reason spelled out in check_evidence_refs.REF_RE: a
# disqualifier section written `- **R1** — 该岗位要求…` matched nothing, so a
# correctly named blocking row fired a false DISQUALIFIER_NOT_NAMED. Same root
# cause, opposite symptom: silent there, cry-wolf here.
_ROW_ID = re.compile(r"(?<![0-9A-Za-z])R\d+(?![0-9A-Za-z])")
# NAMING a row is not the same as mentioning one. `The role requires deep SAP R3
# experience` satisfied row R3 — so a disqualifier section could be told it had
# named the wall when it had only happened to contain a product name, and the
# reader is shown a wall they still walk into.
#
# modes/assess.md mandates the shape this matches: `- **R2** — …`. A bare
# in-prose mention no longer counts, which is stricter than before and is the
# safe direction for a check whose whole job is that the row was pointed at.
_NAMED_ROW = re.compile(
    r"(?:^|\n)\s*(?:[-*+]\s*)?\**(R\d+)\**(?![0-9A-Za-z])"
    r"|\*\*(R\d+)\*\*(?![0-9A-Za-z])")
_HEADING = re.compile(r"^\s{0,3}#{1,6}\s")


def _squeeze(text: str) -> str:
    """Whitespace is not the claim."""
    return re.sub(r"\s+", "", text)


def _verdict_line_index(lines: list[str]) -> int | None:
    for index, line in enumerate(lines):
        if any(marker.casefold() in line.casefold() for marker in VERDICT_MARKERS):
            return index
    return None


def _section_lines(lines: list[str], heading: str) -> tuple[int, list[str]] | None:
    """The lines of the first `heading` section, up to the next heading of any level."""
    for index, line in enumerate(lines):
        if line.strip().casefold().startswith(heading.casefold()):
            body = []
            for later in lines[index + 1:]:
                if _HEADING.match(later):
                    break
                body.append(later)
            return index, body
    return None


def _first_section(lines: list[str], headings) -> tuple[int, list[str]] | None:
    """The first section matching any spelling of the heading. All translations are
    correct output, so trying only one turns a translation into a finding."""
    for heading in headings:
        found = _section_lines(lines, heading)
        if found is not None:
            return found
    return None


def cannot_run(workspace: pathlib.Path, reason: str, code: str = "NO_INPUT") -> int:
    """Exactly one receipt on the could-not-run path, then exit 2.

    `code` is NO_INPUT for a file that is absent and journal.UNREADABLE_INPUT for one
    that is present and unusable. Those are different instructions to the reader.
    """
    print(f"cannot run: {reason}", file=sys.stderr)
    if workspace.is_dir():
        journal.receipt(workspace, GATE, {}, "could_not_run", [f"{code}: {reason}"])
    return 2


def check(workspace: pathlib.Path, market_dir: pathlib.Path,
          today: datetime.date, skill_root: pathlib.Path | None = None) -> list[str]:
    findings: list[str] = []
    root = pathlib.Path(skill_root) if skill_root else paths.SKILL_ROOT
    # Raises journal.YamlUnreadable, which main() routes to cannot_run. Deliberately
    # not caught here: check() returns findings, and a findings list is exactly what
    # "the gate could not read its input" must NOT be reported as.
    assessment = journal.load_yaml(workspace / "fit-assessment.yaml")
    journal.require_lists(assessment, workspace / "fit-assessment.yaml",
                          requirements=dict, stated_conditions=dict, actions=dict,
                          conventions_rendered=str)
    markdown = (workspace / "fit-assessment.md").read_text(encoding="utf-8")
    lines = markdown.splitlines()
    squeezed = _squeeze(markdown)
    block_ids = refs.load_block_ids(workspace / "evidence-blocks.json")

    # Computed HERE, before anything appends, and not down in rule 5 where it used to
    # live. §8's refusal has no verdict from the five, no coverage block and nothing to
    # count, so every rule that presumes an assessment has to be able to scope itself
    # off this flag -- and a flag computed halfway down invites the next rule to be
    # written above it and hard-fail the one output that is always correct.
    verdict = assessment.get("verdict")
    refusing = verdict == vocab.REFUSAL

    # 0. The layer-1.5 backstop, mirrored from check_apply.py. modes/assess.md is
    #    loaded unconditionally on entering the mode; this is what makes that real.
    entry = enter_mode.latest_mode_entry(workspace, MODE)
    mode_path = paths.mode_file(MODE, root)
    if entry is None:
        findings.append("NO_MODE_ENTRY: journal.jsonl has no mode_entry for assess — "
                        "modes/assess.md is loaded unconditionally on entering the "
                        "mode; run scripts/enter_mode.py --mode assess and read it")
    elif not mode_path.exists():
        # `mode_path.exists()` guarded the comparison, so a wrong --skill-root
        # switched the layer-1.5 backstop off and reported nothing at all.
        findings.append(f"MODE_FILE_MISSING: {mode_path} is not on disk, so the hash "
                        "recorded at mode entry could not be checked against it; "
                        "point --skill-root at the skill")
    elif entry.get("mode_file_sha256") != journal.sha256_file(mode_path):
        findings.append("MODE_FILE_CHANGED: modes/assess.md changed after this run "
                        "entered the mode, so what was read is not what is on disk — "
                        "re-enter the mode and re-read it")

    # Every receipt was written by journal.receipt(), not by hand. Reported
    # rather than filtered: dropping a forged PASS would promote an older
    # genuine FAIL into last position and read as the current state.
    for gate_name, line_no in journal.unverified_receipts(workspace):
        findings.append(
            f"RECEIPT_UNVERIFIED: the {gate_name!r} receipt at gate-record "
            f"{line_no} does not match its own receipt_hash — it was hand-written "
            f"or edited after the gate ran, so it is not evidence that the gate ran")

    # 0b. Every upstream gate ran, on this workspace, and did not fail.
    for gate in UPSTREAM_GATES:
        receipts = journal.read_receipts(workspace, gate)
        if not receipts:
            findings.append(f"MISSING_RECEIPT: no journal.jsonl receipt for {gate} — "
                            f"the gate was never run, and a skipped gate looks exactly "
                            f"like a clean one")
            continue
        last = receipts[-1]
        if not journal.receipt_intact(last):
            continue  # The malformed/latest receipt is already a finding.
        if last.get("verdict") not in PASSING_VERDICTS:
            detail = "; ".join(last.get("findings") or []) or "no findings recorded"
            findings.append(f"UPSTREAM_FAILED: {gate} verdict={last.get('verdict')} "
                            f"({detail})")

    # 1. Evidence references, in check-only form: nothing may still need dropping.
    _, dropped = refs.drop_unresolvable_refs(copy.deepcopy(assessment), block_ids)
    findings += dropped
    _, stripped = refs.strip_block_ids(markdown)
    findings += stripped

    # 2. Row-level sourcing. `no_evidence` with an empty list is the honest shape.
    for row in assessment.get("requirements") or []:
        row = journal.as_mapping(row)
        resolvable = [e for e in (row.get("evidence") or [])
                      if str((e or {}).get("ref", "")).strip() in block_ids]
        if row.get("match") == "no_evidence":
            if row.get("evidence"):
                findings.append(f"ROW_UNSOURCED: row {row.get('id')} is no_evidence but "
                                f"carries references; one of the two is wrong")
        elif not resolvable:
            findings.append(f"ROW_UNSOURCED: row {row.get('id')} claims "
                            f"match={row.get('match')!r} with no reference that resolves "
                            f"to a block")

    # 3. The prediction lint, over every rendered surface in the workspace.
    #
    # The capture corpus is passed. Re-scanning WITHOUT it made this gate
    # contradict lint_no_prediction on the same bytes: a row rendering an
    # employer's own `AI/ML Engineer (100 % remote)` title -- which discover
    # requires verbatim -- passed one gate and failed the next, so the artifact
    # that broke was the honest one. Two gates running the same lint must run the
    # same lint.
    corpus = prediction.capture_corpus(workspace)
    for path in prediction.target_files(workspace):
        findings += prediction.scan_text(path.read_text(encoding="utf-8"),
                                         path.relative_to(workspace).as_posix(), corpus)

    # 4. Consistency notices must be attached where they fired.
    for notice in consistency.notices(assessment):
        if not any(notice[f"anchor_{lang}"].casefold() in markdown.casefold()
                   for lang in locales.LANGUAGES):
            findings.append(f"NOTICE_NOT_ATTACHED: {notice['code']} fired and its text "
                            f"is nowhere in fit-assessment.md; attach it beside the "
                            f"thing it qualifies")

    # 4b. The two fields those notices read. Neither is inferred and neither may be:
    #     one is the candidate's own statement, the other is the posting's own words.
    #     consistency.work_authorization_alignment returns None for anything outside
    #     these sets, and None is indistinguishable from "the two agree" -- so a hyphen
    #     in `needs-sponsorship` switches the notice off and leaves a clean-looking card.
    status = assessment.get("declared_work_status")
    if status is not None and status not in vocab.WORK_STATUS:
        findings.append(f"BAD_WORK_STATUS: declared_work_status is {status!r}, not one "
                        f"of {vocab.WORK_STATUS}; a value outside that set reads to the "
                        f"work-authorization notices exactly like agreement")
    for index, condition in enumerate(assessment.get("stated_conditions") or []):
        condition = condition or {}
        for field, allowed in (("type", vocab.CONDITION_TYPES),
                               ("stance", vocab.STANCE)):
            value = condition.get(field)
            if value not in allowed:
                findings.append(
                    f"BAD_STATED_CONDITION: stated_conditions[{index}].{field} is "
                    f"{value!r}, not one of {allowed}; the comparison that reads it "
                    f"returns nothing rather than reporting a mismatch, so the row is "
                    f"inert and looks like a row that found nothing")
    # A WARNING, not a failure, and the asymmetry is the point. An ABSENT status
    # suppresses both notices, which is the safe direction and is exactly what
    # consistency.py intends by "the default must never trigger a downgrade"; §4's
    # `screening: knockout` row is the primary path here, with NO_DISQUALIFIER_SECTION
    # hard behind it. An absent `effort` below is the opposite case -- it makes the card
    # PRINT something -- which is why that one is hard and this one is a line of text.
    if not refusing and status is None:
        findings.append("WARN_NO_WORK_STATUS: modes/assess.md §4 has you ask about work "
                        "authorization; declared_work_status records the answer, and "
                        "`unknown` is a legal answer. Without it the two work-auth "
                        "notices cannot fire at all")

    # 5. The counting path is the only counting path.
    counts = coverage.coverage(assessment.get("requirements"))
    findings += counts["invalid"]
    if not refusing:
        # The two lines of the card that are read off the TOP LEVEL rather than counted
        # off the rows. count_coverage.py used to invent both when they were absent --
        # `unclear` and `not_closable`, then again inside the zh label lookups -- and
        # nothing could see it, because COUNT_MISMATCH compares render_block's output
        # against render_block's output and two identical invented strings are equal.
        # The card now prints "not assessed"; this is what says whose fault that is.
        for field, allowed, code in (
                ("level_direction", vocab.LEVEL_DIRECTION, "MISSING_LEVEL_DIRECTION"),
                ("effort", vocab.EFFORT, "MISSING_EFFORT")):
            value = assessment.get(field)
            if value not in allowed:
                findings.append(
                    f"{code}: {field} is {value!r}, not one of {allowed}; the coverage "
                    f"card prints this line, so leaving it unset ships "
                    f"「{coverage.NOT_ASSESSED_ZH}」/'{coverage.NOT_ASSESSED_EN}' where "
                    f"the reader expects a judgement — assess it or say why you cannot")
        rendered = [coverage.render_block(assessment, counts, lang) for lang in locales.LANGUAGES]
        if not any(block in markdown for block in rendered):
            findings.append("COUNT_MISMATCH: fit-assessment.md does not contain the "
                            "block count_coverage.py produces; a second number written "
                            "by hand cannot be reconciled with this one")
        if not any(anchor.casefold() in markdown.casefold() for anchor in DISCLAIMER_ANCHORS):
            findings.append("NO_DISCLAIMER: the required disclaimer is absent; a count "
                            "without it reads as a prediction")

    # 6. The refusal floor is a refusal, not a sixth level.
    if refusing:
        for marker in VERDICT_MARKERS:
            if marker.casefold() in markdown.casefold():
                findings.append(f"REFUSAL_WITH_VERDICT: verdict is "
                                f"{vocab.REFUSAL} but {marker!r} still renders a "
                                f"conclusion")
    elif verdict not in vocab.VERDICTS:
        findings.append(f"BAD_VERDICT: {verdict!r} is not one of "
                        f"{vocab.VERDICTS} or {vocab.REFUSAL!r}")
    if assessment.get("provisional"):
        findings.append("PROVISIONAL_VERDICT: a discover-stage 基于卡片信息的初判 was "
                        "carried into an assessment; assess always recomputes")

    # 7. Disqualifiers render before the verdict, in a section that names their ids.
    blocking = [journal.as_mapping(row) for row in (assessment.get("requirements") or [])
                if journal.as_mapping(row).get("screening") == "knockout"
                and journal.as_mapping(row).get("match") in ("gap", "no_evidence")]
    if blocking:
        section = _first_section(lines, DISQUALIFIER_HEADINGS)
        if section is None:
            findings.append(
                f"NO_DISQUALIFIER_SECTION: {len(blocking)} knockout requirement(s) are "
                f"not met and there is no {' / '.join(DISQUALIFIER_HEADINGS)!r} "
                f"section; a wall the reader is never "
                f"shown is a wall they walk into")
        else:
            heading_index, body = section
            named = {rid for pair in _NAMED_ROW.findall("\n".join(body))
                     for rid in pair if rid}
            for row in blocking:
                if str(row.get("id")) not in named:
                    findings.append(
                        f"DISQUALIFIER_NOT_NAMED: row {row.get('id')} is a knockout the "
                        f"candidate does not meet and the disqualifier section does not "
                        f"list its id; paraphrase the barrier freely, but name the row")
            verdict_index = _verdict_line_index(lines)
            if verdict_index is not None and heading_index > verdict_index:
                findings.append(
                    "DISQUALIFIER_AFTER_VERDICT: the disqualifier section renders below "
                    "the verdict line; a wall printed after the conclusion is a wall "
                    "nobody read")

    # 8. The "what to do instead" half, on the two verdicts that require it. Scoped to
    #    the section, because that is what the finding names claim and because a
    #    contrast sentence elsewhere ("not apply_anyway but skill_sprint") is ordinary
    #    prose, not a menu — counting it as one is the cry-wolf case again.
    if verdict in OTHER_HALF_VERDICTS:
        strategy_section = _first_section(lines, STRATEGY_HEADINGS)
        body = "\n".join(strategy_section[1]) if strategy_section else ""
        chosen = [name for name in STRATEGIES if name in body]
        if not chosen:
            findings.append(
                f"NO_STRATEGY_SECTION: verdict is {verdict} and no strategy from "
                f"{STRATEGIES} appears under {' / '.join(STRATEGY_HEADINGS)!r}; "
                f"a verdict without the other half is a door "
                f"closed with nothing behind it")
        elif len(chosen) > 1:
            findings.append(
                f"STRATEGY_NOT_UNIQUE: {chosen} all appear in that section; pick "
                f"exactly one. A menu hands the choice back to the reader, which is "
                f"the work they asked for")
        for pair in ACCEPTANCE_COLUMNS:
            if not any(column in markdown for column in pair):
                findings.append(
                    f"NO_ACCEPTANCE_COLUMN: verdict is {verdict} and no {' / '.join(pair)!r} "
                    f"column is present; that column is what turns advice "
                    f"into something checkable, and it is the whole value of this "
                    f"section")

    # 9. Market conventions: allowlisted by id, rendered verbatim, staleness banner-ed.
    market = assessment.get("market")
    table = market_dir / f"{market}.yaml"
    known: dict[str, dict] = {}
    expired: set[str] = set()
    if market in conventions.MARKET_KEYS:
        if not table.exists():
            findings.append(f"CONVENTION_TABLE_MISSING: {table} does not exist")
        else:
            for finding in conventions.check_file(table, today):
                if finding.startswith("EXPIRED_REVIEW_BY:"):
                    # CI keeps this hard. At runtime it is a banner, not a refusal.
                    expired.add(finding.split(":", 1)[1].strip().split()[0])
                    findings.append("WARN_" + finding)
                else:
                    findings.append(finding)
            known = conventions.conventions_by_id(conventions.load_market_file(table))
    for entry_id in assessment.get("conventions_rendered") or []:
        convention = known.get(entry_id)
        if convention is None:
            findings.append(f"CONVENTION_UNKNOWN_ID: {entry_id} is not an entry in "
                            f"{table.name}; the model may not author a convention")
            continue
        if not any(_squeeze(str(convention.get(field, ""))) and
                   _squeeze(str(convention[field])) in squeezed
                   for field in ("text_en", "text_zh")):
            findings.append(f"CONVENTION_PARAPHRASED: {entry_id} was listed as rendered "
                            f"but neither text_en nor text_zh appears verbatim in "
                            f"fit-assessment.md")
        if entry_id in expired and not any(
                banner.casefold() in markdown.casefold() for banner in STALE_BANNER):
            findings.append(f"MISSING_STALE_BANNER: {entry_id} is past its review_by and "
                            f"was rendered without the 「{' / '.join(STALE_BANNER)}」 "
                            f"banner; the card still renders, but the reader has to be "
                            f"told it is stale")
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="The assess-mode gate.")
    parser.add_argument("--workspace", required=True, type=pathlib.Path)
    parser.add_argument("--market-dir", type=pathlib.Path, default=None)
    parser.add_argument("--skill-root", type=pathlib.Path, default=None)
    parser.add_argument("--today", default=None)
    args = parser.parse_args(argv)

    workspace = args.workspace
    market_dir = args.market_dir or conventions.CONVENTIONS_DIR
    skill_root = args.skill_root or paths.SKILL_ROOT
    today = (datetime.date.fromisoformat(args.today) if args.today
             else datetime.date.today())

    if not workspace.is_dir():
        return cannot_run(workspace, f"workspace {workspace} does not exist")
    required = [workspace / "fit-assessment.yaml", workspace / "fit-assessment.md",
                workspace / "evidence-blocks.json"]
    for path in required:
        if not path.exists():
            return cannot_run(workspace, f"{path.name} not found at {path}")

    try:
        findings = check(workspace, market_dir, today, skill_root)
    except (journal.YamlUnreadable, OSError, UnicodeError) as exc:
        return cannot_run(workspace, str(exc), journal.UNREADABLE_INPUT)
    hard = [f for f in findings if not f.startswith("WARN_")]
    for finding in findings:
        print(finding)
    journal.receipt(workspace, GATE,
                    {path.name: journal.sha256_file(path) for path in required},
                    "fail" if hard else "pass", findings)
    return 1 if hard else 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    raise SystemExit(main())
