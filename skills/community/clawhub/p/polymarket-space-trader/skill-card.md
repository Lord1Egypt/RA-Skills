## Description:

Trades Polymarket prediction markets on space launches, SpaceX milestones, satellite deployments, Mars missions, and commercial spaceflight outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover and trade space-related Polymarket prediction markets with configurable position sizing, paper-trading defaults, and an explicit live-trading mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can place real Polymarket orders and expose USDC to financial loss.

Mitigation: Use paper mode first, enable live mode only deliberately, restrict account funds, and avoid live-capable keys in automated environments.

Risk: The advertised minimum-volume filter is not currently enforced.

Mitigation: Review candidate markets manually or update the trading logic before relying on the volume threshold for risk control.

Risk: The skill depends on simmer-sdk for market access and trade execution.

Mitigation: Review the dependency source before providing credentials or enabling live trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-space-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with Python execution and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading unless live mode is explicitly enabled.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
