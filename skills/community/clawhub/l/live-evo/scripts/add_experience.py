#!/usr/bin/env python3
"""
Add a new experience to the database.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from experience_manager import add_experience


def main():
    parser = argparse.ArgumentParser(description="Add a new experience to the database")
    parser.add_argument("--question", "-q", required=True, help="The original task/question")
    parser.add_argument("--failure-reason", "-f", required=True, help="What went wrong")
    parser.add_argument("--improvement", "-i", required=True, help="Key lesson learned")
    parser.add_argument("--missed-info", "-m", default="", help="Information that was missed")
    parser.add_argument("--category", "-c", default="other",
                       choices=["coding", "analysis", "prediction", "debugging", "design", "other"],
                       help="Category of the experience")

    args = parser.parse_args()

    exp = add_experience(
        question=args.question,
        failure_reason=args.failure_reason,
        improvement=args.improvement,
        missed_information=args.missed_info,
        category=args.category
    )

    print(f"Experience added successfully!")
    print(f"  ID: {exp['id']}")
    print(f"  Question: {exp['question'][:60]}...")
    print(f"  Category: {exp['category']}")
    print(f"  Initial weight: {exp['weight']}")
    print(f"\nThis experience will be retrieved when similar tasks are encountered.")


if __name__ == "__main__":
    main()
