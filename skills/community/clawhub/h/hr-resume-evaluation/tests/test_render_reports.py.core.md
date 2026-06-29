---
source: "hr-resume-evaluation/tests/test_render_reports.py"
core_kind: "code_project_core"
file_type: "py"
generated: "2026-06-14T08:55:07"
tags:
  - core-file
  - code-project-core
  - py
---
<!-- CORE_FILE_NOTE_V1 -->
# test_render_reports.py

- Source file: [[hr-resume-evaluation/tests/test_render_reports.py|test_render_reports.py]]
- Folder index: [[hr-resume-evaluation/tests/资料索引|资料索引]]
- Core kind: `code_project_core`
- Size: 7.61 KB
- Modified: 2026-06-13T15:13:57

## Summary
- PY source sample: 238 lines.
- Imports: copy, csv, scripts.render_reports
- Functions: sample_result, test_render_candidate_report_contains_scores_and_compliance, test_render_summary_report_lists_candidate, test_render_summary_report_includes_batch_aggregations, test_render_summary_report_counts_failures_in_total_evaluated, test_render_csv_summary_has_expected_columns, test_candidate_report_uses_safe_filename_inside_output_dir, test_render_candidate_report_does_not_mutate_input, test_summary_table_escapes_markdown_cells, test_csv_escapes_formula_values_and_has_bom, test_csv_escapes_whitespace_prefixed_formula_values, test_csv_escapes_control_prefixed_formula_values

## Related files
- [[hr-resume-evaluation/tests/test_end_to_end_outputs.py.core|test_end_to_end_outputs.py]] - same folder
- [[hr-resume-evaluation/tests/test_evaluate_resumes.py.core|test_evaluate_resumes.py]] - same folder
- [[hr-resume-evaluation/tests/test_validate_results.py.core|test_validate_results.py]] - same folder
- [[hr-resume-evaluation/tests/test_parse_documents.py.core|test_parse_documents.py]] - same folder
- [[hr-resume-evaluation/tests/test_llm_client.py.core|test_llm_client.py]] - same folder

## Graph tags
- #core-file/code-project-core
- #file-type/py

## Content preview
```py
import copy
import csv

from scripts.render_reports import (
    render_candidate_report,
    render_csv_summary,
    render_summary_report,
)


def sample_result(candidate_id="alice"):
    return {
        "candidate_id": candidate_id,
        "file_name": f"{candidate_id}.md",
        "report_path": "",
        "inferred_profile": {
            "role_family": "engineering",
            "seniority": "mid",
            "domain_context": "backend services",
            "confidence": 0.8,
        },
        "scores": {
            "score_basis": "resume_plus_jd_company",
            "overall": 80,
            "resume_quality": 50,
            "jd_company_match": 30,
            "dimensions": [
                {
                    "name": "工程交付",
                    "score": 20,
                    "max_score": 25,
                    "evidence": ["负责后端服务交付。"],
                    "deductions": ["缺少规模化指标。"],
                }
            ],
        },
        "evidence": ["简历体现 Python 和 API 项目经验。"],
        "deductions": ["云平台深度证据不足。"],
        "strengths": ["后端实现经验清晰。"],
        "concerns": ["需要验证分布式系统深度。"],
        "interview_validation_points": ["追问 API 稳定性 ownership。"],
        "
```

## Processing notes
- encoding=utf-8-sig
