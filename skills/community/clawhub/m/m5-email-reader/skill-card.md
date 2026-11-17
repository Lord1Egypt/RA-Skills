## Description:

Reads mailbox messages over POP3 SSL in read-only mode, including message counts, recent subjects, full message bodies with attachment metadata, individual messages, and subject keyword search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyun2000](https://clawhub.ai/user/yuyun2000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent inspect a configured mailbox and answer mail-reading requests such as recent mail summaries, message lookup, and subject search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox credentials may be exposed to the agent or stored in persistent configuration.

Mitigation: Use a revocable app password or authorization code, avoid pasting real account passwords into chat, and avoid storing EMAIL_PASS in global OpenClaw configuration.

Risk: Email body text is untrusted content and may contain instructions that conflict with the user's intent.

Mitigation: Treat email content as data to summarize or quote, not instructions for the agent to obey.

Risk: Full-message reads can expose sensitive email bodies and attachment metadata.

Mitigation: Use the skill only with mailboxes the user is comfortable exposing and prefer subject listing before full-message reads.

## Reference(s):

- [Common POP3 Provider Configuration](artifact/references/providers.md)
- [ClawHub Skill Page](https://clawhub.ai/yuyun2000/skills/m5-email-reader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output for agent interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Email bodies may be summarized or truncated by the agent; the script emits JSON for count, subjects, list, read, and search actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
