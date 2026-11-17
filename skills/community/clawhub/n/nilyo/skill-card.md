## Description:

Connects an agent to a user's authorized messaging, email, social, and calendar accounts through Nilyo for account actions and realtime event handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arnaudh458](https://clawhub.ai/user/arnaudh458)

### License/Terms of Use:

MIT-0

## Use Case:

Users and their agents can manage authorized messages, posts, email, and calendar events across connected accounts and receive account events through a chosen webhook destination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected accounts expose private communications and allow the agent to act on the user's behalf.

Mitigation: Explain the access before connection, connect only necessary accounts, and revoke access when no longer needed.

Risk: A webhook destination can continuously forward account events to an unintended recipient.

Mitigation: Confirm the destination URL belongs to the user and delete destinations when they are no longer needed.

Risk: Entering mailbox credentials in chat can retain them in conversation history.

Mitigation: Prefer secure connection links; if the user elects to enter credentials in chat, warn them and recommend a revocable app-specific password.

## Reference(s):

- [Nilyo on ClawHub](https://clawhub.ai/arnaudh458/skills/nilyo)
- [Nilyo MCP endpoint](https://nilyo.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration]

**Output Format:** [Conversational text and structured account or event responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authorized actions can send messages, publish posts, and configure persistent event delivery.]

## Skill Version(s):

1.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
