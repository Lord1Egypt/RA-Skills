## Description:

Message Chunker helps agents split long outbound messages into multiple parts to avoid platform message length limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[as9530272755](https://clawhub.ai/user/as9530272755)

### License/Terms of Use:

MIT-0

## Use Case:

Agents, developers, and operators use this skill when long reports, plans, logs, or messages need to be sent through Feishu, Telegram, Discord, WhatsApp, or similar channels without exceeding single-message limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic chunking can create repeated, out-of-order, or duplicated outbound messages, especially after send-failure retries.

Mitigation: Confirm channel behavior before deployment and consider approval or tighter retry triggers for public or high-volume messaging channels.

Risk: Splitting structured content can reduce readability or break context if sections, tables, or continuation markers are mishandled.

Mitigation: Prefer heading, table, and paragraph boundaries, and review generated chunks before sending important reports or logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/as9530272755/skills/message-chunker)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Segmented plain text or Markdown messages with optional continuation markers and manual chunk markers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default maximum chunk size is 4000 characters; configured to split on headings and tables and include continuation markers.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact config.yaml, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
