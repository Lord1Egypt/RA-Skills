## Description:

保险保单分析助手 — 帮助用户梳理、分析和优化保险保障方案。用户发送保单或提供信息后，帮你分析保障是否全面、保额是否充足、费用是否合理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[waylonchiao0215](https://clawhub.ai/user/waylonchiao0215)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this Chinese-language skill to collect insurance-policy and personal-context details, organize policy terms, assess coverage completeness, coverage amount adequacy, cost reasonableness, and family fit, and receive prioritized optimization suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for sensitive health, family, financial, and insurance-policy information.

Mitigation: Redact names, ID numbers, addresses, policy numbers, and other identifiers unless they are truly needed, and share only information required for the analysis.

Risk: The output may be mistaken for professional insurance advice.

Mitigation: Treat the analysis as informational, verify conclusions against the policy contract, and consult an insurance broker or qualified professional for decisions.

## Reference(s):

- [Insurance Policy Analysis Guide](references/analysis-guide.md)
- [User Information Questionnaire](references/questionnaire.md)
- [Insurance Terms](references/terms.md)
- [ClawHub Skill Page](https://clawhub.ai/waylonchiao0215/skills/insurance-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured tables, diagnoses, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language insurance analysis guidance; informational only and not professional insurance advice.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
