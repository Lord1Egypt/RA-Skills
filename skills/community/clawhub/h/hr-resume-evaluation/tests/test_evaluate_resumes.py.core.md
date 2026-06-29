---
source: "hr-resume-evaluation/tests/test_evaluate_resumes.py"
core_kind: "code_project_core"
file_type: "py"
generated: "2026-06-14T08:55:07"
tags:
  - core-file
  - code-project-core
  - py
---
<!-- CORE_FILE_NOTE_V1 -->
# test_evaluate_resumes.py

- Source file: [[hr-resume-evaluation/tests/test_evaluate_resumes.py|test_evaluate_resumes.py]]
- Folder index: [[hr-resume-evaluation/tests/资料索引|资料索引]]
- Core kind: `code_project_core`
- Size: 18.39 KB
- Modified: 2026-06-13T15:24:22

## Summary
- PY source sample: 521 lines.
- Imports: csv, json, subprocess, sys, datetime, pathlib, scripts.evaluate_resumes
- Functions: fake_model_result, test_run_batch_generates_reports_without_jd, test_run_batch_retries_validation_failure_and_succeeds, test_run_batch_applies_recruiter_overrides_before_rendering, test_run_batch_enforces_configured_dimension_weights, test_run_batch_retries_non_object_model_output_and_succeeds, test_run_batch_writes_sanitized_raw_json_when_enabled, test_run_batch_skips_raw_json_when_disabled, test_run_batch_repeated_validation_failure_is_sanitized, test_run_batch_writes_distinct_reports_for_chinese_filenames, test_run_batch_records_parse_failure, test_run_batch_sanitizes_parser_exception_details

## Related files
- [[hr-resume-evaluation/tests/test_validate_results.py.core|test_validate_results.py]] - same folder
- [[hr-resume-evaluation/tests/test_parse_documents.py.core|test_parse_documents.py]] - same folder
- [[hr-resume-evaluation/tests/test_render_reports.py.core|test_render_reports.py]] - same folder
- [[hr-resume-evaluation/tests/test_end_to_end_outputs.py.core|test_end_to_end_outputs.py]] - same folder
- [[hr-resume-evaluation/tests/test_llm_client.py.core|test_llm_client.py]] - same folder

## Graph tags
- #core-file/code-project-core
- #file-type/py

## Content preview
```py
import csv
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from scripts.evaluate_resumes import _parser
from scripts.evaluate_resumes import run_batch


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def fake_model_result(candidate_id):
    return {
        "candidate_id": candidate_id,
        "inferred_profile": {
            "role_family": "Sales and Business",
            "seniority": "mid",
            "domain_context": "enterprise sales",
            "confidence": 0.85,
        },
        "scores": {
            "score_basis": "resume_quality_only",
            "overall": 80,
            "resume_quality": 48,
            "jd_company_match": None,
            "dimensions": [
                {
                    "name": "achievement_impact",
                    "score": 12,
                    "max_score": 15,
                    "evidence": ["delivered revenue growth"],
                    "deductions": [],
                }
            ],
        },
        "evidence": ["delivered revenue growth"],
        "deductions": [],
        "strengths": ["Clear evidence of revenue impact."],
        "concerns": ["Validate sales c
```

## Processing notes
- encoding=utf-8-sig
