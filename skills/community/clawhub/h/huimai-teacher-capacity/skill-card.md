## Description:

中国中小学教师教学能力动态评估系统，基于学生学业数据生成同年级班级学业对比图、教师教学能力评估图、同科教师横向对比和趋势分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

External K-12 education teams and school administrators use this skill to design teacher-capacity evaluation reports, compare class and subject performance, define role-based data visibility, and prepare chart or data-model specifications from homework assessment outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Teacher names, student performance data, rankings, exports, and permission changes can expose sensitive education records or personnel-sensitive information.

Mitigation: Use school-approved access controls, privacy review, anonymized comparison settings where appropriate, and explicit authorization before deployment or export.

Risk: Teacher evaluation scores and charts may be treated as decision-ready even when they are based on incomplete or low-confidence assessment inputs.

Mitigation: Review source data quality, confidence thresholds, weighting choices, and human context before using outputs for staffing, ranking, or intervention decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/skills/huimai-teacher-capacity)
- [数据模型参考](references/data-model.md)
- [权限模型参考](references/permission-model.md)
- [教师评估图表规格](references/chart-spec.md)
- [教材版本知识点映射方案](references/textbook-version-mapping.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-style chart, data model, and permission model examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on student knowledge-point mastery, class-level aggregates, and historical trend data from the homework-grading-assessment skill.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
