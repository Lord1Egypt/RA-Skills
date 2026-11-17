## Description:

AgentMail (QQ) enables an agent to operate the agent.qq.com mail service through OOMOL's agent_qq connector for reading, sending, searching, listing, and deleting messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage AgentMail (QQ) mailboxes from an OOMOL-connected account, including listing aliases, searching messages, reading messages, sending messages, and deleting messages. It is intended for agents that need to inspect the live connector schema before running actions and request confirmation before write or destructive operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup includes remote installer commands that could execute unverified code.

Mitigation: Review the installer source and prefer a verified, version-pinned oo CLI installation method with checksum or signature validation.

Risk: Sending messages changes mailbox state and deleting messages moves mail to trash.

Mitigation: Require explicit user approval for the exact payload and target before write or destructive actions.

Risk: Connector action schemas can change over time.

Mitigation: Inspect the live connector schema before constructing each action payload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-agent-qq)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md)
- [AgentMail (QQ) homepage](https://agent.qq.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live connector schema inspection before constructing action payloads.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
