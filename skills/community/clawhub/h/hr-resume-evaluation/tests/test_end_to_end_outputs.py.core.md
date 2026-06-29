---
source: "hr-resume-evaluation/tests/test_end_to_end_outputs.py"
core_kind: "code_project_core"
file_type: "py"
generated: "2026-06-14T08:55:07"
tags:
  - core-file
  - code-project-core
  - py
---
<!-- CORE_FILE_NOTE_V1 -->
# test_end_to_end_outputs.py

- Source file: [[hr-resume-evaluation/tests/test_end_to_end_outputs.py|test_end_to_end_outputs.py]]
- Folder index: [[hr-resume-evaluation/tests/资料索引|资料索引]]
- Core kind: `code_project_core`
- Size: 3.01 KB
- Modified: 2026-06-13T14:26:36

## Summary
- PY source sample: 87 lines.
- Imports: pathlib, scripts.evaluate_resumes
- Functions: model_result, test_end_to_end_outputs_with_jd_and_company

## Related files
- [[hr-resume-evaluation/tests/test_render_reports.py.core|test_render_reports.py]] - same folder
- [[hr-resume-evaluation/tests/test_validate_results.py.core|test_validate_results.py]] - same folder
- [[hr-resume-evaluation/tests/test_evaluate_resumes.py.core|test_evaluate_resumes.py]] - same folder
- [[hr-resume-evaluation/tests/test_llm_client.py.core|test_llm_client.py]] - same folder
- [[hr-resume-evaluation/tests/test_parse_documents.py.core|test_parse_documents.py]] - same folder

## Graph tags
- #core-file/code-project-core
- #file-type/py

## Content preview
```py
from pathlib import Path

from scripts.evaluate_resumes import run_batch


JD_TEXT = "# JD\n\nNeed product launch ownership."
COMPANY_TEXT = "# Company\n\nB2B SaaS."


def model_result(parsed, jd, company, evaluation_config, model_config):
    assert jd == JD_TEXT
    assert company == COMPANY_TEXT

    score_basis = "resume_plus_jd_company" if jd or company else "resume_quality_only"

    return {
        "candidate_id": parsed.candidate_id,
        "inferred_profile": {
            "role_family": "Product and Project",
            "seniority": "mid",
            "domain_context": "B2B SaaS",
            "confidence": 0.75,
        },
        "scores": {
            "score_basis": score_basis,
            "overall": 78 if score_basis == "resume_plus_jd_company" else 80,
            "resume_quality": 48,
            "jd_company_match": 30 if score_basis == "resume_plus_jd_company" else None,
            "dimensions": [
                {
                    "name": "capability_clarity",
                    "score": 8,
                    "max_score": 10,
                    "evidence": ["owns launch work"],
                    "deductions": [],
                }
            ],
```

## Processing notes
- encoding=utf-8-sig
