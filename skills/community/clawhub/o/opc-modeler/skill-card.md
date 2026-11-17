## Description:

一人公司商业模式建模，对应书稿第四章，帮助读者梳理自己的 OPC 商业模式画布并生成 9 要素分析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cglt2026opc](https://clawhub.ai/user/cglt2026opc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and solo-company builders use this skill to model a personal business canvas through guided questions, then generate a structured Markdown report covering resources, value proposition, customers, channels, revenue, costs, activities, partners, and risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects business-planning details that may include private goals, resources, contacts, channels, and income targets.

Mitigation: Share only information suitable for the agent context and choose a private save path when exporting the report.

Risk: Generated business recommendations may be incomplete or unsuitable for real-world decisions.

Mitigation: Review the generated report before acting on it or sharing it externally.

Risk: Broad trigger phrases such as business-modeling terms could activate the skill in conversations where the user did not intend to generate a report.

Mitigation: Prefer explicit invocation with "OPC建模" or "opc-modeler".

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cglt2026opc/skills/opc-modeler)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with tables and action recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save the generated report as a local Markdown file after the user confirms the path.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
