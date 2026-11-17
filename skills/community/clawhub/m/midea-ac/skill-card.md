## Description:

Controls Midea air conditioners by checking status, toggling power, and setting temperature, fan speed, operation mode, and auxiliary heat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamanorange](https://clawhub.ai/user/iamanorange)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent control configured Midea air conditioners on a local network, including status checks and common settings changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic use can change the state of real local air conditioners without enough confirmation.

Mitigation: Review before installing and require confirmation for ambiguous or state-changing AC requests.

Risk: Loosely scoped shell command construction can let arbitrary user text influence device or command arguments.

Mitigation: Use argument-based execution with an allowlist of configured device names such as livingroom and bedroom.

## Reference(s):

- [msmart-ng](https://pypi.org/project/msmart-ng)
- [Mijia skill](https://clawhub.ai/hqman/mijia)
- [ClawHub skill page](https://clawhub.ai/iamanorange/skills/midea-ac)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate on configured local device names and may change real air-conditioner state.]

## Skill Version(s):

0.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
