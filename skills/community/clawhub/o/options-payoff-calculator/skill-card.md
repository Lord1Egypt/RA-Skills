## Description:

Builds an interactive options payoff chart for common stock and ETF strategies using delayed market data and modeled premiums.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesentitrader](https://clawhub.ai/user/thesentitrader)

### License/Terms of Use:

MIT-0

## Use Case:

Options users use this skill to compare payoff shapes, breakeven prices, and modeled profit or loss at expiry across common strategies. The chart provides informational context for research and education, not a personalized recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Modeled premiums use end-of-day implied volatility and are not live option quotes or executable prices.

Mitigation: Present them as delayed model estimates and check current market quotes before making decisions.

Risk: A ticker and optional client identifier are sent to the data provider when requesting data.

Mitigation: Review the request data and omit the optional agent name when it is not needed.

Risk: Writing to an existing output filename could replace that file.

Mitigation: Choose a new output filename.

## Reference(s):

- [SentiSense API documentation](https://sentisense.ai/docs/api/#full-sample-responses-with-a-free-key)
- [SentiSense API key setup](https://app.sentisense.ai/get-api-key)
- [SentiSense](https://sentisense.ai)

## Skill Output:

**Output Type(s):** [Files, HTML, Guidance]

**Output Format:** [A self-contained HTML file with an interactive options payoff chart and explanatory notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a delayed market-data snapshot and modeled premiums; renders offline after creation.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
