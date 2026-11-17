## Description:

Investment Advisor provides technical, fundamental, sentiment, and combined stock analysis with JSON outputs for agent-generated investment reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michael20070814](https://clawhub.ai/user/michael20070814)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to fetch market data for stock symbols, compute technical and fundamental signals, compare holdings, and turn JSON results into Chinese-language investment analysis reports. Its outputs should support education and research around securities analysis, not automated trading or personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill outputs buy/sell signals, price targets, stop-loss levels, take-profit levels, and position sizes that could be mistaken for personalized financial advice.

Mitigation: Present results as educational analysis, require user review, and avoid acting automatically on recommendations.

Risk: Queried ticker symbols are sent to Eastmoney services when the scripts fetch market, fundamental, and news data.

Mitigation: Disclose third-party data access and avoid querying sensitive or non-public watchlists without user consent.

Risk: Remote market data and news headlines can be incomplete, stale, or misleading.

Mitigation: Cross-check material conclusions against trusted market data before trading or portfolio decisions.

## Reference(s):

- [Investment API Reference](Investment_API_Reference.md)
- [ClawHub skill page](https://clawhub.ai/michael20070814/skills/investment-advisor)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [JSON from command-line scripts, typically interpreted into Chinese-language markdown or text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scores, ratings, buy/sell/hold signals, support and resistance levels, stop-loss and take-profit levels, portfolio comparisons, and position-size suggestions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and target metadata; artifact/package.json reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
