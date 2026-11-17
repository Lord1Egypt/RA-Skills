## Description:

Gmail Lead Desk helps agents connect Gmail through the AISA gateway, scan unread sales or support leads, summarize threads, draft template replies, and label or archive completed deals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and customer support users can use this skill to triage Gmail inquiries, prepare CRM-ready thread summaries, draft follow-up replies for review, and archive won deals with labels. It is intended for agent-assisted mailbox workflows where the user remains in control of OAuth, sending, attachments, and mailbox changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires AISA gateway access to the selected Gmail account.

Mitigation: Review OAuth permissions before connecting Gmail, use only the intended mailbox identity, and keep AISA_API_KEY private.

Risk: Drafts or outbound messages could be sent to the wrong recipients or with unreviewed content.

Mitigation: Use the skill's draft-first default, show To/Cc/Bcc/subject/body in full, and send only after explicit user confirmation.

Risk: Mailbox labels or archive operations can modify many messages at once.

Mitigation: List labels before modifying messages, use label IDs rather than display names, show total count and sample message IDs, and confirm before batch changes.

Risk: Attachment handling may expose mailbox contents beyond the user-selected workflow.

Mitigation: Download attachments only after user consent and avoid uploading full mailbox content externally.

Risk: High-volume Gmail operations may hit rate limits or produce partial results.

Mitigation: Limit concurrent thread fetches, reduce batch size when needed, and back off on 429 or user-rate-limit errors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/gmail-lead-desk-aisa-one)
- [AISA](https://aisa.one)
- [Connect Gmail and execute tools](references/connect_and_execute.md)
- [Gmail Lead Desk Workflows](references/workflows.md)
- [Gmail API Gotchas](references/gmail_gotchas.md)
- [Gmail Tool Whitelist](references/tool_whitelist.md)
- [Composio docs - Gmail](https://docs.composio.dev/toolkits/gmail)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, checklists, plain-text email drafts, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Gmail thread summaries, draft previews, suggested next actions, API request examples, and confirmation prompts.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
