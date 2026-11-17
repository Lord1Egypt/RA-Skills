## Description:

Analyzes business plans to produce PESTL, Boston Matrix, SWOT, and business model canvas assessments with scored radar chart outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business analysts use this skill to evaluate a business plan's commercial feasibility, identify missing information, and generate structured strategy recommendations and scoring outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential business plans may contain sensitive commercial, customer, financial, or strategy information.

Mitigation: Review the skill before use with confidential plans, redact unnecessary sensitive details, and add clear privacy and document-handling instructions.

Risk: Generated HTML reports may execute unsafe injected content or third-party scripts.

Mitigation: Prefer PNG-only output, or escape untrusted report fields, pin or vendor ECharts, and apply a restrictive content security policy before sharing HTML reports.

Risk: Promotional runtime content can distract from risk and privacy expectations.

Mitigation: Remove promotional runtime sections from generated reports and keep user-facing guidance focused on analysis limits, security, and privacy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/golngod/skills/hutian-opc-business-model)
- [PESTL Analysis Template](references/01-PESTL分析模板.md)
- [Boston Matrix Template](references/02-波士顿矩阵模板.md)
- [SWOT Analysis Template](references/03-SWOT分析模板.md)
- [Business Model Canvas Template](references/04-画布九宫格模板.md)
- [Information Extraction Prompt](references/05-信息提取提示词.md)
- [Interactive Confirmation Flow](references/06-交互确认流程.md)
- [Radar Chart Generation Guide](references/07-雷达图生成说明.md)
- [Integrated Diagnosis Framework](references/08-综合诊断框架.md)
- [Scoring Criteria](references/09-评分标准详解.md)
- [Report Output Template](references/10-报告输出模板.md)
- [OPC Platform](https://opc.cn)
- [Coze Platform](https://coze.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with structured analysis, JSON scoring data, and optional PNG or HTML radar chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports PDF, Word, and text inputs; generated HTML should be reviewed before sharing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
