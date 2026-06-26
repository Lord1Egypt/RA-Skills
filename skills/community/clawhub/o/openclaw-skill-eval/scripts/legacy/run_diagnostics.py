#!/usr/bin/env python3
"""
Description Diagnostics — Phase 3.2

Diagnose skill description quality issues, output prioritized recommendations.
No automatic optimization (avoids local optimum) — diagnose + human decision.

Usage:
    python scripts/run_diagnostics.py \
        --evals evals/example-triggers.json \
        --skill-path ./SKILL.md \
        --trigger-results workspace/iter-1/trigger_rate_results.json \
        --output-dir workspace/diagnostics-1

    # If no existing trigger results, run trigger test first
    python scripts/run_trigger.py \
        --evals evals/example-triggers.json \
        --output workspace/trigger_results.json
    python scripts/run_diagnostics.py \
        --evals evals/example-triggers.json \
        --skill-path ./SKILL.md \
        --trigger-results workspace/trigger_results.json \
        --output-dir workspace/diagnostics-1

Architecture: ARCHITECTURE.md
Design: PHASE-3-2-DESIGN.md
"""

import argparse
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


# === Data Classes ===

@dataclass
class FailedQuery:
    query_id: str
    query_text: str
    expected: bool
    triggered: bool
    failure_type: str       # "false_negative" | "false_positive"
    severity: str           # "critical" | "high" | "medium" | "low"
    root_cause: str         # "missing_keyword" | "too_broad" | "ambiguous" | "eval_artifact"
    is_worth_fixing: bool
    suggested_fix: str


@dataclass
class DescriptionHealth:
    trigger_recall: float       # 0-1
    trigger_specificity: float  # 0-1
    clarity_score: float        # 0-1 (heuristic)
    coverage_score: float       # 0-1 (heuristic)
    composite_score: float      # weighted
    is_healthy: bool
    weakest_dimension: str


# === Description Analysis ===

def read_skill_description(skill_path: str) -> str:
    """Extract description field from SKILL.md."""
    content = Path(skill_path).read_text(encoding="utf-8")
    
    # Try to extract the description block
    # Common patterns: "description:" or frontmatter or first section
    lines = content.split("\n")
    
    # Look for description in frontmatter (--- block)
    in_frontmatter = False
    desc_lines = []
    for i, line in enumerate(lines):
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter and line.lower().startswith("description:"):
            # Single-line or multi-line description
            desc_lines.append(line[line.index(":") + 1:].strip())
        elif in_frontmatter and desc_lines and line.startswith(" "):
            desc_lines.append(line.strip())
    
    if desc_lines:
        return " ".join(desc_lines)
    
    # Fallback: return first 500 chars of the file
    return content[:500]


def evaluate_clarity(description: str) -> float:
    """
    Heuristic clarity score (0-1).
    NOTE: This is a heuristic, not an LLM judgment.
    Treat results as approximate guidance, not ground truth.

    Checks:
    - Has a short core purpose sentence (+0.2)
    - Has "Use when:" or trigger words section (+0.3)
    - Has "NOT for:" section (+0.3)
    - Reasonable length (100-500 chars) (+0.2)
    """
    score = 0.0

    # Core purpose (first line short)
    first_line = description.split("\n")[0].strip()
    if 10 < len(first_line) < 100:
        score += 0.2

    # USE WHEN section
    use_when_patterns = [
        r"use when",
        r"trigger",
        r"when to use",
        r"use when",
    ]
    if any(re.search(p, description, re.IGNORECASE) for p in use_when_patterns):
        score += 0.3

    # NOT FOR section
    not_for_patterns = [
        r"not for",
        r"not for",
        r"avoid",
        r"avoid",
    ]
    if any(re.search(p, description, re.IGNORECASE) for p in not_for_patterns):
        score += 0.3

    # Length
    length = len(description)
    if 100 < length < 500:
        score += 0.2
    elif 50 < length <= 100 or 500 < length <= 800:
        score += 0.1

    return min(1.0, score)


def evaluate_coverage(description: str, trigger_results: dict) -> float:
    """
    Heuristic coverage score (0-1).
    Based on how many successful trigger queries have keywords in description.
    NOTE: Approximate. Not a substitute for real user testing.
    """
    results = trigger_results.get("results", [])
    correct_positive = [r for r in results if r.get("expected") and r.get("triggered")]

    if not correct_positive:
        return 0.5  # No data, neutral

    desc_lower = description.lower()
    covered = 0
    for r in correct_positive:
        query = r.get("query", "").lower()
        tokens = [t for t in query.split() if len(t) > 2]
        if any(t in desc_lower for t in tokens):
            covered += 1

    return covered / len(correct_positive)


