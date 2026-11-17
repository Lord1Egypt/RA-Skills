## Description:

Trades mispricings in precipitation-range markets by reconstructing the implied probability distribution across bins for the same city and period, detecting sum violations and monotonicity breaks on cumulative precipitation markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents can use this skill to analyze Polymarket precipitation range markets, identify distribution-sum or cumulative-monotonicity violations, and submit simulated or live trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket orders using SIMMER_API_KEY, and the evidence security summary reports gaps that could expose funds beyond user expectations.

Mitigation: Keep the skill in paper mode until the client-mode caching issue, volume check, position-limit enforcement, and market-grouping validation are fixed.

Risk: SIMMER_API_KEY is a high-value trading credential.

Mitigation: Use a tightly scoped trading credential with external account limits and avoid enabling live mode until the configured safeguards have been reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/skills/polymarket-24h-precipitation-range-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Analysis, Text, Shell commands, API Calls]

**Output Format:** [Console text with optional simulated or live trading API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and defaults to paper trading unless live mode is explicitly enabled.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
