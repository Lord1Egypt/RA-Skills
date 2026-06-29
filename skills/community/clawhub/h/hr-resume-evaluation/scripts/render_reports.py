from __future__ import annotations

import copy
from collections import Counter
import csv
import json
import re
import unicodedata
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "templates"

CSV_COLUMNS = [
    "candidate_id",
    "file_name",
    "score_basis",
    "overall_score",
    "resume_quality_score",
    "jd_company_match_score",
    "role_family",
    "seniority",
    "screening_bucket",
    "confidence",
    "top_strengths",
    "top_concerns",
    "manual_review_required",
    "report_path",
]

_SAFE_FILENAME_RE = re.compile(r"[^A-Za-z0-9._-]+")
_CSV_FORMULA_PREFIXES = ("=", "+", "-", "@")


def render_candidate_report(result, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    file_name = _safe_report_filename(result.get("candidate_id"))
    path = _safe_output_path(output_dir, file_name)
    template_result = copy.deepcopy(result)
    template_result["report_path"] = file_name

    template = _environment().get_template("candidate-report-template.md")
    path.write_text(template.render(result=template_result), encoding="utf-8")
    return path


def render_raw_json_result(result, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    file_name = Path(_safe_report_filename(result.get("candidate_id"))).with_suffix(".json").name
    path = _safe_output_path(output_dir, file_name)
    path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return path


def render_summary_report(results, failures, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    path = output_dir / "summary.md"
    rows = [_summary_row(result) for result in results]
    batch_summary = _batch_summary(results, rows, failures)
    template = _environment().get_template("summary-report-template.md")
    path.write_text(
        template.render(
            batch_summary=batch_summary,
            rows=rows,
            failures=failures,
            success_count=len(results),
            failure_count=len(failures),
        ),
        encoding="utf-8",
    )
    return path


def render_csv_summary(results, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    path = output_dir / "summary.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(_csv_safe_row(_summary_row(result)) for result in results)
    return path


def _summary_row(result):
    profile = result.get("inferred_profile", {})
    scores = result.get("scores", {})
    compliance = result.get("compliance", {})
    recommendation = result.get("recommendation", {})

    return {
        "candidate_id": result.get("candidate_id", ""),
        "file_name": result.get("file_name", ""),
        "score_basis": scores.get("score_basis", ""),
        "overall_score": _blank_none(scores.get("overall", "")),
        "resume_quality_score": _blank_none(scores.get("resume_quality", "")),
        "jd_company_match_score": _blank_none(scores.get("jd_company_match", "")),
        "role_family": profile.get("role_family", ""),
        "seniority": profile.get("seniority", ""),
        "screening_bucket": recommendation.get("screening_bucket", ""),
        "confidence": _blank_none(profile.get("confidence", "")),
        "top_strengths": _join_items(result.get("strengths", [])),
        "top_concerns": _join_items(result.get("concerns", [])),
        "manual_review_required": _join_items(compliance.get("manual_review_required", [])),
        "report_path": _safe_report_filename(result.get("candidate_id")),
    }


def _batch_summary(results, rows, failures):
    return {
        "total_evaluated": len(results) + len(failures),
        "jd_company_matching_count": sum(
            1 for row in rows if row["score_basis"] == "resume_plus_jd_company"
        ),
        "score_distribution": _counter_rows(_score_distribution(rows), score_bucket_order),
        "role_family_distribution": _counter_rows(_role_family_distribution(rows)),
        "common_gaps": _counter_rows(_common_gaps(results), by_count_desc=True),
    }


def _score_distribution(rows):
    return Counter(_score_bucket(row["overall_score"]) for row in rows)


def score_bucket_order(label):
    order = {
        "90-100": 0,
        "80-89": 1,
        "70-79": 2,
        "60-69": 3,
        "0-59": 4,
        "unscored": 5,
    }
    return order.get(label, 99)


def _score_bucket(score):
    if score == "":
        return "unscored"

    score = float(score)
    if score >= 90:
        return "90-100"
    if score >= 80:
        return "80-89"
    if score >= 70:
        return "70-79"
    if score >= 60:
        return "60-69"
    return "0-59"


def _role_family_distribution(rows):
    return Counter(row["role_family"] or "unknown" for row in rows)


def _common_gaps(results):
    return Counter(
        concern
        for result in results
        for concern in result.get("concerns", [])
        if str(concern).strip()
    )


def _counter_rows(counter, key=None, by_count_desc=False):
    sort_key = key or (lambda label: label)
    if by_count_desc:
        sorted_items = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    else:
        sorted_items = sorted(counter.items(), key=lambda item: (sort_key(item[0]), item[0]))
    return [
        {"label": label, "count": count}
        for label, count in sorted_items
        if count
    ]


def _environment():
    environment = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    environment.filters["md_table_cell"] = _markdown_table_cell
    return environment


def _safe_report_filename(candidate_id):
    stem = _SAFE_FILENAME_RE.sub("-", str(candidate_id or "candidate"))
    stem = re.sub(r"-+", "-", stem).strip(" ._-")
    return f"{stem or 'candidate'}.md"


def _safe_output_path(output_dir, file_name):
    path = output_dir / file_name
    if path.resolve().parent != output_dir.resolve():
        raise ValueError("candidate report path must stay inside output_dir")
    return path


def _markdown_table_cell(value):
    text = "" if value is None else str(value)
    return text.replace("\r\n", " ").replace("\r", " ").replace("\n", " ").replace("|", r"\|")


def _csv_safe_row(row):
    return {key: _escape_csv_formula(value) for key, value in row.items()}


def _escape_csv_formula(value):
    if isinstance(value, str) and _csv_formula_detection_text(value).startswith(_CSV_FORMULA_PREFIXES):
        return f"'{value}"
    return value


def _csv_formula_detection_text(value):
    index = 0
    while index < len(value) and (
        value[index].isspace() or unicodedata.category(value[index]) == "Cc"
    ):
        index += 1
    return value[index:]


def _join_items(items):
    return "；".join(str(item) for item in items)


def _blank_none(value):
    return "" if value is None else value
