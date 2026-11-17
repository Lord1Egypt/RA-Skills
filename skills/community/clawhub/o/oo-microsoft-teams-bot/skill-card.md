## Description:

Operate Microsoft Teams Bot to read and manage conversations, channels, and bot messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Teams users and developers use this skill to list channels and conversation members, create conversations, and send, reply to, update, or delete bot messages. It requires the oo CLI and a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to execute downloaded CLI installation code, and the remote installer was not verified in this artifact review.

Mitigation: Review and approve installation separately, preferably using a verified, pinned release.

Risk: Teams requests pass through OOMOL, and the hosted connector was not verified in this artifact review.

Mitigation: Understand the OOMOL routing and retain the documented confirmations before sending, updating, or deleting messages.

## Reference(s):

- [Microsoft Bot Service documentation](https://learn.microsoft.com/en-us/azure/bot-service/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON request payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that send, update, or delete messages require confirmation; responses include connector data and an execution ID.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
