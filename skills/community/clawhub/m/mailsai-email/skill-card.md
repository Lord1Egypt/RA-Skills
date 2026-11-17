## Description:

Give your agent a real email address it can send from, receive at, and reply in-thread, with an injection scan on every inbound message and a dry-run sandbox before anything transmits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailsai](https://clawhub.ai/user/mailsai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give an agent a managed mailbox for sending, receiving, and replying to transactional email. It is intended for agent-owned messaging workflows that need test-key sandboxing, inbound prompt-injection signals, and outbound policy checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm MCP server with access to an email API key.

Mitigation: Start with a test key, pin or verify the @mailsai/mcp-server package version before use, and use live keys only for mailboxes and outbound workflows the agent is intended to control.

Risk: Inbound email is untrusted input and may contain prompt-injection attempts.

Mitigation: Treat email content as data, review injection scores and quarantine flags, and require a check before any inbound message can trigger an outbound action.

Risk: Outbound email actions can send real messages from an agent-controlled mailbox.

Mitigation: Use the dry-run sandbox with test keys until a full loop succeeds, then restrict live use to transactional messaging and supported reply workflows.

## Reference(s):

- [Mails.ai documentation](https://mails.ai/docs)
- [Mails.ai](https://mails.ai)
- [ClawHub skill page](https://clawhub.ai/mailsai/skills/mailsai-email)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and MCP tool names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MAILS_API_KEY; MAILS_BASE_URL is optional for non-default API deployments.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
