# 候选人简历评估：{{ result.candidate_id }}

> 本报告仅作为招聘人工复核辅助材料，不构成录用、淘汰或最终筛选决定。

## 元数据

- 候选人 ID：{{ result.candidate_id }}
- 文件名：{{ result.file_name }}
{% if result.audit is defined -%}
- 评估时间：{{ result.audit.evaluation_time }}
- 是否使用 JD/公司背景：{{ "是" if result.audit.jd_company_context_used else "否" }}
{% endif -%}
- score_basis：{{ result.scores.score_basis }}
- 总分：{{ result.scores.overall }}
- 通用简历质量分：{{ result.scores.resume_quality }}
- JD/公司匹配分：{{ result.scores.jd_company_match if result.scores.jd_company_match is not none else "无" }}
- 复核分桶：{{ result.recommendation.screening_bucket }}
- 角色族：{{ result.inferred_profile.role_family }}
- 资历层级：{{ result.inferred_profile.seniority }}
- 置信度：{{ result.inferred_profile.confidence }}

## 维度分

| 维度 | 得分 | 满分 | 证据 | 扣分 |
| --- | ---: | ---: | --- | --- |
{% for dimension in result.scores.dimensions -%}
| {{ dimension.name | md_table_cell }} | {{ dimension.score | md_table_cell }} | {{ dimension.max_score | md_table_cell }} | {{ (dimension.evidence | join("；") if dimension.evidence else "无") | md_table_cell }} | {{ (dimension.deductions | join("；") if dimension.deductions else "无") | md_table_cell }} |
{% endfor %}

## 优势

{% if result.strengths -%}
{% for item in result.strengths -%}
- {{ item }}
{% endfor -%}
{% else -%}
- 无
{% endif %}

## 风险与疑点

{% if result.concerns -%}
{% for item in result.concerns -%}
- {{ item }}
{% endfor -%}
{% else -%}
- 无
{% endif %}

## 面试验证点

{% if result.interview_validation_points -%}
{% for item in result.interview_validation_points -%}
- {{ item }}
{% endfor -%}
{% else -%}
- 无
{% endif %}

## 合规提醒

### 敏感或无关信息

{% if result.compliance.sensitive_or_irrelevant_information -%}
{% for item in result.compliance.sensitive_or_irrelevant_information -%}
- {{ item }}
{% endfor -%}
{% else -%}
- 无
{% endif %}

### 不得作为筛选依据

{% if result.compliance.must_not_use_for_screening -%}
{% for item in result.compliance.must_not_use_for_screening -%}
- {{ item }}
{% endfor -%}
{% else -%}
- 无
{% endif %}

### 人工复核项

{% if result.compliance.manual_review_required -%}
{% for item in result.compliance.manual_review_required -%}
- {{ item }}
{% endfor -%}
{% else -%}
- 无
{% endif %}

### 禁止自动淘汰原因

{% if result.compliance.no_auto_reject_reasons -%}
{% for item in result.compliance.no_auto_reject_reasons -%}
- {{ item }}
{% endfor -%}
{% else -%}
- 无
{% endif %}

## 建议

- 结论分桶：{{ result.recommendation.screening_bucket }}
- 摘要：{{ result.recommendation.summary }}
{% if result.recommendation.next_steps -%}
{% for item in result.recommendation.next_steps -%}
- 下一步：{{ item }}
{% endfor -%}
{% endif %}

> 提醒：评分和分桶必须由招聘人员结合岗位要求复核；敏感或与岗位无关的信息不得作为筛选依据。
