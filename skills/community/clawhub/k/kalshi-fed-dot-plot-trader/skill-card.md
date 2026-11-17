## Description:

Trades Fed rate markets on Kalshi using FOMC dot plot median implied rate path, computes fair probability of cut or hike per meeting, and trades when market prices diverge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate and optionally trade Kalshi Fed rate markets from a dot-plot-implied rate path, with configurable risk limits and a dry-run default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can move real funds, and server security evidence reports unsafe trade scoping and fail-open safeguards that need review before use.

Mitigation: Use dry-run mode or a dedicated low-balance account until exit filtering requires verified strategy ownership and market-context failures block live trades.

Risk: Trading credentials and dependency trust are material because the skill requires SIMMER_API_KEY, SOLANA_PRIVATE_KEY, and simmer-sdk.

Mitigation: Scope credentials to live runs only and pin simmer-sdk to an audited version before providing live credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-fed-dot-plot-trader)
- [Simmer skills homepage](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [CLI output with JSON automaton reports and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run mode is the default; live trading requires the --live flag and configured credentials.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
