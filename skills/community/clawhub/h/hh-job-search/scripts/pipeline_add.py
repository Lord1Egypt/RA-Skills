#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

from job_models import Vacancy


def fmt_salary(v: Vacancy) -> str:
    if v.salary_min and v.salary_max:
        return f"{v.salary_min}-{v.salary_max} {v.salary_currency or ''}".strip()
    if v.salary_min:
        return f"{v.salary_min} {v.salary_currency or ''}".strip()
    return ""


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def main():
    if len(sys.argv) not in (3, 4):
        print("Usage: pipeline_add.py <project-dir> <vacancy.json> [status]", file=sys.stderr)
        sys.exit(2)

    project_dir = Path(sys.argv[1])
    vacancy = Vacancy.model_validate(json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")))
    status = sys.argv[3] if len(sys.argv) == 4 else (vacancy.status or "found")
    pipeline = project_dir / "PIPELINE.md"

    if not pipeline.exists():
        raise SystemExit(f"PIPELINE.md not found in {project_dir}")

    row = "| {date_found} | {source} | {company} | {title} | {url} | {fit_label} | {fit_score} | {salary} | {location} | {status} | {last_action} | {next_follow_up} | {notes} |\n".format(
        date_found=date.today().isoformat(),
        source=md_escape(vacancy.source or ""),
        company=md_escape(vacancy.company or ""),
        title=md_escape(vacancy.title or ""),
        url=md_escape(vacancy.source_url or ""),
        fit_label=md_escape(vacancy.fit_label or ""),
        fit_score=vacancy.fit_score or "",
        salary=md_escape(fmt_salary(vacancy)),
        location=md_escape(vacancy.location or vacancy.remote_mode or ""),
        status=md_escape(status),
        last_action="added",
        next_follow_up="",
        notes=md_escape("; ".join(vacancy.fit_reasons[:3])),
    )
    with pipeline.open("a", encoding="utf-8") as f:
        f.write(row)
    print(f"Added pipeline row for: {vacancy.company or '-'} / {vacancy.title or '-'}")


if __name__ == "__main__":
    main()
