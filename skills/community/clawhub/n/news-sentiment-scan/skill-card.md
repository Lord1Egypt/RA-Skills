## Description:

Generates a headline-based stock news sentiment report with a -10 to +10 score, sentiment thermometer, notable event list, and short operational guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackpipipi](https://clawhub.ai/user/jackpipipi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-monitoring agents can run this skill to generate a quick headline-based sentiment scan for a stock ticker. Treat the result as a supplemental review aid, not as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's financial sentiment claims may overstate its actual coverage.

Mitigation: Treat it as a narrow Yahoo Finance headline sentiment helper and independently check source coverage, dates, and market context.

Risk: Sentiment scores and operation suggestions can be misleading if used as investment signals.

Mitigation: Do not rely on the report for investment decisions without independent source verification and appropriate human review.

Risk: Runtime dependencies can vary across environments.

Mitigation: Install dependencies in an isolated environment with pinned versions where possible.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Console text report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a stock ticker plus optional day range and market argument; sentiment scores are bounded from -10 to +10.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
