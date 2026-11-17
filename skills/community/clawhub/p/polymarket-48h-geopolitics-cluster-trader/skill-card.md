## Description:

Trades logical inconsistencies in geopolitical event clusters on Polymarket by detecting constraint violations and sizing correction trades by conviction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to identify and optionally trade short-horizon geopolitical prediction-market inconsistencies across related Polymarket markets. It defaults to paper trading and requires an explicit live flag before placing real-money Polymarket trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real-money Polymarket trades when run with --live.

Mitigation: Run in simulation by default and enable --live only after reviewing behavior, limiting funded balance, and confirming trading limits.

Risk: SIMMER_API_KEY grants trading authority.

Mitigation: Treat the key as a high-value credential, keep balances tightly limited, and rotate or revoke the key if exposure is suspected.

Risk: Security evidence says live-trading safeguards and dependency controls are not strong enough for unsupervised real-money use.

Mitigation: Address the volume filter, true open-position limits, and dependency pinning or lockfile before unattended live execution.

## Reference(s):

- [Polymarket 48h Geopolitics Cluster Trader on ClawHub](https://clawhub.ai/diagnostikon/skills/polymarket-48h-geopolitics-cluster-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Configuration, API Calls]

**Output Format:** [Console logs and trading API calls, with Markdown documentation and JSON configuration in the skill artifact]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading unless run with --live.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
