#!/usr/bin/env python3
"""
Quality Analyzer (v2 — pure data processing, no OpenClaw API calls)

Takes pre-fetched transcripts (txt files) and computes quality scores.
Mo runs the spawning and history fetching; this script only analyzes data.

Usage:
    python3 scripts/analyze_quality.py \
        --evals evals/weather/quality.json \
        --transcripts workspace/weather/iter-1/raw/transcripts/ \
        --output workspace/weather/iter-1/quality_results.json

Transcript file format:
    workspace/.../raw/transcripts/eval-{id}-with.txt   # with skill
    workspace/.../raw/transcripts/eval-{id}-without.txt # without skill
"""

import argparse
import json
import re
from pathlib import Path
from datetime import datetime


def load_transcript(transcripts_dir: Path, eval_id: int, variant: str) -> str:
    """Load transcript file. variant = 'with' or 'without'."""
    path = transcripts_dir / f"eval-{eval_id}-{variant}.txt"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def score_against_assertions(transcript: str, assertions: list) -> dict:
    """
    Check transcript against each assertion (simple keyword/phrase matching).
    Returns pass/fail per assertion.
    """
    if not assertions:
        return {"passed": 0, "total": 0, "details": []}

    results = []
    transcript_lower = transcript.lower()

    for assertion in assertions:
        # Simple: check if key phrase appears in transcript
        # More complex assertions could use regex or LLM
        check = assertion.lower()
        # Extract key terms (remove common words)
        key_terms = [t for t in check.split() if len(t) > 3
                     and t not in ("that", "this", "with", "from", "uses", "into", "have")]

        passed = any(term in transcript_lower for term in key_terms)
        results.append({
            "assertion": assertion,
            "passed": passed,
            "matched_terms": [t for t in key_terms if t in transcript_lower]
        })

    passed_count = sum(1 for r in results if r["passed"])
    return {
        "passed": passed_count,
        "total": len(assertions),
        "pass_rate": round(passed_count / len(assertions), 2) if assertions else 0,
        "details": results
    }


def estimate_quality_score(transcript: str, assertions_result: dict) -> float:
    """
    Estimate quality score 0-10.
    Combines assertion pass rate + heuristic length/completeness signals.
    """
    if not transcript:
        return 0.0

    score = 5.0  # baseline

    # Assertion bonus
    pass_rate = assertions_result.get("pass_rate", 0)
    score += pass_rate * 3.0  # up to +3

    # Length bonus
    length = len(transcript)
    if length > 200:
        score += 0.5
    if length > 500:
        score += 0.5
    if length > 1000:
        score += 0.5

    # Error penalty
    error_patterns = [r'\berror\b', r'\bfailed\b', r'\bcannot\b', r'\bunable to\b']
    for pattern in error_patterns:
        if re.search(pattern, transcript, re.IGNORECASE):
            score -= 0.5

    # Empty / too short penalty
    if length < 50:
        score -= 3.0

    return round(max(0.0, min(10.0, score)), 1)


def analyze_quality(
    evals_file: str,
    transcripts_dir: str,
    output_file: str,
    verbose: bool = False,
) -> dict:
    """Main quality analysis."""
    with open(evals_file, encoding="utf-8") as f:
        evals_data = json.load(f)

    skill_name = evals_data.get("skill_name", "unknown")
    evals = evals_data.get("evals", [])
    t_dir = Path(transcripts_dir)

    results = []

    for eval_item in evals:
        eval_id = eval_item.get("id")
        name = eval_item.get("name", f"eval-{eval_id}")
        assertions = eval_item.get("assertions", [])

        with_transcript = load_transcript(t_dir, eval_id, "with")
        without_transcript = load_transcript(t_dir, eval_id, "without")

        if not with_transcript and not without_transcript:
            print(f"  ⚠️  Missing transcripts for eval-{eval_id}")
            continue

        with_assertions = score_against_assertions(with_transcript, assertions)
        without_assertions = score_against_assertions(without_transcript, assertions)

        with_score = estimate_quality_score(with_transcript, with_assertions)
        without_score = estimate_quality_score(without_transcript, without_assertions)
        delta = round(with_score - without_score, 1)

        result = {
            "eval_id": eval_id,
            "eval_name": name,
            "with_skill": {
                "quality_score": with_score,
                "assertions": with_assertions,
                "output_length": len(with_transcript),
            },
            "without_skill": {
                "quality_score": without_score,
                "assertions": without_assertions,
                "output_length": len(without_transcript),
            },
            "delta": delta,
            "skill_helps": delta > 0,
        }
        results.append(result)

        if verbose:
         arrow = "↑" if delta > 0 else ("↓" if delta < 0 else "=")
         print(f"  [{eval_id}] {name}: with={with_score} vs without={without_score} "
              f"({arrow}{abs(delta)}) | assertions {with_assertions['passed']}/{with_assertions['total']}")

    if not results:
        print("❌ No results")
        return {}

    avg_with = sum(r["with_skill"]["quality_score"] for r in results) / len(results)
    avg_without = sum(r["without_skill"]["quality_score"] for r in results) / len(results)
    skill_helps_count = sum(1 for r in results if r["skill_helps"])

    output = {
        "skill_name": skill_name,
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "avg_quality_with_skill": round(avg_with, 2),
            "avg_quality_without_skill": round(avg_without, 2),
            "avg_delta": round(avg_with - avg_without, 2),
            "skill_helps_rate": round(skill_helps_count / len(results), 2),
            "total_evals": len(results),
        },
        "results": results,
    }

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print()
    print(f"=== Quality Results ===")
    print(f"With skill:    avg {avg_with:.1f}")
    print(f"Without skill: avg {avg_without:.1f}")
    print(f"Delta:         {avg_with - avg_without:+.1f}")
    print(f"Skill helps:   {skill_helps_count}/{len(results)} evals")
    print(f"✅ Saved to {output_file}")

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Analyze quality scores from pre-fetched transcripts"
    )
    parser.add_argument("--evals", required=True, help="Path to evals JSON")
    parser.add_argument("--transcripts", required=True, help="Directory with eval-{id}-with/without.txt")
    parser.add_argument("--output", required=True, help="Output quality_results.json path")

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output per eval (default: summary only)"
    )
    args = parser.parse_args()

    analyze_quality(
        evals_file=args.evals,
        transcripts_dir=args.transcripts,
        output_file=args.output,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
