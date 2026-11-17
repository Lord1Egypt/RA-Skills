## Description:

Enables OpenClaw and Kiro agents to exchange, read, and delete messages through a shared JSON queue file across local, SSH, or shared-storage setups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonerbo](https://clawhub.ai/user/sonerbo)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to coordinate two or more OpenClaw or Kiro instances by passing messages through a shared JSON queue file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shared queue should be treated as untrusted and not private.

Mitigation: Install only where all agents and machines sharing the queue are already trusted, and do not put secrets in messages.

Risk: Messages could be misused if an agent treats queue content as executable instructions.

Mitigation: Use messages for coordination only and review them before acting on any requested operation.

Risk: Concurrent access to the shared JSON file can cause message loss or corruption.

Mitigation: Restrict filesystem or SSH access to the queue file and avoid simultaneous writers when reliable delivery is required.

## Reference(s):

- [Kiro Agent Chat on ClawHub](https://clawhub.ai/sonerbo/skills/kiro-agent-chat)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text, JSON]

**Output Format:** [Markdown guidance with shell command examples and shared JSON queue data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Messages are stored in a user-selected shared JSON file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
