# 批量简历评估汇总

- 成功数量：{{ success_count }}
- 失败数量：{{ failure_count }}
- total_evaluated: {{ batch_summary.total_evaluated }}
- jd_company_matching_count: {{ batch_summary.jd_company_matching_count }}

## Batch Aggregations

### score_distribution

{% if batch_summary.score_distribution -%}
{% for item in batch_summary.score_distribution -%}
- {{ item.label | md_table_cell }}: {{ item.count }}
{% endfor -%}
{% else -%}
- none
{% endif %}

### role_family_distribution

{% if batch_summary.role_family_distribution -%}
{% for item in batch_summary.role_family_distribution -%}
- {{ item.label | md_table_cell }}: {{ item.count }}
{% endfor -%}
{% else -%}
- none
{% endif %}

### common_gaps

{% if batch_summary.common_gaps -%}
{% for item in batch_summary.common_gaps -%}
- {{ item.label | md_table_cell }}: {{ item.count }}
{% endfor -%}
{% else -%}
- none
{% endif %}

## 候选人列表

| candidate_id | file_name | score_basis | 总分 | 简历质量分 | JD/公司匹配分 | role_family | seniority | bucket | report |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
{% for row in rows -%}
| {{ row.candidate_id | md_table_cell }} | {{ row.file_name | md_table_cell }} | {{ row.score_basis | md_table_cell }} | {{ row.overall_score | md_table_cell }} | {{ row.resume_quality_score | md_table_cell }} | {{ row.jd_company_match_score | md_table_cell }} | {{ row.role_family | md_table_cell }} | {{ row.seniority | md_table_cell }} | {{ row.screening_bucket | md_table_cell }} | {{ row.report_path | md_table_cell }} |
{% endfor %}

## 人工复核列表

{% set manual_rows = rows | selectattr("manual_review_required") | list -%}
{% if manual_rows -%}
{% for row in manual_rows -%}
- {{ row.candidate_id }}：{{ row.manual_review_required }}
{% endfor -%}
{% else -%}
- 无
{% endif %}

## 失败列表

{% if failures -%}
{% for failure in failures -%}
{% set failure_file = failure.file_name | default("") -%}
{% set failure_candidate = failure.candidate_id | default("") -%}
{% if failure_file and failure_candidate -%}
- {{ failure_file }} ({{ failure_candidate }})：{{ failure.error | default("unknown_error") }}
{% elif failure_file -%}
- {{ failure_file }}：{{ failure.error | default("unknown_error") }}
{% elif failure_candidate -%}
- {{ failure_candidate }}：{{ failure.error | default("unknown_error") }}
{% else -%}
- unknown：{{ failure.error | default("unknown_error") }}
{% endif -%}
{% endfor -%}
{% else -%}
- 无
{% endif %}
