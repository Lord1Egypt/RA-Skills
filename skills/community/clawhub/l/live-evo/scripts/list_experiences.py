#!/usr/bin/env python3
"""
List all experiences in the database.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from experience_manager import load_experiences


def main():
    parser = argparse.ArgumentParser(description="List all experiences")
    parser.add_argument("--category", "-c", help="Filter by category")
    parser.add_argument("--sort", "-s", default="weight",
                       choices=["weight", "created", "uses"],
                       help="Sort by field")
    parser.add_argument("--limit", "-l", type=int, default=20, help="Limit results")
    parser.add_argument("--full", "-f", action="store_true", help="Show full details")

    args = parser.parse_args()

    experiences = load_experiences()

    if not experiences:
        print("No experiences in database yet.")
        return

    if args.category:
        experiences = [e for e in experiences if e.get("category") == args.category]

    # Sort
    if args.sort == "weight":
        experiences.sort(key=lambda x: x.get("weight", 1.0), reverse=True)
    elif args.sort == "created":
        experiences.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    elif args.sort == "uses":
        experiences.sort(key=lambda x: x.get("use_count", 0), reverse=True)

    experiences = experiences[:args.limit]

    print(f"Showing {len(experiences)} experiences (sorted by {args.sort}):\n")

    for i, exp in enumerate(experiences, 1):
        weight = exp.get("weight", 1.0)
        weight_indicator = "+" if weight >= 1.5 else "-" if weight <= 0.5 else "="

        print(f"{i}. [{weight_indicator}] ID: {exp.get('id', 'N/A')} | Weight: {weight:.2f} | Uses: {exp.get('use_count', 0)}")
        print(f"   Category: {exp.get('category', 'N/A')}")
        print(f"   Question: {exp.get('question', '')[:70]}...")

        if args.full:
            print(f"   Failure: {exp.get('failure_reason', '')[:70]}...")
            print(f"   Lesson: {exp.get('improvement', '')[:70]}...")
            if exp.get('missed_information'):
                print(f"   Missed: {exp.get('missed_information', '')[:70]}...")
            print(f"   Created: {exp.get('created_at', 'N/A')}")

        print()

    # Summary
    total = len(load_experiences())
    shown = len(experiences)
    print(f"Showing {shown} of {total} total experiences")
    if args.category:
        print(f"(Filtered by category: {args.category})")


if __name__ == "__main__":
    main()
