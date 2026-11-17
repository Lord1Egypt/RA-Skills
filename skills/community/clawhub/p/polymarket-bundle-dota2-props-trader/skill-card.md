## Description:

Trades bundle inconsistencies across correlated Dota 2 match props on Polymarket by comparing prop probabilities against an action-score consensus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to monitor Dota 2 Polymarket prop bundles, identify action-score inconsistencies, and run a configurable paper or live trading workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence states that promised live-trading safeguards are not fully enforced.

Mitigation: Start in paper mode and do not rely on documented volume or concurrent-position safeguards until they are fixed or enforced by the trading platform or account.

Risk: Live trading uses SIMMER_API_KEY as a high-value credential and can place real Polymarket trades.

Mitigation: Protect the credential, review the skill before enabling live trading, and pin or verify simmer-sdk before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/skills/polymarket-bundle-dota2-props-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text logs with command-line execution and environment-based configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading unless live mode is explicitly enabled.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
