---
source: "hr-resume-evaluation/scripts/evaluate_resumes.py"
core_kind: "code_project_core"
file_type: "py"
generated: "2026-06-14T08:55:07"
tags:
  - core-file
  - code-project-core
  - py
---
<!-- CORE_FILE_NOTE_V1 -->
# evaluate_resumes.py

- Source file: [[hr-resume-evaluation/scripts/evaluate_resumes.py|evaluate_resumes.py]]
- Folder index: [[hr-resume-evaluation/scripts/资料索引|资料索引]]
- Core kind: `code_project_core`
- Size: 9.28 KB
- Modified: 2026-06-13T15:23:29

## Summary
- PY source sample: 283 lines.
- Imports: __future__, argparse, copy, json, sys, datetime, pathlib, typing, yaml, scripts.llm_client
- Functions: run_batch, _evaluate_and_validate, _prepare_for_validation, _sanitize_evaluation, _failure_record, _parse_error_code, _model_evaluator, _read_optional_text, _load_yaml, _max_model_retries, _exit_code, _parser

## Related files
- [[hr-resume-evaluation/scripts/validate_results.py.core|validate_results.py]] - same folder
- [[hr-resume-evaluation/scripts/parse_documents.py.core|parse_documents.py]] - same folder
- [[hr-resume-evaluation/scripts/render_reports.py.core|render_reports.py]] - same folder
- [[hr-resume-evaluation/scripts/__init__.py.core|__init__.py]] - same folder
- [[hr-resume-evaluation/scripts/llm_client.py.core|llm_client.py]] - same folder

## Graph tags
- #core-file/code-project-core
- #file-type/py

## Content preview
```py
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import yaml

if __package__ in {None, ""}:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from scripts.llm_client import ModelConfig, build_messages, evaluate_with_model, load_model_config
from scripts.parse_documents import ParsedDocument, discover_resumes, parse_document
from scripts.render_reports import (
    render_candidate_report,
    render_csv_summary,
    render_raw_json_result,
    render_summary_report,
)
from scripts.validate_results import ValidationError, validate_evaluation


KNOWN_PARSE_ERRORS = {"empty_text", "unsupported_extension"}
TOP_LEVEL_RESULT_KEYS = (
    "candidate_id",
    "file_name",
    "inferred_profile",
    "scores",
    "evidence",
    "deductions",
    "strengths",
    "concerns",
    "interview_validation_points",
    "compliance",
    "recommendation",
    "audit",
)

Evaluator = Callable[
    [ParsedDocument, str | None, str | None, dict[str, Any], ModelConfig | Non
```

## Processing notes
- encoding=utf-8-sig
