---
source: "config/evaluation.yaml"
core_kind: "business_material"
file_type: "yaml"
generated: "2026-06-14T19:16:07"
tags:
  - core-file
  - business-material
  - yaml
---
<!-- CORE_FILE_NOTE_V1 -->
# evaluation.yaml

- Source file: [[config/evaluation.yaml|evaluation.yaml]]
- Folder index: [[config/资料索引|资料索引]]
- Core kind: `business_material`
- Size: 666 B
- Modified: 2026-06-14T19:15:21

## Summary
- YAML sample: 26 lines, 666 chars.
- Opening: output_language: "zh"
- Keywords: output_language, include_raw_json, max_model_retries, role_family_override, seniority_override, weights, resume_quality, information_completeness, structure_readability, experience_credibility

## Related files
- [[config/evaluation.yaml.core|evaluation.yaml.core.md]] - same folder
- [[config/model.yaml.core|model.yaml.core.md]] - same folder
- [[config/model.yaml.core|model.yaml]] - same folder

## Graph tags
- #core-file/business-material
- #file-type/yaml

## Content preview
```text
output_language: "zh"
include_raw_json: true
max_model_retries: 2
role_family_override: null
seniority_override: null
weights:
  resume_quality:
    information_completeness: 6
    structure_readability: 5
    experience_credibility: 9
    project_delivery_impact: 18
    technical_depth_and_feasibility: 10
    education_research_competition_signal: 7
    risk_review_signals: 5
  jd_company_match:
    hard_requirement_match: 8
    core_capability_match: 10
    jd_relevant_project_match: 14
    domain_industry_relevance: 4
    seniority_match: 3
    interview_validation_value: 1
screening_buckets:
  - strong_review
  - review
  - weak_review
  - manual_review
```

## Processing notes
- encoding=utf-8-sig
