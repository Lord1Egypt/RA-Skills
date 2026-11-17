## Description:

Use the Mailbird MCP server running locally inside the Mailbird email client for email tasks including inbox triage, sending, search, drafts, attachments, and contacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailbirdagent](https://clawhub.ai/user/mailbirdagent)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent work with a local Mailbird mailbox for triage, search, drafting, attachments, folder actions, and user-approved sends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose mailbox contents, attachments, contacts, and draft or send capabilities to an agent.

Mitigation: Install only when agent access to local Mailbird email is intended, keep the mailbox token private, and enable Mailbird's audit log when visibility is needed.

Risk: Forwarding, tunneling, or sharing the local MCP URL or token could expose mailbox access outside the user's machine.

Mitigation: Keep MAILBIRD_MCP_URL on 127.0.0.1 or localhost, do not proxy or port-forward it, and rotate the token immediately if it leaks.

Risk: Write actions can change mailbox state or send email.

Mitigation: Use Mailbird's Allow write actions gate, show drafts to the user, and require explicit approval before any send.

## Reference(s):

- [ClawHub Mailbird skill page](https://clawhub.ai/mailbirdagent/skills/mailbird-mcp)
- [Mailbird website](https://www.getmailbird.com)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown guidance with MCP tool calls and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Mailbird MCP access through MAILBIRD_MCP_URL and MAILBIRD_MCP_TOKEN; write actions and sends require user-controlled gates.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
