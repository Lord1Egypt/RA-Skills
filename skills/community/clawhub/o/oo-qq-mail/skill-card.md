## Description:

Use OOMOL's connected QQ Mail account to read, search, send, update, and delete email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find and read QQ Mail messages, manage folders and read status, download attachments, and send or delete mail through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run unverified remote software without installation approval.

Mitigation: Review and approve a verified CLI installation separately, including its automatic agent-skill synchronization settings.

Risk: Connecting QQ Mail gives OOMOL-mediated access to the mailbox.

Mitigation: Review the connection and its requested access before connecting the account.

Risk: Mail writes can change mailbox state, and destructive actions can remove or move messages.

Mitigation: Confirm the exact payload and effect before writes, and get explicit approval for destructive actions.

## Reference(s):

- [QQ Mail](https://mail.qq.com/)
- [QQ Mail API documentation](https://help.mail.qq.com/detail/0/1087)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Email content and summaries, connector results, and oo CLI commands with JSON payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read mailbox data or change mailbox state; the skill marks writes and destructive actions and requires confirmation before they run.]

## Skill Version(s):

1.0.5 (source: release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
