## Description:

Analyzes valuation for A-share stocks using Investoday finance data, focusing on PE, PB, PS, PEG, historical percentiles, industry comparison, and valuation-to-fundamentals fit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenneth-bro](https://clawhub.ai/user/kenneth-bro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused agents use this skill to answer A-share valuation questions by identifying a stock and producing a structured valuation report. The report covers valuation level, historical position, fundamental support, and follow-up indicators without giving trading instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake valuation posture for investment advice.

Mitigation: Present outputs as informational analysis and preserve the skill constraints against target buy or sell prices, position sizing, and trade timing.

Risk: Ambiguous finance prompts such as whether a stock is expensive may route into this valuation workflow.

Mitigation: Clarify the user's intent and stock identifier when the request may require financial quality analysis, technical analysis, or another workflow.

Risk: The report depends on public market data returned by the dependent finance-data skill.

Mitigation: State when a dimension lacks data and require numeric evidence for each valuation judgment, including historical period context where applicable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kenneth-bro/skills/investoday-stock-valuation-analysis)
- [ClawHub Publisher Profile](https://clawhub.ai/user/kenneth-bro)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires investoday-finance-data and public A-share market data; avoids target buy or sell prices, trade timing, position sizing, and unsupported valuation claims.]

## Skill Version(s):

1.3.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
