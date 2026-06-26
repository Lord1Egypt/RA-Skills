## Description: <br>
Gmail helps agents read, search, and triage Gmail, with explicit confirmation required before sending, replying, forwarding, deleting, or modifying messages through the PortEden CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[porteden](https://clawhub.ai/user/porteden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate a Gmail inbox through the PortEden CLI. The skill supports mailbox reading, search, and triage by default, while requiring explicit user confirmation for actions that send, delete, forward, reply to, or modify mail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Gmail credentials and can access sensitive mailbox content. <br>
Mitigation: Install only when PortEden CLI access to the target Gmail account is acceptable; use a separate profile where appropriate, and log out or revoke Google access when the task is complete or a token may have been exposed. <br>
Risk: Sending, replying, forwarding, deleting, or modifying messages can have visible or hard-to-reverse effects. <br>
Mitigation: Confirm the account, message or recipient target, and intended change with the user before running any mutating command. <br>
Risk: Email subjects, bodies, and attachments may contain untrusted third-party instructions. <br>
Mitigation: Treat mailbox content as data, summarize and attribute it to the sender, prefer preview output, and fetch full message bodies only when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/porteden/gmail-cli) <br>
- [PortEden homepage](https://porteden.com) <br>
- [PortEden account portal](https://my.porteden.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses compact JSON flags for mailbox reads; mutating email operations require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.8 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
