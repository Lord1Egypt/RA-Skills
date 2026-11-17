## Description:

Connect OpenClaw to OneBot protocol for QQ bot integration. Use when receiving or sending QQ messages via NapCat or other OneBot servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haohaodlam](https://clawhub.ai/user/haohaodlam)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to connect OpenClaw agents to OneBot-compatible QQ bot servers for receiving events, sending private or group messages, and handling common OneBot message patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send QQ private and group messages through the connected bot account.

Mitigation: Use a narrowly scoped token, keep OneBot endpoints on localhost or protected TLS connections, and limit the bot account to approved chats.

Risk: Group moderation examples can kick or ban users if adopted without safeguards.

Mitigation: Require explicit admin checks, approved group allowlists, user confirmation, and audit logging before enabling group-management actions.

Risk: The sample WebSocket listener logs full event payloads that may include private message data.

Mitigation: Avoid full-event logging in production and redact or minimize message, user, and group identifiers in logs.

## Reference(s):

- [OneBot Message Handling](references/message-handling.md)
- [ClawHub skill page](https://clawhub.ai/haohaodlam/skills/onebot-adapter-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent guidance and reusable Python client/listener code for OneBot HTTP and WebSocket workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
