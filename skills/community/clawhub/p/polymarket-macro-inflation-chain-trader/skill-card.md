## Description:

Three-step macro chain reaction trader for Polymarket that chains commodity pressure through inflation and rate expectations to equity-threshold markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents use this skill to monitor Polymarket macro, monetary, and equity markets, then propose or place conviction-sized trades when its chain-reaction signal detects divergence. It defaults to simulated trading and requires explicit live mode before placing real Polymarket orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket orders with USDC when enabled.

Mitigation: Keep the default simulated mode for review and only pass --live after approving the strategy, credentials, sizing, and market selection.

Risk: The security summary reports incomplete or fail-open financial safeguards before possible live trades.

Mitigation: Review liquidity, spread, open-position, and failure handling behavior before enabling scheduling or live trading.

Risk: The skill depends on unpinned simmer-sdk code.

Mitigation: Pin and review the dependency version before using a live trading key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-macro-inflation-chain-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Console text with trading decisions, order status, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; live trading requires an explicit --live flag.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
