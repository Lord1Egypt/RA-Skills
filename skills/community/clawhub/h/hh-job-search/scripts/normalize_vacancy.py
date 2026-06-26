#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from job_models import Vacancy, dump_json, extract_stack, normalize_remote_mode, normalize_salary_text, normalize_seniority


def main():
    if len(sys.argv) != 3:
        print("Usage: normalize_vacancy.py <source> <input-file>", file=sys.stderr)
        sys.exit(2)

    source, path = sys.argv[1], sys.argv[2]
    text = Path(path).read_text(encoding="utf-8")

    try:
        raw = json.loads(text)
    except json.JSONDecodeError:
        raw = {"title": None, "company": None, "description": text, "url": None, "salary": None}

    title = raw.get("title") or raw.get("name") or raw.get("vacancy")
    company = raw.get("company") or raw.get("employer") or raw.get("organization")
    description = raw.get("description") or raw.get("summary") or text
    salary_text = raw.get("salary") or raw.get("compensation") or ""

    vacancy = Vacancy(
        source=source,
        source_url=raw.get("url") or raw.get("link"),
        title=title,
        company=company,
        stack=extract_stack(" ".join([str(title or ""), str(description or "") ])),
        seniority=normalize_seniority(" ".join([str(title or ""), str(description or "") ])),
        remote_mode=normalize_remote_mode(" ".join([str(raw.get('remote_mode') or ''), str(description or '')])),
        summary=str(description)[:800],
        raw_text=str(description)[:4000],
        **normalize_salary_text(str(salary_text)),
    )
    print(dump_json(vacancy.model_dump()))


if __name__ == "__main__":
    main()
