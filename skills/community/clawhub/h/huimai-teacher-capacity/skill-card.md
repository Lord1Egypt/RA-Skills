## Description: <br>
中国中小学教师教学能力动态评估系统，基于学生学业数据生成同年级班级学业对比、同科教师横向对比、教师能力趋势和分级权限视图。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack) <br>

### License/Terms of Use: <br>
MIT-0; Huimai Intelligence commercial terms described in SKILL.md <br>


## Use Case: <br>
School administrators, academic leaders, and teachers use this skill to turn class-level learning data into teacher capacity reports, subject comparisons, trend charts, and role-based views for Chinese K-12 education. <br>

### Deployment Geography for Use: <br>
Global; content and examples are China K-12 focused. <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive student or teacher records may be exposed if role permissions, export controls, or retention settings are misconfigured. <br>
Mitigation: Confirm authorized school roles before deployment, keep anonymous views as the default where appropriate, limit and log exports, and align retention with local education and employment requirements. <br>
Risk: Teacher evaluations may be over-interpreted if generated scores are treated as definitive personnel judgments without reviewing the input data and weighting choices. <br>
Mitigation: Review evaluation weights, source data snapshots, and generated recommendations with school leadership before using outputs for formal decisions. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/yezhaowang888-stack/huimai-teacher-capacity) <br>
- [Data model reference](references/data-model.md) <br>
- [Permission model reference](references/permission-model.md) <br>
- [Teacher evaluation chart specification](references/chart-spec.md) <br>
- [Textbook version knowledge-point mapping](references/textbook-version-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured chart, data-model, permission, and report specifications; some sections include JSON, SQL, YAML, and table examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces analysis guidance and report/chart specifications for downstream agent use; it depends on homework-grading-assessment outputs and school role configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
