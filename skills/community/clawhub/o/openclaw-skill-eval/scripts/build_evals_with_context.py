#!/usr/bin/env python3
"""
Build evals with conversation_history by merging extracted histories.

Phase 3.3a: integrate real session histories into evals.json

Usage flow:
1. Run evaluations with run_orchestrator.py, record session keys
2. Extract history from sessions using extract_session_history.py
3. Merge histories into evals.json using this script

Usage:
    # Step 1: run evaluations, record session keys per eval
    python scripts/run_orchestrator.py \
        --evals evals/example-quality.json \
        --output-dir workspace/iter-1
    
    # Step 2: create histories dir, extract and group histories
    mkdir -p evals/histories
    python scripts/extract_session_history.py \
        --session-key "agent:...:subagent:uuid1" \
        --eval-id 1 \
        --output-file evals/histories/eval-1-fresh.json
    
    python scripts/extract_session_history.py \
        --session-key "agent:...:subagent:uuid2" \
        --eval-id 2 \
        --output-file evals/histories/eval-2-with-context.json
    
    # Step 3: merge histories into evals.json
    python scripts/build_evals_with_context.py \
        --base-evals evals/example-quality.json \
        --histories evals/histories \
        --output evals/with-context.json
"""

import argparse
import json
from pathlib import Path
from typing import Optional


def load_base_evals(evals_file: str) -> dict:
    """Load base evals.json"""
    with open(evals_file, encoding="utf-8") as f:
        return json.load(f)


def load_histories(histories_dir: str) -> dict:
    """
    Load all extracted histories from a directory.
    
    Expected format: eval-{id}-*.json
    Returns: {eval_id: conversation_history}
    """
    histories = {}
    histories_path = Path(histories_dir)
    
    if not histories_path.exists():
        print(f"⚠️  Histories directory not found: {histories_dir}")
        return histories
    
    for history_file in histories_path.glob("eval-*.json"):
        try:
            with open(history_file, encoding="utf-8") as f:
                data = json.load(f)
            
            eval_id = data.get("eval_id")
            conversation = data.get("conversation_history")
            
            if eval_id and conversation:
                histories[eval_id] = conversation
                print(f"✅ Loaded history for eval-{eval_id} ({len(conversation)} messages)")
        except Exception as e:
            print(f"⚠️  Failed to load {history_file}: {e}")
    
    return histories


def build_evals_with_context(
    base_evals: dict,
    histories: dict,
    strategy: str = "parallel"
) -> dict:
    """
    Build new evals with conversation histories.
    
    Strategies:
    - "parallel": create two versions per eval (fresh + with-context)
    - "merged": only create with-context version for evals that have history
    """
    
    result = {
        "skill_name": base_evals.get("skill_name"),
        "evals": []
    }
    
    for eval_item in base_evals.get("evals", []):
        eval_id = eval_item.get("id")
        
        # 1. Keep original eval (fresh)
        eval_fresh = eval_item.copy()
        eval_fresh["conversation_history"] = None
        eval_fresh["variant"] = "fresh"
        result["evals"].append(eval_fresh)
        
        # 2. If history exists, create with-context variant
        if eval_id in histories:
            eval_with_context = eval_item.copy()
            eval_with_context["id"] = eval_id * 10 + 1  # ID convention: original * 10 + 1
            eval_with_context["name"] = eval_item.get("name", "") + "-with-context"
            eval_with_context["conversation_history"] = histories[eval_id]
            eval_with_context["variant"] = "with-context"
            result["evals"].append(eval_with_context)
            
            print(f"✅ Created with-context variant for eval-{eval_id}")
        else:
            print(f"⚠️  No history found for eval-{eval_id} (skipping with-context variant)")
    
    return result


def validate_evals(evals: dict) -> bool:
    """Basic validation"""
    if not evals.get("evals"):
        print("❌ No evals found")
        return False
    
    for eval_item in evals["evals"]:
        if not eval_item.get("id"):
            print(f"❌ Eval missing id: {eval_item.get('name')}")
            return False
        
        if not eval_item.get("prompt"):
            print(f"❌ Eval {eval_item['id']} missing prompt")
            return False
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Build evals.json with conversation_history from extracted sessions"
    )
    parser.add_argument(
        "--base-evals",
        required=True,
        help="Base evals.json file"
    )
    parser.add_argument(
        "--histories",
        default="evals/histories",
        help="Directory containing extracted histories (eval-*.json)"
    )
    parser.add_argument(
        "--output",
        default="evals/with-context.json",
        help="Output evals.json file"
    )
    parser.add_argument(
        "--strategy",
        choices=["parallel", "merged"],
        default="parallel",
        help="How to combine evals and histories"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print summary after building"
    )
    
    args = parser.parse_args()
    
    print("Step 1: Loading base evals...")
    base_evals = load_base_evals(args.base_evals)
    print(f"  Loaded {len(base_evals.get('evals', []))} base evals")
    
    print("\nStep 2: Loading extracted histories...")
    histories = load_histories(args.histories)
    print(f"  Loaded {len(histories)} histories")
    
    print("\nStep 3: Building combined evals...")
    combined_evals = build_evals_with_context(base_evals, histories, args.strategy)
    
    print("\nStep 4: Validating...")
    if not validate_evals(combined_evals):
        print("❌ Validation failed")
        return 1
    
    print(f"  ✅ {len(combined_evals['evals'])} evals are valid")
    
    print("\nStep 5: Saving...")
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(combined_evals, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved to {output_path}")
    
    if args.summary:
        print("\n=== Summary ===")
        fresh_count = sum(1 for e in combined_evals["evals"] if e.get("variant") == "fresh")
        context_count = sum(1 for e in combined_evals["evals"] if e.get("variant") == "with-context")
        print(f"Total evals: {len(combined_evals['evals'])}")
        print(f"  Fresh (no history): {fresh_count}")
        print(f"  With context: {context_count}")
        
        print("\n📋 Next steps:")
        print(f"1. Review evals in {output_path}")
        print(f"2. Run evaluation:")
        print(f"   python scripts/run_orchestrator.py \\")
        print(f"     --evals {output_path} \\")
        print(f"     --mode both \\")
        print(f"     --output-dir workspace/iter-context")
        print(f"3. Compare fresh vs with-context results")
    
    return 0


if __name__ == "__main__":
    exit(main())
