#!/usr/bin/env python3
import argparse, csv, json

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cases_json", help="JSON list of test cases")
    ap.add_argument("--out", default="prompt_experiment.csv")
    args = ap.parse_args()
    cases = json.load(open(args.cases_json, "r", encoding="utf-8"))
    fields = ["case_id","criterion","prompt_a_score","prompt_b_score","notes"]
    with open(args.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for idx, case in enumerate(cases, 1):
            for criterion in case.get("criteria", ["accuracy"]):
                w.writerow({"case_id": idx, "criterion": criterion, "prompt_a_score": "", "prompt_b_score": "", "notes": case.get("notes","")})
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
