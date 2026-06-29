---
source: "hr-resume-evaluation/scripts/validate_results.py"
core_kind: "code_project_core"
file_type: "py"
generated: "2026-06-14T08:55:07"
tags:
  - core-file
  - code-project-core
  - py
---
<!-- CORE_FILE_NOTE_V1 -->
# validate_results.py

- Source file: [[hr-resume-evaluation/scripts/validate_results.py|validate_results.py]]
- Folder index: [[hr-resume-evaluation/scripts/资料索引|资料索引]]
- Core kind: `code_project_core`
- Size: 8.81 KB
- Modified: 2026-06-13T15:23:22

## Summary
- PY source sample: 245 lines.
- Imports: __future__, math, re, collections.abc
- Classes: ValidationError
- Functions: validate_evaluation, _require_keys, _require_list_fields, _validate_profile, _validate_recommendation, _reject_final_decision_labels, _validate_scores, _validate_weighted_dimensions, _dimension_weights, _sum_dimension_scores, _validate_compliance, _number

## Related files
- [[hr-resume-evaluation/scripts/evaluate_resumes.py.core|evaluate_resumes.py]] - same folder
- [[hr-resume-evaluation/scripts/render_reports.py.core|render_reports.py]] - same folder
- [[hr-resume-evaluation/scripts/parse_documents.py.core|parse_documents.py]] - same folder
- [[hr-resume-evaluation/scripts/__init__.py.core|__init__.py]] - same folder
- [[hr-resume-evaluation/scripts/llm_client.py.core|llm_client.py]] - same folder

## Graph tags
- #core-file/code-project-core
- #file-type/py

## Content preview
```py
from __future__ import annotations

import math
import re
from collections.abc import Mapping


ALLOWED_BUCKETS = {"strong_review", "review", "weak_review", "manual_review"}
ALLOWED_SCORE_BASIS = {"resume_quality_only", "resume_plus_jd_company"}
FINAL_DECISION_LABEL_RE = re.compile(
    r"\b(hire|reject|pass|fail|eliminate|admit)\b",
    re.IGNORECASE,
)
FINAL_DECISION_CJK_LABELS = (
    "\u5f55\u7528",
    "\u6dd8\u6c70",
    "\u901a\u8fc7",
    "\u4e0d\u901a\u8fc7",
)


class ValidationError(ValueError):
    pass


def validate_evaluation(data, evaluation_config=None):
    evaluation_config = evaluation_config or {}
    _require_keys(
        data,
        (
            "candidate_id",
            "inferred_profile",
            "scores",
            "evidence",
            "deductions",
            "strengths",
            "concerns",
            "interview_validation_points",
            "compliance",
            "recommendation",
        ),
        "evaluation",
    )
    _require_list_fields(
        data,
        ("evidence", "deductions", "strengths", "concerns", "interview_validation_points"),
        "evaluation",
    )
    _validate_profile(data["inferred_profile"])
```

## Processing notes
- encoding=utf-8-sig
