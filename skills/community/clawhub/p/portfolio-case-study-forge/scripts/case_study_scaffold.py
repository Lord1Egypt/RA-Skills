#!/usr/bin/env python3
import argparse, json

TEMPLATE = {
    "project_snapshot": {"client":"", "timeline":"", "role":"", "outcome":""},
    "problem": "",
    "constraints": "",
    "process": [],
    "decisions": [],
    "results": [],
    "lessons": []
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="case_study_scaffold.json")
    args = ap.parse_args()
    json.dump(TEMPLATE, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
