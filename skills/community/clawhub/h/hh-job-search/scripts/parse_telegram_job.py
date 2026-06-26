#!/usr/bin/env python3
import re
import sys
from pathlib import Path

from job_models import Vacancy, dump_json, extract_stack, normalize_remote_mode, normalize_salary_text, normalize_seniority

TITLE_RE = re.compile(r"^(?:вакансия|ищем|position|role)?\s*[:\-— ]*([^\n]{5,120})", re.I)
COMPANY_RE = re.compile(r"(?:компания|company)\s*[:\-—]\s*([^\n]+)", re.I)
CONTACT_RE = re.compile(r"(@[A-Za-z0-9_]{4,}|https?://t\.me/[^\s]+)")
URL_RE = re.compile(r"https?://[^\s]+")


def first_match(pattern, text):
    m = pattern.search(text)
    return m.group(1).strip() if m else None


def main():
    if len(sys.argv) != 2:
        print("Usage: parse_telegram_job.py <post.txt>", file=sys.stderr)
        sys.exit(2)

    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    lines = [line.strip("•- ") for line in text.splitlines() if line.strip()]
    title = first_match(TITLE_RE, text) or (lines[0] if lines else None)
    company = first_match(COMPANY_RE, text)
    salary_line = next((line for line in lines if any(x in line.lower() for x in ["₽", "руб", "$", "usd", "зарплат"])), "")
    salary = normalize_salary_text(salary_line) if salary_line else {}
    urls = URL_RE.findall(text)
    contacts = CONTACT_RE.findall(text)

    vacancy = Vacancy(
        source="telegram",
        source_url=urls[0] if urls else None,
        company=company,
        title=title,
        stack=extract_stack(text),
        seniority=normalize_seniority(text),
        location=None,
        remote_mode=normalize_remote_mode(text),
        contact_url=contacts[0] if contacts else None,
        summary=" ".join(lines[:6])[:500] if lines else None,
        raw_text=text[:4000],
        **salary,
    )
    print(dump_json(vacancy.model_dump()))


if __name__ == "__main__":
    main()
