#!/usr/bin/env python3
"""The one place a number in an assessment comes from.

The skill this replaces computed must-have coverage twice, with two formulas, over the
same list. The two never agreed, and prose was left managing the disagreement. There is
one function here, one rendered block, and check_assessment.py requires the block in
fit-assessment.md to be byte-identical to what this produces. A second number cannot
survive that.

No percentage, and no slash score. Collapsing strong / partial / gap into one number
needs a weight for a partial match, and any weight would be invented. The block shows
exactly what was counted and claims nothing that was not; every counted row is printed
in the requirement table beside its evidence reference, so the denominator is auditable
row by row and a reader can object to any single line.

Exit 2 still writes a receipt, verdict "could_not_run", unless the workspace directory
itself is absent -- there is nothing to append to.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import journal  # noqa: E402
import vocab  # noqa: E402
import report_locales as locales  # noqa: E402

GATE = "count_coverage"

MATCHES = vocab.MATCH
RECENCIES = vocab.RECENCY
KINDS = ("must_have", "responsibility")

# These two maps are this module's own. VERDICT_ZH is not: lint_no_prediction.py
# masks against the same map, and two copies of it means one of them eventually
# stops matching the label the other one prints.
LEVEL_DIRECTION_ZH = {"step_up": "上跳", "lateral": "平级", "step_down": "下沉",
                      "unclear": "不明"}
EFFORT_ZH = {"quick": "当天", "evening": "一晚", "multi_day": "数日",
             "not_closable": "补不上"}
VERDICT_ZH = vocab.VERDICT_ZH
# Labels for every member and nothing else, so the not-assessed token below is
# reachable only by a field being absent or out of enum. A member with no label
# would render as "not assessed" and read as a judgement nobody made.
assert set(LEVEL_DIRECTION_ZH) == set(vocab.LEVEL_DIRECTION)
assert set(EFFORT_ZH) == set(vocab.EFFORT)

# What the card says when the assessment judged neither of the two fields it
# prints. This used to be `.get("level_direction", "unclear")` and
# `.get("effort", "not_closable")` -- and then AGAIN as the default of each zh
# dict lookup, so the default `--lang zh` card kept inventing a value even with
# the obvious two fallbacks removed. Four fallbacks, one shipped card reading
# 「投递建议：强烈建议投 / 可补缺口所需投入：补不上」 off an assessment whose only
# gapped row said `effort: evening` and carried a how_to_close.
#
# It is not a member of either set and never can be: a reader has to be able to
# tell "nobody judged this" from "judged, and the answer is unclear", and a
# pessimistic guess printed in the same column as a real value is the one thing
# that makes those two indistinguishable. check_assessment.py reports the same
# state as MISSING_LEVEL_DIRECTION / MISSING_EFFORT, so the card admits the hole
# and the gate names it.
NOT_ASSESSED_EN = "not assessed"
NOT_ASSESSED_ZH = "未评估"


def cannot_run(workspace: pathlib.Path, reason: str, code: str = "NO_INPUT") -> int:
    """Exactly one receipt on the could-not-run path, then exit 2.

    `code` is NO_INPUT for a file that is absent and journal.UNREADABLE_INPUT for one
    that is present and unusable. Those are different instructions to the reader.
    """
    print(f"cannot run: {reason}", file=sys.stderr)
    if workspace.is_dir():
        journal.receipt(workspace, GATE, {}, "could_not_run", [f"{code}: {reason}"])
    return 2


def coverage(rows: list[dict] | None) -> dict:
    counts = {"must_total": 0, "must_strong": 0, "must_partial": 0, "must_gap": 0,
              "must_no_evidence": 0, "resp_total": 0, "resp_demonstrated": 0,
              "invalid": []}
    for index, item in enumerate(rows or []):
        item = item or {}
        if not isinstance(item, dict):
            # `item or {}` guards None and falsy, not a non-empty STRING. A row
            # written `- R1` instead of `- {id: R1, ...}` — one missing `id:` in
            # hand-written YAML — raised AttributeError here, so the gate exited
            # 1 with no finding and NO RECEIPT: indistinguishable from a gate
            # nobody ran.
            counts["invalid"].append(
                f"INVALID_ROW: requirement #{index + 1} is a {type(item).__name__}, "
                f"not a mapping ({item!r:.60}); a row needs at least id and match")
            continue
        identifier = item.get("id", f"#{index + 1}")
        match = item.get("match")
        recency = item.get("recency")
        if match not in MATCHES:
            counts["invalid"].append(
                f"INVALID_MATCH: row {identifier} has match {match!r}, "
                f"not one of {MATCHES}")
            match = None
        if recency not in RECENCIES:
            counts["invalid"].append(
                f"INVALID_RECENCY: row {identifier} has recency {recency!r}, "
                f"not one of {RECENCIES}")
            recency = None
        # Evidence that is only dated satisfies the keyword and reads as rusty to a
        # human, so it lands on partial. `undated` does NOT downgrade: a CV that omits
        # dates is a formatting fact, not a staleness fact.
        effective = "partial" if (match == "strong" and recency == "dated") else match
        kind = item.get("kind")
        if kind == "responsibility":
            counts["resp_total"] += 1
            if effective == "strong":
                counts["resp_demonstrated"] += 1
        elif kind == "must_have":
            # Preferred criteria stay in the evidence table but are not
            # mandatory qualifications, even when the schema uses must_have
            # as the requirement-row kind.
            if item.get("level") == "preferred" or item.get("screening") == "nice_to_have":
                continue
            counts["must_total"] += 1
            if effective == "strong":
                counts["must_strong"] += 1
            elif effective == "partial":
                counts["must_partial"] += 1
            elif effective == "gap":
                counts["must_gap"] += 1
            elif effective == "no_evidence":
                counts["must_no_evidence"] += 1
        else:
            # Counted into neither total, so the printed numbers still add up and
            # the row simply vanishes. That is why this one has to be reported.
            counts["invalid"].append(
                f"INVALID_KIND: row {identifier} has kind {kind!r}, "
                f"not one of {KINDS}")
    return counts


def _assessed(value, allowed: tuple, zh_labels: dict, lang: str) -> str:
    """The value as the reader should see it, or the not-assessed token.

    One function for both languages on purpose. Printing the raw token in en
    while zh printed a default was how the same file produced two cards making
    different claims, and the default `--lang zh` one was the one nobody read
    in English.
    """
    if value not in allowed:
        return NOT_ASSESSED_ZH if lang == "zh" else NOT_ASSESSED_EN
    return zh_labels[value] if lang == "zh" else value


def _verdict_zh(verdict) -> str:
    """The Chinese verdict word, for a verdict of ANY shape.

    `VERDICT_ZH.get(verdict, ...)` raised `TypeError: unhashable type: 'list'` on
    `verdict: [worth_applying]` — one stray bracket in hand-written YAML — and the
    gate exited 1 with no receipt, which a composer reads as a gate that never
    ran while the caller reads "found problems". An unusable verdict is exactly
    what the refusal string is for, so it is returned rather than raised.
    """
    try:
        return VERDICT_ZH.get(verdict, "证据不足—不出结论")
    except TypeError:
        return "证据不足—不出结论"


def render_block(assessment: dict, counts: dict, lang: str = "zh") -> str:
    verdict = assessment.get("verdict", "insufficient_evidence")
    if lang not in locales.LANGUAGES:
        raise ValueError(f"Unsupported report language: {lang!r}")
    if lang in locales.CARD_TEXT:
        labels = locales.CARD_TEXT[lang]
        direction_value = assessment.get("level_direction")
        effort_value = assessment.get("effort")
        direction = (labels["directions"][direction_value]
                     if direction_value in vocab.LEVEL_DIRECTION else labels["not_assessed"])
        effort = (labels["efforts"][effort_value]
                  if effort_value in vocab.EFFORT else labels["not_assessed"])
        verdict_label = labels["verdicts"][verdict if verdict in vocab.VERDICTS else vocab.REFUSAL]
        must_count = labels["count"].format(count=counts["must_strong"], total=counts["must_total"])
        resp_count = labels["count"].format(count=counts["resp_demonstrated"], total=counts["resp_total"])
        return (
            f"{labels['must']}: {must_count} "
            f"({labels['partial']} {counts['must_partial']}, {labels['gap']} {counts['must_gap']}, "
            f"{labels['no_evidence']} {counts['must_no_evidence']})\n"
            f"{labels['responsibilities']}: {resp_count}\n"
            f"{labels['level']}: {direction}\n"
            f"{labels['effort']}: {effort}\n"
            f"{locales.GATE_TEXT[lang]['verdict']} {verdict_label}")
    direction = _assessed(assessment.get("level_direction"), vocab.LEVEL_DIRECTION,
                          LEVEL_DIRECTION_ZH, lang)
    effort = _assessed(assessment.get("effort"), vocab.EFFORT, EFFORT_ZH, lang)
    if lang == "zh":
        return (
            f"必备条件有充分证据：   {counts['must_strong']} 项，共 {counts['must_total']} 项   "
            f"（部分符合 {counts['must_partial']}，存在缺口 {counts['must_gap']}，"
            f"无证据 {counts['must_no_evidence']}）\n"
            f"核心职责已证实：     {counts['resp_demonstrated']} 项，共 {counts['resp_total']} 项\n"
            f"职级匹配：           {direction}\n"
            f"可补缺口所需投入：   {effort}\n"
            f"投递建议：           {_verdict_zh(verdict)}")
    return (
        f"must-haves strongly evidenced:   {counts['must_strong']} of "
        f"{counts['must_total']}   (partial {counts['must_partial']}, "
        f"gap {counts['must_gap']}, no evidence {counts['must_no_evidence']})\n"
        f"core responsibilities demonstrated: {counts['resp_demonstrated']} of "
        f"{counts['resp_total']}\n"
        f"level match:                     {direction}\n"
        f"effort to close the gaps:        {effort}\n"
        f"apply verdict:                   {verdict}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Count must-have and responsibility "
                                                 "coverage. The only counting path.")
    parser.add_argument("--workspace", required=True, type=pathlib.Path)
    # The matching disclaimer and report headings are in report_locales.py.
    parser.add_argument("--lang", choices=locales.LANGUAGES, default="zh")
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
    counts = coverage(assessment.get("requirements"))
    findings = list(counts["invalid"])
    block = render_block(assessment, counts, args.lang)

    payload = dict(counts)
    for lang in locales.LANGUAGES:
        payload[f"block_{lang}"] = render_block(assessment, counts, lang)
    (args.workspace / "coverage.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for finding in findings:
        print(finding)
    print(block)
    journal.receipt(args.workspace, GATE,
                    {"fit-assessment.yaml": journal.sha256_file(path)},
                    "fail" if findings else "recorded", findings)
    return 1 if findings else 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    raise SystemExit(main())
