## Description:

Lel Mail lets an agent read configured email inboxes, classify unread messages, queue outbound email, and manage pending outbound messages with Python and shell scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leli1024](https://clawhub.ai/user/leli1024)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to connect an agent to IMAP and SMTP mail workflows, including reading unread messages, requesting user input for replies, queueing outbound email, and reviewing or deleting queued messages before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unread email can trigger persistent memory writes or cross-channel outreach.

Mitigation: Disable automatic memory writes from inbound email and require explicit user approval before notifications or responses.

Risk: Queued outbound email can be sent through configured SMTP accounts.

Mitigation: Require confirmation before enqueueing or sending messages, and review the outgoing queue before the daemon runs.

Risk: The send script has a code-injection risk from an unquoted heredoc.

Mitigation: Fix the heredoc handling before installation and review generated queue entries before sending.

Risk: Mail credentials are stored in the lel-mail configuration file.

Mitigation: Protect the configuration directory with owner-only permissions and prefer a safer secret store over reusable plaintext passwords.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leli1024/skills/lel-mail)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local queue entries under the user's lel-mail configuration directory and may send or classify email when configured.]

## Skill Version(s):

1.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
