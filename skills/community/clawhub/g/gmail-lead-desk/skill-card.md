## Description:

Gmail Lead Desk helps agents connect Gmail through the AISA gateway, scan unread sales or customer-support leads, summarize threads, draft replies, and archive labeled deals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and customer-support users can use this skill to triage Gmail leads: connect an account, review unread inquiries, produce CRM-ready summaries, create draft replies, and label or archive closed conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gmail account access and mailbox data pass through the AISA gateway.

Mitigation: Install only when that connection is approved, protect AISA_API_KEY, and avoid exposing secrets in shared terminals.

Risk: Email sends, draft sends, label creation, and batch archive actions can change a mailbox or send unintended messages.

Mitigation: Keep draft-only behavior by default, require explicit send confirmation, show To/Cc/subject/body before sending, and show sample message IDs plus counts before batch changes.

Risk: Attachments or confidential mailbox content may expose sensitive information if handled without approval.

Mitigation: Ask for user consent before downloading or uploading attachments and avoid confidential attachments unless the third-party transfer is approved.

Risk: Incorrect Gmail IDs or labels can cause failed operations or modify the wrong messages.

Mitigation: Fetch current tool schemas and label IDs, use Gmail API message/thread/draft/label IDs, and avoid deprecated or disabled Gmail tools unless the user explicitly accepts the risk.

## Reference(s):

- [Gmail Lead Desk on ClawHub](https://clawhub.ai/aisadocs/skills/gmail-lead-desk)
- [AISA](https://aisa.one)
- [Connect Gmail and execute tools](references/connect_and_execute.md)
- [Gmail Lead Desk Workflows](references/workflows.md)
- [Gmail API Gotchas](references/gmail_gotchas.md)
- [Gmail Tool Whitelist](references/tool_whitelist.md)
- [Composio docs - Gmail](https://docs.composio.dev/toolkits/gmail)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and a Gmail OAuth connection; defaults to draft-only email workflows with confirmation for writes.]

## Skill Version(s):

1.0.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
