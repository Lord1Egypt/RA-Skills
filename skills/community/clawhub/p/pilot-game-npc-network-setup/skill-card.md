## Description:

Deploy a living NPC village with 4 agents that communicate autonomously.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Game developers and agent engineers use this skill to configure a four-agent NPC village for autonomous character communication, trade, security, and narrative coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs many dependent skills without pinned versions.

Mitigation: Review dependent skills and pin or otherwise verify exact package versions before installation.

Risk: Automatic trust links may be created with under-validated command inputs.

Mitigation: Use a simple validated prefix such as lowercase letters, numbers, and hyphens only, and manually verify each peer identity before accepting trust links.

Risk: Pilot configuration may persist under ~/.pilot.

Mitigation: Run setup from a least-privileged account and review persistent Pilot configuration after setup.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-game-npc-network-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, clawhub, dependent Pilot skills, and a running Pilot daemon.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