def compute_health(
    trigger_results: dict,
    description: str
) -> DescriptionHealth:
    """Compute multi-dimensional description health."""
    recall = trigger_results.get("recall", 0)
    specificity = trigger_results.get("specificity", 0)
    clarity = evaluate_clarity(description)
    coverage = evaluate_coverage(description, trigger_results)

    # Weighted composite (multiplicative to penalize any weak dimension)
    composite = (
        recall ** 0.4 *
        specificity ** 0.3 *
        clarity ** 0.2 *
        coverage ** 0.1
    )

    is_healthy = (
        recall >= 0.80 and
        specificity >= 0.90 and
        clarity >= 0.70 and
        coverage >= 0.75
    )

    scores = {
        "recall": recall,
        "specificity": specificity,
        "clarity": clarity,
        "coverage": coverage,
    }
    weakest = min(scores, key=scores.get)

    return DescriptionHealth(
        trigger_recall=recall,
        trigger_specificity=specificity,
        clarity_score=clarity,
        coverage_score=coverage,
        composite_score=round(composite, 3),
        is_healthy=is_healthy,
        weakest_dimension=weakest,
    )


# === Failure Classification ===

def classify_failure(result: dict, description: str, all_results: list) -> FailedQuery:
    """Classify a single failure with severity and root cause."""
    query = result.get("query", "")
    expected = result.get("expected", True)
    triggered = result.get("triggered", False)
    query_id = str(result.get("id", "?"))

    failure_type = "false_negative" if expected and not triggered else "false_positive"

    # Find similar failures (same first token)
    first_token = query.split()[0].lower() if query.split() else ""
    similar_failures = [
        r for r in all_results
        if not r.get("correct", False) and
        r.get("query", "").lower().startswith(first_token) and
        r.get("query") != query
    ]
    has_pattern = len(similar_failures) >= 1

    # Root cause analysis
    desc_lower = description.lower()
    query_lower = query.lower()
    query_tokens = [t for t in query_lower.split() if len(t) > 2]
    keyword_in_desc = any(t in desc_lower for t in query_tokens)

    if failure_type == "false_negative":
        if not keyword_in_desc:
            root_cause = "missing_keyword"
        elif len(query_tokens) == 1:
            root_cause = "ambiguous"
        else:
            root_cause = "scope_unclear"
    else:  # false_positive
        root_cause = "too_broad"

    # Severity
    if failure_type == "false_negative":
        if has_pattern:
            severity = "critical"   # Multiple failures → real gap
        elif keyword_in_desc:
            severity = "medium"     # Keyword present but not triggering → ambiguous
        else:
            severity = "high"       # Keyword missing → fixable
    else:  # false_positive
        if has_pattern:
            severity = "high"       # Multiple false positives → description too broad
        else:
            severity = "medium"

    # Is it worth fixing?
    # Don't fix: eval artifacts (single, unusual phrasing), ambiguous edge cases
    query_is_unusual = (
        re.search(r'[A-Za-z]+[^\x00-\x7F]', query) or  # mixed script
        len(query.split()) > 8 or                        # very long query
        len(query.split()) == 1 and len(query) < 4      # single very short token
    )
    is_worth_fixing = (
        severity in ("critical", "high") and
        not (severity == "medium" and not has_pattern) and
        not query_is_unusual
    )

    # Suggested fix
    if failure_type == "false_negative" and root_cause == "missing_keyword":
        missing = [t for t in query_tokens if t not in desc_lower]
        suggested_fix = f"Add keyword(s) to description: {', '.join(missing[:3])}"
    elif failure_type == "false_negative" and root_cause == "scope_unclear":
        suggested_fix = f"Clarify 'Use when' to include phrasing like: '{query[:50]}'"
    elif failure_type == "false_positive":
        suggested_fix = f"Add to 'NOT for' section: '{query[:50]}'"
    else:
        suggested_fix = "Review manually — edge case or eval artifact"

    return FailedQuery(
        query_id=query_id,
        query_text=query,
        expected=expected,
        triggered=triggered,
        failure_type=failure_type,
        severity=severity,
        root_cause=root_cause,
        is_worth_fixing=is_worth_fixing,
        suggested_fix=suggested_fix,
    )


def classify_all_failures(trigger_results: dict, description: str) -> dict:
    """Classify all failures by severity."""
    results = trigger_results.get("results", [])
    failed = [r for r in results if not r.get("correct", True)]

    classified = {
        "critical": [],
        "high": [],
        "medium": [],
        "low": [],
    }

    for r in failed:
        failure = classify_failure(r, description, failed)
        classified[failure.severity].append(failure)

    total_fixable = sum(
        1 for failures in classified.values()
        for f in failures if f.is_worth_fixing
    )

    return {
        "critical": classified["critical"],
        "high": classified["high"],
        "medium": classified["medium"],
        "low": classified["low"],
        "total_failures": len(failed),
        "total_fixable": total_fixable,
        "summary": (
            f"Fix {len(classified['critical'])} critical + "
            f"{len(classified['high'])} high, "
            f"consider {len(classified['medium'])} medium, "
            f"ignore {len(classified['low'])} low/artifacts"
        ),
    }


