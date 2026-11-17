#!/usr/bin/env python3
"""
MAGI Weighted Scoring Calculator
===============================
Implements the three-wise-man weighted scoring system for multi-option comparison.

INTERFACE CONTRACT
==================
Input:  Command-line arguments (optional --json flag); sample data is hardcoded
Output: Formatted scoring results to stdout; optional JSON to stdout
Side effects: None
Exit codes: 0 = success, 1 = input validation error, 2 = runtime error
Dependencies: Python standard library only
"""

import argparse
import json
import sys


def magi_score(options: dict, weights: dict = None) -> list:
    """
    Score multiple options using the MAGI three-wise-man weighted scoring system.

    Parameters:
        options: Dict mapping option names to score dicts.
                 Each score dict has keys 'melchior', 'balthasar', 'casper',
                 each mapping to a dict of {dimension: score}.
        weights: Dict mapping persona names to weights.
                 Default: {"melchior": 0.35, "balthasar": 0.35, "casper": 0.30}

    Returns:
        List of result dicts sorted by total score descending.
        Each result dict contains: name, total, breakdown, verdict.
    """
    if weights is None:
        weights = {"melchior": 0.35, "balthasar": 0.35, "casper": 0.30}

    # Validate weights sum to 1.0
    weight_sum = sum(weights.values())
    if abs(weight_sum - 1.0) > 0.01:
        raise ValueError(f"Weights must sum to 1.0, got {weight_sum}")

    results = []
    for name, scores in options.items():
        total = 0.0
        breakdown = {}
        for persona, weight in weights.items():
            if persona not in scores or not scores[persona]:
                continue
            persona_avg = sum(scores[persona].values()) / len(scores[persona])
            weighted = persona_avg * weight
            total += weighted
            breakdown[persona] = {
                "avg": round(persona_avg, 2),
                "weighted": round(weighted, 2),
            }

        if total >= 7.5:
            verdict = "Recommended"
        elif total >= 6.0:
            verdict = "Conditionally Recommended"
        else:
            verdict = "Not Recommended"

        results.append({
            "name": name,
            "total": round(total, 2),
            "breakdown": breakdown,
            "verdict": verdict,
        })

    results.sort(key=lambda x: x["total"], reverse=True)
    return results


def print_results(results: list) -> None:
    """Print formatted scoring results to stdout."""
    print()
    print("=" * 60)
    print("  MAGI Three-Wise-Man Weighted Scoring Results")
    print("=" * 60)

    for i, r in enumerate(results, 1):
        print()
        print(f"  Rank #{i}: {r['name']}")
        print(f"  Total Score: {r['total']} -> {r['verdict']}")
        print(f"  {'-' * 50}")
        for persona, detail in r["breakdown"].items():
            print(f"    {persona.upper():12s}  avg {detail['avg']:5.2f}  x weight  ->  contribution {detail['weighted']:5.2f}")

    # Gap analysis
    if len(results) >= 2:
        gap = results[0]["total"] - results[1]["total"]
        print()
        print(f"  {'=' * 50}")
        print(f"  Gap between 1st and 2nd: {gap:.2f}")
        if gap < 0.5:
            print(f"  WARNING: Gap < 0.5, marked as 'substantially equivalent', recommend additional information or pilot validation")
        else:
            print(f"  CLEAR: Gap is significant, recommended option has clear distinction")

    print()
    print("=" * 60)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Calculate MAGI weighted scores.")
    parser.add_argument("--json", action="store_true", help="Also print JSON results.")
    args = parser.parse_args()
    try:
        # Sample data
        sample_options = {
            "Option A - Aggressive Expansion": {
                "melchior": {"revenue_potential": 9, "logical_feasibility": 6, "data_support": 7},
                "balthasar": {"risk_controllability": 4, "ethical_compliance": 8, "long_term_safety": 5},
                "casper": {"timing_alignment": 8, "team_acceptance": 5, "trend_fit": 9},
            },
            "Option B - Steady Iteration": {
                "melchior": {"revenue_potential": 6, "logical_feasibility": 9, "data_support": 8},
                "balthasar": {"risk_controllability": 9, "ethical_compliance": 9, "long_term_safety": 8},
                "casper": {"timing_alignment": 6, "team_acceptance": 8, "trend_fit": 6},
            },
            "Option C - Strategic Alliance": {
                "melchior": {"revenue_potential": 7, "logical_feasibility": 7, "data_support": 6},
                "balthasar": {"risk_controllability": 7, "ethical_compliance": 8, "long_term_safety": 7},
                "casper": {"timing_alignment": 7, "team_acceptance": 7, "trend_fit": 7},
            },
        }

        results = magi_score(sample_options)
        print_results(results)

        # Optional JSON output
        if args.json:
            print()
            print("--- JSON Output ---")
            print(json.dumps(results, ensure_ascii=False, indent=2))

        return 0

    except ValueError as e:
        print(f"Input validation error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Runtime error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
