#!/usr/bin/env python3
"""Sum integers from a JSON reference file and print `sum=<value>`."""
import json
import sys


def main(argv):
    path = argv[1] if len(argv) > 1 else "references/sample_numbers.json"
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    values = payload.get("numbers") or []
    total = sum(int(v) for v in values)
    print(f"sum={total}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
