# {{role_title}} 评分卡（飞书/钉钉版）

## 一句话结论
{{summary}}

## 关键筛选
- 地点：{{filters.location}}
- 年限：{{filters.years_min}}
- 学历：{{filters.education_min}}

## 权重与阈值
- 推荐阈值：{{thresholds.recommend_min}}
- 复核阈值：{{thresholds.review_min}}
- 必备项：{{weights.must_have}}
- 加分项：{{weights.nice_to_have}}
- 岗位匹配：{{weights.title_match}}
- 行业匹配：{{weights.industry_match}}
- 经验：{{weights.experience}}
- 学历：{{weights.education}}
- 地点：{{weights.location}}

## 必备项
{{#each must_have}}
- {{this}}
{{/each}}

## 加分项
{{#each nice_to_have}}
- {{this}}
{{/each}}

## 排除项
{{#each exclude}}
- {{this}}
{{/each}}

## 面试题
{{#each interview_questions}}
- {{this}}
{{/each}}

## 红旗
{{#each red_flags}}
- {{this}}
{{/each}}

## 备注
{{#each assumptions}}
- {{this}}
{{/each}}

## 下一步
{{#each next_steps}}
- {{this}}
{{/each}}
