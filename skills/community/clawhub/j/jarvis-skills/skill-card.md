## Description:

Control robotic arms and grippers through voice or code using OpenClaw-style robotic movement, force sensing, collision detection, and simulation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aly-joseph](https://clawhub.ai/user/aly-joseph)

### License/Terms of Use:

MIT

## Use Case:

Developers and robotics operators use this skill to connect agent workflows to robotic arm and gripper commands, including movement, grasping, status checks, and simulation-oriented control flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for real robotic arms and grippers, while the provided package lacks the declared implementation file.

Mitigation: Review the local implementation before installation or execution and only use a verified implementation with supervised operation.

Risk: Physical movement could cause harm if workspace, force, or motion limits are missing or misconfigured.

Mitigation: Require explicit operator confirmation for movement, configure workspace and force limits, start in simulation or dry-run mode, and maintain an independent emergency stop.

Risk: Advertised collision detection and safety behavior is not sufficient evidence of safe hardware operation.

Mitigation: Do not rely on those claims until the missing implementation is supplied, reviewed, and validated with the target hardware.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operator-facing robotic control steps, integration examples, and safety guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
