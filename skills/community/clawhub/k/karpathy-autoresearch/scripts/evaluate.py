#!/usr/bin/env python3
"""
Autoresearch — Generic Evaluation Harness

Template for scoring a mutable file against test cases.
Customize the `score_one()` function for your domain.

Usage:
    python evaluate.py <mutable_file> <test_cases.json>
    python evaluate.py strategy.json tests/cases.json
    python evaluate.py SKILL.md eval/test_cases.json

Output:
    Prints "SCORE: <float>" to stdout (parsed by the loop).
"""

import json
import sys
import os
from pathlib import Path


def score_one(mutable_content: str, test_case: dict) -> float:
    """
    Score a single test case against the current mutable content.
    
    CUSTOMIZE THIS for your domain:
    
    Examples:
    
    1. LLM-as-judge (content/prompts):
        response = call_llm(mutable_content, test_case["input"])
        judge_score = call_llm(f"Rate this 1-100: {response}")
        return float(judge_score)
    
    2. Binary pass/fail (code/logic):
        output = run_with_config(mutable_content, test_case["input"])
        return 1.0 if output == test_case["expected"] else 0.0
    
    3. Numeric metric (trading/analytics):
        result = backtest(mutable_content, test_case["data"])
        return result["sharpe_ratio"]
    
    4. Similarity scoring (text quality):
        output = generate(mutable_content, test_case["input"])
        return cosine_similarity(output, test_case["reference"])
    
    Args:
        mutable_content: The full text of the mutable file being optimized
        test_case: A dict from your test_cases.json array
    
    Returns:
        A float score. Higher is better.
    """
    # --- REPLACE THIS WITH YOUR LOGIC ---
    raise NotImplementedError(
        "You must implement score_one() for your domain.\n"
        "See the examples in the docstring above."
    )


def evaluate(mutable_file: str, test_cases_file: str) -> dict:
    """
    Run all test cases and return aggregate results.
    
    Returns dict with:
        - score: float (mean score across all cases)
        - total: int (number of test cases)
        - scores: list[float] (individual scores)
        - min: float
        - max: float
    """
    with open(mutable_file, "r", encoding="utf-8") as f:
        mutable_content = f.read()
    
    with open(test_cases_file, "r", encoding="utf-8") as f:
        test_cases = json.load(f)
    
    if not isinstance(test_cases, list):
        # Support {"cases": [...]} wrapper format
        test_cases = test_cases.get("cases", test_cases.get("test_cases", []))
    
    if not test_cases:
        print("ERROR: No test cases found", file=sys.stderr)
        sys.exit(1)
    
    scores = []
    for i, case in enumerate(test_cases):
        try:
            s = score_one(mutable_content, case)
            scores.append(float(s))
        except NotImplementedError:
            raise
        except Exception as e:
            print(f"WARNING: Test case {i} failed: {e}", file=sys.stderr)
            scores.append(0.0)
    
    result = {
        "score": sum(scores) / len(scores),
        "total": len(scores),
        "scores": scores,
        "min": min(scores),
        "max": max(scores),
    }
    
    return result


def main():
    if len(sys.argv) < 3:
        print("Usage: python evaluate.py <mutable_file> <test_cases.json>")
        print()
        print("The mutable_file is whatever you're optimizing.")
        print("test_cases.json is a JSON array of test case objects.")
        print()
        print("You MUST customize score_one() in this file for your domain.")
        sys.exit(1)
    
    mutable_file = sys.argv[1]
    test_cases_file = sys.argv[2]
    
    if not os.path.exists(mutable_file):
        print(f"ERROR: Mutable file not found: {mutable_file}", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.exists(test_cases_file):
        print(f"ERROR: Test cases file not found: {test_cases_file}", file=sys.stderr)
        sys.exit(1)
    
    result = evaluate(mutable_file, test_cases_file)
    
    # The loop.py parses this line
    print(f"SCORE: {result['score']:.4f}")
    print(f"  Cases: {result['total']} | Min: {result['min']:.4f} | Max: {result['max']:.4f}")


if __name__ == "__main__":
    main()
