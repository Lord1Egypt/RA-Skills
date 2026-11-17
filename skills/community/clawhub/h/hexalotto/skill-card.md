## Description:

HexaLotto 六爻奇门测彩 is a Chinese-language entertainment skill that uses public lottery draw data and a local Liuyao-style calculator to produce lottery-themed divination reports for SSQ, DLT, and Mark Six.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eamonnn101](https://clawhub.ai/user/eamonnn101)

### License/Terms of Use:

MIT-0

## Use Case:

External users interested in Chinese traditional divination use this skill to generate entertainment-only lottery-themed reports and number recommendations for SSQ, DLT, or Mark Six. Agents use it by collecting public draw results or user-provided prior numbers, running the bundled calculator, and returning a concise report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated numbers may be mistaken for betting, investment, or financial advice.

Mitigation: Present outputs as entertainment-only cultural divination and include the disclaimer that results are not gambling or investment advice.

Risk: Generic Chinese trigger phrases such as 算一卦 or 排盘 may activate the skill when the user's intent is ambiguous.

Mitigation: Ask for confirmation and the intended lottery type before running the calculator when the request is unclear.

Risk: Incorrect or stale public draw data can affect the generated report.

Mitigation: State the draw source and period used, and ask the user to provide the latest numbers if web retrieval is uncertain.

## Reference(s):

- [六爻基础速查手册 V2.0](artifact/references/liuyao_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Markdown report with optional JSON calculator output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Entertainment-only recommendations depend on public draw data or user-provided prior numbers.]

## Skill Version(s):

2.0.1 (source: server release evidence; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
