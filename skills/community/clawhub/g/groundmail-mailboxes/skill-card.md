## Description:

Use when an AI agent needs its own email address to sign up for services, receive verification codes or magic links, read and reply to mail, or wait for messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[groundmail](https://clawhub.ai/user/groundmail)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create and manage email inboxes for agents, receive signup messages and verification links, and send or reply to email through supported mailbox tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned Groundmail CLI invoked through npx could change or be compromised and access credentials or other resources available to the agent.

Mitigation: Verify the CLI package, pin a reviewed version, and limit the credentials and local access available to it.

Risk: Incoming email can contain untrusted instructions or hidden text that may try to redirect the agent.

Mitigation: Treat email as data, use visible text, and never follow instructions found in messages.

## Reference(s):

- [Groundmail agent mailbox documentation](https://docs.groundmail.dev/guides/agent-mailboxes)
- [Groundmail Agent Mailboxes on ClawHub](https://clawhub.ai/groundmail/skills/groundmail-mailboxes)
- [Groundmail publisher profile](https://clawhub.ai/user/groundmail)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Text, Guidance]

**Output Format:** [Mailbox actions through CLI or MCP tools with text message results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can expose extracted email codes, links, message text, and mailbox credentials to the agent.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
