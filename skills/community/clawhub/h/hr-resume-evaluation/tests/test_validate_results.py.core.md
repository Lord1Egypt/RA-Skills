---
source: "hr-resume-evaluation/tests/test_validate_results.py"
core_kind: "code_project_core"
file_type: "py"
generated: "2026-06-14T08:55:07"
tags:
  - core-file
  - code-project-core
  - py
---
<!-- CORE_FILE_NOTE_V1 -->
# test_validate_results.py

- Source file: [[hr-resume-evaluation/tests/test_validate_results.py|test_validate_results.py]]
- Folder index: [[hr-resume-evaluation/tests/资料索引|资料索引]]
- Core kind: `code_project_core`
- Size: 12.79 KB
- Modified: 2026-06-13T15:24:06

## Summary
- PY source sample: 403 lines.
- Imports: copy, pytest, scripts.validate_results
- Functions: valid_result, test_valid_result_passes, test_invalid_bucket_fails, test_missing_profile_role_family_fails, test_missing_recommendation_summary_fails, test_recommendation_next_steps_must_be_list, test_recommendation_summary_rejects_final_decision_label, test_recommendation_next_steps_reject_final_decision_label, test_compliance_warning_labels_do_not_trigger_recommendation_label_check, weighted_config, weighted_result, test_configured_weight_dimensions_pass

## Related files
- [[hr-resume-evaluation/tests/test_evaluate_resumes.py.core|test_evaluate_resumes.py]] - same folder
- [[hr-resume-evaluation/tests/test_render_reports.py.core|test_render_reports.py]] - same folder
- [[hr-resume-evaluation/tests/test_end_to_end_outputs.py.core|test_end_to_end_outputs.py]] - same folder
- [[hr-resume-evaluation/tests/test_parse_documents.py.core|test_parse_documents.py]] - same folder
- [[hr-resume-evaluation/tests/test_llm_client.py.core|test_llm_client.py]] - same folder

## Graph tags
- #core-file/code-project-core
- #file-type/py

## Content preview
```py
from copy import deepcopy

import pytest

from scripts.validate_results import ValidationError, validate_evaluation


def valid_result():
    return {
        "candidate_id": "alice-resume",
        "inferred_profile": {
            "role_family": "engineering",
            "seniority": "mid",
            "domain_context": "backend services",
            "confidence": 0.8,
        },
        "scores": {
            "score_basis": "resume_plus_jd_company",
            "overall": 82,
            "resume_quality": 50,
            "jd_company_match": 32,
            "dimensions": [
                {
                    "name": "backend experience",
                    "score": 24,
                    "max_score": 30,
                    "evidence": ["Built production API services."],
                    "deductions": [],
                }
            ],
        },
        "evidence": ["Python and API delivery experience."],
        "deductions": ["Limited explicit cloud ownership evidence."],
        "strengths": ["Clear backend implementation history."],
        "concerns": ["Needs validation on distributed systems depth."],
        "interview_validation_points": ["Probe API reliabili
```

## Processing notes
- encoding=utf-8-sig
