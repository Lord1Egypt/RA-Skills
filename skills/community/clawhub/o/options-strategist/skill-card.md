## Description:

Analyze options chains, compute implied volatility rank, and select optimal multi-leg strategies based on market conditions via the Finskills API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finskills](https://clawhub.ai/user/finskills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze options chains for a ticker, compare volatility conditions, select multi-leg options strategies, and produce trade metrics and risk-management guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticker lookups and the Finskills API key are visible to the Finskills service provider.

Mitigation: Use a scoped API key, follow the provider's key-management guidance, and avoid submitting sensitive account, broker, or personal financial information in prompts.

Risk: Options strategy recommendations may be incorrect, incomplete, stale, or unsuitable for a user's financial situation.

Mitigation: Independently verify market data, calculations, liquidity, fees, assignment risk, and suitability before trading; consult a qualified financial professional when appropriate.

Risk: Options chain quotes, implied volatility, and Greeks may not reflect executable prices or future market conditions.

Mitigation: Treat generated metrics as analytical estimates, confirm live bid/ask data with a trading platform, and size positions according to documented risk limits.

## Reference(s):

- [Options Strategist homepage](https://github.com/finskills/options-strategist)
- [ClawHub skill page](https://clawhub.ai/finskills/skills/options-strategist)
- [Finskills API](https://finskills.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with options strategy analysis, position metrics, Greeks, alternatives, and risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ticker, market outlook, target time horizon, risk tolerance, and Finskills API access for market data.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
