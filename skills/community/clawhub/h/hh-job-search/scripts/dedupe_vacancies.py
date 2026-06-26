#!/usr/bin/env python3
import json
import sys
from collections import defaultdict

from rapidfuzz import fuzz

from job_models import Vacancy, dump_json, vacancy_key


def load_jsonl(path: str):
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield Vacancy.model_validate(json.loads(line))


def similar(a: Vacancy, b: Vacancy) -> bool:
    if a.source_url and b.source_url and a.source_url == b.source_url:
        return True
    if vacancy_key(a) == vacancy_key(b) and vacancy_key(a) != "::":
        return True
    title_score = fuzz.token_set_ratio(a.title or "", b.title or "")
    company_score = fuzz.token_set_ratio(a.company or "", b.company or "")
    return title_score >= 92 and company_score >= 85


def main():
    if len(sys.argv) != 2:
        print("Usage: dedupe_vacancies.py <vacancies.jsonl>", file=sys.stderr)
        sys.exit(2)

    groups = []
    for vacancy in load_jsonl(sys.argv[1]):
        placed = False
        for group in groups:
            if similar(vacancy, group[0]):
                group.append(vacancy)
                placed = True
                break
        if not placed:
            groups.append([vacancy])

    result = []
    for group in groups:
        canonical = max(group, key=lambda v: len((v.summary or "")) + len((v.raw_text or "")))
        duplicates = [v.model_dump() for v in group if v is not canonical]
        result.append({
            "canonical": canonical.model_dump(),
            "duplicates": duplicates,
            "count": len(group),
        })

    print(dump_json(result))


if __name__ == "__main__":
    main()
