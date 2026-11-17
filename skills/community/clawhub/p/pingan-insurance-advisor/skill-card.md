## Description:

健康保险顾问助手，帮助保险从业人员按标准SOP为客户进行需求分析、风险评估、保障缺口计算，并生成专业的方案建议书。

This skill is ready for commercial/non-commercial use.

## Publisher:

[918774384lwt-pixel](https://clawhub.ai/user/918774384lwt-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

External insurance advisors use this skill to guide customer KYC conversations, assess health and financial protection needs, match Ping An health insurance products, and prepare insurance proposal materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health and financial insurance details may be collected, exported, or retained outside approved workflows.

Mitigation: Use only in authorized insurance-advisor workflows with customer consent, redact unnecessary sensitive details, confirm destinations before Feishu, PDF, email, or archive use, and store records only in approved systems.

Risk: Report generation depends on local Python dependencies and document-export workflows that may fail or produce incomplete materials.

Mitigation: Use pinned dependencies for the report generator and verify generated Feishu documents or PDF reports before sharing them with customers.

Risk: Insurance recommendations may become stale as product availability, prices, or underwriting requirements change.

Mitigation: Review product data and final recommendations against current authorized product materials before presenting them to customers.

## Reference(s):

- [Insurance Advisor SOP Guide](references/sop-guide.md)
- [Ping An Product Library](assets/pingan_products.json)
- [ClawHub Skill Page](https://clawhub.ai/918774384lwt-pixel/skills/pingan-insurance-advisor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Conversational text and Markdown guidance, with optional JSON inputs and generated proposal report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce PDF reports through the bundled report-generation script and Feishu-style document content when the user confirms report generation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
