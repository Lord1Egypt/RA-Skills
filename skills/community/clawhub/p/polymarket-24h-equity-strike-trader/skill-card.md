## Description:

Trades structural mispricings in equity and stock price-threshold markets by reconstructing implied probability curves across strike levels and detecting monotonicity, range-sum, and bin-sum inconsistencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent scan Polymarket equity strike-ladder markets, identify mathematically inconsistent prices, and optionally place paper or explicitly enabled live trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can commit real USDC through Polymarket.

Mitigation: Use paper mode first and enable --live only after review with tightly limited trading credentials.

Risk: The security summary says live financial automation relies on safeguards the code does not fully enforce.

Mitigation: Do not enable live automation until liquidity filtering, open-position caps, date grouping, and dependency pinning have been reviewed and fixed.

Risk: SIMMER_API_KEY grants trading authority.

Mitigation: Provide only a scoped, low-limit credential and rotate it if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-24h-equity-strike-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, analysis, shell commands, configuration, API calls]

**Output Format:** [Console text and Simmer SDK trade requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live trading requires the explicit --live flag and a SIMMER_API_KEY credential.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
