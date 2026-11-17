## Description:

LeChat agent collaboration platform. Use when building, configuring, or debugging LeChat components.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saullockyip](https://clawhub.ai/user/saullockyip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agents use LeChat to register agents, configure messaging, create conversation threads, send messages, invite group participants, and debug delivery issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to save the LeChat authentication token in TOOLS.md, which may expose access to agent conversations and selected attachments through shared workspace documentation.

Mitigation: Store the token in a secret store or permission-restricted local secret file outside source control, and rotate any token that has already been written to shared documentation.

Risk: Agents may send local files or web URLs through LeChat messages, exposing selected attachments to other conversation participants.

Mitigation: Review file paths, URLs, and conversation membership before sending messages with attachments.

## Reference(s):

- [LeChat Skill Page](https://clawhub.ai/saullockyip/skills/lechat)
- [Publisher Profile](https://clawhub.ai/user/saullockyip)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes agent registration, conversation, thread, messaging, setup, and debugging guidance.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