# === Improvement Estimation ===

def estimate_improvement(failures: dict) -> dict:
    """
    Estimate expected improvement from fixing failures.
    Very rough heuristic — treat as directional only.
    """
    total_queries = failures.get("total_fixable", 0) + len(failures.get("low", []))
    if total_queries == 0:
        return {
            "estimated_recall_gain_pp": 0,
            "estimated_recall_gain": 0,
            "note": "No failures found — description may already be healthy.",
            "warning": "No fixes needed based on current eval set."
        }

    # Assume each fixable critical = +5pp, high = +3pp, medium = +1pp
    gain_pp = (
        len(failures["critical"]) * 5 +
        len(failures["high"]) * 3 +
        len([f for f in failures["medium"] if f.is_worth_fixing]) * 1
    )

    return {
        "estimated_recall_gain_pp": min(gain_pp, 30),  # cap at 30pp
        "note": "Rough estimate. Actual gain depends on description changes.",
        "warning": "Fixing all issues may reduce specificity. Review each fix carefully.",
        "estimated_recall_gain": min(gain_pp, 30),     # alias
    }


# === Report Generation ===

def generate_markdown_report(
    health: DescriptionHealth,
    failures: dict,
    improvement: dict,
    description: str,
    skill_name: str,
    trigger_results: dict,
) -> str:
    lines = [
        f"# Description Diagnostics: {skill_name}",
        "",
        f"Generated: {datetime.now().isoformat()}",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"- Trigger Rate: {trigger_results.get('trigger_rate', 0):.0%} "
        f"(recall: {health.trigger_recall:.0%}, "
        f"specificity: {health.trigger_specificity:.0%})",
        f"- Failed Queries: "
        f"{len(failures['critical'])} critical, "
        f"{len(failures['high'])} high, "
        f"{len(failures['medium'])} medium, "
        f"{len(failures['low'])} low",
        f"- Composite Health Score: {health.composite_score:.2f}",
        f"- Healthy: {'✅ YES' if health.is_healthy else '❌ NO'}",
        f"- Weakest Dimension: **{health.weakest_dimension}**",
        "",
        f"**{failures['summary']}**",
        "",
        "---",
        "",
        "## Health Dimensions",
        "",
        "| Dimension | Score | Threshold | Status |",
        "|-----------|-------|-----------|--------|",
        f"| Recall (trigger) | {health.trigger_recall:.0%} | ≥80% | {'✅' if health.trigger_recall >= 0.80 else '❌'} |",
        f"| Specificity | {health.trigger_specificity:.0%} | ≥90% | {'✅' if health.trigger_specificity >= 0.90 else '❌'} |",
        f"| Clarity (heuristic) | {health.clarity_score:.0%} | ≥70% | {'✅' if health.clarity_score >= 0.70 else '⚠️'} |",
        f"| Coverage (heuristic) | {health.coverage_score:.0%} | ≥75% | {'✅' if health.coverage_score >= 0.75 else '⚠️'} |",
        "",
        "> **Note**: Clarity and Coverage are heuristic estimates based on text patterns.",
        "> They are directional guides, not definitive scores. Use your judgment.",
        "",
        "---",
        "",
    ]

    # Critical issues
    if failures["critical"]:
        lines.extend([
            "## Critical Issues (Must Fix)",
            "",
        ])
        for i, f in enumerate(failures["critical"], 1):
            lines.extend([
                f"### Issue C{i}: \"{f.query_text}\"",
                f"- Type: {f.failure_type.replace('_', ' ')}",
                f"- Root Cause: {f.root_cause.replace('_', ' ')}",
                f"- **Fix**: {f.suggested_fix}",
                "",
            ])

    # High priority
    if failures["high"]:
        lines.extend([
            "## High Priority Issues (Should Fix)",
            "",
        ])
        for i, f in enumerate(failures["high"], 1):
            lines.extend([
                f"### Issue H{i}: \"{f.query_text}\"",
                f"- Type: {f.failure_type.replace('_', ' ')}",
                f"- Root Cause: {f.root_cause.replace('_', ' ')}",
                f"- **Fix**: {f.suggested_fix}",
                "",
            ])

    # Medium / Low (consolidated)
    medium_worth = [f for f in failures["medium"] if f.is_worth_fixing]
    if medium_worth:
        lines.extend([
            "## Medium Priority Issues (Consider)",
            "",
        ])
        for f in medium_worth:
            lines.append(f"- \"{f.query_text}\" — {f.suggested_fix}")
        lines.append("")

    if failures["low"] or [f for f in failures["medium"] if not f.is_worth_fixing]:
        lines.extend([
            "## Ignored Issues (Eval Artifacts / Edge Cases)",
            "",
        ])
        ignored = failures["low"] + [f for f in failures["medium"] if not f.is_worth_fixing]
        for f in ignored:
            lines.append(f"- \"{f.query_text}\" — likely eval artifact, skip")
        lines.append("")

    # Improvement estimate
    lines.extend([
        "---",
        "",
        "## Expected Improvement (Rough Estimate)",
        "",
        f"Fixing critical + high issues: ~+{improvement.get('estimated_recall_gain_pp', improvement.get('estimated_recall_gain', 0))}pp recall",
        "",
        f"> ⚠️  {improvement['warning']}",
        "",
        "---",
        "",
        "## Action Items",
        "",
    ])

    for i, f in enumerate(
        failures["critical"] + failures["high"] + medium_worth, 1
    ):
        lines.append(f"- [ ] {f.suggested_fix}")

    lines.extend([
        "",
        "After changes, re-run trigger test to verify improvement:",
        "```bash",
        "python scripts/run_orchestrator.py \\",
        "    --evals <your-evals> \\",
        "    --skill-path ./SKILL.md \\",
        "    --mode trigger \\",
        "    --output-dir workspace/diagnostics-retest",
        "```",
    ])

    return "\n".join(lines)


