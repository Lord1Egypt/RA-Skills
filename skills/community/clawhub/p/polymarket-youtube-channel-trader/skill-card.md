## Description:

Trades Polymarket YouTube channel markets, including subscriber milestones and view-count races, using simmer-sdk with paper trading by default and real trades only when explicitly run with --live.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced trading automation users use this skill to discover YouTube and creator-related Polymarket markets, compute channel-specific trade signals, and place paper or explicitly enabled live trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real USDC trades, and security evidence says live-trading controls may be under-enforced.

Mitigation: Keep the default paper mode unless live trading has been reviewed, and set conservative SIMMER_MAX_POSITION, SIMMER_MAX_POSITIONS, volume, spread, and threshold values before using --live.

Risk: SIMMER_API_KEY is a high-value trading credential.

Mitigation: Use a narrowly scoped or segregated key where possible and avoid exposing the credential in shared environments.

Risk: Live mode may trade broader YouTube or creator markets than expected.

Mitigation: Review candidate market selection and run in paper mode first to confirm market coverage before enabling live trades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-youtube-channel-trader)
- [Simmer skills homepage](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Configuration guidance]

**Output Format:** [Console text with Simmer trade API calls and environment-based configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live trading requires the --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.2 (source: ClawHub release evidence and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
