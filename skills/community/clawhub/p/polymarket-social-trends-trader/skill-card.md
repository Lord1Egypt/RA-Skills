## Description:

Trades Polymarket prediction markets on social trend indicators: loneliness indices, mental health policy, drug legalization, and cultural inflection points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to discover social policy and wellbeing prediction markets, compute conviction-adjusted YES/NO trade signals, and run simulated or live orders through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket trades with financial exposure.

Mitigation: Keep the default paper mode unless deliberately enabling live trading; use a limited, revocable SIMMER_API_KEY.

Risk: Security evidence says several advertised financial safety limits are unreliable.

Mitigation: Keep live trading disabled until the risk-control issues are fixed and reviewed.

Risk: The trading dependency is not pinned in the artifact.

Mitigation: Pin or otherwise verify simmer-sdk before trusting the skill with real funds.

## Reference(s):

- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, API calls, Shell commands, Configuration]

**Output Format:** [Console text with simulated or live trade order requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trades require an explicit --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
