## Description:

工业领域招投标技术方案智能审查，帮助用户逐条对标国家和行业强制性标准，输出9维合规评分、审查清单、整改建议和交互式HTML合规报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, legal, and technical review teams use this skill to pre-review industrial bid technical proposals against applicable Chinese bidding, safety, environmental, energy-efficiency, quality, acceptance, qualification, and intellectual-property requirements. It is intended to surface likely non-compliance, missing items, rejection risks, and remediation actions before professional review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can embed bid document content, including untrusted user-supplied fields.

Mitigation: Open generated HTML reports only from trusted bid data until escaping or an auto-escaping template engine is verified.

Risk: Compliance conclusions are high-stakes and may exceed the implemented checks.

Mitigation: Treat findings as preliminary screening and require professional legal and technical review before relying on them.

Risk: Python dependencies are specified as broad version ranges.

Mitigation: Pin and audit dependencies before installation or operational use.

Risk: Industrial standards and legal requirements can change over time.

Mitigation: Verify cited standards and legal references against official sources at the time of review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/industrial-bid-compliance)
- [9维合规审查框架](references/compliance_framework.md)
- [工业领域标准分类映射表](references/industrial_standards_map.md)
- [逐条合规检查清单模板](references/bid_compliance_checklist.md)
- [招投标法律法规核心要点速查](references/bid_law_essentials.md)
- [国家标准全文公开系统](https://openstd.samr.gov.cn)
- [全国标准信息公共服务平台](https://std.samr.gov.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, JSON review data, and single-file HTML compliance reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include a 9-dimension compliance score, clause-level review records, rejection-risk summaries, remediation guidance, and generated report files.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
