## Description:

Trades mispricings in precipitation-range markets by reconstructing the implied probability distribution across bins for the same city and period, detecting sum violations and monotonicity breaks on cumulative precipitation markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to scan Polymarket precipitation-range markets, identify probability-distribution inconsistencies, and place simulated or explicitly enabled live trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can expose real funds, and the server security summary flags weak live-trading safeguards and market validation.

Mitigation: Use paper mode by default; for live use, require explicit confirmation or strong account-level limits and review the trading logic before enabling real orders.

Risk: A scoped trading API key is required and can authorize trades.

Mitigation: Pin the SDK, protect the API key, and use the least-privileged trading credentials available.

Risk: Incorrectly grouped markets can make probability-distribution checks unreliable.

Mitigation: Verify that compared markets share the exact same event and resolution period before submitting any order.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-48h-precipitation-range-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls]

**Output Format:** [Console logs and Simmer SDK trade requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading unless live execution is explicitly requested.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
