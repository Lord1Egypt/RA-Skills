## Description:

Trades post-count bin markets by detecting cross-person contagion where one public figure posting heavily causes correlated figures to increase their rate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents use this skill to analyze Polymarket post-count bin markets and place paper-mode trades by default, with live trading only when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket trades when --live is used.

Mitigation: Use paper mode by default and provide only a restricted API key with tight account-level limits unless live behavior has been reviewed.

Risk: The trading SDK dependency is unpinned.

Mitigation: Pin and audit simmer-sdk before using the skill with a live-capable key.

Risk: Volume and open-position safeguards are weaker than documented.

Mitigation: Fix those safeguards or enforce volume and open-position limits independently before live trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-twitter-cross-contagion-trader)
- [Simmer Markets skills](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus plain text execution logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; paper mode is the default, and live trading requires --live.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
