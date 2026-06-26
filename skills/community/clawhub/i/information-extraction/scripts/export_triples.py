#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path


def load_triples(path):
    data = json.loads(Path(path).read_text())
    return data.get("triples", [])


def export_json(triples, output):
    Path(output).write_text(json.dumps(triples, ensure_ascii=False, indent=2))


def export_jsonl(triples, output):
    with open(output, "w", encoding="utf-8") as f:
        for row in triples:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def export_tsv(triples, output):
    with open(output, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["subject", "predicate", "object", "evidence", "confidence"], delimiter="\t")
        writer.writeheader()
        for row in triples:
            writer.writerow({k: row.get(k) for k in writer.fieldnames})


def main():
    parser = argparse.ArgumentParser(description="Export triples in JSON, JSONL, or TSV")
    parser.add_argument("--input", required=True)
    parser.add_argument("--format", required=True, choices=["json", "jsonl", "tsv"])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    triples = load_triples(args.input)
    if args.format == "json":
        export_json(triples, args.output)
    elif args.format == "jsonl":
        export_jsonl(triples, args.output)
    else:
        export_tsv(triples, args.output)
    print(args.output)


if __name__ == "__main__":
    main()
