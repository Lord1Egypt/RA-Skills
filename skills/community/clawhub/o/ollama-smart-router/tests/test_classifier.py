#!/usr/bin/env python3
"""
Test suite for the task classifier.
Run with: python -m pytest tests/test_classifier.py -v
Or: python tests/test_classifier.py
"""

import sys
import subprocess
from pathlib import Path

# Test cases: (task, expected_min_score, expected_max_score, description)
TEST_CASES = [
    # Score 1: Simple
    ("What is the capital of France?", 1, 1, "Simple factual question"),
    ("Who invented the telephone?", 1, 1, "Simple who question"),
    ("When did WWII end?", 1, 1, "Simple when question"),
    ("Define entropy", 1, 2, "Definition request"),
    ("List the planets", 1, 2, "List request"),
    
    # Score 2: Basic
    ("Write a hello world in Python", 2, 2, "Simple code"),
    ("Summarize this paragraph", 2, 2, "Summarization"),
    ("Give me an example of a for loop", 2, 2, "Example request"),
    ("Convert 100C to F", 2, 2, "Conversion"),
    
    # False positives (should NOT be high complexity)
    ("What is the zip code for Austin?", 1, 1, "Zip code (not code)"),
    ("Error code 404 meaning", 1, 2, "Error code (not debugging)"),
    ("VS Code shortcuts", 1, 2, "VS Code (not code writing)"),
    
    # Score 3: Complex
    ("Debug this Python script throwing KeyError", 3, 3, "Debugging"),
    ("Compare Python vs JavaScript", 3, 3, "Comparison"),
    ("Analyze this code for bugs", 3, 3, "Analysis"),
    ("Refactor this function to use async", 3, 3, "Refactoring"),
    
    # Score 4: Deep
    ("Design a system for real-time chat", 4, 4, "System design"),
    ("Research the pros and cons of microservices", 4, 4, "Research"),
    ("Write an article about AI safety", 4, 4, "Creative writing"),
    
    # Score 5: Expert
    ("Build a multi-agent system from scratch", 5, 5, "Multi-agent"),
    ("Design a workflow automation system", 5, 5, "Workflow automation"),
]

def run_classifier(task: str) -> tuple[int, str]:
    """Run classifier and return (score, reason)."""
    classify_script = Path(__file__).parent.parent / "scripts" / "classify.py"
    result = subprocess.run(
        [sys.executable, str(classify_script), task],
        capture_output=True,
        text=True
    )
    
    output = result.stdout.strip()
    try:
        score = int(output.split(":")[0])
    except (ValueError, IndexError):
        score = result.returncode if result.returncode in range(1, 6) else 2
    
    reason = output.split(":")[1] if ":" in output else "unknown"
    return score, reason

def test_classifier():
    """Run all test cases."""
    passed = 0
    failed = 0
    
    print("Running classifier tests...")
    print("=" * 70)
    
    for task, min_score, max_score, description in TEST_CASES:
        score, reason = run_classifier(task)
        
        if min_score <= score <= max_score:
            status = "✓ PASS"
            passed += 1
        else:
            status = "✗ FAIL"
            failed += 1
        
        print(f"{status} [{score}] {description}")
        print(f"       Task: {task[:60]}...")
        print(f"       Reason: {reason}")
        print()
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    
    return failed == 0

if __name__ == "__main__":
    success = test_classifier()
    sys.exit(0 if success else 1)
