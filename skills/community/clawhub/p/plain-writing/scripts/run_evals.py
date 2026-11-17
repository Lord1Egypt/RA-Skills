#!/usr/bin/env python3
"""Run Plain Writing's focused behavior and context-budget evaluations."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

SKILL_ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

import lint_prose  # noqa: E402

CASES_PATH = SKILL_ROOT / "evals" / "cases.json"
SKILL_PATH = SKILL_ROOT / "SKILL.md"
MAX_SKILL_LINES = 220
MAX_SKILL_WORDS = 1250
MAX_ESTIMATED_TOKENS = 2200


def labels(result: lint_prose.LintResult) -> list[str]:
    return [f"{item.code}:{item.severity}" for item in result.findings]


def run_evals() -> dict[str, object]:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    failures: list[str] = []
    checks = 0
    covered: set[str] = set()

    for case in cases:
        expected_by_mode = case.get("expect", {})
        missing_modes = {"strict", "technical"} - set(expected_by_mode)
        if missing_modes:
            failures.append(
                f"{case['id']}: missing mode expectations: {sorted(missing_modes)}"
            )
            continue

        for mode in lint_prose.MODES:
            checks += 1
            expected = list(
                expected_by_mode.get(mode, expected_by_mode["technical"])
            )
            actual = labels(
                lint_prose.lint_text(
                    case["text"],
                    path=f"<eval:{case['id']}>",
                    mode=mode,
                )
            )
            covered.update(label.split(":", 1)[0] for label in expected)
            if Counter(actual) != Counter(expected):
                failures.append(
                    f"{case['id']} [{mode}]: expected {expected}, got {actual}"
                )

    missing_rules = set(lint_prose.RULES) - covered
    if missing_rules:
        failures.append(f"missing positive eval coverage: {sorted(missing_rules)}")

    phrase_groups = {
        "CLR007": lint_prose.NOMINAL_PHRASES,
        "CLR008": lint_prose.PHRASAL,
        "WRD001": lint_prose.INFLATED,
        "WRD002": lint_prose.PROMOTIONAL,
        "WRD003": lint_prose.HEDGES,
        "WRD004": lint_prose.CLICHES,
        "WRD005": lint_prose.VAGUE,
        "WRD006": lint_prose.WEASEL_ATTRIBUTIONS,
        "WRD007": lint_prose.IMPORTANCE_PUFFERY,
        "WRD009": lint_prose.GENERIC_ENDINGS,
        "WRD011": lint_prose.AI_DICTION,
    }
    phrase_owners: dict[str, str] = {}
    lexicon_checks = 0
    for code, phrases in phrase_groups.items():
        for phrase in phrases:
            normalized = phrase.lower()
            previous = phrase_owners.get(normalized)
            if previous and previous != code:
                failures.append(
                    f"phrase {phrase!r} appears in both {previous} and {code}"
                )
            phrase_owners[normalized] = code
            for mode in lint_prose.MODES:
                expected_level = lint_prose.severity_for(mode, code)
                if expected_level == "off":
                    continue
                lexicon_checks += 1
                result = lint_prose.lint_text(
                    f"The draft contains {phrase}.",
                    path=f"<lexicon:{code}:{phrase}>",
                    mode=mode,
                )
                matches = [
                    item for item in result.findings if item.code == code
                ]
                if not matches:
                    failures.append(
                        f"lexicon {phrase!r} did not trigger {code} in {mode}"
                    )
                elif any(item.severity != expected_level for item in matches):
                    levels = sorted({item.severity for item in matches})
                    failures.append(
                        f"lexicon {phrase!r} [{mode}] expected "
                        f"{expected_level}, got {levels}"
                    )

    for code, rule in lint_prose.RULES.items():
        if not rule.title.strip() or not rule.suggestion.strip():
            failures.append(f"{code} lacks an actionable title or suggestion")
    base_rules = {code for code in lint_prose.RULES if not code.startswith("STR")}
    structural_rules = {code for code in lint_prose.RULES if code.startswith("STR")}
    for mode in lint_prose.MODES:
        configured = set(lint_prose.MODE_CONFIG[mode]["severity"])
        if configured != base_rules:
            missing = sorted(base_rules - configured)
            extra = sorted(configured - base_rules)
            failures.append(
                f"{mode} rule configuration mismatch; missing={missing}, extra={extra}"
            )
    if set(lint_prose.ANTI_SLOP_SEVERITY) != structural_rules:
        failures.append("structural anti-slop rule configuration mismatch")

    skill_text = SKILL_PATH.read_text(encoding="utf-8")
    skill_lines = len(skill_text.splitlines())
    skill_words = len(skill_text.split())
    estimated_tokens = (len(skill_text) + 3) // 4
    if skill_lines > MAX_SKILL_LINES:
        failures.append(
            f"SKILL.md has {skill_lines} lines; budget is {MAX_SKILL_LINES}"
        )
    if skill_words > MAX_SKILL_WORDS:
        failures.append(
            f"SKILL.md has {skill_words} words; budget is {MAX_SKILL_WORDS}"
        )
    if estimated_tokens > MAX_ESTIMATED_TOKENS:
        failures.append(
            "SKILL.md estimated token count is "
            f"{estimated_tokens}; budget is {MAX_ESTIMATED_TOKENS}"
        )

    self_lint: dict[str, dict[str, int]] = {}
    for mode in lint_prose.MODES:
        result = lint_prose.lint_text(
            skill_text,
            path=str(SKILL_PATH),
            mode=mode,
        )
        self_lint[mode] = {
            "errors": result.errors,
            "warnings": result.warnings,
        }
        if result.errors or result.warnings:
            failures.append(
                f"SKILL.md self-lint [{mode}]: "
                f"{result.errors} errors, {result.warnings} warnings"
            )

    return {
        "passed": not failures,
        "cases": len(cases),
        "mode_checks": checks,
        "covered_rules": len(covered),
        "total_rules": len(lint_prose.RULES),
        "lexicon_entries": len(phrase_owners),
        "lexicon_mode_checks": lexicon_checks,
        "skill_budget": {
            "lines": skill_lines,
            "max_lines": MAX_SKILL_LINES,
            "words": skill_words,
            "max_words": MAX_SKILL_WORDS,
            "estimated_tokens": estimated_tokens,
            "max_estimated_tokens": MAX_ESTIMATED_TOKENS,
        },
        "self_lint": self_lint,
        "failures": failures,
    }


def render_human(report: dict[str, object]) -> str:
    budget = report["skill_budget"]
    lines = [
        "PASS" if report["passed"] else "FAIL",
        (
            f"Cases: {report['cases']} "
            f"({report['mode_checks']} mode checks)"
        ),
        (
            f"Rule coverage: {report['covered_rules']}/"
            f"{report['total_rules']}"
        ),
        (
            f"Lexicon checks: {report['lexicon_entries']} entries, "
            f"{report['lexicon_mode_checks']} active-mode checks"
        ),
        (
            "SKILL.md budget: "
            f"{budget['lines']}/{budget['max_lines']} lines, "
            f"{budget['words']}/{budget['max_words']} words, "
            f"~{budget['estimated_tokens']}/{budget['max_estimated_tokens']} tokens"
        ),
    ]
    for mode, counts in report["self_lint"].items():
        lines.append(
            f"Self-lint {mode}: "
            f"{counts['errors']} error(s), {counts['warnings']} warning(s)"
        )
    for failure in report["failures"]:
        lines.append(f"- {failure}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("human", "json"), default="human")
    args = parser.parse_args()
    report = run_evals()
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_human(report))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
