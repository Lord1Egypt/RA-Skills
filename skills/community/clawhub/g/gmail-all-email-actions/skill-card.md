## Description:

Enables agents to search, read, send, reply to, forward, and organize Gmail messages, including drafts and attachments, through AgentPMT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to triage Gmail messages, send notifications and replies, manage labels and drafts, and forward messages with attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Gmail access can expose message contents and enable sending or forwarding sensitive email.

Mitigation: Grant access only if appropriate and manually verify recipients, From addresses, BCC, attachments, and forwarded content before execution.

Risk: Mailbox actions can trash messages or permanently delete drafts without clear confirmation controls.

Mitigation: Review the target messages and drafts and explicitly confirm destructive actions before allowing the agent to execute them.

Risk: Unreviewed installation steps can affect the safety of a broad-access Gmail connection.

Mitigation: Prefer the OpenClaw install path or pinned, audited setup commands.

## Reference(s):

- [Gmail - All Email Actions on ClawHub](https://clawhub.ai/agentpmt/skills/gmail-all-email-actions)
- [AgentPMT Gmail marketplace page](https://www.agentpmt.com/marketplace/gmail-all-email-actions)
- [Gmail action schema](artifact/schema.md)
- [AgentPMT account and connection setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown guidance and JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses can include email content, message metadata, draft details, and attachment metadata; some actions change mailbox state.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
