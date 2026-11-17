## Description:

Trades Polymarket prediction markets focused on supply chain disruptions, port congestion, shipping delays, commodity prices, and logistics outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover and paper-trade or live-trade Polymarket markets related to supply chain, logistics, shipping, commodity, and demand-disruption events. It is intended for agents that can run the trading script with configured Simmer credentials and tunable risk limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can place real Polymarket orders when a live-capable SIMMER_API_KEY is provided and live mode is enabled.

Mitigation: Use paper mode by default, avoid live-capable credentials unless live trading is intended, and enforce spending and trading limits outside the skill.

Risk: The security review reports that live-trading safeguards are weaker than the documentation suggests.

Mitigation: Review the implemented controls before installation for live trading and validate the configured risk limits in the execution environment.

Risk: The skill depends on simmer-sdk for market access and trade execution.

Mitigation: Review or pin the simmer-sdk dependency before using credentials with trading authority.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-supply-chain-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk source](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text from a Python trading script, plus Markdown setup and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and supports tunable trading limits through SIMMER-prefixed environment variables.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
