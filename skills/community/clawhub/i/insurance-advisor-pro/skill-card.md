## Description:

健康保险顾问助手，帮助保险从业人员按标准SOP为客户进行需求分析(KYC)、风险评估、保障缺口计算，并生成专业的方案建议书。

This skill is ready for commercial/non-commercial use.

## Publisher:

[918774384lwt-pixel](https://clawhub.ai/user/918774384lwt-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

保险顾问和保险从业人员使用此技能按SOP收集客户KYC信息，评估健康、财务和保障缺口，并生成面向客户的保险方案建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive customer health and financial KYC data may be exposed in generated reports or cloud documents.

Mitigation: Use the skill only with clear customer consent, minimize or redact sensitive fields, and verify document destinations and sharing settings before export.

Risk: Insurance recommendations may be unsuitable if product details, eligibility, health disclosures, exclusions, or customer needs are incomplete.

Mitigation: Confirm current product terms, customer disclosures, and applicable compliance requirements before presenting or submitting any insurance application.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/918774384lwt-pixel/skills/insurance-advisor-pro)
- [保险顾问标准作业流程（SOP）参考](references/sop-guide.md)
- [平安健康险产品库](assets/pingan_products.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Conversational text and Markdown reports with optional JSON inputs and PDF report generation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product recommendations, risk analysis, coverage gap calculations, and customer-facing proposal content.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
