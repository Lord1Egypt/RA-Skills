#!/usr/bin/env python3
import argparse, json, csv

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tasks_json", help="JSON list with title/owner/due/priority/status")
    ap.add_argument("--out", default="kanban.csv")
    args = ap.parse_args()
    tasks = json.load(open(args.tasks_json, "r", encoding="utf-8"))
    fields = ["title","owner","due","priority","status","notes"]
    with open(args.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for t in tasks:
            w.writerow({k: t.get(k, "") for k in fields})
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