# === Main ===

def run_diagnostics(
    evals_file: str,
    skill_path: str,
    trigger_results_file: str,
    output_dir: str,
) -> dict:
    """Run full diagnostics workflow."""

    # Load data
    with open(evals_file, encoding="utf-8") as f:
        evals_data = json.load(f)
    skill_name = evals_data.get("skill_name", Path(skill_path).stem)

    with open(trigger_results_file, encoding="utf-8") as f:
        trigger_results = json.load(f)

    description = read_skill_description(skill_path)

    print(f"Running diagnostics for: {skill_name}")
    print(f"  Trigger rate: {trigger_results.get('trigger_rate', 0):.0%}")
    print(f"  Failed queries: {len([r for r in trigger_results.get('results', []) if not r.get('correct', True)])}")
    print()

    # Analyze
    health = compute_health(trigger_results, description)
    failures = classify_all_failures(trigger_results, description)
    improvement = estimate_improvement(failures)

    print(f"Health: {'✅' if health.is_healthy else '❌'} (composite={health.composite_score:.2f})")
    print(f"Weakest: {health.weakest_dimension}")
    print(f"Critical: {len(failures['critical'])}, High: {len(failures['high'])}, Medium: {len(failures['medium'])}, Low: {len(failures['low'])}")
    print()

    # Build output
    output = {
        "skill_name": skill_name,
        "timestamp": datetime.now().isoformat(),
        "trigger_rate": trigger_results.get("trigger_rate", 0),
        "health": asdict(health),
        "failures": {
            k: [asdict(f) for f in v] if isinstance(v, list) else v
            for k, v in failures.items()
        },
        "improvement_estimate": improvement,
    }

    # Save
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    json_file = out_path / "diagnosis.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {json_file}")

    report = generate_markdown_report(
        health, failures, improvement, description, skill_name, trigger_results
    )
    md_file = out_path / "RECOMMENDATIONS.md"
    md_file.write_text(report, encoding="utf-8")
    print(f"✅ Saved {md_file}")

    # Print action items
    print()
    print("=== Action Items ===")
    all_fixable = (
        failures["critical"] +
        failures["high"] +
        [f for f in failures["medium"] if f.is_worth_fixing]
    )
    if all_fixable:
        for f in all_fixable:
            print(f"  [ ] {f.suggested_fix}")
    else:
        print("  No actionable fixes found.")

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Description Diagnostics — analyze and diagnose skill description quality"
    )
    parser.add_argument("--evals", required=True, help="Path to evals.json")
    parser.add_argument("--skill-path", required=True, help="Path to SKILL.md")
    parser.add_argument(
        "--trigger-results",
        required=True,
        help="Path to trigger_rate_results.json (from run_trigger.py)"
    )
    parser.add_argument(
        "--output-dir",
        default="workspace/diagnostics",
        help="Output directory"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output per eval (default: summary only)"
    )
    args = parser.parse_args()

    run_diagnostics(
        evals_file=args.evals,
        skill_path=args.skill_path,
        trigger_results_file=args.trigger_results,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
