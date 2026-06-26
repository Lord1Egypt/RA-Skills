#!/usr/bin/env python3
"""Eval runner for pronoun-resolver skill.

Runs each test case through the Tier 1 self-check prompt via claude CLI,
then scores the response against expected outcomes.

Usage:
    python3 evals/run_evals.py                    # Run all cases
    python3 evals/run_evals.py --case high-context-single-file  # Run one case
    python3 evals/run_evals.py --tier1-only       # Skip council tests (faster)
    python3 evals/run_evals.py --dry-run          # Show prompts without calling LLM
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
REPO_DIR = SCRIPT_DIR.parent
CASES_FILE = SCRIPT_DIR / "cases.json"
SELF_CHECK_TEMPLATE = REPO_DIR / "prompts" / "self-check.md"


def load_cases(case_id=None):
    with open(CASES_FILE) as f:
        cases = json.load(f)
    if case_id:
        cases = [c for c in cases if c["id"] == case_id]
        if not cases:
            print(f"ERROR: case '{case_id}' not found")
            sys.exit(1)
    return cases


def build_prompt(case):
    with open(SELF_CHECK_TEMPLATE) as f:
        template = f.read()
    prompt = template
    prompt = prompt.replace("{{USER_MESSAGE}}", case["prompt"])
    prompt = prompt.replace("{{PRONOUNS}}", ",".join(case["pronouns"]))
    prompt = prompt.replace("{{CONVERSATION_CONTEXT}}", case["context"])
    prompt = prompt.replace(
        "{{CONTEXT_RELIABILITY}}", json.dumps(case.get("context_reliability", {}))
    )
    return prompt


def call_haiku(prompt):
    result = subprocess.run(
        ["claude", "-p", "--model", "haiku", "--output-format", "json"],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=45,
    )
    raw = result.stdout.strip()
    try:
        wrapper = json.loads(raw)
        inner = str(wrapper.get("result", raw))
    except (json.JSONDecodeError, TypeError):
        inner = raw

    inner = inner.strip()
    if inner.startswith("```"):
        lines = inner.split("\n")
        end_idx = len(lines) - 1
        for i in range(1, len(lines)):
            if lines[i].strip().startswith("```"):
                end_idx = i
                break
        inner = "\n".join(lines[1:end_idx])

    try:
        return json.loads(inner)
    except (json.JSONDecodeError, TypeError):
        return {"resolutions": [], "parse_error": inner[:200]}


def score_case(case, result):
    expected = case["expected"]
    target_pronoun = expected["pronoun"]
    scores = {}
    details = {}

    resolutions = result.get("resolutions", [])
    match = None
    for r in resolutions:
        if r.get("pronoun") == target_pronoun:
            match = r
            break

    if not match:
        scores["found"] = False
        details["error"] = f"No resolution for pronoun '{target_pronoun}' in response"
        return scores, details, match

    scores["found"] = True
    actual_idiomatic = match.get("idiomatic", False)
    actual_confidence = float(match.get("confidence", 0))
    actual_referent = match.get("referent", "")

    # Idiomatic check -- flexible means either value is acceptable
    if expected.get("expected_idiomatic_flexible"):
        scores["idiomatic_correct"] = True
        details["idiomatic"] = {"expected": "flexible (either ok)", "actual": actual_idiomatic}
    else:
        scores["idiomatic_correct"] = actual_idiomatic == expected["expected_idiomatic"]
        details["idiomatic"] = {"expected": expected["expected_idiomatic"], "actual": actual_idiomatic}

    # Confidence check
    if expected["should_resolve"]:
        scores["confidence_met"] = actual_confidence >= expected["min_confidence"]
        details["confidence"] = {
            "expected_min": expected["min_confidence"],
            "actual": actual_confidence,
        }
    else:
        scores["confidence_met"] = True
        details["confidence"] = {"note": "not applicable (should not resolve)"}

    # Referent check -- fuzzy: normalize hyphens/underscores/spaces, require 50%+ keyword match
    # For flexible idiomatic cases, referent check passes if idiomatic OR if referent matches
    if expected.get("expected_idiomatic_flexible") and actual_idiomatic:
        scores["referent_match"] = True
        scores["referent_partial"] = 1.0
        details["referent"] = {"note": "skipped (idiomatic=true, flexible case)"}
    elif expected["should_resolve"] and expected["expected_referent_contains"]:
        referent_normalized = actual_referent.lower().replace("-", " ").replace("_", " ")
        matches = []
        misses = []
        for keyword in expected["expected_referent_contains"]:
            keyword_normalized = keyword.lower().replace("-", " ").replace("_", " ")
            if keyword_normalized in referent_normalized:
                matches.append(keyword)
            else:
                misses.append(keyword)
        match_ratio = len(matches) / len(expected["expected_referent_contains"])
        scores["referent_match"] = match_ratio >= 0.5
        scores["referent_partial"] = match_ratio
        details["referent"] = {
            "actual": actual_referent,
            "matched_keywords": matches,
            "missed_keywords": misses,
        }
    elif not expected["should_resolve"] and expected.get("expected_referent_contains") and not actual_idiomatic:
        referent_normalized = actual_referent.lower().replace("-", " ").replace("_", " ")
        matches = []
        misses = []
        for keyword in expected["expected_referent_contains"]:
            keyword_normalized = keyword.lower().replace("-", " ").replace("_", " ")
            if keyword_normalized in referent_normalized:
                matches.append(keyword)
            else:
                misses.append(keyword)
        match_ratio = len(matches) / len(expected["expected_referent_contains"]) if expected["expected_referent_contains"] else 1.0
        scores["referent_match"] = match_ratio >= 0.5
        scores["referent_partial"] = match_ratio
        details["referent"] = {
            "actual": actual_referent,
            "matched_keywords": matches,
            "missed_keywords": misses,
            "note": "flexible case: not expected to resolve but did, checking referent quality",
        }
    else:
        scores["referent_match"] = True
        scores["referent_partial"] = 1.0
        details["referent"] = {"note": "not applicable"}

    # Tier prediction (based on confidence vs default threshold 0.8)
    threshold = 0.8
    if expected["should_resolve"]:
        if actual_confidence >= threshold:
            predicted_tier = "self-check"
        else:
            predicted_tier = "council"
    else:
        predicted_tier = "self-check"

    if expected.get("expected_tier_flexible"):
        scores["tier_correct"] = True
        details["tier"] = {"expected": "flexible", "predicted": predicted_tier}
    else:
        scores["tier_correct"] = predicted_tier == expected["expected_tier"]
        details["tier"] = {"expected": expected["expected_tier"], "predicted": predicted_tier}

    return scores, details, match


def run_evals(case_id=None, tier1_only=True, dry_run=False):
    cases = load_cases(case_id)
    print(f"Running {len(cases)} eval case(s)...\n")

    results = []
    total_pass = 0
    total_fail = 0
    total_cases = len(cases)

    for i, case in enumerate(cases):
        print(f"[{i+1}/{total_cases}] {case['id']}: {case['description']}")
        prompt = build_prompt(case)

        if dry_run:
            print(f"  PROMPT ({len(prompt)} chars): {prompt[:100]}...")
            print()
            continue

        start = time.time()
        try:
            result = call_haiku(prompt)
        except subprocess.TimeoutExpired:
            result = {"resolutions": [], "error": "timeout"}
        except Exception as e:
            result = {"resolutions": [], "error": str(e)}
        elapsed = time.time() - start

        if "parse_error" in result:
            print(f"  PARSE ERROR: {result['parse_error']}")
            total_fail += 1
            results.append({"case": case["id"], "pass": False, "error": "parse_error"})
            continue

        scores, details, match = score_case(case, result)

        if not scores.get("found"):
            print(f"  FAIL: {details.get('error', 'unknown')}")
            print(f"  Raw: {json.dumps(result, indent=2)[:200]}")
            total_fail += 1
            results.append({"case": case["id"], "pass": False, "error": "not_found"})
            continue

        all_pass = all(
            v
            for k, v in scores.items()
            if k not in ("referent_partial",) and isinstance(v, bool)
        )

        status = "PASS" if all_pass else "FAIL"
        if all_pass:
            total_pass += 1
        else:
            total_fail += 1

        print(f"  {status} ({elapsed:.1f}s)")
        print(f"    Confidence: {details['confidence']}")
        print(f"    Idiomatic:  expected={details['idiomatic']['expected']}, actual={details['idiomatic']['actual']} {'ok' if scores['idiomatic_correct'] else 'MISMATCH'}")
        if details["referent"].get("actual"):
            print(f"    Referent:   \"{details['referent']['actual']}\"")
            if details["referent"].get("missed_keywords"):
                print(f"    Missing:    {details['referent']['missed_keywords']}")
        print(f"    Tier:       expected={details['tier']['expected']}, predicted={details['tier']['predicted']} {'ok' if scores['tier_correct'] else 'MISMATCH'}")
        print()

        results.append({
            "case": case["id"],
            "pass": all_pass,
            "scores": {k: v for k, v in scores.items() if isinstance(v, (bool, float))},
            "confidence": match.get("confidence") if match else None,
            "referent": match.get("referent") if match else None,
            "elapsed_s": round(elapsed, 1),
        })

    if dry_run:
        return

    # Summary
    print("=" * 60)
    print(f"RESULTS: {total_pass}/{total_cases} passed, {total_fail}/{total_cases} failed")
    print()

    if total_fail > 0:
        print("Failed cases:")
        for r in results:
            if not r["pass"]:
                print(f"  - {r['case']}: {r.get('error', 'assertion failure')}")
        print()

    # Confidence distribution
    confidences = [r["confidence"] for r in results if r.get("confidence") is not None]
    if confidences:
        print(f"Confidence: min={min(confidences):.2f} max={max(confidences):.2f} avg={sum(confidences)/len(confidences):.2f}")

    # Latency
    latencies = [r["elapsed_s"] for r in results if "elapsed_s" in r]
    if latencies:
        print(f"Latency:    min={min(latencies):.1f}s max={max(latencies):.1f}s avg={sum(latencies)/len(latencies):.1f}s")

    # Write results
    results_file = SCRIPT_DIR / "results.json"
    with open(results_file, "w") as f:
        json.dump(
            {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "total": total_cases,
                "passed": total_pass,
                "failed": total_fail,
                "cases": results,
            },
            f,
            indent=2,
        )
    print(f"\nResults written to {results_file}")

    return total_fail == 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run pronoun-resolver evals")
    parser.add_argument("--case", help="Run a single case by ID")
    parser.add_argument("--tier1-only", action="store_true", default=True, help="Only test Tier 1 (default)")
    parser.add_argument("--dry-run", action="store_true", help="Show prompts without calling LLM")
    args = parser.parse_args()

    success = run_evals(case_id=args.case, tier1_only=args.tier1_only, dry_run=args.dry_run)
    sys.exit(0 if success else 1)
