#!/usr/bin/env python3
"""
Autoresearch — Autonomous Experiment Loop

Runs the mutate → evaluate → keep/revert cycle with git tracking.

This script is a REFERENCE IMPLEMENTATION. In practice, the OpenClaw agent
runs the loop itself (reading files, making mutations via LLM, evaluating,
and committing). This script shows the exact algorithm.

Usage:
    python loop.py \
        --mutable strategy.json \
        --eval "python evaluate.py strategy.json tests/cases.json" \
        --experiments 20

Algorithm:
    1. Git init + baseline commit
    2. Run eval → baseline score
    3. For each experiment:
        a. Backup mutable file
        b. Apply mutation (user-provided or random)
        c. Run eval → new score
        d. If improved: git commit, update baseline
        e. If not: revert from backup
    4. Print summary
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


def run_eval(eval_cmd: str) -> float:
    """Run the evaluation command and parse SCORE from output."""
    try:
        result = subprocess.run(
            eval_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300,  # 5 min timeout per eval
        )
        
        output = result.stdout + result.stderr
        
        # Parse "SCORE: <number>" from output
        match = re.search(r"SCORE:\s*([\d.+-]+)", output)
        if match:
            return float(match.group(1))
        
        # Fallback: try to parse last line as a number
        lines = [l.strip() for l in output.strip().split("\n") if l.strip()]
        if lines:
            try:
                return float(lines[-1])
            except ValueError:
                pass
        
        print(f"ERROR: Could not parse score from eval output:\n{output}", file=sys.stderr)
        return float("-inf")
    
    except subprocess.TimeoutExpired:
        print("ERROR: Eval timed out (300s)", file=sys.stderr)
        return float("-inf")
    except Exception as e:
        print(f"ERROR: Eval failed: {e}", file=sys.stderr)
        return float("-inf")


def git_init(workdir: str):
    """Initialize git repo if not already initialized."""
    subprocess.run(["git", "init"], cwd=workdir, capture_output=True)
    subprocess.run(["git", "add", "-A"], cwd=workdir, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "autoresearch: initial state", "--allow-empty"],
        cwd=workdir,
        capture_output=True,
    )


def git_commit(workdir: str, message: str):
    """Stage all changes and commit."""
    subprocess.run(["git", "add", "-A"], cwd=workdir, capture_output=True)
    subprocess.run(["git", "commit", "-m", message], cwd=workdir, capture_output=True)


def git_revert_file(workdir: str, filepath: str):
    """Revert a single file to last committed version."""
    subprocess.run(
        ["git", "checkout", "--", filepath], cwd=workdir, capture_output=True
    )


def run_loop(
    mutable_file: str,
    eval_cmd: str,
    num_experiments: int,
    workdir: str,
    log_file: str = None,
):
    """
    Main autoresearch loop.
    
    In the reference implementation, mutations are done by copying
    a pre-generated mutation file. In practice, the OpenClaw agent
    generates mutations via LLM reasoning.
    """
    mutable_path = Path(mutable_file)
    if not mutable_path.exists():
        print(f"ERROR: Mutable file not found: {mutable_file}")
        sys.exit(1)
    
    # Initialize
    git_init(workdir)
    
    log = []
    start_time = time.time()
    
    # Baseline
    print("=" * 60)
    print("AUTORESEARCH — Autonomous Experiment Loop")
    print("=" * 60)
    print(f"Mutable file: {mutable_file}")
    print(f"Eval command: {eval_cmd}")
    print(f"Experiments:  {num_experiments}")
    print()
    
    baseline = run_eval(eval_cmd)
    print(f"📊 BASELINE SCORE: {baseline:.4f}")
    print()
    
    git_commit(workdir, f"baseline: score {baseline:.4f}")
    
    best_score = baseline
    improvements = 0
    
    for i in range(1, num_experiments + 1):
        print(f"--- Experiment {i}/{num_experiments} ---")
        
        # In practice, the agent reads the file, reasons about a mutation,
        # and writes the modified version. This script expects the user
        # to provide mutations interactively or via a mutation script.
        
        # For automated use, you'd integrate an LLM call here:
        # mutation_description = llm_generate_mutation(mutable_content)
        # mutated_content = llm_apply_mutation(mutable_content, mutation_description)
        
        # Run eval on current state (after external mutation)
        print("  Waiting for mutation (modify the mutable file, then press Enter)...")
        
        # Check if running non-interactively
        if not sys.stdin.isatty():
            print("  ERROR: Non-interactive mode requires agent-driven mutations")
            break
        
        input("  Press Enter after applying mutation...")
        
        new_score = run_eval(eval_cmd)
        delta = new_score - best_score
        
        entry = {
            "experiment": i,
            "score": new_score,
            "delta": delta,
            "baseline": best_score,
            "timestamp": datetime.now().isoformat(),
        }
        
        if new_score > best_score:
            print(f"  ✅ KEPT — {best_score:.4f} → {new_score:.4f} (+{delta:.4f})")
            git_commit(workdir, f"exp-{i}: score {best_score:.4f} → {new_score:.4f}")
            best_score = new_score
            improvements += 1
            entry["status"] = "kept"
        else:
            print(f"  ❌ REVERTED — {new_score:.4f} <= {best_score:.4f} ({delta:+.4f})")
            git_revert_file(workdir, str(mutable_path))
            entry["status"] = "reverted"
        
        log.append(entry)
        print()
    
    # Summary
    elapsed = time.time() - start_time
    print("=" * 60)
    print("AUTORESEARCH — Summary")
    print("=" * 60)
    print(f"  Experiments run:  {len(log)}")
    print(f"  Improvements:     {improvements}")
    print(f"  Baseline score:   {baseline:.4f}")
    print(f"  Final score:      {best_score:.4f}")
    print(f"  Total improvement: {best_score - baseline:+.4f} ({((best_score - baseline) / baseline * 100) if baseline else 0:+.1f}%)")
    print(f"  Time elapsed:     {elapsed:.1f}s")
    print()
    
    # Save log
    if log_file:
        log_path = Path(log_file)
    else:
        log_path = Path(workdir) / "autoresearch_log.json"
    
    with open(log_path, "w") as f:
        json.dump(
            {
                "baseline": baseline,
                "final": best_score,
                "improvement_pct": ((best_score - baseline) / baseline * 100) if baseline else 0,
                "experiments": log,
                "duration_seconds": elapsed,
            },
            f,
            indent=2,
        )
    
    print(f"Log saved to: {log_path}")


def main():
    parser = argparse.ArgumentParser(description="Autoresearch experiment loop")
    parser.add_argument("--mutable", required=True, help="Path to the mutable file")
    parser.add_argument("--eval", required=True, help="Eval command (must print 'SCORE: <float>')")
    parser.add_argument("--experiments", type=int, default=20, help="Number of experiments")
    parser.add_argument("--workdir", default=".", help="Working directory (for git)")
    parser.add_argument("--log", default=None, help="Log file path")
    
    args = parser.parse_args()
    
    run_loop(
        mutable_file=args.mutable,
        eval_cmd=args.eval,
        num_experiments=args.experiments,
        workdir=args.workdir,
        log_file=args.log,
    )


if __name__ == "__main__":
    main()
