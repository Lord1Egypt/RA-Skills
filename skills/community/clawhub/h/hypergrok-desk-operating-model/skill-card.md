## Description:

How the HyperGrok trading desk works as a team of Grok Bots - roles, seats, shared workspace, evidence standard, approval model and handoff format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Desk leads and specialist trading bots use this operating model to assign ownership, collect and label evidence, manage approval boundaries, and hand work off consistently. It also guides setup and requests that fall outside the normal trade lifecycle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marks the skill suspicious over autonomous high-impact decisions without approval; standing-mandate behavior can affect whether each order requires separate approval.

Mitigation: Before installing, review the standing-mandate behavior and limits for the intended runtime, including whether orders can be placed without per-order approval.

Risk: The security scan is incomplete because several local references were unresolved.

Mitigation: Review the unresolved references and treat the scan as incomplete until their behavior has been assessed.

## Reference(s):

- [ClawHub release](https://clawhub.ai/galleonlabs/skills/hypergrok-desk-operating-model)
- [HyperGrok Trading Desk (project named in attribution)](https://github.com/galleonlabs/hypergrok-trading-desk)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Structured Markdown operating guidance and handoff text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defines roles, approval boundaries, evidence practices, and handoff formats; includes no trading strategy.]

## Skill Version(s):

1.9.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
