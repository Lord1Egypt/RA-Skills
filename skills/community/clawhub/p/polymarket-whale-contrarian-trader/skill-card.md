## Description:

Detects smart money divergence where top-performing whale wallets take positions opposite to retail consensus, then trades with the whales using conviction-boosted sizing when markets are at probability extremes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor Polymarket whale activity, identify contrarian signals against retail consensus, and place paper or live trades through Simmer with configurable risk limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real-money Polymarket trades.

Mitigation: Keep the skill in paper mode unless live trading has been explicitly reviewed and approved.

Risk: Documented safeguards may be missing or flawed.

Mitigation: Review trade-direction parsing and advertised safeguards before enabling live mode.

Risk: The skill depends on simmer-sdk and SIMMER_API_KEY.

Mitigation: Pin and verify the SDK dependency, and scope SIMMER_API_KEY to limited trading permissions and account exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-whale-contrarian-trader)
- [Polymarket leaderboard API](https://predicting.top/api/leaderboard)
- [Polymarket data API](https://data-api.polymarket.com)

## Skill Output:

**Output Type(s):** [text, configuration, API calls]

**Output Format:** [Console text with Simmer SDK trade requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper mode unless live mode is explicitly enabled.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
