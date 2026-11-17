## Description:

Outlook / Microsoft mail integration via Maton managed OAuth and a Microsoft Graph-compatible gateway for reading, searching, summarizing, drafting, sending, labeling, moving, and managing Outlook, Hotmail, Live, or Microsoft 365 email through an existing Maton Outlook connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junzhongjunzi](https://clawhub.ai/user/junzhongjunzi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect and manage Outlook-compatible mailboxes through an existing Maton Outlook connection. It supports mailbox triage, message search and reading, draft creation, and confirmed send or mailbox-management actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox content and outgoing message details can be transmitted through the Maton/Microsoft gateway when the skill is configured.

Mitigation: Install only when the user intends to let an agent use the Maton Outlook connection, keep MATON_API_KEY scoped to this integration where possible, and use narrow read queries before expanding access.

Risk: State-changing actions can send, delete, move, or mark messages in the connected mailbox.

Mitigation: Require explicit user confirmation before writes and review the recipient, subject, body, target message, and requested operation before execution.

Risk: Reading full message bodies can expose more sensitive mailbox data than needed for triage.

Mitigation: Prefer small result limits, selected fields, and body previews before fetching full message bodies.

## Reference(s):

- [Outlook Graph / Maton Examples](references/graph-examples.md)
- [ClawHub Skill Page](https://clawhub.ai/junzhongjunzi/skills/maton-outlook)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline API paths, JSON payload examples, and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit JSON responses from helper scripts when an agent runs mailbox read, draft, or send operations.]

## Skill Version(s):

0.1.0 (source: release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
