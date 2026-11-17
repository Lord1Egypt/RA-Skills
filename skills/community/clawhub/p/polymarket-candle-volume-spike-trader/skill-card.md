## Description:

Detects cross-coin volume spikes in Polymarket crypto Up or Down markets and trades lagging coins in the next interval when BTC, ETH, SOL, and XRP show same-direction conviction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to monitor short-interval Polymarket crypto markets, detect cross-asset directional spikes, and place paper or live trades through Simmer SDK when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented live-trading safeguards may not be enforced as described.

Mitigation: Keep the default paper mode until the strategy and safeguards are reviewed, and independently verify min-volume and max-open-position behavior before enabling live trading.

Risk: SIMMER_API_KEY grants trading authority for the configured venue.

Mitigation: Use a scoped or limited key when available and protect it as a high-value credential.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-candle-volume-spike-trader)
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/)
- [Simmer SDK GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration, Text]

**Output Format:** [Console text with Simmer SDK trading API calls and environment-based configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trades require the explicit --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
