#!/usr/bin/env python3
"""
Update experience weights based on contrastive evaluation results.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from experience_manager import update_weights


def main():
    parser = argparse.ArgumentParser(description="Update experience weights after verification")
    parser.add_argument("--task", "-t", required=True, help="Task description")
    parser.add_argument("--result-a", "-a", required=True, help="Result without memory (baseline)")
    parser.add_argument("--result-b", "-b", required=True, help="Result with guideline")
    parser.add_argument("--correct", "-c", required=True, help="Correct answer/outcome")
    parser.add_argument("--experience-ids", "-e", required=True, help="Comma-separated experience IDs used")

    args = parser.parse_args()

    experience_ids = [id.strip() for id in args.experience_ids.split(",") if id.strip()]

    if not experience_ids:
        print("No experience IDs provided. Nothing to update.")
        return

    # Simple evaluation: check if results match correct answer
    # In practice, you might want more sophisticated comparison
    result_a_correct = args.correct.lower() in args.result_a.lower() or args.result_a.lower() in args.correct.lower()
    result_b_correct = args.correct.lower() in args.result_b.lower() or args.result_b.lower() in args.correct.lower()

    print(f"Task: {args.task[:60]}...")
    print(f"\nBaseline (without memory): {'CORRECT' if result_a_correct else 'INCORRECT'}")
    print(f"With guideline: {'CORRECT' if result_b_correct else 'INCORRECT'}")

    # Determine if guideline helped
    if result_b_correct and not result_a_correct:
        helped = True
        print("\n=> Guideline HELPED (turned incorrect into correct)")
    elif result_b_correct and result_a_correct:
        helped = True
        print("\n=> Both correct, guideline maintained quality")
    elif not result_b_correct and result_a_correct:
        helped = False
        print("\n=> Guideline HURT (turned correct into incorrect)")
    else:
        # Both incorrect - neutral, but lean toward decreased weight
        helped = False
        print("\n=> Both incorrect, slight weight decrease")

    # Update weights
    result = update_weights(experience_ids, helped)

    print(f"\nWeight updates:")
    for update in result["updates"]:
        print(f"  - {update['id']}: {update['old_weight']:.2f} -> {update['new_weight']:.2f} ({update['change']})")

    if result["total_updated"] == 0:
        print("  No experiences found with the provided IDs")


if __name__ == "__main__":
    main()
