#!/usr/bin/env python3
"""
MORDRED TEST RUNNER — Morgana's Security Testing Framework
Run all vulnerability tests and collect results
"""

import os
import sys
import json
import subprocess
from datetime import datetime

SANDBOX_PATH = "/media/ezekiel/Morgana/sandbox/mordred"
SYSTEMS_PATH = f"{SANDBOX_PATH}/systems"
RESULTS_PATH = f"{SANDBOX_PATH}/results"
LOG_PATH = f"{SANDBOX_PATH}/logs"

TESTS = [
    {"name": "flawed_auth", "description": "SQL injection & auth bypass", "risk": "CRITICAL"},
    {"name": "weak_sandbox", "description": "Code execution escape", "risk": "CRITICAL"},
    {"name": "prompt_injection", "description": "Prompt injection vectors", "risk": "HIGH"},
    {"name": "data_leak", "description": "Information disclosure", "risk": "HIGH"},
    {"name": "race_condition", "description": "TOCTOU race conditions", "risk": "MEDIUM"},
]

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(f"{LOG_PATH}/mordred.log", "a") as f:
        f.write(line + "\n")

def run_test(test_name):
    """Execute a test system and capture output"""
    test_file = f"{SYSTEMS_PATH}/{test_name}.py"
    
    if not os.path.exists(test_file):
        return {"status": "ERROR", "output": "Test file not found"}
    
    try:
        result = subprocess.run(
            ["python3", test_file],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=SYSTEMS_PATH
        )
        return {
            "status": "COMPLETED",
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {"status": "ERROR", "output": str(e)}

def run_all_tests():
    """Run all vulnerability tests"""
    log("=== MORDRED TEST SUITE STARTING ===")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": []
    }
    
    for test in TESTS:
        log(f"Running: {test['name']} ({test['description']})")
        result = run_test(test['name'])
        
        results['tests'].append({
            "name": test['name'],
            "description": test['description'],
            "risk": test['risk'],
            "result": result
        })
        
        log(f"  → Status: {result['status']}")
    
    # Save results
    results_file = f"{RESULTS_PATH}/results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    
    log(f"=== RESULTS SAVED TO: {results_file} ===")
    
    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test" and len(sys.argv) > 2:
            result = run_test(sys.argv[2])
            print(json.dumps(result, indent=2))
        elif sys.argv[1] == "--all":
            results = run_all_tests()
            print(f"\nRan {len(results['tests'])} tests")
    else:
        print("Usage:")
        print("  python3 mordred_runner.py --all    # Run all tests")
        print("  python3 mordred_runner.py --test <name>  # Run specific test")
