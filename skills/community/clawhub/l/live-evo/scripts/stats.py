#!/usr/bin/env python3
"""
Show statistics about the experience database.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from experience_manager import get_statistics, load_experiences, WEIGHT_HISTORY_PATH


def main():
    stats = get_statistics()

    if stats.get("total", 0) == 0 and "total_experiences" not in stats:
        print("No experiences in database yet.")
        print("\nStart using Live-Evo by adding experiences from your learnings:")
        print("  python ~/.claude/skills/live-evo/scripts/add_experience.py \\")
        print("    --question 'Your task' \\")
        print("    --failure-reason 'What went wrong' \\")
        print("    --improvement 'What you learned'")
        return

    print("=" * 50)
    print("         Live-Evo Experience Statistics")
    print("=" * 50)

    print(f"\nTotal Experiences: {stats.get('total_experiences', 0)}")
    print(f"\nBy Category:")
    for cat, count in stats.get("categories", {}).items():
        print(f"  - {cat}: {count}")

    print(f"\nWeight Statistics:")
    print(f"  Average: {stats.get('average_weight', 0):.2f}")
    print(f"  Min: {stats.get('min_weight', 0):.2f}")
    print(f"  Max: {stats.get('max_weight', 0):.2f}")
    print(f"  High quality (>=1.5): {stats.get('high_quality_count', 0)}")
    print(f"  Low quality (<=0.5): {stats.get('low_quality_count', 0)}")

    # Weight history
    if WEIGHT_HISTORY_PATH.exists():
        with open(WEIGHT_HISTORY_PATH, 'r') as f:
            history = [json.loads(line) for line in f if line.strip()]

        if history:
            helped_count = len([h for h in history if h.get("helped", False)])
            hurt_count = len(history) - helped_count

            print(f"\nWeight Update History:")
            print(f"  Total updates: {len(history)}")
            print(f"  Helped (weight increased): {helped_count}")
            print(f"  Hurt (weight decreased): {hurt_count}")
            if history:
                print(f"  Success rate: {helped_count/len(history)*100:.1f}%")

    # Top experiences
    experiences = load_experiences()
    if experiences:
        experiences.sort(key=lambda x: x.get("weight", 1.0), reverse=True)

        print(f"\nTop 3 Most Useful Experiences:")
        for i, exp in enumerate(experiences[:3], 1):
            print(f"  {i}. [{exp.get('weight', 1.0):.2f}] {exp.get('question', '')[:50]}...")

        experiences.sort(key=lambda x: x.get("use_count", 0), reverse=True)
        print(f"\nMost Used Experiences:")
        for i, exp in enumerate(experiences[:3], 1):
            uses = exp.get("use_count", 0)
            successes = exp.get("success_count", 0)
            print(f"  {i}. [{uses} uses, {successes} successes] {exp.get('question', '')[:40]}...")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
