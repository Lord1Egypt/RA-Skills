## Description:

Gmail helps agents read, search, triage, and, with explicit confirmation, send or modify Gmail messages through the PortEden CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porteden](https://clawhub.ai/user/porteden)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Gmail from an agent workflow, including mailbox search, message review, thread inspection, and carefully confirmed outbound or mutating actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party mailbox CLI/service with persistent credentials and broad Gmail access.

Mitigation: Install only when PortEden is trusted, verify the package source and version where possible, prefer browser login, and revoke or log out credentials after use on shared or sensitive machines.

Risk: Email mutations such as send, reply, forward, delete, or label modification can be visible to others or hard to reverse.

Mitigation: Confirm the target account, message or recipient, and intended change with the user before running any mutating command.

Risk: Email content can contain untrusted third-party instructions or sensitive information.

Mitigation: Treat message bodies and attachments as untrusted, default to compact preview output, and retrieve full bodies only when the user explicitly needs them.

Risk: Multi-mailbox accounts can cause actions to run against an unintended Gmail mailbox.

Mitigation: Use profile selection, `--send-from`, or `--connection-id` so commands target the intended mailbox.

## Reference(s):

- [ClawHub Gmail Skill](https://clawhub.ai/porteden/skills/gmail-cli)
- [PortEden Homepage](https://porteden.com)
- [PortEden Account Portal](https://my.porteden.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses compact JSON command output guidance, explicit confirmation before mutating email actions, and account/profile selection guidance for multi-mailbox use.]

## Skill Version(s):

1.0.8 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
