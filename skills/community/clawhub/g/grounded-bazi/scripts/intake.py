#!/usr/bin/env python3
import argparse
import json


def main():
    p = argparse.ArgumentParser(description="Normalize BaZi reading intake details.")
    p.add_argument("--dob", required=True, help="Date of birth")
    p.add_argument("--time", default="unknown", help="Time of birth")
    p.add_argument("--place", required=True, help="Place of birth")
    p.add_argument("--focus", required=True, help="Reading focus")
    args = p.parse_args()

    result = {
        "dob": args.dob,
        "time": args.time,
        "place": args.place,
        "focus": args.focus,
        "precision": "lighter" if args.time.lower() in {"unknown", "", "n/a", "na"} else "standard",
        "disclaimer": (
            "Birth time missing; give a lighter, less precise reading."
            if args.time.lower() in {"unknown", "", "n/a", "na"}
            else "Give a high-level reflective BaZi-style reading unless a chart calculator is used."
        ),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
