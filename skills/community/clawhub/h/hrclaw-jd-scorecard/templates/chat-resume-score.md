# 简历评分结果（飞书/钉钉版）

## 候选人概况
- 姓名：{{candidate_profile.name}}
- 年限：{{candidate_profile.years_experience}}
- 学历：{{candidate_profile.education_level}}
- 当前岗位：{{candidate_profile.current_title}}
- 当前公司：{{candidate_profile.current_company}}
- 来源：{{source_type}} / {{extraction_status}}

## 评分结论
- 岗位：{{scorecard_name}}
- 结果：{{decision}}
- 总分：{{total_score}}
- 硬筛通过：{{hard_filter_pass}}

## 维度得分
- 必备项：{{dimension_scores.must_have_match}}
- 加分项：{{dimension_scores.nice_to_have_match}}
- 岗位匹配：{{dimension_scores.title_match}}
- 行业匹配：{{dimension_scores.industry_match}}
- 经验：{{dimension_scores.experience_fit}}
- 学历：{{dimension_scores.education_fit}}
- 地点：{{dimension_scores.location_fit}}

## 技能与行业
### 技能
{{#each candidate_profile.skills}}
- {{this}}
{{/each}}

### 行业标签
{{#each candidate_profile.industry_tags}}
- {{this}}
{{/each}}

## 命中项
{{#each matched_terms}}
- {{this}}
{{/each}}

## 缺失项
{{#each missing_terms}}
- {{this}}
{{/each}}

## 风险项
{{#each blocked_terms}}
- {{this}}
{{/each}}

## 硬筛失败原因
{{#each hard_filter_fail_reasons}}
- {{this}}
{{/each}}

## 证据
- 简历摘录：{{evidence.resume_excerpt}}
{{#each evidence.scorecard_signals}}
- {{this}}
{{/each}}

## 复核原因
{{#each review_reasons}}
- {{this}}
{{/each}}

## 下一步
{{#each next_steps}}
- {{this}}
{{/each}}
