## Description:

Trades post-count bin markets using a Poisson statistical model to predict the most likely bins based on historical posting rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to evaluate Polymarket post-count bin markets with a Poisson cadence model and produce paper or explicitly live trade decisions through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real Polymarket trades when run with --live and supplied with a live-capable Simmer API key.

Mitigation: Keep the skill in paper mode unless the code and dependency have been independently reviewed; do not provide live-capable credentials to unattended runs.

Risk: Server security evidence reports that several documented trading safeguards are not actually enforced in code.

Mitigation: Do not run live until the market-volume check, account-wide position limit, order-size bounds, and live/paper client handling are fixed.

Risk: The skill depends on SIMMER_API_KEY for trading authority.

Mitigation: Store the key only in a controlled secret environment and rotate it if it is exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-twitter-cadence-model-trader)
- [Simmer Markets skills](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and command-line text with trading decisions, skip reasons, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; paper mode is the default and live trading requires --live.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
