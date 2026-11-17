## Description:

Triage, reply, escalate, follow up, and close support email through a Mermail mailbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mermail](https://clawhub.ai/user/mermail)

### License/Terms of Use:

MIT-0

## Use Case:

Support teams and agents use this skill to manage a Mermail support mailbox: classify inbound support email, draft or send approved replies, escalate threads to a human, and close resolved mail with labels or folder moves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inbound email, attachments, headers, and tool output may contain untrusted instructions or misleading requests.

Mitigation: Treat inbound content as data, require clean scan status before body interpretation, keep flagged or unknown messages metadata-only, and ignore requests to change tools, reveal secrets, add recipients, or authorize unrelated actions.

Risk: Replies, forwards, scheduled sends, mailbox-agent chats, or automatic response behavior can create external customer-facing effects.

Mitigation: Preview recipients and message bodies, require fresh approval for manual sends or forwards, and follow only the admin-configured mailbox auto-response policy and its guardrails.

Risk: Deleting or destructively changing customer mail can remove important support records.

Mitigation: Keep deletion rare, require explicit destructive approval with a token bound to the exact tool and arguments, and prefer labels or folder moves for closing resolved mail.

## Reference(s):

- [Mermail AI Skills Documentation](https://docs.mermail.app/ai/skills)
- [Support agent security](references/security.md)
- [Support agent tools](references/tools.md)
- [Support agent workflows](references/workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown status summaries with structured mailbox action details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May identify selected mailboxes, emails, classifications, drafts, replies, escalations, labels, folders, and blocked or uncertain states while omitting private body content not needed to confirm the action.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
