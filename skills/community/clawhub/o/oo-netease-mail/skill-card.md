## Description:

NetEase Mail (mail.163.com). Use this skill for ANY NetEase Mail request — reading, creating, updating, and deleting data. Whenever a task involves NetEase Mail, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected NetEase Mail account can use the skill to search and read messages, manage folders and message status, download attachments, and send or reply to email. The skill guides the agent to check each action's schema and obtain confirmation before sending, changing, moving, or deleting mail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can direct the agent to execute an online installer that was not bundled for inspection.

Mitigation: Review and install the oo CLI separately; do not let a mail task trigger setup automatically.

Risk: Sending, replying, forwarding, changing, moving, or deleting mail can affect the connected account.

Mitigation: Confirm the exact action and its payload with the user before making mail changes, and confirm the target before moving or deleting a message.

## Reference(s):

- [NetEase Mail](https://mail.163.com/)
- [oo CLI repository and documentation](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON action requests and responses, with human-readable email and folder information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that send, reply, forward, mark, move, or delete mail can change account state; obtain the required user confirmation before execution.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
