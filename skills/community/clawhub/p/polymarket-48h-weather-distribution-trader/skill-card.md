## Description:

Trades mispricings in weather temperature-bin markets by reconstructing the implied probability distribution across bins for the same city and date, detecting sum violations and monotonicity breaks on cumulative markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to scan Polymarket weather temperature-bin markets, detect distribution-sum and monotonicity inconsistencies, and place paper or explicitly live trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous trading can create unintended real-money exposure if live mode is used or if the live/paper boundary behaves unexpectedly.

Mitigation: Run only in paper mode until the live/paper client caching issue is reviewed and fixed, and require an explicit operator check before using --live.

Risk: Trading safeguards may not fail closed when market context, slippage checks, or supporting services fail.

Mitigation: Treat safeguard errors as trade blockers, test failure paths, and keep position limits small until the fail-closed behavior is verified.

Risk: A high-value SIMMER_API_KEY can authorize trades beyond the intended release scope.

Mitigation: Use a limited trading credential, rotate it regularly, and configure conservative SIMMER_MAX_POSITION, SIMMER_MIN_TRADE, and SIMMER_MAX_POSITIONS values.

Risk: Unpinned dependencies can change trading behavior across installations.

Mitigation: Pin and review simmer-sdk versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-48h-weather-distribution-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Console logs and trade requests produced by a Python trading script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and configurable trading limits; defaults to paper mode unless run with --live.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
