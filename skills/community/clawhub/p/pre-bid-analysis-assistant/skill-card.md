## Description:

基于招中标历史数据，协助分析招标项目、采购方、潜在竞争者、报价参考和投标风险，并生成投标决策报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

投标团队和采购分析人员可用此技能调查具体招标项目，评估采购方历史、竞争格局、历史成交价格与资格风险，并形成有依据的投标建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read or store a vendor API key and create a trial account tied to a hashed device identifier.

Mitigation: Use a preconfigured key to skip registration, or obtain explicit consent before account creation; safeguard stored credentials.

Risk: Reports can contain signed auto-login links that grant access when shared.

Mitigation: Review and remove sensitive links before sharing reports or screenshots; share only with intended recipients.

Risk: Procurement analysis uses a vendor API and can consume account credits.

Mitigation: Confirm the expected query cost before running a full analysis and verify consequential recommendations against source records.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dragonzu/skills/pre-bid-analysis-assistant)
- [API quick reference](artifact/references/api-quick.md)
- [Analysis workflow](artifact/references/workflow.md)
- [Report template](artifact/references/report-template.md)
- [Account registration guide](artifact/references/auto-register.md)

## Skill Output:

**Output Type(s):** [Markdown, HTML report, Guidance]

**Output Format:** [Markdown decision report; shareable HTML file for full analyses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes supporting citations, confidence and data gaps; report links may grant signed access.]

## Skill Version(s):

1.0.9 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
