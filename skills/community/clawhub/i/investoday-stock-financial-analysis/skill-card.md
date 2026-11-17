## Description:

Analyzes Chinese A-share stock financial quality, including profitability, earnings quality, growth durability, cash flow, leverage, solvency, and financial safety, using Investoday financial data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenneth-bro](https://clawhub.ai/user/kenneth-bro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to generate structured Chinese-language financial analysis reports for A-share stocks from stock names or six-digit stock codes. It is intended for informational financial quality review and explicitly avoids buy or sell advice, target prices, position sizing, and trading timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial analysis could be misread as investment advice or used for trading decisions.

Mitigation: Treat outputs as informational only and preserve the skill constraint against buy or sell advice, target prices, position sizing, and timing recommendations.

Risk: Incomplete or unavailable market data can produce weak or unsupported conclusions.

Mitigation: Require numerical evidence for each conclusion and state that a dimension cannot be judged when data is insufficient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenneth-bro/skills/investoday-stock-financial-analysis)
- [Publisher profile](https://clawhub.ai/user/kenneth-bro)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown financial analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output based on public market data; conclusions require numerical evidence and do not include investment advice.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
