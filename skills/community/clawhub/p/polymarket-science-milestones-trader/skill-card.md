## Description:

Trades Polymarket prediction markets on scientific breakthroughs, Nobel Prizes, physics discoveries, and research milestones using science hype correction and Nobel calendar timing signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading-agent operators use this skill to discover science and research prediction markets, size positions, and execute paper or live Polymarket trades through Simmer. The skill is intended for users who can review market assumptions and manage financial exposure before enabling live trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can create unintended financial exposure.

Mitigation: Keep paper trading as the default, use restricted trading credentials, maintain low balances, and set conservative per-trade and open-position limits before enabling live trading.

Risk: Configured safeguards may not be enforced consistently during live orders.

Mitigation: Require the publisher to pin simmer-sdk and verify that minimum volume, spread, position-size, and live-mode controls are enforced before deployment.

Risk: Long-lived or imported deployments may carry unresolved client-cache risk.

Mitigation: Avoid long-lived or imported use until the client-cache issue identified by the security evidence is fixed.

## Reference(s):

- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/)
- [Simmer SDK GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Console text, configuration values, and trading API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paper trading is the default; live trading requires an explicit live flag and a SIMMER_API_KEY credential.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
