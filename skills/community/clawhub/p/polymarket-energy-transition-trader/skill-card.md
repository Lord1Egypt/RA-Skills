## Description:

Trades Polymarket prediction markets on EV adoption milestones, solar and wind capacity, nuclear energy restarts, oil price thresholds, and energy policy events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a configurable Polymarket energy-transition trading agent that discovers relevant markets, computes conviction-based trade signals, and can place paper or live orders through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can use real USDC and security evidence says safeguards can fail open or exceed configured financial limits.

Mitigation: Keep the skill in paper mode until safeguards and trade-size validation are reviewed and fixed; use live mode only with explicit approval and narrowly funded credentials.

Risk: The SIMMER_API_KEY grants trading authority.

Mitigation: Use a narrowly scoped Simmer or Polymarket credential and rotate it if exposed.

Risk: The skill depends on simmer-sdk for market access and trade execution.

Mitigation: Pin or review the simmer-sdk dependency before trusting it with live trading authority.

## Reference(s):

- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Console output and agent guidance with configurable environment variables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading unless live mode is explicitly enabled.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
