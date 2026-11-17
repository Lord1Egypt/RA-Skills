## Description:

Trades mispricings in weather temperature-bin markets by reconstructing the implied probability distribution across bins for the same city and date, detecting sum violations and monotonicity breaks on cumulative markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to scan Polymarket weather temperature-bin markets, identify distribution-sum or cumulative monotonicity violations, and place simulated or explicitly live trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real-money Polymarket trades when run in live mode.

Mitigation: Keep the default paper mode unless live trading is intentional, and use a limited account or API key where possible.

Risk: Documented safeguards may not fully prevent unintended financial exposure.

Mitigation: Review the strategy and tune position size, threshold, spread, volume, and open-position limits before enabling live execution.

Risk: SIMMER_API_KEY grants trading authority.

Mitigation: Store the key securely, restrict access to the runtime, and rotate or revoke it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-24h-weather-distribution-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Console text with market analysis, trade actions, skip reasons, and configuration-driven execution behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket orders require the --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
