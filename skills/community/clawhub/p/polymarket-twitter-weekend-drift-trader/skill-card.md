## Description:

Analyzes Polymarket post-count bin markets for weekday/weekend posting-rate drift and uses simmer-sdk to produce paper-by-default trading actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to identify weekend posting-rate drift in Polymarket post-count bin markets and run the strategy in paper mode by default. Operators can explicitly enable live trading after reviewing credentials, dependency trust, and risk controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live-trading safeguards are incomplete enough that real-funds use needs review first.

Mitigation: Use paper mode unless the live risk controls have been reviewed and fixed, then verify market volume, total open-position limits, and min/max trade sizing are enforced before enabling live trading.

Risk: A live-capable SIMMER_API_KEY can authorize real trades.

Mitigation: Keep the credential private, use a limited trading credential, and do not provide a live-capable key to automated environments unless live trading is intentional.

Risk: The skill depends on simmer-sdk for market access and execution.

Mitigation: Pin and review simmer-sdk before providing live credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-twitter-weekend-drift-trader)
- [Simmer Markets skills](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; runtime output is plain text trading logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless --live is passed.]

## Skill Version(s):

0.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
