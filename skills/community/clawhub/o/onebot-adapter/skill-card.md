## Description:

Connect OpenClaw to OneBot protocol for QQ bot integration. Use when receiving or sending QQ messages via NapCat or other OneBot servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gu-heping](https://clawhub.ai/user/gu-heping)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to connect OpenClaw agents to QQ through OneBot-compatible servers such as NapCat, receive message events, and send private or group messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access a configured OneBot server and the associated bot account.

Mitigation: Install only for trusted OneBot endpoints, restrict the token to the minimum required scope, and keep credentials out of shared logs and prompts.

Risk: Incoming QQ private and group message data may be exposed through verbose event logging.

Mitigation: Disable or redact verbose event logging before production use, especially for private messages and group identifiers.

Risk: The skill includes examples and client methods for moderation actions such as message deletion, kicks, bans, and group setting changes.

Mitigation: Require explicit authorization and confirmation before enabling moderation actions or group-setting changes.

Risk: Remote or public OneBot endpoints may expose bot actions if transport or authentication is weak.

Mitigation: Prefer TLS for remote connections and limit endpoint access to trusted hosts.

## Reference(s):

- [OneBot Message Handling](references/message-handling.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes example environment variables, HTTP API calls, WebSocket listener usage, and message-handling patterns.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
