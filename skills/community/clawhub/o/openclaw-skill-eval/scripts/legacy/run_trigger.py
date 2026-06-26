#!/usr/bin/env python3
"""Test skill description trigger rate using sessions_history (ground truth).

Detection method: spawn a subagent with sandbox=inherit, then check
sessions_history(includeTools=True) for a tool_use read call on SKILL.md.
This is more accurate than inspecting CLI output — it observes real behavior.

Usage:
    # Step 1: Run trigger queries via orchestrator (produces trigger_results_raw.json)
    # Step 2: Run this script to analyze histories and compute metrics
    python run_trigger.py \
        --raw trigger_results_raw.json \
        --output trigger_rate_results.json

Input format (trigger_results_raw.json):
    [
      {
        "id": "tq-1",
        "query": "...",
        "expected": true,
        "session_key": "agent:...:subagent:uuid"
      }
    ]

Output format (trigger_rate_results.json):
    {
      "trigger_rate": 0.7,
      "recall": 0.9,
      "specificity": 1.0,
      "accuracy": 0.95,
      "total_queries": 10,
      "results": [...]
    }
"""

import argparse
import json
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from oc_tools import invoke


SKILL_KEYWORD = "SKILL.md"


def was_skill_triggered(history: dict, keyword: str = SKILL_KEYWORD) -> bool:
    """
    Check if skill was triggered by scanning sessions_history for a
    tool_use Read/read call whose path contains the keyword.

    This is ground truth — no inference, no LLM judgment.
    """
    messages = history.get("messages", [])
    for msg in messages:
        if msg.get("role") != "assistant":
            continue
        content = msg.get("content", [])
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") != "tool_use":
                continue
            if block.get("name") not in ("Read", "read"):
                continue
            inp = block.get("input", {})
            path = inp.get("path", "") or inp.get("file_path", "") or ""
            if keyword in path:
                return True
    return False


def analyze_query(item: dict, save_dir: Path) -> dict:
    """Analyze a single query: fetch history, check trigger, save files.
    
    Returns: result dict with id, query, expected, triggered, correct
    """
    query_id = item["id"]
    query = item["query"]
    expected = item["expected"]
    session_key = item["session_key"]

    try:
        history = invoke("sessions_history", {
            "sessionKey": session_key,
            "includeTools": True
        })

        # Save complete history (source of truth)
        if save_dir:
            save_dir.mkdir(parents=True, exist_ok=True)
            history_path = save_dir / f"{query_id}_full_history.json"
            with open(history_path, "w") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)

        triggered = was_skill_triggered(history)
        correct = (triggered == expected)

        return {
            "id": query_id,
            "query": query,
            "expected": expected,
            "triggered": triggered,
            "correct": correct,
            "session_key": session_key,
            "error": None
        }
    except Exception as e:
        return {
            "id": query_id,
            "query": query,
            "expected": expected,
            "triggered": False,
            "correct": False,
            "session_key": session_key,
            "error": str(e)
        }


def run(raw_file: str, output_file: str, workers: int = 4) -> None:
    with open(raw_file) as f:
        raw = json.load(f)

    # Save full history to histories/ directory alongside output_file
    save_dir = Path(output_file).parent / "histories"

    print(f"Analyzing {len(raw)} queries with {workers} workers...")
    start = time.time()

    results = []
    triggered_count = 0
    correct_count = 0
    errors = 0

    # Parallel execution
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(analyze_query, item, save_dir): item["id"]
            for item in raw
        }
        for future in as_completed(futures):
            result = future.result()
            query_id = result["id"]
            
            if result["error"]:
                print(f"  ❌ {query_id}: error={result['error']}")
                errors += 1
            else:
                status = "✅" if result["correct"] else "❌"
                print(f"  {status} {query_id}: triggered={result['triggered']}, expected={result['expected']}")
                if result["triggered"]:
                    triggered_count += 1
                if result["correct"]:
                    correct_count += 1
            
            results.append(result)

    elapsed = time.time() - start
    total = len(results)
    trigger_rate = triggered_count / total if total > 0 else 0
    accuracy = correct_count / total if total > 0 else 0

    positive = [r for r in results if r["expected"]]
    negative = [r for r in results if not r["expected"]]
    recall = sum(1 for r in positive if r["triggered"]) / len(positive) if positive else 0
    specificity = sum(1 for r in negative if not r["triggered"]) / len(negative) if negative else 0

    summary = {
        "total_queries": total,
        "triggered_count": triggered_count,
        "error_count": errors,
        "elapsed_seconds": round(elapsed, 1),
        "trigger_rate": round(trigger_rate, 3),
        "accuracy": round(accuracy, 3),
        "recall": round(recall, 3),
        "specificity": round(specificity, 3),
        "results": results
    }

    with open(output_file, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\n=== Trigger Rate Results ===")
    print(f"Total:       {total} queries in {elapsed:.1f}s")
    print(f"Recall:      {recall:.0%}  (skill triggered when it should be)")
    print(f"Specificity: {specificity:.0%}  (skill NOT triggered when it shouldn't be)")
    print(f"Accuracy:    {accuracy:.0%}")
    if errors:
        print(f"Errors:      {errors}")
    print(f"Saved: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze trigger rate from sessions_history")
    parser.add_argument("--raw", default="trigger_results_raw.json",
                        help="Input file with session keys (from orchestrator)")
    parser.add_argument("--output", default="trigger_rate_results.json",
                        help="Output file for results")
    parser.add_argument("--workers", type=int, default=4,
                        help="Number of parallel workers (default: 4)")
    args = parser.parse_args()
    run(args.raw, args.output, args.workers)
