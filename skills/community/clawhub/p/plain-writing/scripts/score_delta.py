#!/usr/bin/env python3
"""Compare mechanical prose-lint results before and after an edit."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Sequence

import lint_prose


def has_term(text: str, term: str) -> bool:
    return bool(
        re.search(
            r"(?<![A-Za-z])" + re.escape(term) + r"(?![A-Za-z])",
            text,
            re.IGNORECASE,
        )
    )


def scope_strengthening_signals(
    before_text: str, after_text: str
) -> list[dict[str, object]]:
    """Return conservative source-aware review signals, never pass/fail claims."""
    comparisons = (
        (("some",), ("all", "every", "each")),
        (("one",), ("all", "every", "each")),
        (("either",), ("both",)),
        (("sometimes", "often"), ("always", "never")),
        (
            ("may", "might", "could", "appears", "appeared", "seems", "suggests"),
            ("will", "confirmed", "proves", "proven"),
        ),
        (
            ("associated", "correlated", "followed", "after"),
            ("caused", "causes", "causing"),
        ),
    )
    before_sentences = re.split(r"(?<=[.!?])\s+|\n+", before_text)
    after_sentences = re.split(r"(?<=[.!?])\s+|\n+", after_text)
    signals: list[dict[str, object]] = []
    seen: set[tuple[tuple[str, ...], tuple[str, ...]]] = set()
    for source in before_sentences:
        source_words = {word.casefold() for word in lint_prose.WORD_RE.findall(source)}
        if len(source_words) < 3:
            continue
        for weaker, stronger in comparisons:
            source_terms = tuple(term for term in weaker if has_term(source, term))
            if not source_terms:
                continue
            for candidate in after_sentences:
                candidate_words = {
                    word.casefold() for word in lint_prose.WORD_RE.findall(candidate)
                }
                if len(candidate_words) < 3:
                    continue
                overlap = len(source_words & candidate_words) / min(
                    len(source_words), len(candidate_words)
                )
                if overlap < 0.5:
                    continue
                added_terms = tuple(
                    term
                    for term in stronger
                    if not has_term(source, term) and has_term(candidate, term)
                )
                key = (source_terms, added_terms)
                if not added_terms or key in seen:
                    continue
                seen.add(key)
                signals.append(
                    {
                        "source_terms": list(source_terms),
                        "candidate_terms": list(added_terms),
                        "message": (
                            f"review {', '.join(source_terms)} → "
                            f"{', '.join(added_terms)} for stronger scope or certainty"
                        ),
                    }
                )
    return signals


def structure(text: str) -> dict[str, int]:
    lines: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker[0]
            elif marker[0] == fence:
                fence = None
            continue
        if fence is None:
            lines.append(line)
    visible_text = "\n".join(lines)
    headings = sum(bool(re.match(r"^\s*#{1,6}\s+", line)) for line in lines)
    standalone_bold_labels = sum(
        bool(re.match(r"^\s*\*\*[^*\n]{1,100}\*\*\s*$", line))
        for line in lines
    )
    plain_labels = sum(
        bool(re.match(r"^\s*[A-Z][^.!?\n]{0,80}:\s*$", line))
        and len(lint_prose.WORD_RE.findall(line)) <= 4
        for line in lines
    )
    list_items = sum(
        bool(re.match(r"^\s*(?:[-+*]|\d+[.)])\s+", line))
        for line in lines
    )
    bold_spans = len(re.findall(r"(?<!\*)\*\*[^*\n]+\*\*(?!\*)", visible_text))
    emoji_headings = sum(
        bool(
            re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", line)
        )
        for line in lines
        if re.match(r"^\s*#{1,6}\s+", line)
    )
    return {
        "headings": headings,
        "section_labels": headings + standalone_bold_labels + plain_labels,
        "standalone_bold_labels": standalone_bold_labels,
        "plain_labels": plain_labels,
        "list_items": list_items,
        "bold_spans": bold_spans,
        "emoji_headings": emoji_headings,
    }


def summarize(text: str, path: Path, mode: str) -> dict[str, object]:
    result = lint_prose.lint_text(text, path=str(path), mode=mode)
    rules = Counter(item.code for item in result.findings)
    findings = len(result.findings)
    rate = findings * 100 / result.words if result.words else 0.0
    return {
        "path": str(path),
        "words": result.words,
        "errors": result.errors,
        "warnings": result.warnings,
        "findings": findings,
        "findings_per_100_words": rate,
        "rules": dict(sorted(rules.items())),
        "structure": structure(text),
    }


def compare(
    before_path: Path,
    after_path: Path,
    mode: str,
    protected_tokens: Sequence[str] = (),
    protected_count: bool = False,
) -> dict[str, object]:
    before_text = before_path.read_text(encoding="utf-8")
    after_text = after_path.read_text(encoding="utf-8")
    before = summarize(before_text, before_path, mode)
    after = summarize(after_text, after_path, mode)
    before_rate = float(before["findings_per_100_words"])
    after_rate = float(after["findings_per_100_words"])
    token_counts = [
        {
            "token": token,
            "source_count": before_text.count(token),
            "candidate_count": after_text.count(token),
        }
        for token in protected_tokens
    ]
    lost = []
    for item in token_counts:
        source_count = int(item["source_count"])
        candidate_count = int(item["candidate_count"])
        if source_count and (
            candidate_count == 0 or (protected_count and candidate_count < source_count)
        ):
            lost.append(item["token"])
    source_occurrences = sum(int(item["source_count"]) for item in token_counts)
    retained_occurrences = sum(
        min(int(item["source_count"]), int(item["candidate_count"]))
        for item in token_counts
    )
    rule_codes = sorted(set(before["rules"]) | set(after["rules"]))
    rule_delta = {
        code: int(after["rules"].get(code, 0))
        - int(before["rules"].get(code, 0))
        for code in rule_codes
    }
    mechanical_regression = (
        int(after["errors"]) > int(before["errors"])
        or after_rate > before_rate + 1e-12
    )
    structure_delta = {
        key: int(after["structure"][key]) - int(before["structure"][key])
        for key in before["structure"]
    }
    structural_expansion = (
        structure_delta["section_labels"] > 0 or structure_delta["list_items"] > 0
    )
    fidelity_signals = scope_strengthening_signals(before_text, after_text)
    return {
        "tool": "plain-writing-score-delta",
        "mode": mode,
        "judges_truth_or_quality": False,
        "before": before,
        "after": after,
        "delta": {
            "words": int(after["words"]) - int(before["words"]),
            "words_pct": (
                (int(after["words"]) - int(before["words"]))
                * 100
                / int(before["words"])
                if before["words"]
                else 0.0
            ),
            "errors": int(after["errors"]) - int(before["errors"]),
            "warnings": int(after["warnings"]) - int(before["warnings"]),
            "findings": int(after["findings"]) - int(before["findings"]),
            "findings_per_100_words": after_rate - before_rate,
            "reduction_pct": (
                (before_rate - after_rate) * 100 / before_rate
                if before_rate
                else 0.0
            ),
            "rules": rule_delta,
            "structure": structure_delta,
        },
        "protected_tokens": {
            "requested": len(protected_tokens),
            "retained": len(protected_tokens) - len(lost),
            "lost": lost,
            "source_occurrences": source_occurrences,
            "retained_occurrences": retained_occurrences,
            "retention_pct": (
                retained_occurrences * 100 / source_occurrences
                if source_occurrences
                else 100.0
            ),
            "counts": token_counts,
            "requires_source_count": protected_count,
        },
        "mechanical_regression": mechanical_regression,
        "structural_expansion": structural_expansion,
        "fidelity_signals": fidelity_signals,
        "review_required": (
            "A lower lint rate does not prove that the edit is accurate, "
            "complete, clear, or good. Heading, list, and word reductions are "
            "not fidelity failures."
        ),
    }


def render_human(report: dict[str, object]) -> str:
    before = report["before"]
    after = report["after"]
    delta = report["delta"]
    protected = report["protected_tokens"]
    lines = [
        (
            f"Before: {before['findings']} finding(s), "
            f"{before['findings_per_100_words']:.2f}/100 words, "
            f"{before['words']} word(s)"
        ),
        (
            f"After:  {after['findings']} finding(s), "
            f"{after['findings_per_100_words']:.2f}/100 words, "
            f"{after['words']} word(s)"
        ),
        (
            f"Delta:  {delta['findings']:+d} finding(s), "
            f"{delta['findings_per_100_words']:+.2f}/100 words, "
            f"{delta['reduction_pct']:.1f}% reduction, "
            f"{delta['words']:+d} words ({delta['words_pct']:+.1f}%)"
        ),
    ]
    changed_rules = {
        code: value for code, value in delta["rules"].items() if value
    }
    if changed_rules:
        lines.append(
            "Rules: "
            + ", ".join(
                f"{code} {value:+d}" for code, value in changed_rules.items()
            )
        )
    if protected["requested"]:
        lines.append(
            f"Protected tokens: {protected['retained']}/"
            f"{protected['requested']} retained; "
            f"{protected['retention_pct']:.1f}% of source occurrences; "
            f"count_required={protected['requires_source_count']}"
        )
        if protected["lost"]:
            lines.append("Lost: " + ", ".join(repr(item) for item in protected["lost"]))
    lines.append(str(report["review_required"]))
    if report["structural_expansion"]:
        lines.append("Structural expansion: section labels or list items increased.")
    if report["fidelity_signals"]:
        lines.append(
            "Fidelity review: "
            + "; ".join(item["message"] for item in report["fidelity_signals"])
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path, help="Source text or Markdown file.")
    parser.add_argument("after", type=Path, help="Edited text or Markdown file.")
    parser.add_argument(
        "--mode",
        choices=lint_prose.MODES,
        default="technical",
        help="Language mode. Default: technical.",
    )
    parser.add_argument(
        "--protected-token",
        action="append",
        default=[],
        help="Exact source token that the edit must retain. Repeat as needed.",
    )
    parser.add_argument(
        "--protected-count",
        action="store_true",
        help="Require every source occurrence of each protected token.",
    )
    parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        dest="output_format",
    )
    parser.add_argument(
        "--fail-on-regression",
        action="store_true",
        help="Return 1 if error count or finding rate rises, or a token is lost.",
    )
    parser.add_argument(
        "--fail-on-structural-expansion",
        action="store_true",
        help="Return 1 if heading or list-item count rises.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        report = compare(
            args.before,
            args.after,
            args.mode,
            args.protected_token,
            args.protected_count,
        )
    except (OSError, UnicodeError) as error:
        parser.exit(2, f"score_delta.py: error: {error}\n")
    if args.output_format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_human(report))
    failed = bool(
        report["mechanical_regression"]
        or report["protected_tokens"]["lost"]
    )
    should_fail = (
        (args.fail_on_regression and failed)
        or (args.fail_on_structural_expansion and report["structural_expansion"])
    )
    return 1 if should_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
