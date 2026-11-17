## Description:

Trades F1 Drivers Championship winner markets on Kalshi by using current points standings and Monte Carlo simulation to estimate win probabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to evaluate F1 Drivers Championship Kalshi markets, compare a points-based Monte Carlo model to market prices, and optionally execute paper or live trades when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place and close real Kalshi trades when live mode is enabled.

Mitigation: Keep dry-run mode enabled until trade-size limits, slippage limits, exit thresholds, and fail-closed behavior have been reviewed against the operator's risk tolerance.

Risk: Live trading requires high-value credentials, including SIMMER_API_KEY and SOLANA_PRIVATE_KEY.

Mitigation: Use a dedicated low-balance wallet and API key, restrict credential exposure, and rotate credentials if they may have been exposed.

Risk: The security evidence notes an unpinned trading SDK dependency and weak fail-closed safeguards.

Mitigation: Review or pin simmer-sdk before supplying live credentials, and verify safeguards using paper trading before enabling --live.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-f1-points-model-trader)
- [Simmer Markets skills](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands, configuration parameters, and optional JSON automaton reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to dry-run mode; live trading requires the explicit --live flag and configured credentials.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
