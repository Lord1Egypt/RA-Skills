## Description:

Trades AI-vs-market divergence on Polymarket only when the gap clears fees, spread, and a configurable safety margin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chasewebb](https://clawhub.ai/user/chasewebb)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to run a scheduled Simmer-based trading strategy that evaluates Polymarket-imported markets and only places trades when the post-cost divergence clears configured thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place automated trades when configured with trading credentials or a live venue.

Mitigation: Keep the default sim venue until results are reviewed, set account-side spending and order limits, and expose only the required API key.

Risk: Weak safety validation could allow unsuitable market conditions or configuration mistakes to reach live trading.

Mitigation: Review or patch validation gaps, backtest before enabling real-money trading, and avoid providing a wallet private key unless it is required.

## Reference(s):

- [Simmer Markets](https://simmer.markets)
- [ClawHub skill page](https://clawhub.ai/chasewebb/skills/polymarket-fee-aware-divergence)

## Skill Output:

**Output Type(s):** [API Calls, Text, Configuration]

**Output Format:** [Console log text and Simmer trade API calls with reasoning strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs on a configurable schedule; trade size, edge thresholds, spread limit, time-to-resolution window, venue, and max trades are controlled by environment variables.]

## Skill Version(s):

0.1.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
