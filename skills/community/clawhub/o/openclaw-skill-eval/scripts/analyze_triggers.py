#!/usr/bin/env python3
"""
Trigger Rate Analyzer (v2 — pure data processing, no OpenClaw API calls)

Takes pre-fetched session histories (JSON files) and computes trigger metrics.
Mo runs the spawning and history fetching; this script only analyzes data.

Usage:
    python3 scripts/analyze_triggers.py \
        --evals evals/weather/triggers.json \
        --histories workspace/weather/iter-1/raw/histories/ \
        --output workspace/weather/iter-1/trigger_results.json

History file format (one per eval):
    workspace/.../raw/histories/eval-{id}.json
    {
        "eval_id": 1,
        "query": "...",
        "expected": true,
        "messages": [...]   # from sessions_history(includeTools=True)
    }
"""

import argparse
import json
from pathlib import Path
from datetime import datetime


def check_skill_triggered(messages: list, skill_path: str) -> bool:
    """
    Check if skill was triggered by scanning tool_use blocks for skill reads.
    """
    skill_filename = Path(skill_path).name  # e.g. "SKILL.md"
    skill_dir = Path(skill_path).parent.name  # e.g. "weather"

    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, list):
            for block in content:
                if not isinstance(block, dict):
                    continue
                # tool_use: check if read/file_path contains skill path
                if block.get("type") == "toolCall":
                    tool_name = block.get("name", "")
                    args = block.get("arguments", {})
                    if tool_name in ("read", "Read"):
                        path_arg = args.get("file_path", "") or args.get("path", "")
                        # Check filename match, and directory match only if non-empty
                        if skill_filename in path_arg:
                            return True
                        if skill_dir and skill_dir in path_arg:
                            return True

    return False


def load_history_file(history_path: Path) -> dict:
    """Load a single history JSON file."""
    with open(history_path, encoding="utf-8") as f:
        return json.load(f)


def analyze_triggers(
    evals_file: str,
    histories_dir: str,
    output_file: str,
    skill_path: str = None,
    verbose: bool = False
) -> dict:
    """
    Main analysis function.

    Loads each eval + its history file, checks if skill was triggered,
    computes recall/specificity/accuracy.
    """
    # Load evals
    with open(evals_file, encoding="utf-8") as f:
        evals_data = json.load(f)

    skill_name = evals_data.get("skill_name", "unknown")
    skill_path = skill_path or evals_data.get("skill_path", "SKILL.md")
    evals = evals_data.get("evals", [])

    hist_dir = Path(histories_dir)

    results = []
    missing = []

    for eval_item in evals:
        eval_id = eval_item.get("id")
        query = eval_item.get("query", "")
        expected = eval_item.get("expected", True)
        category = eval_item.get("category", "unknown")

        # Find history file
        hist_file = hist_dir / f"eval-{eval_id}.json"
        if not hist_file.exists():
            print(f"  ⚠️  Missing history: eval-{eval_id} ({hist_file})")  # always show warnings
            missing.append(eval_id)
            continue

        history = load_history_file(hist_file)
        messages = history.get("messages", [])
        triggered = check_skill_triggered(messages, skill_path)
        correct = (triggered == expected)

        results.append({
            "id": eval_id,
            "query": query,
            "expected": expected,
            "triggered": triggered,
            "correct": correct,
            "category": category,
        })

        if verbose:
            status = "✅" if correct else "❌"
            print(f"  [{eval_id}] {status} expected={expected} triggered={triggered} | '{query[:50]}'")

    if not results:
        print("❌ No results — check histories directory")
        return {}

    # Compute metrics
    total = len(results)
    correct_count = sum(1 for r in results if r["correct"])
    positives = [r for r in results if r["expected"]]
    negatives = [r for r in results if not r["expected"]]
    true_positives = [r for r in positives if r["triggered"]]
    true_negatives = [r for r in negatives if not r["triggered"]]

    # Calculate all metrics
    false_positives = [r for r in negatives if r["triggered"]]
    false_negatives = [r for r in positives if not r["triggered"]]
    
    tp = len(true_positives)
    tn = len(true_negatives)
    fp = len(false_positives)
    fn = len(false_negatives)
    
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    accuracy = correct_count / total

    # Description diagnosis: analyze failures
    diagnosis = {
        "false_negatives": [],  # Should trigger but didn't
        "false_positives": [],  # Should NOT trigger but did
    }
    
    for r in false_negatives:
        diagnosis["false_negatives"].append({
            "eval_id": r["id"],
            "query": r["query"],
            "issue": "Should trigger but didn't. Description may lack keywords for this query pattern.",
        })
    
    for r in false_positives:
        diagnosis["false_positives"].append({
            "eval_id": r["id"],
            "query": r["query"],
            "issue": "Should NOT trigger but did. Description may be too broad or contain misleading keywords.",
        })

    output = {
        "skill_name": skill_name,
        "skill_path": skill_path,
        "timestamp": datetime.now().isoformat(),
        "metrics": {
            "accuracy": round(accuracy, 3),
            "recall": round(recall, 3),
            "specificity": round(specificity, 3),
            "precision": round(precision, 3),
            "f1": round(f1, 3),
        },
        "counts": {
            "total": total,
            "true_positives": tp,
            "true_negatives": tn,
            "false_positives": fp,
            "false_negatives": fn,
        },
        "triggered_count": sum(1 for r in results if r["triggered"]),
        "missing_histories": missing,
        "results": results,
        "description_diagnosis": diagnosis,
    }

    # Save
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print()
    print(f"=== Trigger Results ===")
    print(f"Accuracy:    {accuracy:.0%} ({correct_count}/{total})")
    print(f"Precision:   {precision:.0%} ({tp}/{tp + fp})" if (tp + fp) > 0 else "Precision:   N/A (no triggers)")
    print(f"Recall:      {recall:.0%} ({tp}/{tp + fn})" if (tp + fn) > 0 else "Recall:      N/A (no positives)")
    print(f"Specificity: {specificity:.0%} ({tn}/{tn + fp})" if (tn + fp) > 0 else "Specificity: N/A (no negatives)")
    print(f"F1 Score:    {f1:.2f}")
    if missing:
        print(f"⚠️  Missing histories: {missing}")

    # Print description diagnosis
    fn_list = diagnosis["false_negatives"]
    fp_list = diagnosis["false_positives"]
    
    if fn_list:
        print()
        print(f"=== False Negatives ({len(fn_list)}) ===")
        print("Should trigger but didn't → description lacks coverage:")
        for d in fn_list:
            print(f"  [{d['eval_id']}] \"{d['query']}\"")
    
    if fp_list:
        print()
        print(f"=== False Positives ({len(fp_list)}) ===")
        print("Should NOT trigger but did → description too broad:")
        for d in fp_list:
            print(f"  [{d['eval_id']}] \"{d['query']}\"")

    print()
    print(f"✅ Saved to {output_file}")

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Analyze trigger rate from pre-fetched session histories"
    )
    parser.add_argument("--evals", required=True, help="Path to evals JSON")
    parser.add_argument("--histories", required=True, help="Directory with eval-{id}.json history files")
    parser.add_argument("--output", required=True, help="Output trigger_results.json path")
    parser.add_argument("--skill-path", help="Override skill path for trigger detection")

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output per eval (default: summary only)"
    )
    args = parser.parse_args()

    analyze_triggers(
        evals_file=args.evals,
        histories_dir=args.histories,
        output_file=args.output,
        skill_path=args.skill_path,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
