## Description:

Use when working through the workspace mailbox protocol under .mailbox, including reading inbox items, composing replies in a private scratch area, and delivering final replies to a reply inbox path for agent-to-agent communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leoustc](https://clawhub.ai/user/leoustc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to exchange workspace mailbox messages between agents, including new requests, replies, channel-aware handling, and private scratch drafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox metadata can steer file writes outside intended inbox locations.

Mitigation: Use the skill only in a sandboxed workspace with trusted mailbox producers, and require canonical path checks under approved .mailbox/inbox roots before copying messages.

Risk: Malformed or duplicate frontmatter can make routing metadata ambiguous.

Mitigation: Reject path traversal, symlinks, duplicate metadata, and newline-bearing frontmatter values before accepting or generating mailbox messages.

Risk: The newer-Markdown override rule can broaden instruction authority.

Mitigation: Remove the override rule or tightly constrain it to explicitly trusted local policy files before broad installation.

## Reference(s):

- [Channel flow example](artifact/references/channel_flow_example.md)
- [New message example](artifact/references/new_message_example.md)
- [Reply flow example](artifact/references/reply_flow_example.md)
- [Reply scratch example](artifact/references/reply_scratch_example.md)
- [Send flow example](artifact/references/send_flow_example.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown mailbox messages with frontmatter, plus inline shell commands and Python helper usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mailbox messages require REQUEST_ID, MESSAGE_TYPE, RECEIVER_INBOX_PATH, and REPLY_INBOX_PATH frontmatter fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
