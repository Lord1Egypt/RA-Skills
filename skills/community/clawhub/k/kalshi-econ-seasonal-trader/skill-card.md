## Description:

Trades CPI/inflation markets on Kalshi using documented seasonal patterns in CPI data. Energy costs spike summer, housing adjustments January. Requires SIMMER_API_KEY and simmer-sdk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents use this skill to discover Kalshi CPI/inflation markets, compare market prices against a static seasonal CPI model, and optionally execute bounded trades through Simmer. It defaults to dry-run mode and requires explicit live execution for real USDC exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access high-value trading and wallet credentials.

Mitigation: Use paper mode first, provide a restricted Simmer API key and low-balance wallet, and avoid setting SOLANA_PRIVATE_KEY except in an isolated environment for explicit live runs.

Risk: Live execution can place real USDC trades through the Simmer SDK.

Mitigation: Run without --live for dry-run behavior until strategy parameters, market selection, and account limits have been reviewed.

Risk: The Simmer SDK dependency is not pinned in the artifact metadata.

Mitigation: Pin or verify the installed simmer-sdk version before using real trading credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/skills/kalshi-econ-seasonal-trader)
- [Simmer Skills](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk Repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Console text with optional JSON automaton status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute paper or live trading actions depending on runtime flags and credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
