#!/usr/bin/env python3
"""Orchestrator: end-to-end parallel eval execution.

Spawn subagents for all evals, wait for completion, then analyze.

Usage:
    python run_orchestrator.py \
        --evals evals/example-quality.json \
        --mode compare \
        --output-dir workspace/iteration-2 \
        --workers 6

Modes:
    - compare: A vs B quality comparison (with/without skill)
    - trigger: Description trigger rate detection
    - both: Run both sequentially

Roughly 5-10x faster than sequential execution due to parallel subagent spawning.
"""

import argparse
import json
import time
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from oc_tools import invoke


def spawn_eval(eval_item: dict, skill_path: str, compare_mode: str = "with") -> dict:
    """Spawn subagent for a single eval.
    
    Args:
        eval_item: {"id", "name", "prompt", "context", ...}
        skill_path: path to SKILL.md
        compare_mode: "with" or "without" (ignored for trigger mode)
    
    Returns:
        {"eval_id", "eval_name", "session_key", "compare_mode"}
    """
    eval_id = eval_item["id"]
    eval_name = eval_item["name"]
    prompt = eval_item["prompt"]
    context = eval_item.get("context", "")

    # Build task (with context prefix if provided)
    if context:
        task = f"[Context: {context}]\n\n{prompt}"
    else:
        task = prompt

    # Add skill hint if compare_mode="with"
    if compare_mode == "with":
        task = f"Please read {skill_path} first.\n\n{task}"

    try:
        result = invoke("sessions_spawn", {
            "task": task,
            "sandbox": "inherit",
            "cleanup": "keep",
            "mode": "run"
        })
        
        # Extract session_key from result
        session_key = result.get("sessionKey") or result.get("session_key") or result.get("id")
        return {
            "eval_id": eval_id,
            "eval_name": eval_name,
            "session_key": session_key,
            "compare_mode": compare_mode,
            "error": None
        }
    except Exception as e:
        return {
            "eval_id": eval_id,
            "eval_name": eval_name,
            "session_key": None,
            "compare_mode": compare_mode,
            "error": str(e)
        }


def run_compare(evals_file: str, skill_path: str, output_dir: str, workers: int = 6) -> bool:
    """Run quality comparison: spawn with_skill + without_skill for each eval."""
    with open(evals_file) as f:
        evals_data = json.load(f)
    
    evals = evals_data.get("evals", [])
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"\n=== COMPARE MODE ===")
    print(f"Spawning {len(evals) * 2} subagents (with + without skill)...\n")
    start = time.time()

    results_raw = []
    errors = []

    # Spawn all subagents in parallel
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Create futures for both with_skill and without_skill
        futures = {}
        for eval_item in evals:
            # with_skill variant
            f_with = executor.submit(spawn_eval, eval_item, skill_path, "with")
            futures[f_with] = ("with", eval_item)
            
            # without_skill variant
            f_without = executor.submit(spawn_eval, eval_item, skill_path, "without")
            futures[f_without] = ("without", eval_item)

        results_by_eval = {}
        for future in as_completed(futures):
            mode, eval_item = futures[future]
            result = future.result()
            eval_id = eval_item["id"]
            
            if result["error"]:
                print(f"  ❌ eval-{eval_id} ({mode}): {result['error']}")
                errors.append((eval_id, result["error"]))
            else:
                print(f"  ✓ eval-{eval_id} ({mode}) spawned → {result['session_key'][:20]}...")
                
                if eval_id not in results_by_eval:
                    results_by_eval[eval_id] = {}
                results_by_eval[eval_id][mode] = result

        # Construct results_raw from paired results
        for eval_id, variants in sorted(results_by_eval.items()):
            eval_item = next(e for e in evals if e["id"] == eval_id)
            if "with" in variants and "without" in variants:
                results_raw.append({
                    "eval_id": eval_id,
                    "eval_name": eval_item["name"],
                    "with_skill_session": variants["with"]["session_key"],
                    "without_skill_session": variants["without"]["session_key"]
                })

    elapsed = time.time() - start
    print(f"\nSpawned {len(results_raw)} eval pairs in {elapsed:.1f}s")

    # Save raw results
    raw_path = output_path / "compare_results_raw.json"
    with open(raw_path, "w") as f:
        json.dump(results_raw, f, indent=2)
    print(f"Saved: {raw_path}")

    # Run transcription + metadata extraction
    if results_raw:
        print(f"\nExtracting transcripts...")
        cmd = [
            "python", "run_compare.py",
            "--evals", evals_file,
            "--results", str(raw_path),
            "--output-dir", output_dir,
            "--workers", str(workers)
        ]
        result = subprocess.run(cmd, cwd=Path(__file__).parent)
        if result.returncode != 0:
            print(f"Error running run_compare.py")
            return False

    if errors:
        print(f"\n⚠️ {len(errors)} spawn errors (may be retried)")
        return len(results_raw) > 0
    return True


