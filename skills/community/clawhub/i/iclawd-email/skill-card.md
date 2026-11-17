## Description:

Get a real email address for your AI agent. Create an inbox, send and receive email, with optional PGP encryption and DID verified identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[karimibadr](https://clawhub.ai/user/karimibadr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give an AI agent a managed email inbox for sending, receiving, searching, and replying to email through the iClawd HTTP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent an authenticated mailbox with authority to send external email, sign up for services, manage webhooks, and delete the inbox.

Mitigation: Require explicit approval for new recipients, service sign-ups, webhook changes, forwarding sensitive content, and inbox deletion.

Risk: Mailbox credentials and private PGP keys could be exposed if direct-chat credential sharing is treated as routine.

Mitigation: Override the credential instructions before use so the agent does not reveal ~/.iclawd/config.md, API keys, or private PGP keys in ordinary chat.

Risk: Mutable remote fetch instructions can change after review.

Mitigation: Install from a pinned, reviewed artifact instead of fetching the live remote skill at runtime.

## Reference(s):

- [iClawd Email ClawHub Page](https://clawhub.ai/karimibadr/skills/iclawd-email)
- [iClawd Website](https://iclawd.email)
- [iClawd Skill and API Documentation](https://iclawd.email/skill)
- [iClawd MCP Endpoint](https://iclawd.email/mcp)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON-RPC and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces email setup guidance, API call patterns, mailbox handling instructions, and credential storage guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
