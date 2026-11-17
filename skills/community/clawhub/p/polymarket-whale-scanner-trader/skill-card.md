## Description:

Scans public Polymarket leaderboards to identify top-performing whale wallets by SmartScore and trade markets where those wallets have high-conviction positions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan public Polymarket whale-trader activity, compare whale consensus with conviction-based market signals, and submit simulated or explicitly live prediction-market trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can place real Polymarket orders, and the security summary flags weak live-trading safeguards.

Mitigation: Use paper mode until the skill is audited, and require explicit approval before running with --live.

Risk: Keyword or title matching can select the wrong market identity.

Mitigation: Require exact market identity matching before enabling live trading or automation.

Risk: A compromised or over-permissioned trading credential could expose funds.

Mitigation: Use a dedicated revocable API key with strict spend limits and no withdrawal permissions.

Risk: Dependency behavior affects trade execution and credential handling.

Mitigation: Pin and review simmer-sdk before providing live credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-whale-scanner-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk source](https://github.com/SpartanLabsXyz/simmer-sdk)
- [predicting.top leaderboard API](https://predicting.top/api/leaderboard)
- [Polymarket data API](https://data-api.polymarket.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text with trade decisions, skip reasons, configuration guidance, and Simmer trade requests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live trading requires an explicit --live flag and a SIMMER_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
