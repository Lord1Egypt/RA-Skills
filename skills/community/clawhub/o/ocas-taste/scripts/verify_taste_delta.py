#!/usr/bin/python3
"""verify_taste_delta.py — integrity check after a Styx->Taste delta write.

Run from the data directory:
  cd <hermes-home>/commons/data/ocas-taste && /usr/bin/python3 \
    <hermes-home>/profiles/<profile>/skills/ocas-taste/scripts/verify_taste_delta.py

Asserts (exits non-zero on any violation):
  - zero duplicate item_id across items.jsonl
  - zero place_id collisions across items.jsonl (same place_id on >1 item)
  - zero signals.jsonl rows whose item_id does not resolve to a real item
  - zero (merchant_name, date) duplicates among source=styx signals
If --expect-place-ids is given (comma-separated place_ids), also asserts exactly one
item per given place_id.

A successful ingestion SCRIPT return ("N created") is NOT proof of integrity. This
script is the proof. Status is testimony, not action.
"""
import sys
if __name__ == "__main__" and ("--help" in sys.argv or "-h" in sys.argv):
    print('Verify Styx delta write integrity: place_id collisions, item dupes, orphaned signals.')
    print("Usage: verify_taste_delta.py [options]")
    print("Run with no arguments for default behavior; see SKILL.md for flags.")
    print("  -h, --help  Show this help message")
    sys.exit(0)
import json
import sys
import collections
import argparse

DATA = "<hermes-home>/commons/data/ocas-taste"
ITEMS = f"{DATA}/items.jsonl"
SIGNALS = f"{DATA}/signals.jsonl"


def load(p):
    out = []
    with open(p) as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--expect-place-ids", default="",
                    help="comma-separated canonical place_ids; asserts exactly 1 item each")
    ap.add_argument("--data-dir", default=DATA)
    args = ap.parse_args()
    items = load(f"{args.data_dir}/items.jsonl")
    sigs = load(f"{args.data_dir}/signals.jsonl")

    errors = []

    # 1) item_id uniqueness
    idc = collections.Counter(it.get("item_id") for it in items)
    id_dupes = [k for k, c in idc.items() if c > 1]
    if id_dupes:
        errors.append(f"item_id duplicates: {id_dupes}")

    # 2) place_id collisions
    pidc = collections.defaultdict(list)
    for it in items:
        if it.get("place_id"):
            pidc[it["place_id"]].append(it.get("item_id"))
    coll = {p: ids for p, ids in pidc.items() if len(ids) > 1}
    if coll:
        errors.append(f"place_id collisions: {coll}")

    # 3) orphaned signals
    ids = {it.get("item_id") for it in items}
    orphans = []
    for s in sigs:
        iid = s.get("item_id")
        if iid and iid not in ids:
            orphans.append((s.get("merchant_name"), iid, s.get("date")))
    if orphans:
        errors.append(f"orphaned signals (item_id not found): {orphans[:5]}"
                     + (f" (+{len(orphans)-5} more)" if len(orphans) > 5 else ""))

    # 4) (merchant_name, date) dupes among source=styx
    k = collections.Counter((s.get("merchant_name"), s.get("date"))
                            for s in sigs if s.get("source") == "styx")
    sdup = [x for x, c in k.items() if c > 1]
    if sdup:
        errors.append(f"duplicate (merchant,date) styx signals: {sdup}")

    # 5) optional: exactly-one-item per expected place_id
    if args.expect_place_ids:
        for pid in [p for p in args.expect_place_ids.split(",") if p]:
            recs = [it for it in items if it.get("place_id") == pid]
            if len(recs) != 1:
                errors.append(f"expected 1 item for place {pid}, found {len(recs)}")

    print(f"items={len(items)} signals={len(sigs)}")
    if errors:
        print("VERIFY FAILED:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("VERIFY PASSED")


if __name__ == "__main__":
    main()