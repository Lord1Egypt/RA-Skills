#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from job_models import Vacancy


FIELDS = ["source", "company", "title", "source_url", "fit_label", "fit_score", "salary_min", "salary_max", "salary_currency", "remote_mode", "seniority"]


def load_jsonl(path: str):
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield Vacancy.model_validate(json.loads(line))


def main():
    if len(sys.argv) not in (3, 4):
        print("Usage: export_shortlist.py <vacancies.jsonl> <out.csv> [min_score]", file=sys.stderr)
        sys.exit(2)

    min_score = int(sys.argv[3]) if len(sys.argv) == 4 else 60
    rows = [v for v in load_jsonl(sys.argv[1]) if (v.fit_score or 0) >= min_score or v.fit_label == "strong-match"]

    out = Path(sys.argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for v in rows:
            writer.writerow({k: getattr(v, k) for k in FIELDS})

    print(f"Exported {len(rows)} shortlisted vacancies -> {out}")


if __name__ == "__main__":
    main()
