## Description:

IMAP Mailbox (rfc-editor.org). Use this skill for ANY IMAP Mailbox request — reading, creating, updating, and deleting data. Whenever a task involves IMAP Mailbox, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to search, read, organize, and manage messages in a connected IMAP mailbox, including sending and replying to email. It requires the oo CLI and an active mailbox connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute a remote installer whose contents and hosted connector behavior have not been verified.

Mitigation: Install a reviewed, verified oo CLI release yourself and review its automatic bundled-skill synchronization before use.

Risk: Sending, replying, forwarding, marking messages, moving messages, or deleting messages can change mailbox state.

Mitigation: Keep approval requirements for each write or destructive action, and confirm the exact target and effect before execution.

## Reference(s):

- [IMAP RFC 3501](https://www.rfc-editor.org/rfc/rfc3501)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-generic-imap)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Guidance]

**Output Format:** [Markdown instructions with shell command examples, JSON action payloads, and connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected mailbox action; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
