## Description:

Inspect Leina robot status and send text notifications through configured channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Leina users use this skill to inspect robot status and send text notifications through configured channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run downloaded code that has not been verified, without a clear approval step.

Mitigation: Review the CLI installation separately and approve a verified version before setup.

Risk: Setup may automatically install additional agent skills.

Mitigation: Review or disable automatic installation of additional agent skills.

Risk: A notification may be sent through the wrong robot or to unintended recipients.

Mitigation: Confirm the robot, recipients, and message before sending notifications.

## Reference(s):

- [Leina](https://leina.ai)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-leina)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON action requests and responses; plain-text notification messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-dependent; inspect the current action schema before submitting a request.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
