## Description:

Detects macro risk regimes (risk-on vs risk-off) by scanning ALL Polymarket categories simultaneously. When crypto drops, geopolitical escalation rises, and commodity stress increases, the regime is risk-off. Trades markets in other categories that have not repriced to the new regime yet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to detect cross-category Polymarket macro regimes and identify lagging markets for simulated or explicitly enabled live trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real USDC trades on Polymarket.

Mitigation: Keep paper mode unless live trading risk is accepted, and use only a limited Simmer or Polymarket key.

Risk: The security summary says live-trading risk controls do not fully match documented safeguards users may rely on.

Mitigation: Review before installing and do not rely on the documented minimum-volume or max-open-position safeguards until the implementation enforces them.

Risk: The Simmer SDK dependency is not pinned in the artifact.

Mitigation: Pin simmer-sdk to a reviewed version before deployment.

## Reference(s):

- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, API calls, configuration, guidance]

**Output Format:** [Plain text logs with Simmer SDK market scans and trade actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live trading requires the explicit --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
