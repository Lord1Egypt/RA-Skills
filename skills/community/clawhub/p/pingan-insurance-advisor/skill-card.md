## Description: <br>
健康保险顾问助手，帮助保险从业人员按标准SOP为客户进行需求分析(KYC)、风险评估、保障缺口计算，并生成专业的方案建议书。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[918774384lwt-pixel](https://clawhub.ai/user/918774384lwt-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Insurance advisors use this skill to conduct customer KYC conversations, assess health and financial risk, calculate insurance coverage gaps, recommend Ping An health insurance products, and generate customer-facing proposal reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collects and exports sensitive customer health, identity, financial, family, and insurance information. <br>
Mitigation: Use it only with explicit customer consent, collect the minimum necessary fields, avoid unnecessary identifiers or raw medical details, and define retention and deletion rules before real-client use. <br>
Risk: Generated insurance recommendations and reports may be shared through Feishu documents or exported files with inappropriate access permissions. <br>
Mitigation: Verify document sharing permissions and review generated reports for completeness, accuracy, and compliance before sharing with customers. <br>
Risk: Insurance advice may be misleading if product data, health disclosures, or local regulatory requirements are incomplete or stale. <br>
Mitigation: Have a qualified insurance advisor validate product availability, health告知, exemptions, budget assumptions, and required disclosures before any sales or policy action. <br>


## Reference(s): <br>
- [SOP Guide](references/sop-guide.md) <br>
- [Ping An Product Library](assets/pingan_products.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/918774384lwt-pixel/pingan-insurance-advisor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational guidance and Markdown-style insurance recommendations, with optional JSON inputs, shell command snippets, Feishu document instructions, and PDF report generation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process customer KYC, health, identity, financial, insurance budget, and family responsibility details; generated reports should be reviewed before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
