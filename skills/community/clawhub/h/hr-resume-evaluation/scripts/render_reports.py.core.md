---
source: "hr-resume-evaluation/scripts/render_reports.py"
core_kind: "code_project_core"
file_type: "py"
generated: "2026-06-14T08:55:07"
tags:
  - core-file
  - code-project-core
  - py
---
<!-- CORE_FILE_NOTE_V1 -->
# render_reports.py

- Source file: [[hr-resume-evaluation/scripts/render_reports.py|render_reports.py]]
- Folder index: [[hr-resume-evaluation/scripts/资料索引|资料索引]]
- Core kind: `code_project_core`
- Size: 7.08 KB
- Modified: 2026-06-13T18:22:28

## Summary
- PY source sample: 244 lines.
- Imports: __future__, copy, collections, csv, json, re, unicodedata, pathlib, jinja2
- Functions: render_candidate_report, render_raw_json_result, render_summary_report, render_csv_summary, _summary_row, _batch_summary, _score_distribution, score_bucket_order, _score_bucket, _role_family_distribution, _common_gaps, _counter_rows

## Related files
- [[hr-resume-evaluation/scripts/evaluate_resumes.py.core|evaluate_resumes.py]] - same folder
- [[hr-resume-evaluation/scripts/validate_results.py.core|validate_results.py]] - same folder
- [[hr-resume-evaluation/scripts/parse_documents.py.core|parse_documents.py]] - same folder
- [[hr-resume-evaluation/scripts/llm_client.py.core|llm_client.py]] - same folder
- [[hr-resume-evaluation/scripts/__init__.py.core|__init__.py]] - same folder

## Graph tags
- #core-file/code-project-core
- #file-type/py

## Content preview
```py
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
    path.write_text(template.render(result=template_result), encoding="ut
```

## Processing notes
- encoding=utf-8-sig
