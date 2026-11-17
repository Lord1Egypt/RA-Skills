## Description:

根据用户输入的医疗设备软件缺陷描述，生成包含问题现象、复现步骤、环境信息、严重等级和影响分析的 Markdown 问题报告草稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gnllk](https://clawhub.ai/user/gnllk)

### License/Terms of Use:

MIT-0

## Use Case:

测试工程师、质量工程师、技术支持和开发团队使用该技能把缺陷描述整理为可提交到 Jira、禅道或质量管理系统的问题报告草稿，并初步标注严重等级和待补充字段。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation keywords such as issue report or bug report may trigger the skill during routine discussions.

Mitigation: Confirm the invocation is intentional before generating or relying on a report draft.

Risk: Generated severity and medical-device report content may be incomplete or inaccurate for patient-safety, quality, or regulatory decisions.

Mitigation: Treat output as a draft and require review by qualified engineering, quality, or regulatory personnel before submission or action.

## Reference(s):

- [医疗设备软件问题报告模板](artifact/references/issue-template.md)
- [严重等级判断指南](artifact/references/severity-guidelines.md)
- [ClawHub Skill Page](https://clawhub.ai/gnllk/skills/issue-report-generator)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown issue-report draft with structured fields and completion checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated severity labels and medical-device issue content should be reviewed by qualified personnel before use in patient-safety, quality, or regulatory workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