def run_trigger(evals_file: str, skill_path: str, output_dir: str, workers: int = 6) -> bool:
    """Run trigger detection: spawn evals without skill hint, check if SKILL.md is read."""
    with open(evals_file) as f:
        evals_data = json.load(f)
    
    evals = evals_data.get("evals", [])
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"\n=== TRIGGER MODE ===")
    print(f"Spawning {len(evals)} subagents (trigger detection)...\n")
    start = time.time()

    results_raw = []
    errors = []

    # Spawn all subagents in parallel
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(spawn_eval, eval_item, skill_path, "without"): eval_item
            for eval_item in evals
        }

        for future in as_completed(futures):
            eval_item = futures[future]
            result = future.result()
            eval_id = eval_item["id"]
            
            if result["error"]:
                print(f"  ❌ eval-{eval_id}: {result['error']}")
                errors.append((eval_id, result["error"]))
            else:
                print(f"  ✓ eval-{eval_id} spawned → {result['session_key'][:20]}...")
                results_raw.append({
                    "id": f"tq-{eval_id}",
                    "query": eval_item["prompt"],
                    "expected": True,  # We expect SKILL.md to be triggered
                    "session_key": result["session_key"]
                })

    elapsed = time.time() - start
    print(f"\nSpawned {len(results_raw)} trigger queries in {elapsed:.1f}s")

    # Save raw results
    raw_path = output_path / "trigger_results_raw.json"
    with open(raw_path, "w") as f:
        json.dump(results_raw, f, indent=2)
    print(f"Saved: {raw_path}")

    # Run analysis
    if results_raw:
        print(f"\nAnalyzing trigger detection...")
        cmd = [
            "python", "run_trigger.py",
            "--raw", str(raw_path),
            "--output", str(output_path / "trigger_rate_results.json"),
            "--workers", str(workers)
        ]
        result = subprocess.run(cmd, cwd=Path(__file__).parent)
        if result.returncode != 0:
            print(f"Error running run_trigger.py")
            return False

    if errors:
        print(f"\n⚠️ {len(errors)} spawn errors (may be retried)")
        return len(results_raw) > 0
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Orchestrator for parallel skill evaluation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run quality comparison (with vs without skill)
  python run_orchestrator.py \\
    --evals evals/example-quality.json \\
    --skill-path /path/to/SKILL.md \\
    --mode compare \\
    --output-dir workspace/iteration-1

  # Run trigger detection
  python run_orchestrator.py \\
    --evals evals/example-triggers.json \\
    --skill-path /path/to/SKILL.md \\
    --mode trigger \\
    --output-dir workspace/iteration-1

  # Run both modes
  python run_orchestrator.py \\
    --evals evals/example-quality.json \\
    --skill-path /path/to/SKILL.md \\
    --mode both \\
    --output-dir workspace/iteration-1 \\
    --workers 8
        """
    )
    parser.add_argument("--evals", required=True, help="Evals JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to SKILL.md for skill hint")
    parser.add_argument("--mode", choices=["compare", "trigger", "both"], default="both",
                        help="Evaluation mode (default: both)")
    parser.add_argument("--output-dir", default="workspace/iteration-1", help="Output directory")
    parser.add_argument("--workers", type=int, default=6,
                        help="Number of parallel workers (default: 6)")
    
    args = parser.parse_args()

    overall_start = time.time()
    success = True

    if args.mode in ("compare", "both"):
        if not run_compare(args.evals, args.skill_path, args.output_dir, args.workers):
            success = False

    if args.mode in ("trigger", "both"):
        if not run_trigger(args.evals, args.skill_path, args.output_dir, args.workers):
            success = False

    overall_elapsed = time.time() - overall_start
    print(f"\n{'='*40}")
    print(f"✅ All done in {overall_elapsed:.1f}s!" if success else "⚠️  Some modes failed")
    print(f"Output: {args.output_dir}")
    print(f"{'='*40}")

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
