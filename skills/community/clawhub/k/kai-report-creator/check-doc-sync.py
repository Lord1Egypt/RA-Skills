#!/usr/bin/env python3
"""
check-doc-sync.py -- lightweight contract checker for kai-report-creator review docs.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RuleResult:
    name: str
    ok: bool
    detail: str


def read_required(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    return path.read_text(encoding="utf-8")


def contains_all(text: str, snippets: list[str]) -> tuple[bool, str]:
    missing = [snippet for snippet in snippets if snippet not in text]
    if missing:
        return False, "missing: " + ", ".join(repr(item) for item in missing)
    return True, "all expected markers present"


def contains_none(text: str, snippets: list[str]) -> tuple[bool, str]:
    present = [snippet for snippet in snippets if snippet in text]
    if present:
        return False, "unexpected: " + ", ".join(repr(item) for item in present)
    return True, "no forbidden markers present"


def evaluate(root: Path) -> list[RuleResult]:
    skill = read_required(root / "SKILL.md")
    readme_en = read_required(root / "README.md")
    readme_zh = read_required(root / "README.zh-CN.md")
    checklist = read_required(root / "references" / "review-checklist.md")

    results: list[RuleResult] = []

    ok, detail = contains_all(
        skill,
        [
            "--review [file]",
            "references/review-checklist.md",
            "references/review-report-template.md",
            "silent final review pass",
            "one-pass automatic refinement",
        ],
    )
    results.append(RuleResult("skill-contract", ok, detail))

    ok, detail = contains_all(
        readme_en,
        [
            "/report --review",
            "13-checkpoint review system",
            "silent final review",
            "review-report-template.md",
        ],
    )
    results.append(RuleResult("readme-en-contract", ok, detail))

    ok, detail = contains_all(
        readme_zh,
        [
            "/report --review",
            "13 项检查点",
            "静默终审",
            "review-report-template.md",
        ],
    )
    results.append(RuleResult("readme-zh-contract", ok, detail))

    ok, detail = contains_all(
        checklist,
        [
            "### 1.1 BLUF Opening",
            "### 1.5 Takeaway After Data",
            "### 2.3 Conditional Reader Guidance",
            "## Rejected Candidates",
        ],
    )
    results.append(RuleResult("checklist-contract", ok, detail))

    # v4 guardrails: Doc drift protection (验收清单 #11, #12)
    ok, detail = contains_all(
        skill,
        [
            "no file given",  # SKILL.md must preserve context-backed generate prose
            "IR from context",  # SKILL.md must preserve IR-from-context routing
        ],
    )
    results.append(RuleResult("skill-context-backed-contract", ok, detail))

    ok, detail = contains_all(
        skill,
        [
            "report_class: mixed",  # SKILL.md must preserve optional report_class prose
        ],
    )
    results.append(RuleResult("report_class-mixed-contract", ok, detail))

    ok, detail = contains_all(
        skill,
        [
            "extract exactly one valid IR block from context",
            "Never render the surrounding conversation.",
            "Load reference files minimally",
            "load only the references that materially help the current render path",
        ],
    )
    results.append(RuleResult("skill-late-context-boundary-contract", ok, detail))

    ok, detail = contains_none(
        skill,
        [
            "read ALL of these before generating any HTML",
        ],
    )
    results.append(RuleResult("skill-no-full-reference-load-contract", ok, detail))

    ok, detail = contains_all(
        skill,
        [
            "Thin Routing Over Prompt Growth",
            "Contracts and Gates Beat Prompt Soup",
        ],
    )
    results.append(RuleResult("skill-context-budget-contract", ok, detail))

    ok, detail = contains_all(
        readme_en,
        [
            "Capability Growth Must Reduce Context Load",
            "Move quality checks off the hot path.",
        ],
    )
    results.append(RuleResult("readme-en-context-budget-contract", ok, detail))

    ok, detail = contains_all(
        readme_zh,
        [
            "能力增长先减少上下文负担",
            "质量机制后移",
        ],
    )
    results.append(RuleResult("readme-zh-context-budget-contract", ok, detail))

    return results


def print_results(results: list[RuleResult], dry_run: bool) -> int:
    if dry_run:
        print("DRY RUN: checking document contracts only, no files will be changed.")

    failures = 0
    for result in results:
        status = "PASS" if result.ok else "FAIL"
        print(f"{status} {result.name}: {result.detail}")
        if not result.ok:
            failures += 1

    if failures:
        print(f"\nSummary: {failures} rule(s) failed.")
        return 1

    print(f"\nSummary: {len(results)} rule(s) passed.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root to inspect.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Check-only mode. This script never modifies files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    try:
        results = evaluate(root)
    except FileNotFoundError as exc:
        print(f"FAIL missing-file: {exc}")
        return 1
    return print_results(results, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
