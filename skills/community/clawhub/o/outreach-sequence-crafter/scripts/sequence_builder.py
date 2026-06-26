#!/usr/bin/env python3
import argparse, json

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preset", default="creator_invite")
    ap.add_argument("--out", default="outreach_sequence.json")
    args = ap.parse_args()
    seq = {
        "preset": args.preset,
        "touches": [
            {"day":0,"name":"first_touch","goal":"open conversation"},
            {"day":3,"name":"follow_up","goal":"bump politely"},
            {"day":7,"name":"proof_followup","goal":"send evidence"},
            {"day":10,"name":"breakup","goal":"close loop"}
        ]
    }
    json.dump(seq, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
