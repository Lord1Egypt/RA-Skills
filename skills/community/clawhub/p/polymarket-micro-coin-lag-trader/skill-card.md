## Description:

Micro-trades altcoin 5-min Up/Down markets when BTC leads with strong directional bias and ETH/SOL/XRP haven't caught up yet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading automation users can use this skill to run a configurable Polymarket micro-trading strategy for short-interval crypto Up/Down markets. It defaults to paper trading and requires an explicit live mode for real USDC trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can spend real USDC through Polymarket.

Mitigation: Run in the default paper mode first, use --live only after review, and set conservative position and trade-size tunables.

Risk: The security review found that live-trading safeguards do not fully match the documented claims.

Mitigation: Do not rely on volume, threshold, or position safeguards as complete controls until they are fixed and independently reviewed.

Risk: SIMMER_API_KEY grants trading authority.

Mitigation: Use a dedicated least-privileged key and keep unrelated secrets out of the same runtime environment.

## Reference(s):

- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Console logs and Simmer SDK trade API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; paper trading is the default and live trading requires --live.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
