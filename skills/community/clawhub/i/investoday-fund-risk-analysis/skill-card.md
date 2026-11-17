## Description:

Analyzes public fund risk using Investoday finance data, focusing on drawdown, volatility, downside risk, VaR, beta, Sharpe ratio, and risk-return fit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenneth-bro](https://clawhub.ai/user/kenneth-bro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial-analysis agents use this skill to identify a public fund by name or six-digit code, retrieve Investoday market-data metrics, and produce a structured fund risk report. The report is analytical reference only and does not provide subscription, redemption, allocation, or market-timing advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fund names, fund codes, and the original user query may be sent to the Investoday finance-data integration for public market-data lookup.

Mitigation: Confirm users are comfortable sharing those query details with the integration before installing or enabling the skill.

Risk: Users may over-rely on the generated fund-risk analysis as investment advice.

Mitigation: Present outputs as analytical reference only and preserve the skill's restrictions against subscription, redemption, allocation, or market-timing recommendations.

Risk: Risk conclusions can be misleading when market-data fields are missing, time windows are unclear, or different fund types are compared directly.

Mitigation: Require explicit time horizons and numeric evidence where available; state data insufficiency when metrics are unavailable and compare risk metrics within similar fund types or strategies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenneth-bro/skills/investoday-fund-risk-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown fund risk analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires clear time windows and numeric evidence for risk conclusions when data is available; states that data is insufficient when a dimension cannot be judged.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
