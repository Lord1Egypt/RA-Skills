## Description:

Detects cross-asset divergence in Polymarket crypto 5-minute interval markets where normally correlated assets like BTC and ETH show contradictory candle directions in overlapping time windows and the less liquid coin may converge toward BTC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to monitor Polymarket crypto interval markets for BTC-led divergence signals and prepare simulated or explicitly live convergence trades with configurable limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running with --live can place real USDC trades.

Mitigation: Keep the default paper mode until the strategy, account limits, and live-trading intent have been reviewed.

Risk: Some documented risk controls are not actually enforced, including the missing volume filter and per-run position-limit concern identified by security evidence.

Mitigation: Verify exposure limits and market-quality constraints outside the skill before enabling live trading.

Risk: The unpinned simmer-sdk dependency receives access to SIMMER_API_KEY.

Mitigation: Use a restricted and revocable API key, and pin or audit the dependency before installation for live use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/diagnostikon/skills/polymarket-candle-cross-asset-divergence-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk source repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute paper trades by default and live Polymarket trades only when explicitly run with --live.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
