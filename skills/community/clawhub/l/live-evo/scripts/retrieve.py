#!/usr/bin/env python3
"""
Retrieve relevant experiences and generate task-specific guideline.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from experience_manager import find_relevant_experiences, generate_guideline, load_experiences


def main():
    parser = argparse.ArgumentParser(description="Retrieve relevant experiences for a task")
    parser.add_argument("--query", "-q", required=True, help="Task description to search for")
    parser.add_argument("--top-k", "-k", type=int, default=5, help="Number of experiences to retrieve")
    parser.add_argument("--threshold", "-t", type=float, default=0.1, help="Minimum similarity threshold")
    parser.add_argument("--category", "-c", help="Filter by category")
    parser.add_argument("--raw", action="store_true", help="Show raw experiences without guideline")

    args = parser.parse_args()

    # Check if we have any experiences
    all_experiences = load_experiences()
    if not all_experiences:
        print("No experiences in database yet.")
        print("As you complete verifiable tasks and learn from mistakes,")
        print("use `add_experience.py` to store lessons learned.")
        return

    # Find relevant experiences
    results = find_relevant_experiences(
        query=args.query,
        top_k=args.top_k,
        threshold=args.threshold,
        category=args.category
    )

    if not results:
        print(f"No relevant experiences found for: {args.query[:60]}...")
        print(f"(Total experiences in database: {len(all_experiences)})")
        print("\nProceed without guideline, but consider adding an experience after this task if you learn something.")
        return

    print(f"Found {len(results)} relevant experiences:\n")

    experiences = []
    experience_ids = []

    for i, (exp, score) in enumerate(results, 1):
        experiences.append(exp)
        experience_ids.append(exp.get("id", ""))
        print(f"{i}. [Score: {score:.3f}] [Weight: {exp.get('weight', 1.0):.2f}] [ID: {exp.get('id', 'N/A')}]")
        print(f"   Question: {exp.get('question', '')[:80]}...")
        print(f"   Category: {exp.get('category', 'N/A')}")
        print()

    if args.raw:
        print("\n--- Raw Experiences ---")
        for exp in experiences:
            print(f"\n**Question:** {exp.get('question', '')}")
            print(f"**Failure Reason:** {exp.get('failure_reason', '')}")
            print(f"**Improvement:** {exp.get('improvement', '')}")
            print(f"**Missed Info:** {exp.get('missed_information', '')}")
            print("-" * 40)
    else:
        guideline = generate_guideline(args.query, experiences)
        print("\n" + "=" * 60)
        print(guideline)
        print("=" * 60)

    print(f"\nExperience IDs (for update): {','.join(experience_ids)}")


if __name__ == "__main__":
    main()
