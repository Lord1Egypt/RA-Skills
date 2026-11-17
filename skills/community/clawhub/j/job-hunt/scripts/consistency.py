#!/usr/bin/env python3
"""Contradictions inside a single assessment, found in code rather than asked for in
prose. Pure, deterministic, and deliberately not the model's job to police.

The mode file already states each of these rules, and the model already follows them
most of the time. That is exactly the problem this file exists for: a rule obeyed most
of the time still ships the defect, and this one ships it invisibly. Nothing about the
top verdict priced at three days looks broken on screen -- it looks like an assessment.
The reader has no way to know the two halves were produced by a model contradicting
itself, so they average them, and the average is not a judgement anyone made.

Every check reports rather than repairs. Code can see that two fields disagree; it
cannot see which one is right, and picking silently would replace a visible
contradiction with an invisible guess.

These are deliberately the checks that survive being wrong. Each fires on a countable
fact, never on meaning, so a false positive costs the reader one line of caution and
never suppresses a finding.

Exit 2 still writes a receipt, verdict "could_not_run", unless the workspace directory
itself is absent -- there is nothing to append to. A clean run's verdict is "recorded":
this script reports, it does not judge, and the composer that reads it --
check_assessment.py, not check_apply.py -- has PASSING_VERDICTS ("pass", "recorded").
"recorded" here means "ran, nothing to report", never "stored a baseline"; the setup
half of a two-step gate is "baseline_recorded". See journal.VERDICTS.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import journal  # noqa: E402
import vocab  # noqa: E402

GATE = "consistency"

# A threshold over vocab.EFFORT, not a second copy of it. The assertion is what
# makes that claim checkable rather than a comment nobody reads.
CONFLICT_EFFORTS = ("multi_day", "not_closable")
assert set(CONFLICT_EFFORTS) <= set(vocab.EFFORT)

# The condition types that are about the right to work, which is a subset of the
# seven a posting can state -- a `licence` or an `onsite_location` is a real wall
# and simply not one this comparison knows how to make. Same assertion for the
# same reason as above: rename a type in vocab and this tuple would keep matching
# nothing at all, which reads from the outside exactly like "no conflict found".
AUTH_CONDITION_TYPES = ("sponsorship", "work_authorization", "citizenship")
assert set(AUTH_CONDITION_TYPES) <= set(vocab.CONDITION_TYPES)

NOTICE_CODES = ("NOTICE_VERDICT_EFFORT", "NOTICE_LOOSE_KNOCKOUTS", "NOTICE_GAP_ACTIONS",
                "NOTICE_WORK_AUTH_CONFLICT", "NOTICE_WORK_AUTH_VERIFY")


def cannot_run(workspace: pathlib.Path, reason: str, code: str = "NO_INPUT") -> int:
    """Exactly one receipt on the could-not-run path, then exit 2.

    `code` is NO_INPUT for a file that is absent and journal.UNREADABLE_INPUT for one
    that is present and unusable. Those are different instructions to the reader.
    """
    print(f"cannot run: {reason}", file=sys.stderr)
    if workspace.is_dir():
        journal.receipt(workspace, GATE, {}, "could_not_run", [f"{code}: {reason}"])
    return 2


def verdict_effort_conflict(assessment: dict | None) -> bool:
    """A verdict saying the CV already covers what this posting screens on, beside an
    effort estimate saying the remaining gaps take days or cannot be closed at all.

    `evening` is NOT included, and that is a deliberate divergence from the extension
    this is ported from. There, effort priced the whole tailoring job. Here it prices
    closing the gaps, and a strong apply with an evening of work left is an ordinary,
    honest assessment. A check that fired on those would be ignored within a week.
    """
    # VERDICTS is ordered strongest-first and its order is pinned by test_vocab.py,
    # so index 0 is the top verdict. Written this way rather than as the literal
    # because Plan 1's test_no_other_script_redeclares_a_closed_set fails any
    # scripts/*.py that spells a verdict out — one source, one spelling.
    if not assessment or assessment.get("verdict") != vocab.VERDICTS[0]:
        return False
    return assessment.get("effort") in CONFLICT_EFFORTS


def loose_knockouts(rows: list[dict] | None) -> int:
    """How many requirements were marked hard filters, when that count is high enough
    to mean the rule was applied loosely.

    A knockout is a condition a recruiter can check without judgement and which ends
    the application on its own. Postings label half their list "required", and the whole
    point of the screening axis is to be the smaller, harder list underneath that label.
    When it stops being smaller it has collapsed back into the thing it was separating
    from, and the ordering built on it is no longer a screening order.

    Not reclassified: code can count them but cannot tell which one is genuine.
    """
    count = sum(1 for item in (rows or [])
                if isinstance(item, dict) and item.get("screening") == "knockout")
    return count if count > 2 else 0


def uncovered_gap_actions(rows: list[dict] | None,
                          actions: list[dict] | None) -> dict | None:
    """Gaps that claim a pre-application fix while the plan is too short to hold them.

    `actions` is the single authoritative to-do list; every instruction implied by a
    row's how_to_close is supposed to appear there exactly once. Matching them by
    meaning would need the model back and would produce false positives on wording
    alone, so only the degenerate case is checked: more closable gaps than there are
    actions in total. That is narrower than the rule it guards, and it is the part of
    the rule that can be checked without guessing.
    """
    closable = sum(1 for item in (rows or [])
                   if journal.as_mapping(item).get("match") in ("gap", "partial")
                   and journal.as_mapping(item).get("effort") in ("quick", "evening", "multi_day")
                   and str(journal.as_mapping(item).get("how_to_close") or "").strip())
    total = len(actions or [])
    return {"gaps": closable, "actions": total} if closable > total else None


def work_authorization_alignment(condition: dict | None,
                                 declared_status: str | None) -> str | None:
    """Arithmetic on two self-reported facts, in code because the answer must be the
    same every run. A model asked to make this comparison gets it right most of the
    time, and the case it gets wrong is the one where the job is impossible for the
    reader.

    The output is always "these two appear to conflict, check it yourself", never
    "you are not eligible".
    """
    # `condition or {}` is the exact idiom `journal.as_mapping`'s docstring says
    # it exists to replace: it guards None and every falsy value and NOT a
    # non-empty string, so `stated_conditions: [visa_sponsorship]` — a plausible
    # hand-edit — raised AttributeError here. Measured 2026-09-06: exit 1, no
    # finding, NO RECEIPT, which a composer reads as a gate that never ran while
    # the caller reads "found problems".
    condition = journal.as_mapping(condition)
    if condition.get("type") not in AUTH_CONDITION_TYPES:
        return None
    if declared_status in (None, "", "unknown"):
        return None                     # the default must never trigger a downgrade
    stance = condition.get("stance")
    if stance == "offers_support" and declared_status == "needs_sponsorship":
        return "supported"
    if stance == "requires_existing":
        if declared_status == "needs_sponsorship":
            return "conflict"
        if declared_status in ("student_or_graduate", "temporary_route"):
            # Calling this a conflict would wrongly kill viable applications, so it asks.
            return "verify"
    return None


def overall_authorization_alignment(conditions: list[dict] | None,
                                    declared_status: str | None) -> str | None:
    # The CONTAINER can be wrong too: `stated_conditions: none` is a plausible way
    # to write "there are none" and iterating a string yields its characters,
    # while a bool or an int is not iterable at all.
    if not isinstance(conditions, (list, tuple)):
        conditions = []
    results = [work_authorization_alignment(c, declared_status) for c in conditions]
    for level in ("conflict", "verify", "supported"):
        if level in results:
            return level
    return None


def _notice(code: str, text_zh: str, text_en: str, anchor_zh: str, anchor_en: str,
            **values) -> dict:
    from report_locales import NOTICE_TEXT
    result = {"code": code, "text_zh": text_zh, "text_en": text_en,
              "anchor_zh": anchor_zh, "anchor_en": anchor_en}
    for lang, (anchor, text) in NOTICE_TEXT[code].items():
        result[f"anchor_{lang}"] = anchor
        result[f"text_{lang}"] = text.format(**values)
    return result


def notices(assessment: dict | None) -> list[dict]:
    assessment = assessment or {}
    rows = assessment.get("requirements") or []
    produced: list[dict] = []

    alignment = overall_authorization_alignment(
        assessment.get("stated_conditions"), assessment.get("declared_work_status"))
    if alignment == "conflict":
        produced.append(_notice(
            "NOTICE_WORK_AUTH_CONFLICT",
            "岗位写明要求已持有工作许可，而你声明需要担保：这两条看起来冲突，请你自己向雇主核实。"
            "本 skill 不判定任何人的法律资格。",
            "The posting requires existing work authorization and you have declared that "
            "you need sponsorship. These two appear to conflict — check it with the "
            "employer yourself. This skill does not decide anyone's legal eligibility.",
            "这两条看起来冲突", "These two appear to conflict"))
    elif alignment == "verify":
        produced.append(_notice(
            "NOTICE_WORK_AUTH_VERIFY",
            "岗位写明要求已持有工作许可，而你走的是学生/毕业生或临时通道：这不一定是冲突，"
            "但要向雇主核实这条通道算不算数。",
            "The posting requires existing work authorization and your route is a "
            "student/graduate or temporary one. That is not necessarily a conflict — ask "
            "the employer whether that route counts.",
            "不一定是冲突", "not necessarily a conflict"))

    if verdict_effort_conflict(assessment) and alignment != "conflict":
        # Suppressed under a work-auth conflict: that notice is already telling the
        # reader the verdict above it does not hold.
        produced.append(_notice(
            "NOTICE_VERDICT_EFFORT",
            "结论与投入互相矛盾：一份已经覆盖了这个岗位筛选项的简历，不该还要数日的投入、"
            "或者根本补不上。请以下面的需求表为准，而不是上面那个词。",
            "The verdict and the effort estimate disagree: a CV that already covers what "
            "this posting screens on should not still need days of work, or work that "
            "cannot be done at all. Weigh the requirement rows below over the word above.",
            "结论与投入互相矛盾", "The verdict and the effort estimate disagree"))

    count = loose_knockouts(rows)
    if count:
        produced.append(_notice(
            "NOTICE_LOOSE_KNOCKOUTS",
            f"有 {count} 条需求被标成了硬性筛选项。多数岗位最多只有一条，"
            f"所以下面的排序请当作近似，而不是真正会把你筛掉的东西。",
            f"{count} requirements are marked hard filters. Most postings have at most "
            f"one, so read the order below as approximate rather than as what actually "
            f"screens you out.",
            "被标成了硬性筛选项", "are marked hard filters", count=count))

    uncovered = uncovered_gap_actions(rows, assessment.get("actions"))
    if uncovered:
        produced.append(_notice(
            "NOTICE_GAP_ACTIONS",
            f"有 {uncovered['gaps']} 个缺口写着可以在投递前补上，"
            f"但行动清单只有 {uncovered['actions']} 条——上面的建议有一部分没有进入这份清单。",
            f"{uncovered['gaps']} gaps say they can be closed before applying, but the "
            f"plan lists {uncovered['actions']} actions — some of the advice above did "
            f"not make it into this list.",
            "没有进入这份清单", "did not make it into this list", **uncovered))
    return produced


def main(argv: list[str] | None = None) -> int:
    from report_locales import LANGUAGES
    parser = argparse.ArgumentParser(description="Report contradictions in an assessment.")
    parser.add_argument("--workspace", required=True, type=pathlib.Path)
    parser.add_argument("--lang", choices=LANGUAGES, default="en")
    args = parser.parse_args(argv)

    path = args.workspace / "fit-assessment.yaml"
    if not args.workspace.is_dir():
        return cannot_run(args.workspace,
                          f"workspace {args.workspace} does not exist")
    if not path.exists():
        return cannot_run(args.workspace,
                          f"fit-assessment.yaml not found at {path}")

    try:
        assessment = journal.load_yaml(path)
    except journal.YamlUnreadable as exc:
        return cannot_run(args.workspace, str(exc), journal.UNREADABLE_INPUT)
    findings = [f"{n['code']}: {n[f'text_{args.lang}']}" for n in notices(assessment)]
    for finding in findings:
        print(finding)
    journal.receipt(args.workspace, GATE,
                    {"fit-assessment.yaml": journal.sha256_file(path)},
                    "recorded", findings)
    return 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    raise SystemExit(main())
