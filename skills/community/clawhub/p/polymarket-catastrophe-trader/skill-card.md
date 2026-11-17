## Description:

Trades Polymarket prediction markets on hurricane seasons, earthquake probabilities, wildfire forecasts, and extreme weather records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents use this skill to discover catastrophe and extreme-weather prediction markets, evaluate conviction using documented hazard and seasonality heuristics, and run paper or live Polymarket trades with configured limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running with --live can submit real Polymarket trades and spend USDC.

Mitigation: Keep the skill in paper mode until review is complete, and use a limited trading key with only the balance and permissions intended for this strategy.

Risk: Some advertised trading safeguards are not actually enforced.

Mitigation: Review and fix the minimum-volume filter and final order-size cap before live use.

Risk: The simmer-sdk dependency can affect trading behavior.

Mitigation: Pin simmer-sdk to a reviewed version before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-catastrophe-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls]

**Output Format:** [Console text from Python execution plus configured paper or live trading actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading and uses --live for real Polymarket trades.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
