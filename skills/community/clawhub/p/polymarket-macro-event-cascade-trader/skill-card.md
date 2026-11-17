## Description:

Trades second- and third-order effects from nearly resolved Polymarket events by identifying cascade chains and lagging downstream markets before they reprice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and agent operators use this skill to scan Polymarket for nearly resolved macro events, map likely downstream market moves, and execute paper or explicitly enabled live trades with configurable limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real Polymarket trades when live mode is enabled.

Mitigation: Keep the skill in paper mode until trading behavior has been reviewed and deliberately enable live mode only with credentials scoped for the intended account.

Risk: Advertised volume and concurrent-position safeguards are not complete account-level controls.

Mitigation: Use the smallest practical funded account, configure conservative trade limits, and monitor account-level exposure outside the skill.

Risk: The skill depends on simmer-sdk for market access and order execution.

Mitigation: Pin or review the SDK dependency before deployment.

## Reference(s):

- [Polymarket Macro Event Cascade Trader on ClawHub](https://clawhub.ai/diagnostikon/skills/polymarket-macro-event-cascade-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configurable risk parameters and may place simulated or live prediction-market trades depending on runtime flags and credentials.]

## Skill Version(s):

0.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
